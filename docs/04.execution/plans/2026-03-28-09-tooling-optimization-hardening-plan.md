---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-03-28-09-tooling-optimization-hardening-plan.md -->

# 09-Tooling Optimization Hardening Implementation Plan

## Overview

This document is the optimization/hardening implementation plan for `infra/09-tooling`. It stages gateway+SSO boundary alignment, explicit network isolation, test-tool runtime stabilization, CI policy gate introduction, and catalog expansion roadmap work.

## Context

- Baseline catalog: [../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Parent priority plan: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- Target configuration: `infra/09-tooling/**/*`, `scripts/`, `.github/workflows/`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}`

## Goals & In-Scope

- **Goals**:
  - Align SonarQube/Terrakube/Syncthing public paths with gateway standard and SSO policy.
  - Standardize the `infra_net` external boundary declaration in tooling compose files.
  - Align the locust-worker healthcheck and k6 volume contract.
  - Align tooling tier hardening verification with `scripts/hardening/check-all-hardening.sh 09-tooling` and the integrated `infrastructure-hardening` CI gate.
  - Make catalog expansion items executable through documents and tasks.
- **In Scope**:
  - `infra/09-tooling/*/docker-compose.yml`
  - `scripts/hardening/check-all-hardening.sh 09-tooling`
  - `scripts/README.md`
  - `.github/workflows/ci-quality.yml`
  - `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}` tooling optimization-hardening documents/READMEs

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Immediate full runtime application of catalog expansion items
  - Tooling service major upgrades
- **Out of Scope**:
  - Introducing new tools
  - Data tier architecture changes

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-TLG-001 | Align SonarQube/Terrakube/Syncthing middleware with the gateway+SSO chain | `infra/09-tooling/{sonarqube,terrakube,syncthing}/docker-compose.yml` | REQ-PRD-TLG-FUN-01 | Compose labels confirmed |
| PLN-TLG-002 | Standardize tooling compose `infra_net` external declarations | `infra/09-tooling/*/docker-compose.yml` | REQ-PRD-TLG-FUN-02 | Network contract confirmed |
| PLN-TLG-003 | Align locust worker healthcheck and k6 volume references | `infra/09-tooling/{locust,k6}/docker-compose.yml` | REQ-PRD-TLG-FUN-03 | Health/volume contract confirmed |
| PLN-TLG-004 | Add tooling hardening script and CI gate | `scripts/hardening/check-all-hardening.sh 09-tooling`, `.github/workflows/ci-quality.yml`, `scripts/README.md` | REQ-PRD-TLG-FUN-04 | Script/CI job confirmed |
| PLN-TLG-005 | Create PRD-to-Runbook document system and cross-links | `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**` | REQ-PRD-TLG-FUN-05 | Link consistency confirmed |
| PLN-TLG-006 | Break down catalog expansion items by tool | Plan/Task/Ops/Guide docs | REQ-PRD-TLG-FUN-06 | Task/policy reflection confirmed |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-TLG-001 | Structural | Verify tooling optional compose boundary | `bash scripts/hardening/check-all-hardening.sh 09-tooling`; approved runtime rehearsal uses root network/secret/dependency context | 0 failures; service-local standalone config is not treated as the success criterion |
| VAL-TLG-002 | Compliance | Verify tooling hardening baseline | `bash scripts/hardening/check-all-hardening.sh 09-tooling` | 0 failures |
| VAL-TLG-003 | Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | 0 failures |
| VAL-TLG-004 | Traceability | Verify document traceability | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| SSO hardening affects existing test access paths | Medium | Reflect exceptions and recovery procedures in the runbook |
| locust/k6 runtime contract changes affect test scripts | Medium | Use staged verification and basic scenario checks |
| Incomplete catalog expansion items leave policy gaps | Medium | Specify phases, priorities, and approval gates in tasks |

## Completion Criteria

- [x] Tooling compose/script/CI hardening reflected
- [x] Tooling optimization-hardening document set created
- [x] Stage 01-05 README indexes reflected
- [ ] Runtime rehearsal/performance evidence secured when the environment allows

## Related Documents

- **PRD**: [../01.requirements/021-tooling-optimization-hardening.md](../../01.requirements/021-tooling-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0024-tooling-optimization-hardening-architecture.md](../../02.architecture/requirements/0024-tooling-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../03.specs/010-tooling/spec.md](../../03.specs/010-tooling/spec.md)
- **Tasks**: [../04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md](../tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/09-tooling/optimization-hardening.md](../../05.operations/guides/09-tooling/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/09-tooling/optimization-hardening.md](../../05.operations/policies/09-tooling/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/09-tooling/optimization-hardening.md](../../05.operations/runbooks/09-tooling/optimization-hardening.md)
