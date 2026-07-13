# Publication Claim Verification

[← Audit home](../README.md) · [Verification notes](VERIFICATION-NOTES.md)

## Result

The publication set contains **63 confirmed defects**, each represented by one canonical Markdown report. Six reports cover coordinated changes in both `openhop_core` and `openhop_repeater`; they are no longer split into repository-specific issue files. Every retained claim was checked against the supplied OpenHop Core, OpenHop Repeater, and official MeshCore source snapshots. The publication archive contains no intended-behavior or non-bug findings.

## Corrections made during final verification

| Claim | Publication decision | Reason |
|---|---|---|
| BUG-004 — Invalid UTF-8 advert names | Retained with corrected mechanism | The decoder catches the decode error, stores diagnostic raw bytes, then the advert handler rejects the contact because no decoded name exists. |
| BUG-005 — Advert name trimming | Retained with narrowed scope | The evidence supports trimming of advert names and its effect on stored, published, and name-matched values. |
| BUG-013 — Coordinate `(0, 0)` | Retained with corrected condition | OpenHop uses `lat != 0.0 or lon != 0.0`; the defect is specifically that the all-zero but valid coordinate cannot be represented as present. |

## Verification method

1. Followed integrated Core + Repeater call paths rather than treating every missing Core feature as a stack defect.
2. Compared each retained behavior with the supplied official MeshCore implementation, including packet construction, parsing, routing, companion framing, persistence, timing, and capability semantics.
3. Checked that each retained mismatch is a defect rather than an intentional product capability difference.
4. Compared all **217 embedded source excerpts** with the referenced files in the supplied archives. Every numbered source line matches; BUG-027 retains the corrected outer Markdown fence needed for an excerpt containing an internal code fence.
5. Rebuilt the flat bug index, canonical report paths, manifest, links, and checksums from the retained publication set.

## Evidence boundary

“Verified” in this audit means that the relevant mismatch and control flow are directly supported by the supplied source snapshots. It does not mean every consequence was reproduced over RF hardware. The Repeater archive has no Git metadata, so its exact commit is not asserted. The OpenHop Core test suite was not completely green in the supplied snapshot due to unrelated hardware CAD validation failures; this audit does not conceal or reinterpret that result.
