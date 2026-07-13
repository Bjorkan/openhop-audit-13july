# BUG-002 — Advert application data exceeds the MeshCore limit

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Medium** |
| Area | Packet format |
| Affected components | OpenHop Core |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

OpenHop permits 96 bytes of application data in an advert, while MeshCore reserves at most 32 bytes. An advert accepted or produced by OpenHop can therefore be rejected, truncated, or parsed differently by MeshCore nodes. To fix it, change the OpenHop limit to 32 bytes and reject longer inbound and outbound application data. Test lengths 32 and 33 on both encode and decode paths.

## What happens

OpenHop permits 96 bytes of application data in an advert, while MeshCore reserves at most 32 bytes. An advert accepted or produced by OpenHop can therefore be rejected, truncated, or parsed differently by MeshCore nodes.

## How official MeshCore handles it

MeshCore defines MAX_ADVERT_APP_DATA_SIZE as 32 and builds/parses advertisements around that bound.

## How the OpenHop stack handles it

**OpenHop Core:** OpenHop defines MAX_ADVERT_APP_DATA_SIZE as 96 and uses that value in its advert model and builder validation.

## What needs to change

Change the OpenHop limit to 32 bytes and reject longer inbound and outbound application data. Test lengths 32 and 33 on both encode and decode paths.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/MeshCore.h` L5–L21](https://github.com/meshcore-dev/MeshCore/blob/main/src/MeshCore.h#L5-L21) |
| OpenHop Core | Affected implementation | [`src/openhop_core/protocol/constants.py` L41–L63](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/protocol/constants.py#L41-L63) |
| OpenHop Core | Affected implementation | [`src/openhop_core/protocol/packet_builder.py` L165–L210](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/protocol/packet_builder.py#L165-L210) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/MeshCore.h</code> (L5–L21)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/MeshCore.h#L5-L21)

```cpp
 5 | #include <math.h>
 6 | 
 7 | #define MAX_HASH_SIZE        8
 8 | #define PUB_KEY_SIZE        32
 9 | #define PRV_KEY_SIZE        64
10 | #define SEED_SIZE           32
11 | #define SIGNATURE_SIZE      64
12 | #define MAX_ADVERT_DATA_SIZE  32
13 | #define CIPHER_KEY_SIZE     16
14 | #define CIPHER_BLOCK_SIZE   16
15 | 
16 | // V1
17 | #define CIPHER_MAC_SIZE      2
18 | #define PATH_HASH_SIZE       1
19 | 
20 | #define MAX_PACKET_PAYLOAD  184
21 | #define MAX_GROUP_DATA_LENGTH  (MAX_PACKET_PAYLOAD - CIPHER_BLOCK_SIZE - 3)
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/protocol/constants.py</code> (L41–L63)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/protocol/constants.py#L41-L63)

```python
41 | PAYLOAD_VER_1 = 0x00  # Currently supported
42 | PAYLOAD_VER_2 = 0x01  # Reserved for future use
43 | PAYLOAD_VER_3 = 0x02  # Reserved for future use
44 | PAYLOAD_VER_4 = 0x03  # Reserved for future use
45 | MAX_SUPPORTED_PAYLOAD_VERSION = PAYLOAD_VER_2  # Accept versions 0-1
46 | 
47 | # ---------------------------------------------------------------------------
48 | # Misc sizes
49 | # ---------------------------------------------------------------------------
50 | MAX_ADVERT_DATA_SIZE = 96
51 | PUB_KEY_SIZE = 32
52 | SIGNATURE_SIZE = 64
53 | PATH_HASH_SIZE = 1  # Legacy default; see PathUtils for multi-byte path support
54 | PATH_HASH_COUNT_MASK = 0x3F  # bits 0-5 of encoded path_len (max encodable hop count)
55 | PATH_HASH_SIZE_SHIFT = 6  # bits 6-7 of encoded path_len
56 | CIPHER_MAC_SIZE = 32  # SHA‑256 HMAC
57 | CIPHER_BLOCK_SIZE = 16
58 | MAX_PACKET_PAYLOAD = 256  # firmware's default
59 | MAX_TEXT_LEN = 10 * CIPHER_BLOCK_SIZE  # firmware BaseChatMesh.h message text cap (160)
60 | 
61 | MAX_PATH_SIZE = 64
62 | MAX_PACKET_PAYLOAD = 256
63 | MAX_HASH_SIZE = 32  # SHA-256 truncated
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/protocol/packet_builder.py</code> (L165–L210)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/protocol/packet_builder.py#L165-L210)

```python
165 |     def _encode_advert_data(
166 |         name: str,
167 |         lat: float = 0.0,
168 |         lon: float = 0.0,
169 |         feature1: int = 0,
170 |         feature2: int = 0,
171 |         flags: int = 0,
172 |     ) -> bytes:
173 |         """Encodes advertisement metadata including location and features."""
174 |         buf = bytearray()
175 | 
176 |         # Set flags based on what data is provided
177 |         final_flags = flags
178 |         if lat != 0.0 or lon != 0.0:
179 |             final_flags |= ADVERT_FLAG_HAS_LOCATION
180 |         if feature1 != 0:
181 |             final_flags |= ADVERT_FLAG_HAS_FEATURE1
182 |         if feature2 != 0:
183 |             final_flags |= ADVERT_FLAG_HAS_FEATURE2
184 |         if name:
185 |             final_flags |= ADVERT_FLAG_HAS_NAME
186 | 
187 |         buf.append(final_flags)
188 | 
189 |         # Add location data if present
190 |         if final_flags & ADVERT_FLAG_HAS_LOCATION:
191 |             lat_int = int(lat * 1000000)
192 |             lon_int = int(lon * 1000000)
193 |             buf += struct.pack("<i", lat_int)
194 |             buf += struct.pack("<i", lon_int)
195 | 
196 |         # Add feature data if present
197 |         if final_flags & ADVERT_FLAG_HAS_FEATURE1:
198 |             buf += struct.pack("<H", feature1)
199 | 
200 |         if final_flags & ADVERT_FLAG_HAS_FEATURE2:
201 |             buf += struct.pack("<H", feature2)
202 | 
203 |         # Add name if present
204 |         if final_flags & ADVERT_FLAG_HAS_NAME:
205 |             name_bytes = name.encode("utf-8")
206 |             # Copy name bytes up to remaining space in MAX_ADVERT_DATA_SIZE
207 |             remaining = MAX_ADVERT_DATA_SIZE - len(buf)
208 |             buf += name_bytes[:remaining]
209 | 
210 |         return bytes(buf)
```

</details>
