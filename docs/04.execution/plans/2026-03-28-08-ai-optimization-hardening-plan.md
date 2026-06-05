---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md -->

# 08-AI Optimization Hardening Implementation Plan

## Overview

This document is the optimization/hardening implementation plan for `infra/08-ai`. It stages gateway boundary security alignment, GPU concurrency protection, Open WebUI stateful consistency, exporter health contracts, CI policy gates, and catalog expansion policy work.

## Context

- Baseline catalog: [../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Parent priority plan: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- Target configuration: `infra/08-ai/**/*`, `scripts/`, `.github/workflows/`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}`

## Goals & In-Scope

- **Goals**:
  - Align Ollama/Open WebUI public paths with gateway standard and SSO policy.
  - Declare concurrency/queue limits to protect Ollama GPU resources.
  - Align Open WebUI with the stateful operations template.
  - Stabilize the exporter through health-gated startup.
  - Catch AI hardening regressions early through script/CI coverage.
  - Make catalog expansion items (model promotion, access separation, log policy) executable through documents and tasks.
- **In Scope**:
  - `infra/08-ai/ollama/docker-compose.yml`
  - `infra/08-ai/open-webui/docker-compose.yml`
  - `scripts/hardening/check-all-hardening.sh 08-ai`
  - `scripts/README.md`
  - `.github/workflows/ci-quality.yml`
  - AI optimization-hardening documents and READMEs under `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Immediate migration to multi-node or multi-region AI inference architecture
  - Standardizing external LLM providers
- **Out of Scope**:
  - Changing the Qdrant internal data model
  - Building model training or fine-tuning pipelines

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-AI-001 | Align Ollama/Open WebUI gateway+SSO middleware | `infra/08-ai/*/docker-compose.yml` | REQ-PRD-AI-FUN-01 | Compose labels confirmed |
| PLN-AI-002 | Declare Ollama concurrency/queue/resource limits | `infra/08-ai/ollama/docker-compose.yml` | REQ-PRD-AI-FUN-02 | env contract confirmed |
| PLN-AI-003 | Align Open WebUI stateful template | `infra/08-ai/open-webui/docker-compose.yml` | REQ-PRD-AI-FUN-03 | `template-stateful-med` confirmed |
| PLN-AI-004 | Strengthen exporter health-gated dependency and healthcheck | `infra/08-ai/ollama/docker-compose.yml` | REQ-PRD-AI-FUN-04 | `depends_on`/healthcheck confirmed |
| PLN-AI-005 | Add AI hardening script and CI gate | `scripts/hardening/check-all-hardening.sh 08-ai`, `.github/workflows/ci-quality.yml`, `scripts/README.md` | REQ-PRD-AI-FUN-05 | Script/CI job confirmed |
| PLN-AI-006 | Create PRD-to-Runbook document system and cross-links | `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**` | REQ-PRD-AI-FUN-06 | Link consistency confirmed |
| PLN-AI-007 | Break down catalog expansion policy work (model promotion, access separation, log policy) | Plan/Task/Ops/Guide docs | REQ-PRD-AI-FUN-07 | Task/policy reflection confirmed |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-AI-001 | Structural | Static AI optional compose contract validation | `bash scripts/hardening/check-all-hardening.sh 08-ai` | 0 failures |
| VAL-AI-002 | Structural | root-active compose profile validation | `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh` | No errors |
| VAL-AI-003 | Compliance | Verify AI hardening baseline | `bash scripts/hardening/check-all-hardening.sh 08-ai` | 0 failures |
| VAL-AI-004 | Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | 0 failures |
| VAL-AI-005 | Traceability | Document traceability validation | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Incorrect concurrency limits reduce throughput | Medium | Tune in stages and readjust based on exporter metrics |
| SSO hardening blocks existing test paths | Medium | Reflect exceptions and recovery procedures in the runbook |
| Undefined log retention/masking policy causes operations variance | Medium | Specify approval gates in operations/task documents |
| Stateful template drift recurs | Low | Enforce policy with the AI hardening script |

## Completion Criteria

- [x] AI compose/script/CI hardening reflected
- [x] AI optimization-hardening document set created
- [x] Stage 01 through 05 README indexes reflected
- [ ] Runtime startup/rehearsal evidence secured when the environment allows

## Related Documents

- **PRD**: [../01.requirements/2026-03-28-08-ai-optimization-hardening.md](../../01.requirements/2026-03-28-08-ai-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0023-ai-optimization-hardening-architecture.md](../../02.architecture/requirements/0023-ai-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../03.specs/08-ai/spec.md](../../03.specs/08-ai/spec.md)
- **Tasks**: [../04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/08-ai/optimization-hardening.md](../../05.operations/guides/08-ai/optimization-hardening.md)
- **Operations**: [../../05.operations/policies/08-ai/optimization-hardening.md](../../05.operations/policies/08-ai/optimization-hardening.md)
- **Runbooks**: [../../05.operations/runbooks/08-ai/optimization-hardening.md](../../05.operations/runbooks/08-ai/optimization-hardening.md)
