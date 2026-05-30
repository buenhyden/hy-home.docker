---
status: draft
---
<!-- Target: docs/04.execution/tasks/2026-05-30-standardizing-agent-governance.md -->

# Task: Standardizing Agent Governance

---

## Overview (KR)

이 문서는 AI Agent 거버넌스 정비 작업의 구현 및 검증 태스크 목록이다. 계획(Plan)에서 정의된 아키텍처 정비 단계를 추적 가능한 태스크 항목으로 나누어 관리하고 검증한다.

## Inputs

- **Parent Plan**: [Execution plan](../plans/2026-05-30-standardizing-agent-governance.md)

## Working Rules

- Verify parity rules across Claude, Codex, and Gemini.
- Core behavior must comply with the 3-tier Provider Parity Model.
- Run validation scripts after every file modification to prevent syntax or parity breaks.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create and structure Plan & Task documents | doc | N/A | Phase 1 | Files present in docs/04.execution/ | Antigravity | Completed |
| T-002 | Standardize Core Governance policies (README/workflows/matrix) | doc | N/A | Phase 1 | Matrix checks passed | Antigravity | Todo |
| T-003 | Aling Platform Overlays (gemini.md / GEMINI.md / AGENTS.md) | doc | N/A | Phase 2 | Pointer parity validation success | Antigravity | Todo |
| T-004 | Run contract verification script | eval | N/A | Phase 2 | `bash scripts/validation/check-repo-contracts.sh` | Antigravity | Todo |

## Verification Summary

- **Test Commands**:
  - `bash scripts/validation/check-repo-contracts.sh`
- **Logs / Evidence Location**:
  - Console validation output (failures=0 PASS)

## Related Documents

- **Parent Plan**: [Execution plan](../plans/2026-05-30-standardizing-agent-governance.md)
- **Operations / References**: [Operations index](../../05.operations/README.md)
