# 07-Workflow Optimization Hardening Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 `07-workflow` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. gateway 경계 보안, health 기반 의존성, n8n 이미지 하드닝, 카탈로그 기반 확장 로드맵을 아키텍처 관점에서 정리한다.

## Summary

Workflow tier는 두 가지 실행 평면으로 운영된다.

- Airflow (code-first orchestration)
- n8n (low-code automation)

양 시스템의 관리 평면은 Traefik TLS 경계 뒤에서 표준 middleware+SSO를 공유한다.

## Boundaries & Non-goals

- **Owns**:
  - Workflow 관리 경로 보안 계약
  - Airflow/n8n startup dependency/health 계약
  - n8n runtime image hardening 기준
  - workflow 하드닝 CI 게이트
- **Consumes**:
  - `01-gateway` Traefik middleware chain
  - `02-auth` SSO middleware
  - `04-data` management PostgreSQL
- **Does Not Own**:
  - DAG/workflow 내부 도메인 로직
  - Airbyte production artifact 구현
- **Non-goals**:
  - 즉시 다중 region/cluster workflow 운영
  - Airbyte full deployment 즉시 활성화

## Quality Attributes

- **Performance**: health 기반 기동 순서로 초기 장애/재시작 폭주를 줄인다.
- **Security**: gateway-standard-chain + SSO 체인, n8n non-root + secret guard를 강제한다.
- **Reliability**: worker/task-runner healthcheck와 dependency gating으로 안정성을 강화한다.
- **Scalability**: Airflow worker autoscale 기준과 queue metrics 기반 확장 정책을 준비한다.
- **Observability**: workflow stack health를 compose/CI 수준에서 검증한다.
- **Operability**: `check-workflow-hardening.sh`를 운영 기준선으로 사용한다.

## System Overview & Context

- **Ingress path**:
  - Client -> Traefik(websecure) -> workflow routers -> Airflow/n8n UI
- **Control plane**:
  - Airflow API/Scheduler/Worker/Triggerer + Flower
  - n8n main/worker/task-runner
- **Data/control dependencies**:
  - PostgreSQL (metadata), Valkey (queue/broker), SSO middleware

## Data Architecture

- **Key Entities / Flows**:
  - DAG metadata, workflow executions, queue tasks
- **Storage Strategy**:
  - Airflow/n8n state via bind volumes + PostgreSQL metadata
- **Data Boundaries**:
  - workflow tier는 orchestration metadata를 소유하고 business payload schema는 각 도메인이 소유한다.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose (`infra/07-workflow/*`)
- **Deployment Model**:
  - Airflow distributed components + dedicated valkey
  - n8n queue mode + external runner
- **Operational Evidence**:
  - `docker compose config` checks
  - `scripts/check-workflow-hardening.sh`
  - CI `workflow-hardening` job

## Catalog-aligned Expansion Targets

- **Airflow**:
  - DAG quality gate (parse/schedule/delay) CI
  - worker autoscale 기준 정의 및 운영 표준화
- **n8n**:
  - workflow versioning/Git backup 표준화
  - credential store Vault 연계 강화
- **airbyte**:
  - infra artifact(Compose/README) 부재 갭 해소 계획 수립
  - connector 승격 기준(실험 -> 운영) 정의

## Related Documents

- **PRD**: [../01.prd/2026-03-28-07-workflow-optimization-hardening.md](../01.prd/2026-03-28-07-workflow-optimization-hardening.md)
- **Spec**: [../04.specs/07-workflow/spec.md](../04.specs/07-workflow/spec.md)
- **Plan**: [../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0022-workflow-hardening-and-ha-expansion-strategy.md](../03.adr/0022-workflow-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/07-workflow/optimization-hardening.md](../07.guides/07-workflow/optimization-hardening.md)
- **Operation**: [../08.operations/07-workflow/optimization-hardening.md](../08.operations/07-workflow/optimization-hardening.md)
- **Runbook**: [../09.runbooks/07-workflow/optimization-hardening.md](../09.runbooks/07-workflow/optimization-hardening.md)
