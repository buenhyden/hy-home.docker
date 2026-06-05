---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-05-31-claude-harness-governance-verification.md -->

# Claude Harness Governance Verification Implementation Plan

## Overview

이 문서는 공유 거버넌스(Stage 00)와 Claude 하네스의 정합성을 검증하고, 확인된 실제 드리프트만 외과적으로
수정하는 실행 계획서다. 모델 정책을 웹으로 재검증하고, 비집행(non-enforced) 갭은 거버넌스 메모리에 기록한다.

## Context

`/plan` 요청은 Stage 00을 신규 구축하는 것처럼 작성되었으나, Phase 1 조사 결과 해당 작업은 이미
2026-05-29 및 2026-05-31 작업으로 완료되어 있다. Model Policy, QA & CI/CD 정책, Template Contract,
clarification duty, 15개 에이전트 모델 별칭(`opus`/`sonnet`)이 모두 존재하며 `check-repo-contracts.sh`가
`failures=0`로 통과한다. 따라서 본 작업은 신규 구축이 아니라 **검증 + 실제 드리프트 수정 + 갭 기록**으로
범위를 한정한다(사용자 승인 결정).

## Goals & In-Scope

- **Goals**: 공유 거버넌스와 Claude 하네스 정합성을 증거 기반으로 입증하고, 확인된 드리프트만 수정한다.
- **In Scope**:
  - 검증 스크립트 실행(`check-repo-contracts.sh`, `check-doc-traceability.sh`) 및 결과 기록.
  - 웹 기반 모델 재검증(Claude / Codex / Gemini, 2026-05).
  - 확인된 텍스트 드리프트 수정: `agents/agents/workflow-supervisor.md:31` 모델 식별자.
  - 비집행 갭(Gemini 티어 역전) 거버넌스 메모리 기록.
  - 추적성 Plan/Task 문서 및 progress 로그 작성.

## Non-Goals & Out-of-Scope

- **Non-goals**: 거버넌스/템플릿/하네스의 신규 정의 또는 대규모 재작성.
- **Out of Scope**:
  - ~499개 stage 문서 일괄 재작성(read-only 기본값 유지, 갭은 기록만).
  - Model Policy를 2026-05-29 스냅샷으로 롤백.
  - `.codex/**`, `.agents/**` 미러 수정, Docker 런타임/시크릿/배포/브랜치 보호 변경.

## Work Breakdown

| Task    | Description                           | Files / Docs Affected                                                                        | Target REQ | Validation Criteria                           |
| ------- | ------------------------------------- | -------------------------------------------------------------------------------------------- | ---------- | --------------------------------------------- |
| PLN-001 | Baseline 검증 스크립트 실행           | `scripts/validation/check-repo-contracts.sh`, `scripts/validation/check-doc-traceability.sh` | N/A        | 두 스크립트 `failures=0`                      |
| PLN-002 | 웹 모델 재검증 후 정책 권위 확정      | `subagent-protocol.md` (검토만)                                                              | N/A        | Claude/Codex 현행 확인, Gemini 티어 이슈 식별 |
| PLN-003 | 확인된 모델 식별자 드리프트 수정      | `docs/00.agent-governance/agents/agents/workflow-supervisor.md`                              | N/A        | stale-model grep 무결과                       |
| PLN-004 | Gemini 티어 역전 갭 메모리 기록       | `docs/00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md`                     | N/A        | 메모리 템플릿 준수, placeholder 없음          |
| PLN-005 | 추적성 Plan/Task/README/progress 작성 | 본 plan, 짝 task, 두 README, `progress.md`                                                   | N/A        | 템플릿/frontmatter/Related Documents 준수     |

## Verification Plan

| ID          | Level      | Description                  | Command / How to Run                                                   | Pass Criteria |
| ----------- | ---------- | ---------------------------- | ---------------------------------------------------------------------- | ------------- |
| VAL-PLN-001 | Structural | 리포지토리 계약 검증         | `bash scripts/validation/check-repo-contracts.sh`                      | `failures=0`  |
| VAL-PLN-002 | Structural | 문서 추적성 검증             | `bash scripts/validation/check-doc-traceability.sh`                    | `failures=0`  |
| VAL-PLN-003 | Content    | stale 모델 문자열 부재       | `grep -rn -E 'gemini-3-pro\|gpt-5.1' docs/00.agent-governance .claude` | 무결과        |
| VAL-PLN-004 | Hygiene    | 화이트스페이스 드리프트 부재 | `git diff --check`                                                     | 무결과        |

## Risks & Mitigations

| Risk                          | Impact | Mitigation                                                          |
| ----------------------------- | ------ | ------------------------------------------------------------------- |
| 이미 정확한 파일을 churn      | Medium | "verify + fix real drift only" 범위 고수, grep으로 정확 매치만 수정 |
| Gemini 티어를 성급히 변경     | Medium | 정책 표는 보존하고 메모리에 결정 항목으로만 기록(3.5 Pro 미출시)    |
| 추적성 짝(plan↔task) 비동기화 | High   | plan/task 동시 생성 및 양쪽 README 등록, 추적성 검증 재실행         |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: N/A (거버넌스 문서/검증 작업, 도메인 코드 변경 없음).
- **Sandbox / Canary Rollout**: N/A.
- **Human Approval Gate**: plan 승인 완료(plan mode).
- **Rollback Trigger**: 검증 스크립트가 `failures>0`이면 변경 되돌림.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [ ] Scoped work completed
- [ ] Verification passed (`check-repo-contracts.sh`, `check-doc-traceability.sh` 모두 `failures=0`)
- [ ] Required docs updated (plan, task, 두 README, progress, 메모리 노트)

## Related Documents

- **Governance (Model Policy SSOT)**: [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Provider Capability Matrix**: [provider-capability-matrix.md](../../00.agent-governance/rules/provider-capability-matrix.md)
- **Documentation Protocol**: [documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Gemini Model Tier Review (memory)**: [2026-05-31-gemini-model-tier-review.md](../../00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md)
- **Task**: [2026-05-31-claude-harness-governance-verification.md](../tasks/2026-05-31-claude-harness-governance-verification.md)
- **Current Governance Plan**: [Agent Governance Decision Items and Attachment-Gap Plan](./2026-06-02-agent-governance-decision-items-plan.md)
