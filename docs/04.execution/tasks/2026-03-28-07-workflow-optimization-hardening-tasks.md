---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md -->

# Task: 07-Workflow Optimization Hardening

## Overview

This document tracks the `07-workflow` optimization and hardening execution tasks. It manages compose/image hardening, CI gates, documentation traceability, and catalog expansion roadmap work as task units.

## Inputs

- **Parent Spec**: [../../03.specs/008-workflow/spec.md](../../03.specs/008-workflow/spec.md)
- **Parent Plan**: [../plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../plans/2026-03-28-07-workflow-optimization-hardening-plan.md)

## Working Rules

- Workflow configuration changes leave compose static validation plus hardening script results.
- Security-boundary changes record the gateway/auth impact boundary.
- Documentation changes update PRD-to-Runbook links and README indexes together.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-WRK-001 | Align Airflow/n8n middleware with the gateway+SSO chain | impl | Contracts / Config | PLN-WRK-001 | Confirm compose labels | DevOps | Done |
| T-WRK-002 | Strengthen Airflow service dependencies based on Valkey health | impl | Contracts / Config | PLN-WRK-002 | Confirm compose `service_healthy` | DevOps | Done |
| T-WRK-003 | Add n8n worker/task-runner healthchecks and dependency gating | impl | Contracts / Config | PLN-WRK-003 | Confirm healthcheck/depends_on | DevOps | Done |
| T-WRK-004 | Promote n8n custom image compose and apply entrypoint secret guard | impl | Core Design / Image Hardening | PLN-WRK-004 | Confirm Dockerfile/entrypoint | DevOps | Done |
| T-WRK-005 | Align the workflow hardening command | ops | Governance Contract | PLN-WRK-005 | `bash scripts/hardening/check-all-hardening.sh 07-workflow` | DevOps | Done |
| T-WRK-006 | Add the CI `infrastructure-hardening` job | ops | Governance Contract | PLN-WRK-005 | Confirm workflow job | DevOps | Done |
| T-WRK-007 | Refresh scripts inventory/usage README | doc | Related Docs | PLN-WRK-005 | Reflect README entries | Docs | Done |
| T-WRK-008 | Create PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook docs | doc | Related Docs | PLN-WRK-006 | Synchronize links/indexes | Docs | Done |
| T-WRK-009 | Document Airflow DAG quality gate and worker autoscale criteria | doc | Catalog Expansion Targets | PLN-WRK-007 | Reflect ops/guide/task updates | DevOps | Done |
| T-WRK-010 | Document n8n Git backup/Vault credential integration criteria | doc | Catalog Expansion Targets | PLN-WRK-007 | Reflect ops/guide/task updates | DevOps | Done |
| T-WRK-012 | Run static validation and record results | test | Verification | PLN-WRK-001~007 | Check compose/script/baseline/traceability | DevOps | Done |
| T-WRK-013 | Collect runtime startup and recovery rehearsal evidence | test | Verification | PLN-WRK-001~007 | Live health/recovery logs require an approved runtime rehearsal | DevOps | Deferred |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-WRK-001
- [x] T-WRK-002
- [x] T-WRK-003
- [x] T-WRK-004
- [x] T-WRK-005
- [x] T-WRK-006
- [x] T-WRK-007

### Phase 2

- [x] T-WRK-008
- [x] T-WRK-009
- [x] T-WRK-010
- [x] T-WRK-012
- [x] T-WRK-013 (Deferred runtime evidence recorded)

## Verification Summary

- **Test Commands**:
  - `HYHOME_COMPOSE_PROFILES=workflow bash scripts/validation/validate-docker-compose.sh`
  - `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
  - `bash scripts/hardening/check-all-hardening.sh 07-workflow`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: Local validation logs + CI `infrastructure-hardening` job
- **Deferred Runtime Evidence**: T-WRK-013 remains a live rehearsal item, not an unimplemented static hardening task.

## Related Documents

- **PRD**: [../01.requirements/019-workflow-optimization-hardening.md](../../01.requirements/019-workflow-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md](../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **Guide**: [../../05.operations/guides/07-workflow/optimization-hardening.md](../../05.operations/guides/07-workflow/optimization-hardening.md)
- **Operation**: [../../05.operations/policies/07-workflow/optimization-hardening.md](../../05.operations/policies/07-workflow/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/07-workflow/optimization-hardening.md](../../05.operations/runbooks/07-workflow/optimization-hardening.md)
