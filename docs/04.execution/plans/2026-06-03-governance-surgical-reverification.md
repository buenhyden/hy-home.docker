---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-06-03-governance-surgical-reverification.md -->

# Governance Surgical Re-Verification + Tech-Stack Drift Closure Implementation Plan

## Overview

이 문서는 공유 거버넌스(Stage 00)·Claude 하네스·Model Policy·Template Contract의 외과적
재검증과, 그 과정에서 드러난 단일 비(非)거버넌스 블로커(Dependabot發 tech-stack 버전
드리프트) 종결의 실행 계획서다. 본 작업은 cross-cutting 거버넌스 작업으로, parent Spec
대신 거버넌스 문서를 참조한다(`documentation-protocol.md` §8.5).

## Context

`/plan` 요청은 단일 공유 거버넌스의 3-Phase 신규 구축을 가정했으나, Phase 1 조사 결과
거버넌스·Claude 하네스·QA/CI·Template Contract·Model Policy가 이미 성숙·정합 상태이며
2026-06-02까지 검증을 통과했음이 확인되었다(`memory/progress.md`). 사용자 승인에 따라
범위를 "외과적 재검증 + 갭 종결"로 한정하고, 모델 최신성은 웹으로 재검증했다.

재검증 중 `check-repo-contracts.sh`가 유일하게 `failures=1`을 보고했고, 원인은 거버넌스와
무관한 Dependabot 자동 범프(`71edcd7d`, `5d0ed12b`)가 compose 이미지 태그를 올린 뒤 정본
레지스트리 `infra/tech-stack.versions.json`이 따라가지 못한 9개 컴포넌트의 버전 드리프트였다.
사용자 승인에 따라 레지스트리를 실제 compose 선언값에 동기화했다(런타임·compose 무변경).

## Goals & In-Scope

- **Goals**:
  - 거버넌스·Claude 하네스·Model Policy·Template Contract가 여전히 정합·통과함을 재검증한다.
  - 모델 최신성(Claude/Codex/Gemini)을 2026-06-03 기준으로 재확인하고 증거를 갱신한다.
  - 집계 게이트를 막는 tech-stack 버전 드리프트를 레지스트리 동기화로 종결한다.
  - Phase 1–4 추적 증거(PLAN/TASK/progress)를 남긴다.
- **In Scope**:
  - `infra/tech-stack.versions.json` 9개 항목 동기화(데이터 레지스트리만).
  - 재발 방지: compose→레지스트리 sync 스크립트 + 읽기전용 CI 드리프트 게이트.
  - Gemini 티어 리뷰 메모리 노트의 2026-06-03 재검증 기록.
  - Stage 04 PLAN/TASK 및 progress 로그 작성.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Stage 00 정책·정의 재작성, Model Policy 표 편집, provider adapter 재생성.
  - `docs/01–05` 일괄 재작성(Template Contract는 이미 강제·통과).
- **Out of Scope**:
  - compose 파일·런타임 컨테이너·secret·remote GitHub 변경.
  - Gemini 티어 정책 변경(`gemini-3.5-pro` 미출시로 게이트 조건 미충족).
  - CI 자동커밋: 저장소 보안 계약이 워크플로 `contents: write`를 하드 금지하므로 미채택
    (읽기전용 게이트 + 원커맨드 sync로 대체).

## Work Breakdown

| Task    | Description                              | Files / Docs Affected                                                                            | Target REQ          | Validation Criteria                                    |
| ------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------- | ------------------------------------------------------ |
| PLN-001 | 거버넌스 범위 QA/CI 게이트 재실행        | `scripts/validation/*`, `scripts/hardening/*`                                                    | N/A (cross-cutting) | 모든 거버넌스 게이트 `failures=0`/PASS                 |
| PLN-002 | 모델 최신성 웹 재검증 + 저장소 교차 점검 | `subagent-protocol.md`, `.claude/agents/*.md`                                                    | N/A                 | Claude/Codex 현행, Gemini `3.5-pro` 미GA, stale 모델 0 |
| PLN-003 | tech-stack 드리프트 동기화               | `infra/tech-stack.versions.json`                                                                 | N/A                 | `check-repo-contracts.sh` `failures=0`                 |
| PLN-004 | Gemini 티어 메모리 재검증 기록           | `memory/2026-05-31-gemini-model-tier-review.md`                                                  | N/A                 | 2026-06-03 재검증 절 추가, `Last Verified` 갱신        |
| PLN-005 | 추적 증거 작성                           | 본 PLAN, 짝 TASK, 두 README, `progress.md`                                                       | N/A                 | 문서 4종 작성/갱신, traceability PASS                  |
| PLN-006 | compose→레지스트리 sync 스크립트 + 등록  | `scripts/operations/sync-tech-stack-versions.sh`, `check-repo-contracts.sh`, `scripts/README.md` | N/A                 | 양성 테스트 통과, usage contract PASS                  |
| PLN-007 | 읽기전용 CI 드리프트 게이트              | `.github/workflows/tech-stack-version-sync.yml`                                                  | N/A                 | 워크플로 보안 계약 PASS, `contents: read`              |

## Verification Plan

| ID          | Level      | Description                                        | Command / How to Run                                            | Pass Criteria                          |
| ----------- | ---------- | -------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------- |
| VAL-PLN-001 | Structural | 저장소 계약(Model Policy + Template Contract 포함) | `bash scripts/validation/check-repo-contracts.sh`               | `failures=0`                           |
| VAL-PLN-002 | Structural | 문서 추적성                                        | `bash scripts/validation/check-doc-traceability.sh`             | `failures=0`, `catalog_pairs_total=46` |
| VAL-PLN-003 | Structural | 문서-구현 정합                                     | `bash scripts/validation/check-doc-implementation-alignment.sh` | `failures=0`                           |
| VAL-PLN-004 | Runtime    | Compose 검증 + 하드닝                              | `validate-docker-compose.sh`, `check-all-hardening.sh`          | PASS                                   |
| VAL-PLN-005 | Integrity  | JSON 유효성 + diff 위생                            | `python3 -m json.tool`, `git diff --check`                      | OK / 무결과                            |

## Risks & Mitigations

| Risk                                        | Impact | Mitigation                                                       |
| ------------------------------------------- | ------ | ---------------------------------------------------------------- |
| 레지스트리 동기화가 의도치 않은 런타임 영향 | Low    | compose·런타임 무변경, 데이터 레지스트리(드리프트 게이트)만 수정 |
| Gemini 티어를 근거 없이 변경                | Medium | `gemini-3.5-pro` 미GA 확인, 표 무변경·메모리 로그 유지           |
| 범위 확장(거버넌스 외 인프라)               | Medium | 사용자 승인 후에만 드리프트 종결, 9개 항목으로 한정              |

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

## Related Documents

- **Governance (Model Policy SSOT)**: [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Governance Hub**: [Stage 00 README](../../00.agent-governance/README.md)
- **Task**: [Governance Surgical Re-Verification task](../tasks/2026-06-03-governance-surgical-reverification.md)
- **Gemini Model Tier Review (memory)**: [2026-05-31-gemini-model-tier-review.md](../../00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md)
- **Progress Log**: [progress.md](../../00.agent-governance/memory/progress.md)
