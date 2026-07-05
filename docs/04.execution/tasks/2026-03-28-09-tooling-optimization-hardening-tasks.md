---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md -->

# Task: 09-Tooling Optimization Hardening

## Overview

This document tracks the `09-tooling` optimization and hardening execution tasks. It manages compose hardening, CI policy gates, documentation traceability, and catalog expansion items as task units.

## Inputs

- **Parent Spec**: [../../03.specs/09-tooling/spec.md](../../03.specs/09-tooling/spec.md)
- **Parent Plan**: [../plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../plans/2026-03-28-09-tooling-optimization-hardening-plan.md)

## Working Rules

- Tooling configuration changes leave hardening script results and the optional root-context compose boundary.
- Changes that affect gateway/auth record the access-boundary impact.
- Documentation changes update PRD-to-Runbook links and README indexes together.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-TLG-001 | Align SonarQube/Terrakube/Syncthing middleware with the gateway+SSO chain | impl | Contracts / Config | PLN-TLG-001 | Confirm compose labels | DevOps | Done |
| T-TLG-002 | Align the tooling compose `infra_net` external declaration | impl | Contracts / Config | PLN-TLG-002 | Confirm network contract | DevOps | Done |
| T-TLG-003 | Add locust-worker healthcheck | impl | Runtime Stability | PLN-TLG-003 | Confirm compose healthcheck | DevOps | Done |
| T-TLG-004 | Align k6 volume reference drift | impl | Runtime Stability | PLN-TLG-003 | Confirm `k6-data` mount | DevOps | Done |
| T-TLG-005 | Add the tooling hardening script | ops | Governance Contract | PLN-TLG-004 | `bash scripts/hardening/check-all-hardening.sh 09-tooling` | DevOps | Done |
| T-TLG-006 | Add the CI `infrastructure-hardening` job | ops | Governance Contract | PLN-TLG-004 | Confirm workflow job | DevOps | Done |
| T-TLG-007 | Refresh scripts inventory/usage README | doc | Related Docs | PLN-TLG-004 | Reflect README entries | Docs | Done |
| T-TLG-008 | Create PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook docs | doc | Related Docs | PLN-TLG-005 | Synchronize links/indexes | Docs | Done |
| T-TLG-009 | Define terraform approval gate/state backup/drift auto-detection roadmap | doc | Catalog Expansion Targets | PLN-TLG-006 | Reflect operations/tasks updates | Platform Owner | Done |
| T-TLG-010 | Define terrakube workspace separation/permission/audit-log roadmap | doc | Catalog Expansion Targets | PLN-TLG-006 | Reflect operations/tasks updates | Platform Owner | Done |
| T-TLG-011 | Define registry signing/verification/vulnerability blocking roadmap | doc | Catalog Expansion Targets | PLN-TLG-006 | Reflect operations/tasks updates | Security/DevOps | Done |
| T-TLG-012 | Define sonarqube/k6/locust/syncthing expansion policy roadmap | doc | Catalog Expansion Targets | PLN-TLG-006 | Reflect operations/tasks updates | Platform Owner | Done |
| T-TLG-013 | Run static validation and record results | test | Verification | PLN-TLG-001~006 | Check compose/script/baseline/traceability | DevOps | Done |
| T-TLG-014 | Collect runtime rehearsal and operations evidence | test | Verification | PLN-TLG-001~006 | Live health/latency/log evidence requires an approved runtime rehearsal | DevOps | Deferred |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-TLG-001
- [x] T-TLG-002
- [x] T-TLG-003
- [x] T-TLG-004
- [x] T-TLG-005
- [x] T-TLG-006
- [x] T-TLG-007

### Phase 2

- [x] T-TLG-008
- [x] T-TLG-009
- [x] T-TLG-010
- [x] T-TLG-011
- [x] T-TLG-012
- [x] T-TLG-013
- [x] T-TLG-014 (Deferred runtime evidence recorded)

## Verification Summary

- **Test Commands**:
  - `bash scripts/hardening/check-all-hardening.sh 09-tooling`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/validation/check-repo-contracts.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: Local validation logs + CI `infrastructure-hardening` job
- **Deferred Runtime Evidence**: T-TLG-014 remains a live rehearsal item, not an unimplemented static hardening task.

## Related Documents

- **PRD**: [../01.requirements/021-tooling-optimization-hardening.md](../../01.requirements/021-tooling-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0024-tooling-optimization-hardening-architecture.md](../../02.architecture/requirements/0024-tooling-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- **Guide**: [../../05.operations/guides/09-tooling/optimization-hardening.md](../../05.operations/guides/09-tooling/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/09-tooling/optimization-hardening.md](../../05.operations/policies/09-tooling/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/09-tooling/optimization-hardening.md](../../05.operations/runbooks/09-tooling/optimization-hardening.md)
