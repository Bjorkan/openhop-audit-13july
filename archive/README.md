# Archived findings

This directory preserves reports that are no longer active defects.

## Fully fixed defects

The **57** reports in [`archive/findings/`](findings/) are fully fixed in the supplied OpenHop snapshots. Their historical LLM-generated implementation sketches are in [`archive/patches/`](patches/).

## Intentional divergences

[`archive/intentional/`](intentional/) contains numbered reports whose behavior is deliberately different and is not currently classified as a defect. BUG-023 is stored there after the maintainer clarified that reception-quality scoring is observational and its use in flood routing is intentionally deferred pending real-world data. Historical sketches in this directory are retained only for provenance and are not recommended changes.

- Complete active and archived tables: [main README](../README.md)
- Intentional-difference policy: [docs/INTENTIONAL-DIFFERENCES.md](../docs/INTENTIONAL-DIFFERENCES.md)
