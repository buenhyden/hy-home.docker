<!-- Target: docs/06.tasks/YYYY-MM-DD-<feature-or-stream>.md -->
# [Feature or Stream] Tasks

> Use this template for `docs/06.tasks/YYYY-MM-DD-<feature-or-stream>.md`.
>
> Rules:
>
> - Task documents are traceability-first.
> - Core behavior should default to TDD.
> - Agent work must include eval tasks where applicable.
> - This is the canonical execution-tracking location; feature-local task notes under `04.specs/` are secondary.

---

## Overview (KR)

이 문서는 [기능 또는 작업 흐름명]의 구현·검증 작업 목록이다. Spec과 Plan에서 파생된 작업을 추적 가능하게 기록한다.

## Inputs

- **Parent Spec**: `[../04.specs/<feature-id>/spec.md]`
- **Parent Plan**: `[../05.plans/YYYY-MM-DD-<feature>.md]`

## Working Rules

- Write failing tests first for core behavior.
- Every task must define evidence.
- Documentation-only work still needs validation evidence.
- If a feature-local `tasks.md` exists under `04.specs/`, this document remains the execution-tracking source of truth.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | [Action] | impl | SPC-001 / §2 | Phase 1 | `pytest ...` | [Name] | Todo |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

### Phase 1

- [ ] T-001 [Description]

### Phase 2

- [ ] T-002 [Description]

## Verification Summary

- **Test Commands**:
- **Eval Commands**:
- **Logs / Evidence Location**:
