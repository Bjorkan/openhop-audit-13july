# Targeted runtime reproduction checks

These focused checks were executed against the exact supplied source snapshots in addition to the complete project test suites. The raw follow-up output is preserved in [DEEPER-FOLLOW-UP-CHECK-OUTPUT.txt](DEEPER-FOLLOW-UP-CHECK-OUTPUT.txt). They exercise compact, deterministic manifestations of selected active findings.

| Finding | Check | Observed result |
|---|---|---|
| BUG-064 | Read the public `CIPHER_MAC_SIZE` constant. | `32`; the MeshCore wire MAC is 2 bytes. |
| BUG-065 | Parse a packet carrying reserved payload version value 1. | Parsing succeeded and exposed version `1`. |
| BUG-066 | Feed ownership checks a one-byte ADVERT collision and a one-byte ACK collision. | Both unrelated packets were classified as local/own. |
| BUG-068 | Time out a dispatcher ACK wait. | One waiter remained registered after timeout. |
| BUG-070 | Compare the public-key first byte with `get_identity_address()`. | Public-key prefix and reported address differed. |
| BUG-072 | Submit 5,000 distinct malformed raw frames. | The permanent blacklist grew to 5,000 entries. |
| BUG-075 | Send a packet successfully, then inspect the dispatcher seen table. | Send succeeded; the outbound packet hash was not tracked. |
| BUG-078 | Store a 31-character name made from two-byte UTF-8 characters. | The accepted value occupied 62 wire bytes. |
| BUG-080 | Read the room-server post-length constant. | `160` characters rather than the 151-byte payload budget. |
| BUG-081 | Submit radio settings at the new validation boundaries and include `repeat=1`. | BW/SF/CR and gross frequency errors are rejected, but 100 MHz still passes and `client_repeat` remains unchanged. |
| BUG-082 | Advertise a 14 dBm backend maximum, inspect SELF_INFO, then request 22 dBm. | SELF_INFO now reports 14 dBm correctly, but the command-level generic range still accepts 22 dBm. |
| BUG-083 | Submit the three-reserved-byte self-telemetry payload. | The handler returned ILLEGAL_ARG and emitted no telemetry push. |
| BUG-084 | Submit GET_CHANNEL with no index. | The handler emitted 40 CHANNEL_INFO frames. |
| BUG-085 | Trace RAW_PACKET priority into the low-level send call. | The parsed priority was not present in `_send_packet()`. |
| BUG-086 | Use a two-byte TRACE path and inspect timeout/final-hop logic. | Timeout scaled by bytes and final-hop matching used one trailing byte. |
| BUG-087 | Submit empty SET_ADVERT_NAME and SET_FLOOD_SCOPE_KEY payloads. | Both mutated state and returned OK. |
| BUG-088 | Compare the official 0x9A setter reply with `_send_command()` acceptable responses, then deliver DATA without RX_META. | 0x9A was not accepted for SET_SIGNAL_REPORT; DATA remained queued indefinitely. |
| BUG-089 | Submit the official-rejected 32-byte SET_CHANNEL secret form. | OpenHop accepted and stored it. |
| BUG-090 | Return a custom-variable serialization whose first 140 characters are `é`. | The response carried 280 UTF-8 data bytes plus its response code. |
| BUG-091 | Push a stored post whose timestamp differs from current wall time. | Serialized plaintext used current delivery time and attempt bits `00`. |
| BUG-092 | Give a client an older unsynced post, then let it author a newer one. | The author's watermark advanced past the older post, removing it from the unsynced query. |
| BUG-093 | Inspect and invoke the registered authenticated REQ handler set for a repeater identity. | Request type `0x03` (telemetry) was absent and produced no response. |
| BUG-094 | Submit invalid UTF-8 message bytes through companion text commands. | Replacement decoding changed the original bytes before packet construction. |
| BUG-095 | Submit a direct-message body containing exactly the 12 metadata bytes and no text. | The handler called the send pipeline with an empty string and returned a sent response. |
| BUG-096 | Submit the one-byte control body `0x80`. | OpenHop returned ILLEGAL_ARG although official MeshCore accepts and sends it zero-hop. |
| BUG-097 | Submit zero-hop RAW_DATA with its four-byte minimum payload. | The initial fixed guard rejected the valid five-byte handler body before the path-aware check. |
| BUG-098 | Compare protocol-level command constants with the frame-server handler map. | REBOOT (19), SET_DEVICE_PIN (37) and FACTORY_RESET (51) were all absent while level 13 is reported. |
| BUG-099 | Emit a path-discovery push for a two-hop path using two-byte hashes. | Both encoded length fields became raw byte count `4` instead of encoded value `0x42`. |
| BUG-100 | Await `GlobalRateLimiter.acquire()` and inspect its lock immediately on return. | The lock was already released, proving the caller's transmission is outside the intended global critical section. |

BUG-067, BUG-069, BUG-071, BUG-073, BUG-074, BUG-076, BUG-077 and BUG-079 are established primarily by direct source and control-flow comparison rather than a single compact runtime assertion.

## Full-suite baseline

- OpenHop Core: **1,182 passed**.
- OpenHop Repeater: **1,193 passed, 20 subtests passed**.

Passing existing tests does not invalidate these checks. The findings cover compatibility assertions, command forms, race windows and protocol edge cases that are not represented by the current suites.

## New commit-range verification

The full transition checks for BUG-002, BUG-023, BUG-048 and BUG-060 are covered by the newly added project tests and the 259/440 changed-path test runs summarized in [NEW-COMMITS-REVIEW.md](NEW-COMMITS-REVIEW.md).

## Deeper logic recheck: BUG-101–BUG-118

The current pass used focused source assertions because several optional radio/web dependencies were unavailable in the execution environment. These checks do not replace the previously completed full suites; they isolate the exact parity predicates behind the new reports.

| Finding | Focused check | Result |
|---|---|---|
| BUG-101 | Standalone MeshNode registers group text but not group data | PASS |
| BUG-102 | Repeater pushes non-zero-hop and non-discovery CONTROL packets to companions | PASS |
| BUG-103 | The command-response waiter captures unrelated or wrong-sender messages | PASS |
| BUG-104 | CMD_ADD_UPDATE_CONTACT rejects the valid 35-byte minimum body | PASS |
| BUG-105 | Companion endpoints cannot answer peer protocol requests | PASS |
| BUG-106 | Incoming plain and signed messages do not refresh contact lastmod | PASS |
| BUG-107 | ACL role values are wire-incompatible and collapse read-only and read-write | PASS |
| BUG-108 | Room-server read-only fallback only works for blank passwords | PASS |
| BUG-109 | Room-server read-only clients can create posts | PASS |
| BUG-110 | Room-server message replays can create duplicate posts | PASS |
| BUG-111 | Repeater and room ACL identities are lost on restart | PASS |
| BUG-112 | Unsupported inbound text types are delivered as application messages | PASS |
| BUG-113 | Room-server CLI and posts are classified by text prefix instead of wire type | PASS |
| BUG-114 | Room delivery ACKs are sent before post acceptance | PASS |
| BUG-115 | Authenticated request replies wait 500 ms instead of 300 ms | PASS |
| BUG-116 | Room-server posts lose trailing whitespace | PASS |
| BUG-117 | CLI replies do not use a unique timestamp distinct from the request | PASS |
| BUG-118 | CLI command retries can execute administrative actions again | PASS |

The complete output is stored in [`DEEPER-LOGIC-CHECK-OUTPUT.txt`](DEEPER-LOGIC-CHECK-OUTPUT.txt). Core and Repeater bytecode compilation also passed.

## Continued deep review: BUG-119–BUG-124

| Finding | Focused parity predicate | Result |
|---|---|---|
| BUG-119 | Pending ACK entries are created before a text packet is successfully sent | PASS |
| BUG-120 | Successful server logins do not start keep-alive connections | PASS |
| BUG-121 | Local identities can use MeshCore-reserved 0x00 and 0xFF prefixes | PASS |
| BUG-122 | Flood forwarding retransmits RAW_CUSTOM and unknown payload types | PASS |
| BUG-123 | CMD_RESET_PATH does not persist the cleared route | PASS |
| BUG-124 | KISS fallback airtime retains a non-firmware 50 ms floor | PASS |

The complete 16-assertion output is stored in [`CONTINUED-DEEP-CHECK-OUTPUT.txt`](CONTINUED-DEEP-CHECK-OUTPUT.txt). These checks isolate the cited source behavior and do not replace physical-radio interoperability testing.

## Latest-snapshot checks for BUG-125–BUG-130

The executable focused harness is represented by the captured output in [LATEST-DEEP-CHECK-OUTPUT.txt](LATEST-DEEP-CHECK-OUTPUT.txt). It verified:

1. An unsolicited heartbeat frame `3e05000978563412` is emitted without a command.
2. A two-byte header/path-length packet is accepted with `payload_len == 0`.
3. Non-zero `total_tx`/`total_rx` become zero `sent`/`recv` fields in the packet-stats wire frame.
4. A pre-registered application callback is absent after FrameServer setup.
5. Binary/discovery ownership state has no timeout, disconnect or stop cleanup.
6. The default client idle timeout is 28,800 seconds rather than firmware-compatible `None`.
