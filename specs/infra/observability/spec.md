---
title: 'Infrastructure Observability (LGTM) Implementation Spec'
status: 'Draft'
version: '1.0'
owner: 'Reliability Engineer'
prd_reference: '../../../docs/prd/observability-prd.md'
api_reference: 'N/A'
arch_reference: '../../../ARCHITECTURE.md'
tags: ['spec', 'infra', 'observability', 'lgtm', 'grafana', 'loki', 'tempo', 'prometheus']
---

# Implementation Specification (Spec)

> **Status**: Draft
> **Related PRD**: [docs/prd/observability-prd.md](../../../docs/prd/observability-prd.md)
> **Related Architecture**: [ARCHITECTURE.md](../../../ARCHITECTURE.md)

_Target Directory: `specs/infra/observability/spec.md`_

---

## 0. Pre-Implementation Checklist (Governance)

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Root-only Compose stack with `obs` profile. | Section 1 |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | Boundaries are defined by `infra/06-observability/docker-compose.yml`. | Section 5 |
| Domain Model       | Are core domain entities and relationships defined?   | Must     | N/A (infra stack). | N/A |
| Backend Stack      | Are language/framework/libs (web, ORM, auth) decided? | Must     | N/A (infra stack). | N/A |
| Frontend Stack     | Are framework/state/build tools decided?              | Must     | Grafana UI is a containerized dependency (no in-repo build). | Section 1 |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | Compose config validation + healthchecks + UI/API smoke checks. | Section 7 |
| Test Tooling    | Agreed framework/runner and mock strategy?     | Must     | `docker compose config -q` + runtime smoke checks. | Section 7 |
| Coverage Policy | Are goals defined as numbers (e.g. 100%)?      | Must     | N/A (infra-only). | N/A |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | Grafana auth is configured at the stack level; SSO middleware must be explicit (no implied controls). | Section 4 |
| Data Protection | Encryption/access policies for sensitive data? | Must     | Credentials (Grafana admin, SMTP, etc.) are injected via Docker secrets. | Section 9 |
| Performance     | Are Core Web Vitals/Latency metrics targeted?  | Must     | N/A (infra-only). | N/A |
| Accessibility   | Is WCAG compliance integrated (contrast/ARIA)? | Must     | N/A (third-party UI). | N/A |

### 0.3 Operations / Deployment / Monitoring

| Item         | Check Question                                           | Required | Alignment Notes | Where to document |
| ------------ | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments | Are tiers (dev/staging/prod) clarified for this feature? | Must     | Local/internal development environment only. | Section 9 |
| Logging      | Required structured logs defined (fields, IDs)?          | Must     | Loki logging driver is used by infra services via shared templates. | Section 9 |
| Monitoring   | Metrics and dashboards defined (RED/USE)?                | Must     | Prometheus scrapes infra exporters; Grafana dashboards visualize metrics/logs/traces. | Section 9 |
| Alerts       | Are alert thresholds and routing defined?                | Must     | Alertmanager runs in `obs` profile; alert rules live under `infra/06-observability/prometheus/config/alert_rules`. | Section 9 |
| Backups      | Are backup policies defined for added data?              | Must     | Persistence uses host-mapped volumes; backups are out of scope for this spec. | Section 9 |

---

## 1. Technical Overview & Architecture Style

This spec defines the local observability stack (LGTM):

- **Loki**: log storage
- **Tempo**: trace storage
- **Prometheus**: metrics storage and scraping
- **Grafana**: unified UI for logs/metrics/traces
- **Alloy**: telemetry collection/forwarding (OTLP) where applicable

The stack is enabled via the standard Compose profile `obs` and runs inside `infra_net`.

## 2. Coded Requirements (Traceability)

| ID                 | Requirement Description | Priority | Parent PRD REQ |
| ------------------ | ----------------------- | -------- | -------------- |
| **REQ-SPC-OBS-001** | Observability stack MUST be gated behind the `obs` profile. | High | REQ-PRD-OBS-FUN-001 |
| **REQ-SPC-OBS-002** | Secrets (Grafana admin, SMTP, etc.) MUST be injected via Docker secrets. | Critical | N/A |
| **REQ-SPC-OBS-003** | All containers SHOULD use the Loki logging driver via shared templates. | High | REQ-PRD-OBS-FUN-001 |

## 3. Data Modeling & Storage Strategy

- **Prometheus TSDB**: `${DEFAULT_OBSERVABILITY_DIR}/prometheus`
- **Loki data**: `${DEFAULT_OBSERVABILITY_DIR}/loki`
- **Tempo data**: `${DEFAULT_OBSERVABILITY_DIR}/tempo`
- **Grafana data**: `${DEFAULT_OBSERVABILITY_DIR}/grafana`

## 4. Interfaces & Data Structures

### 4.1 Core Interfaces

- **Grafana**: `https://grafana.${DEFAULT_URL}`
- **Prometheus**: `https://prometheus.${DEFAULT_URL}`

### 4.2 AuthN / AuthZ

- Any SSO/RBAC controls must be explicitly configured and traceable to ADR/ARD (avoid “implied” auth).

## 5. Component Breakdown

- **`infra/06-observability/docker-compose.yml`**: primary LGTM stack definition (profile `obs`)
- **`infra/common-optimizations.yml`**: shared logging/security/resource templates (Loki logging driver)

## 6. Edge Cases & Error Handling

- **Loki driver not installed**: host must support the Loki logging driver used by the shared templates.
- **High-cardinality labels**: label hygiene is required to avoid Loki ingestion overload.

## 7. Verification Plan (Testing & QA)

- **[VAL-OBS-001] Compose schema**: `COMPOSE_PROFILES=core,data,obs docker compose --env-file .env.example config -q`
- **[VAL-OBS-002] Runtime health**: `docker compose up -d` then `docker compose ps` shows `healthy` where defined
- **[VAL-OBS-003] Grafana health**: `curl -fk https://grafana.${DEFAULT_URL}/api/health`

## 8. Non-Functional Requirements (NFR) & Scalability

- **Stability**: every long-running service must declare resource bounds through shared templates.
- **Portability**: DNS-only internal connectivity, no static IP dependencies.

## 9. Operations & Observability

- **Logs**: Loki logging driver + Loki backend storage.
- **Metrics**: Prometheus + exporters across core/data services.
- **Traces**: Tempo + OTLP collection (as configured via Alloy).
- **Sensitive Data Handling**: all credentials are mounted under `/run/secrets/*`.

