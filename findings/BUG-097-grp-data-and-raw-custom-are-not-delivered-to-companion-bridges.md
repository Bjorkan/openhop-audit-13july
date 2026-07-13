# BUG-097 — GRP_DATA and RAW_CUSTOM are not delivered to companion bridges

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **High** |
| Area | Repeater companion packet routing |
| Affected components | OpenHop Repeater |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

PacketRouter has a branch for GRP_TXT but none for GRP_DATA or RAW_CUSTOM. Core CompanionBridge already has handlers for both, but `process_received_packet` is never called for them. To fix it, add explicit route-aware delivery: fan out GRP_DATA to companions that can authenticate the channel, and deliver RAW_CUSTOM when the packet is flood-local or at the final direct hop. Continue forwarding after the local callback where MeshCore does so.

## What happens

PacketRouter has a branch for GRP_TXT but none for GRP_DATA or RAW_CUSTOM. Core CompanionBridge already has handlers for both, but `process_received_packet` is never called for them.

## How official MeshCore handles it

Companion firmware delivers valid group data to the offline/message flow and RAW_CUSTOM to `PUSH_CODE_RAW_DATA` when the packet reaches local processing. This is separate from diagnostic raw-RX logging.

## How the OpenHop stack handles it

**OpenHop Repeater:** The client may see `PUSH_CODE_LOG_RX_DATA` from the raw radio subscription but never receives semantic CHANNEL_DATA_RECV or RAW_DATA events. The packet may still be forwarded, hiding the local feature loss.

## What needs to change

Add explicit route-aware delivery: fan out GRP_DATA to companions that can authenticate the channel, and deliver RAW_CUSTOM when the packet is flood-local or at the final direct hop. Continue forwarding after the local callback where MeshCore does so.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/Mesh.cpp` L215–L235](https://github.com/meshcore-dev/MeshCore/blob/main/src/Mesh.cpp#L215-L235) |
| MeshCore | Reference | [`src/Mesh.cpp` L280–L287](https://github.com/meshcore-dev/MeshCore/blob/main/src/Mesh.cpp#L280-L287) |
| MeshCore | Reference | [`examples/companion_radio/MyMesh.cpp` L793–L810](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L793-L810) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/companion_bridge.py` L140–L158](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/companion_bridge.py#L140-L158) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/companion_bridge.py` L293–L311](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/companion_bridge.py#L293-L311) |
| OpenHop Repeater | Affected implementation | [`repeater/packet_router.py` L389–L620](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/packet_router.py#L389-L620) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/Mesh.cpp</code> (L215–L235)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/Mesh.cpp#L215-L235)

```cpp
215 |     case PAYLOAD_TYPE_GRP_DATA: 
216 |     case PAYLOAD_TYPE_GRP_TXT: {
217 |       int i = 0;
218 |       uint8_t channel_hash = pkt->payload[i++];
219 | 
220 |       uint8_t* macAndData = &pkt->payload[i];   // MAC + encrypted data 
221 |       if (i + 2 >= pkt->payload_len) {
222 |         MESH_DEBUG_PRINTLN("%s Mesh::onRecvPacket(): incomplete data packet", getLogDateTime());
223 |       } else if (!_tables->hasSeen(pkt)) {
224 |         // scan channels DB, for all matching hashes of 'channel_hash' (max 4 matches supported ATM)
225 |         GroupChannel channels[4];
226 |         int num = searchChannelsByHash(&channel_hash, channels, 4);
227 |         // for each matching channel, try to decrypt data
228 |         for (int j = 0; j < num; j++) {
229 |           // decrypt, checking MAC is valid
230 |           uint8_t data[MAX_PACKET_PAYLOAD];
231 |           int len = Utils::MACThenDecrypt(channels[j].secret, data, macAndData, pkt->payload_len - i);
232 |           if (len > 0) {  // success!
233 |             onGroupDataRecv(pkt, pkt->getPayloadType(), channels[j], data, len);
234 |             break;
235 |           }
```

</details>

<details>
<summary><strong>MeshCore</strong> — <code>src/Mesh.cpp</code> (L280–L287)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/Mesh.cpp#L280-L287)

```cpp
280 |     case PAYLOAD_TYPE_RAW_CUSTOM: {
281 |       if (pkt->isRouteDirect() && !_tables->hasSeen(pkt)) {
282 |         onRawDataRecv(pkt);
283 |         //action = routeRecvPacket(pkt);    don't flood route these (yet)
284 |       }
285 |       break;
286 |     }
287 |     case PAYLOAD_TYPE_MULTIPART:
```

</details>

<details>
<summary><strong>MeshCore</strong> — <code>examples/companion_radio/MyMesh.cpp</code> (L793–L810)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L793-L810)

```cpp
793 | void MyMesh::onRawDataRecv(mesh::Packet *packet) {
794 |   if (packet->payload_len + 4 > sizeof(out_frame)) {
795 |     MESH_DEBUG_PRINTLN("onRawDataRecv(), payload_len too long: %d", packet->payload_len);
796 |     return;
797 |   }
798 |   int i = 0;
799 |   out_frame[i++] = PUSH_CODE_RAW_DATA;
800 |   out_frame[i++] = (int8_t)(_radio->getLastSNR() * 4);
801 |   out_frame[i++] = (int8_t)(_radio->getLastRSSI());
802 |   out_frame[i++] = 0xFF; // reserved (possibly path_len in future)
803 |   memcpy(&out_frame[i], packet->payload, packet->payload_len);
804 |   i += packet->payload_len;
805 | 
806 |   if (_serial->isConnected()) {
807 |     _serial->writeFrame(out_frame, i);
808 |   } else {
809 |     MESH_DEBUG_PRINTLN("onRawDataRecv(), data received while app offline");
810 |   }
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/companion_bridge.py</code> (L140–L158)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/companion_bridge.py#L140-L158)

```python
140 | # Raw custom payload handler: fires raw_data_received (PUSH 0x84)
141 | # ---------------------------------------------------------------------------
142 | 
143 | 
144 | class _RawCustomHandler:
145 |     """Handles PAYLOAD_TYPE_RAW_CUSTOM packets; fires raw_data_received(payload, snr, rssi)."""
146 | 
147 |     def __init__(self, bridge: "CompanionBridge") -> None:
148 |         self._bridge = bridge
149 | 
150 |     @staticmethod
151 |     def payload_type() -> int:
152 |         return PAYLOAD_TYPE_RAW_CUSTOM
153 | 
154 |     async def __call__(self, packet: Packet) -> None:
155 |         payload_bytes = bytes(packet.payload) if packet.payload else b""
156 |         snr = packet.get_snr() if hasattr(packet, "get_snr") else getattr(packet, "_snr", 0)
157 |         rssi = packet.rssi if hasattr(packet, "rssi") else getattr(packet, "_rssi", 0)
158 |         await self._bridge._fire_callbacks("raw_data_received", payload_bytes, snr, rssi)
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/companion_bridge.py</code> (L293–L311)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/companion_bridge.py#L293-L311)

```python
293 |     async def process_received_packet(self, packet: Packet) -> None:
294 |         """Process a packet destined for this companion."""
295 |         ptype = packet.get_payload_type()
296 |         route_type = packet.get_route_type()
297 |         is_flood = route_type in (ROUTE_TYPE_FLOOD, ROUTE_TYPE_TRANSPORT_FLOOD)
298 |         self.stats.record_rx(is_flood=is_flood)
299 | 
300 |         handler = self._handlers.get(ptype)
301 |         if handler:
302 |             try:
303 |                 await handler(packet)
304 |             except Exception as e:
305 |                 logger.error("Handler error for type %02X: %s", ptype, e)
306 |         elif ptype == PAYLOAD_TYPE_GRP_DATA:
307 |             try:
308 |                 await self._handle_group_data_packet(packet)
309 |             except Exception as e:
310 |                 logger.error("Group data handler error: %s", e)
311 | 
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/packet_router.py</code> (L577–L593, L600–L616)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/packet_router.py#L389-L620)

```python
577 |                             await bridge.process_received_packet(packet)
578 |                         except Exception as e:
579 |                             logger.debug(f"Companion bridge RESPONSE (final hop) error: {e}")
580 |                 processed_by_injection = True
581 |                 self._record_for_ui(packet, metadata)
582 | 
583 |         elif payload_type == ProtocolRequestHandler.payload_type():
584 |             dest_hash = packet.payload[0] if packet.payload else None
585 |             companion_bridges = self._companion_bridges_for_packet(packet, metadata)
586 |             if dest_hash is not None and dest_hash in companion_bridges:
587 |                 await companion_bridges[dest_hash].process_received_packet(packet)
588 |                 processed_by_injection = True
589 |                 self._record_for_ui(packet, metadata)
590 |             elif self.daemon.protocol_request_helper:
591 |                 handled = await self.daemon.protocol_request_helper.process_request_packet(packet)
592 |                 if handled:
593 |                     processed_by_injection = True
…
600 |                     except Exception as e:
601 |                         logger.debug(f"Companion bridge REQ (final hop) error: {e}")
602 |                 processed_by_injection = True
603 |                 self._record_for_ui(packet, metadata)
604 | 
605 |         elif payload_type == GroupTextHandler.payload_type():
606 |             # GRP_TXT: pass to all companions (they filter by channel); still forward.
607 |             # Policy drop is final and blocks companion delivery.
608 |             companion_bridges = self._companion_bridges_for_packet(packet, metadata)
609 |             if companion_bridges:
610 |                 for bridge in companion_bridges.values():
611 |                     try:
612 |                         await bridge.process_received_packet(packet)
613 |                     except Exception as e:
614 |                         logger.debug(f"Companion bridge GRP_TXT error: {e}")
615 | 
616 |         # Only pass to repeater engine if not already processed by injection
```

</details>
