---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md -->

# 07-Workflow Optimization Hardening Implementation Plan

## Overview

This document is the optimization/hardening implementation plan for `infra/07-workflow`. It stages gateway boundary security alignment, health-based startup stabilization, n8n custom image hardening, CI policy gates, and catalog expansion roadmap work.

## Context

- Baseline catalog: [../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Parent priority plan: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- Target configuration: `infra/07-workflow/**/*`, `scripts/`, `.github/workflows/`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}`

## Goals & In-Scope

- **Goals**:
  - Align Airflow/n8n paths with gateway standard and SSO policy.
  - Stabilize orchestrator/runtime startup based on health.
  - Reflect the n8n custom image non-root/secret guard contract as Compose defaults.
  - Introduce workflow tier hardening verification commands and CI gates.
  - Make catalog expansion items executable through documents and tasks.
- **In Scope**:
  - `infra/07-workflow/airflow/docker-compose.yml`
  - `infra/07-workflow/n8n/{docker-compose.yml,Dockerfile,docker-entrypoint.sh}`
  - `scripts/hardening/check-all-hardening.sh 07-workflow`
  - `scripts/README.md`
  - `.github/workflows/ci-quality.yml`
  - `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}` workflow optimization-hardening documents/READMEs

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Immediate deployment of new workflow services
  - Refactoring individual DAG/workflow logic
- **Out of Scope**:
  - Direct infrastructure changes outside the workflow tier
  - Implementing long-term HA topology such as multi-cluster topology

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-WRK-001 | Align Airflow/n8n gateway+SSO middleware | `infra/07-workflow/*/docker-compose.yml` | REQ-PRD-WRK-FUN-01 | Compose labels confirmed |
| PLN-WRK-002 | Strengthen Airflow health-gated dependency | `infra/07-workflow/airflow/docker-compose.yml` | REQ-PRD-WRK-FUN-02 | `service_healthy` contract confirmed |
| PLN-WRK-003 | Strengthen n8n worker/task-runner health/dependency | `infra/07-workflow/n8n/docker-compose.yml` | REQ-PRD-WRK-FUN-03 | healthcheck/depends_on confirmed |
| PLN-WRK-004 | Reflect n8n custom image and entrypoint hardening | `infra/07-workflow/n8n/{Dockerfile,docker-entrypoint.sh,docker-compose.yml}` | REQ-PRD-WRK-FUN-04 | non-root/secret guard confirmed |
| PLN-WRK-005 | Align workflow hardening command and CI gate | `scripts/hardening/check-all-hardening.sh`, `.github/workflows/ci-quality.yml`, `scripts/README.md` | REQ-PRD-WRK-FUN-05 | Script/CI job confirmed |
| PLN-WRK-006 | Create PRD-to-Runbook document system and cross-links | `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**` | REQ-PRD-WRK-FUN-06 | Link consistency confirmed |
| PLN-WRK-007 | Break down catalog expansion items for Airflow/n8n | Plan/Task/Ops/Guide docs | REQ-PRD-WRK-FUN-07 | Task/policy reflection confirmed |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-WRK-001 | Structural | Static workflow root compose validation | `HYHOME_COMPOSE_PROFILES=workflow bash scripts/validation/validate-docker-compose.sh` | No errors |
| VAL-WRK-002 | Structural | Static workflow root dev compose validation | `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh` | No errors |
| VAL-WRK-003 | Compliance | Verify workflow hardening baseline | `bash scripts/hardening/check-all-hardening.sh 07-workflow` | 0 failures |
| VAL-WRK-004 | Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | 0 failures |
| VAL-WRK-005 | Traceability | Verify document traceability | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| SSO hardening affects existing operations access paths | Medium | Reflect exceptions and recovery procedures in the runbook |
| Custom image build failure delays deployment | Medium | Keep image pinning and run Compose static validation first |
| Healthcheck false positives create restart loops | Medium | Start with the minimum process-based contract and tune based on operations metrics |
| Unimplemented workflow service docs remain in the active chain | Medium | Remove unimplemented service active docs and task rows, and track them only in the archive tombstone ledger |

## Completion Criteria

- [x] Workflow compose/image/script/CI hardening reflected
- [x] Workflow optimization-hardening document set created
- [x] Stage 01-05 README indexes reflected
- [ ] Runtime startup/rehearsal evidence secured when the environment allows

## Related Documents

- **PRD**: [../01.requirements/2026-03-28-07-workflow-optimization-hardening.md](../../01.requirements/2026-03-28-07-workflow-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md](../../02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../03.specs/07-workflow/spec.md](../../03.specs/07-workflow/spec.md)
- **Tasks**: [../04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/07-workflow/optimization-hardening.md](../../05.operations/guides/07-workflow/optimization-hardening.md)
- **Operations**: [../../05.operations/policies/07-workflow/optimization-hardening.md](../../05.operations/policies/07-workflow/optimization-hardening.md)
- **Runbooks**: [../../05.operations/runbooks/07-workflow/optimization-hardening.md](../../05.operations/runbooks/07-workflow/optimization-hardening.md)
