# BUG-012 — Group binary data over 165 bytes is accepted

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Low** |
| Area | Group packet construction |
| Affected components | OpenHop Core |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

OpenHop's core send path accepts group data up to 255 bytes, and its companion command gate permits 167. The included MeshCore sendGroupData caps the application data at 165 bytes so the type, length, MAC, and worst-case padded ciphertext fit every packet. To fix it, set the public GRP_DATA limit to 165 and enforce it before building plaintext. Test 165 succeeds and 166 fails without queueing or reporting SENT.

## What happens

OpenHop's core send path accepts group data up to 255 bytes, and its companion command gate permits 167. The included MeshCore sendGroupData caps the application data at 165 bytes so the type, length, MAC, and worst-case padded ciphertext fit every packet. Thus lengths 166–167 can return success only in OpenHop's companion implementation.

## How official MeshCore handles it

MAX_GROUP_DATA_LENGTH is MAX_PACKET_PAYLOAD minus one cipher block and three plaintext metadata bytes, which is 165. BaseChatMesh rejects longer data before packet creation.

## How the OpenHop stack handles it

**OpenHop Core:** send_channel_data checks only len(payload) > 255. The frame handler's MAX_CHANNEL_DATA_LENGTH check is 167, so neither layer enforces the MeshCore group-packet ceiling.

## What needs to change

Set the public GRP_DATA limit to 165 and enforce it before building plaintext. Test 165 succeeds and 166 fails without queueing or reporting SENT.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/MeshCore.h` L21–L21](https://github.com/meshcore-dev/MeshCore/blob/main/src/MeshCore.h#L21-L21) |
| MeshCore | Reference | [`src/helpers/BaseChatMesh.cpp` L496–L524](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L496-L524) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/base_send.py` L439–L475](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_send.py#L439-L475) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/frame_server/commands_messaging.py` L107–L143](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/frame_server/commands_messaging.py#L107-L143) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/MeshCore.h</code> (L21–L21)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/MeshCore.h#L21-L21)

```cpp
21 | #define MAX_GROUP_DATA_LENGTH  (MAX_PACKET_PAYLOAD - CIPHER_BLOCK_SIZE - 3)
```

</details>

<details>
<summary><strong>MeshCore</strong> — <code>src/helpers/BaseChatMesh.cpp</code> (L496–L524)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L496-L524)

```cpp
496 | bool BaseChatMesh::sendGroupData(mesh::GroupChannel& channel, uint8_t* path, uint8_t path_len, uint16_t data_type, const uint8_t* data, int data_len) {
497 |   if (data_len < 0) {
498 |     MESH_DEBUG_PRINTLN("sendGroupData: invalid negative data_len=%d", data_len);
499 |     return false;
500 |   }
501 |   if (data_len > MAX_GROUP_DATA_LENGTH) {
502 |     MESH_DEBUG_PRINTLN("sendGroupData: data_len=%d exceeds max=%d", data_len, MAX_GROUP_DATA_LENGTH);
503 |     return false;
504 |   }
505 | 
506 |   uint8_t temp[3 + MAX_GROUP_DATA_LENGTH];
507 |   temp[0] = (uint8_t)(data_type & 0xFF);
508 |   temp[1] = (uint8_t)(data_type >> 8);
509 |   temp[2] = (uint8_t)data_len;
510 |   if (data_len > 0) memcpy(&temp[3], data, data_len);
511 | 
512 |   auto pkt = createGroupDatagram(PAYLOAD_TYPE_GRP_DATA, channel, temp, 3 + data_len);
513 |   if (pkt == NULL) {
514 |     MESH_DEBUG_PRINTLN("sendGroupData: unable to create group datagram, data_len=%d", data_len);
515 |     return false;
516 |   }
517 | 
518 |   if (path_len == OUT_PATH_UNKNOWN) {
519 |     sendFloodScoped(channel, pkt);
520 |   } else {
521 |     sendDirect(pkt, path, path_len);
522 |   }
523 | 
524 |   return true;
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/base_send.py</code> (L439–L475)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_send.py#L439-L475)

```python
439 |     async def send_channel_data(
440 |         self,
441 |         channel_idx: int,
442 |         data_type: int,
443 |         payload: bytes,
444 |         *,
445 |         path: Optional[bytes] = None,
446 |         path_len_encoded: Optional[int] = None,
447 |     ) -> bool:
448 |         """Send a group binary datagram (PAYLOAD_TYPE_GRP_DATA)."""
449 |         channel = self.channels.get(channel_idx)
450 |         if not channel or data_type <= 0 or data_type > 0xFFFF:
451 |             return False
452 |         payload = bytes(payload or b"")
453 |         if len(payload) > 255:
454 |             return False
455 |         try:
456 |             secret_bytes = bytes(channel.secret or b"")
457 |             if len(secret_bytes) < 32:
458 |                 secret_bytes = secret_bytes + b"\x00" * (32 - len(secret_bytes))
459 |             else:
460 |                 secret_bytes = secret_bytes[:32]
461 | 
462 |             hash_input = (
463 |                 secret_bytes[:16]
464 |                 if len(secret_bytes) >= 32 and secret_bytes[16:32] == b"\x00" * 16
465 |                 else secret_bytes
466 |             )
467 |             channel_hash = hashlib.sha256(hash_input).digest()[0]
468 |             plaintext = struct.pack("<HB", data_type & 0xFFFF, len(payload)) + payload
469 |             pkt = PacketBuilder.create_group_data_packet(
470 |                 PAYLOAD_TYPE_GRP_DATA,
471 |                 channel_hash,
472 |                 secret_bytes,
473 |                 plaintext,
474 |                 secret_bytes,
475 |             )
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/frame_server/commands_messaging.py</code> (L107–L143)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/frame_server/commands_messaging.py#L107-L143)

```python
107 |         path_len = data[1]
108 |         if self.bridge.get_channel(channel_idx) is None:
109 |             self._write_err(ERR_CODE_NOT_FOUND)
110 |             return
111 |         offset = 2
112 |         path = b""
113 |         if path_len != OUT_PATH_UNKNOWN:
114 |             if not PathUtils.is_valid_path_len(path_len):
115 |                 self._write_err(ERR_CODE_ILLEGAL_ARG)
116 |                 return
117 |             path_byte_len = PathUtils.get_path_byte_len(path_len)
118 |             if len(data) < offset + path_byte_len + 2:
119 |                 self._write_err(ERR_CODE_ILLEGAL_ARG)
120 |                 return
121 |             path = data[offset : offset + path_byte_len]
122 |             offset += path_byte_len
123 |         if len(data) < offset + 2:
124 |             self._write_err(ERR_CODE_ILLEGAL_ARG)
125 |             return
126 |         data_type = int.from_bytes(data[offset : offset + 2], "little")
127 |         payload = data[offset + 2 :]
128 |         if data_type == 0 or len(payload) > MAX_CHANNEL_DATA_LENGTH:
129 |             self._write_err(ERR_CODE_ILLEGAL_ARG)
130 |             return
131 |         send_channel_data = getattr(self.bridge, "send_channel_data", None)
132 |         if not send_channel_data:
133 |             self._write_err(ERR_CODE_UNSUPPORTED_CMD)
134 |             return
135 |         ok = await send_channel_data(
136 |             channel_idx,
137 |             data_type,
138 |             payload,
139 |             path=path if path_len != OUT_PATH_UNKNOWN else None,
140 |             path_len_encoded=path_len,
141 |         )
142 |         if ok:
143 |             self._write_ok()
```

</details>
