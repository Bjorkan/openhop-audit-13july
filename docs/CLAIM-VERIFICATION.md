# Claim verification

## Verified claims

| Claim | Verification |
|---|---|
| Complete numbered history retained | IDs 001–100 exist exactly once across active and archived directories. |
| Old reports were not renumbered | Original IDs 001–063 and later IDs 064–100 remain unchanged. |
| Fixed reports archived | 61 fully fixed/implemented reports and their historical sketches are under `archive/findings/` and `archive/patches/`. |
| Active set complete | 39 active reports: 4 partially fixed and 35 not fixed. |
| Current intentional set | No numbered report is currently classified as an intentional divergence; BUG-023 is now implemented and archived as fixed. |
| Patch-sketch coverage | Every active and archived report has exactly one corresponding historical/illustrative patch file. |
| Core tests | 1,182 tests passed against Core [`41b6201`](https://github.com/openhop-dev/openhop_core/commit/41b6201ea2e3cb9b8468b0eb80c9e22fdad4a6c8). |
| Repeater tests | 1,193 tests and 20 subtests passed against Repeater [`dd6dfce`](https://github.com/openhop-dev/openhop_repeater/commit/dd6dfce9e89fab76967d91e202d8e47217c30474). |
| Changed-path tests | 259 Core and 440 Repeater targeted tests passed. |
| Full source inventory | 88 Core Python, 67 Repeater Python and 164 protocol-relevant MeshCore reference files are listed in the review matrix. |
| New commit coverage | All 8 Core commits and all 11 Repeater commits between the prior and current supplied heads were reviewed. |
| Regression check | None of the previously archived corrections regressed. |
| Maintainer policy applied | Bounded host-side capacity and observational neighbour metrics are not defects solely because they differ from embedded limits. |

## Limits

This is a source-level and local-test audit. It does not substitute for over-the-air interoperability testing with multiple physical radios, clock drift, packet loss and RF collisions. Suggested patches are illustrative only.
