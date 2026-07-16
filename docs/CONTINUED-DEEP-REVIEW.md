# Continued failure-path and lifecycle review

## Scope

This pass used the same supplied source heads as the preceding audit and continued into code paths where protocol parity depends on failure ordering, long-lived state, restart durability or payload policy rather than only successful packet decoding.

Reviewed themes:

- pending ACK creation and send failure cleanup;
- successful login connection/keep-alive lifecycle;
- reserved local identity prefixes;
- flood forwarding policy for RAW_CUSTOM and unknown types;
- persistence of contact route resets;
- KISS airtime fallback behavior.

## Result

Six additional confirmed mismatches were added:

| Finding | Severity | Summary |
|---|---|---|
| BUG-119 | High | Pending ACK entries are created before a text packet is successfully sent |
| BUG-120 | High | Successful server logins do not start keep-alive connections |
| BUG-121 | High | Local identities can use MeshCore-reserved 0x00 and 0xFF prefixes |
| BUG-122 | High | Flood forwarding retransmits RAW_CUSTOM and unknown payload types |
| BUG-123 | Medium | CMD_RESET_PATH does not persist the cleared route |
| BUG-124 | Low | KISS fallback airtime retains a non-firmware 50 ms floor |

Severity distribution: **4 High**, **1 Medium**, **1 Low**.

The audit now contains **124 confirmed numbered findings**: **61 archived** and **63 active** (**4 partially fixed**, **59 not fixed**). No previous status changed and no archived correction regressed in the paths rechecked here.

## Verification

- Every new report embeds current OpenHop and official MeshCore source excerpts.
- `continued_logic_checks.py` ran 16 focused assertions covering both sides of all six mismatches.
- `python -m compileall -q` remained successful for Core and Repeater.
- Full pytest totals in the README are retained as the previously verified baseline for these exact snapshots, not as fresh executions from this pass.

## Non-findings retained

- A larger bounded host-side table is not a defect by itself.
- The neighbour-link observation/reporting design is not reopened as a bug; only actual forwarding behavior is compared.
- The generic own-packet and dispatcher-seen findings remain separate from the reserved identity-prefix rule documented in BUG-121.
- The existing short-command report remains the home for undersized import-command validation, avoiding a duplicate numbered issue.
