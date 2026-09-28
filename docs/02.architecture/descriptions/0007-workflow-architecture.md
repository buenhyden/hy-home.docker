---
title: "Workflow Tier (07-workflow) Architecture Description"
version: "1.2.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0007"
parent_ids:
- "REQ-0008"
created: "2026-03-26"
---

# Workflow Tier (07-workflow) Architecture Description

## Context and Stakeholders

`07-workflow` is the owner-confirmed always-on HOME workflow orchestration layer that runs Apache Airflow and n8n together.
The `dedicated-valkey` profile starts a dedicated broker pair. The actual broker
boundary is chosen by each of Airflow's/n8n's host/secret environment pairs, and
selecting the profile alone does not change the default `mng-valkey` connection.

- **Airflow**: code-first DAG orchestration.
  Web/API authentication uses application-native OIDC/authorization through the
  Keycloak Auth Manager.
- **n8n**: low-code automation and integration.
  The public UI keeps the approved OAuth2 Proxy ForwardAuth boundary.

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

- **Reliability**: scheduler/worker/triggerer health and broker availability.
- **Security**: Airflow uses Native OIDC; Flower/n8n each use their approved gateway auth policy.
- **Scalability**: Celery worker horizontal scaling.
- **Observability**: Flower, StatsD exporter, logs/metrics.
- **Operability**: Manages the provider/database migration and auth bootstrap procedures through Operations documents.

## Components

### Programmatic Orchestration — Airflow

- `airflow-apiserver`
- `airflow-scheduler`
- `airflow-dag-processor`
- `airflow-worker`
- `airflow-triggerer`
- `flower`
- `airflow-statsd-exporter`

The Airflow UI/API directly uses the Keycloak `home-airflow` client and
Authorization Services.

Airflow router:

```text
Traefik -> Airflow -> Keycloak
```

OAuth2 Proxy ForwardAuth is not applied to the Airflow router.

### Visual Automation — n8n

n8n runs in queue mode, and the public UI follows the gateway ForwardAuth policy.

### Broker

Default:

- `mng-valkey`

OPTIONAL services started by the `dedicated-valkey` profile:

- `airflow-valkey`
- `n8n-valkey`

Airflow must switch `AIRFLOW_VALKEY_HOST`/`AIRFLOW_VALKEY_SECRET`, and n8n must
switch `N8N_VALKEY_HOST`/`N8N_VALKEY_SECRET`, as a matching pair to use the
dedicated broker. Core services are `HOME`; the two broker/exporter pairs are
`OPTIONAL`.

## Data Flow

### Airflow

```text
Browser
  -> Traefik TLS
  -> airflow-apiserver
  -> Keycloak OIDC
  -> Keycloak Authorization Services
```

The Airflow internal JWT is separate from the Keycloak access token.

### Flower/n8n

Public routes use each service's approved ForwardAuth chain.

### Workflow Execution

- DAG definitions -> scheduler/dag-processor
- scheduler -> Celery broker
- worker -> task execution
- task metadata -> PostgreSQL

PostgreSQL metadata and the application encryption key are the durable recovery
authority. The Valkey queue is in-flight coordination, not the exact workflow
recovery record.

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
- **Airflow Operations**: [Guide](../../05.operations/guides/0050-airflow.md)
- **Auth Integration**: [Application Authentication Integration Guide](../../05.operations/guides/0079-application-auth-integration.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
