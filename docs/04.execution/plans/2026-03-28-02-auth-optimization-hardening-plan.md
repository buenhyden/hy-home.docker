---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md -->

# 02-Auth Optimization Hardening Implementation Plan

## Overview

This document is the optimization/hardening implementation plan for `infra/02-auth` (Keycloak, OAuth2 Proxy). It includes configuration improvements, CI validation gates, and documentation traceability synchronization across `01.requirements` through `05.operations`.

## Context

- Baseline catalog: [infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Parent priority plan: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- Application principles:
  - Scope: `Config+Docs`
  - Security posture: `Fail-closed`
  - Hardening level: `Balanced`
  - Validation gate: `Strict CI Gate`

## Goals & In-Scope

- **Goals**:
  - Align OAuth2 Proxy secret injection and runtime permissions with the standard hardening model.
  - Fix Keycloak/OAuth2 Proxy authentication path operations criteria in documents and automated validation.
  - Make Plan/Task/Guide/Operation/Runbook cross-links consistent.
- **In Scope**:
  - `infra/02-auth/keycloak/docker-compose.yml`
  - `infra/02-auth/oauth2-proxy/{docker-compose.dev.yml,docker-compose.yml,Dockerfile,dev.Dockerfile,docker-entrypoint.sh,docker-entrypoint.dev.sh,config/oauth2-proxy.cfg}`
  - `scripts/hardening/check-all-hardening.sh 02-auth`, `.github/workflows/ci-quality.yml`, `scripts/README.md`
  - 02-auth related documents and READMEs under `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Redesigning Keycloak realm or business RBAC structure
  - Bulk-changing settings for other tiers (01, 03 through 11)
- **Out of Scope**:
  - Adding new externally exposed ports
  - Introducing new IdPs or authentication protocols

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-AUTH-001 | Recenter OAuth2 Proxy secret injection on the entrypoint | `infra/02-auth/oauth2-proxy/docker-entrypoint.sh`, `docker-compose.yml` | REQ-PRD-FUN-01 | Secret-file-based export confirmed |
| PLN-AUTH-002 | Harden the OAuth2 Proxy image as non-root | `infra/02-auth/oauth2-proxy/Dockerfile` | REQ-PRD-FUN-02 | `USER oauth2proxy:oauth2proxy` exists |
| PLN-AUTH-003 | Minimize Keycloak secret exposure in logs | `infra/02-auth/keycloak/docker-compose.yml` | REQ-PRD-FUN-01 | Secret length echo removed |
| PLN-AUTH-004 | Add 02-auth hardening validation script coverage | `scripts/hardening/check-all-hardening.sh 02-auth` | REQ-PRD-FUN-03 | Non-zero on failure, zero on pass |
| PLN-AUTH-005 | Add the `infrastructure-hardening` gate to CI | `.github/workflows/ci-quality.yml` | REQ-PRD-FUN-03 | Job runs on PR/push |
| PLN-AUTH-006 | Create and maintain the PRD-to-Runbook document set | 02-auth related files under `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}` | REQ-PRD-FUN-04 | Bidirectional links and README indexes reflected |
| PLN-AUTH-007 | Codify degraded-mode operations and recovery procedures | `docs/05.operations/{policies,runbooks}/02-auth/*.md` | REQ-PRD-FUN-05 | Policy and procedure documents match |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-AUTH-001 | Structural | Static 02-auth hardening validation | `bash scripts/hardening/check-all-hardening.sh 02-auth` | 0 failures |
| VAL-AUTH-002 | Compliance | Template/security baseline validation | `bash scripts/validation/check-template-security-baseline.sh` | 0 failures |
| VAL-AUTH-003 | Traceability | Execution/operations traceability validation | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |
| VAL-AUTH-004 | Root Compose | Root auth profile resolution validation | `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh` | 0 failures |
| VAL-AUTH-005 | Dependency Compose | Root core profile resolution validation | `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` | 0 failures |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Domain environment-variable mismatch breaks OIDC redirects | High | Add a domain/Redirect synchronization checklist to the operations guide |
| Runtime permission issues after non-root conversion | Medium | Explicitly set entrypoint and binary ownership |
| Authentication outage broadens service access impact | Medium | Keep fail-closed behavior and document degraded-mode procedures narrowly |
| Document links regress | Medium | Synchronize README indexes and cross-references in the same commit |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Pass `check-all-hardening.sh 02-auth`, `check-template-security-baseline`, and `check-doc-traceability`.
- **Sandbox / Canary Rollout**: Apply OAuth2 Proxy changes before Keycloak changes.
- **Human Approval Gate**: Merge after Infra/Ops reviewer approval.
- **Rollback Trigger**: Sustained authentication loops, sustained `/ping` failure, or increased OIDC callback failures.
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] 02-auth configuration hardening reflected
- [x] CI gate and script added
- [x] PRD-to-Runbook document set synchronized
- [x] README indexes refreshed
- [x] Verification commands passed

## Related Documents

- **PRD**: [../01.requirements/2026-03-28-02-auth-optimization-hardening.md](../../01.requirements/2026-03-28-02-auth-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0014-auth-optimization-hardening-architecture.md](../../02.architecture/requirements/0014-auth-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md](../../02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md)
- **Spec**: [../03.specs/02-auth/spec.md](../../03.specs/02-auth/spec.md)
- **Tasks**: [../04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md](../tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- **Operations**: [../../05.operations/guides/02-auth/README.md](../../05.operations/guides/02-auth/README.md)
- **Runbooks**: [../../05.operations/runbooks/02-auth/README.md](../../05.operations/runbooks/02-auth/README.md)
