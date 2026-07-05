---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-03-28-06-observability-optimization-hardening-plan.md -->

# 06-Observability Optimization Hardening Implementation Plan

## Overview

This document is the optimization/hardening implementation plan for `infra/06-observability`. It stages gateway boundary hardening, health-based startup stabilization, custom image hardening, CI baseline introduction, and document hierarchy synchronization.

## Context

- Baseline catalog: [infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Parent priority plan: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- Target configuration: `infra/06-observability` compose plus custom image and docs/CI/scripts

## Goals & In-Scope

- **Goals**:
  - Align observability public paths with the gateway standard chain and SSO policy.
  - Strengthen health-based dependency contracts for initial startup stability.
  - Strengthen runtime hardening for Loki/Tempo custom images.
  - Add an observability-specific hardening gate to CI.
  - Synchronize PRD-to-Runbook documents against the optimization-hardening baseline.
- **In Scope**:
  - `infra/06-observability/docker-compose.yml`
  - `infra/06-observability/loki/{Dockerfile,docker-entrypoint.sh}`
  - `infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
  - `scripts/hardening/check-all-hardening.sh 06-observability`
  - `.github/workflows/ci-quality.yml`
  - Observability optimization-hardening documents and READMEs under `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Immediately introducing multi-cluster observability
  - Refactoring application instrumentation SDKs
- **Out of Scope**:
  - Directly changing non-observability tiers
  - Migrating long-term retention backends (TSDB/remote backend migration)

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-OBS-001 | Align public router middleware contract | `infra/06-observability/docker-compose.yml` | REQ-PRD-OBS-FUN-01,02 | Label strings verified |
| PLN-OBS-002 | Declare Loki/Tempo/Pyroscope routing boundaries | `infra/06-observability/docker-compose.yml` | REQ-PRD-OBS-FUN-01,02 | Router/service labels confirmed |
| PLN-OBS-003 | Strengthen health-based dependencies and cAdvisor healthcheck | `infra/06-observability/docker-compose.yml` | REQ-PRD-OBS-FUN-03,04 | Compose static check |
| PLN-OBS-004 | Harden Loki/Tempo custom images | `infra/06-observability/loki/*`, `infra/06-observability/tempo/*` | REQ-PRD-OBS-FUN-05 | Dockerfile/entrypoint patterns confirmed |
| PLN-OBS-005 | Add observability hardening baseline script coverage | `scripts/hardening/check-all-hardening.sh 06-observability` | REQ-PRD-OBS-FUN-06 | Script pass/fail behavior |
| PLN-OBS-006 | Add CI `infrastructure-hardening` job | `.github/workflows/ci-quality.yml` | REQ-PRD-OBS-FUN-06 | Workflow job confirmed |
| PLN-OBS-007 | Create/update PRD-to-Runbook document set | `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**` | REQ-PRD-OBS-FUN-07 | Cross-links and README entries reflected |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-OBS-001 | Structural | Static Observability compose validation | `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh` or service-local network/secret overlay | No errors |
| VAL-OBS-002 | Compliance | Verify observability hardening baseline | `bash scripts/hardening/check-all-hardening.sh 06-observability` | 0 failures |
| VAL-OBS-003 | Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | 0 failures |
| VAL-OBS-004 | Traceability | Document traceability validation | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| SSO chain hardening affects some operations access paths | Medium | Document exception approval and recovery procedures in the runbook |
| Router misconfiguration breaks UI access | High | Use compose static validation, hardening script coverage, and rollback procedures |
| Document indexes are omitted | Medium | Refresh modified folder READMEs together |
| Runtime environment dependency delays production verification | Medium | Promote CI static/policy validation to a required gate |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: `check-all-hardening.sh 06-observability`, `check-template-security-baseline`, `check-doc-traceability`
- **Sandbox / Canary Rollout**: Start by `obs` profile and then verify health.
- **Human Approval Gate**: Access-control relaxation, expanded port exposure, or HA topology changes.
- **Rollback Trigger**: Compose validation error, CI gate failure, or routing access failure.
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] Observability compose hardening items reflected
- [x] `check-all-hardening.sh 06-observability` and CI gate reflected
- [x] Stage 01 through 05 optimization-hardening documents and README indexes synchronized
- [ ] Runtime validation evidence secured when the environment allows

## Related Documents

- **PRD**: [../01.requirements/018-observability-optimization-hardening.md](../../01.requirements/018-observability-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0021-observability-optimization-hardening-architecture.md](../../02.architecture/requirements/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../03.specs/06-observability/spec.md](../../03.specs/06-observability/spec.md)
- **Tasks**: [../04.execution/tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/06-observability/optimization-hardening.md](../../05.operations/guides/06-observability/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/06-observability/optimization-hardening.md](../../05.operations/policies/06-observability/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/06-observability/optimization-hardening.md](../../05.operations/runbooks/06-observability/optimization-hardening.md)
