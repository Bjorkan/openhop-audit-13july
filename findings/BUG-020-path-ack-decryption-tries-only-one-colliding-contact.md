# BUG-020 — PATH ACK decryption tries only one colliding contact

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Medium** |
| Area | PATH and ACK parsing |
| Affected components | OpenHop Core |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

PATH packets carry a one-byte source hash. Multiple contacts can share it. OpenHop selects one contact and gives up if its HMAC fails, so ACKs from any other colliding contact are lost. To fix it, enumerate all contacts with the source prefix and attempt authenticated decryption for each, stopping only on a valid MAC. Use the matched full public key for subsequent state updates.

## What happens

PATH packets carry a one-byte source hash. Multiple contacts can share it. OpenHop selects one contact and gives up if its HMAC fails, so ACKs from any other colliding contact are lost.

## How official MeshCore handles it

MeshCore contact-response handling resolves the encrypted packet against matching identities rather than treating a one-byte prefix as unique; the valid shared secret determines the sender.

## How the OpenHop stack handles it

**OpenHop Core:** _try_decrypt_encrypted_ack calls _find_contact_by_hash, receives one candidate, and attempts only that candidate's secret.

## What needs to change

Enumerate all contacts with the source prefix and attempt authenticated decryption for each, stopping only on a valid MAC. Use the matched full public key for subsequent state updates.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/Mesh.cpp` L126–L180](https://github.com/meshcore-dev/MeshCore/blob/main/src/Mesh.cpp#L126-L180) |
| OpenHop Core | Affected implementation | [`src/openhop_core/node/handlers/ack.py` L102–L150](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/node/handlers/ack.py#L102-L150) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/Mesh.cpp</code> (L135–L151, L159–L175)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/Mesh.cpp#L126-L180)

```cpp
135 |       if (i + CIPHER_MAC_SIZE >= pkt->payload_len) {
136 |         MESH_DEBUG_PRINTLN("%s Mesh::onRecvPacket(): incomplete data packet", getLogDateTime());
137 |       } else if (!_tables->hasSeen(pkt)) {
138 |         // NOTE: this is a 'first packet wins' impl. When receiving from multiple paths, the first to arrive wins.
139 |         //       For flood mode, the path may not be the 'best' in terms of hops.
140 |         // FUTURE: could send back multiple paths, using createPathReturn(), and let sender choose which to use(?)
141 | 
142 |         if (self_id.isHashMatch(&dest_hash)) {
143 |           // scan contacts DB, for all matching hashes of 'src_hash' (max 4 matches supported ATM)
144 |           int num = searchPeersByHash(&src_hash);
145 |           // for each matching contact, try to decrypt data
146 |           bool found = false;
147 |           for (int j = 0; j < num; j++) {
148 |             uint8_t secret[PUB_KEY_SIZE];
149 |             getPeerSharedSecret(secret, j);
150 | 
151 |             // decrypt, checking MAC is valid
…
159 |                 uint8_t hash_count = path_len & 63;
160 |                 uint8_t* path = &data[k]; k += hash_size*hash_count;
161 |                 uint8_t extra_type = data[k++] & 0x0F;   // upper 4 bits reserved for future use
162 |                 uint8_t* extra = &data[k];
163 |                 uint8_t extra_len = len - k;   // remainder of packet (may be padded with zeroes!)
164 |                 if (onPeerPathRecv(pkt, j, secret, path, path_len, extra_type, extra, extra_len)) {
165 |                   if (pkt->isRouteFlood()) {
166 |                     // send a reciprocal return path to sender, but send DIRECTLY!
167 |                     mesh::Packet* rpath = createPathReturn(&src_hash, secret, pkt->path, pkt->path_len, 0, NULL, 0);
168 |                     if (rpath) sendDirect(rpath, path, path_len, 500);
169 |                   }
170 |                 }
171 |               } else {
172 |                 onPeerDataRecv(pkt, pkt->getPayloadType(), j, secret, data, len);
173 |               }
174 |               found = true;
175 |               break;
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/node/handlers/ack.py</code> (L102–L114, L141–L150)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/node/handlers/ack.py#L102-L150)

```python
102 |             # dest_hash = payload[0]  # Not currently used
103 |             src_hash = payload[1]
104 | 
105 |             # Find contact for decryption
106 |             contact = await self.dispatcher._find_contact_by_hash(src_hash)
107 |             if not contact:
108 |                 return None
109 | 
110 |             from ...protocol import CryptoUtils, Identity
111 | 
112 |             peer_id = Identity(bytes.fromhex(contact.public_key))
113 |             shared_secret = peer_id.calc_shared_secret(
114 |                 self.dispatcher.local_identity.get_private_key()
…
141 |             return None
142 | 
143 |     async def _process_bundled_ack_in_path(self, payload: bytes) -> Optional[int]:
144 |         """Process bundled ACKs in returned path messages according to protocol spec."""
145 |         if len(payload) < 1:
146 |             return None
147 | 
148 |         path_length = payload[0]
149 |         path_byte_len = PathUtils.get_path_byte_len(path_length)
150 | 
```

</details>
