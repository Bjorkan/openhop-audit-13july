# BUG-031 — CONTACTS_START reports the filtered result count

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Low** |
| Area | Companion contact synchronization |
| Affected components | OpenHop Core |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

For CMD_GET_CONTACTS with a since filter, OpenHop reports the number of frames it plans to emit. MeshCore reports the total contact-table count before applying the iterator filter. Clients that use MeshCore's count semantics observe a different value. To fix it, expose and send the same total table count as MeshCore, independent of since. Keep the end watermark and emitted frames filtered exactly as the firmware iterator does.

## What happens

For CMD_GET_CONTACTS with a since filter, OpenHop reports the number of frames it plans to emit. MeshCore reports the total contact-table count before applying the iterator filter. Clients that use MeshCore's count semantics observe a different value.

## How official MeshCore handles it

The companion writes RESP_CODE_CONTACTS_START with getNumContacts(), then starts an iterator that applies _iter_filter_since and skips transient records while emitting.

## How the OpenHop stack handles it

**OpenHop Core:** _cmd_get_contacts first calls get_contacts(since), then writes len(contacts), which is already filtered and excludes transient contacts.

## What needs to change

Expose and send the same total table count as MeshCore, independent of since. Keep the end watermark and emitted frames filtered exactly as the firmware iterator does.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`examples/companion_radio/MyMesh.cpp` L1177–L1195](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L1177-L1195) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/frame_server/commands_contacts.py` L36–L43](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/frame_server/commands_contacts.py#L36-L43) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>examples/companion_radio/MyMesh.cpp</code> (L1177–L1195)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L1177-L1195)

```cpp
1177 |   } else if (cmd_frame[0] == CMD_GET_CONTACTS) { // get Contact list
1178 |     if (_iter_started) {
1179 |       writeErrFrame(ERR_CODE_BAD_STATE); // iterator is currently busy
1180 |     } else {
1181 |       if (len >= 5) { // has optional 'since' param
1182 |         memcpy(&_iter_filter_since, &cmd_frame[1], 4);
1183 |       } else {
1184 |         _iter_filter_since = 0;
1185 |       }
1186 | 
1187 |       uint8_t reply[5];
1188 |       reply[0] = RESP_CODE_CONTACTS_START;
1189 |       uint32_t count = getNumContacts(); // total, NOT filtered count
1190 |       memcpy(&reply[1], &count, 4);
1191 |       _serial->writeFrame(reply, 5);
1192 | 
1193 |       // start iterator
1194 |       _iter = startContactsIterator();
1195 |       _iter_started = true;
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/frame_server/commands_contacts.py</code> (L36–L43)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/frame_server/commands_contacts.py#L36-L43)

```python
36 |     async def _cmd_get_contacts(self, data: bytes) -> None:
37 |         since = struct.unpack("<I", data[:4])[0] if len(data) >= 4 else 0
38 |         contacts = self.bridge.get_contacts(since=since)
39 |         self._write_frame(bytes([RESP_CODE_CONTACTS_START]) + struct.pack("<I", len(contacts)))
40 |         for i, c in enumerate(contacts):
41 |             self._write_contact_frame(c)
42 |         most_recent = max((c.lastmod for c in contacts), default=0)
43 |         self._write_frame(bytes([RESP_CODE_END_OF_CONTACTS]) + struct.pack("<I", most_recent))
```

</details>
