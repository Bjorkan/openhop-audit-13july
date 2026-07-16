# Verification notes

## Source snapshots

- Core: `9ea7269a7e7e903fe433b1f952a4026fe3dcc81b` (`1.1.3.dev6`), with only a version bump after functional commit `9355d08e21423886a17979c0d8defb891f5d9d72`.
- Repeater: `6aafa7fe991b5b3199b18149f84417f8522d94b2`, from the supplied ZIP.
- MeshCore: supplied `v1.16.0` source snapshot.

Later online Repeater commits were deliberately excluded from the audit result because the user supplied and identified the Repeater ZIP as unchanged.

## Test commands

Core and Repeater test suites were run after installing their declared test/runtime dependencies. Logs from the working audit environment reported:

```text
Core: 1110 passed
Repeater: 1136 passed, 20 subtests passed
```

## Static checks

- Compared 113 shared companion command constants numerically.
- Compared packet payload type, route, path-mode, size and crypto constants.
- Indexed 1,468 Core symbols and 1,153 Repeater symbols.
- Traced handler registration and fall-through paths.
- Reviewed all TODO/placeholder and broad-exception sites for compatibility relevance.
- Rechecked every previously fixed status for a regression in the supplied code.

## Interpretation

A green test suite confirms internal expectations, not wire parity. Findings were retained where the current tests encode OpenHop behavior that differs from MeshCore or omit the affected path.

## Deeper follow-up

- Rechecked the complete 317-file review matrix after the first full differential pass.
- Added BUG-081 through BUG-100 from companion, KISS, TRACE, room-server and authenticated REQ paths.
- Reclassified BUG-023 as an intentional policy divergence after the maintainer clarification; it is not counted as fixed or active.
- Executed 21 focused deterministic assertions covering the 20 newly added reports; BUG-088 has two independent reproductions.
- Re-ran the complete suites: Core collected and passed 1,110 tests; Repeater passed 1,136 tests and 20 subtests.
- No source code in the supplied projects was modified.
