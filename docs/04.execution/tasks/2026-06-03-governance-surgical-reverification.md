---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-06-03-governance-surgical-reverification.md -->

# Task: Governance Surgical Re-Verification + Tech-Stack Drift Closure

## Overview

이 문서는 공유 거버넌스·Claude 하네스 외과적 재검증과, 그 과정에서 드러난 Dependabot發
tech-stack 버전 드리프트의 종결 및 재발 방지 자동화 작업의 수행·검증 audit trail이다. 본
작업은 cross-cutting 거버넌스 작업으로, parent Spec 대신 거버넌스 문서를 참조한다
(`documentation-protocol.md` §8.5).

## Inputs

- **Parent Plan**: [Governance Surgical Re-Verification Plan](../plans/2026-06-03-governance-surgical-reverification.md)
- **Governance Scope**: [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)

## Working Rules

- 문서/검증/스크립트 작업이며 모든 작업에 검증 evidence를 남긴다.
- raw logs, secret 값, shell history는 저장하지 않는다.
- read-only stage 문서는 일괄 수정하지 않으며 갭은 거버넌스 메모리에 기록한다.
- 보안/CI 거버넌스 계약은 우회하지 않으며, 충돌 시 사용자 승인으로 방향을 결정한다.

## Approved Surface Evidence

| Surface             | Approval Source                        | Target                                          | Before Evidence                                    | After Evidence                                              | Rollback / Recovery        | Redaction Boundary         |
| ------------------- | -------------------------------------- | ----------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------- | -------------------------- | -------------------------- |
| Infra registry data | 사용자 "versions.json 동기화" 승인     | `infra/tech-stack.versions.json`                | 9개 컴포넌트 태그 stale (Dependabot 범프와 불일치) | compose 선언값과 일치, `check-repo-contracts.sh failures=0` | `git revert`/재실행 `sync` | secret 없음, 이미지 태그만 |
| CI workflow         | 사용자 "읽기전용 드리프트 게이트" 승인 | `.github/workflows/tech-stack-version-sync.yml` | 없음                                               | `contents: read` 드리프트 게이트(자동커밋 미채택)           | 워크플로 파일 삭제         | secret 없음                |
| Contract validator  | 스크립트 등록 필수(usage contract)     | `scripts/validation/check-repo-contracts.sh`    | `expected_implementations`에 신규 스크립트 부재    | 신규 스크립트 등재, `failures=0`                            | 등재 라인 제거             | 없음                       |

## Task Table

| Task ID | Description                              | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence                                                                                                    | Owner | Status |
| ------- | ---------------------------------------- | ---- | --------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------ | ----- | ------ |
| T-001   | 거버넌스 범위 QA/CI 게이트 재실행        | ops  | N/A (cross-cutting)   | PLN-001             | repo-contracts/traceability/impl-alignment/compose/hardening/quickwin/template-security/wiki 전부 `failures=0`/PASS      | hy    | Done   |
| T-002   | 모델 최신성 웹 재검증 + 저장소 교차 점검 | doc  | N/A                   | PLN-002             | Claude `opus-4.8`/`sonnet-4.6` 현행; `gemini-3.5-pro` 미GA; `.claude/agents` 1 opus+14 sonnet; stale 모델 0              | hy    | Done   |
| T-003   | tech-stack 드리프트 동기화               | impl | N/A                   | PLN-003             | `infra/tech-stack.versions.json` 9개 태그 compose 일치; `check-repo-contracts.sh failures=0`                             | hy    | Done   |
| T-004   | Gemini 티어 메모리 재검증 기록           | doc  | N/A                   | PLN-004             | `memory/2026-05-31-gemini-model-tier-review.md` 2026-06-03 재검증 절 추가                                                | hy    | Done   |
| T-005   | tech-stack sync 스크립트 작성            | impl | N/A                   | PLN-006             | `scripts/operations/sync-tech-stack-versions.sh` (`--check`/`--dry-run`/write); 주입 드리프트 감지·수정 양성 테스트 통과 | hy    | Done   |
| T-006   | 스크립트 거버넌스 등록                   | impl | N/A                   | PLN-006             | `check-repo-contracts.sh` allowlist + `scripts/README.md` 3개 표 등재; usage contract PASS                               | hy    | Done   |
| T-007   | 읽기전용 CI 드리프트 게이트              | impl | N/A                   | PLN-007             | `.github/workflows/tech-stack-version-sync.yml` `contents: read`로 `sync --check`; 워크플로 보안 계약 PASS               | hy    | Done   |
| T-008   | 추적 증거 작성                           | doc  | N/A                   | PLN-005             | plan, task, 두 README 인덱스, progress 행 갱신                                                                           | hy    | Done   |

## Suggested Types

- `impl`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-001 거버넌스 게이트 재실행
- [x] T-002 웹 모델 재검증

### Phase 2

- [x] T-003 드리프트 동기화
- [x] T-004 Gemini 티어 메모리 기록
- [x] T-005 sync 스크립트 작성
- [x] T-006 스크립트 거버넌스 등록
- [x] T-007 읽기전용 CI 드리프트 게이트
- [x] T-008 추적 증거 작성

## Verification Summary

- **Test Commands**: `bash scripts/operations/sync-tech-stack-versions.sh --check` → in sync; 주입 드리프트 양성 테스트(감지 rc=1 → write 수정 → 재검증 in sync).
- **Eval Commands**: `bash scripts/validation/check-repo-contracts.sh` → `failures=0`; `check-doc-traceability.sh` → `failures=0` (`catalog_pairs_total=46`); `check-doc-implementation-alignment.sh` → `failures=0`; `validate-docker-compose.sh`/`check-all-hardening.sh`/quickwin/template-security → PASS; LLM Wiki freshness PASS; `git diff --check` → 무결과.
- **Logs / Evidence Location**: 본 문서 Task Table 및 `docs/00.agent-governance/memory/progress.md` 최신 행.

### Deviation Notes

- 원 요청은 greenfield 3-Phase 거버넌스 구축을 가정했으나 거버넌스가 이미 성숙·정합 상태여서,
  사용자 승인에 따라 범위를 "외과적 재검증 + 갭 종결 + 재발 방지 자동화"로 한정했다.
- Gemini 티어 역전은 `gemini-3.5-pro` 미GA로 정책 미변경, 메모리 결정 항목으로 재검증만 기록했다.
- tech-stack 드리프트의 근본 원인은 Dependabot 자동 범프이며, 사용자 선택에 따라 CI **자동커밋** 대신
  **읽기전용 드리프트 게이트 + 원커맨드 sync 스크립트**로 구현했다. 사유: 저장소 보안 거버넌스가
  워크플로의 `contents: write`를 하드 금지한다(`check-repo-contracts.sh` GitHub workflow security
  contracts). 보안 계약은 우회하지 않았다.

## Related Documents

- **Parent Plan**: [Governance Surgical Re-Verification Plan](../plans/2026-06-03-governance-surgical-reverification.md)
- **Governance (Model Policy SSOT)**: [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Gemini Model Tier Review (memory)**: [2026-05-31-gemini-model-tier-review.md](../../00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md)
- **Progress Log**: [progress.md](../../00.agent-governance/memory/progress.md)
