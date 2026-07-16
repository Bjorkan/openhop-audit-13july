# Intentional differences and non-findings

This audit does not require a host implementation to reproduce embedded-memory constraints or experimental routing policy when a different design remains bounded, safe and wire-compatible. The following differences were reviewed and deliberately **not** classified as active bugs.

| Difference | Audit conclusion |
|---|---|
| Reception-quality neighbour reporting | The bounded observational report remains an intentional host feature. It is separate from forwarding. The former BUG-023 routing mismatch is now implemented and archived as fixed. |
| Larger pending-ACK capacity than firmware | Intentional and bounded. BUG-021 remains archived because OpenHop now uses defined FIFO eviction instead of silent saturation. |
| `MAX_HASH_SIZE = 32` in Python | Used as an internal full SHA-256 representation. Wire path hashes remain separately encoded; the larger internal value is not itself incompatible. |
| Larger host-side contact/message databases | Acceptable where limits, eviction, authentication and wire serialization remain defined. Unbounded attacker-controlled storage is still a defect, as in BUG-072. |
| 32-byte normalized channel secrets in internal host APIs | Acceptable only outside the standard companion wire command. BUG-089 tracks the separate problem that CMD_SET_CHANNEL accepts the 32-byte/hex forms that official firmware rejects. |
| Missing reboot, factory-reset and device-PIN hardware commands | These operations are target/hardware lifecycle functions and are not required for a virtual or host process to claim packet interoperability. In contrast, HAS_CONNECTION and GET_TUNING_PARAMS are data-plane companion queries and are reported in BUG-069. |
| Journald/Python logging instead of firmware log CLI controls | Intentional platform substitution. The common maintenance commands `clear stats` and `tempradio` are still reported because they affect protocol/runtime behavior rather than log transport. |
| Additional SQLite retention and observability | Acceptable provided data fidelity and ordering are preserved. The previously tracked metadata loss in BUG-060 is now fixed; additional retention remains acceptable while fidelity and ordering are preserved. |
| Additional rate limiting and abuse protection | Acceptable when disabled/default behavior does not silently reject traffic that official MeshCore forwards and when wire semantics remain unchanged. |
| Host UI, REST, MQTT, RRD and web assets | Reviewed for their use of protocol fields and persistence contracts, but visual or platform-specific features are not expected to match firmware UI code. |

## Decision rule

A difference becomes a finding when it changes bytes on the wire, accepts or rejects traffic differently, changes routing/ACK/security semantics, breaks a documented companion/CLI contract, loses protocol data, introduces unbounded attacker-controlled state, or causes externally visible identity/telemetry to disagree with MeshCore. A consciously added observational subsystem is not a defect when it does not alter the default interoperable path.

## Rechecked non-findings in the deeper logic pass

- ACL capacity: rejecting or evicting at a different bounded host-side capacity was not filed by itself. BUG-111 concerns persistence, not table size.
- Neighbour-link observation: the additional report and scoring state remain intentional and do not reopen BUG-023.
- Host-side post rate limits: the extra limit is not inherently a defect. BUG-114 is specifically about sending a protocol ACK before knowing whether that host-side policy accepted the post.

## Latest rechecked non-finding

- Private-key import remains intentionally unavailable for the configuration-managed host identity. This is not reopened as a defect because complete import frames receive the protocol-defined disabled response; BUG-042 remains archived.
