---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md -->

# Task: 11-Laboratory Optimization Hardening

## Overview

This document tracks the `11-laboratory` optimization and hardening execution tasks. It manages ingress boundary strengthening, direct exposure removal, least-privilege improvements, CI policy gates, and catalog expansion roadmap work as task units.

## Inputs

- **Parent Spec**: [../../03.specs/11-laboratory/spec.md](../../03.specs/11-laboratory/spec.md)
- **Parent Plan**: [../plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)

## Working Rules

- Laboratory compose changes leave static validation plus hardening check results.
- Authentication/allowlist relaxation changes require approver review.
- Documentation changes update PRD-to-Runbook links and README indexes together.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-LAB-001 | Align all Laboratory router middleware with the gateway+allowlist+SSO chain | impl | Contracts / Config | PLN-LAB-001 | Confirm compose labels | DevOps | Done |
| T-LAB-002 | Align the root `infra_net` service network block | impl | Network Boundary | PLN-LAB-002 | Confirm network contract | DevOps | Done |
| T-LAB-003 | Remove dashboard direct host `ports` and switch to `expose` | impl | Least Privilege | PLN-LAB-003 | Confirm ports removal | DevOps | Done |
| T-LAB-004 | Apply read-only docker socket access for dozzle | impl | Least Privilege | PLN-LAB-004 | Confirm `docker.sock:ro` | DevOps | Done |
| T-LAB-005 | Add service-mount-based healthcheck | impl | Runtime Stability | PLN-LAB-001~004 | Confirm healthcheck block | DevOps | Done |
| T-LAB-006 | Add the laboratory hardening script | ops | Governance Contract | PLN-LAB-005 | `bash scripts/hardening/check-all-hardening.sh 11-laboratory` | DevOps | Done |
| T-LAB-007 | Add the CI `infrastructure-hardening` job | ops | Governance Contract | PLN-LAB-005 | Confirm workflow job | DevOps | Done |
| T-LAB-008 | Refresh scripts inventory/usage README | doc | Related Docs | PLN-LAB-005 | Reflect README entries | Docs | Done |
| T-LAB-009 | Create PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook docs | doc | Related Docs | PLN-LAB-006 | Synchronize links/indexes | Docs | Done |
| T-LAB-010 | Define the dashboard expiration policy roadmap | doc | Catalog Expansion Targets | PLN-LAB-007 | Reflect operations/tasks updates | Platform Owner | Done |
| T-LAB-011 | Define the dozzle log access restriction roadmap | doc | Catalog Expansion Targets | PLN-LAB-007 | Reflect operations/tasks updates | Platform Owner | Done |
| T-LAB-012 | Define the portainer session/approval policy roadmap | doc | Catalog Expansion Targets | PLN-LAB-007 | Reflect operations/tasks updates | Security/DevOps | Done |
| T-LAB-013 | Define the redisinsight least-privilege/audit policy roadmap | doc | Catalog Expansion Targets | PLN-LAB-007 | Reflect operations/tasks updates | Security/DevOps | Done |
| T-LAB-014 | Run static validation and record results | test | Verification | PLN-LAB-001~007 | Check compose/script/baseline/traceability | DevOps | Done |
| T-LAB-015 | Collect runtime rehearsal and operations evidence | test | Verification | PLN-LAB-001~007 | Live health/access evidence requires an approved runtime rehearsal | DevOps | Deferred |
| T-LAB-016 | Correct Open Notebook route/secret/readiness hardening current truth | impl | Contracts / Config | PLN-LAB-008 | Confirm open-notebook middleware, secret file, healthcheck | DevOps | Done |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-LAB-001
- [x] T-LAB-002
- [x] T-LAB-003
- [x] T-LAB-004
- [x] T-LAB-005
- [x] T-LAB-006
- [x] T-LAB-007
- [x] T-LAB-008

### Phase 2

- [x] T-LAB-009
- [x] T-LAB-010
- [x] T-LAB-011
- [x] T-LAB-012
- [x] T-LAB-013
- [x] T-LAB-014
- [x] T-LAB-015 (Deferred runtime evidence recorded)
- [x] T-LAB-016

## Verification Summary

- **Test Commands**:
  - `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
  - `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: Local validation logs + CI `infrastructure-hardening` job
- **Deferred Runtime Evidence**: T-LAB-015 remains a live rehearsal item, not an unimplemented static hardening task.

## Related Documents

- **PRD**: [../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md](../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md](../../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Guide**: [../../05.operations/guides/11-laboratory/optimization-hardening.md](../../05.operations/guides/11-laboratory/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/11-laboratory/optimization-hardening.md](../../05.operations/policies/11-laboratory/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/11-laboratory/optimization-hardening.md](../../05.operations/runbooks/11-laboratory/optimization-hardening.md)
