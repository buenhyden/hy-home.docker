# 07-Workflow Optimization Hardening Implementation Plan

## Overview (KR)

이 문서는 `infra/07-workflow` 최적화/하드닝 실행 계획서다. gateway 경계 보안 정렬, health 기반 기동 안정화, n8n custom image 하드닝, CI 정책 게이트, 카탈로그 확장 로드맵을 단계적으로 수행한다.

## Context

- 기준 카탈로그: [../08.operations/12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 상위 우선순위 계획: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- 대상 구성: `infra/07-workflow/**/*`, `scripts/`, `.github/workflows/`, `docs/01~09`

## Goals & In-Scope

- **Goals**:
  - Airflow/n8n 경로를 gateway 표준+SSO 정책으로 정렬한다.
  - orchestrator/runtime startup을 health 기반으로 안정화한다.
  - n8n custom image의 non-root/secret guard 계약을 compose 기본값으로 반영한다.
  - workflow 전용 하드닝 검증 스크립트 및 CI 게이트를 도입한다.
  - 카탈로그 확장 항목을 문서/태스크로 실행 가능하게 만든다.
- **In Scope**:
  - `infra/07-workflow/airflow/docker-compose.yml`
  - `infra/07-workflow/n8n/{docker-compose.yml,Dockerfile,docker-entrypoint.sh}`
  - `scripts/check-workflow-hardening.sh`
  - `scripts/README.md`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09` workflow optimization-hardening 문서/README

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Airbyte 서비스 즉시 배포
  - 개별 DAG/workflow 로직 리팩터링
- **Out of Scope**:
  - workflow tier 외 인프라 직접 변경
  - 장기 HA 토폴로지(멀티클러스터) 구현

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-WRK-001 | Airflow/n8n gateway+SSO middleware 정렬 | `infra/07-workflow/*/docker-compose.yml` | REQ-PRD-WRK-FUN-01 | compose labels 확인 |
| PLN-WRK-002 | Airflow health-gated dependency 강화 | `infra/07-workflow/airflow/docker-compose.yml` | REQ-PRD-WRK-FUN-02 | `service_healthy` 계약 확인 |
| PLN-WRK-003 | n8n worker/task-runner health/dependency 보강 | `infra/07-workflow/n8n/docker-compose.yml` | REQ-PRD-WRK-FUN-03 | healthcheck/depends_on 확인 |
| PLN-WRK-004 | n8n custom image 및 entrypoint hardening 반영 | `infra/07-workflow/n8n/{Dockerfile,docker-entrypoint.sh,docker-compose.yml}` | REQ-PRD-WRK-FUN-04 | non-root/secret guard 확인 |
| PLN-WRK-005 | workflow hardening script + CI 게이트 추가 | `scripts/check-workflow-hardening.sh`, `.github/workflows/ci-quality.yml`, `scripts/README.md` | REQ-PRD-WRK-FUN-05 | script/CI job 확인 |
| PLN-WRK-006 | PRD~Runbook 문서 체계 생성 및 상호 링크 | `docs/01~09/**` | REQ-PRD-WRK-FUN-06 | 링크 정합성 확인 |
| PLN-WRK-007 | 카탈로그 확장 항목 작업 분해(Airflow/n8n/airbyte) | Plan/Task/Ops/Guide docs | REQ-PRD-WRK-FUN-07 | 태스크/정책 반영 확인 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-WRK-001 | Structural | Airflow compose 정적 검증 | `docker compose -f infra/07-workflow/airflow/docker-compose.yml config` | 오류 없음 |
| VAL-WRK-002 | Structural | n8n compose 정적 검증 | `docker compose -f infra/07-workflow/n8n/docker-compose.yml config` | 오류 없음 |
| VAL-WRK-003 | Compliance | workflow 하드닝 기준선 검증 | `bash scripts/check-workflow-hardening.sh` | 실패 0건 |
| VAL-WRK-004 | Baseline | 템플릿/보안 기준선 | `bash scripts/check-template-security-baseline.sh` | 실패 0건 |
| VAL-WRK-005 | Traceability | 문서 추적성 검증 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| SSO 강화로 기존 운영 접근 경로 영향 | Medium | runbook에 예외/복구 절차 반영 |
| custom image 빌드 실패로 배포 지연 | Medium | image pin 유지 + compose static 검증 선행 |
| healthcheck 오탐으로 재시작 루프 | Medium | 프로세스 기반 최소 계약으로 시작, 운영 지표 기반 튜닝 |
| airbyte artifact 부재로 계획 공백 | Medium | tasks에 별도 backlog 항목으로 명시 |

## Completion Criteria

- [x] workflow compose/image/script/ci 하드닝 반영
- [x] workflow optimization-hardening 문서 세트 생성
- [x] docs `01~09` README 인덱스 반영
- [ ] runtime 기동/리허설 증적 확보 (환경 허용 시)

## Related Documents

- **PRD**: [../01.prd/2026-03-28-07-workflow-optimization-hardening.md](../01.prd/2026-03-28-07-workflow-optimization-hardening.md)
- **ARD**: [../02.ard/0022-workflow-optimization-hardening-architecture.md](../02.ard/0022-workflow-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0022-workflow-hardening-and-ha-expansion-strategy.md](../03.adr/0022-workflow-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../04.specs/07-workflow/spec.md](../04.specs/07-workflow/spec.md)
- **Tasks**: [../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/07-workflow/optimization-hardening.md](../07.guides/07-workflow/optimization-hardening.md)
- **Operations**: [../08.operations/07-workflow/optimization-hardening.md](../08.operations/07-workflow/optimization-hardening.md)
- **Runbooks**: [../09.runbooks/07-workflow/optimization-hardening.md](../09.runbooks/07-workflow/optimization-hardening.md)
