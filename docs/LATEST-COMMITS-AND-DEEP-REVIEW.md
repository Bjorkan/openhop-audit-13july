# Latest commit-impact and deeper protocol review

## Scope

This pass compared the newly supplied snapshots against the previous audit heads and then continued a targeted differential review against the unchanged official MeshCore `v1.16.0` source snapshot.

| Project | Previous audited head | Latest supplied head | New commits |
|---|---|---|---:|
| OpenHop Core | [`41b6201`](https://github.com/openhop-dev/openhop_core/commit/41b6201ea2e3cb9b8468b0eb80c9e22fdad4a6c8) | [`abe1d85`](https://github.com/openhop-dev/openhop_core/commit/abe1d857734d5d1f549ada27af6f95c7e5e53e95) | 3 |
| OpenHop Repeater | [`dd6dfce`](https://github.com/openhop-dev/openhop_repeater/commit/dd6dfce9e89fab76967d91e202d8e47217c30474) | [`b62960f`](https://github.com/openhop-dev/openhop_repeater/commit/b62960fa3041447bedadb2131d892a6565d7e519) | 2 |

## Commit-impact review

Core changed flood reception metrics, packet-score/airtime helpers and SX1262 diagnostics/formatting. Repeater changed the shared flood-score use, trace routing predicate and neighbour-report UI. Every changed source path was mapped to active and archived reports that depend on packet timing, dispatcher filtering, route classification, radio timing or neighbour observations.

Outcome:

- No existing finding changed status.
- No archived finding regressed.
- BUG-023 remains fully implemented and archived. The shared `flood_rx_metrics()` extraction preserves the disabled-by-default reception-quality hold.
- BUG-124 remains not fixed because `PacketTimingUtils.estimate_airtime_ms()` still enforces `max(airtime_ms, 50.0)`.
- The new dispatcher maintenance code calls `cleanup_old_hashes()` once per second; therefore the normal duplicate-history table is not a new unbounded-storage finding.

## New findings

| Finding | Result |
|---|---|
| BUG-125 | TCP FrameServer injects unsolicited `RESP_CODE_CURR_TIME` frames every idle heartbeat interval. |
| BUG-126 | `Packet.read_from()` accepts a header/path-only packet with no payload byte. |
| BUG-127 | Companion packet stats use mismatched keys and Repeater collapses all routing counters to flood. |
| BUG-128 | A TCP connection clears unrelated callbacks registered through the public bridge API. |
| BUG-129 | Binary/discovery ownership tags and callbacks lack timeout and disconnect cleanup. |
| BUG-130 | The default eight-hour inbound idle timeout disconnects valid long-lived sessions unlike firmware. |

## Verification

- Core full suite: **1,184 passed**.
- Repeater full suite: **1,193 passed, 20 subtests passed**, with seven existing marker warnings.
- Focused new-finding checks: **6 passed**.
- All 130 report IDs and patch-sketch pairs were validated during packaging.

Passing tests establish internal consistency but do not override direct wire/state-machine differences demonstrated by the findings.

## Captured evidence

- [Core full-suite output](LATEST-CORE-TEST-OUTPUT.txt)
- [Repeater full-suite output](LATEST-REPEATER-TEST-OUTPUT.txt)
- [Focused check script](LATEST-DEEP-CHECK-SCRIPT.py)
- [Focused check output](LATEST-DEEP-CHECK-OUTPUT.txt)
