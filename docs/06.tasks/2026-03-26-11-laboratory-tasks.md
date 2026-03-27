# Task: 11-laboratory Standardization

## Overview (KR)

이 문서는 `11-laboratory` 계층의 구현·검증 작업 목록이다. Spec과 Plan에서 파생된 작업을 추적 가능하게 기록한다.

## Inputs

- **Parent Spec**: `[../04.specs/11-laboratory/spec.md]`
- **Parent Plan**: `[../05.plans/2026-03-26-11-laboratory-standardization.md]`

## Working Rules

- Every task must define evidence.
- Documentation-only work still needs validation evidence.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-11-LAB-001 | Update PRD with vision & personas | doc | §1 | PLN-001 | File review | Antigravity | Done |
| T-11-LAB-002 | Update ARD with mermaid diagram | doc | §3 | PLN-002 | Mermaid render | Antigravity | Done |
| T-11-LAB-003 | Update ADR with service stack | doc | §3 | PLN-003 | Decision logic check | Antigravity | Done |
| T-11-LAB-004 | Update Spec with port/label details | doc | §1 | PLN-004 | Config vs Spec check | Antigravity | Done |
| T-11-LAB-005 | Update READMEs in all docs/ folders | doc | N/A | N/A | File review | Antigravity | Todo |

## Verification Summary

- **Test Commands**: `grep -r "11-laboratory" docs/`
- **Logs / Evidence Location**: Correct rendering of all updated .md files.
