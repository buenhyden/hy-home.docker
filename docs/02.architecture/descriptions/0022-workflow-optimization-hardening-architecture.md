---
title: "07-Workflow Optimization Hardening Architecture Description"
version: "1.1.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0022"
parent_ids:
- "REQ-0008"
created: "2026-03-28"
---
# 07-Workflow Optimization Hardening Architecture Description

## Overview

### Overview

## Scope

### Scope

### Context and Stakeholders

This document defines the optimization/hardening reference architecture of
the `07-workflow` layer. It organizes the gateway boundary security,
health-based dependency, n8n image hardening, and catalog-based expansion
roadmap from an architecture perspective.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded
in this section and the following views. Only concerns confirmed in the
existing document are covered here.

The workflow tier operates with two execution planes.

- Airflow (code-first orchestration)
- n8n (low-code automation)

The management plane of both systems shares standard middleware+SSO behind
the Traefik TLS boundary.

### System Boundaries

This section preserves the system boundary, consumption relationships,
non-goals, and constraints already recorded in the current document.

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

### Traceability

The disposition of the parent requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Architecture

### Architecture

### Components

### Viewpoints and Views

The context, component, or deployment representation in this section serves
as the view for that concern.

- **Ingress path**:
  - Client -> Traefik(websecure) -> workflow routers -> Airflow/n8n UI
- **Control plane**:
  - Airflow API/Scheduler/Worker/Triggerer + Flower
  - n8n main/worker/task-runner
- **Data/control dependencies**:
  - PostgreSQL (metadata), Valkey (queue/broker), SSO middleware

### Data Flow

### Data and Control Flows

The data and control flows include only the interactions specified in this
section and the existing infrastructure/deployment descriptions.

- **Key Entities / Flows**:
  - DAG metadata, workflow executions, queue tasks
- **Storage Strategy**:
  - Airflow/n8n state via bind volumes + PostgreSQL metadata
- **Data Boundaries**:
  - the workflow tier owns orchestration metadata, and each domain owns its
    business payload schema.

### Deployment View

- **Runtime / Platform**: Docker Compose (`infra/07-workflow/*`)
- **Deployment Model**:
  - Airflow distributed components; the `dedicated-valkey` profile starts `airflow-valkey`, and without it `${AIRFLOW_VALKEY_HOST:-mng-valkey}` resolves to the shared `mng-valkey`
  - n8n queue mode + external runner; the `dedicated-valkey` profile starts `n8n-valkey`, and without it `${N8N_VALKEY_HOST:-mng-valkey}` resolves to the shared `mng-valkey`
- **Operational Evidence**:
  - `docker compose config` checks
  - `scripts/hardening/check-all-hardening.sh 07-workflow`
  - CI `infrastructure-hardening` job

### Evolution

- **Airflow**:
  - DAG quality gate (parse/schedule/delay) CI
  - defining worker autoscale criteria and standardizing operation
- **n8n**:
  - standardizing workflow versioning/Git backup
  - strengthening credential store OpenBao integration
A new workflow service without a tracked infra artifact is excluded from the
active workflow architecture scope.

## Quality Attributes

### Quality Scenarios

The quality scenarios point to the existing configuration, failure boundary,
and verification expectation to which the attributes below apply. Concrete
execution evidence is owned by the related Spec and Operations documents.

- **Performance**: reduces initial failure/restart bursts through
  health-based boot order.
- **Security**: enforces the gateway-standard-chain + SSO chain, and n8n
  non-root + secret guard.
- **Reliability**: strengthens stability with worker/task-runner healthcheck
  and dependency gating.
- **Scalability**: prepares Airflow worker autoscale criteria and a queue
  metrics-based expansion policy.
- **Observability**: verifies workflow stack health at the compose/CI level.
- **Operability**: uses `check-all-hardening.sh 07-workflow` as the
  operational baseline.

## Related Documents

- **PRD**: [../01.requirements/0008-workflow.md](../../01.requirements/0008-workflow.md)
- **Spec**: [../03.specs/008-workflow/spec.md](0007-workflow-architecture.md)
- **ADR**: [../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md](../decisions/0022-workflow-hardening-and-ha-expansion-strategy.md)
- **Guide**: [../../05.operations/guides/07-workflow/optimization-hardening.md](../../05.operations/guides/0054-workflow-optimization-hardening.md)
- **Operation**: [../../05.operations/policies/07-workflow/optimization-hardening.md](../../05.operations/policies/0054-workflow-optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/07-workflow/optimization-hardening.md](../../05.operations/runbooks/0054-workflow-optimization-hardening.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
