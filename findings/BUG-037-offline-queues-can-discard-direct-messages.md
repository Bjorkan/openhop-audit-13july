# BUG-037 — Offline queues can discard direct messages

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Medium** |
| Area | Companion offline messages |
| Affected components | OpenHop Core, OpenHop Repeater |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

Both OpenHop offline queues can delete an existing direct message when they reach capacity. MeshCore protects direct messages by evicting the oldest channel message first and rejecting a new insertion when no channel message can be removed. The same explicit policy is needed in Core memory and Repeater SQLite storage.

## What happens

### OpenHop Core

The core MessageQueue uses `deque(maxlen=...)`, which silently drops the oldest entry at capacity without considering whether it is a protected direct message or lower-priority channel traffic.

### OpenHop Repeater

The SQLite retention query keeps only the newest rows and blindly deletes older overflow, including direct messages. Its behavior therefore disagrees with the protected eviction policy required by the core queue.

## How official MeshCore handles it

### Relevant to OpenHop Core

At capacity, MeshCore replaces the oldest channel message first. If all retained messages are direct contact messages, it refuses the new insertion rather than deleting a direct message.

### Relevant to OpenHop Repeater

Capacity pressure evicts the oldest channel message first and never silently sacrifices an existing direct message.

## How the OpenHop stack handles it

### OpenHop Core

Every push returns success and may invisibly evict the oldest queue element.

### OpenHop Repeater

`companion_push_message` inserts first and then deletes every row outside a newest-N subquery, without inspecting `is_channel`.

## What needs to change

### OpenHop Core

Remove implicit `deque(maxlen)` eviction. Implement explicit insertion that removes the oldest channel message first and returns failure when no evictable channel message exists. Preserve configurable capacity and make callers observe the boolean result. Test channel and direct-message combinations at and above capacity.

### OpenHop Repeater

Perform capacity handling atomically in the insertion transaction. When full, delete the oldest channel row; if none exists, reject the new row and return a visible failure. Ensure the frame-server persistence hook handles rejected insertion without falsely treating the message as safely persisted. Add parity tests against the core queue policy.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`examples/companion_radio/MyMesh.cpp` L219–L241](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L219-L241) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/message_queue.py` L12–L36](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/message_queue.py#L12-L36) |
| OpenHop Repeater | Affected implementation | [`repeater/data_acquisition/sqlite_handler.py` L2666–L2723](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/data_acquisition/sqlite_handler.py#L2666-L2723) |
| OpenHop Repeater | Affected implementation | [`repeater/companion/frame_server.py` L52–L82](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/companion/frame_server.py#L52-L82) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>examples/companion_radio/MyMesh.cpp</code> (L219–L241)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L219-L241)

```cpp
219 | void MyMesh::addToOfflineQueue(const uint8_t frame[], int len) {
220 |   if (offline_queue_len >= OFFLINE_QUEUE_SIZE) {
221 |     MESH_DEBUG_PRINTLN("WARN: offline_queue is full!");
222 |     int pos = 0;
223 |     while (pos < offline_queue_len) {
224 |       if (offline_queue[pos].isChannelMsg()) {
225 |         for (int i = pos; i < offline_queue_len - 1; i++) { // delete oldest channel msg from queue
226 |           offline_queue[i] = offline_queue[i + 1];
227 |         }
228 |         MESH_DEBUG_PRINTLN("INFO: removed oldest channel message from queue.");
229 |         offline_queue[offline_queue_len - 1].len = len;
230 |         memcpy(offline_queue[offline_queue_len - 1].buf, frame, len);
231 |         return;
232 |       }
233 |       pos++;
234 |     }
235 |     MESH_DEBUG_PRINTLN("INFO: no channel messages to remove from queue.");
236 |   } else {
237 |     offline_queue[offline_queue_len].len = len;
238 |     memcpy(offline_queue[offline_queue_len].buf, frame, len);
239 |     offline_queue_len++;
240 |   }
241 | }
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/message_queue.py</code> (L12–L36)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/message_queue.py#L12-L36)

```python
12 | class MessageQueue:
13 |     """Fixed-size offline message queue (FIFO).
14 | 
15 |     Stores incoming messages that arrive when no consumer is actively
16 |     reading. Matches the firmware's offline_queue behaviour with a
17 |     configurable maximum size. When full, the oldest messages are
18 |     silently dropped (deque maxlen behaviour).
19 |     """
20 | 
21 |     def __init__(self, max_size: int = DEFAULT_OFFLINE_QUEUE_SIZE):
22 |         self._queue: deque[QueuedMessage] = deque(maxlen=max_size)
23 |         self._max_size = max_size
24 | 
25 |     @property
26 |     def max_size(self) -> int:
27 |         """Maximum number of messages retained (oldest dropped beyond this)."""
28 |         return self._max_size
29 | 
30 |     def push(self, msg: QueuedMessage) -> bool:
31 |         """Add a message to the queue. Returns True on success.
32 | 
33 |         If the queue is at capacity the oldest message is silently dropped.
34 |         """
35 |         self._queue.append(msg)
36 |         return True
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/data_acquisition/sqlite_handler.py</code> (L2666–L2674, L2701–L2717)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/data_acquisition/sqlite_handler.py#L2666-L2723)

```python
2666 |     def companion_push_message(
2667 |         self, companion_hash: str, msg: Dict, max_messages: Optional[int] = None
2668 |     ) -> bool:
2669 |         """Append a message to the companion's queue.
2670 | 
2671 |         Deduplicates by (companion_hash, packet_hash) using INSERT OR IGNORE
2672 |         backed by the UNIQUE index added in migration 8.  This replaces the
2673 |         previous SELECT + INSERT round-trip (two statements, two SD-card reads)
2674 |         with a single atomic statement.
…
2701 |                         msg.get("channel_idx", 0),
2702 |                         msg.get("path_len", 0),
2703 |                         packet_hash,
2704 |                         time.time(),
2705 |                     ),
2706 |                 )
2707 |                 inserted = cursor.rowcount > 0
2708 |                 if inserted and max_messages is not None:
2709 |                     # Keep the newest `max_messages` rows; drop older overflow.
2710 |                     conn.execute(
2711 |                         """
2712 |                         DELETE FROM companion_messages
2713 |                         WHERE companion_hash = ? AND id NOT IN (
2714 |                             SELECT id FROM companion_messages
2715 |                             WHERE companion_hash = ?
2716 |                             ORDER BY created_at DESC, id DESC
2717 |                             LIMIT ?
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/companion/frame_server.py</code> (L52–L82)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/companion/frame_server.py#L52-L82)

```python
52 |             stats_getter=stats_getter,
53 |             control_handler=control_handler,
54 |         )
55 |         self.sqlite_handler = sqlite_handler
56 | 
57 |     # -----------------------------------------------------------------
58 |     # Persistence hook overrides
59 |     # -----------------------------------------------------------------
60 | 
61 |     async def _persist_companion_message(self, msg_dict: dict) -> None:
62 |         """Persist message to SQLite and pop from bridge queue.
63 | 
64 |         The bridge's ``offline_queue_size`` (``message_queue._max_size``) doubles
65 |         as the SQLite retention limit: 0 disables offline storage entirely, so the
66 |         message is dropped instead of persisted.
67 |         """
68 |         if not self.sqlite_handler:
69 |             return
70 |         retention = getattr(self.bridge.message_queue, "_max_size", None)
71 |         if retention == 0:
72 |             self.bridge.message_queue.pop_last()
73 |             return
74 |         await asyncio.to_thread(
75 |             self.sqlite_handler.companion_push_message,
76 |             self.companion_hash,
77 |             msg_dict,
78 |             retention,
79 |         )
80 |         self.bridge.message_queue.pop_last()
81 | 
82 |     def _sync_next_from_persistence(self) -> Optional[QueuedMessage]:
```

</details>
