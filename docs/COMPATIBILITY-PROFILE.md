# OpenHop Compatibility Profile

[← Audit home](../README.md)

This profile defines the product assumptions used by the audit. A difference from dedicated MeshCore companion-radio firmware is not classified as a defect when it is explicitly covered here and valid supported traffic remains correct.

## Virtual companion identity

A companion hosted by OpenHop Repeater is a virtual MeshCore identity sharing one physical radio and one host process with the repeater. It is not a separate hardware node.

Consequences:

- radio parameters and TX power are read-only from the companion perspective;
- multiple companions cannot maintain independent physical radio settings;
- client-repeat frequency capabilities may be empty;
- self telemetry does not imply a separate battery or sensor set;
- repeater coordinates are owned by daemon configuration and GPS services.

Commands that are unsupported must return an explicit disabled or unsupported response. Returning success for a no-op remains a defect.

## Administrative boundary

The companion transport is not a host-administration channel. The supported profile excludes:

- host reboot;
- factory reset of the repeater installation;
- remote private-key replacement;
- device-PIN administration for the Linux service;
- implicit mutation of the global radio.

A future administrative API must be repeater-owned, separately authorized, and atomic across configuration, radio state, identity registration, and persistence.

## Reliability and persistence extensions

OpenHop may intentionally provide:

- high-level request retries above the wire-compatibility layer;
- an offline queue larger than MeshCore firmware's embedded default;
- SQLite-backed persistence;
- TCP keepalive;
- additional companion query forms such as a full channel listing.

These extensions must not corrupt standard responses, duplicate messages, discard protected direct messages, or falsely report success.

## Region identifiers

The reviewed profile uses bounded ASCII region identifiers, including hashtag and IATA-style names. Non-ASCII region names are outside the supported profile. Transport-key matching and forwarding policy for supported ASCII regions must still be correct.

## Optional anti-abuse policy

Advert rate limiting, penalties, and adaptive limiting are optional operator policies. They intentionally change MeshCore forwarding when enabled. They must default to disabled when absent from configuration and must be clearly documented when enabled.

## Parser extensions

Permissive handling of reserved versions or malformed optional commands is not considered a defect unless it changes valid supported traffic, creates a security boundary failure, or desynchronizes a compliant client.
