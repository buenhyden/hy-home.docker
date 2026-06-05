---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md -->

# Task: 05-Messaging Optimization Hardening

## Overview

This document tracks the `05-messaging` optimization and hardening implementation tasks. It manages compose hardening, CI baseline automation, and documentation traceability synchronization as task units.

## Inputs

- **Parent Spec**: [../../03.specs/05-messaging/spec.md](../../03.specs/05-messaging/spec.md)
- **Parent Plan**: [../plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../plans/2026-03-28-05-messaging-optimization-hardening-plan.md)

## Working Rules

- Messaging compose changes leave static validation and hardening script evidence.
- Routing policy changes state the gateway/SSO impact boundary.
- Documentation changes update PRD-to-Runbook cross-links and README indexes together.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-MSG-001 | Pin the Kafka UI image tag | impl | 05-messaging/spec.md / Contracts | PLN-MSG-001 | Confirm `rg 'kafbat/kafka-ui:v1.5.0' infra/05-messaging/kafka` | DevOps | Done |
| T-MSG-002 | Apply the gateway chain to the Kafka management router | impl | 05-messaging/spec.md / Core Design | PLN-MSG-001 | Confirm label strings | DevOps | Done |
| T-MSG-003 | Improve Kafka dev compose volume path consistency | impl | 05-messaging/spec.md / Contracts | PLN-MSG-002 | dev compose config passes | DevOps | Done |
| T-MSG-004 | Apply chain+SSO to the Kafka dev router | impl | 05-messaging/spec.md / Core Design | PLN-MSG-002 | Confirm label strings | DevOps | Done |
| T-MSG-005 | Apply chain+SSO to the RabbitMQ management router | impl | 05-messaging/spec.md / Contracts | PLN-MSG-003 | Confirm label strings | DevOps | Done |
| T-MSG-006 | Add the messaging hardening validation script | ops | 05-messaging/spec.md / Governance | PLN-MSG-004 | `bash scripts/hardening/check-all-hardening.sh 05-messaging` | DevOps | Done |
| T-MSG-007 | Add the CI `infrastructure-hardening` job | ops | 05-messaging/spec.md / Governance | PLN-MSG-005 | Confirm workflow definition | DevOps | Done |
| T-MSG-008 | Refresh the scripts README index | doc | 05-messaging/spec.md / Related Docs | PLN-MSG-006 | Confirm README entries/examples | Docs | Done |
| T-MSG-009 | Reflect PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook docs | doc | 05-messaging/spec.md / Related Docs | PLN-MSG-007 | Confirm document links/README sync | Docs | Done |
| T-MSG-010 | Run static validation and record results | test | 05-messaging/spec.md / Verification | PLN-MSG-001~007 | Check compose + hardening + traceability | DevOps | Done |
| T-MSG-011 | Collect runtime/disaster-recovery rehearsal evidence | test | 05-messaging/spec.md / Verification | PLN-MSG-001~007 | Live health/recovery logs require an approved runtime rehearsal | DevOps | Deferred |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-MSG-001
- [x] T-MSG-002
- [x] T-MSG-003
- [x] T-MSG-004
- [x] T-MSG-005
- [x] T-MSG-006
- [x] T-MSG-007

### Phase 2

- [x] T-MSG-008
- [x] T-MSG-009
- [x] T-MSG-010
- [x] T-MSG-011 (Deferred runtime evidence recorded)

## Verification Summary

- **Test Commands**:
  - `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh`
  - `HYHOME_COMPOSE_PROFILES='messaging dev' bash scripts/validation/validate-docker-compose.sh`
  - service-local compose checks require root `infra_net`/secret context or a temporary validation overlay
  - `bash scripts/hardening/check-all-hardening.sh 05-messaging`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: Local validation logs + CI `infrastructure-hardening` job
- **Deferred Runtime Evidence**: T-MSG-011 remains a live rehearsal item, not an unimplemented static hardening task.

## Related Documents

- **PRD**: [../01.requirements/2026-03-28-05-messaging-optimization-hardening.md](../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md](../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Guide**: [../../05.operations/guides/05-messaging/optimization-hardening.md](../../05.operations/guides/05-messaging/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/05-messaging/optimization-hardening.md](../../05.operations/policies/05-messaging/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/05-messaging/optimization-hardening.md](../../05.operations/runbooks/05-messaging/optimization-hardening.md)
