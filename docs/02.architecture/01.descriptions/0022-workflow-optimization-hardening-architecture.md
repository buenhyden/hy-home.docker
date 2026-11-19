---
title: "07-Workflow Optimization Hardening Architecture Description"
version: "1.3.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0022"
parent_ids:
- "REQ-0008"
created: "2026-03-28"
---

# 07-Workflow Optimization Hardening Architecture Description

## Context and Boundaries

### System Boundary

The workflow tier operates with two execution planes.

- Airflow (code-first orchestration)
- n8n (low-code automation)

Both systems use Traefik TLS and the gateway standard chain. Airflow's UI
uses Keycloak Auth Manager, n8n uses its own login, and the optional Flower
UI uses ForwardAuth.

- **Owns**:
  - Workflow management path security contract
  - Airflow/n8n startup dependency/health contract
  - n8n runtime image hardening standard
  - workflow hardening CI gate
- **Consumes**:
  - `01-gateway` Traefik middleware chain
  - `02-auth` SSO middleware
  - `04-data` management PostgreSQL
- **Does Not Own**:
  - DAG/workflow internal domain logic
  - new workflow service production artifact implementation
- **Non-goals**:
  - immediate multi-region/cluster workflow operation
  - immediate full activation of a new workflow service deployment

#### Purpose and Readers

This document defines the optimization/hardening reference architecture of
the `07-workflow` layer. It organizes the gateway boundary security,
health-based dependency, n8n image hardening, and catalog-based expansion
roadmap from an architecture perspective.

#### Context

The tier consumes the `01-gateway` Traefik middleware chain, `02-auth` SSO middleware and `04-data` management PostgreSQL; clients reach the Airflow and n8n UIs through Traefik.

### Constraints

The gateway-standard-chain is enforced (plus the SSO chain on Flower only; Airflow and n8n use their own login), and n8n runs non-root with a secret guard.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.

## Structure

### Building Blocks

- **Ingress path**:
  - Client -> Traefik(websecure) -> workflow routers -> Airflow/n8n UI
- **Control plane**:
  - Airflow API server, scheduler, DAG processor, worker, triggerer and Flower
  - n8n main, worker, task runners, plus the `blog-ingestion` service under its own profile
- **Data/control dependencies**:
  - PostgreSQL (metadata), Valkey (queue/broker), SSO middleware

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Ingress path (Traefik `websecure` to workflow routers) | Airflow and n8n UIs | Clients | `01-gateway` gateway standard chain; Airflow uses Keycloak Auth Manager, n8n its own login | The description records no failure handling for this interface. |
| Optional Flower UI | Airflow Flower (`airflow-flower` profile) | The description names no consumer for this interface. | `02-auth` SSO middleware via ForwardAuth | The description records no failure handling for this interface. |
| PostgreSQL metadata | `04-data` management PostgreSQL | Airflow and n8n | The description links no contract for this interface. | The description records no failure handling for this interface. |
| Valkey queue/broker | Shared `mng-valkey` via `${AIRFLOW_VALKEY_HOST:-mng-valkey}` and `${N8N_VALKEY_HOST:-mng-valkey}` | Airflow distributed components and n8n queue mode | The description links no contract for this interface. | The description records no failure handling for this interface. |

- Ingress path: Client -> Traefik(websecure) -> workflow routers -> Airflow/n8n UI.
- Data/control dependencies: PostgreSQL (metadata), Valkey (queue/broker), SSO middleware.

## Runtime Behavior

### Normal Flow

#### Runtime View

- **Key Entities / Flows**:
  - DAG metadata, workflow executions, queue tasks
- **Storage Strategy**:
  - Airflow/n8n state via bind volumes + PostgreSQL metadata
- **Data Boundaries**:
  - the workflow tier owns orchestration metadata, and each domain owns its
    business payload schema.

#### Deployment View

- **Runtime / Platform**: Docker Compose (`infra/07-workflow/*`)
- **Deployment Model**:
  - Airflow distributed components; `${AIRFLOW_VALKEY_HOST:-mng-valkey}` resolves to the shared `mng-valkey`
  - Flower is selected separately by `airflow-flower`; `workflow` does not select it
  - n8n queue mode + external runner; `${N8N_VALKEY_HOST:-mng-valkey}` resolves to the shared `mng-valkey`
- **Verification**: the registered `infrastructure-hardening` gate in
  `.github/workflow-contract.yml` and Compose validation

### Failure and Recovery

Health-based boot order reduces initial failure/restart bursts, and worker/task-runner healthcheck and dependency gating strengthen stability. The description records no failure boundary beyond the linked operations documents under Interfaces.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- **Performance**: reduces initial failure/restart bursts through
  health-based boot order.
- **Security**: enforces the gateway-standard-chain (plus the SSO chain on
  Flower only; Airflow and n8n use their own login), and n8n non-root + secret
  guard.
- **Reliability**: strengthens stability with worker/task-runner healthcheck
  and dependency gating.
- **Scalability**: prepares Airflow worker autoscale criteria and a queue
  metrics-based expansion policy.
- **Observability**: verifies workflow stack health at the compose/CI level.
- **Operability**: uses the registered hardening gate as the baseline.

### Trade-offs

- The SSO chain applies to Flower only; Airflow and n8n keep their own login
  behind the gateway standard chain (Constraints, Quality Attributes).
- Scalability is prepared, not implemented: Airflow worker autoscale criteria
  and a queue metrics-based expansion policy remain Evolution items, and
  multi-region or cluster workflow operation is a non-goal (Quality
  Attributes, System Boundary).
- A new workflow service without a tracked infra artifact stays outside the
  active workflow architecture scope, and its immediate full activation is a
  non-goal (Evolution, System Boundary).
- The description records no failure boundary beyond the linked operations
  documents (Failure and Recovery).

## Decisions and Adoption

### Decisions

- **ADR**: [ADR-0059 Native OIDC for Open WebUI and the Airflow UI](../02.decisions/0059-native-oidc-open-webui-and-airflow.md)
- **ADR**: [ADR-0062 optional Flower activation](../02.decisions/0062-home-lab-membership.md)

### Adoption Boundaries

#### Requirement Mapping

- **Requirement**: [REQ-0008 Workflow](../../01.requirements/0008-workflow.md)

#### Currentness and Lineage

- **Tier Architecture Description**: [AD-0007 Workflow Tier (07-workflow) Architecture Description](0007-workflow-architecture.md)
- **Guide**: [Workflow optimization hardening guide](../../05.operations/01.guides/08.workflows-and-automation/0054-workflow-optimization-hardening.md)
- **Policy**: [Workflow optimization hardening policy](../../05.operations/02.policies/08.workflows-and-automation/0054-workflow-optimization-hardening.md)
- **Runbook**: [Workflow optimization hardening runbook](../../05.operations/03.runbooks/08.workflows-and-automation/0054-workflow-optimization-hardening.md)

#### Evolution

- **Airflow**:
  - DAG quality gate (parse/schedule/delay) CI
  - defining worker autoscale criteria and standardizing operation
- **n8n**:
  - standardizing workflow versioning/Git backup
  - strengthening credential store OpenBao integration

A new workflow service without a tracked infra artifact is excluded from the active workflow architecture scope.
