<!-- Target: docs/05.plans/YYYY-MM-DD-<feature>.md -->

# [Feature Name] Implementation Plan

> Use this template for `docs/05.plans/YYYY-MM-DD-<feature>.md`.
>
> Rules:
>
> - Every active plan must include explicit verification criteria.
> - Plan explains execution order, risk control, and rollout strategy.

---

# [Feature or Component] Plan

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

- **PRD**: `[../01.prd/YYYY-MM-DD-<feature-or-system>.md]`
- **ARD**: `[../02.ard/####-<system-or-domain>.md]`
- **Spec**: `[../04.specs/<feature-id>/spec.md]`
- **ADR**: `[../03.adr/####-<short-title>.md]`
