# BUG-020 — Older advertisements can overwrite newer contacts

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **High** |
| Area | Contact synchronization |
| Affected components | OpenHop Core |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

OpenHop updates a contact without enforcing MeshCore's advertisement timestamp replay rule. A delayed or replayed advert can replace newer contact name, location, type, or application data. To fix it, compare the raw advertised timestamp before updating any persisted fields. Port MeshCore's exact equality and special-case rules and test new, equal, older, and wrap/restart scenarios.

## What happens

OpenHop updates a contact without enforcing MeshCore's advertisement timestamp replay rule. A delayed or replayed advert can replace newer contact name, location, type, or application data.

## How official MeshCore handles it

BaseChatMesh compares the received advert timestamp with the stored contact and rejects stale updates, while still handling allowed special cases.

## How the OpenHop stack handles it

**OpenHop Core:** The base contact event path parses and applies the incoming advert but does not perform the equivalent monotonic timestamp rejection before mutation.

## What needs to change

Compare the raw advertised timestamp before updating any persisted fields. Port MeshCore's exact equality and special-case rules and test new, equal, older, and wrap/restart scenarios.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/helpers/BaseChatMesh.cpp` L99–L128](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L99-L128) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/base_contacts.py` L188–L244](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_contacts.py#L188-L244) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/helpers/BaseChatMesh.cpp</code> (L99–L128)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L99-L128)

```cpp
 99 | void BaseChatMesh::populateContactFromAdvert(ContactInfo& ci, const mesh::Identity& id, const AdvertDataParser& parser, uint32_t timestamp) {
100 |   memset(&ci, 0, sizeof(ci));
101 |   ci.id = id;
102 |   ci.out_path_len = OUT_PATH_UNKNOWN;
103 |   StrHelper::strncpy(ci.name, parser.getName(), sizeof(ci.name));
104 |   ci.type = parser.getType();
105 |   if (parser.hasLatLon()) {
106 |     ci.gps_lat = parser.getIntLat();
107 |     ci.gps_lon = parser.getIntLon();
108 |   }
109 |   ci.last_advert_timestamp = timestamp;
110 |   ci.lastmod = getRTCClock()->getCurrentTime();
111 | }
112 | 
113 | void BaseChatMesh::onAdvertRecv(mesh::Packet* packet, const mesh::Identity& id, uint32_t timestamp, const uint8_t* app_data, size_t app_data_len) {
114 |   AdvertDataParser parser(app_data, app_data_len);
115 |   if (!(parser.isValid() && parser.hasName())) {
116 |     MESH_DEBUG_PRINTLN("onAdvertRecv: invalid app_data, or name is missing: len=%d", app_data_len);
117 |     return;
118 |   }
119 | 
120 |   ContactInfo* from = NULL;
121 |   for (int i = 0; i < num_contacts; i++) {
122 |     if (id.matches(contacts[i].id)) {  // is from one of our contacts
123 |       from = &contacts[i];
124 |       if (timestamp <= from->last_advert_timestamp) {  // check for replay attacks!!
125 |         MESH_DEBUG_PRINTLN("onAdvertRecv: Possible replay attack, name: %s", from->name);
126 |         return;
127 |       }
128 |       break;
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/base_contacts.py</code> (L202–L218, L223–L239)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_contacts.py#L188-L244)

```python
202 |             path_len_encoded: Encoded path_len byte from the packet. If None,
203 |                 falls back to len(inbound_path) (assumes 1-byte hashes).
204 |         """
205 |         try:
206 |             if len(contact.public_key) < 7 or not contact.name:
207 |                 return None
208 |             inbound_path = inbound_path or b""
209 |             advert_path_len = (
210 |                 path_len_encoded if path_len_encoded is not None else len(inbound_path)
211 |             )
212 |             self.path_cache.update(
213 |                 AdvertPath(
214 |                     public_key_prefix=contact.public_key[:7],
215 |                     name=contact.name,
216 |                     path_len=advert_path_len,
217 |                     path=inbound_path,
218 |                     recv_timestamp=int(time.time()),
…
223 |                 contact.out_path_len = existing.out_path_len
224 |                 contact.out_path = existing.out_path
225 |                 contact.flags = existing.flags
226 |                 contact.sync_since = existing.sync_since
227 |                 if contact.last_advert_packet is None:
228 |                     contact.last_advert_packet = existing.last_advert_packet
229 |                 self.contacts.update(contact)
230 |                 return contact
231 |             if not self.should_auto_add_contact_type(contact.adv_type):
232 |                 logger.debug("Auto-add filtered: type %d not allowed", contact.adv_type)
233 |                 return None
234 |             if self.should_overwrite_when_full() and self.contacts.is_full():
235 |                 ok, overwritten = self.contacts.add_or_overwrite(contact)
236 |                 if ok and overwritten:
237 |                     await self._fire_callbacks("contact_deleted", overwritten)
238 |                 elif not ok:
239 |                     await self._fire_callbacks("contacts_full")
```

</details>
