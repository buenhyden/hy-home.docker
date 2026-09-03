---
title: 07-Workflow Optimization Hardening Architecture Description
version: 1.0.0
type: sdlc/architecture-description
layer: architecture
status: active
owner: "@buenhyden"
artifact_id: AD-0022
parent_ids:
  - REQ-0008
created: 2026-03-28
updated: 2026-09-01
---
# 07-Workflow Optimization Hardening Architecture Description

## Context and Stakeholders

이 문서는 `07-workflow` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. gateway 경계 보안, health 기반 의존성, n8n 이미지 하드닝, 카탈로그 기반 확장 로드맵을 아키텍처 관점에서 정리한다.

### Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

Workflow tier는 두 가지 실행 평면으로 운영된다.

- Airflow (code-first orchestration)
- n8n (low-code automation)

양 시스템의 관리 평면은 Traefik TLS 경계 뒤에서 표준 middleware+SSO를 공유한다.


## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

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
  - 신규 workflow service production artifact 구현
- **Non-goals**:
  - 즉시 다중 region/cluster workflow 운영
  - 신규 workflow service full deployment 즉시 활성화

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: health 기반 기동 순서로 초기 장애/재시작 폭주를 줄인다.
- **Security**: gateway-standard-chain + SSO 체인, n8n non-root + secret guard를 강제한다.
- **Reliability**: worker/task-runner healthcheck와 dependency gating으로 안정성을 강화한다.
- **Scalability**: Airflow worker autoscale 기준과 queue metrics 기반 확장 정책을 준비한다.
- **Observability**: workflow stack health를 compose/CI 수준에서 검증한다.
- **Operability**: `check-all-hardening.sh 07-workflow`를 운영 기준선으로 사용한다.

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

- **Ingress path**:
  - Client -> Traefik(websecure) -> workflow routers -> Airflow/n8n UI
- **Control plane**:
  - Airflow API/Scheduler/Worker/Triggerer + Flower
  - n8n main/worker/task-runner
- **Data/control dependencies**:
  - PostgreSQL (metadata), Valkey (queue/broker), SSO middleware

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**:
  - DAG metadata, workflow executions, queue tasks
- **Storage Strategy**:
  - Airflow/n8n state via bind volumes + PostgreSQL metadata
- **Data Boundaries**:
  - workflow tier는 orchestration metadata를 소유하고 business payload schema는 각 도메인이 소유한다.

## Deployment View

- **Runtime / Platform**: Docker Compose (`infra/07-workflow/*`)
- **Deployment Model**:
  - Airflow distributed components; root dev uses shared `mng-valkey`, service-local compose declares dedicated `airflow-valkey`
  - n8n queue mode + external runner; root dev uses shared `mng-valkey`, service-local compose declares dedicated `n8n-valkey`
- **Operational Evidence**:
  - `docker compose config` checks
  - `scripts/hardening/check-all-hardening.sh 07-workflow`
  - CI `infrastructure-hardening` job

## Evolution

- **Airflow**:
  - DAG quality gate (parse/schedule/delay) CI
  - worker autoscale 기준 정의 및 운영 표준화
- **n8n**:
  - workflow versioning/Git backup 표준화
  - credential store Vault 연계 강화
Tracked infra artifact가 없는 신규 workflow service는 active workflow architecture scope에서 제외한다.

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../01.requirements/0019-workflow-optimization-hardening.md](../../01.requirements/0008-workflow.md)
- **Spec**: [../03.specs/008-workflow/spec.md](0007-workflow-architecture.md)
- **ADR**: [../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md](../decisions/0022-workflow-hardening-and-ha-expansion-strategy.md)
- **Guide**: [../../05.operations/guides/07-workflow/optimization-hardening.md](../../05.operations/catalog/07-workflow/0054-optimization-hardening/guide.md)
- **Operation**: [../../05.operations/policies/07-workflow/optimization-hardening.md](../../05.operations/catalog/07-workflow/0054-optimization-hardening/policy.md)
- **Runbook**: [../../05.operations/runbooks/07-workflow/optimization-hardening.md](../../05.operations/catalog/07-workflow/0054-optimization-hardening/runbook.md)
