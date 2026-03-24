<!-- Target: docs/04.specs/<feature-id>/data-model.md -->

# [Feature Name] Data Model

> Use this template for `docs/04.specs/<feature-id>/data-model.md`.
>
> Rules:
>
> - This document captures logical/physical data structures for the feature.
> - Keep API surface details in `api-spec.md`.
> - Keep migration execution steps in Plan or Runbook, not here.

---

## Overview (KR)

이 문서는 [기능명]의 데이터 모델과 저장 전략을 정의한다. 엔터티, 관계, 식별자, 무결성 규칙, 보존 정책, 변경 전략을 설명한다.

## Parent Documents

- **Spec**: `[./spec.md]`
- **API Spec**: `[./api-spec.md]`

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

- **Spec**: `[./spec.md]`
- **Plan**: `[../../05.plans/YYYY-MM-DD-<feature>.md]`
- **Runbook**: `[../../09.runbooks/####-<topic>.md]`
