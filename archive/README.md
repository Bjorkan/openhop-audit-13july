# Archived findings

This directory preserves reports that are no longer active defects.

## Fully fixed or fully implemented reports

The **61** reports in [`archive/findings/`](findings/) are fully fixed or, for former policy report BUG-023, fully implemented in the supplied OpenHop snapshots. Their historical LLM-generated implementation sketches are in [`archive/patches/`](patches/).

BUG-023 was previously separated as an intentional routing-policy divergence. Core [`41b6201`](https://github.com/openhop-dev/openhop_core/commit/41b6201ea2e3cb9b8468b0eb80c9e22fdad4a6c8) and Repeater [`dd6dfce`](https://github.com/openhop-dev/openhop_repeater/commit/dd6dfce9e89fab76967d91e202d8e47217c30474) now implement MeshCore’s disabled-by-default reception-quality flood hold, so it has been moved into the ordinary fixed archive.

## Intentional divergences

There are no numbered reports currently stored as intentional divergences. The retained [`archive/intentional/`](intentional/) directory is empty and exists only to preserve the audit taxonomy.

- Complete active and archived tables: [main README](../README.md)
- Intentional-difference policy: [docs/INTENTIONAL-DIFFERENCES.md](../docs/INTENTIONAL-DIFFERENCES.md)
