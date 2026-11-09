---
title: "Workflow Tier (07-workflow) Architecture Description"
version: "1.3.2"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-09"
layer: "architecture"
artifact_id: "AD-0007"
parent_ids:
- "REQ-0008"
created: "2026-03-26"
---

# Workflow Tier (07-workflow) Architecture Description

## Overview

`07-workflow` is the owner-confirmed always-on HOME orchestration layer. It
runs Apache Airflow for code-first DAGs, authenticated natively through the
Keycloak Auth Manager, and n8n for low-code automation with its own login and no
gateway SSO.

## Scope

- **Owns:** the Airflow services (`airflow-apiserver`, `airflow-scheduler`,
  `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`,
  `airflow-init`, `flower`, `airflow-statsd-exporter`); the n8n services (`n8n`,
  `n8n-worker`, `n8n-task-runner-worker`); the optional
  `blog-ingestion` job; broker wiring; and the Airflow authentication boundary.
- **Consumes:** `04-data` `mng-pg` and `mng-valkey`; `02-auth` Keycloak and
  OAuth2 Proxy; `06-observability` Prometheus and Loki.
- **Does not own:** business logic inside DAGs or n8n workflows, external
  CI/CD, or stream processing.

## Structure

### Architecture

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
- **Broker:** both default to `mng-valkey`. The `dedicated-valkey` profile adds
  `airflow-valkey` and `n8n-valkey` with exporters, but selecting it does not
  switch the connection: Airflow must set `AIRFLOW_VALKEY_HOST` and
  `AIRFLOW_VALKEY_SECRET`, and n8n `N8N_VALKEY_HOST` and `N8N_VALKEY_SECRET`,
  as matching pairs.

## Runtime and Deployment

### Runtime View

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

### Deployment View

`workflow` selects Airflow and n8n; `workflow-airflow` and `workflow-n8n`
select one each. `dedicated-valkey` adds the dedicated broker and exporter
pairs, which are OPTIONAL; core services are HOME. The `blog-ingestion`
capability profile selects the blog ingestion gateway, which shares isolated
internal networks only with `n8n-worker` and Traefik.

## Quality and Risks

### Quality Attributes

- **Reliability:** scheduler, worker and triggerer health and broker
  availability.
- **Security:** Airflow uses native OIDC; Flower uses ForwardAuth; n8n uses its own login.
- **Scalability:** Celery workers scale horizontally.
- **Observability:** Flower, the StatsD exporter, logs and metrics.
- **Operability:** provider, database migration and auth bootstrap procedures
  live in Stage 05.

### Risks

Without `dedicated-valkey`, Airflow, n8n and OAuth2 Proxy share `mng-valkey`;
its outage stops queued work in both engines.

### Evolution

Switching to the dedicated brokers is an environment change of the host and
secret pairs, not a profile change.

## Related Documents

- [REQ-0008 Workflow](../../01.requirements/0008-workflow.md)
- [ADR-0007 Airflow and n8n hybrid](../decisions/0007-airflow-n8n-hybrid-workflow.md)
- [ADR-0038 Selective Native OIDC](../decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- [Airflow guide](../../05.operations/guides/08-workflows-and-automation/0050-airflow.md)
- [Application authentication integration](../../05.operations/guides/03-identity-and-access/0079-application-auth-integration.md)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
