# OpenHop / MeshCore Full Differential Audit

A source-level interoperability audit of OpenHop Core and OpenHop Repeater against the official MeshCore firmware. The review covers the complete supplied protocol-relevant source snapshots, including packet encoding, cryptography, routing, forwarding, ACK/PATH behavior, companion framing, room-server behavior, radio scheduling, persistence, CLI and telemetry.

The audit distinguishes between **protocol defects** and **intentional host-side differences**. A larger cache, queue or database is not treated as a defect merely because firmware uses a smaller embedded structure, provided the host implementation remains bounded, safe and interoperable.

## Audited snapshots

| Project | Snapshot | Notes |
|---|---|---|
| OpenHop Core | [`9ea7269`](https://github.com/openhop-dev/openhop_core/commit/9ea7269a7e7e903fe433b1f952a4026fe3dcc81b) | Version `1.1.3.dev6`; functional code is unchanged from `9355d08` |
| OpenHop Repeater | [`6aafa7f`](https://github.com/openhop-dev/openhop_repeater/commit/6aafa7fe991b5b3199b18149f84417f8522d94b2) | Supplied ZIP; later online branch commits were not used as the source of truth |
| MeshCore | `v1.16.0` snapshot | Official comparison implementation; companion protocol level 13 |

Exact ZIP hashes are recorded in [AUDIT-SNAPSHOT.txt](AUDIT-SNAPSHOT.txt).

## Results

| Metric | Count |
|---|---:|
| Total audit reports | **100** |
| Confirmed defect findings | **99** |
| Newly confirmed in the original full pass | **17** |
| Newly confirmed in this deeper follow-up | **20** |
| Archived as fully fixed | **57** |
| Archived intentional divergences | **1** |
| Active defects | **42** |
| Active: partially fixed | **5** |
| Active: not fixed | **37** |
| Core Python source files reviewed | **87** |
| Repeater Python source files reviewed | **66** |
| MeshCore C/C++ and header reference files reviewed | **164** |
| Protocol-relevant source lines indexed | **95,241** |
| Core tests | **1,110 passed** |
| Repeater tests | **1,136 passed + 20 subtests passed** |

The [file review matrix](docs/FILE-REVIEW-MATRIX.md) records every reviewed source file and the finding IDs associated with it.
Focused runtime reproductions are recorded in [REPRODUCTION-CHECKS.md](docs/REPRODUCTION-CHECKS.md).

## Active findings

| Finding | Severity | Area | Components | Summary |
|---|---|---|---|---|
| 🟡 [BUG-002](findings/BUG-002-packet-payload-limit-is-larger-than-meshcore-s-wire-limit.md) | Medium | Packet format | OpenHop Core | Packet payload limit is larger than MeshCore's wire limit |
| 🟡 [BUG-022](findings/BUG-022-multipart-packets-and-routed-acks-lack-their-special-forwarding-paths.md) | High | Mesh routing | OpenHop Repeater | Multipart packets and routed ACKs lack their special forwarding paths |
| 🟡 [BUG-048](findings/BUG-048-lora-airtime-calculations-use-incompatible-coding-rate-representations.md) | High | Radio timing | OpenHop Core | LoRa airtime calculations use incompatible coding-rate representations |
| 🟡 [BUG-054](findings/BUG-054-unsupported-radio-changes-report-success-for-virtual-companions.md) | Medium | Companion/repeater integration | OpenHop Core, OpenHop Repeater | Unsupported radio changes report success for virtual companions |
| 🟡 [BUG-060](findings/BUG-060-the-sqlite-queue-loses-binary-payload-signed-sender-and-signal-metadata.md) | High | Repeater companion persistence | OpenHop Repeater | The SQLite queue loses binary payload, signed sender, and signal metadata |
| 🔴 [BUG-064](findings/BUG-064-the-exported-cipher-mac-size-is-32-bytes-instead-of-2.md) | Low | Protocol constants | OpenHop Core | The exported cipher MAC size is 32 bytes instead of 2 |
| 🔴 [BUG-065](findings/BUG-065-reserved-payload-version-1-is-accepted-as-a-supported-wire-format.md) | Medium | Packet parsing | OpenHop Core | Reserved payload version 1 is accepted as a supported wire format |
| 🔴 [BUG-066](findings/BUG-066-the-generic-own-packet-filter-drops-valid-packets-on-one-byte-collisions.md) | High | Receive filtering | OpenHop Core | The generic own-packet filter drops valid packets on one-byte collisions |
| 🔴 [BUG-067](findings/BUG-067-advert-timestamps-share-the-global-unique-request-clock-and-can-run-into-the-future.md) | Medium | Advertisement timestamps | OpenHop Core | Advert timestamps share the global unique-request clock and can run into the future |
| 🔴 [BUG-068](findings/BUG-068-timed-out-dispatcher-ack-waiters-are-never-removed.md) | Medium | ACK lifecycle | OpenHop Core | Timed-out dispatcher ACK waiters are never removed |
| 🔴 [BUG-069](findings/BUG-069-has-connection-and-get-tuning-params-are-advertised-but-unimplemented.md) | Medium | Companion command coverage | OpenHop Core | HAS_CONNECTION and GET_TUNING_PARAMS are advertised but unimplemented |
| 🔴 [BUG-070](findings/BUG-070-identity-addresses-hash-the-public-key-instead-of-using-its-prefix.md) | Low | Identity addressing | OpenHop Core + Repeater | Identity addresses hash the public key instead of using its prefix |
| 🔴 [BUG-071](findings/BUG-071-repeater-status-hardcodes-tx-queue-depth-and-error-events-to-zero.md) | Low | Repeater telemetry | OpenHop Repeater | Repeater status hardcodes TX queue depth and error events to zero |
| 🔴 [BUG-072](findings/BUG-072-malformed-frame-blacklist-storage-is-permanent-and-unbounded.md) | Medium | Malformed packet handling | OpenHop Core | Malformed-frame blacklist storage is permanent and unbounded |
| 🔴 [BUG-073](findings/BUG-073-self-info-omits-the-configured-environment-telemetry-bits.md) | Low | Companion SELF_INFO | OpenHop Core | SELF_INFO omits the configured environment telemetry bits |
| 🔴 [BUG-074](findings/BUG-074-cmd-send-txt-msg-accepts-reserved-text-type-values.md) | Medium | Companion text sending | OpenHop Core | CMD_SEND_TXT_MSG accepts reserved text-type values |
| 🔴 [BUG-075](findings/BUG-075-outbound-packets-are-not-recorded-in-the-dispatcher-seen-table.md) | High | Loopback suppression | OpenHop Core | Outbound packets are not recorded in the dispatcher seen table |
| 🔴 [BUG-076](findings/BUG-076-concurrent-receive-tasks-race-replay-state-and-reorder-protocol-handling.md) | High | Receive scheduling | OpenHop Core | Concurrent receive tasks race replay state and reorder protocol handling |
| 🔴 [BUG-077](findings/BUG-077-standalone-core-lacks-meshcore-s-rolling-transmit-airtime-budget.md) | High | Transmit scheduling | OpenHop Core | Standalone Core lacks MeshCore’s rolling transmit-airtime budget |
| 🔴 [BUG-078](findings/BUG-078-companion-node-names-are-limited-by-characters-instead-of-the-31-byte-field.md) | Low | Companion naming | OpenHop Core | Companion node names are limited by characters instead of the 31-byte field |
| 🔴 [BUG-079](findings/BUG-079-exposed-repeater-cli-maintenance-commands-remain-no-op-stubs.md) | Low | Repeater CLI | OpenHop Repeater | Exposed repeater CLI maintenance commands remain no-op stubs |
| 🔴 [BUG-080](findings/BUG-080-room-server-post-length-uses-160-characters-instead-of-151-wire-bytes.md) | Medium | Room server messages | OpenHop Repeater | Room-server post length uses 160 characters instead of 151 wire bytes |
| 🔴 [BUG-081](findings/BUG-081-cmd-set-radio-params-cannot-enable-client-repeat-and-accepts-out-of-range-frequencies.md) | High | Companion radio configuration | OpenHop Core | CMD_SET_RADIO_PARAMS cannot enable client repeat and accepts out-of-range frequencies |
| 🔴 [BUG-082](findings/BUG-082-cmd-set-radio-tx-power-ignores-the-advertised-hardware-limit.md) | Medium | Companion radio configuration | OpenHop Core | CMD_SET_RADIO_TX_POWER ignores the advertised hardware limit |
| 🔴 [BUG-083](findings/BUG-083-cmd-send-telemetry-req-rejects-meshcore-s-self-telemetry-form.md) | Medium | Companion telemetry | OpenHop Core | CMD_SEND_TELEMETRY_REQ rejects MeshCore's self-telemetry form |
| 🔴 [BUG-084](findings/BUG-084-index-less-cmd-get-channel-emits-a-multi-frame-dump-absent-from-meshcore.md) | Medium | Companion channel protocol | OpenHop Core | Index-less CMD_GET_CHANNEL emits a multi-frame dump absent from MeshCore |
| 🔴 [BUG-085](findings/BUG-085-cmd-send-raw-packet-discards-the-requested-transmit-priority.md) | Medium | Companion raw transmission | OpenHop Core | CMD_SEND_RAW_PACKET discards the requested transmit priority |
| 🔴 [BUG-086](findings/BUG-086-cmd-send-trace-path-miscomputes-multi-byte-route-completion-and-timeout-hints.md) | Medium | TRACE routing | OpenHop Core | CMD_SEND_TRACE_PATH miscomputes multi-byte route completion and timeout hints |
| 🔴 [BUG-087](findings/BUG-087-short-companion-commands-are-accepted-and-can-silently-mutate-device-state.md) | Medium | Companion frame validation | OpenHop Core | Short companion commands are accepted and can silently mutate device state |
| 🔴 [BUG-088](findings/BUG-088-kiss-signal-report-negotiation-can-stall-all-received-packet-delivery.md) | High | KISS modem transport | OpenHop Core | KISS signal-report negotiation can stall all received packet delivery |
| 🔴 [BUG-089](findings/BUG-089-cmd-set-channel-accepts-secret-encodings-that-meshcore-explicitly-rejects.md) | Medium | Companion channel protocol | OpenHop Core | CMD_SET_CHANNEL accepts secret encodings that MeshCore explicitly rejects |
| 🔴 [BUG-090](findings/BUG-090-cmd-get-custom-vars-applies-its-140-byte-limit-before-utf-8-encoding.md) | Low | Companion custom variables | OpenHop Core | CMD_GET_CUSTOM_VARS applies its 140-byte limit before UTF-8 encoding |
| 🔴 [BUG-091](findings/BUG-091-room-server-pushes-replace-the-post-timestamp-and-omit-retry-attempt-entropy.md) | Medium | Room server delivery | OpenHop Repeater | Room-server pushes replace the post timestamp and omit retry-attempt entropy |
| 🔴 [BUG-092](findings/BUG-092-posting-to-a-room-can-skip-older-unsynced-messages-for-the-author.md) | High | Room server synchronization | OpenHop Repeater | Posting to a room can skip older unsynced messages for the author |
| 🔴 [BUG-093](findings/BUG-093-the-repeater-does-not-implement-meshcore-telemetry-req-responses.md) | High | Authenticated repeater requests | OpenHop Repeater | The repeater does not implement MeshCore telemetry REQ responses |
| 🔴 [BUG-094](findings/BUG-094-companion-text-commands-rewrite-invalid-utf-8-payload-bytes.md) | Low | Companion text serialization | OpenHop Core | Companion text commands rewrite invalid UTF-8 payload bytes |
| 🔴 [BUG-095](findings/BUG-095-cmd-send-txt-msg-accepts-a-direct-message-with-no-text-byte.md) | Low | Companion text validation | OpenHop Core | CMD_SEND_TXT_MSG accepts a direct message with no text byte |
| 🔴 [BUG-096](findings/BUG-096-cmd-send-control-data-rejects-meshcore-s-minimum-one-byte-control-payload.md) | Medium | Companion control data | OpenHop Core | CMD_SEND_CONTROL_DATA rejects MeshCore's minimum one-byte control payload |
| 🔴 [BUG-097](findings/BUG-097-cmd-send-raw-data-rejects-the-valid-zero-hop-four-byte-minimum-payload.md) | Medium | Companion raw data | OpenHop Core | CMD_SEND_RAW_DATA rejects the valid zero-hop four-byte minimum payload |
| 🔴 [BUG-098](findings/BUG-098-protocol-level-13-is-reported-while-reboot-device-pin-and-factory-reset-commands-are-absent.md) | Medium | Companion command coverage | OpenHop Core | Protocol level 13 is reported while reboot, device-PIN and factory-reset commands are absent |
| 🔴 [BUG-099](findings/BUG-099-path-discovery-pushes-replace-encoded-path-lengths-with-raw-byte-counts.md) | High | Companion path discovery | OpenHop Core | Path-discovery pushes replace encoded path lengths with raw byte counts |
| 🔴 [BUG-100](findings/BUG-100-the-global-room-server-rate-limiter-releases-its-lock-before-transmission-begins.md) | High | Room server scheduling | OpenHop Repeater | The global room-server rate limiter releases its lock before transmission begins |

## Intentional divergences

The report below remains part of the numbered audit history but is not counted as an active defect. The maintainer has confirmed that the different policy is deliberate and still under data-driven evaluation.

| Finding | Classification | Area | Components | Summary |
|---|---|---|---|---|
| ⚪ [BUG-023](archive/intentional/findings/BUG-023-flood-packets-bypass-meshcore-s-reception-quality-delay.md) | Intentional / under evaluation | Radio receive scheduling | OpenHop Core, OpenHop Repeater | Reception-quality scoring is observational and deliberately not yet connected to flood routing |

## Archived findings

The reports below remain available as historical evidence, but their audited defect is fully fixed in the supplied snapshots. Their implementation sketches have also been moved to `archive/patches/`. Intentional divergences are archived separately under `archive/intentional/` and are not included in this fixed table.

| Finding | Severity | Area | Components | Summary |
|---|---|---|---|---|
| ✅ [BUG-001](archive/findings/BUG-001-advert-application-data-exceeds-the-meshcore-limit.md) | Medium | Packet format | OpenHop Core | Advert application data exceeds the MeshCore limit |
| ✅ [BUG-003](archive/findings/BUG-003-malformed-advert-optional-fields-are-accepted-and-misaligned.md) | Medium | Advert parsing | OpenHop Core | Malformed advert optional fields are accepted and misaligned |
| ✅ [BUG-004](archive/findings/BUG-004-invalid-utf-8-advert-names-discard-otherwise-valid-adverts.md) | Low | Advert parsing | OpenHop Core | Invalid UTF-8 advert names discard otherwise valid adverts |
| ✅ [BUG-005](archive/findings/BUG-005-advert-names-are-trimmed-during-parsing.md) | Low | Advert name parsing | OpenHop Core | Advert names are trimmed during parsing |
| ✅ [BUG-006](archive/findings/BUG-006-empty-path-returns-omit-meshcore-s-random-uniqueness-filler.md) | Medium | Encrypted packet construction | OpenHop Core | Empty PATH returns omit MeshCore's random uniqueness filler |
| ✅ [BUG-007](archive/findings/BUG-007-group-binary-data-is-encrypted-with-the-wrong-aes-key.md) | High | Group encryption | OpenHop Core | Group binary data is encrypted with the wrong AES key |
| ✅ [BUG-008](archive/findings/BUG-008-group-binary-data-over-165-bytes-is-accepted.md) | Low | Group packet construction | OpenHop Core | Group binary data over 165 bytes is accepted |
| ✅ [BUG-009](archive/findings/BUG-009-direct-messages-are-not-capped-at-160-bytes.md) | Medium | Text packet construction | OpenHop Core | Direct messages are not capped at 160 bytes |
| ✅ [BUG-010](archive/findings/BUG-010-text-attempt-numbers-above-three-are-discarded.md) | Medium | Text retry encoding | OpenHop Core | Text attempt numbers above three are discarded |
| ✅ [BUG-011](archive/findings/BUG-011-aes-padding-and-extended-attempt-metadata-are-delivered-as-message-text.md) | High | Text receive parsing | OpenHop Core | AES padding and extended-attempt metadata are delivered as message text |
| ✅ [BUG-012](archive/findings/BUG-012-login-passwords-are-truncated-by-characters-instead-of-bytes.md) | Low | Login request construction | OpenHop Core | Login passwords are truncated by characters instead of bytes |
| ✅ [BUG-013](archive/findings/BUG-013-the-valid-coordinate-0-0-is-omitted-from-adverts.md) | Low | Self advertisement | OpenHop Core | The valid coordinate (0, 0) is omitted from adverts |
| ✅ [BUG-014](archive/findings/BUG-014-older-advertisements-can-overwrite-newer-contacts.md) | High | Contact synchronization | OpenHop Core | Older advertisements can overwrite newer contacts |
| ✅ [BUG-015](archive/findings/BUG-015-group-text-attempt-bits-are-interpreted-as-message-subtypes.md) | High | Group text receive parsing | OpenHop Core | Group-text attempt bits are interpreted as message subtypes |
| ✅ [BUG-016](archive/findings/BUG-016-group-messages-are-suppressed-when-a-peer-shares-the-local-display-name.md) | Medium | Group message delivery | OpenHop Core | Group messages are suppressed when a peer shares the local display name |
| ✅ [BUG-017](archive/findings/BUG-017-transport-scoped-flood-dms-are-classified-as-direct.md) | High | Text receive routing | OpenHop Core | Transport-scoped flood DMs are classified as direct |
| ✅ [BUG-018](archive/findings/BUG-018-delivery-acks-use-route-timeout-calculations-instead-of-the-200-ms-delay.md) | Medium | ACK scheduling | OpenHop Core | Delivery ACKs use route timeout calculations instead of the 200 ms delay |
| ✅ [BUG-019](archive/findings/BUG-019-synchronous-text-sends-wait-for-the-wrong-ack-identifier.md) | High | ACK correlation | OpenHop Core | Synchronous text sends wait for the wrong ACK identifier |
| ✅ [BUG-020](archive/findings/BUG-020-path-ack-decryption-tries-only-one-colliding-contact.md) | Medium | PATH and ACK parsing | OpenHop Core | PATH ACK decryption tries only one colliding contact |
| ✅ [BUG-021](archive/findings/BUG-021-pending-ack-storage-is-an-unbounded-time-set-with-silent-saturation.md) | Low | ACK state | OpenHop Core | Pending ACK storage is an unbounded-time set with silent saturation |
| ✅ [BUG-024](archive/findings/BUG-024-server-side-req-replay-protection-is-absent.md) | High | Server-side REQ security | OpenHop Core | Server-side REQ replay protection is absent |
| ✅ [BUG-025](archive/findings/BUG-025-response-waiters-are-keyed-by-a-one-byte-contact-prefix.md) | Medium | Request/response correlation | OpenHop Core | Response waiters are keyed by a one-byte contact prefix |
| ✅ [BUG-026](archive/findings/BUG-026-path-discovery-can-remain-direct-after-the-contact-is-forced-to-flood.md) | High | Path discovery | OpenHop Core | Path discovery can remain direct after the contact is forced to flood |
| ✅ [BUG-027](archive/findings/BUG-027-path-discovery-builds-the-wrong-request-body-and-tracks-the-wrong-tag.md) | High | Path discovery | OpenHop Core | Path discovery builds the wrong request body and tracks the wrong tag |
| ✅ [BUG-028](archive/findings/BUG-028-a-zero-hop-direct-binary-request-is-reported-as-flood.md) | Low | Companion response metadata | OpenHop Core | A zero-hop direct binary request is reported as flood |
| ✅ [BUG-029](archive/findings/BUG-029-control-packets-are-accepted-on-non-direct-routes.md) | Medium | Control packet dispatch | OpenHop Core | CONTROL packets are accepted on non-direct routes |
| ✅ [BUG-030](archive/findings/BUG-030-a-private-region-without-stored-keys-becomes-a-public-hashtag-scope.md) | Medium | Transport regions | OpenHop Core | A private region without stored keys becomes a public hashtag scope |
| ✅ [BUG-031](archive/findings/BUG-031-contacts-start-reports-the-filtered-result-count.md) | Low | Companion contact synchronization | OpenHop Core | CONTACTS_START reports the filtered result count |
| ✅ [BUG-032](archive/findings/BUG-032-encoded-contact-path-length-is-parsed-as-signed.md) | High | Companion contact storage | OpenHop Core | Encoded contact path length is parsed as signed |
| ✅ [BUG-033](archive/findings/BUG-033-valid-zero-bytes-are-stripped-from-stored-paths.md) | High | Companion contact storage | OpenHop Core | Valid zero bytes are stripped from stored paths |
| ✅ [BUG-034](archive/findings/BUG-034-contact-exchange-does-not-preserve-signed-advert-packets.md) | High | Companion contact exchange | OpenHop Core, OpenHop Repeater | Contact exchange does not preserve signed ADVERT packets |
| ✅ [BUG-035](archive/findings/BUG-035-share-contact-maps-send-failure-to-not-found.md) | Low | Companion command responses | OpenHop Core | SHARE_CONTACT maps send failure to NOT_FOUND |
| ✅ [BUG-036](archive/findings/BUG-036-incoming-direct-message-path-metadata-is-hardcoded-to-zero.md) | Medium | Companion offline messages | OpenHop Core | Incoming direct-message path metadata is hardcoded to zero |
| ✅ [BUG-037](archive/findings/BUG-037-offline-queues-can-discard-direct-messages.md) | Medium | Companion offline messages | OpenHop Core, OpenHop Repeater | Offline queues can discard direct messages |
| ✅ [BUG-038](archive/findings/BUG-038-auto-add-maximum-hops-is-neither-stored-nor-enforced.md) | Medium | Companion contact policy | OpenHop Core | Auto-add maximum hops is neither stored nor enforced |
| ✅ [BUG-039](archive/findings/BUG-039-send-confirmed-always-reports-zero-trip-time.md) | Low | Companion ACK events | OpenHop Core | SEND_CONFIRMED always reports zero trip time |
| ✅ [BUG-040](archive/findings/BUG-040-app-start-overwrites-protocol-version-from-a-reserved-byte-and-accepts-short-frames.md) | Medium | Companion session negotiation | OpenHop Core | APP_START overwrites protocol version from a reserved byte and accepts short frames |
| ✅ [BUG-041](archive/findings/BUG-041-self-info-reports-a-hardcoded-maximum-tx-power.md) | Low | Companion SELF_INFO | OpenHop Core, OpenHop Repeater | SELF_INFO reports a hardcoded maximum TX power |
| ✅ [BUG-042](archive/findings/BUG-042-disabled-private-key-import-is-acknowledged-as-successful.md) | Medium | Companion key management | OpenHop Core | Disabled private-key import is acknowledged as successful |
| ✅ [BUG-043](archive/findings/BUG-043-the-implemented-companion-signing-pipeline-is-unreachable.md) | Medium | Companion signing | OpenHop Core | The implemented companion signing pipeline is unreachable |
| ✅ [BUG-044](archive/findings/BUG-044-outbound-companion-payloads-are-truncated-at-173-instead-of-176-bytes.md) | Low | Companion framing | OpenHop Core | Outbound companion payloads are truncated at 173 instead of 176 bytes |
| ✅ [BUG-045](archive/findings/BUG-045-login-status-and-telemetry-commands-report-sent-before-attempting-the-send.md) | Medium | Companion command responses | OpenHop Core | Login, status, and telemetry commands report SENT before attempting the send |
| ✅ [BUG-046](archive/findings/BUG-046-companion-send-failures-use-the-wrong-error-classes.md) | Low | Companion command responses | OpenHop Core | Companion send failures use the wrong error classes |
| ✅ [BUG-047](archive/findings/BUG-047-short-set-other-params-frames-reset-fields-they-should-preserve.md) | Medium | Companion preferences | OpenHop Core | Short SET_OTHER_PARAMS frames reset fields they should preserve |
| ✅ [BUG-049](archive/findings/BUG-049-maximum-length-valid-direct-paths-are-rejected.md) | Medium | Core/repeater routing | OpenHop Core, OpenHop Repeater | Maximum-length valid direct paths are rejected |
| ✅ [BUG-050](archive/findings/BUG-050-transport-flood-and-direct-routes-use-incorrect-retransmit-delays.md) | High | Repeater timing | OpenHop Repeater | Transport flood and direct routes use incorrect retransmit delays |
| ✅ [BUG-051](archive/findings/BUG-051-loop-thresholds-ignore-path-hash-width.md) | Low | Repeater loop detection | OpenHop Repeater | Loop thresholds ignore path-hash width |
| ✅ [BUG-052](archive/findings/BUG-052-advert-sends-report-success-after-failure-and-bypass-the-repeater-engine.md) | Medium | Repeater outbound adverts | OpenHop Repeater | Advert sends report success after failure and bypass the repeater engine |
| ✅ [BUG-053](archive/findings/BUG-053-destination-prefix-matches-claim-packets-before-mac-verification.md) | High | Repeater authenticated routing | OpenHop Core, OpenHop Repeater | Destination-prefix matches claim packets before MAC verification |
| ✅ [BUG-055](archive/findings/BUG-055-missing-advert-limiter-configuration-falls-back-to-forwarding-blocking-defaults.md) | Medium | Repeater advert forwarding | OpenHop Repeater | Missing advert-limiter configuration falls back to forwarding-blocking defaults |
| ✅ [BUG-056](archive/findings/BUG-056-configuring-a-companion-makes-the-repeater-path-handler-unreachable.md) | High | Repeater PATH dispatch | OpenHop Repeater | Configuring a companion makes the repeater PATH handler unreachable |
| ✅ [BUG-057](archive/findings/BUG-057-pathhelper-treats-encoded-path-len-as-a-byte-count.md) | High | Repeater PATH parsing | OpenHop Repeater | PathHelper treats encoded path_len as a byte count |
| ✅ [BUG-058](archive/findings/BUG-058-a-locally-authenticated-path-packet-is-still-forwarded.md) | Medium | Repeater PATH routing | OpenHop Repeater | A locally authenticated PATH packet is still forwarded |
| ✅ [BUG-059](archive/findings/BUG-059-local-one-byte-identity-collisions-overwrite-routing-and-persistence-state.md) | High | Repeater multi-identity lifecycle | OpenHop Repeater | Local one-byte identity collisions overwrite routing and persistence state |
| ✅ [BUG-061](archive/findings/BUG-061-grp-data-and-raw-custom-are-not-delivered-to-companion-bridges.md) | High | Repeater companion packet routing | OpenHop Repeater | GRP_DATA and RAW_CUSTOM are not delivered to companion bridges |
| ✅ [BUG-062](archive/findings/BUG-062-payload-handlers-run-before-a-direct-packet-reaches-its-final-destination.md) | High | Repeater routing order | OpenHop Repeater | Payload handlers run before a direct packet reaches its final destination |
| ✅ [BUG-063](archive/findings/BUG-063-preloaded-sqlite-messages-are-delivered-twice-after-restart.md) | Medium | Repeater companion persistence | OpenHop Repeater | Preloaded SQLite messages are delivered twice after restart |

## Supporting documents

- [Deep differential audit report](docs/DEEP-DIFFERENTIAL-AUDIT.md)
- [File-by-file review matrix](docs/FILE-REVIEW-MATRIX.md)
- [Intentional differences and non-findings](docs/INTENTIONAL-DIFFERENCES.md)
- [Claim verification](docs/CLAIM-VERIFICATION.md)
- [Verification notes](docs/VERIFICATION-NOTES.md)
- [Archived findings guide](archive/README.md)
- [Active patch-sketch disclaimer](patches/README.md)

## Interpretation of statuses

- **✅ Fully fixed:** the originally reported mismatch is absent and no regression was found.
- **🟡 Partially fixed:** meaningful corrective work exists, but at least one interoperability path remains incomplete.
- **🔴 Not fixed:** the mismatch remains reproducible from the supplied source.
- **⚪ Intentional divergence:** the behavior differs deliberately and is not classified as a defect under the current maintainer decision.

All patch files are LLM-generated implementation sketches. They are not ready-to-apply changes and must be independently rewritten, tested and reviewed.
