# Claim verification

## Verified claims

| Claim | Verification |
|---|---|
| Complete numbered history retained | IDs 001–100 exist exactly once across active, fully fixed, and intentional-divergence directories. |
| Old reports were not renumbered | Original IDs 001–063, first-pass IDs 064–080, and deeper-follow-up IDs 081–100 remain contiguous within their respective additions. |
| Fixed reports archived | 57 fully fixed reports and their historical sketches are under `archive/findings/` and `archive/patches/`. |
| Intentional policy divergence separated | BUG-023 and its withdrawn sketch are under `archive/intentional/` and are not counted as active or fixed. |
| Active set complete | 42 active reports: 5 partially fixed and 37 not fixed. |
| Every active report has a sketch | One `patches/BUG-NNN.patch` exists for every active report. |
| Every fixed report has a historical sketch | One `archive/patches/BUG-NNN.patch` exists for every fully fixed report. |
| Core tests | 1,110 tests passed against the supplied Core snapshot. |
| Repeater tests | 1,136 tests and 20 subtests passed against the supplied Repeater snapshot. |
| Deeper focused checks | 21 deterministic assertions passed for BUG-081–BUG-100, including both independent BUG-088 failure modes. Raw output is in [DEEPER-FOLLOW-UP-CHECK-OUTPUT.txt](DEEPER-FOLLOW-UP-CHECK-OUTPUT.txt). |
| Full source inventory | 87 Core Python, 66 Repeater Python, and 164 MeshCore C/C++/header files are listed in the review matrix. |
| Maintainer clarification applied | BUG-023 is documented as an intentional data-gathering/routing-policy divergence rather than a defect. Bounded, safe host-side capacity differences are likewise not classified solely by firmware size. |

## Limits

This is a source-level and local-test audit. It does not substitute for over-the-air interoperability testing with multiple physical radios, clock drift, packet loss and RF collisions. Suggested patches are illustrative only.

## Second deeper continuation

BUG-095 through BUG-100 were independently traced from companion minimum-frame guards, command registration, encoded PATH callback data and concurrent room-server scheduling. Each has a focused deterministic reproduction in `DEEPER-FOLLOW-UP-CHECK-OUTPUT.txt`.
