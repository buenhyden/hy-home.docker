<!-- Target: docs/05.plans/2026-03-27-infra-service-optimization-priority-plan.md -->

# Infra Service Optimization Priority Plan (Quick Wins + Quarterly) Implementation Plan

> 기준 문서: `docs/08.operations/12-infra-service-optimization-catalog.md`

---

# Infra Service Optimization Priority Plan (Quick Wins + Quarterly)

## Overview (KR)

이 문서는 인프라 서비스 최적화 카탈로그를 기준으로 `docs/05.plans` 레이어에서 실행 우선순위를 고정하는 통합 실행 계획서다.
범위는 문서 기반 실행계획 수립이며, 실제 Compose 변경은 후속 `docs/06.tasks` 단계에서 수행한다.
계획 구조는 Quick Wins(30일) + Quarterly(향후 2개 분기: 2026 Q2, 2026 Q3)로 구성한다.

## Context

- 기준 문서: [12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 기준 데이터(39개 서비스 스냅샷):
  - `healthcheck` 미구성: 6
  - `restart` 미구성: 21
  - `no-new-privileges` 미구성: 37
  - `limits(cpus/memory)` 미구성: 37
  - `secrets` 미구성: 16
- `common-optimizations.yml` 기반 커버리지 스냅샷(2026-03-28):
  - 서비스 디렉터리 기준: `39/39 (100%)` 적용
  - Compose 파일 기준: `43/43 (100%)` 적용
  - 미적용 서비스: 없음 (서비스 기준 `0건`)
  - 보조 Compose: `04-data/analytics/opensearch/docker-compose.cluster.yml` 적용 완료
  - 의도된 템플릿 예외 SSoT: `infra/common-optimizations.exceptions.json`
- `PLN-QW-001~005` 기준선 강제 적용 상태(2026-03-28):
  - 검증 명령: `bash scripts/check-quickwin-baseline.sh`
  - 템플릿/보안 검증 명령: `bash scripts/check-template-security-baseline.sh`
  - 결과: `restart/healthcheck/no-new-privileges/cpus/mem_limit/secrets` 누락 `0` (승인 예외 반영)
  - 승인 예외 SSoT: `infra/common-optimizations.exceptions.json`
- 일정 고정:
  - Quick Wins 기준일: 2026-03-27
  - Quick Wins 목표 완료일: 2026-04-26
  - Quarterly 범위: 2026 Q2, 2026 Q3

## Public Interfaces Impact

- 런타임 API/스키마/코드 인터페이스 변경 없음
- 문서 인터페이스 변경만 발생:
  - `docs/05.plans/README.md` 인덱스 항목 추가
  - 본 계획서의 상대경로 기반 추적 링크 추가

## Goals & In-Scope

- **Goals**:
  - 카탈로그 기반의 실행 우선순위를 의사결정 완료 상태로 고정
  - 30일 내 즉시 위험 저감이 가능한 Quick Wins 백로그 확정
  - 2026 Q2/Q3 분기별 운영 고도화 목표와 완료조건 정의
- **In Scope**:
  - 우선순위 모델 정의 및 티어 가중치 고정
  - Quick Wins 작업 항목(PLN-QW-001 ~ PLN-QW-007) 정의
  - Quarterly 로드맵(분기별 목표/산출물/완료조건) 정의
  - 검증 계획 및 테스트 시나리오 정의

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 실제 `infra/*/docker-compose*` 파일 변경
  - 런타임 서비스 스케일링/배포 수행
- **Out of Scope**:
  - 코드 레벨 성능 튜닝 구현
  - 서비스별 세부 런북 절차 작성/수정

## Priority Model

- Priority Score = `Risk Reduction(40) + Availability Impact(25) + Security Impact(25) + Execution Effort Inverse(10)`
- Tier Weight:
  - Tier A: 01-gateway, 02-auth, 03-security, 04-data, 05-messaging, 06-observability
  - Tier B: 07-workflow, 08-ai, 09-tooling, 10-communication
  - Tier C: 11-laboratory

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-QW-001 | Tier A/B 장기 실행 서비스 `restart` 정책 표준화 | `infra/**/docker-compose*.yml`, `docs/06.tasks/*` | REQ-OPS-BASE-001 | Tier A/B 대상 서비스 `restart` 누락 0건 |
| PLN-QW-002 | `healthcheck` 누락 서비스 보강 우선 적용 (운영 핵심 우선, lab 후순위) | `infra/**/docker-compose*.yml`, `docs/09.runbooks/**` | REQ-OPS-BASE-002 | Tier A/B 핵심 서비스 `healthcheck` 누락 0건 |
| PLN-QW-003 | `no-new-privileges` 기본 적용 원칙 도입 및 예외 목록화 | `infra/**/docker-compose*.yml`, `docs/08.operations/**` | REQ-SEC-BASE-003 | 예외 목록 명시 + 기본 적용률 100% |
| PLN-QW-004 | 리소스 최소 상한(`cpus`, `memory`) 정책 초안 확정 | `docs/08.operations/12-infra-service-optimization-catalog.md`, `docs/06.tasks/*` | REQ-OPS-CAP-004 | 티어별 최소 상한 정책 문서화 완료 |
| PLN-QW-005 | 민감정보 주입 경로 표준화(`secrets`/Vault 우선) | `infra/**/docker-compose*.yml`, `infra/03-security/vault/**`, `docs/08.operations/**` | REQ-SEC-SECRETS-005 | 평문 비밀 주입 경로 감축 및 표준 경로 명시 |
| PLN-QW-006 | `infra/07-workflow/airbyte` 실체 정의 갭 해소 계획(Compose/README) 수립 | `infra/07-workflow/airbyte/**`, `docs/08.operations/07-workflow/airbyte.md`, `docs/09.runbooks/07-workflow/airbyte.md` | REQ-WF-GAP-006 | airbyte 인프라 실체 정의 완료 기준 합의 |
| PLN-QW-007 | 문서 추적성 정리 (`05.plans` ↔ `08.operations` ↔ `09.runbooks`) | `docs/05.plans/**`, `docs/08.operations/**`, `docs/09.runbooks/**` | REQ-DOC-TRACE-007 | 교차 링크 무결성 100% |

## Quarterly Roadmap

| Quarter | Goals | Deliverables | Completion Criteria |
| --- | --- | --- | --- |
| 2026 Q2 (2026-04-01 ~ 2026-06-30) | 운영 기준 코드화(Compose lint/gate), 백업·복구 리허설 정례화, SLO/Alert 정합성 강화 | Compose policy gate 초안, 복구 리허설 캘린더, SLO/Alert 정합성 리포트 | Tier A 핵심 서비스 운영 기준선 100% 충족 |
| 2026 Q3 (2026-07-01 ~ 2026-09-30) | 확장성/성능 최적화(메시징·데이터·AI), 정책 자동검증 CI, 보안 하드닝 고도화 | 성능 최적화 백로그 완료 리포트, 정책 검증 CI 파이프라인, 보안 하드닝 체크리스트 | 분기 성능 회귀 및 장애 복구 리드타임 목표 달성 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | 링크 무결성 (`05.plans` 신규 문서 상대경로 점검) | 상대경로 링크 점검 스크립트 또는 수동 검증 | 모든 링크 대상 파일 존재 |
| VAL-PLN-002 | Compliance | 템플릿 필수 섹션 준수 (`Overview (KR)`, `Work Breakdown`, `Verification`, `Completion`) | 문서 섹션 체크리스트 검토 | 필수 섹션 누락 0건 |
| VAL-PLN-003 | Traceability | 기준 카탈로그와 항목 일치성(Quick Wins/Quarterly 매핑) | 카탈로그 대비 항목 매핑 리뷰 | 누락/중복 없이 1:1 매핑 |
| VAL-PLN-004 | Indexing | `docs/05.plans/README.md` 인덱스 반영 확인 | README Structure 섹션 검토 | 신규 계획서 항목 존재 |
| VAL-PLN-005 | Automation | `05.plans ↔ 08.operations ↔ 09.runbooks` 링크 동기화 자동 검증 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |

## Test Cases / Scenarios

| ID | Scenario | Expected Result |
| --- | --- | --- |
| TST-PLN-001 | 신규 계획서 단독 열람 | Quick Wins/Quarterly/검증 기준/완료 조건이 한 문서에서 의사결정 가능 |
| TST-PLN-002 | 운영자가 카탈로그와 계획서 교차 확인 | 카탈로그 권고가 누락 없이 계획 Task로 매핑됨 |
| TST-PLN-003 | 문서 인덱스 탐색 | `docs/05.plans/README.md`에서 신규 계획서로 즉시 이동 가능 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: 문서 정책/카탈로그/런북 간 링크 및 요구사항 매핑 완전성 검토
- **Sandbox / Canary Rollout**: 후속 `docs/06.tasks` 단계에서 Tier A부터 점진 적용
- **Human Approval Gate**: Infra Lead + Security Reviewer 승인 후 Compose 변경 착수
- **Rollback Trigger**: 계획-카탈로그 불일치 또는 운영 영향 리스크 증가 시 작업 중지/재계획
- **Prompt / Model Promotion Criteria**: N/A (문서 계획 단계)

## Completion Criteria

- [x] 단일 통합 계획서 작성 완료 (Quick Wins + Quarterly 포함)
- [x] 우선순위 모델 및 티어 가중치 고정
- [x] Quick Wins 7개 작업 항목 정의 완료
- [x] 2026 Q2/Q3 분기 로드맵 정의 완료
- [x] 검증 계획(VAL-PLN-001~005) 및 테스트 시나리오 정의 완료
- [x] `docs/05.plans/README.md` 인덱스 갱신 완료

## Assumptions & Defaults

- 실행 담당자 표기는 개인명 대신 역할(Infra Lead, DevOps, SRE, Security) 기준으로 유지한다.
- 본 산출물은 계획 수립 및 인덱싱까지 포함하며, 실제 Compose 수정은 후속 Task 단계에서 수행한다.
- 분기 로드맵 기준일은 2026-03-27로 고정한다.

## Related Documents

- **Operations Catalog**: [12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- **Operations Index**: [08.operations README](../08.operations/README.md)
- **Runbook Index**: [09.runbooks README](../09.runbooks/README.md)
- **Plan Index**: [05.plans README](./README.md)
- **Task Layer**: [06.tasks README](../06.tasks/README.md)
