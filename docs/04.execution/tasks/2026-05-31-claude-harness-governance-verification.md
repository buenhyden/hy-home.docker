---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-05-31-claude-harness-governance-verification.md -->

# Task: Claude Harness Governance Verification

## Overview

이 문서는 공유 거버넌스와 Claude 하네스 정합성 검증 작업의 수행·검증 audit trail이다. 짝 Plan에서 파생된
작업을 추적 가능하게 기록한다. 본 작업은 cross-cutting 거버넌스 작업으로, parent Spec 대신 거버넌스 문서를
참조한다(`documentation-protocol.md` §8.5).

## Inputs

- **Parent Plan**: [Claude Harness Governance Verification Plan](../plans/2026-05-31-claude-harness-governance-verification.md)
- **Governance Scope**: [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)

## Working Rules

- 문서/검증 작업이므로 도메인 코드 TDD는 N/A이나 모든 작업에 검증 evidence를 남긴다.
- raw logs, secret 값, shell history는 저장하지 않는다.
- read-only stage 문서는 일괄 수정하지 않으며 갭은 거버넌스 메모리에 기록한다.

## Task Table

| Task ID | Description                      | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence                                                                                          | Owner | Status |
| ------- | -------------------------------- | ---- | --------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------- | ----- | ------ |
| T-001   | Baseline 검증 스크립트 실행      | ops  | N/A (cross-cutting)   | PLN-001             | `check-repo-contracts.sh` failures=0 (499 docs); `check-doc-traceability.sh` failures=0 (46 pairs)             | hy    | Done   |
| T-002   | 웹 모델 재검증                   | doc  | N/A                   | PLN-002             | Claude opus-4.8/sonnet-4.6, Codex gpt-5.5/gpt-5.4-mini 현행 확인; Gemini 3.5-flash > 3.1-pro, 3.5-pro 6월 지연 | hy    | Done   |
| T-003   | 모델 식별자 드리프트 수정        | impl | N/A                   | PLN-003             | `workflow-supervisor.md:31` gemini-3-pro→gemini-3.1-pro, gpt-5.1-codex→gpt-5.5; stale grep 무결과              | hy    | Done   |
| T-004   | Gemini 티어 갭 메모리 기록       | doc  | N/A                   | PLN-004             | `memory/2026-05-31-gemini-model-tier-review.md` 생성                                                           | hy    | Done   |
| T-005   | 추적성 문서/README/progress 작성 | doc  | N/A                   | PLN-005             | plan, task, 두 README, progress 행 갱신                                                                        | hy    | Done   |

## Suggested Types

- `impl`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-001 Baseline 검증
- [x] T-002 웹 모델 재검증

### Phase 2

- [x] T-003 드리프트 수정
- [x] T-004 갭 메모리 기록
- [x] T-005 추적성 문서 작성

## Verification Summary

- **Test Commands**: N/A (도메인 코드 변경 없음 → quality-standards 90% 커버리지 N/A: docs/policy 변경).
- **Eval Commands**: `bash scripts/validation/check-repo-contracts.sh` → `failures=0`; `bash scripts/validation/check-doc-traceability.sh` → `failures=0`; stale-model `grep` → 무결과; `git diff --check` → 무결과.
- **Logs / Evidence Location**: 본 문서 Task Table 및 `docs/00.agent-governance/memory/progress.md` 최신 행.

### Deviation Notes

- 원 요청은 greenfield 거버넌스 구축을 가정했으나 거버넌스가 이미 성숙·정합 상태여서, 사용자 승인에 따라
  범위를 "검증 + 실제 드리프트 수정 + 갭 기록"으로 한정했다.
- Gemini 티어 역전은 정책을 즉시 변경하지 않고 메모리 결정 항목으로 기록했다(`gemini-3.5-pro` 미출시).

## Related Documents

- **Parent Plan**: [Claude Harness Governance Verification Plan](../plans/2026-05-31-claude-harness-governance-verification.md)
- **Governance (Model Policy SSOT)**: [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Gemini Model Tier Review (memory)**: [2026-05-31-gemini-model-tier-review.md](../../00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md)
- **Progress Log**: [progress.md](../../00.agent-governance/memory/progress.md)
