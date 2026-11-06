---
title: "07-Workflow Optimization Hardening Architecture Description"
version: "1.2.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "AD-0022"
parent_ids:
- "REQ-0008"
created: "2026-03-28"
---
# 07-Workflow Optimization Hardening Architecture Description

## Overview

### Context and Stakeholders

This document defines the optimization/hardening reference architecture of
the `07-workflow` layer. It organizes the gateway boundary security,
health-based dependency, n8n image hardening, and catalog-based expansion
roadmap from an architecture perspective.

## Scope

The workflow tier operates with two execution planes.

- Airflow (code-first orchestration)
- n8n (low-code automation)

The management plane of both systems shares standard middleware+SSO behind
the Traefik TLS boundary.

### System Boundaries

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

## Structure

### Architecture

- **Ingress path**:
  - Client -> Traefik(websecure) -> workflow routers -> Airflow/n8n UI
- **Control plane**:
  - Airflow API server, scheduler, DAG processor, worker, triggerer and Flower
  - n8n main, worker, task runners, plus the `blog-ingestion` service under its own profile
- **Data/control dependencies**:
  - PostgreSQL (metadata), Valkey (queue/broker), SSO middleware

## Runtime and Deployment

### Runtime View

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
- **Verification**: the registered `infrastructure-hardening` gate in
  `.github/workflow-contract.yml` and Compose validation

### Evolution

- **Airflow**:
  - DAG quality gate (parse/schedule/delay) CI
  - defining worker autoscale criteria and standardizing operation
- **n8n**:
  - standardizing workflow versioning/Git backup
  - strengthening credential store OpenBao integration
A new workflow service without a tracked infra artifact is excluded from the
active workflow architecture scope.

## Quality and Risks

### Quality Attributes

- **Performance**: reduces initial failure/restart bursts through
  health-based boot order.
- **Security**: enforces the gateway-standard-chain + SSO chain, and n8n
  non-root + secret guard.
- **Reliability**: strengthens stability with worker/task-runner healthcheck
  and dependency gating.
- **Scalability**: prepares Airflow worker autoscale criteria and a queue
  metrics-based expansion policy.
- **Observability**: verifies workflow stack health at the compose/CI level.
- **Operability**: uses the registered hardening gate as the baseline.

## Related Documents

- **Requirement**: [REQ-0008 Workflow](../../01.requirements/0008-workflow.md)
- **Tier Architecture Description**: [AD-0007 Workflow Tier (07-workflow) Architecture Description](0007-workflow-architecture.md)
- **ADR**: [ADR-0059 Native OIDC for Open WebUI and the Airflow UI](../decisions/0059-native-oidc-open-webui-and-airflow.md)
- **Guide**: [Workflow optimization hardening guide](../../05.operations/guides/08-workflows-and-automation/0054-workflow-optimization-hardening.md)
- **Policy**: [Workflow optimization hardening policy](../../05.operations/policies/08-workflows-and-automation/0054-workflow-optimization-hardening.md)
- **Runbook**: [Workflow optimization hardening runbook](../../05.operations/runbooks/08-workflows-and-automation/0054-workflow-optimization-hardening.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
