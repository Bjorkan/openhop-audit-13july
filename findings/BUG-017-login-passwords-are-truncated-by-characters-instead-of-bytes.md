# BUG-017 — Login passwords are truncated by characters instead of bytes

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Low** |
| Area | Login request construction |
| Affected components | OpenHop Core |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

The password field is byte-limited on the wire. OpenHop truncates the Python string before UTF-8 encoding, so multibyte characters can produce more password bytes than MeshCore accepts and shift or enlarge the encrypted request. To fix it, encode first, truncate to the MeshCore byte limit without splitting a UTF-8 sequence if a textual policy is desired, and base all packet length checks on the resulting bytes. Add multibyte password tests.

## What happens

The password field is byte-limited on the wire. OpenHop truncates the Python string before UTF-8 encoding, so multibyte characters can produce more password bytes than MeshCore accepts and shift or enlarge the encrypted request.

## How official MeshCore handles it

MeshCore operates on the encoded char buffer and bounds the actual byte count placed in the request.

## How the OpenHop stack handles it

**OpenHop Core:** The request builder slices the Unicode value by character count and encodes afterward.

## What needs to change

Encode first, truncate to the MeshCore byte limit without splitting a UTF-8 sequence if a textual policy is desired, and base all packet length checks on the resulting bytes. Add multibyte password tests.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/helpers/BaseChatMesh.cpp` L560–L576](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L560-L576) |
| OpenHop Core | Affected implementation | [`src/openhop_core/protocol/packet_builder.py` L648–L650](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/protocol/packet_builder.py#L648-L650) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/helpers/BaseChatMesh.cpp</code> (L560–L576)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/BaseChatMesh.cpp#L560-L576)

```cpp
560 | int BaseChatMesh::sendLogin(const ContactInfo& recipient, const char* password, uint32_t& est_timeout) {
561 |   mesh::Packet* pkt;
562 |   {
563 |     int tlen;
564 |     uint8_t temp[24];
565 |     uint32_t now = getRTCClock()->getCurrentTimeUnique();
566 |     memcpy(temp, &now, 4);   // mostly an extra blob to help make packet_hash unique
567 |     if (recipient.type == ADV_TYPE_ROOM) {
568 |       memcpy(&temp[4], &recipient.sync_since, 4);
569 |       int len = strlen(password); if (len > 15) len = 15;  // max 15 chars currently
570 |       memcpy(&temp[8], password, len);
571 |       tlen = 8 + len;
572 |     } else {
573 |       int len = strlen(password); if (len > 15) len = 15;  // max 15 chars currently
574 |       memcpy(&temp[4], password, len);
575 |       tlen = 4 + len;
576 |     }
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/protocol/packet_builder.py</code> (L648–L650)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/protocol/packet_builder.py#L648-L650)

```python
648 |         timestamp = PacketBuilder._get_timestamp()
649 |         password_truncated = password[:15]
650 |         password_bytes = password_truncated.encode("utf-8")
```

</details>
