# BUG-056 — A private region without stored keys becomes a public hashtag scope

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Medium** |
| Area | Transport regions |
| Affected components | OpenHop Core |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

Private MeshCore region names begin with $. If no explicit keys are attached, OpenHop falls through to automatic name hashing and derives a public key for #$name. This silently changes a private/unusable region into a deterministic public scope. To fix it, branch on name.startswith("$") first and yield only stored private keys, including none. Do not fall through based on whether the key list is empty.

## What happens

Private MeshCore region names begin with $. If no explicit keys are attached, OpenHop falls through to automatic name hashing and derives a public key for #$name. This silently changes a private/unusable region into a deterministic public scope.

## How official MeshCore handles it

RegionMap::getTransportKeysFor calls loadKeysFor for a $ region and returns zero when no private key is stored. It never derives an automatic key from that name.

## How the OpenHop stack handles it

**OpenHop Core:** _iter_region_keys uses private keys only when region.private_keys is nonempty. Otherwise every non-# name, including $, is prefixed with # and auto-hashed.

## What needs to change

Branch on name.startswith("$") first and yield only stored private keys, including none. Do not fall through based on whether the key list is empty.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`src/helpers/RegionMap.cpp` L171–L185](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/RegionMap.cpp#L171-L185) |
| OpenHop Core | Affected implementation | [`src/openhop_core/protocol/region_map.py` L49–L74](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/protocol/region_map.py#L49-L74) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>src/helpers/RegionMap.cpp</code> (L171–L185)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/RegionMap.cpp#L171-L185)

```cpp
171 | int RegionMap::getTransportKeysFor(const RegionEntry& src, TransportKey dest[], int max_num) {
172 |   int num;
173 |   if (src.name[0] == '$') {   // private region
174 |     num = _store->loadKeysFor(src.id, dest, max_num);
175 |   } else if (src.name[0] == '#') {   // auto hashtag region
176 |     _store->getAutoKeyFor(src.id, src.name, dest[0]);
177 |     num = 1;
178 |   } else {   // new: implicit auto hashtag region
179 |     char tmp[sizeof(src.name)+1];
180 |     tmp[0] = '#';
181 |     strcpy(&tmp[1], src.name);
182 |     _store->getAutoKeyFor(src.id, tmp, dest[0]);
183 |     num = 1;
184 |   }
185 |   return num;
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/protocol/region_map.py</code> (L49–L74)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/protocol/region_map.py#L49-L74)

```python
49 |     def _iter_region_keys(self, region: RegionEntry) -> Iterable[bytes]:
50 |         """Yield all transport keys for a region."""
51 |         # Private regions: caller supplies explicit keys (e.g. from secure store)
52 |         if region.private_keys:
53 |             for key in region.private_keys:
54 |                 if len(key) == 16:
55 |                     yield key
56 |             return
57 | 
58 |         name = region.name or ""
59 |         if not name:
60 |             return
61 | 
62 |         # Public hashtag region: firmware treats names starting with '#' as
63 |         # canonical, and everything else as an "implicit hashtag" region.
64 |         if name[0] == "#":
65 |             canonical = name
66 |         else:
67 |             canonical = f"#{name}"
68 | 
69 |         # Reuse the existing SHA-256 → 16-byte key logic
70 |         try:
71 |             yield get_auto_key_for(canonical)
72 |         except ValueError:
73 |             # Invalid region name; ignore it rather than raising in callers.
74 |             return
```

</details>
