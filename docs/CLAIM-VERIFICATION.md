# Claim verification

## Verified claims

| Claim | Verification |
|---|---|
| Complete numbered history retained | IDs 001–130 exist exactly once across active and archived directories. |
| Old reports were not renumbered | Original IDs 001–100 remain unchanged; new reports use 101–130. |
| Fixed reports archived | 61 fully fixed/implemented reports and their historical sketches remain under `archive/findings/` and `archive/patches/`. |
| Active set complete | 69 active reports: 4 partially fixed and 65 not fixed. |
| Confirmed numbered defects | All 130 numbered reports are classified as defects; no numbered intentional-divergence report remains. |
| Current intentional set | No numbered report is currently classified as an intentional divergence; accepted host-side differences remain documented separately. |
| Patch-sketch coverage | Every active and archived report has exactly one corresponding historical/illustrative patch file. |
| Core baseline tests | 1,184 tests passed against Core [`abe1d85`](https://github.com/openhop-dev/openhop_core/commit/abe1d857734d5d1f549ada27af6f95c7e5e53e95). |
| Repeater baseline tests | 1,193 tests and 20 subtests passed against Repeater [`b62960f`](https://github.com/openhop-dev/openhop_repeater/commit/b62960fa3041447bedadb2131d892a6565d7e519). |
| Focused latest checks | Six executable checks for BUG-125–BUG-130 passed against the supplied snapshots. |
| Deeper source checks | 18 assertions for BUG-101–BUG-118, 16 assertions for BUG-119–BUG-124 and 6 focused checks for BUG-125–BUG-130 passed. |
| Compilation | `compileall` passed for both current Python packages. |
| Full source inventory | 88 Core Python, 68 Repeater Python and 164 protocol-relevant MeshCore reference files remain listed in the review matrix. |
| Regression check | None of the previously archived corrections regressed in the reviewed paths. |
| Maintainer policy applied | Bounded host-side capacity and observational neighbour metrics are not defects solely because they differ from embedded limits. |

## Limits

This is a source-level and local-test audit. It does not substitute for over-the-air interoperability testing with multiple physical radios, clock drift, packet loss and RF collisions. The full test-suite figures above were freshly executed against the latest supplied snapshots. Suggested patches are illustrative only.
