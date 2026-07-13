# BUG-019 — Synchronous text sends wait for the wrong ACK identifier

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **High** |
| Area | ACK correlation |
| Affected components | OpenHop Core |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

The text builder correctly returns MeshCore's expected four-byte delivery-ACK value, but the companion path does not pass it into Dispatcher.send_packet. Dispatcher falls back to Packet.get_crc, a different value, so a real delivery ACK cannot satisfy the synchronous wait. To fix it, thread expected_crc=ack_crc through the node/bridge send APIs or stop using the generic packet wait for text. Add a test where the expected ACK and packet CRC differ and the MeshCore ACK completes the wait.

## What happens

The text builder correctly returns MeshCore's expected four-byte delivery-ACK value, but the companion path does not pass it into Dispatcher.send_packet. Dispatcher falls back to Packet.get_crc, a different value, so a real delivery ACK cannot satisfy the synchronous wait.

## How official MeshCore handles it

composeMsgPacket calculates expected_ack from timestamp, flags, text, and sender public key. sendMessage returns that exact value for correlation.

## How the OpenHop stack handles it

**OpenHop Core:** send_text_message records ack_crc in a separate pending set, then calls _send_packet with only wait_for_ack=True. The dispatcher consequently waits on packet.get_crc().

## What needs to change

Thread expected_crc=ack_crc through the node/bridge send APIs or stop using the generic packet wait for text. Add a test where the expected ACK and packet CRC differ and the MeshCore ACK completes the wait.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/helpers/BaseChatMesh.cpp` L408–L427](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L408-L427) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/base_send.py` L367–L382](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_send.py#L367-L382) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/companion_radio.py` L102–L104](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/companion_radio.py#L102-L104) |
| OpenHop Core | Affected implementation | [`src/openhop_core/node/dispatcher.py` L597–L610](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/node/dispatcher.py#L597-L610) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/helpers/BaseChatMesh.cpp</code> (L408–L427)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L408-L427)

```cpp
408 | mesh::Packet* BaseChatMesh::composeMsgPacket(const ContactInfo& recipient, uint32_t timestamp, uint8_t attempt, const char *text, uint32_t& expected_ack) {
409 |   int text_len = strlen(text);
410 |   if (text_len > MAX_TEXT_LEN) return NULL;
411 |   if (attempt > 3 && text_len > MAX_TEXT_LEN-2) return NULL;
412 | 
413 |   uint8_t temp[5+MAX_TEXT_LEN+1];
414 |   memcpy(temp, &timestamp, 4);   // mostly an extra blob to help make packet_hash unique
415 |   temp[4] = (attempt & 3);
416 |   memcpy(&temp[5], text, text_len + 1);
417 | 
418 |   // calc expected ACK reply
419 |   mesh::Utils::sha256((uint8_t *)&expected_ack, 4, temp, 5 + text_len, self_id.pub_key, PUB_KEY_SIZE);
420 | 
421 |   int len = 5 + text_len;
422 |   if (attempt > 3) {
423 |     temp[len++] = 0;  // null terminator
424 |     temp[len++] = attempt;  // hide attempt number at tail end of payload
425 |   }
426 | 
427 |   return createDatagram(PAYLOAD_TYPE_TXT_MSG, recipient.id, recipient.getSharedSecret(self_id), temp, len);
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/base_send.py</code> (L367–L382)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_send.py#L367-L382)

```python
367 |             pkt, ack_crc = PacketBuilder.create_text_message(
368 |                 contact=proxy,
369 |                 local_identity=self._identity,
370 |                 message=text,
371 |                 attempt=attempt,
372 |                 message_type=msg_type,
373 |                 txt_type=txt_type,
374 |                 timestamp=timestamp,
375 |             )
376 |             self._apply_flood_scope(pkt)
377 |             self._apply_path_hash_mode(pkt)
378 |             effective_wait_ack = wait_for_ack and txt_type != TXT_TYPE_CLI_DATA
379 |             if txt_type != TXT_TYPE_CLI_DATA:
380 |                 self._track_pending_ack(ack_crc)
381 |             if effective_wait_ack:
382 |                 success = await self._send_packet(pkt, wait_for_ack=True)
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/companion_radio.py</code> (L102–L104)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/companion_radio.py#L102-L104)

```python
102 |     async def _send_packet(self, pkt: Packet, wait_for_ack: bool = False) -> bool:
103 |         """Send a packet via the MeshNode dispatcher."""
104 |         return await self.node.dispatcher.send_packet(pkt, wait_for_ack=wait_for_ack)
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/node/dispatcher.py</code> (L597–L610)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/node/dispatcher.py#L597-L610)

```python
597 |         # Set the expected CRC for ACK matching
598 |         if expected_crc is not None:
599 |             self._current_expected_crc = expected_crc
600 |         else:
601 |             self._current_expected_crc = packet.get_crc()
602 | 
603 |         self._log(
604 |             f"Waiting for ACK with CRC {self._current_expected_crc:08X} (timeout: {ACK_TIMEOUT}s)"
605 |         )
606 | 
607 |         try:
608 |             # Wait for the ACK using the event-based system
609 |             ack_received = await self.wait_for_ack(self._current_expected_crc, ACK_TIMEOUT)
610 |             if ack_received:
```

</details>
