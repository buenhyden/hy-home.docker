# 07-Workflow Optimization Hardening Technical Specification

## Overview (KR)

이 문서는 `infra/07-workflow`(Airflow, n8n) 계층의 최적화/하드닝 기술 명세다. 게이트웨이 경계 보안, health 기반 기동 안정성, n8n 컨테이너 하드닝, CI 정책 게이트, 카탈로그 기반 확장 요구를 구현 계약으로 정의한다.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Airflow/n8n Traefik middleware 계약
  - Airflow/n8n dependency/healthcheck 계약
  - n8n custom image runtime hardening 계약
  - `check-workflow-hardening.sh` 정책 게이트 계약
- **Does Not Own**:
  - 개별 Airflow DAG 비즈니스 로직
  - n8n 워크플로 내부 비즈니스 로직
  - Airbyte 프로덕션 배포(현 단계는 artifact 정의와 승격 기준 정리)

## Related Inputs

- **PRD**: [../../01.prd/2026-03-28-07-workflow-optimization-hardening.md](../../01.prd/2026-03-28-07-workflow-optimization-hardening.md)
- **ARD**: [../../02.ard/0022-workflow-optimization-hardening-architecture.md](../../02.ard/0022-workflow-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../03.adr/0007-airflow-n8n-hybrid-workflow.md](../../03.adr/0007-airflow-n8n-hybrid-workflow.md)
  - [../../03.adr/0022-workflow-hardening-and-ha-expansion-strategy.md](../../03.adr/0022-workflow-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - Airflow UI/Flower 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 사용한다.
  - n8n UI 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 사용한다.
  - Airflow 핵심 서비스(`apiserver`, `scheduler`, `dag-processor`, `worker`, `triggerer`, `flower`)는 `airflow-valkey` health 기반 의존성을 가진다.
  - n8n `worker`, `task-runner`는 healthcheck를 제공하며 `task-runner`는 `n8n`/`n8n-valkey` health 기반 의존성을 가진다.
- **Data / Interface Contract**:
  - Airflow: CeleryExecutor + Valkey broker + PostgreSQL result backend
  - n8n: Queue mode + external runner + PostgreSQL metadata backend
- **Governance Contract**:
  - `scripts/check-workflow-hardening.sh` 통과가 workflow tier 하드닝 기본선이다.
  - CI `workflow-hardening` job이 PR 단계에서 회귀를 차단한다.

## Core Design

- **Gateway Security Plane**:
  - 외부 노출 관리 경로는 TLS 종료 후 표준 체인 + SSO 체인을 강제한다.
- **Orchestration Runtime Plane**:
  - Airflow는 Valkey health를 선행 조건으로 의존성을 정렬한다.
  - n8n은 main/worker/task-runner를 분리해 queue mode로 운영한다.
- **Image Hardening Plane**:
  - n8n은 multi-stage Dockerfile과 `USER node` 기반 비루트 실행을 유지한다.
  - n8n entrypoint는 필수 secret 파일 부재 시 즉시 fail-close 한다.

## Data Modeling & Storage Strategy

- Airflow DAG/log/config/plugins는 `${DEFAULT_WORKFLOW_DIR}/airflow/*` 바인드 볼륨을 사용한다.
- n8n state/custom/task-runner data는 `${DEFAULT_WORKFLOW_DIR}/n8n*` 바인드 볼륨을 사용한다.
- 워크플로 메타데이터는 management PostgreSQL(`infra/04-data`)을 사용한다.

## Interfaces & Data Structures

### Workflow Hardening Control Surface

```yaml
workflow_hardening_controls:
  ingress_security:
    airflow: gateway-standard-chain + sso-errors + sso-auth
    flower: gateway-standard-chain + sso-errors + sso-auth
    n8n: gateway-standard-chain + sso-errors + sso-auth
  startup_health_contract:
    airflow_depends_on: service_healthy
    n8n_worker_healthcheck: required
    n8n_task_runner_healthcheck: required
  container_hardening:
    n8n_runtime_user: node
    n8n_entrypoint_secret_guard: required
```

## Edge Cases & Error Handling

- SSO 체인 강화 이후 자동화 경로 접근 실패 시 운영 승인 기반 예외 절차를 적용한다.
- Airflow Valkey health 미통과 시 orchestrator startup은 fail-fast 한다.
- n8n 필수 secret 누락 시 entrypoint에서 즉시 종료하고 장애를 명시적으로 노출한다.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: middleware 오구성으로 UI 접근 실패
  - **Fallback**: 최근 정상 compose 버전으로 롤백
  - **Human Escalation**: Gateway/Auth 운영 승인자
- **Failure Mode**: worker/task-runner 기동 실패
  - **Fallback**: healthcheck/depends_on 계약 재적용 후 재기동
  - **Human Escalation**: Workflow on-call

## Verification

```bash
docker compose -f infra/07-workflow/airflow/docker-compose.yml config
docker compose -f infra/07-workflow/n8n/docker-compose.yml config
bash scripts/check-workflow-hardening.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-WRK-001**: Airflow/n8n compose static validation 통과
- **VAL-WRK-002**: workflow hardening baseline script 실패 0건
- **VAL-WRK-003**: PRD~Runbook optimization-hardening 문서 링크 정합성 유지
- **VAL-WRK-004**: 카탈로그 `07-workflow` 확장 항목(Airflow DAG quality gate, n8n backup/Vault, airbyte artifact gap)이 문서/태스크에 반영

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/07-workflow/optimization-hardening.md](../../07.guides/07-workflow/optimization-hardening.md)
- **Operation**: [../../08.operations/07-workflow/optimization-hardening.md](../../08.operations/07-workflow/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/07-workflow/optimization-hardening.md](../../09.runbooks/07-workflow/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
