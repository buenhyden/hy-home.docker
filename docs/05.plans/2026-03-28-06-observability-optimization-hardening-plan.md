# 06-Observability Optimization Hardening Implementation Plan

## Overview (KR)

이 문서는 `infra/06-observability` 최적화/하드닝 실행 계획서다. 게이트웨이 경계 강화, health 기반 기동 안정화, 커스텀 이미지 하드닝, CI 기준선 도입, 문서 계층 동기화를 단계적으로 수행한다.

## Context

- 기준 카탈로그: [12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 상위 우선순위 계획: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- 대상 구성: `infra/06-observability` compose + custom image + docs/ci/scripts

## Goals & In-Scope

- **Goals**:
  - 관측성 공개 경로를 게이트웨이 표준 체인 + SSO 정책에 정렬한다.
  - 초기 기동 안정성을 위해 health 기반 의존성 계약을 강화한다.
  - Loki/Tempo 커스텀 이미지 런타임 하드닝을 보강한다.
  - 관측성 전용 하드닝 게이트를 CI에 추가한다.
  - PRD~Runbook 문서를 optimization-hardening 기준으로 동기화한다.
- **In Scope**:
  - `infra/06-observability/docker-compose.yml`
  - `infra/06-observability/loki/{Dockerfile,docker-entrypoint.sh}`
  - `infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
  - `scripts/check-observability-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09/**` observability optimization-hardening 문서/README

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 멀티클러스터 observability 즉시 도입
  - 애플리케이션 계측 SDK 리팩터링
- **Out of Scope**:
  - 비관측성 티어 직접 변경
  - 장기보관 백엔드 전환(TSDB/remote backend migration)

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-OBS-001 | 공개 라우터 middleware 계약 정렬 | `infra/06-observability/docker-compose.yml` | REQ-PRD-OBS-FUN-01,02 | 라벨 문자열 검증 |
| PLN-OBS-002 | Loki/Tempo/Pyroscope 라우팅 경계 명시 | `infra/06-observability/docker-compose.yml` | REQ-PRD-OBS-FUN-01,02 | router/service 라벨 확인 |
| PLN-OBS-003 | health 기반 의존성 및 cAdvisor healthcheck 보강 | `infra/06-observability/docker-compose.yml` | REQ-PRD-OBS-FUN-03,04 | compose static check |
| PLN-OBS-004 | Loki/Tempo 커스텀 이미지 하드닝 | `infra/06-observability/loki/*`, `infra/06-observability/tempo/*` | REQ-PRD-OBS-FUN-05 | Dockerfile/entrypoint 패턴 확인 |
| PLN-OBS-005 | observability 하드닝 기준선 스크립트 추가 | `scripts/check-observability-hardening.sh` | REQ-PRD-OBS-FUN-06 | script pass/fail 동작 |
| PLN-OBS-006 | CI `observability-hardening` job 추가 | `.github/workflows/ci-quality.yml` | REQ-PRD-OBS-FUN-06 | workflow job 확인 |
| PLN-OBS-007 | PRD~Runbook 문서 세트 생성/갱신 | `docs/01~09/**` | REQ-PRD-OBS-FUN-07 | 상호 링크/README 반영 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-OBS-001 | Structural | Observability compose 정적 검증 | `docker compose -f infra/06-observability/docker-compose.yml config` | 오류 없음 |
| VAL-OBS-002 | Compliance | 관측성 하드닝 기준선 검증 | `bash scripts/check-observability-hardening.sh` | 실패 0건 |
| VAL-OBS-003 | Baseline | 템플릿/보안 기준선 | `bash scripts/check-template-security-baseline.sh` | 실패 0건 |
| VAL-OBS-004 | Traceability | 문서 추적성 검증 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| SSO 체인 강화로 일부 운영 접근 경로 영향 | Medium | runbook에 예외 승인/복구 절차 명시 |
| 라우터 오구성으로 UI 접근 장애 | High | compose 정적 검증 + hardening script + 롤백 절차 |
| 문서 인덱스 누락 | Medium | 변경 폴더 README 동시 갱신 |
| runtime 환경 의존으로 실운영 검증 지연 | Medium | CI 정적/정책 검증을 필수 게이트로 승격 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: `check-observability-hardening`, `check-template-security-baseline`, `check-doc-traceability`
- **Sandbox / Canary Rollout**: `obs` profile 단위 기동 후 health 확인
- **Human Approval Gate**: 접근제어 완화, 포트 노출 확대, HA 토폴로지 변경
- **Rollback Trigger**: compose 검증 오류, CI 게이트 실패, 라우팅 접근 장애
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] observability compose 하드닝 항목 반영
- [x] observability-hardening 스크립트 및 CI 게이트 반영
- [x] 01~09 optimization-hardening 문서 및 README 인덱스 동기화
- [ ] runtime 검증 증적 확보(환경 가능 시)

## Related Documents

- **PRD**: [../01.prd/2026-03-28-06-observability-optimization-hardening.md](../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../02.ard/0021-observability-optimization-hardening-architecture.md](../02.ard/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../04.specs/06-observability/spec.md](../04.specs/06-observability/spec.md)
- **Tasks**: [../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/06-observability/optimization-hardening.md](../07.guides/06-observability/optimization-hardening.md)
- **Operations**: [../08.operations/06-observability/optimization-hardening.md](../08.operations/06-observability/optimization-hardening.md)
- **Runbooks**: [../09.runbooks/06-observability/optimization-hardening.md](../09.runbooks/06-observability/optimization-hardening.md)
