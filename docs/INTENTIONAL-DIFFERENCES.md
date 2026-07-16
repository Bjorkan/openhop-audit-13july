# Intentional differences and non-findings

This audit does not require a host implementation to reproduce embedded-memory constraints or experimental routing policy when a different design remains bounded, safe and wire-compatible. The following differences were reviewed and deliberately **not** classified as active bugs.

| Difference | Audit conclusion |
|---|---|
| Reception-quality flood-routing policy (BUG-023) | Intentional and under evaluation. OpenHop records MeshCore-inspired neighbour scores and exposes a report, but deliberately does not let that observational data influence forwarding yet. Both systems leave reception-quality routing disabled by default. |
| Larger pending-ACK capacity than firmware | Intentional and bounded. BUG-021 remains archived because OpenHop now uses defined FIFO eviction instead of silent saturation. |
| `MAX_HASH_SIZE = 32` in Python | Used as an internal full SHA-256 representation. Wire path hashes remain separately encoded; the larger internal value is not itself incompatible. |
| Larger host-side contact/message databases | Acceptable where limits, eviction, authentication and wire serialization remain defined. Unbounded attacker-controlled storage is still a defect, as in BUG-072. |
| 32-byte normalized channel secrets in internal host APIs | Acceptable only outside the standard companion wire command. BUG-089 tracks the separate problem that CMD_SET_CHANNEL accepts the 32-byte/hex forms that official firmware rejects. |
| Missing reboot, factory-reset and device-PIN hardware commands | These operations are target/hardware lifecycle functions and are not required for a virtual or host process to claim packet interoperability. In contrast, HAS_CONNECTION and GET_TUNING_PARAMS are data-plane companion queries and are reported in BUG-069. |
| Journald/Python logging instead of firmware log CLI controls | Intentional platform substitution. The common maintenance commands `clear stats` and `tempradio` are still reported because they affect protocol/runtime behavior rather than log transport. |
| Additional SQLite retention and observability | Acceptable provided data fidelity and ordering are preserved. Remaining metadata loss is tracked in BUG-060. |
| Additional rate limiting and abuse protection | Acceptable when disabled/default behavior does not silently reject traffic that official MeshCore forwards and when wire semantics remain unchanged. |
| Host UI, REST, MQTT, RRD and web assets | Reviewed for their use of protocol fields and persistence contracts, but visual or platform-specific features are not expected to match firmware UI code. |

## Decision rule

A difference becomes a finding when it changes bytes on the wire, accepts or rejects traffic differently, changes routing/ACK/security semantics, breaks a documented companion/CLI contract, loses protocol data, introduces unbounded attacker-controlled state, or causes externally visible identity/telemetry to disagree with MeshCore. A consciously deferred experimental routing policy is documented but is not a defect when the default interoperable path remains unchanged.
