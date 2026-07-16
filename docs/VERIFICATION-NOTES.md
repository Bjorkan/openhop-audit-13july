# Verification notes

## Source snapshots

- Core: `41b6201ea2e3cb9b8468b0eb80c9e22fdad4a6c8` (`fix/all-the-things-core` supplied ZIP), 8 commits after `9ea7269a7e7e903fe433b1f952a4026fe3dcc81b`.
- Repeater: `dd6dfce9e89fab76967d91e202d8e47217c30474` (`fix/all-the-things` supplied ZIP), 11 commits after `6aafa7fe991b5b3199b18149f84417f8522d94b2`.
- MeshCore: unchanged supplied `v1.16.0` source snapshot.

## Test commands and results

Core and Repeater were installed into an isolated virtual environment and run with their complete collected suites:

```text
Core: 1182 passed in 24.18s
Repeater: 1193 passed, 20 subtests passed in 10.59s
```

Changed-path suites were also run independently:

```text
Core targeted: 259 passed in 2.77s
Repeater targeted: 440 passed in 2.06s
```

The Repeater suite emits seven warnings because synchronous neighbour-link tests carry an asyncio marker. No test failed.

## Commit-delta method

- Compared every changed source and test file against the prior supplied snapshots.
- Mapped changed files to all active and archived findings that cite or transitively depend on them.
- Re-read the changed control flow against the same official MeshCore reference files.
- Re-ran complete suites and focused changed-path suites.
- Rechecked unchanged active findings where shared packet, timing, dispatcher, radio or persistence primitives changed.
- Rechecked every archived correction for regression.

## Outcome

- BUG-002, BUG-023, BUG-048 and BUG-060 moved to the fixed archive.
- BUG-081 and BUG-082 moved from red to partial.
- BUG-022 and BUG-054 remain partial.
- 35 findings remain not fixed.
- No new numbered finding was established by the new commit ranges.
- No archived correction regressed.

Passing tests confirm internal consistency but do not by themselves prove wire parity; active reports remain where direct source comparison still establishes a mismatch.


## Deeper logic pass

- Source snapshots remained Core `41b6201ea2e3cb9b8468b0eb80c9e22fdad4a6c8` and Repeater `dd6dfce9e89fab76967d91e202d8e47217c30474`.
- Added 18 focused, fail-closed source assertions for BUG-101–BUG-118; all passed.
- `compileall` passed for both Python packages.
- No previous active report was closed and no archived correction regressed.
- The earlier full-suite totals remain valid baseline evidence for these same ZIP snapshots, but were not rerun in the current environment. Optional dependencies including PyCryptodome/PyNaCl/CherryPy/serial/radio packages were unavailable and package installation could not complete, so this pass does not present inherited test totals as fresh executions.


## Continued deep review

- Source heads remained Core `41b6201ea2e3cb9b8468b0eb80c9e22fdad4a6c8` and Repeater `dd6dfce9e89fab76967d91e202d8e47217c30474`.
- Added BUG-119–BUG-124 after failure-path, connection-lifecycle, identity, forwarding-policy, durability and fallback-timing review.
- Sixteen focused source assertions passed.
- Core and Repeater compileall remained successful.
- No prior status changed and no archived correction regressed in the reviewed paths.
- Full pytest suites were not freshly rerun because optional crypto, web, serial and radio dependencies are unavailable; inherited suite totals remain clearly labelled as baseline results.


## Latest commits and deeper protocol-lifecycle pass

- Core advanced from `41b6201ea2e3cb9b8468b0eb80c9e22fdad4a6c8` to `abe1d857734d5d1f549ada27af6f95c7e5e53e95` (3 commits).
- Repeater advanced from `dd6dfce9e89fab76967d91e202d8e47217c30474` to `b62960fa3041447bedadb2131d892a6565d7e519` (2 commits).
- Fresh full tests passed: Core 1,184; Repeater 1,193 plus 20 subtests.
- All 124 prior reports were rechecked against changed and transitively affected paths. No status changed and no archived fix regressed.
- Six new reports, BUG-125–BUG-130, were established by direct source comparison and focused checks.
- Final classification: 130 reports, 61 archived, 69 active (4 partial, 65 not fixed).
