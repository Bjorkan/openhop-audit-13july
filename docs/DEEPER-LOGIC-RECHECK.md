# Deeper logic, ACL and room-server recheck

## Scope

This pass continued from the already-reviewed Core `41b6201` and Repeater `dd6dfce` snapshots. It did not assume that a larger host-side table or database was a defect. The review concentrated on behavior that survives unit-level packet parsing but diverges when state, roles, retries, concurrent requests or the Core/Repeater boundary are considered together.

Reviewed themes:

- default payload dispatch versus firmware switch coverage;
- companion command body boundaries and request handling;
- text subtype validation, activity timestamps and command correlation;
- ACL wire values, login fallback and persistence;
- room permission, replay, ACK and message-fidelity state machines;
- authenticated request and CLI response timing/uniqueness.

## Result

Eighteen new confirmed mismatches were added as BUG-101–BUG-118:

| Finding | Severity | Summary |
|---|---|---|
| BUG-101 | Medium | Standalone MeshNode registers group text but not group data |
| BUG-102 | Medium | Repeater pushes non-zero-hop and non-discovery CONTROL packets to companions |
| BUG-103 | High | The command-response waiter captures unrelated or wrong-sender messages |
| BUG-104 | Medium | CMD_ADD_UPDATE_CONTACT rejects the valid 35-byte minimum body |
| BUG-105 | High | Companion endpoints cannot answer peer protocol requests |
| BUG-106 | Medium | Incoming plain and signed messages do not refresh contact lastmod |
| BUG-107 | High | ACL role values are wire-incompatible and collapse read-only and read-write |
| BUG-108 | Medium | Room-server read-only fallback only works for blank passwords |
| BUG-109 | High | Room-server read-only clients can create posts |
| BUG-110 | High | Room-server message replays can create duplicate posts |
| BUG-111 | High | Repeater and room ACL identities are lost on restart |
| BUG-112 | Medium | Unsupported inbound text types are delivered as application messages |
| BUG-113 | High | Room-server CLI and posts are classified by text prefix instead of wire type |
| BUG-114 | High | Room delivery ACKs are sent before post acceptance |
| BUG-115 | Low | Authenticated request replies wait 500 ms instead of 300 ms |
| BUG-116 | Low | Room-server posts lose trailing whitespace |
| BUG-117 | Medium | CLI replies do not use a unique timestamp distinct from the request |
| BUG-118 | High | CLI command retries can execute administrative actions again |

Severity distribution: **9 High**, **7 Medium**, **2 Low**.

The audit now contains 118 numbered reports: 61 archived and 57 active (4 partially fixed, 53 not fixed). No archived correction regressed in the source paths touched by this pass.

## Verification method

- Each new report has at least one OpenHop range and one official MeshCore range embedded in the report.
- `deeper_logic_checks.py` asserted all 18 concrete source predicates and completed with 18 passes.
- `python -m compileall -q` completed for both `src/openhop_core` and `repeater`.
- Existing full-suite results (1,182 Core tests; 1,193 Repeater tests plus 20 subtests) remain the verified baseline for the same snapshots. They were not claimed as newly rerun in this pass because the current environment lacked several optional project dependencies and package installation was unavailable.

## Deliberate non-findings

The following were considered but not filed:

- OpenHop's larger bounded ACL/contact capacities are not defects merely because firmware uses smaller embedded arrays.
- The neighbour-link scoring/reporting design remains a deliberate observational feature; BUG-023 stays archived because the current routing hold is implemented.
- A path slice using an encoded `out_path_len` was not filed where the stored path buffer already contains exactly the encoded byte count; Python's oversized slice does not alter the wire path in that specific call site.
- Additional host-side post rate limiting was not classified as a parity defect by itself. Reports were filed only where ACK, permission or replay semantics falsely claim firmware-compatible acceptance.
