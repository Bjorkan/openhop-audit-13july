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
