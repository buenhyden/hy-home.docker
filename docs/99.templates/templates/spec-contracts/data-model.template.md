---
status: draft
artifact_id: <artifact-id>
artifact_type: spec
parent_ids: [<parent-artifact-id>]
---
<!-- Target: docs/03.specs/NNN-<feature-id>/data-model.md -->

# [Feature Name] Data Model

> Use this template for `docs/03.specs/NNN-<feature-id>/data-model.md`.
>
> Rules:
>
> - This document captures logical/physical data structures for the feature.
> - Keep API surface details in `api-spec.md`.
> - Keep migration execution steps in Plan or Runbook, not here.
> - Write this document in English. Preserve code identifiers, command names,
>   service names, environment variables, and quoted upstream terms exactly.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.

---

## Overview

This document defines the data model and storage strategy for [feature name]. It
describes entities, relationships, identifiers, integrity rules, retention
policy, and change strategy.

## Parent Documents

- **Spec**: [./spec.md](./spec.md)
- **API Spec**: [./api-spec.md](./api-spec.md)

## Scope & Non-goals

- **Covers**:
- **Does Not Cover**:

## Entities / Aggregates

| Entity | Purpose | Identifier | Ownership | Notes |
| --- | --- | --- | --- | --- |
| [Entity] | [Purpose] | [ID] | [Owner] | [Notes] |

## Relationships

- [Entity A] -> [Entity B]:
- Cardinality:
- Invariants:

## Schema / Structures

```sql
-- Example
CREATE TABLE example (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL
);
```

## Validation & Integrity Rules

- **Required fields**:
- **Uniqueness**:
- **Referential integrity**:
- **State transition rules**:

## Storage Strategy

- **Primary store**:
- **Indexes / partitioning**:
- **Caching strategy**:
- **Backup / retention**:

## Privacy / Security

- **Sensitive fields**:
- **Encryption / masking**:
- **Access boundary**:
- **Retention / deletion policy**:

## Migration & Compatibility

- **Backward compatibility rule**:
- **Migration approach**:
- **Rollback notes**:

## Related Documents

- **Spec**: [./spec.md](./spec.md)
- **Plan**: [../../04.execution/plans/YYYY-MM-DD-<feature>.md](../../04.execution/plans/YYYY-MM-DD-<feature>.md)
- **Runbook, direct operations target**: [../../05.operations/runbooks/<topic>.md](../../05.operations/runbooks/<topic>.md)
- **Runbook, domain operations target**: [../../05.operations/runbooks/<domain>/<topic>.md](../../05.operations/runbooks/<domain>/<topic>.md)
