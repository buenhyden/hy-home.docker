---
status: active
---
<!-- Target: docs/03.specs/07-workflow/spec.md -->

# 07-Workflow Optimization Hardening Technical Specification

## Overview

This document is the optimization/hardening technical specification for the `infra/07-workflow` tier (Airflow, n8n). It defines gateway boundary security, health-based startup stability, n8n container hardening, CI policy gates, and catalog-based expansion requirements as implementation contracts.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Airflow/n8n Traefik middleware contract
  - Airflow/n8n dependency/healthcheck contract
  - n8n custom image runtime hardening contract
  - `check-all-hardening.sh 07-workflow` policy gate contract
- **Does Not Own**:
  - Individual Airflow DAG business logic
  - Internal n8n workflow business logic
  - Production deployment of new workflow services

## Related Inputs

- **PRD**: [../../01.requirements/019-workflow-optimization-hardening.md](../../01.requirements/019-workflow-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md](../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md](../../02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md)
  - [../../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - Airflow UI/Flower routers use `gateway-standard-chain@file,sso-errors@file,sso-auth@file`.
  - The n8n UI router uses `gateway-standard-chain@file,sso-errors@file,sso-auth@file`.
  - service-local Airflow core services (`apiserver`, `scheduler`, `dag-processor`, `worker`, `triggerer`, `flower`) have `airflow-valkey` health-based dependencies.
  - root-included dev Airflow compose documents the shared `mng-valkey` broker boundary.
  - n8n `worker` and `task-runner` provide healthchecks, and the service-local `task-runner` has `n8n`/`n8n-valkey` health-based dependencies.
  - root-included dev n8n compose documents the shared `mng-valkey` broker boundary.
- **Data / Interface Contract**:
  - Airflow: CeleryExecutor + Valkey broker + PostgreSQL result backend
  - n8n: Queue mode + external runner + PostgreSQL metadata backend
- **Governance Contract**:
  - Passing `scripts/hardening/check-all-hardening.sh 07-workflow` is the workflow tier hardening baseline.
  - The CI `infrastructure-hardening` job blocks regressions at PR time.

## Core Design

- **Gateway Security Plane**:
  - Externally exposed management paths enforce the standard chain and SSO chain after TLS termination.
- **Orchestration Runtime Plane**:
  - Airflow orders dependencies in service-local compose with Valkey health as a prerequisite.
  - n8n separates main/worker/task-runner and operates in queue mode.
- **Image Hardening Plane**:
  - n8n keeps non-root execution through a multi-stage Dockerfile and `USER node`.
  - The n8n entrypoint fails closed immediately when required secret files are missing.

## Data Modeling & Storage Strategy

- Airflow DAG/log/config/plugins use `${DEFAULT_WORKFLOW_DIR}/airflow/*` bind volumes.
- n8n state/custom/task-runner data uses `${DEFAULT_WORKFLOW_DIR}/n8n*` bind volumes.
- Workflow metadata uses management PostgreSQL (`infra/04-data`).

## Interfaces & Data Structures

### Workflow Hardening Control Surface

```yaml
workflow_hardening_controls:
  ingress_security:
    airflow: gateway-standard-chain + sso-errors + sso-auth
    flower: gateway-standard-chain + sso-errors + sso-auth
    n8n: gateway-standard-chain + sso-errors + sso-auth
  startup_health_contract:
    airflow_depends_on: service_healthy
    n8n_worker_healthcheck: required
    n8n_task_runner_healthcheck: required
  container_hardening:
    n8n_runtime_user: node
    n8n_entrypoint_secret_guard: required
```

## Edge Cases & Error Handling

- If automation paths fail after SSO chain hardening, apply the operations-approved exception procedure.
- If Airflow Valkey health does not pass, orchestrator startup fails fast.
- If required n8n secrets are missing, the entrypoint exits immediately and exposes the failure explicitly.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: UI access failure due to middleware misconfiguration
  - **Fallback**: roll back to the most recent working compose version
  - **Human Escalation**: Gateway/Auth operations approver
- **Failure Mode**: worker/task-runner startup failure
  - **Fallback**: reapply the healthcheck/depends_on contract, then restart
  - **Human Escalation**: Workflow on-call

## Verification

```bash
HYHOME_COMPOSE_PROFILES=workflow bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 07-workflow
bash scripts/validation/check-template-security-baseline.sh
bash scripts/validation/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-WRK-001**: Airflow/n8n compose static validation passes.
- **VAL-WRK-002**: workflow hardening baseline script has zero failures.
- **VAL-WRK-003**: PRD~Runbook optimization-hardening document links remain consistent.
- **VAL-WRK-004**: catalog `07-workflow` expansion items (Airflow DAG quality gate, n8n backup/Vault) are reflected in documents/tasks.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Agent Design**: [./agent-design.md](./agent-design.md)
- **Plan**: [../../04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **Cross-Validation Plan**: [../../04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md](../../04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/07-workflow/optimization-hardening.md](../../05.operations/guides/07-workflow/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/07-workflow/optimization-hardening.md](../../05.operations/policies/07-workflow/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/07-workflow/optimization-hardening.md](../../05.operations/runbooks/07-workflow/optimization-hardening.md)
- **Catalog**: [../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
