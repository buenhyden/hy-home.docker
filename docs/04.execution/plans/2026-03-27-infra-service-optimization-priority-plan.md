---
status: active
---
<!-- Target: docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md -->

# Infra Service Optimization Priority Plan (Quick Wins + Quarterly) Implementation Plan

> Baseline document: `docs/05.operations/policies/00-workspace/infra-service-optimization-catalog.md`

---

## Overview

This document is the integrated implementation plan that fixes execution priorities in the `docs/04.execution/plans` layer based on the infrastructure service optimization catalog.
The scope is documentation-based implementation planning; actual Compose changes are performed in the later `docs/04.execution/tasks` stage.
The plan structure is Quick Wins (30 days) plus Quarterly work for the next two quarters: 2026 Q2 and 2026 Q3.

## Status Boundary

This plan intentionally remains `status: active` as an umbrella roadmap and
priority contract. The checked `Completion Criteria` below mean the plan
document itself was authored, indexed, and verified; they do not mean every
2026 Q2/Q3 roadmap deliverable has been fully executed or superseded.

The plan can move to `status: completed` only when a later task record proves
that the remaining quarterly roadmap and operations-standard codification work
has either been implemented, superseded by a newer active roadmap, or explicitly
retired with replacement evidence. Until then, this file remains the active
parent plan for historical 2026-03 optimization and hardening child plans.

## Context

- Baseline document: [infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Baseline data (39-service snapshot):
  - `healthcheck` not configured: 6
  - `restart` not configured: 21
  - `no-new-privileges` not configured: 37
  - `limits(cpus/memory)` not configured: 37
  - `secrets` not configured: 16
- `common-optimizations.yml` coverage snapshot (2026-03-28):
  - Service directory basis: `39/39 (100%)` applied
  - Compose file basis: `43/43 (100%)` applied
  - Unapplied services: none (`0` on a service basis)
  - Auxiliary Compose: `04-data/analytics/opensearch/docker-compose.cluster.yml` applied
  - Intentional template exception SSoT: `infra/common-optimizations.exceptions.json`
- `PLN-QW-001~005` baseline enforcement status (2026-03-28):
  - Validation command: `bash scripts/validation/check-quickwin-baseline.sh`
  - Template/security validation command: `bash scripts/validation/check-template-security-baseline.sh`
  - Result: `0` missing `restart/healthcheck/no-new-privileges/cpus/mem_limit/secrets` after approved exceptions
  - Approved exception SSoT: `infra/common-optimizations.exceptions.json`
- Fixed schedule:
  - Quick Wins baseline date: 2026-03-27
  - Quick Wins target completion date: 2026-04-26
  - Quarterly scope: 2026 Q2, 2026 Q3

## Public Interfaces Impact

- No runtime API, schema, or code interface changes.
- Only documentation interface changes occur:
  - Add an index entry to `docs/04.execution/plans/README.md`.
  - Add relative-path traceability links in this plan.

## Goals & In-Scope

- **Goals**:
  - Fix catalog-based execution priorities as completed decisions.
  - Confirm a Quick Wins backlog that can reduce immediate risk within 30 days.
  - Define operating-improvement goals and completion criteria for 2026 Q2/Q3.
- **In Scope**:
  - Define the priority model and fix tier weights.
  - Define Quick Wins work items (PLN-QW-001 through PLN-QW-007).
  - Define the Quarterly roadmap (quarterly goals, deliverables, and completion criteria).
  - Define verification plan and test scenarios.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Changing actual `infra/*/docker-compose*` files
  - Performing runtime service scaling or deployment
- **Out of Scope**:
  - Implementing code-level performance tuning
  - Writing or editing detailed per-service runbook procedures

## Priority Model

- Priority Score = `Risk Reduction(40) + Availability Impact(25) + Security Impact(25) + Execution Effort Inverse(10)`
- Tier Weight:
  - Tier A: 01-gateway, 02-auth, 03-security, 04-data, 05-messaging, 06-observability
  - Tier B: 07-workflow, 08-ai, 09-tooling, 10-communication
  - Tier C: 11-laboratory

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-QW-001 | Standardize `restart` policy for long-running Tier A/B services | `infra/**/docker-compose*.yml`, `docs/04.execution/tasks/*` | REQ-OPS-BASE-001 | 0 missing `restart` entries for target Tier A/B services |
| PLN-QW-002 | Prioritize strengthening services missing `healthcheck` coverage, with operations-critical services first and lab services later | `infra/**/docker-compose*.yml`, `docs/05.operations/**` | REQ-OPS-BASE-002 | 0 missing `healthcheck` entries for core Tier A/B services |
| PLN-QW-003 | Introduce default `no-new-privileges` application principle and list exceptions | `infra/**/docker-compose*.yml`, `docs/05.operations/**` | REQ-SEC-BASE-003 | Exception list documented and default application rate is 100% |
| PLN-QW-004 | Confirm resource minimum cap (`cpus`, `memory`) policy draft | `docs/05.operations/policies/00-workspace/infra-service-optimization-catalog.md`, `docs/04.execution/tasks/*` | REQ-OPS-CAP-004 | Tier-specific minimum cap policy documented |
| PLN-QW-005 | Standardize sensitive-data injection paths with `secrets`/Vault first | `infra/**/docker-compose*.yml`, `infra/03-security/vault/**`, `docs/05.operations/**` | REQ-SEC-SECRETS-005 | Plaintext secret injection paths reduced and standard paths documented |
| PLN-QW-006 | Establish criteria for handling workflow tier new-service definition gaps | `docs/98.archive/README.md`, `docs/05.operations/**/07-workflow/README.md` | REQ-WF-GAP-006 | Unimplemented workflow services are removed from the active chain and tracked only in the archive ledger |
| PLN-QW-007 | Clean up document traceability (`04.execution/plans` to `05.operations/{guides,policies,runbooks}`) | `docs/04.execution/plans/**`, `docs/05.operations/**` | REQ-DOC-TRACE-007 | Cross-link integrity is 100% |

## Quarterly Roadmap

| Quarter | Goals | Deliverables | Completion Criteria |
| --- | --- | --- | --- |
| 2026 Q2 (2026-04-01 ~ 2026-06-30) | Codify operations criteria (Compose lint/gate), regularize backup/recovery rehearsals, and strengthen SLO/Alert alignment | Compose policy gate draft, recovery rehearsal calendar, SLO/Alert alignment report | Tier A core services meet 100% of the operations baseline |
| 2026 Q3 (2026-07-01 ~ 2026-09-30) | Optimize scalability/performance for messaging, data, and AI; add policy auto-validation CI; improve security hardening | Performance optimization backlog completion report, policy validation CI pipeline, security hardening checklist | Quarterly performance regression and incident recovery lead-time targets are met |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Link integrity for new `04.execution/plans` document relative paths | Relative-path link check script or manual validation | Every link target file exists |
| VAL-PLN-002 | Compliance | Required template section compliance (`Overview`, `Work Breakdown`, `Verification`, `Completion`) | Document section checklist review | 0 missing required sections |
| VAL-PLN-003 | Traceability | Item consistency against the baseline catalog (Quick Wins/Quarterly mapping) | Review item mapping against the catalog | 1:1 mapping with no omissions or duplicates |
| VAL-PLN-004 | Indexing | Confirm reflection in `docs/04.execution/plans/README.md` index | Review README Structure section | New plan entry exists |
| VAL-PLN-005 | Automation | Automated verification for `04.execution/plans` to `05.operations/{guides,policies,runbooks}` link synchronization | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |

## Test Cases / Scenarios

| ID | Scenario | Expected Result |
| --- | --- | --- |
| TST-PLN-001 | Read the new plan in isolation | Quick Wins, Quarterly work, verification criteria, and completion criteria support decisions in one document |
| TST-PLN-002 | Operator cross-checks the catalog and plan | Catalog recommendations map to plan tasks without omissions |
| TST-PLN-003 | Navigate the document index | The new plan is immediately reachable from `docs/04.execution/plans/README.md` |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Review link and requirement mapping completeness across document policy, catalog, and runbooks.
- **Sandbox / Canary Rollout**: Apply progressively from Tier A in the later `docs/04.execution/tasks` stage.
- **Human Approval Gate**: Start Compose changes after Infra Lead and Security Reviewer approval.
- **Rollback Trigger**: Stop and replan if plan-catalog mismatch or operations impact risk increases.
- **Prompt / Model Promotion Criteria**: N/A for the documentation planning stage.

## Completion Criteria

- [x] Single integrated plan completed, including Quick Wins and Quarterly work
- [x] Priority model and tier weights fixed
- [x] 7 Quick Wins work items defined
- [x] 2026 Q2/Q3 quarterly roadmap defined
- [x] Verification plan (VAL-PLN-001 through VAL-PLN-005) and test scenarios defined
- [x] `docs/04.execution/plans/README.md` index refreshed

## Assumptions & Defaults

- Execution owner labels remain role-based (Infra Lead, DevOps, SRE, Security) instead of personal names.
- This deliverable includes planning and indexing; actual Compose edits happen in the later Task stage.
- The quarterly roadmap baseline date is fixed at 2026-03-27.

## Related Documents

- **Operations Catalog**: [infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- **Operations Index**: [05.operations README](../../05.operations/README.md)
- **Runbook Index**: [05.operations README](../../05.operations/README.md)
- **Plan Index**: [04.execution/plans README](./README.md)
- **Task Layer**: [04.execution/tasks README](../tasks/README.md)
