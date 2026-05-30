---
status: active
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
- Core behavior must comply with the 3-tier Provider Parity Model using the 2026-05-29 canonical models.
- Run validation scripts after every file modification to prevent syntax or parity breaks.

## Task Table

| Task ID | Description | Type | Parent Plan | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-001 | Stage 00 공통 거버넌스 업데이트 | doc | PLN-001 | `provider-capability-matrix.md`, `stage-authoring-matrix.md` updated | Antigravity | Completed |
| T-002 | 템플릿 계약 명시 및 매핑 리팩터링 | doc | PLN-002 | `policy.template.md` created, references updated | Antigravity | Completed |
| T-003 | 모델 및 Reasoning 설정 업데이트 | doc | PLN-003 | `subagent-protocol.md` already correct (Opus 4.8 / Sonnet 4.6 / GPT-5.5 / Gemini 3.1 Pro). Capability matrix aligned. | Antigravity | Completed |
| T-004 | 플랫폼별 하네스 정비 (Claude, Codex, Gemini) | doc | PLN-004 | `.claude`, `.codex`, `.agents` pointers checked | Antigravity | Completed |
| T-005 | Run contract verification script | eval | All | `bash scripts/validation/check-repo-contracts.sh` | Antigravity | Completed |

## Verification Summary

- **Test Commands**:
  - `bash scripts/validation/check-repo-contracts.sh`
- **Logs / Evidence Location**:
  - Console validation output: `failures=0 PASS`

## Related Documents

- **Parent Plan**: [Execution plan](../plans/2026-05-30-standardizing-agent-governance.md)
- **Operations / References**: [Operations index](../../05.operations/README.md)
