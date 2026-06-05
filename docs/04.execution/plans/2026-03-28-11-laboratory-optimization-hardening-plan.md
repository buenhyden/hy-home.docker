---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md -->

# 11-Laboratory Optimization Hardening Implementation Plan

## Overview

This document is the optimization/hardening implementation plan for `infra/11-laboratory`. It strengthens ingress security boundaries, removes direct exposure, improves least privilege, introduces CI policy gates, and applies catalog expansion items to operations in stages.

## Context

- Baseline catalog: [../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Parent priority plan: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- Target configuration: `infra/11-laboratory/**/*`, `scripts/`, `.github/workflows/`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}`

## Goals & In-Scope

- **Goals**:
  - Align Laboratory UI routers with gateway+allowlist+SSO boundaries.
  - Remove dashboard direct host exposure.
  - Standardize service network blocks that join the root `infra_net` context.
  - Apply least privilege (read-only) to the dozzle socket.
  - Align the laboratory hardening baseline with `scripts/hardening/check-all-hardening.sh 11-laboratory` and the integrated `infrastructure-hardening` CI gate.
  - Reflect catalog expansion items in policy/task roadmaps.
- **In Scope**:
  - `infra/11-laboratory/*/docker-compose.yml`
  - `.env.example`
  - `scripts/hardening/check-all-hardening.sh 11-laboratory`
  - `.github/workflows/ci-quality.yml`
  - `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}` optimization-hardening documents/READMEs
  - root-active Open Notebook/SurrealDB hardening boundary

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Introducing or replacing Laboratory service groups
  - Redesigning Keycloak/Traefik core policies
- **Out of Scope**:
  - Runtime changes outside the Laboratory tier
  - Tool major version migration

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-LAB-001 | Align router middleware with the gateway+allowlist+SSO chain | `infra/11-laboratory/*/docker-compose.yml` | REQ-PRD-LAB-FUN-01/02 | Compose labels confirmed |
| PLN-LAB-002 | Standardize root `infra_net` service network blocks | `infra/11-laboratory/*/docker-compose.yml` | REQ-PRD-LAB-FUN-04 | Network contract confirmed |
| PLN-LAB-003 | Remove dashboard direct host exposure | `infra/11-laboratory/dashboard/docker-compose.yml` | REQ-PRD-LAB-FUN-03 | `ports:` removed and `expose` confirmed |
| PLN-LAB-004 | Apply least privilege to the dozzle socket | `infra/11-laboratory/dozzle/docker-compose.yml` | REQ-PRD-LAB-FUN-05 | `docker.sock:ro` confirmed |
| PLN-LAB-005 | Add lab hardening script and CI gate | `scripts/hardening/check-all-hardening.sh 11-laboratory`, `.github/workflows/ci-quality.yml`, `scripts/README.md` | REQ-PRD-LAB-FUN-06 | Script/CI job confirmed |
| PLN-LAB-006 | Sync PRD-to-Runbook document set and README indexes | `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**` | REQ-PRD-LAB-FUN-07 | Link consistency confirmed |
| PLN-LAB-007 | Document catalog expansion item roadmap | Plan/Task/Ops/Guide docs | REQ-PRD-LAB-FUN-08 | Policy/task reflection confirmed |
| PLN-LAB-008 | Reflect Open Notebook route/secret/readiness hardening | `infra/11-laboratory/open-notebook/docker-compose.yml` | REQ-PRD-LAB-FUN-09 | SSO/allowlist/secret/healthcheck confirmed |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-LAB-001 | Structural | Static root-active laboratory compose validation | `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh` | No errors |
| VAL-LAB-002 | Compliance | Verify laboratory hardening baseline | `bash scripts/hardening/check-all-hardening.sh 11-laboratory` | 0 failures |
| VAL-LAB-003 | Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | 0 failures |
| VAL-LAB-004 | Traceability | Verify document traceability | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Allowlist policy blocks operator access | Medium | Provide standard operating procedures for the `LAB_ALLOWED_CIDRS` environment value |
| Removing dashboard direct paths causes existing access confusion | Low | Announce new access paths in guides/runbooks |
| Experimental service policy expansion remains incomplete | Medium | Specify phase, approval, and evidence criteria in tasks |

## Completion Criteria

- [x] Compose/script/CI hardening reflected
- [x] Optimization-hardening document set created
- [x] docs `01~05` README indexes reflected
- [ ] Runtime rehearsal/operations evidence secured when the environment allows

## Related Documents

- **PRD**: [../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md](../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md](../../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../03.specs/11-laboratory/spec.md](../../03.specs/11-laboratory/spec.md)
- **Tasks**: [../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/11-laboratory/optimization-hardening.md](../../05.operations/guides/11-laboratory/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/11-laboratory/optimization-hardening.md](../../05.operations/policies/11-laboratory/optimization-hardening.md)
- **Runbooks**: [../../05.operations/runbooks/11-laboratory/optimization-hardening.md](../../05.operations/runbooks/11-laboratory/optimization-hardening.md)
