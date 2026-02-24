---
title: 'Infrastructure Resource Budgets Implementation Spec'
status: 'Draft'
version: '1.0'
owner: 'Platform/DevOps'
prd_reference: 'N/A'
api_reference: 'N/A'
arch_reference: '../../ARCHITECTURE.md'
tags: ['spec', 'implementation', 'infra', 'performance']
---

# Implementation Specification (Spec)

> **Status**: Draft
> **Related PRD**: N/A
> **Related API Spec**: N/A
> **Related Architecture**: `../../ARCHITECTURE.md`

_Target Directory: `specs/infra-resource-budgets/spec.md`_

---

## 0. Pre-Implementation Checklist (Governance)

> **Mandatory**: Coder agents MUST verify these checklists before generating code.

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Infra modular services | Section 1 |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | infra/* compose services | Section 1 |
| Domain Model       | Are core domain entities and relationships defined?   | Must     | N/A | Section 3 |
| Backend Stack      | Are language/framework/libs (web, ORM, auth) decided? | Must     | N/A | Section 1 |
| Frontend Stack     | Are framework/state/build tools decided?              | Must     | N/A | Section 1 |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | Config validation | Section 7 |
| Test Tooling    | Agreed framework/runner and mock strategy?     | Must     | Compose config checks | Section 7 |
| Coverage Policy | Are goals defined as numbers (e.g., 100%)?      | Must     | N/A | Section 7 |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | N/A | Section 4 |
| Data Protection | Encryption/access policies for sensitive data? | Must     | N/A | Section 9 |
| Performance     | Are Core Web Vitals/Latency metrics targeted?  | Must     | N/A | Section 8 |
| Accessibility   | Is WCAG compliance integrated (contrast/ARIA)? | Must     | N/A | Section 8 |

### 0.3 Operations / Deployment / Monitoring

| Item         | Check Question                                           | Required | Alignment Notes | Where to document |
| ------------ | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments | Are tiers (dev/staging/prod) clarified for this feature? | Must     | `OPERATIONS.md` | OPERATIONS.md |
| Logging      | Required structured logs defined (fields, IDs)?          | Must     | N/A | Section 9 |
| Monitoring   | Metrics and dashboards defined (RED/USE)?                | Must     | N/A | Section 9 |
| Alerts       | Are alert thresholds and routing defined?                | Must     | N/A | Section 9 |
| Backups      | Are backup policies defined for added data?              | Must     | N/A | Section 9 |

---

## 1. Technical Overview & Architecture Style

This spec defines standardized CPU/memory budgets for infra services to prevent OOM and CPU starvation. It applies to compose `deploy.resources.limits` and reservations where supported.

- **Component Boundary**: infra compose services that declare resource limits.
- **Key Dependencies**: Docker Compose resource settings.
- **Tech Stack**: Docker Compose YAML.

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **REQ-SPC-001** | Define Tier 1 critical budgets | High | N/A |
| **REQ-SPC-002** | Define Tier 2 state handler budgets | High | N/A |
| **REQ-SPC-003** | Define Tier 3 observability budgets | Medium | N/A |
| **REQ-SPC-004** | Changes >25% require ADR | High | N/A |

## 3. Data Modeling & Storage Strategy

No data model changes.

## 4. Interfaces & Data Structures

N/A

## 5. Component Breakdown

Resource budgets apply to infra components as documented in tiers below.

### Tier 1: Critical Core

| Component             | Default CPU Limits | RAM Limit | RAM Reservation | Justification              |
| :-------------------- | :----------------- | :-------- | :-------------- | :------------------------- |
| PostgreSQL (pg-0/1/2) | 1.0 CPU            | 2G        | 1G              | Memory intensive indexing  |
| Traefik               | 1.0 CPU            | 1G        | 512M            | High I/O routing load      |
| Keycloak              | 1.5 CPU            | 1.5G      | 1G              | Java JVM heap requirements |
| MinIO                 | 1.0 CPU            | 1G        | 512M            | Foundation for logs/traces |

### Tier 2: State Handlers & Control Planes

| Component           | Default CPU Limits | RAM Limit | RAM Reservation | Justification                  |
| :------------------ | :----------------- | :-------- | :-------------- | :----------------------------- |
| Etcd (3x nodes)     | 0.5 CPU            | 256M      | 128M            | Patroni split-brain prevention |
| HAProxy (Pg-router) | 0.5 CPU            | 256M      | 128M            | Fast forwarding of PG traffic  |
| OAuth2-Proxy        | 0.5 CPU            | 256M      | 128M            | Middleware gatekeeper          |

### Tier 3: Observability (Best Effort)

| Component  | Default CPU Limits | RAM Limit | RAM Reservation | Justification            |
| :--------- | :----------------- | :-------- | :-------------- | :----------------------- |
| Prometheus | 2.0 CPU            | 2G        | 1G              | High cardinality metrics |
| Loki       | 1.0 CPU            | 1G        | 512M            | Ingestion burst          |
| Tempo      | 1.0 CPU            | 1G        | 512M            | Span buffering           |
| Grafana    | 0.5 CPU            | 512M      | 256M            | Visualization            |
| Alloy      | 0.5 CPU            | 512M      | 256M            | Log shipping buffering   |

## 6. Edge Cases & Error Handling

- **Resource spikes**: Escalate via ADR if sustained >25% adjustment required.

## 7. Verification Plan (Testing & QA)

- **[VAL-SPC-001]** Compose files include `deploy.resources` where applicable.
- **[VAL-SPC-002]** Any changes >25% include ADR link.

## 8. Non-Functional Requirements (NFR) & Scalability

- **Performance / Latency**: Ensure core services have reserved headroom.

## 9. Operations & Observability

- **Deployment Strategy**: No change.
- **Monitoring & Alerts**: Track OOM and throttling events.
- **Logging**: N/A.
- **Data Protection**: N/A.
- **Sensitive Data Handling**: N/A.
