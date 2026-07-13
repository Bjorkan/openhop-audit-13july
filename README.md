# OpenHop Compatibility Audit

A source-level audit of the combined OpenHop Core and OpenHop Repeater stack against the official MeshCore implementation.

Each confirmed defect has one Markdown file. A report includes both Core and Repeater changes when the fix crosses repository boundaries. Every report also links to an annotated, LLM-generated implementation sketch in `patches/` showing the likely files and before/after code shape. These sketches are not reviewed, tested, or ready to apply directly; they are only an approximate guide to the work a maintainer may need to perform. Every report also links to an annotated, LLM-generated implementation sketch in `patches/` showing the likely files and before/after code shape. These sketches are not reviewed, tested, or ready to apply directly; they are only an approximate guide to the work a maintainer may need to perform.

## At a glance

| Metric | Count |
|---|---:|
| Confirmed bugs | **63** |
| High severity | **22** |
| Medium severity | **27** |
| Low severity | **14** |
| Bugs involving OpenHop Core | **50** |
| Bugs involving OpenHop Repeater | **19** |

## Bug list

| Bug | Severity | Area | Components | Summary |
|---|---|---|---|---|
| [BUG-001](findings/BUG-001-advert-application-data-exceeds-the-meshcore-limit.md) | Medium | Packet format | Core | Advert application data exceeds the MeshCore limit |
| [BUG-002](findings/BUG-002-packet-payload-limit-is-larger-than-meshcore-s-wire-limit.md) | Medium | Packet format | Core | Packet payload limit is larger than MeshCore's wire limit |
| [BUG-003](findings/BUG-003-malformed-advert-optional-fields-are-accepted-and-misaligned.md) | Medium | Advert parsing | Core | Malformed advert optional fields are accepted and misaligned |
| [BUG-004](findings/BUG-004-invalid-utf-8-advert-names-discard-otherwise-valid-adverts.md) | Low | Advert parsing | Core | Invalid UTF-8 advert names discard otherwise valid adverts |
| [BUG-005](findings/BUG-005-advert-names-are-trimmed-during-parsing.md) | Low | Advert name parsing | Core | Advert names are trimmed during parsing |
| [BUG-006](findings/BUG-006-empty-path-returns-omit-meshcore-s-random-uniqueness-filler.md) | Medium | Encrypted packet construction | Core | Empty PATH returns omit MeshCore's random uniqueness filler |
| [BUG-007](findings/BUG-007-group-binary-data-is-encrypted-with-the-wrong-aes-key.md) | High | Group encryption | Core | Group binary data is encrypted with the wrong AES key |
| [BUG-008](findings/BUG-008-group-binary-data-over-165-bytes-is-accepted.md) | Low | Group packet construction | Core | Group binary data over 165 bytes is accepted |
| [BUG-009](findings/BUG-009-direct-messages-are-not-capped-at-160-bytes.md) | Medium | Text packet construction | Core | Direct messages are not capped at 160 bytes |
| [BUG-010](findings/BUG-010-text-attempt-numbers-above-three-are-discarded.md) | Medium | Text retry encoding | Core | Text attempt numbers above three are discarded |
| [BUG-011](findings/BUG-011-aes-padding-and-extended-attempt-metadata-are-delivered-as-message-text.md) | High | Text receive parsing | Core | AES padding and extended-attempt metadata are delivered as message text |
| [BUG-012](findings/BUG-012-login-passwords-are-truncated-by-characters-instead-of-bytes.md) | Low | Login request construction | Core | Login passwords are truncated by characters instead of bytes |
| [BUG-013](findings/BUG-013-the-valid-coordinate-0-0-is-omitted-from-adverts.md) | Low | Self advertisement | Core | The valid coordinate (0, 0) is omitted from adverts |
| [BUG-014](findings/BUG-014-older-advertisements-can-overwrite-newer-contacts.md) | High | Contact synchronization | Core | Older advertisements can overwrite newer contacts |
| [BUG-015](findings/BUG-015-group-text-attempt-bits-are-interpreted-as-message-subtypes.md) | High | Group text receive parsing | Core | Group-text attempt bits are interpreted as message subtypes |
| [BUG-016](findings/BUG-016-group-messages-are-suppressed-when-a-peer-shares-the-local-display-name.md) | Medium | Group message delivery | Core | Group messages are suppressed when a peer shares the local display name |
| [BUG-017](findings/BUG-017-transport-scoped-flood-dms-are-classified-as-direct.md) | High | Text receive routing | Core | Transport-scoped flood DMs are classified as direct |
| [BUG-018](findings/BUG-018-delivery-acks-use-route-timeout-calculations-instead-of-the-200-ms-delay.md) | Medium | ACK scheduling | Core | Delivery ACKs use route timeout calculations instead of the 200 ms delay |
| [BUG-019](findings/BUG-019-synchronous-text-sends-wait-for-the-wrong-ack-identifier.md) | High | ACK correlation | Core | Synchronous text sends wait for the wrong ACK identifier |
| [BUG-020](findings/BUG-020-path-ack-decryption-tries-only-one-colliding-contact.md) | Medium | PATH and ACK parsing | Core | PATH ACK decryption tries only one colliding contact |
| [BUG-021](findings/BUG-021-pending-ack-storage-is-an-unbounded-time-set-with-silent-saturation.md) | Low | ACK state | Core | Pending ACK storage is an unbounded-time set with silent saturation |
| [BUG-022](findings/BUG-022-multipart-packets-and-routed-acks-lack-their-special-forwarding-paths.md) | High | Mesh routing | Repeater | Multipart packets and routed ACKs lack their special forwarding paths |
| [BUG-023](findings/BUG-023-flood-packets-bypass-meshcore-s-reception-quality-delay.md) | Medium | Radio receive scheduling | Core | Flood packets bypass MeshCore's reception-quality delay |
| [BUG-024](findings/BUG-024-server-side-req-replay-protection-is-absent.md) | High | Server-side REQ security | Core | Server-side REQ replay protection is absent |
| [BUG-025](findings/BUG-025-response-waiters-are-keyed-by-a-one-byte-contact-prefix.md) | Medium | Request/response correlation | Core | Response waiters are keyed by a one-byte contact prefix |
| [BUG-026](findings/BUG-026-path-discovery-can-remain-direct-after-the-contact-is-forced-to-flood.md) | High | Path discovery | Core | Path discovery can remain direct after the contact is forced to flood |
| [BUG-027](findings/BUG-027-path-discovery-builds-the-wrong-request-body-and-tracks-the-wrong-tag.md) | High | Path discovery | Core | Path discovery builds the wrong request body and tracks the wrong tag |
| [BUG-028](findings/BUG-028-a-zero-hop-direct-binary-request-is-reported-as-flood.md) | Low | Companion response metadata | Core | A zero-hop direct binary request is reported as flood |
| [BUG-029](findings/BUG-029-control-packets-are-accepted-on-non-direct-routes.md) | Medium | Control packet dispatch | Core | CONTROL packets are accepted on non-direct routes |
| [BUG-030](findings/BUG-030-a-private-region-without-stored-keys-becomes-a-public-hashtag-scope.md) | Medium | Transport regions | Core | A private region without stored keys becomes a public hashtag scope |
| [BUG-031](findings/BUG-031-contacts-start-reports-the-filtered-result-count.md) | Low | Companion contact synchronization | Core | CONTACTS_START reports the filtered result count |
| [BUG-032](findings/BUG-032-encoded-contact-path-length-is-parsed-as-signed.md) | High | Companion contact storage | Core | Encoded contact path length is parsed as signed |
| [BUG-033](findings/BUG-033-valid-zero-bytes-are-stripped-from-stored-paths.md) | High | Companion contact storage | Core | Valid zero bytes are stripped from stored paths |
| [BUG-034](findings/BUG-034-contact-exchange-does-not-preserve-signed-advert-packets.md) | High | Companion contact exchange | Core + Repeater | Contact exchange does not preserve signed ADVERT packets |
| [BUG-035](findings/BUG-035-share-contact-maps-send-failure-to-not-found.md) | Low | Companion command responses | Core | SHARE_CONTACT maps send failure to NOT_FOUND |
| [BUG-036](findings/BUG-036-incoming-direct-message-path-metadata-is-hardcoded-to-zero.md) | Medium | Companion offline messages | Core | Incoming direct-message path metadata is hardcoded to zero |
| [BUG-037](findings/BUG-037-offline-queues-can-discard-direct-messages.md) | Medium | Companion offline messages | Core + Repeater | Offline queues can discard direct messages |
| [BUG-038](findings/BUG-038-auto-add-maximum-hops-is-neither-stored-nor-enforced.md) | Medium | Companion contact policy | Core | Auto-add maximum hops is neither stored nor enforced |
| [BUG-039](findings/BUG-039-send-confirmed-always-reports-zero-trip-time.md) | Low | Companion ACK events | Core | SEND_CONFIRMED always reports zero trip time |
| [BUG-040](findings/BUG-040-app-start-overwrites-protocol-version-from-a-reserved-byte-and-accepts-short-frames.md) | Medium | Companion session negotiation | Core | APP_START overwrites protocol version from a reserved byte and accepts short frames |
| [BUG-041](findings/BUG-041-self-info-reports-a-hardcoded-maximum-tx-power.md) | Low | Companion SELF_INFO | Core + Repeater | SELF_INFO reports a hardcoded maximum TX power |
| [BUG-042](findings/BUG-042-disabled-private-key-import-is-acknowledged-as-successful.md) | Medium | Companion key management | Core | Disabled private-key import is acknowledged as successful |
| [BUG-043](findings/BUG-043-the-implemented-companion-signing-pipeline-is-unreachable.md) | Medium | Companion signing | Core | The implemented companion signing pipeline is unreachable |
| [BUG-044](findings/BUG-044-outbound-companion-payloads-are-truncated-at-173-instead-of-176-bytes.md) | Low | Companion framing | Core | Outbound companion payloads are truncated at 173 instead of 176 bytes |
| [BUG-045](findings/BUG-045-login-status-and-telemetry-commands-report-sent-before-attempting-the-send.md) | Medium | Companion command responses | Core | Login, status, and telemetry commands report SENT before attempting the send |
| [BUG-046](findings/BUG-046-companion-send-failures-use-the-wrong-error-classes.md) | Low | Companion command responses | Core | Companion send failures use the wrong error classes |
| [BUG-047](findings/BUG-047-short-set-other-params-frames-reset-fields-they-should-preserve.md) | Medium | Companion preferences | Core | Short SET_OTHER_PARAMS frames reset fields they should preserve |
| [BUG-048](findings/BUG-048-lora-airtime-calculations-use-incompatible-coding-rate-representations.md) | High | Radio timing | Core | LoRa airtime calculations use incompatible coding-rate representations |
| [BUG-049](findings/BUG-049-maximum-length-valid-direct-paths-are-rejected.md) | Medium | Core/repeater routing | Core + Repeater | Maximum-length valid direct paths are rejected |
| [BUG-050](findings/BUG-050-transport-flood-and-direct-routes-use-incorrect-retransmit-delays.md) | High | Repeater timing | Repeater | Transport flood and direct routes use incorrect retransmit delays |
| [BUG-051](findings/BUG-051-loop-thresholds-ignore-path-hash-width.md) | Low | Repeater loop detection | Repeater | Loop thresholds ignore path-hash width |
| [BUG-052](findings/BUG-052-advert-sends-report-success-after-failure-and-bypass-the-repeater-engine.md) | Medium | Repeater outbound adverts | Repeater | Advert sends report success after failure and bypass the repeater engine |
| [BUG-053](findings/BUG-053-destination-prefix-matches-claim-packets-before-mac-verification.md) | High | Repeater authenticated routing | Core + Repeater | Destination-prefix matches claim packets before MAC verification |
| [BUG-054](findings/BUG-054-unsupported-radio-changes-report-success-for-virtual-companions.md) | Medium | Companion/repeater integration | Core + Repeater | Unsupported radio changes report success for virtual companions |
| [BUG-055](findings/BUG-055-missing-advert-limiter-configuration-falls-back-to-forwarding-blocking-defaults.md) | Medium | Repeater advert forwarding | Repeater | Missing advert-limiter configuration falls back to forwarding-blocking defaults |
| [BUG-056](findings/BUG-056-configuring-a-companion-makes-the-repeater-path-handler-unreachable.md) | High | Repeater PATH dispatch | Repeater | Configuring a companion makes the repeater PATH handler unreachable |
| [BUG-057](findings/BUG-057-pathhelper-treats-encoded-path-len-as-a-byte-count.md) | High | Repeater PATH parsing | Repeater | PathHelper treats encoded path_len as a byte count |
| [BUG-058](findings/BUG-058-a-locally-authenticated-path-packet-is-still-forwarded.md) | Medium | Repeater PATH routing | Repeater | A locally authenticated PATH packet is still forwarded |
| [BUG-059](findings/BUG-059-local-one-byte-identity-collisions-overwrite-routing-and-persistence-state.md) | High | Repeater multi-identity lifecycle | Repeater | Local one-byte identity collisions overwrite routing and persistence state |
| [BUG-060](findings/BUG-060-the-sqlite-queue-loses-binary-payload-signed-sender-and-signal-metadata.md) | High | Repeater companion persistence | Repeater | The SQLite queue loses binary payload, signed sender, and signal metadata |
| [BUG-061](findings/BUG-061-grp-data-and-raw-custom-are-not-delivered-to-companion-bridges.md) | High | Repeater companion packet routing | Repeater | GRP_DATA and RAW_CUSTOM are not delivered to companion bridges |
| [BUG-062](findings/BUG-062-payload-handlers-run-before-a-direct-packet-reaches-its-final-destination.md) | High | Repeater routing order | Repeater | Payload handlers run before a direct packet reaches its final destination |
| [BUG-063](findings/BUG-063-preloaded-sqlite-messages-are-delivered-twice-after-restart.md) | Medium | Repeater companion persistence | Repeater | Preloaded SQLite messages are delivered twice after restart |

## Finding format

Every bug report follows the same order:

1. **TL;DR** — the defect and the fix direction.
2. **What happens** — the practical and logical failure.
3. **How official MeshCore handles it** — the reference behavior.
4. **How the OpenHop stack handles it** — the conflicting Core and/or Repeater path.
5. **What needs to change** — implementation guidance, including both repositories where required.
6. **Source links** — direct links to the relevant code, followed by collapsed verified excerpts.

## Supporting documents

- [Claim verification and publication decisions](docs/CLAIM-VERIFICATION.md)
- [Verification notes and remaining runtime tests](docs/VERIFICATION-NOTES.md)

## Source repositories

| Project | Reviewed branch | Links |
|---|---|---|
| OpenHop Core | `dev` | [README](https://github.com/openhop-dev/openhop_core/blob/dev/README.md) · [source tree](https://github.com/openhop-dev/openhop_core/tree/dev) |
| OpenHop Repeater | `dev` | [README](https://github.com/openhop-dev/openhop_repeater/blob/dev/README.md) · [source tree](https://github.com/openhop-dev/openhop_repeater/tree/dev) |
| MeshCore | `main` | [README](https://github.com/meshcore-dev/MeshCore/blob/main/README.md) · [source tree](https://github.com/meshcore-dev/MeshCore/tree/main) |

## Scope and verification

The 63 listed bugs were rechecked against the supplied source snapshots. The archive contains only confirmed defects; intentionally different or unsupported behavior is not listed as a finding. Full RF, hardware, and cross-device runtime validation was not performed.
