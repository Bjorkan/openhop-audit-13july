# BUG-036 — Multipart packets and routed ACKs lack their special forwarding paths

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **High** |
| Area | Mesh routing |
| Affected components | OpenHop Repeater |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

MeshCore does not forward multipart data and ACKs like an ordinary directed packet. It updates multipart state and routes embedded/early ACKs specially. OpenHop implements neither receive-forwarding branch. To fix it, port both specialized branches and their dedupe/remaining-count semantics before enabling general direct forwarding. Test ACK propagation through at least one intermediate node and multipart fragments in both directions.

## What happens

MeshCore does not forward multipart data and ACKs like an ordinary directed packet. It updates multipart state and routes embedded/early ACKs specially. OpenHop implements neither receive-forwarding branch.

## How official MeshCore handles it

The direct route code calls forwardMultipartDirect for multipart traffic and routeDirectRecvAcks for ACK traffic, including early ACK notification and no-retransmit safeguards.

## How the OpenHop stack handles it

**OpenHop Repeater:** PacketRouter can deliver ACK and multipart payloads to local handlers, while RepeaterHandler.direct_forward treats every directed packet as a generic path-pop-and-forward operation. The repeater has no MeshCore-equivalent multipart forwarding or routed-ACK branch.

## What needs to change

Port both specialized branches and their dedupe/remaining-count semantics before enabling general direct forwarding. Test ACK propagation through at least one intermediate node and multipart fragments in both directions.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/Mesh.cpp` L67–L107](https://github.com/meshcore-dev/MeshCore/blob/main/src/Mesh.cpp#L67-L107) |
| MeshCore | Reference | [`src/Mesh.cpp` L320–L387](https://github.com/meshcore-dev/MeshCore/blob/main/src/Mesh.cpp#L320-L387) |
| OpenHop Repeater | Affected implementation | [`repeater/packet_router.py` L458–L475](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/packet_router.py#L458-L475) |
| OpenHop Repeater | Affected implementation | [`repeater/packet_router.py` L616–L643](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/packet_router.py#L616-L643) |
| OpenHop Repeater | Affected implementation | [`repeater/engine.py` L980–L1023](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/engine.py#L980-L1023) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/Mesh.cpp</code> (L67–L107)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/Mesh.cpp#L67-L107)

```cpp
 67 |   }
 68 | 
 69 |   if (pkt->isRouteDirect() && pkt->getPayloadType() == PAYLOAD_TYPE_CONTROL && (pkt->payload[0] & 0x80) != 0) {
 70 |     if (pkt->getPathHashCount() == 0) {
 71 |       onControlDataRecv(pkt);
 72 |     }
 73 |     // just zero-hop control packets allowed (for this subset of payloads)
 74 |     return ACTION_RELEASE;
 75 |   }
 76 | 
 77 |   if (pkt->isRouteDirect() && pkt->getPathHashCount() > 0) {
 78 |     // check for 'early received' ACK
 79 |     if (pkt->getPayloadType() == PAYLOAD_TYPE_ACK) {
 80 |       int i = 0;
 81 |       uint32_t ack_crc;
 82 |       memcpy(&ack_crc, &pkt->payload[i], 4); i += 4;
 83 |       if (i <= pkt->payload_len) {
 84 |         onAckRecv(pkt, ack_crc);
 85 |       }
 86 |     }
 87 | 
 88 |     if (self_id.isHashMatch(pkt->path, pkt->getPathHashSize()) && allowPacketForward(pkt)) {
 89 |       if (pkt->getPayloadType() == PAYLOAD_TYPE_MULTIPART) {
 90 |         return forwardMultipartDirect(pkt);
 91 |       } else if (pkt->getPayloadType() == PAYLOAD_TYPE_ACK) {
 92 |         if (!_tables->hasSeen(pkt)) {  // don't retransmit!
 93 |           removeSelfFromPath(pkt);
 94 |           routeDirectRecvAcks(pkt, 0);
 95 |         }
 96 |         return ACTION_RELEASE;
 97 |       }
 98 | 
 99 |       if (!_tables->hasSeen(pkt)) {
100 |         removeSelfFromPath(pkt);
101 | 
102 |         uint32_t d = getDirectRetransmitDelay(pkt);
103 |         return ACTION_RETRANSMIT_DELAYED(0, d);  // Routed traffic is HIGHEST priority 
104 |       }
105 |     }
106 |     return ACTION_RELEASE;   // this node is NOT the next hop (OR this packet has already been forwarded), so discard.
107 |   }
```

</details>

<details>
<summary><strong>MeshCore</strong> — <code>src/Mesh.cpp</code> (L327–L343, L356–L372)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/Mesh.cpp#L320-L387)

```cpp
327 |   }
328 | }
329 | 
330 | DispatcherAction Mesh::routeRecvPacket(Packet* packet) {
331 |   uint8_t n = packet->getPathHashCount();
332 |   if (packet->isRouteFlood() && !packet->isMarkedDoNotRetransmit()
333 |     && (n + 1)*packet->getPathHashSize() <= MAX_PATH_SIZE && allowPacketForward(packet)) {
334 |     // append this node's hash to 'path'
335 |     self_id.copyHashTo(&packet->path[n * packet->getPathHashSize()], packet->getPathHashSize());
336 |     packet->setPathHashCount(n + 1);
337 | 
338 |     uint32_t d = getRetransmitDelay(packet);
339 |     // as this propagates outwards, give it lower and lower priority
340 |     return ACTION_RETRANSMIT_DELAYED(packet->getPathHashCount(), d);   // give priority to closer sources, than ones further away
341 |   }
342 |   return ACTION_RELEASE;
343 | }
…
356 |     if (!_tables->hasSeen(&tmp)) {   // don't retransmit!
357 |       removeSelfFromPath(&tmp);
358 |       routeDirectRecvAcks(&tmp, ((uint32_t)remaining + 1) * 300);  // expect multipart ACKs 300ms apart (x2)
359 |     }
360 |   }
361 |   return ACTION_RELEASE;
362 | }
363 | 
364 | void Mesh::routeDirectRecvAcks(Packet* packet, uint32_t delay_millis) {
365 |   if (!packet->isMarkedDoNotRetransmit()) {
366 |     uint8_t extra = getExtraAckTransmitCount();
367 |     while (extra > 0) {
368 |       delay_millis += getDirectRetransmitDelay(packet) + 300;
369 |       auto a1 = createMultiAck(packet->payload, packet->payload_len, extra);
370 |       if (a1) {
371 |         a1->path_len = Packet::copyPath(a1->path, packet->path, packet->path_len);
372 |         a1->header &= ~PH_ROUTE_MASK;
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/packet_router.py</code> (L458–L475)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/packet_router.py#L458-L475)

```python
458 |             elif self.daemon.login_helper:
459 |                 handled = await self.daemon.login_helper.process_login_packet(packet)
460 |                 if handled:
461 |                     processed_by_injection = True
462 |             if processed_by_injection:
463 |                 self._record_for_ui(packet, metadata)
464 | 
465 |         elif payload_type == AckHandler.payload_type():
466 |             # ACK has no dest in payload (4-byte CRC only); deliver to all bridges so sender sees send_confirmed.
467 |             # Do not set processed_by_injection so packet also reaches engine for DIRECT forwarding when we're a middle hop.
468 |             companion_bridges = self._companion_bridges_for_packet(packet, metadata)
469 |             for bridge in companion_bridges.values():
470 |                 try:
471 |                     await bridge.process_received_packet(packet)
472 |                 except Exception as e:
473 |                     logger.debug(f"Companion bridge ACK error: {e}")
474 | 
475 |         elif payload_type == TextMessageHandler.payload_type():
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/packet_router.py</code> (L616–L643)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/packet_router.py#L616-L643)

```python
616 |         # Only pass to repeater engine if not already processed by injection
617 |         # Skip engine for packets we injected for TX (already sent; avoid double-send/double-count)
618 |         if getattr(packet, "_injected_for_tx", False):
619 |             processed_by_injection = True
620 |         if self.daemon.repeater_handler and not processed_by_injection:
621 |             sent = await self.daemon.repeater_handler(packet, metadata)
622 |             if sent is False:
623 |                 drop_reason = getattr(packet, "_repeater_drop_reason", None)
624 |                 if not isinstance(drop_reason, str):
625 |                     drop_reason = _drop_reason_from_recent_packets(
626 |                         self.daemon.repeater_handler, packet
627 |                     )
628 |                 if _is_expected_drop_reason(drop_reason):
629 |                     logger.debug(
630 |                         "Inbound packet intentionally not transmitted by repeater handler "
631 |                         "(type=%s, header=0x%02x, reason=%s)",
632 |                         payload_type,
633 |                         getattr(packet, "header", 0),
634 |                         drop_reason,
635 |                     )
636 |                 else:
637 |                     logger.warning(
638 |                         "Inbound packet not transmitted by repeater handler "
639 |                         "(type=%s, header=0x%02x, reason=%s)",
640 |                         payload_type,
641 |                         getattr(packet, "header", 0),
642 |                         drop_reason or "unknown",
643 |                     )
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/engine.py</code> (L980–L1023)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/engine.py#L980-L1023)

```python
 980 |     def direct_forward(self, packet: Packet, packet_hash: Optional[str] = None) -> Optional[Packet]:
 981 |         """Forward a DIRECT packet, removing the first hop from the path.
 982 | 
 983 |         INVARIANT: purely synchronous — no await points.  The is_duplicate +
 984 |         mark_seen pair is atomic within the asyncio event loop.  Do NOT add any
 985 |         await here without revisiting that invariant in __call__ / process_packet.
 986 |         """
 987 |         # Validate packet (empty payload, oversized path, etc.)
 988 |         valid, reason = self.validate_packet(packet)
 989 |         if not valid:
 990 |             packet.drop_reason = reason
 991 |             return None
 992 | 
 993 |         # Check if packet is marked do-not-retransmit
 994 |         if packet.is_marked_do_not_retransmit():
 995 |             if not packet.drop_reason:
 996 |                 packet.drop_reason = "Marked do not retransmit"
 997 |             return None
 998 | 
 999 |         hash_size = packet.get_path_hash_size()
1000 |         hop_count = packet.get_path_hash_count()
1001 | 
1002 |         # Check if we're the next hop
1003 |         if not packet.path or len(packet.path) < hash_size:
1004 |             packet.drop_reason = "Direct: no path"
1005 |             return None
1006 | 
1007 |         next_hop = bytes(packet.path[:hash_size])
1008 |         if next_hop != self.local_hash_bytes[:hash_size]:
1009 |             packet.drop_reason = "Direct: not for us"
1010 |             return None
1011 | 
1012 |         # Suppress duplicates — pass pre-computed hash to avoid a second SHA-256.
1013 |         if self.is_duplicate(packet, packet_hash=packet_hash):
1014 |             packet.drop_reason = "Duplicate"
1015 |             return None
1016 | 
1017 |         self.mark_seen(packet, packet_hash=packet_hash)
1018 | 
1019 |         # Remove first hash entry (hash_size bytes)
1020 |         packet.path = bytearray(packet.path[hash_size:])
1021 |         packet.path_len = PathUtils.encode_path_len(hash_size, hop_count - 1)
1022 | 
1023 |         return packet
```

</details>
