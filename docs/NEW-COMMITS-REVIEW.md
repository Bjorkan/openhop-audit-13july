# Review of newly supplied OpenHop commits

## Commit ranges

| Project | Previous audited head | Current supplied head | Commits | Result |
|---|---|---|---:|---|
| OpenHop Core | [`9ea7269`](https://github.com/openhop-dev/openhop_core/commit/9ea7269a7e7e903fe433b1f952a4026fe3dcc81b) | [`41b6201`](https://github.com/openhop-dev/openhop_core/commit/41b6201ea2e3cb9b8468b0eb80c9e22fdad4a6c8) | 8 | All changed source and tests reviewed |
| OpenHop Repeater | [`6aafa7f`](https://github.com/openhop-dev/openhop_repeater/commit/6aafa7fe991b5b3199b18149f84417f8522d94b2) | [`dd6dfce`](https://github.com/openhop-dev/openhop_repeater/commit/dd6dfce9e89fab76967d91e202d8e47217c30474) | 11 | All changed source, migrations, tests and generated UI references reviewed |

The supplied ZIP contents, not mutable branch state, are the audit source of truth. GitHub commit ranges were used to establish provenance and scope.

## Core changes reviewed

| Area | Changed implementation | Audit disposition |
|---|---|---|
| Packet wire ceiling | Generic builder, serializer and parser now enforce 184 bytes | BUG-002 fully fixed |
| Packet path/hash behavior | Hash composition and encoded path utilities refactored with regression tests | Existing routing fixes remain intact; BUG-065 remains |
| Flood reception delay | Official score, airtime, threshold, cap and post-hold dedupe order added | BUG-023 fully implemented |
| LoRa airtime | One shared RadioLib-compatible estimator used by timing and SX1262 paths | BUG-048 fully fixed |
| Radio capabilities | New backend maximum-power resolver and capability tests | BUG-082 becomes partial; command-side enforcement remains absent |
| Radio command validation | Frequency/BW/SF/CR checks added | BUG-081 becomes partial; repeat byte and 150 MHz lower bound remain |
| Companion contacts and stores | Contact overwrite, count and callback paths refactored | No regression in BUG-014/026/031–035/038 |
| Protocol REQ replay state | Dead fallback side map removed; production ACL client watermark retained | No MeshCore divergence introduced |
| Group-text dedupe | Bounded cache hit refresh added | No regression in BUG-015/016 |
| Receive filtering | Packet hash cache refresh semantics changed; malformed blacklist unchanged | BUG-072 remains active; no new finding |

## Repeater changes reviewed

| Area | Changed implementation | Audit disposition |
|---|---|---|
| Multipart/direct ACK forwarding | Dedicated direct multipart transformation and delay path added | BUG-022 improved but remains partial |
| Companion SQLite queue | Signal and binary channel-data columns, migration, FIFO ID ordering and rehydration added | BUG-060 fully fixed |
| Flood delay wiring | `rx_delay_base` configured, CLI-updatable and passed to Core dispatcher | Completes BUG-023 |
| Airtime and TX delay | Shared Core estimator replaces duplicated formula | Completes BUG-048; BUG-050 remains non-regressed |
| Neighbour-link reporting | New bounded, monotonic-time observational tracker and API/UI | Accepted non-finding; no forwarding or acceptance effect |
| CLI delay settings | Correct configuration section used | Does not resolve BUG-079 maintenance-command stubs |
| Packet router integration | Multipart dispatch and constants updated | Existing BUG-053/056/058/061/062 fixes remain intact |
| Storage and web/API | Schema/query/API extensions plus rebuilt generated assets | No new wire-format divergence found |

## Status transitions

| Finding | Previous | Current | Reason |
|---|---|---|---|
| BUG-002 | 🟡 | ✅ | All generic payload entry/exit points enforce 184 bytes |
| BUG-023 | ⚪ | ✅ | Official disabled-by-default reception-quality hold is now implemented |
| BUG-048 | 🟡 | ✅ | All reviewed airtime paths delegate to one firmware-compatible estimator |
| BUG-060 | 🟡 | ✅ | SQLite round-trips all protocol metadata and binary payload |
| BUG-081 | 🔴 | 🟡 | Core validates four radio fields, but repeat semantics and lower bound remain wrong |
| BUG-082 | 🔴 | 🟡 | True maximum is advertised, but requests above it are not rejected |

BUG-022 and BUG-054 remain partially fixed. Every other active report was traced through the changed files and remains correctly classified. All 57 reports that were already fixed before this update were checked for regression; none regressed.

## Tests

```text
Core full suite:       1182 passed
Repeater full suite:   1193 passed, 20 subtests passed
Core targeted paths:   259 passed
Repeater targeted paths: 440 passed
```

The seven Repeater warnings are pre-existing-style pytest warnings for synchronous neighbour-link tests marked with `@pytest.mark.asyncio`; they are not test failures.
