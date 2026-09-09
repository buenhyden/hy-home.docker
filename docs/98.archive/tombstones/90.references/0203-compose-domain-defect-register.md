---
title: "Compose Domain Defect Register Tombstone"
version: "1.0.0"
type: "archive/tombstone"
status: "sealed"
owner: "@buenhyden"
updated: "2026-09-09"
layer: "archive"
artifact_id: "tomb-AUD-0097"
parent_ids:
- "SPEC-0173"
created: "2026-09-09"
---

# Compose Domain Defect Register Tombstone

## Retired Path

`docs/90.references/audits/0097-compose-domain-defect-register/README.md`

## Replacement

`docs/05.operations/catalog/09-tooling/0061-k6/guide.md`

## Reason

Three of the four registered defects are fixed in the tree. The hardening
suite no longer pins a literal Valkey tag, no compose file publishes host 8000,
and no exporter targets `mng-n8n-valkey`. Four operations guides still linked
here as the owner of an "open" defect that had already been closed, which is
the failure mode a dated register produces once its findings are resolved.

CDR-04 is still reproducible: `infra/09-tooling/k6/` declares `build: .` with no
Dockerfile, so the `tooling` and `testing` profiles fail to build. That finding
moved into the guide of the subject that owns it, together with the decision it
needs, so the defect outlives this register. The register's remaining value was
its dated snapshot, which Git preserves.

## Recovery Commit

`af9f27f6fb0322b69ad67ba7f879ceddd7a3cf0b`

## Traceability

- [Archive index](../../README.md)
