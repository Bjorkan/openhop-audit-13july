# BUG-018 — Delivery ACKs use route timeout calculations instead of the 200 ms delay

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Medium** |
| Area | ACK scheduling |
| Affected components | OpenHop Core |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

OpenHop delays a received message ACK using its flood/direct timeout estimator and adds a separate multi-ACK stagger. MeshCore schedules the ordinary text response using TXT_ACK_DELAY, 200 ms, with its own sendAckTo behavior. To fix it, port the exact MeshCore ACK scheduling constants and sendAckTo rules. Keep sender timeout estimation separate from receiver response delay.

## What happens

OpenHop delays a received message ACK using its flood/direct timeout estimator and adds a separate multi-ACK stagger. MeshCore schedules the ordinary text response using TXT_ACK_DELAY, 200 ms, with its own sendAckTo behavior.

## How official MeshCore handles it

For a flood DM, BaseChatMesh sends the PATH return with a 200 ms delay. The direct ACK helper follows firmware-specific scheduling rather than a full route timeout wait.

## How the OpenHop stack handles it

**OpenHop Core:** TextHandler calculates a flood or direct response timeout from estimated airtime and hop count, which can be substantially different.

## What needs to change

Port the exact MeshCore ACK scheduling constants and sendAckTo rules. Keep sender timeout estimation separate from receiver response delay.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/helpers/BaseChatMesh.cpp` L4–L10](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L4-L10) |
| MeshCore | Reference | [`src/helpers/BaseChatMesh.cpp` L236–L243](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L236-L243) |
| OpenHop Core | Affected implementation | [`src/openhop_core/node/handlers/text.py` L115–L185](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/node/handlers/text.py#L115-L185) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/helpers/BaseChatMesh.cpp</code> (L4–L10)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L4-L10)

```cpp
 4 | #ifndef SERVER_RESPONSE_DELAY
 5 |   #define SERVER_RESPONSE_DELAY   300
 6 | #endif
 7 | 
 8 | #ifndef TXT_ACK_DELAY
 9 |   #define TXT_ACK_DELAY     200
10 | #endif
```

</details>

<details>
<summary><strong>MeshCore</strong> — <code>src/helpers/BaseChatMesh.cpp</code> (L236–L243)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L236-L243)

```cpp
236 |       if (packet->isRouteFlood()) {
237 |         // let this sender know path TO here, so they can use sendDirect(), and ALSO encode the ACK
238 |         mesh::Packet* path = createPathReturn(from.id, secret, packet->path, packet->path_len,
239 |                                                 PAYLOAD_TYPE_ACK, (uint8_t *) &ack_hash, 6);
240 |         if (path) sendFloodScoped(from, path, TXT_ACK_DELAY);
241 |       } else {
242 |         sendAckTo(from, ack_hash, 6);
243 |       }
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/node/handlers/text.py</code> (L149–L180)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/node/handlers/text.py#L115-L185)

```python
149 |         if not has_known_path:
150 |             # out_path unknown: flood the discrete ACK so it can reach the sender without a
151 |             # known reverse path (mirrors firmware sendAckTo OUT_PATH_UNKNOWN -> sendFloodScoped;
152 |             # a path-less direct ACK would not be relayed past direct neighbours). The
153 |             # dispatcher applies flood scope at send time.
154 |             ack_packet = PacketBuilder.create_ack_from_bytes(
155 |                 ack_hash, route_type="flood"
156 |             )
157 |             delay_ms = PacketTimingUtils.calc_flood_timeout_ms(airtime(ack_packet))
158 |             self.log(f"FLOOD ACK timing (no out_path) - delay:{delay_ms:.1f}ms")
159 |             return [(ack_packet, delay_ms / 1000.0)]
160 | 
161 |         out_path = bytes(out_path_raw)
162 |         path_hops = PathUtils.get_path_hash_count(out_path_len)
163 |         ack_packet = PacketBuilder.create_ack_from_bytes(
164 |             ack_hash, path=out_path, path_len_encoded=out_path_len
165 |         )
166 |         base_delay_ms = PacketTimingUtils.calc_direct_timeout_ms(
167 |             airtime(ack_packet), path_hops
168 |         )
169 | 
170 |         if self.multi_acks <= 0:
171 |             self.log(
172 |                 f"DIRECT ACK timing (routed) - delay:{base_delay_ms:.1f}ms, hops:{path_hops}"
173 |             )
174 |             return [(ack_packet, base_delay_ms / 1000.0)]
175 | 
176 |         # multi-ack fires at the base delay; the normal ACK is staggered later
177 |         multi_packet = PacketBuilder.create_multi_ack(
178 |             ack_hash, remaining=1, path=out_path, path_len_encoded=out_path_len
179 |         )
180 |         self.log(
```

</details>
