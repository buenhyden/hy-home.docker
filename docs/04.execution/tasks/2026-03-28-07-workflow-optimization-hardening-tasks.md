---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md -->

# Task: 07-Workflow Optimization Hardening

## Overview (KR)

이 문서는 `07-workflow` 최적화/하드닝 실행 태스크를 추적한다. compose/image hardening, CI 게이트, 문서 추적성, 카탈로그 확장 로드맵을 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../../03.specs/07-workflow/spec.md](../../03.specs/07-workflow/spec.md)
- **Parent Plan**: [../plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../plans/2026-03-28-07-workflow-optimization-hardening-plan.md)

## Working Rules

- workflow 구성 변경은 compose static validation + hardening script 결과를 남긴다.
- 보안 경계 변경은 gateway/auth 영향 범위를 기록한다.
- 문서 변경은 PRD~Runbook 링크와 README 인덱스를 동시 갱신한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-WRK-001 | Airflow/n8n middleware를 gateway+SSO 체인으로 정렬 | impl | Contracts / Config | PLN-WRK-001 | compose label 확인 | DevOps | Done |
| T-WRK-002 | Airflow service dependency를 valkey health 기반으로 강화 | impl | Contracts / Config | PLN-WRK-002 | compose `service_healthy` 확인 | DevOps | Done |
| T-WRK-003 | n8n worker/task-runner healthcheck 및 dependency gating 추가 | impl | Contracts / Config | PLN-WRK-003 | healthcheck/depends_on 확인 | DevOps | Done |
| T-WRK-004 | n8n custom image compose 승격 + entrypoint secret guard 적용 | impl | Core Design / Image Hardening | PLN-WRK-004 | Dockerfile/entrypoint 확인 | DevOps | Done |
| T-WRK-005 | workflow hardening command 정렬 | ops | Governance Contract | PLN-WRK-005 | `bash scripts/hardening/check-all-hardening.sh 07-workflow` | DevOps | Done |
| T-WRK-006 | CI `infrastructure-hardening` job 추가 | ops | Governance Contract | PLN-WRK-005 | workflow job 확인 | DevOps | Done |
| T-WRK-007 | scripts inventory/usage README 갱신 | doc | Related Docs | PLN-WRK-005 | README 항목 반영 | Docs | Done |
| T-WRK-008 | PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook 문서 생성 | doc | Related Docs | PLN-WRK-006 | 링크/인덱스 동기화 | Docs | Done |
| T-WRK-009 | Airflow DAG quality gate/worker autoscale 기준 문서화 | doc | Catalog Expansion Targets | PLN-WRK-007 | ops/guide/task 반영 | DevOps | Done |
| T-WRK-010 | n8n Git backup/Vault credential 연계 기준 문서화 | doc | Catalog Expansion Targets | PLN-WRK-007 | ops/guide/task 반영 | DevOps | Done |
| T-WRK-012 | 정적 검증 실행 및 결과 기록 | test | Verification | PLN-WRK-001~007 | compose/script/baseline/traceability 체크 | DevOps | Done |
| T-WRK-013 | runtime 기동 및 복구 리허설 증적 수집 | test | Verification | PLN-WRK-001~007 | Live health/recovery logs require an approved runtime rehearsal | DevOps | Deferred |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-WRK-001
- [x] T-WRK-002
- [x] T-WRK-003
- [x] T-WRK-004
- [x] T-WRK-005
- [x] T-WRK-006
- [x] T-WRK-007

### Phase 2

- [x] T-WRK-008
- [x] T-WRK-009
- [x] T-WRK-010
- [x] T-WRK-012
- [x] T-WRK-013 (Deferred runtime evidence recorded)

## Verification Summary

- **Test Commands**:
  - `HYHOME_COMPOSE_PROFILES=workflow bash scripts/validation/validate-docker-compose.sh`
  - `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
  - `bash scripts/hardening/check-all-hardening.sh 07-workflow`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: 로컬 검증 로그 + CI `infrastructure-hardening` job
- **Deferred Runtime Evidence**: T-WRK-013 remains a live rehearsal item, not an unimplemented static hardening task.

## Related Documents

- **PRD**: [../01.requirements/2026-03-28-07-workflow-optimization-hardening.md](../../01.requirements/2026-03-28-07-workflow-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md](../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **Guide**: [../../05.operations/guides/07-workflow/optimization-hardening.md](../../05.operations/guides/07-workflow/optimization-hardening.md)
- **Operation**: [../../05.operations/policies/07-workflow/optimization-hardening.md](../../05.operations/policies/07-workflow/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/07-workflow/optimization-hardening.md](../../05.operations/runbooks/07-workflow/optimization-hardening.md)
