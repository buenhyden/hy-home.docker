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

`07-workflow`는 Apache Airflow와 n8n을 함께 운영하는 owner-confirmed always-on HOME workflow orchestration 계층이다.
`dedicated-valkey` profile은 전용 broker pair를 기동한다. 실제 broker
경계는 Airflow/n8n 각각의 host/secret environment pair가 선택하며, profile
선택만으로 기본 `mng-valkey` 연결은 바뀌지 않는다.

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

`dedicated-valkey` profile이 기동하는 OPTIONAL services:

- `airflow-valkey`
- `n8n-valkey`

Airflow는 `AIRFLOW_VALKEY_HOST`/`AIRFLOW_VALKEY_SECRET`, n8n은
`N8N_VALKEY_HOST`/`N8N_VALKEY_SECRET`을 matching pair로 바꿔야 전용
broker를 사용한다. 코어 services는 `HOME`, 두 broker/exporter pairs는
`OPTIONAL`이다.

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

PostgreSQL metadata와 application encryption key가 durable recovery
authority다. Valkey queue는 in-flight coordination이며 정확한 workflow
복구 기록이 아니다.

## Deployment View

Airflow compose:
`infra/07-workflow/airflow/docker-compose.yml`

Airflow auth:

- Airflow, pinned in [build source](../../../infra/07-workflow/airflow/Dockerfile)
- Keycloak provider, pinned in the same Airflow build source
- `KeycloakAuthManager`
- fixed `airflow_api_jwt_secret`
- CA bundle + `--proxy-headers`
- gateway-only router

## Traceability

- **PRD**: [REQ-0008 Workflow](../../01.requirements/0008-workflow.md)
- **ADR**: [Airflow/n8n hybrid](../decisions/0007-airflow-n8n-hybrid-workflow.md)
- **ADR**: [ADR-0038 Selective Native OIDC](../decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- **Airflow Operations**: [Guide](../../05.operations/catalog/07-workflow/0050-airflow/guide.md)
- **Auth Integration**: [Application Authentication Integration Guide](../../05.operations/catalog/02-auth/0079-application-auth-integration/guide.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
