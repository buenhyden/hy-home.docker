---
status: draft
---
<!-- Target: docs/04.execution/plans/YYYY-MM-DD-<feature>.md -->

# [Feature Name] Implementation Plan

> Use this template for `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`.
>
> Rules:
>
> - Every active plan must include explicit verification criteria.
> - Plan explains execution order, risk control, and rollout strategy.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.
> - Replace example links with real target-relative links, or delete unused examples before saving.
>
> Target-relative examples from `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`:
>
> - PRD: `../../01.requirements/YYYY-MM-DD-feature-or-system.md`
> - ARD: `../../02.architecture/requirements/####-system-or-domain.md`
> - ADR: `../../02.architecture/decisions/####-short-title.md`
> - Spec: `../../03.specs/feature-id/spec.md`
> - Task: `../tasks/YYYY-MM-DD-feature-or-stream.md`
> - Operations: `../../05.operations/README.md`

---

## Overview (KR)

이 문서는 [기능 또는 컴포넌트명]의 실행 계획서다. 작업 분해, 검증, 롤아웃, 위험 관리, 완료 기준을 정의한다.

## Context

[Why this work exists.]

## Goals & In-Scope

- **Goals**:
- **In Scope**:

## Non-Goals & Out-of-Scope

- **Non-goals**:
- **Out of Scope**:

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | [Action] | `path/to/file` | REQ-001 | [Evidence] |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | [Check] | [Command] | [Pass] |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| [Risk] | High | [Mitigation] |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**:
- **Sandbox / Canary Rollout**:
- **Human Approval Gate**:
- **Rollback Trigger**:
- **Prompt / Model Promotion Criteria**:

## Completion Criteria

- [ ] Scoped work completed
- [ ] Verification passed
- [ ] Required docs updated

## Related Documents

- **PRD**: [YYYY-MM-DD-<feature-or-system>](../../01.requirements/YYYY-MM-DD-<feature-or-system>.md)
- **ARD**: [####-<system-or-domain>](../../02.architecture/requirements/####-<system-or-domain>.md)
- **Spec**: [<feature-id> spec](../../03.specs/<feature-id>/spec.md)
- **ADR**: [####-<short-title>](../../02.architecture/decisions/####-<short-title>.md)
- **Task**: [YYYY-MM-DD-<feature-or-stream> task](../tasks/YYYY-MM-DD-<feature-or-stream>.md)
- **Operations**: [Operations index](../../05.operations/README.md)
