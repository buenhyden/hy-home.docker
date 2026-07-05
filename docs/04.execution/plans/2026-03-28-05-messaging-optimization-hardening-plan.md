---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md -->

# 05-Messaging Optimization Hardening Implementation Plan

## Overview

This document is the optimization/hardening implementation plan for `infra/05-messaging`. It stages stronger gateway boundary controls, image tag/path consistency, CI hardening gate introduction, and document hierarchy synchronization.

## Context

- Baseline catalog: [infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Parent priority plan: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- Target configuration: `kafka`, `rabbitmq` compose plus related docs/CI/scripts

## Goals & In-Scope

- **Goals**:
  - Align messaging management paths with the gateway standard chain and SSO policy.
  - Remove floating-tag and path-consistency risks.
  - Add a messaging-specific hardening gate to CI.
  - Synchronize PRD-to-Runbook documents against the optimization-hardening baseline.
- **In Scope**:
  - `infra/05-messaging/kafka/docker-compose.yml`
  - `infra/05-messaging/kafka/docker-compose.dev.yml`
  - `infra/05-messaging/rabbitmq/docker-compose.yml`
  - `scripts/hardening/check-all-hardening.sh 05-messaging`
  - `.github/workflows/ci-quality.yml`
  - Messaging optimization-hardening documents and READMEs under `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Building a new Kafka/RabbitMQ topology
  - Implementing application reprocessing code
- **Out of Scope**:
  - Changing non-messaging tier configuration
  - Introducing cloud-managed messaging

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-MSG-001 | Pin Kafka UI image tag and apply gateway chain | `infra/05-messaging/kafka/docker-compose.yml` | REQ-PRD-MSG-FUN-01,03 | Compose config and grep checks |
| PLN-MSG-002 | Align Kafka dev compose paths and apply chain | `infra/05-messaging/kafka/docker-compose.dev.yml` | REQ-PRD-MSG-FUN-01,04 | Compose config passes |
| PLN-MSG-003 | Strengthen RabbitMQ management-path middleware chain | `infra/05-messaging/rabbitmq/docker-compose.yml` | REQ-PRD-MSG-FUN-01,02 | Router labels confirmed |
| PLN-MSG-004 | Write messaging hardening baseline script coverage | `scripts/hardening/check-all-hardening.sh 05-messaging` | REQ-PRD-MSG-FUN-05 | Script pass/fail behavior |
| PLN-MSG-005 | Add CI `infrastructure-hardening` job | `.github/workflows/ci-quality.yml` | REQ-PRD-MSG-FUN-05 | Workflow definition confirmed |
| PLN-MSG-006 | Refresh scripts index | `scripts/README.md` | REQ-PRD-MSG-FUN-05 | README entry and example reflected |
| PLN-MSG-007 | Create/update PRD-to-Runbook optimization document set | `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**` | REQ-PRD-MSG-FUN-06 | Cross-links and README entries reflected |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-MSG-001 | Structural | Static root-included messaging compose validation | `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh` | No errors |
| VAL-MSG-002 | Structural | Static root-included messaging+dev compose validation | `HYHOME_COMPOSE_PROFILES='messaging dev' bash scripts/validation/validate-docker-compose.sh` | No errors |
| VAL-MSG-003 | Structural | service-local compose context boundary | `docker compose --env-file .env.example -f infra/05-messaging/rabbitmq/docker-compose.yml --profile messaging config --services` | Because `undefined network infra_net` occurs without root `infra_net` context, the root profile or overlay is required |
| VAL-MSG-004 | Compliance | Verify messaging hardening baseline | `bash scripts/hardening/check-all-hardening.sh 05-messaging` | 0 failures |
| VAL-MSG-005 | Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | 0 failures |
| VAL-MSG-006 | Traceability | Document traceability validation | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| SSO chain hardening affects operations automation API access | Medium | Document internal-port operations paths and exception procedures in the runbook |
| Incorrect router middleware application breaks management UI | High | Run compose static validation immediately after changes and provide rollback procedures |
| Catalog expansion remains incomplete | Medium | Document the staged expansion roadmap in operations policy, guide, and task records |
| Document indexes are omitted | Medium | Synchronize modified folder READMEs in the same change set |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: `check-all-hardening.sh 05-messaging`, `check-template-security-baseline`, `check-doc-traceability`
- **Sandbox / Canary Rollout**: Start by messaging profile stage and then check health.
- **Human Approval Gate**: Approval is required for external exposure policy, SSO bypass, or HA topology expansion changes.
- **Rollback Trigger**: Management UI access failure, compose validation error, or CI gate failure.
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] Messaging compose hardening items reflected
- [x] `check-all-hardening.sh 05-messaging` and CI gate reflected
- [x] Stage 01 through 05 optimization-hardening documents and README indexes synchronized
- [ ] Runtime validation evidence secured when the environment allows

## Related Documents

- **PRD**: [../01.requirements/017-messaging-optimization-hardening.md](../../01.requirements/017-messaging-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md](../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../03.specs/006-messaging/spec.md](../../03.specs/006-messaging/spec.md)
- **Tasks**: [../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/05-messaging/optimization-hardening.md](../../05.operations/guides/05-messaging/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/05-messaging/optimization-hardening.md](../../05.operations/policies/05-messaging/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/05-messaging/optimization-hardening.md](../../05.operations/runbooks/05-messaging/optimization-hardening.md)
