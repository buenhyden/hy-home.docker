---
title: "Workflow Tier (07-workflow) Architecture Description"
version: "1.4.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0007"
parent_ids:
- "REQ-0008"
created: "2026-03-26"
---

# Workflow Tier (07-workflow) Architecture Description

## Context and Boundaries

### System Boundary

- **Owns:** the Airflow services (`airflow-apiserver`, `airflow-scheduler`,
  `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`,
  `airflow-init`, `flower`, `airflow-statsd-exporter`); the n8n services (`n8n`,
  `n8n-worker`, `n8n-task-runner-worker`); the optional
  `blog-ingestion` job; broker wiring; and the Airflow authentication boundary.
- **Consumes:** `04-data` `mng-pg` and `mng-valkey`; `02-auth` Keycloak and
  OAuth2 Proxy; `06-observability` Prometheus and Loki.
- **Does not own:** business logic inside DAGs or n8n workflows, external
  CI/CD, or stream processing.

#### Purpose and Readers

`07-workflow` is the owner-confirmed always-on HOME orchestration layer. It
runs Apache Airflow for code-first DAGs, authenticated natively through the
Keycloak Auth Manager, and n8n for low-code automation with its own login and no
gateway SSO.

#### Context

Browsers reach Airflow, Flower and n8n through Traefik. The tier consumes `mng-pg` and `mng-valkey` (`04-data`), Keycloak and OAuth2 Proxy (`02-auth`), and Prometheus and Loki (`06-observability`).

### Constraints

The tier is owner-confirmed always-on HOME orchestration. Airflow authenticates natively through the Keycloak Auth Manager, n8n through its own login with no gateway SSO, and both share `mng-valkey` as broker with no per-app broker (ADR-0062 decision 10).

## Structure

### Building Blocks

- **Airflow** (`infra/07-workflow/airflow/`) uses `CeleryExecutor`. The image
  is built from `airflow/Dockerfile`, which pins Airflow and the Keycloak
  provider. The API server uses `KeycloakAuthManager` with the Keycloak
  `home-airflow` client and Authorization Services, reads the fixed
  `airflow_api_jwt_secret`, trusts the CA bundle and runs with
  `--proxy-headers`. Its router applies only `gateway-standard-chain@file`.
- **Flower** routes through ForwardAuth.
- **n8n** (`infra/07-workflow/n8n/`) runs in queue mode
  (`EXECUTIONS_MODE: queue`) with an external task runner for the worker
  process (main starts none); its router applies only
  `gateway-standard-chain@file`, and n8n's own login authenticates users.
- **Broker:** both use the shared `mng-valkey`; no per-app broker exists
  (ADR-0062 decision 10).

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Airflow API server browser route | `airflow-apiserver` | Browsers through Traefik `gateway-standard-chain@file` | `KeycloakAuthManager` with the Keycloak `home-airflow` client and Authorization Services; [ADR-0038 Selective Native OIDC](../02.decisions/0038-selective-native-oidc-for-native-auth-apps.md) | The description records no failure handling for this interface. |
| Flower browser route | `flower` | Browsers through the Traefik ForwardAuth chain | ForwardAuth | The description records no failure handling for this interface. |
| n8n browser route | `n8n` | Browsers through Traefik `gateway-standard-chain@file` | The description links no contract for this interface. | The description records no failure handling for this interface. |
| Celery and queue broker | `mng-valkey` (`04-data`) | Airflow (`CeleryExecutor`) and n8n queue mode (`EXECUTIONS_MODE: queue`) | The description links no contract for this interface. | A `mng-valkey` outage stops queued work in both engines; the queue is not a recovery record. |
| Workflow metadata store | `mng-pg` (`04-data`) | Airflow | The description links no contract for this interface. | PostgreSQL metadata and the application encryption key are the durable recovery authority. |
| Metrics and logs | `airflow-statsd-exporter` and Flower | Prometheus and Loki (`06-observability`) | The description links no contract for this interface. | The description records no failure handling for this interface. |

Airflow uses `CeleryExecutor` and a Keycloak `home-airflow` client with Authorization Services; its internal JWT is separate from the Keycloak access token. Flower routes through ForwardAuth, and n8n runs in queue mode with its own login.

## Runtime Behavior

### Normal Flow

#### Runtime View

```text
Browser -> Traefik TLS -> airflow-apiserver -> Keycloak OIDC + Authorization Services
Browser -> Traefik ForwardAuth chain -> flower
Browser -> Traefik TLS -> n8n (own login)
DAG files -> scheduler / dag-processor -> Celery broker -> worker -> task metadata in mng-pg
```

The Airflow internal JWT is separate from the Keycloak access token.
PostgreSQL metadata and the application encryption key are the durable
recovery authority; the Valkey queue is in-flight coordination, not a recovery
record.

#### Deployment View

`workflow` selects Airflow and n8n; `workflow-airflow` and `workflow-n8n`
select one each; core services are HOME. The `blog-ingestion`
capability profile selects the blog ingestion gateway, which shares isolated
internal networks only with `n8n-worker` and Traefik.

### Failure and Recovery

Airflow, n8n and OAuth2 Proxy share `mng-valkey`, so its outage stops queued work in both engines (see Risks below). PostgreSQL metadata and the application encryption key are the durable recovery authority; the Valkey queue is in-flight coordination only.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- **Reliability:** scheduler, worker and triggerer health and broker
  availability.
- **Security:** Airflow uses native OIDC; Flower uses ForwardAuth; n8n uses its own login.
- **Scalability:** Celery workers scale horizontally.
- **Observability:** Flower, the StatsD exporter, logs and metrics.
- **Operability:** provider, database migration and auth bootstrap procedures
  live in Stage 05.

#### Risks

Airflow, n8n and OAuth2 Proxy share `mng-valkey`;
its outage stops queued work in both engines.

### Trade-offs

- Airflow and n8n share `mng-valkey` as broker with no per-app broker
  (ADR-0062 decision 10); the accepted cost is that a `mng-valkey` outage,
  shared also with OAuth2 Proxy, stops queued work in both engines (Risks).
- The Valkey queue is in-flight coordination, not a recovery record;
  PostgreSQL metadata and the application encryption key are the durable
  recovery authority (Runtime View).
- n8n uses its own login with no gateway SSO (Constraints).

## Decisions and Adoption

### Decisions

- [ADR-0007 Airflow and n8n hybrid](../02.decisions/0007-airflow-n8n-hybrid-workflow.md)
- [ADR-0038 Selective Native OIDC](../02.decisions/0038-selective-native-oidc-for-native-auth-apps.md)

### Adoption Boundaries

#### Requirement Mapping

- [REQ-0008 Workflow](../../01.requirements/0008-workflow.md)

#### Currentness and Lineage

The description reflects the current tree at its `updated` date and history lives in Git.

- [Airflow guide](../../05.operations/01.guides/08.workflows-and-automation/0050-airflow.md)
- [Application authentication integration](../../05.operations/01.guides/03.identity-and-access/0079-application-auth-integration.md)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
