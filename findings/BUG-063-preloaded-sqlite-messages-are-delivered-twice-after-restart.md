# BUG-063 — Preloaded SQLite messages are delivered twice after restart

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Medium** |
| Area | Repeater companion persistence |
| Affected components | OpenHop Repeater |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

At startup, `main` reads `companion_load_messages` and pushes the rows into `bridge.message_queue` without deleting or marking the SQLite rows. To fix it, choose one authoritative queue. Recommended: do not preload payloads into memory; use SQLite as the FIFO source and use count or peek for waiting status. Alternatively, move rows atomically into memory and delete them in the same startup transaction.

## What happens

At startup, `main` reads `companion_load_messages` and pushes the rows into `bridge.message_queue` without deleting or marking the SQLite rows. `SYNC_NEXT_MESSAGE` drains the in-memory queue first; when that queue becomes empty, the frame server calls `companion_pop_message` and retrieves the same rows from SQLite again.

## How official MeshCore handles it

Official MeshCore has one offline FIFO. `getFromOfflineQueue` copies the oldest frame and removes it from that queue before `CMD_SYNC_NEXT_MESSAGE` sends the response. A frame therefore has one owner and cannot be returned again after it has been delivered.

## How the OpenHop stack handles it

**OpenHop Repeater:** After restart, every preloaded message is delivered first from memory and then a second time from the database. `PUSH_CODE_MSG_WAITING` and client history can also become inconsistent or duplicated.

## What needs to change

Choose one authoritative queue. Recommended: do not preload payloads into memory; use SQLite as the FIFO source and use count or peek for waiting status. Alternatively, move rows atomically into memory and delete them in the same startup transaction. Test N messages, restart, and verify exactly N unique sync responses.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference single-owner FIFO removal | [`examples/companion_radio/MyMesh.cpp` L243–L254](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L243-L254) |
| MeshCore | Reference SYNC_NEXT_MESSAGE handling | [`examples/companion_radio/MyMesh.cpp` L1354–L1364](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L1354-L1364) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/message_queue.py` L30–L47](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/message_queue.py#L30-L47) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/base_send.py` L1048–L1050](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_send.py#L1048-L1050) |
| OpenHop Repeater | Affected implementation | [`repeater/main.py` L647–L669](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/main.py#L647-L669) |
| OpenHop Repeater | Affected implementation | [`repeater/companion/frame_server.py` L82–L111](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/companion/frame_server.py#L82-L111) |
| OpenHop Repeater | Affected implementation | [`repeater/data_acquisition/sqlite_handler.py` L2648–L2664](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/data_acquisition/sqlite_handler.py#L2648-L2664) |
| OpenHop Repeater | Affected implementation | [`repeater/data_acquisition/sqlite_handler.py` L2728–L2749](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/data_acquisition/sqlite_handler.py#L2728-L2749) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>examples/companion_radio/MyMesh.cpp</code> (L243–L254)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L243-L254)

```cpp
243 | int MyMesh::getFromOfflineQueue(uint8_t frame[]) {
244 |   if (offline_queue_len > 0) {         // check offline queue
245 |     size_t len = offline_queue[0].len; // take from top of queue
246 |     memcpy(frame, offline_queue[0].buf, len);
247 | 
248 |     offline_queue_len--;
249 |     for (int i = 0; i < offline_queue_len; i++) { // delete top item from queue
250 |       offline_queue[i] = offline_queue[i + 1];
251 |     }
252 |     return len;
253 |   }
254 |   return 0; // queue is empty
```

</details>

<details>
<summary><strong>MeshCore</strong> — <code>examples/companion_radio/MyMesh.cpp</code> (L1354–L1364)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L1354-L1364)

```cpp
1354 |   } else if (cmd_frame[0] == CMD_SYNC_NEXT_MESSAGE) {
1355 |     int out_len;
1356 |     if ((out_len = getFromOfflineQueue(out_frame)) > 0) {
1357 |       _serial->writeFrame(out_frame, out_len);
1358 | #ifdef DISPLAY_CLASS
1359 |       if (_ui) _ui->msgRead(offline_queue_len);
1360 | #endif
1361 |     } else {
1362 |       out_frame[0] = RESP_CODE_NO_MORE_MESSAGES;
1363 |       _serial->writeFrame(out_frame, 1);
1364 |     }
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/message_queue.py</code> (L30–L47)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/message_queue.py#L30-L47)

```python
30 |     def push(self, msg: QueuedMessage) -> bool:
31 |         """Add a message to the queue. Returns True on success.
32 | 
33 |         If the queue is at capacity the oldest message is silently dropped.
34 |         """
35 |         self._queue.append(msg)
36 |         return True
37 | 
38 |     def pop(self) -> Optional[QueuedMessage]:
39 |         """Remove and return the oldest message, or None if empty."""
40 |         if self._queue:
41 |             return self._queue.popleft()
42 |         return None
43 | 
44 |     def pop_last(self) -> Optional[QueuedMessage]:
45 |         """Remove and return the most recently pushed message, or None if empty."""
46 |         if self._queue:
47 |             return self._queue.pop()
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/base_send.py</code> (L1048–L1050)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_send.py#L1048-L1050)

```python
1048 |     def sync_next_message(self) -> Optional[QueuedMessage]:
1049 |         """Pop and return the next queued message, or None."""
1050 |         return self.message_queue.pop()
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/main.py</code> (L647–L669)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/main.py#L647-L669)

```python
647 |                     # Preload queued messages from SQLite into bridge, bounded by
648 |                     # offline_queue_size (0 disables offline storage entirely).
649 |                     retention = getattr(bridge.message_queue, "_max_size", None)
650 |                     if retention != 0:
651 |                         for msg_dict in sqlite_handler.companion_load_messages(
652 |                             companion_hash_str, limit=retention or 100
653 |                         ):
654 |                             from openhop_core.companion.models import QueuedMessage
655 | 
656 |                             sk = msg_dict.get("sender_key", b"")
657 |                             if isinstance(sk, str):
658 |                                 sk = bytes.fromhex(sk)
659 |                             bridge.message_queue.push(
660 |                                 QueuedMessage(
661 |                                     sender_key=sk,
662 |                                     txt_type=msg_dict.get("txt_type", 0),
663 |                                     timestamp=msg_dict.get("timestamp", 0),
664 |                                     text=msg_dict.get("text", ""),
665 |                                     is_channel=bool(msg_dict.get("is_channel", False)),
666 |                                     channel_idx=msg_dict.get("channel_idx", 0),
667 |                                     path_len=msg_dict.get("path_len", 0),
668 |                                 )
669 |                             )
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/companion/frame_server.py</code> (L82–L111)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/companion/frame_server.py#L82-L111)

```python
 82 |     def _sync_next_from_persistence(self) -> Optional[QueuedMessage]:
 83 |         """Retrieve next message from SQLite when bridge queue is empty."""
 84 |         if not self.sqlite_handler:
 85 |             return None
 86 |         msg_dict = self.sqlite_handler.companion_pop_message(self.companion_hash)
 87 |         if not msg_dict:
 88 |             return None
 89 |         return QueuedMessage(
 90 |             sender_key=msg_dict.get("sender_key", b""),
 91 |             txt_type=msg_dict.get("txt_type", 0),
 92 |             timestamp=msg_dict.get("timestamp", 0),
 93 |             text=msg_dict.get("text", ""),
 94 |             is_channel=bool(msg_dict.get("is_channel", False)),
 95 |             channel_idx=msg_dict.get("channel_idx", 0),
 96 |             path_len=msg_dict.get("path_len", 0),
 97 |         )
 98 | 
 99 |     # -----------------------------------------------------------------
100 |     # Non-blocking command overrides (keep event loop responsive)
101 |     # -----------------------------------------------------------------
102 | 
103 |     async def _cmd_sync_next_message(self, data: bytes) -> None:
104 |         """Sync next message; run persistence read in thread so SQLite does not block."""
105 |         msg = self.bridge.sync_next_message()
106 |         if msg is None:
107 |             msg = await asyncio.to_thread(self._sync_next_from_persistence)
108 |         if msg is None:
109 |             self._write_frame(bytes([RESP_CODE_NO_MORE_MESSAGES]))
110 |             return
111 |         self._write_frame(self._build_message_frame(msg))
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/data_acquisition/sqlite_handler.py</code> (L2648–L2664)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/data_acquisition/sqlite_handler.py#L2648-L2664)

```python
2648 |     def companion_load_messages(self, companion_hash: str, limit: int = 100) -> List[Dict]:
2649 |         """Load queued messages for a companion (oldest first for queue order)."""
2650 |         try:
2651 |             with self._connect() as conn:
2652 |                 conn.row_factory = sqlite3.Row
2653 |                 cursor = conn.execute(
2654 |                     """
2655 |                     SELECT sender_key, txt_type, timestamp, text, is_channel, channel_idx, path_len
2656 |                     FROM companion_messages WHERE companion_hash = ?
2657 |                     ORDER BY created_at ASC LIMIT ?
2658 |                 """,
2659 |                     (companion_hash, limit),
2660 |                 )
2661 |                 return [dict(row) for row in cursor.fetchall()]
2662 |         except Exception as e:
2663 |             logger.error(f"Failed to load companion messages: {e}")
2664 |             return []
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/data_acquisition/sqlite_handler.py</code> (L2728–L2749)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/data_acquisition/sqlite_handler.py#L2728-L2749)

```python
2728 |     def companion_pop_message(self, companion_hash: str) -> Optional[Dict]:
2729 |         """Remove and return the oldest message from the companion's queue."""
2730 |         try:
2731 |             with self._connect() as conn:
2732 |                 conn.row_factory = sqlite3.Row
2733 |                 cursor = conn.execute(
2734 |                     """
2735 |                     SELECT id, sender_key, txt_type, timestamp, text, is_channel, channel_idx, path_len
2736 |                     FROM companion_messages WHERE companion_hash = ?
2737 |                     ORDER BY created_at ASC LIMIT 1
2738 |                 """,
2739 |                     (companion_hash,),
2740 |                 )
2741 |                 row = cursor.fetchone()
2742 |                 if not row:
2743 |                     return None
2744 |                 msg = dict(row)
2745 |                 conn.execute("DELETE FROM companion_messages WHERE id = ?", (msg["id"],))
2746 |                 conn.commit()
2747 |                 return {k: v for k, v in msg.items() if k != "id"}
2748 |         except Exception as e:
2749 |             logger.error(f"Failed to pop companion message: {e}")
```

</details>
