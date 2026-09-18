---
title: "Workflow Tier (07-workflow) Architecture Description"
version: "1.2.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-18"
layer: "architecture"
artifact_id: "AD-0007"
parent_ids:
- "REQ-0008"
created: "2026-03-26"
---

# Workflow Tier (07-workflow) Architecture Description

## Context and Stakeholders

`07-workflow`는 Apache Airflow와 n8n을 함께 운영하는 workflow orchestration 계층이다.
`dedicated-valkey` profile 선택 여부로 broker 경계를 분리한다.

- **Airflow**: code-first DAG orchestration.
  Web/API authentication은 Keycloak Auth Manager를 통한 application-native
  OIDC/authorization을 사용한다.
- **n8n**: low-code automation과 integration.
  공개 UI는 승인된 OAuth2 Proxy ForwardAuth 경계를 유지한다.

## System Boundaries

- **Owns**:
  - Airflow services (`airflow-apiserver`, scheduler, dag-processor, worker, triggerer, Flower)
  - n8n Server/Worker/Task Runner
  - workflow broker wiring
  - Airflow authentication boundary:
    Traefik gateway-only routing + `KeycloakAuthManager`
- **Consumes**:
  - `04-data` PostgreSQL Management DB
  - `02-auth` Keycloak / OAuth2 Proxy
  - `06-observability` Prometheus/Loki
- **Does Not Own**:
  - business logic inside individual DAGs
  - external CI/CD
  - stream processing

## Quality Attributes

- **Reliability**: scheduler/worker/triggerer health와 broker availability.
- **Security**: Airflow는 Native OIDC, Flower/n8n은 각 승인된 gateway auth 정책.
- **Scalability**: Celery worker horizontal scaling.
- **Observability**: Flower, StatsD exporter, logs/metrics.
- **Operability**: provider/database migration과 auth bootstrap 절차를 Operations 문서로 관리.

## Components

### Programmatic Orchestration — Airflow

- `airflow-apiserver`
- `airflow-scheduler`
- `airflow-dag-processor`
- `airflow-worker`
- `airflow-triggerer`
- `flower`
- `airflow-statsd-exporter`

Airflow UI/API는 Keycloak `home-airflow` client와 Authorization Services를 직접
사용한다.

Airflow router:

```text
Traefik -> Airflow -> Keycloak
```

OAuth2 Proxy ForwardAuth는 Airflow router에 적용하지 않는다.

### Visual Automation — n8n

n8n은 queue mode로 실행되고 공개 UI는 gateway ForwardAuth 정책을 따른다.

### Broker

기본:
- `mng-valkey`

`dedicated-valkey` profile:
- `airflow-valkey`
- `n8n-valkey`

## Data Flow

### Airflow

```text
Browser
  -> Traefik TLS
  -> airflow-apiserver
  -> Keycloak OIDC
  -> Keycloak Authorization Services
```

Airflow internal JWT는 Keycloak access token과 별개다.

### Flower/n8n

공개 route는 서비스별 승인된 ForwardAuth chain을 사용한다.

### Workflow Execution

- DAG definitions -> scheduler/dag-processor
- scheduler -> Celery broker
- worker -> task execution
- task metadata -> PostgreSQL

## Deployment View

Airflow compose:
`infra/07-workflow/airflow/docker-compose.yml`

Airflow auth:
- Airflow 3.3.1
- Keycloak provider 0.9.0
- `KeycloakAuthManager`
- fixed `airflow_api_jwt_secret`
- CA bundle + `--proxy-headers`
- gateway-only router

## Related Documents

- **PRD**: [REQ-0008 Workflow](../../01.requirements/0008-workflow.md)
- **ADR**: [Airflow/n8n hybrid](../decisions/0007-airflow-n8n-hybrid-workflow.md)
- **ADR**: [ADR-0038 Selective Native OIDC](../decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- **Airflow Operations**: [Guide](../../05.operations/catalog/07-workflow/0050-airflow/guide.md)
- **Auth Integration**: [Application Authentication Integration Guide](../../05.operations/catalog/02-auth/0079-application-auth-integration/guide.md)
