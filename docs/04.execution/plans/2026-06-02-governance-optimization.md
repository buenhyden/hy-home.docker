---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-06-02-governance-optimization.md -->

# Governance Optimization (I1+I2) Implementation Plan

> 거버넌스 고도화 라운드의 실행 계획서다. 범위는 I1(신규 서비스 Project Template)과
> I2(코드리뷰 요청/수용 루프)로 한정한다.

## Overview (KR)

이 문서는 워크스페이스 거버넌스 고도화의 실행 계획서다. Phase 1 진단에서 토대가
견고함(계약 검사 통과)을 확인한 뒤, 실질 가치가 큰 두 항목만 우선 적용한다.

## Context

Phase 1 조사 결과 Stage 00 거버넌스·QA/CI·Template Contract·Model Policy·Claude 하니스
패리티는 이미 충족 상태였고, `check-repo-contracts.sh`와 `check-doc-traceability.sh`가
모두 `failures=0`이었다. 따라서 재구축이 아니라 빈칸 보강이 필요했다. 진단에서 도출된
실질 갭은 두 가지다. 첫째, 신규 서비스 온보딩용 복사 가능한 표준 시드가 없었다
(`examples/`는 비어 있었다). 둘째, 코드리뷰의 요청→수용→반영 규율이 명문화되지 않았다.

## Goals & In-Scope

- **Goals**: 신규 서비스를 보안 하드닝 표준과 함께 시작할 수 있는 시드·템플릿·가이드를 제공하고, 코드리뷰 루프를 거버넌스에 명문화한다.
- **In Scope**: I1(`examples/sample-web-service/` 시드, `service.template.md`, 온보딩 가이드, 4파일 등록), I2(`workflows.md`·`git-workflow.md` 리뷰 루프).

## Non-Goals & Out-of-Scope

- **Non-goals**: Node 빌드 체계 도입(R1=현행 유지), 서비스 온보딩 워크플로우 승격(R2=단발 템플릿).
- **Out of Scope**: I3(humanizer 경계)·I4(QA 선제 주석)·I5(중복 Related Documents 가드)·I6(RTK 규약)은 후속 라운드로 이연.

## Work Breakdown

| Task    | Description                                                      | Files / Docs Affected                                                                                                                                                                                                                        | Target REQ | Validation Criteria                      |
| ------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------- |
| PLN-001 | 보안 하드닝 내장 서비스 시드 작성                                | `examples/sample-web-service/`                                                                                                                                                                                                               | I1         | `docker compose config` 파싱, YAML 유효  |
| PLN-002 | 서비스 스캐폴드 템플릿 신설 및 4파일 등록                        | `docs/99.templates/service.template.md`, `scripts/validation/check-repo-contracts.sh`, `docs/99.templates/README.md`, `docs/00.agent-governance/rules/documentation-protocol.md`, `docs/00.agent-governance/rules/stage-authoring-matrix.md` | I1         | 계약 검사 `failures=0`                   |
| PLN-003 | 신규 서비스 온보딩 가이드 작성                                   | `docs/05.operations/guides/00-workspace/new-service-onboarding.md`                                                                                                                                                                                        | I1         | guide 프로파일 heading 충족, 정규화 통과 |
| PLN-004 | 코드리뷰 요청/수용 루프 명문화                                   | `docs/00.agent-governance/rules/workflows.md`, `docs/00.agent-governance/rules/git-workflow.md`                                                                                                                                              | I2         | 계약 검사 `failures=0`                   |
| PLN-005 | 생성물 freshness 계약(LLM Wiki 인덱스 재생성)을 QA 스코프에 주입 | `docs/00.agent-governance/scopes/qa.md`                                                                                                                                                                                                      | QA         | 계약 검사 `failures=0`                   |

## Verification Plan

| ID          | Level      | Description         | Command / How to Run                                                                               | Pass Criteria |
| ----------- | ---------- | ------------------- | -------------------------------------------------------------------------------------------------- | ------------- |
| VAL-PLN-001 | Structural | 저장소 계약 동기화  | `bash scripts/validation/check-repo-contracts.sh`                                                  | `failures=0`  |
| VAL-PLN-002 | Structural | 문서 트레이서빌리티 | `bash scripts/validation/check-doc-traceability.sh`                                                | `failures=0`  |
| VAL-PLN-003 | Structural | 시드 compose 유효성 | `python3 -c "import yaml; yaml.safe_load(open('examples/sample-web-service/docker-compose.yml'))"` | 예외 없음     |

## Risks & Mitigations

| Risk                                       | Impact | Mitigation                                                              |
| ------------------------------------------ | ------ | ----------------------------------------------------------------------- |
| 새 템플릿 유형 추가로 4파일 결합 계약 위반 | High   | 등록 직후 계약 검사 재실행, 단계별 검증                                 |
| 시드 compose가 인프라 게이트에 잡힘        | Medium | 디스커버리 스코프 확인 — 게이트는 `infra/`만 스캔, `examples/`는 비스캔 |
| 가이드 placeholder 잔존으로 정규화 실패    | Medium | placeholder 패턴 제거 후 재검증                                         |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: N/A — 거버넌스/문서 변경, 모델 평가 대상 아님.
- **Sandbox / Canary Rollout**: N/A.
- **Human Approval Gate**: plan mode 승인 + 구현 중 결정 확인(R1/R2/D3 + I1 착지면).
- **Rollback Trigger**: 계약 검사 회귀 시 변경 되돌림.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

## Related Documents

- **Task**: [Governance optimization task](../tasks/2026-06-02-governance-optimization.md)
- **Service template**: [Service scaffold template](../../99.templates/service.template.md)
- **Workflow rule**: [Workflows](../../00.agent-governance/rules/workflows.md)
- **Operations**: [New-service onboarding guide](../../05.operations/guides/00-workspace/new-service-onboarding.md)
