---
title: "Research Package Consolidation Migration"
version: "1.0.0"
type: "archive/migration"
status: "sealed"
owner: "@buenhyden"
updated: "2026-09-18"
layer: "archive"
artifact_id: "MIG-0004"
parent_ids:
- "ADR-0036"
created: "2026-09-18"
---

# Research Package Consolidation Migration

## Purpose

Record the disposition of the learning-roadmap research line and the routing
integration of the related Stage 90 packages under `RES-0002`.

## Moved Scope

`RES-0002` is the current topical research hub. `RES-0084`, `RES-0085`, and
`RES-0096` retain their specialized or historical evidence ownership and are
routed from the hub. `RES-0081` is no longer active and is preserved as
superseded history; its predecessor `RES-0080` was already preserved as
superseded history.

```yaml
schema_version: 3
migration_id: mig-0004
baseline_commit: bb43abb5e0894f45d1179a60770d489a0da41e7c
rows:
- source_path: docs/90.references/research/0081-roadmap/README.md
  target_path: docs/98.archive/superseded/90.references/research/0081-roadmap/README.md
  artifact_id: RES-0081
  action: supersede
  replacement: RES-0002
  source_commit: bb43abb5e0894f45d1179a60770d489a0da41e7c
  reason: Remove the learning roadmap from the active research index and route current topical research through RES-0002 while preserving the dated source.
```

## Current Owner

`RES-0002` owns current topical research routing. `RES-0084`, `RES-0085`, and
`RES-0096` remain the owners of their specialized or dated evidence. The
superseded RES-0081 body is retained only as historical context.

## Approval

The operator request of 2026-09-18 authorizes removal of RES-0080/RES-0081
from the active research index and integration of RES-0084/RES-0085/RES-0096
under RES-0002 routing. No runtime, secret, remote, or deployment action is
authorized by this migration.

## Traceability

- [Research Packages](../../90.references/research/README.md)
- [RES-0002](../../90.references/research/0002-agentic-engineering-research-pack/README.md)
- [ADR-0036](../../02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md)