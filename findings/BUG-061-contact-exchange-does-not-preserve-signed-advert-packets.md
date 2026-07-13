# BUG-061 — Contact exchange does not preserve signed ADVERT packets

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **High** |
| Area | Companion contact exchange |
| Affected components | OpenHop Core, OpenHop Repeater |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

OpenHop exports contacts through a custom unsigned record instead of the original signed MeshCore ADVERT, and the repeater database does not preserve the raw ADVERT across restarts. The stack must use verified raw ADVERT packets for import and export and persist those bytes in SQLite.

## What happens

### OpenHop Core

The core companion API exports contacts through a custom unsigned 73-byte record and imports that record directly into contact storage. This loses the original ADVERT timestamp, flags, signature, application data, and authenticity.

### OpenHop Repeater

The repeater persistence adapter omits `last_advert_packet` when converting contacts to SQLite records. Even after core exports the original signed ADVERT, a daemon restart would discard that packet and make the contact non-exportable in the compatible format.

## How official MeshCore handles it

### Relevant to OpenHop Core

MeshCore exports the stored raw signed ADVERT blob. Import parses that ADVERT and feeds it through normal verification and contact-update handling.

### Relevant to OpenHop Repeater

Persistent contact state retains the signed advert material needed for later contact sharing.

## How the OpenHop stack handles it

### OpenHop Core

The Contact model can carry `last_advert_packet`, but `export_contact` still calls `encode_exported_contact`, and `import_contact` still trusts `decode_exported_contact` instead of verifying an ADVERT packet.

### OpenHop Repeater

`CompanionFrameServer._contact_to_dict` does not include `last_advert_packet`, and the SQLite contact schema/save/load path has no corresponding BLOB field.

## What needs to change

### OpenHop Core

Make the verified raw ADVERT packet the canonical peer-contact export. Return it byte-for-byte for peer exports; parse and authenticate imported data as an ADVERT; pass successful imports through the normal advert/contact update path; reject the custom 73-byte format. Ensure the contact serialization contract exposes `last_advert_packet` so repository-specific persistence can store it.

### OpenHop Repeater

Add a migration-safe nullable BLOB column for the raw ADVERT packet. Include it in single-contact upsert, bulk save, load, and conversion back into the core Contact model. Existing rows may remain null until a new verified advert is received. Add a restart test that receives an advert, persists it, reloads it, and exports exactly the same bytes.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/helpers/BaseChatMesh.cpp` L527–L557](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L527-L557) |
| MeshCore | Reference | [`examples/companion_radio/MyMesh.cpp` L1298–L1353](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L1298-L1353) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/base_contacts.py` L64–L105](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_contacts.py#L64-L105) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/binary_parsing.py` L21–L63](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/binary_parsing.py#L21-L63) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/models.py` L11–L30](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/models.py#L11-L30) |
| OpenHop Repeater | Affected implementation | [`repeater/companion/frame_server.py` L105–L160](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/companion/frame_server.py#L105-L160) |
| OpenHop Repeater | Affected implementation | [`repeater/data_acquisition/sqlite_handler.py` L2370–L2440](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/data_acquisition/sqlite_handler.py#L2370-L2440) |
| OpenHop Repeater | Affected implementation | [`repeater/main.py` L600–L692](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/main.py#L600-L692) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/helpers/BaseChatMesh.cpp</code> (L527–L557)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L527-L557)

```cpp
527 | bool BaseChatMesh::shareContactZeroHop(const ContactInfo& contact) {
528 |   int plen = getBlobByKey(contact.id.pub_key, PUB_KEY_SIZE, temp_buf);  // retrieve last raw advert packet
529 |   if (plen == 0) return false;  // not found
530 | 
531 |   auto packet = obtainNewPacket();
532 |   if (packet == NULL) return false;  // no Packets available
533 | 
534 |   packet->readFrom(temp_buf, plen);  // restore Packet from 'blob'
535 |   uint16_t codes[2];
536 |   codes[0] = codes[1] = 0;   // { 0, 0 } means 'send this nowhere'
537 |   sendZeroHop(packet, codes);
538 |   return true;  // success
539 | }
540 | 
541 | uint8_t BaseChatMesh::exportContact(const ContactInfo& contact, uint8_t dest_buf[]) {
542 |   return getBlobByKey(contact.id.pub_key, PUB_KEY_SIZE, dest_buf);  // retrieve last raw advert packet
543 | }
544 | 
545 | bool BaseChatMesh::importContact(const uint8_t src_buf[], uint8_t len) {
546 |   auto pkt = obtainNewPacket();
547 |   if (pkt) {
548 |     if (pkt->readFrom(src_buf, len) && pkt->getPayloadType() == PAYLOAD_TYPE_ADVERT) {
549 |       pkt->header |= ROUTE_TYPE_FLOOD;   // simulate it being received flood-mode
550 |       getTables()->clear(pkt);  // remove packet hash from table, so we can receive/process it again
551 |       _pendingLoopback = pkt;  // loop-back, as if received over radio
552 |       return true;  // success
553 |     } else {
554 |       releasePacket(pkt);   // undo the obtainNewPacket()
555 |     }
556 |   }
557 |   return false; // error
```

</details>

<details>
<summary><strong>MeshCore</strong> — <code>examples/companion_radio/MyMesh.cpp</code> (L1322–L1353)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L1298-L1353)

```cpp
1322 |       if (_prefs.advert_loc_policy == ADVERT_LOC_NONE) {
1323 |         pkt = createSelfAdvert(_prefs.node_name);
1324 |       } else {
1325 |         pkt = createSelfAdvert(_prefs.node_name, sensors.node_lat, sensors.node_lon);
1326 |       }
1327 |       if (pkt) {
1328 |         pkt->header |= ROUTE_TYPE_FLOOD; // would normally be sent in this mode
1329 | 
1330 |         out_frame[0] = RESP_CODE_EXPORT_CONTACT;
1331 |         uint8_t out_len = pkt->writeTo(&out_frame[1]);
1332 |         releasePacket(pkt); // undo the obtainNewPacket()
1333 |         _serial->writeFrame(out_frame, out_len + 1);
1334 |       } else {
1335 |         writeErrFrame(ERR_CODE_TABLE_FULL); // Error
1336 |       }
1337 |     } else {
1338 |       uint8_t *pub_key = &cmd_frame[1];
1339 |       ContactInfo *recipient = lookupContactByPubKey(pub_key, PUB_KEY_SIZE);
1340 |       uint8_t out_len;
1341 |       if (recipient && (out_len = exportContact(*recipient, &out_frame[1])) > 0) {
1342 |         out_frame[0] = RESP_CODE_EXPORT_CONTACT;
1343 |         _serial->writeFrame(out_frame, out_len + 1);
1344 |       } else {
1345 |         writeErrFrame(ERR_CODE_NOT_FOUND); // not found
1346 |       }
1347 |     }
1348 |   } else if (cmd_frame[0] == CMD_IMPORT_CONTACT && len > 2 + 32 + 64) {
1349 |     if (importContact(&cmd_frame[1], len - 1)) {
1350 |       writeOKFrame();
1351 |     } else {
1352 |       writeErrFrame(ERR_CODE_ILLEGAL_ARG);
1353 |     }
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/base_contacts.py</code> (L64–L105)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_contacts.py#L64-L105)

```python
 64 |     def export_contact(self, pub_key: Optional[bytes] = None) -> Optional[bytes]:
 65 |         """Export a contact (or self) as a 73-byte binary packet."""
 66 |         if pub_key is None:
 67 |             return encode_exported_contact(
 68 |                 self._identity.get_public_key(),
 69 |                 self.prefs.adv_type,
 70 |                 self.prefs.node_name,
 71 |                 self.prefs.latitude,
 72 |                 self.prefs.longitude,
 73 |             )
 74 |         contact = self.contacts.get_by_key(pub_key)
 75 |         if not contact:
 76 |             return None
 77 |         return encode_exported_contact(
 78 |             contact.public_key,
 79 |             contact.adv_type,
 80 |             contact.name,
 81 |             contact.gps_lat,
 82 |             contact.gps_lon,
 83 |         )
 84 | 
 85 |     def import_contact(self, packet_data: bytes) -> bool:
 86 |         """Import a contact from a 73-byte binary packet."""
 87 |         parsed = decode_exported_contact(packet_data)
 88 |         if parsed is None:
 89 |             logger.warning("Import data too short: %s bytes", len(packet_data))
 90 |             return False
 91 |         try:
 92 |             contact = Contact(
 93 |                 public_key=parsed["public_key"],
 94 |                 name=parsed["name"],
 95 |                 adv_type=parsed["adv_type"],
 96 |                 gps_lat=parsed["gps_lat"],
 97 |                 gps_lon=parsed["gps_lon"],
 98 |                 lastmod=int(time.time()),
 99 |             )
100 |             return self.contacts.add(contact)
101 |         except Exception as e:
102 |             logger.error("Error importing contact: %s", e)
103 |             return False
104 | 
105 |     # -------------------------------------------------------------------------
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/binary_parsing.py</code> (L21–L63)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/binary_parsing.py#L21-L63)

```python
21 | # ---------------------------------------------------------------------------
22 | # Exported-contact binary format (CMD_EXPORT_CONTACT / CMD_IMPORT_CONTACT):
23 | # pubkey(32) + adv_type(1) + name(32, NUL padded) + lat(i32 µdeg) + lon(i32 µdeg)
24 | # ---------------------------------------------------------------------------
25 | EXPORTED_CONTACT_STRUCT = "<32sB32sii"
26 | EXPORTED_CONTACT_SIZE = struct.calcsize(EXPORTED_CONTACT_STRUCT)  # 73 bytes
27 | 
28 | 
29 | def encode_exported_contact(
30 |     pub_key: bytes, adv_type: int, name: str, gps_lat: float, gps_lon: float
31 | ) -> bytes:
32 |     """Encode the 73-byte exported-contact blob."""
33 |     name_field = name.encode("utf-8")[:CONTACT_NAME_SIZE].ljust(CONTACT_NAME_SIZE, b"\x00")
34 |     return struct.pack(
35 |         EXPORTED_CONTACT_STRUCT,
36 |         pub_key,
37 |         adv_type,
38 |         name_field,
39 |         int(gps_lat * 1e6),
40 |         int(gps_lon * 1e6),
41 |     )
42 | 
43 | 
44 | def decode_exported_contact(data: bytes) -> Optional[dict]:
45 |     """Decode a 73-byte exported-contact blob; returns None if too short.
46 | 
47 |     ``name_raw`` preserves the undecoded name bytes (up to the first NUL) for
48 |     callers that re-encode the name on the wire.
49 |     """
50 |     if len(data) < EXPORTED_CONTACT_SIZE:
51 |         return None
52 |     pub_key, adv_type, name_field, lat, lon = struct.unpack_from(EXPORTED_CONTACT_STRUCT, data)
53 |     name_raw = name_field.split(b"\x00")[0]
54 |     return {
55 |         "public_key": pub_key,
56 |         "adv_type": adv_type,
57 |         "name": name_raw.decode("utf-8", errors="replace"),
58 |         "name_raw": name_raw,
59 |         "gps_lat": lat / 1e6,
60 |         "gps_lon": lon / 1e6,
61 |         "lat_microdeg": lat,
62 |         "lon_microdeg": lon,
63 |     }
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/models.py</code> (L11–L30)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/models.py#L11-L30)

```python
11 | class Contact:
12 |     """Represents a mesh network contact."""
13 | 
14 |     public_key: bytes  # 32 bytes (Ed25519)
15 |     name: str = ""  # up to 32 chars
16 |     adv_type: int = 0  # ADV_TYPE_CHAT/REPEATER/ROOM/SENSOR
17 |     flags: int = 0  # bitfield
18 |     out_path_len: int = -1  # -1 = unknown, 0 = direct, >0 = multi-hop
19 |     out_path: bytes = b""  # routing path bytes
20 |     last_advert_timestamp: int = 0  # remote timestamp
21 |     lastmod: int = 0  # local modification timestamp
22 |     gps_lat: float = 0.0  # degrees
23 |     gps_lon: float = 0.0  # degrees
24 |     sync_since: int = 0  # for filtered iteration
25 |     # Last on-wire ADVERT packet bytes (Packet.write_to),
26 |     # for CMD_SHARE_CONTACT replay (firmware blob).
27 |     last_advert_packet: Optional[bytes] = None
28 | 
29 |     @property
30 |     def public_key_bytes(self) -> bytes:
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/companion/frame_server.py</code> (L106–L122, L145–L160)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/companion/frame_server.py#L105-L160)

```python
106 |         if msg is None:
107 |             msg = await asyncio.to_thread(self._sync_next_from_persistence)
108 |         if msg is None:
109 |             self._write_frame(bytes([RESP_CODE_NO_MORE_MESSAGES]))
110 |             return
111 |         self._write_frame(self._build_message_frame(msg))
112 | 
113 |     @staticmethod
114 |     def _contact_to_dict(c) -> dict:
115 |         """Convert a Contact object to a persistence dict."""
116 |         pk = c.public_key if isinstance(c.public_key, bytes) else bytes.fromhex(c.public_key)
117 |         return {
118 |             "pubkey": pk,
119 |             "name": c.name,
120 |             "adv_type": c.adv_type,
121 |             "flags": c.flags,
122 |             "out_path_len": c.out_path_len,
…
145 | 
146 |     async def _save_contacts(self) -> None:
147 |         """Persist all contacts to SQLite (non-blocking)."""
148 |         if not self.sqlite_handler:
149 |             return
150 |         contacts = self.bridge.get_contacts()
151 |         dicts = [self._contact_to_dict(c) for c in contacts]
152 |         await asyncio.to_thread(
153 |             self.sqlite_handler.companion_save_contacts,
154 |             self.companion_hash,
155 |             dicts,
156 |         )
157 | 
158 |     async def _save_channels(self) -> None:
159 |         """Persist channels to SQLite (non-blocking)."""
160 |         if not self.sqlite_handler:
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/data_acquisition/sqlite_handler.py</code> (L2380–L2396, L2423–L2439)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/data_acquisition/sqlite_handler.py#L2370-L2440)

```python
2380 |                 """,
2381 |                     (companion_hash,),
2382 |                 )
2383 |                 return [dict(row) for row in cursor.fetchall()]
2384 |         except Exception as e:
2385 |             logger.error(f"Failed to load companion contacts: {e}")
2386 |             return []
2387 | 
2388 |     def companion_save_contacts(self, companion_hash: str, contacts: List[Dict]) -> bool:
2389 |         """Replace all contacts for a companion in storage using batch insert."""
2390 |         try:
2391 |             with self._connect() as conn:
2392 |                 conn.execute(
2393 |                     "DELETE FROM companion_contacts WHERE companion_hash = ?", (companion_hash,)
2394 |                 )
2395 |                 now = time.time()
2396 |                 # Batch insert all contacts at once instead of loop-based inserts
…
2423 |                         rows,
2424 |                     )
2425 |                 conn.commit()
2426 |                 return True
2427 |         except Exception as e:
2428 |             logger.error(f"Failed to save companion contacts: {e}")
2429 |             return False
2430 | 
2431 |     def companion_upsert_contact(self, companion_hash: str, contact: dict) -> bool:
2432 |         """Insert or update a single contact for a companion in storage."""
2433 |         try:
2434 |             with self._connect() as conn:
2435 |                 now = time.time()
2436 |                 conn.execute(
2437 |                     """
2438 |                     INSERT INTO companion_contacts
2439 |                     (companion_hash, pubkey, name, adv_type, flags, out_path_len, out_path,
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/main.py</code> (L610–L626, L677–L692)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/main.py#L600-L692)

```python
610 |                     sqlite_handler=sqlite_handler,
611 |                     companion_hash=companion_hash_str,
612 |                     on_prefs_saved=_make_sync_node_name_to_config(name),
613 |                     **bridge_kwargs,
614 |                 )
615 | 
616 |                 # Load contacts from SQLite
617 |                 if sqlite_handler:
618 |                     contact_rows = sqlite_handler.companion_load_contacts(companion_hash_str)
619 |                     if contact_rows:
620 |                         records = []
621 |                         for row in contact_rows:
622 |                             d = dict(row)
623 |                             d["public_key"] = d.pop("pubkey", d.get("public_key", b""))
624 |                             records.append(d)
625 |                         bridge.contacts.load_from_dicts(records)
626 | 
…
677 |                 self.companion_bridges[companion_hash] = bridge
678 | 
679 |                 frame_server = CompanionFrameServer(
680 |                     bridge=bridge,
681 |                     companion_hash=companion_hash_str,
682 |                     port=tcp_port,
683 |                     bind_address=bind_address,
684 |                     client_idle_timeout_sec=client_idle_timeout_sec,
685 |                     sqlite_handler=sqlite_handler,
686 |                     local_hash=self.local_hash,
687 |                     stats_getter=self._get_companion_stats,
688 |                     control_handler=(
689 |                         self.discovery_helper.control_handler if self.discovery_helper else None
690 |                     ),
691 |                 )
692 |                 await frame_server.start()
```

</details>
