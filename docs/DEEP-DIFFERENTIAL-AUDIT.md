# Deep differential audit report

## Scope and method

This follow-up continued the complete source-level comparison of OpenHop Core and OpenHop Repeater against the supplied official MeshCore snapshot. The previous 317-file inventory remained the baseline and every existing finding was rechecked while the review was extended through companion command edge cases, KISS modem negotiation, authenticated repeater requests, TRACE routing, room-server synchronization, byte-preservation behavior, command minimum lengths, encoded path metadata and cross-room transmission serialization.

The review used both automated inventories and manual source tracing:

1. Re-read every protocol-relevant Python source file and its official C/C++ counterpart in the existing file matrix.
2. Compared every companion command branch, minimum length, optional field, response count and serialized limit.
3. Traced radio configuration capabilities from SELF_INFO through mutation handlers and backend application.
4. Compared KISS request/response IDs and receive delivery with signal metadata both enabled and disabled.
5. Re-audited TRACE hash-width handling, timeout hints and low-level TX priority propagation.
6. Replayed room-server post insertion, delivery, ACK and sync-watermark state transitions.
7. Compared authenticated repeater REQ handler registration against the official status, telemetry, ACL, neighbours and owner-info request set.
8. Rechecked all archived fixed findings for regression and applied maintainer decisions to intentional host-side policy differences.
9. Ran the complete available Core and Repeater test suites and focused deterministic reproductions.

The file-level disposition is recorded in [FILE-REVIEW-MATRIX.md](FILE-REVIEW-MATRIX.md). Focused executable checks are summarized in [REPRODUCTION-CHECKS.md](REPRODUCTION-CHECKS.md).

## Snapshot result

- **57** defect findings remain fully fixed in `archive/findings/`.
- **1** numbered report, BUG-023, is now archived as an intentional routing-policy divergence under evaluation.
- **5** active findings remain partially fixed: BUG-002, BUG-022, BUG-048, BUG-054 and BUG-060.
- **37** active findings are not fixed.
- **20** additional unintentional differences were confirmed in this deeper follow-up.
- No fully fixed archived finding regressed in the supplied snapshots.

## Maintainer clarification applied to BUG-023

RightUp clarified that OpenHop deliberately uses a separately designed, MeshCore-inspired neighbour score and report. Like official MeshCore, reception-quality routing is disabled by default. The score is intentionally observational while real data is collected, and no decision has yet been made about allowing it to influence flood forwarding. BUG-023 has therefore been moved to `archive/intentional/` and is excluded from active-defect counts.

## Newly confirmed in this deeper follow-up

| Finding | Severity | Area | Summary |
|---|---|---|---|
| [BUG-081](../findings/BUG-081-cmd-set-radio-params-cannot-enable-client-repeat-and-accepts-out-of-range-frequencies.md) | High | Companion radio configuration | CMD_SET_RADIO_PARAMS cannot enable client repeat and accepts out-of-range frequencies |
| [BUG-082](../findings/BUG-082-cmd-set-radio-tx-power-ignores-the-advertised-hardware-limit.md) | Medium | Companion radio configuration | CMD_SET_RADIO_TX_POWER ignores the advertised hardware limit |
| [BUG-083](../findings/BUG-083-cmd-send-telemetry-req-rejects-meshcore-s-self-telemetry-form.md) | Medium | Companion telemetry | CMD_SEND_TELEMETRY_REQ rejects MeshCore's self-telemetry form |
| [BUG-084](../findings/BUG-084-index-less-cmd-get-channel-emits-a-multi-frame-dump-absent-from-meshcore.md) | Medium | Companion channel protocol | Index-less CMD_GET_CHANNEL emits a multi-frame dump absent from MeshCore |
| [BUG-085](../findings/BUG-085-cmd-send-raw-packet-discards-the-requested-transmit-priority.md) | Medium | Companion raw transmission | CMD_SEND_RAW_PACKET discards the requested transmit priority |
| [BUG-086](../findings/BUG-086-cmd-send-trace-path-miscomputes-multi-byte-route-completion-and-timeout-hints.md) | Medium | TRACE routing | CMD_SEND_TRACE_PATH miscomputes multi-byte route completion and timeout hints |
| [BUG-087](../findings/BUG-087-short-companion-commands-are-accepted-and-can-silently-mutate-device-state.md) | Medium | Companion frame validation | Short companion commands are accepted and can silently mutate device state |
| [BUG-088](../findings/BUG-088-kiss-signal-report-negotiation-can-stall-all-received-packet-delivery.md) | High | KISS modem transport | KISS signal-report negotiation can stall all received packet delivery |
| [BUG-089](../findings/BUG-089-cmd-set-channel-accepts-secret-encodings-that-meshcore-explicitly-rejects.md) | Medium | Companion channel protocol | CMD_SET_CHANNEL accepts secret encodings that MeshCore explicitly rejects |
| [BUG-090](../findings/BUG-090-cmd-get-custom-vars-applies-its-140-byte-limit-before-utf-8-encoding.md) | Low | Companion custom variables | CMD_GET_CUSTOM_VARS applies its 140-byte limit before UTF-8 encoding |
| [BUG-091](../findings/BUG-091-room-server-pushes-replace-the-post-timestamp-and-omit-retry-attempt-entropy.md) | Medium | Room server delivery | Room-server pushes replace the post timestamp and omit retry-attempt entropy |
| [BUG-092](../findings/BUG-092-posting-to-a-room-can-skip-older-unsynced-messages-for-the-author.md) | High | Room server synchronization | Posting to a room can skip older unsynced messages for the author |
| [BUG-093](../findings/BUG-093-the-repeater-does-not-implement-meshcore-telemetry-req-responses.md) | High | Authenticated repeater requests | The repeater does not implement MeshCore telemetry REQ responses |
| [BUG-094](../findings/BUG-094-companion-text-commands-rewrite-invalid-utf-8-payload-bytes.md) | Low | Companion text serialization | Companion text commands rewrite invalid UTF-8 payload bytes |
| [BUG-095](../findings/BUG-095-cmd-send-txt-msg-accepts-a-direct-message-with-no-text-byte.md) | Low | Companion text validation | CMD_SEND_TXT_MSG accepts a direct message with no text byte |
| [BUG-096](../findings/BUG-096-cmd-send-control-data-rejects-meshcore-s-minimum-one-byte-control-payload.md) | Medium | Companion control data | CMD_SEND_CONTROL_DATA rejects MeshCore's minimum one-byte control payload |
| [BUG-097](../findings/BUG-097-cmd-send-raw-data-rejects-the-valid-zero-hop-four-byte-minimum-payload.md) | Medium | Companion raw data | CMD_SEND_RAW_DATA rejects the valid zero-hop four-byte minimum payload |
| [BUG-098](../findings/BUG-098-protocol-level-13-is-reported-while-reboot-device-pin-and-factory-reset-commands-are-absent.md) | Medium | Companion command coverage | Protocol level 13 is reported while reboot, device-PIN and factory-reset commands are absent |
| [BUG-099](../findings/BUG-099-path-discovery-pushes-replace-encoded-path-lengths-with-raw-byte-counts.md) | High | Companion path discovery | Path-discovery pushes replace encoded path lengths with raw byte counts |
| [BUG-100](../findings/BUG-100-the-global-room-server-rate-limiter-releases-its-lock-before-transmission-begins.md) | High | Room server scheduling | The global room-server rate limiter releases its lock before transmission begins |

## Highest-risk follow-up mismatches

- **BUG-081:** companion radio settings advertise client-repeat state but cannot configure or enact it, and accept an official-invalid frequency range.
- **BUG-088:** KISS signal-report negotiation cannot match the official setter response; disabled metadata can leave every DATA frame undelivered.
- **BUG-092:** authoring a new room post can move the sync watermark past an older undelivered post.
- **BUG-093:** authenticated repeater telemetry requests are consumed without the official CayenneLPP response.
- **BUG-099:** multi-byte path-discovery routes are exposed to companion apps with corrupt hop-count/hash-width metadata.
- **BUG-100:** multiple room identities can enter overlapping push/ACK workflows because the shared limiter never holds its lock across transmission.

## Tests

- OpenHop Core: `1110 passed`.
- OpenHop Repeater: `1136 passed, 20 subtests passed`.

Passing tests do not negate the findings. The new cases concern missing command forms, byte-level compatibility, capability inconsistencies and state transitions that are not represented by the current suites.
