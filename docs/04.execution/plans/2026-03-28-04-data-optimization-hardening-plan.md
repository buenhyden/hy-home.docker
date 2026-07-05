---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md -->

# 04-Data Optimization Hardening Implementation Plan

## Overview

This document is the optimization/hardening implementation plan for `infra/04-data`. It first reflects configuration-consistency items with high immediate regression risk, then defines a staged implementation plan for catalog expansion items through operations policy and runbooks.

## Context

- Baseline catalog: [infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Parent priority plan: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- Immediate hardening targets: `supabase`, `valkey-cluster`, `seaweedfs`, `ksql`

## Goals & In-Scope

- **Goals**:
  - Fix 04-data compose configuration consistency for healthchecks, secrets, labels, and tokens.
  - Introduce a 04-data-specific CI hardening gate.
  - Synchronize the Stage 01 through 05 document system in the optimization/hardening context.
- **In Scope**:
  - `infra/04-data/operational/supabase/docker-compose.yml`
  - `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`
  - `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`
  - `infra/04-data/analytics/ksql/docker-compose.yml`
  - `scripts/hardening/check-all-hardening.sh 04-data`
  - `.github/workflows/ci-quality.yml`
  - `scripts/README.md`
  - `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}` and related README indexes

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Immediate implementation of catalog expansion items across all services at once
  - App-level performance tuning or query refactoring
- **Out of Scope**:
  - Introducing a new data engine
  - Migrating to a cloud-managed data platform

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-DATA-001 | Strengthen core `supabase` service healthchecks | `infra/04-data/operational/supabase/docker-compose.yml` | REQ-PRD-DATA-FUN-01 | Compose config and service-block healthchecks confirmed |
| PLN-DATA-002 | Align the Valkey exporter secret-path contract | `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml` | REQ-PRD-DATA-FUN-02 | 0 stale secret paths |
| PLN-DATA-003 | Remove the SeaweedFS expose token typo | `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml` | REQ-PRD-DATA-FUN-03 | 0 malformed expose tokens |
| PLN-DATA-004 | Normalize ksql tier labels | `infra/04-data/analytics/ksql/docker-compose.yml` | REQ-PRD-DATA-FUN-04 | `hy-home.tier: data` confirmed |
| PLN-DATA-005 | Add 04-data hardening validation script coverage | `scripts/hardening/check-all-hardening.sh 04-data` | REQ-PRD-DATA-FUN-05 | Script pass/fail behavior works normally |
| PLN-DATA-006 | Add CI `infrastructure-hardening` job | `.github/workflows/ci-quality.yml` | REQ-PRD-DATA-FUN-05 | Workflow static check passes |
| PLN-DATA-007 | Refresh scripts index | `scripts/README.md` | REQ-PRD-DATA-FUN-05 | README entry and usage example reflected |
| PLN-DATA-008 | Create/update PRD-to-Runbook documents and align cross-links | `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**` | REQ-PRD-DATA-FUN-06 | Links and indexes reflected |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-DATA-001 | Structural | Static Supabase compose validation | `docker compose -f infra/04-data/operational/supabase/docker-compose.yml config` | No errors |
| VAL-DATA-002 | Structural | Static Valkey compose validation | `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml config` | No errors |
| VAL-DATA-003 | Structural | Static SeaweedFS compose validation | `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml config` | No errors |
| VAL-DATA-004 | Structural | Static ksql compose validation | `docker compose -f infra/04-data/analytics/ksql/docker-compose.yml config` | No errors |
| VAL-DATA-005 | Compliance | 04-data hardening validation | `bash scripts/hardening/check-all-hardening.sh 04-data` | 0 failures |
| VAL-DATA-006 | Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | 0 failures |
| VAL-DATA-007 | Traceability | Document traceability | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Liveness-based healthcheck limitations | Medium | Improve with readiness endpoint coverage in a later phase |
| Simultaneous multi-service changes create broad impact | High | Limit immediate hardening scope to consistency items |
| Catalog expansion remains incomplete | Medium | Pre-reflect approval conditions and transition procedures in policy/runbook documents |
| Document links regress | Medium | Refresh README indexes and cross-links in the same change set |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: `check-all-hardening.sh 04-data`, `check-template-security-baseline`, `check-doc-traceability`
- **Sandbox / Canary Rollout**: Apply by stage after validating compose config for each 04-data service.
- **Human Approval Gate**: Operations approval is required for HA expansion, retention policy changes, or external exposure policy changes.
- **Rollback Trigger**: Sustained healthcheck failure, exporter authentication failure, or compose parsing error.
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] Immediate 04-data hardening items reflected
- [x] data-hardening validation and CI gate reflected
- [x] Stage 01 through 05 documents and README indexes synchronized
- [ ] Runtime validation evidence secured when the environment allows

## Related Documents

- **PRD**: [../01.requirements/016-data-optimization-hardening.md](../../01.requirements/016-data-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0019-data-optimization-hardening-architecture.md](../../02.architecture/requirements/0019-data-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../03.specs/004-data/spec.md](../../03.specs/004-data/spec.md)
- **Tasks**: [../04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md](../tasks/2026-03-28-04-data-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/04-data/optimization/optimization-hardening.md](../../05.operations/guides/04-data/optimization/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/04-data/optimization/optimization-hardening.md](../../05.operations/policies/04-data/optimization/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/04-data/optimization/optimization-hardening.md](../../05.operations/runbooks/04-data/optimization/optimization-hardening.md)
