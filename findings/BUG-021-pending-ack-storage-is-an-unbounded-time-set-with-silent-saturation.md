# BUG-021 — Pending ACK storage is an unbounded-time set with silent saturation

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Low** |
| Area | ACK state |
| Affected components | OpenHop Core |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

OpenHop stores up to 64 ACK values in a set with no timestamp or cyclic replacement. Once full, every new value is silently untracked, and values never expire unless matched or the entire connection resets. To fix it, mirror the eight-slot table and its lifecycle, or implement time-bounded FIFO semantics proven equivalent. Never silently prefer arbitrarily old ACKs over current sends.

## What happens

OpenHop stores up to 64 ACK values in a set with no timestamp or cyclic replacement. Once full, every new value is silently untracked, and values never expire unless matched or the entire connection resets.

## How official MeshCore handles it

MyMesh uses an eight-entry expected-ACK table with entry state and cyclic allocation/expiry behavior appropriate to a constrained pending window.

## How the OpenHop stack handles it

**OpenHop Core:** _track_pending_ack only adds when set size is below MAX_PENDING_ACK_CRCS. It neither removes stale entries nor evicts the oldest.

## What needs to change

Mirror the eight-slot table and its lifecycle, or implement time-bounded FIFO semantics proven equivalent. Never silently prefer arbitrarily old ACKs over current sends.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`examples/companion_radio/MyMesh.h` L245–L250](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.h#L245-L250) |
| MeshCore | Reference | [`examples/companion_radio/MyMesh.cpp` L411–L424](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L411-L424) |
| MeshCore | Reference | [`examples/companion_radio/MyMesh.cpp` L1099–L1103](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L1099-L1103) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/base_send.py` L1035–L1045](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_send.py#L1035-L1045) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>examples/companion_radio/MyMesh.h</code> (L245–L250)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.h#L245-L250)

```cpp
245 |     uint32_t ack;
246 |     ContactInfo* contact;
247 |   };
248 |   #define EXPECTED_ACK_TABLE_SIZE 8
249 |   AckTableEntry expected_ack_table[EXPECTED_ACK_TABLE_SIZE]; // circular table
250 |   int next_ack_idx;
```

</details>

<details>
<summary><strong>MeshCore</strong> — <code>examples/companion_radio/MyMesh.cpp</code> (L411–L424)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L411-L424)

```cpp
411 | ContactInfo*  MyMesh::processAck(const uint8_t *data) {
412 |   // see if matches any in a table
413 |   for (int i = 0; i < EXPECTED_ACK_TABLE_SIZE; i++) {
414 |     if (memcmp(data, &expected_ack_table[i].ack, 4) == 0) { // got an ACK from recipient
415 |       out_frame[0] = PUSH_CODE_SEND_CONFIRMED;
416 |       memcpy(&out_frame[1], data, 4);
417 |       uint32_t trip_time = _ms->getMillis() - expected_ack_table[i].msg_sent;
418 |       memcpy(&out_frame[5], &trip_time, 4);
419 |       _serial->writeFrame(out_frame, 9);
420 | 
421 |       // NOTE: the same ACK can be received multiple times!
422 |       expected_ack_table[i].ack = 0; // clear expected hash, now that we have received ACK
423 |       return expected_ack_table[i].contact;
424 |     }
```

</details>

<details>
<summary><strong>MeshCore</strong> — <code>examples/companion_radio/MyMesh.cpp</code> (L1099–L1103)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L1099-L1103)

```cpp
1099 |         if (expected_ack) {
1100 |           expected_ack_table[next_ack_idx].msg_sent = _ms->getMillis(); // add to circular table
1101 |           expected_ack_table[next_ack_idx].ack = expected_ack;
1102 |           expected_ack_table[next_ack_idx].contact = recipient;
1103 |           next_ack_idx = (next_ack_idx + 1) % EXPECTED_ACK_TABLE_SIZE;
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/base_send.py</code> (L1035–L1045)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_send.py#L1035-L1045)

```python
1035 |     def _track_pending_ack(self, ack_crc: int) -> None:
1036 |         """Track pending ACK CRC for send_confirmed (capped)."""
1037 |         if len(self._pending_ack_crcs) < MAX_PENDING_ACK_CRCS:
1038 |             self._pending_ack_crcs.add(ack_crc)
1039 | 
1040 |     async def _try_confirm_send(self, crc: int) -> bool:
1041 |         """If CRC is pending, discard it and fire send_confirmed. Returns True if fired."""
1042 |         if crc not in self._pending_ack_crcs:
1043 |             return False
1044 |         self._pending_ack_crcs.discard(crc)
1045 |         await self._fire_callbacks("send_confirmed", crc)
```

</details>
