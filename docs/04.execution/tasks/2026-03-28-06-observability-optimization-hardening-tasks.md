---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-06-observability-optimization-hardening-tasks.md -->

# Task: 06-Observability Optimization Hardening

## Overview

This document tracks the `06-observability` optimization and hardening implementation tasks. It manages gateway boundary strengthening, health-based dependency improvements, container hardening, CI baseline automation, and documentation traceability synchronization as task units.

## Inputs

- **Parent Spec**: [../../03.specs/06-observability/spec.md](../../03.specs/06-observability/spec.md)
- **Parent Plan**: [../plans/2026-03-28-06-observability-optimization-hardening-plan.md](../plans/2026-03-28-06-observability-optimization-hardening-plan.md)

## Working Rules

- Observability compose changes leave static validation plus hardening script evidence.
- Routing/authentication policy changes record the gateway/auth impact boundary.
- Documentation changes update PRD-to-Runbook cross-links and README indexes together.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-OBS-001 | Align the public router middleware contract | impl | 06-observability/spec.md / Contracts | PLN-OBS-001 | Confirm label strings | DevOps | Done |
| T-OBS-002 | Align Loki/Tempo/Pyroscope/cAdvisor Traefik routing boundaries | impl | 06-observability/spec.md / Core Design | PLN-OBS-002 | Confirm router/service labels | DevOps | Done |
| T-OBS-003 | Strengthen the Alloy/Grafana depends_on health contract | impl | 06-observability/spec.md / Core Design | PLN-OBS-003 | compose config passes | DevOps | Done |
| T-OBS-004 | Add cAdvisor healthcheck | impl | 06-observability/spec.md / Verification | PLN-OBS-003 | Confirm healthcheck definition | DevOps | Done |
| T-OBS-005 | Improve non-root and secret-guard handling for Loki/Tempo custom images | impl | 06-observability/spec.md / Contracts | PLN-OBS-004 | Confirm Dockerfile/entrypoint | DevOps | Done |
| T-OBS-006 | Add the observability hardening validation script | ops | 06-observability/spec.md / Governance | PLN-OBS-005 | `bash scripts/hardening/check-all-hardening.sh 06-observability` | DevOps | Done |
| T-OBS-007 | Add the CI `infrastructure-hardening` job | ops | 06-observability/spec.md / Governance | PLN-OBS-006 | Confirm workflow definition | DevOps | Done |
| T-OBS-008 | Refresh the scripts README index | doc | 06-observability/spec.md / Related Docs | PLN-OBS-006 | Reflect README entries/examples | Docs | Done |
| T-OBS-009 | Reflect PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook docs | doc | 06-observability/spec.md / Related Docs | PLN-OBS-007 | Confirm document links/README sync | Docs | Done |
| T-OBS-010 | Run static validation and record results | test | 06-observability/spec.md / Verification | PLN-OBS-001~007 | Check compose + hardening + traceability | DevOps | Done |
| T-OBS-011 | Collect runtime/recovery rehearsal evidence | test | 06-observability/spec.md / Verification | PLN-OBS-001~007 | Live health/recovery logs require an approved runtime rehearsal | DevOps | Deferred |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-OBS-001
- [x] T-OBS-002
- [x] T-OBS-003
- [x] T-OBS-004
- [x] T-OBS-005
- [x] T-OBS-006
- [x] T-OBS-007

### Phase 2

- [x] T-OBS-008
- [x] T-OBS-009
- [x] T-OBS-010
- [x] T-OBS-011 (Deferred runtime evidence recorded)

## Verification Summary

- **Test Commands**:
  - `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh`
  - service-local `docker compose -f infra/06-observability/docker-compose.yml config` only with root network/secret overlay
  - `bash scripts/hardening/check-all-hardening.sh 06-observability`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: Local validation logs + CI `infrastructure-hardening` job
- **Deferred Runtime Evidence**: T-OBS-011 remains a live rehearsal item, not an unimplemented static hardening task.

## Related Documents

- **PRD**: [../01.requirements/2026-03-28-06-observability-optimization-hardening.md](../../01.requirements/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0021-observability-optimization-hardening-architecture.md](../../02.architecture/requirements/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../plans/2026-03-28-06-observability-optimization-hardening-plan.md](../plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Guide**: [../../05.operations/guides/06-observability/optimization-hardening.md](../../05.operations/guides/06-observability/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/06-observability/optimization-hardening.md](../../05.operations/policies/06-observability/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/06-observability/optimization-hardening.md](../../05.operations/runbooks/06-observability/optimization-hardening.md)
