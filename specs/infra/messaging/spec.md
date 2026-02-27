---
title: 'Infrastructure Messaging (Kafka) Implementation Spec'
status: 'Draft'
version: '1.0'
owner: 'Infrastructure Architect'
prd_reference: '../../../docs/prd/messaging-prd.md'
api_reference: 'N/A'
arch_reference: '../../../ARCHITECTURE.md'
tags: ['spec', 'infra', 'messaging', 'kafka']
---

# Implementation Specification (Spec)

> **Status**: Draft
> **Related PRD**: [docs/prd/messaging-prd.md](../../../docs/prd/messaging-prd.md)
> **Related Architecture**: [ARCHITECTURE.md](../../../ARCHITECTURE.md)

_Target Directory: `specs/infra/messaging/spec.md`_

---

## 0. Pre-Implementation Checklist (Governance)

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Root-only Compose stack with `messaging` profile. | Section 1 |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | Kafka cluster services are defined in a dedicated Compose file. | Section 5 |
| Domain Model       | Are core domain entities and relationships defined?   | Must     | N/A (infra stack). | N/A |
| Backend Stack      | Are language/framework/libs (web, ORM, auth) decided? | Must     | N/A (infra-only). | N/A |
| Frontend Stack     | Are framework/state/build tools decided?              | Must     | N/A. | N/A |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | Compose config validation + broker healthchecks + basic topic publish/consume smoke tests. | Section 7 |
| Test Tooling    | Agreed framework/runner and mock strategy?     | Must     | `docker compose config -q` + local CLI smoke checks. | Section 7 |
| Coverage Policy | Are goals defined as numbers (e.g. 100%)?      | Must     | N/A (infra-only). | N/A |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | ACL/TLS is deferred; baseline is dev-only networking. | Section 4 |
| Data Protection | Encryption/access policies for sensitive data? | Must     | No secrets in plaintext env vars; credentials must be secrets if introduced. | Section 9 |
| Performance     | Are Core Web Vitals/Latency metrics targeted?  | Must     | N/A (infra-only). | N/A |
| Accessibility   | Is WCAG compliance integrated (contrast/ARIA)? | Must     | N/A. | N/A |

### 0.3 Operations / Deployment / Monitoring

| Item         | Check Question                                           | Required | Alignment Notes | Where to document |
| ------------ | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments | Are tiers (dev/staging/prod) clarified for this feature? | Must     | Local/internal development environment only. | Section 9 |
| Logging      | Required structured logs defined (fields, IDs)?          | Must     | Loki logging driver is used via shared templates where supported. | Section 9 |
| Monitoring   | Metrics and dashboards defined (RED/USE)?                | Must     | JMX exporter + Kafka exporter are exposed for Prometheus scraping. | Section 9 |
| Alerts       | Are alert thresholds and routing defined?                | Must     | Alerting is handled in the Observability spec. | Section 9 |
| Backups      | Are backup policies defined for added data?              | Must     | Event retention is local; backups are out of scope. | Section 9 |

---

## 1. Technical Overview & Architecture Style

This spec defines the local Kafka cluster for development and integration testing:

- 3-node Kafka cluster (KRaft mode)
- Schema Registry (if enabled in the compose file)
- Connect/REST proxy components (if enabled)
- Exporters for Prometheus scraping (where configured)

The stack is enabled via the standard Compose profile `messaging` and runs inside `infra_net`.

## 2. Coded Requirements (Traceability)

| ID                 | Requirement Description | Priority | Parent PRD REQ |
| ------------------ | ----------------------- | -------- | -------------- |
| **REQ-SPC-MSG-001** | Kafka stack MUST be gated behind the `messaging` profile. | High | REQ-PRD-MSG-FUN-01 |
| **REQ-SPC-MSG-002** | Cluster MUST be multi-node (3 brokers) for local HA testing. | High | REQ-PRD-MSG-FUN-01 |
| **REQ-SPC-MSG-003** | Internal connectivity MUST use Docker DNS (no static IP pinning). | High | N/A |

## 3. Data Modeling & Storage Strategy

- Broker data is persisted to host paths under `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/*`.

## 4. Interfaces & Data Structures

### 4.1 Core Interfaces

- Producers/consumers connect to the internal listener via Docker DNS and the internal port defined in `.env.example`.

### 4.2 AuthN / AuthZ

- ACLs and TLS are deferred for local development; when enabled, configuration must be documented via ADR + spec update.

## 5. Component Breakdown

- **`infra/05-messaging/kafka/docker-compose.yml`**: Kafka stack (profile `messaging`)

## 6. Edge Cases & Error Handling

- **Host disk pressure**: broker logs can grow quickly; ensure `${DEFAULT_MESSAGE_BROKER_DIR}` has space.
- **Port conflicts**: external listener ports must be coordinated via `.env`.

## 7. Verification Plan (Testing & QA)

- **[VAL-MSG-001] Compose schema**: `COMPOSE_PROFILES=core,data,obs,messaging docker compose --env-file .env.example config -q`
- **[VAL-MSG-002] Broker health (runtime)**: `docker compose --profile messaging up -d` then brokers are healthy
- **[VAL-MSG-003] Topic smoke**: create a topic and produce/consume a test message (local CLI)

## 8. Non-Functional Requirements (NFR) & Scalability

- **Stability**: services declare resource bounds and healthchecks.
- **Portability**: DNS-only internal addressing.

## 9. Operations & Observability

- **Metrics**: JMX exporter + Kafka exporter (as configured) for Prometheus scraping.
- **Logs**: Loki logging driver via shared templates where supported.

