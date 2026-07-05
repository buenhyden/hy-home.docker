---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md -->

# 03-Security (Vault) Optimization Hardening Implementation Plan

## Overview

This document is the optimization/hardening implementation plan for `infra/03-security/vault`. It prioritizes immediately applicable hardening implementation and validation automation, while fixing auto-unseal and remote audit as policy and transition procedures.

## Context

- Baseline catalog: [infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
- Parent priority plan: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- Application strategy: phased application (immediate hardening -> policy/transition design -> documentation traceability synchronization)

## Goals & In-Scope

- **Goals**:
  - Stabilize the Vault Agent template, health, and volume contracts.
  - Enforce 03-security hardening validation through a CI gate.
  - Synchronize the Stage 01 through 05 document system for the optimization/hardening purpose.
  - Fix the root `security`/`core` profile validation boundary against current implementation.
- **In Scope**:
  - `infra/03-security/vault/docker-compose.yml`
  - `infra/03-security/vault/config/templates/*.ctmpl`
  - `scripts/hardening/check-all-hardening.sh 03-security`
  - `.github/workflows/ci-quality.yml`
  - `scripts/README.md`
  - `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}` and README indexes

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Immediate auto-unseal (KMS/HSM) implementation
  - Immediate remote audit sink implementation
- **Out of Scope**:
  - Changing the internal TLS model
  - Changing application settings in other tiers

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-SEC-001 | Normalize `vault-agent` healthcheck, `/vault/out` volume, and capabilities | `infra/03-security/vault/docker-compose.yml` | REQ-PRD-FUN-02,03 | Compose config and healthcheck contract confirmed |
| PLN-SEC-002 | Remove Vault Agent template placeholders and normalize paths/keys | `infra/03-security/vault/config/templates/*.ctmpl` | REQ-PRD-FUN-01 | 0 placeholders; source/destination integrity preserved |
| PLN-SEC-003 | Add 03-security hardening validation script coverage | `scripts/hardening/check-all-hardening.sh 03-security` | REQ-PRD-FUN-04 | Script pass/fail behavior verified |
| PLN-SEC-004 | Add CI `infrastructure-hardening` job | `.github/workflows/ci-quality.yml` | REQ-PRD-FUN-04 | Job runs on PR/push |
| PLN-SEC-005 | Reflect scripts README inventory | `scripts/README.md` | REQ-PRD-FUN-04 | README entry and example exist |
| PLN-SEC-006 | Clarify root security profile validation boundary | `docs/03.specs/003-security/spec.md`, operations docs | REQ-PRD-FUN-04 | Root profile validation passes |
| PLN-SEC-007 | Create/update PRD-to-Runbook documents and synchronize README indexes | `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**` | REQ-PRD-FUN-05 | Cross-links and indexes reflected |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-SEC-001 | Root Compose | Static root security profile validation | `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh` | 0 failures |
| VAL-SEC-002 | Compliance | 03-security hardening validation | `bash scripts/hardening/check-all-hardening.sh 03-security` | 0 failures |
| VAL-SEC-003 | Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | 0 failures |
| VAL-SEC-004 | Traceability | Document traceability validation | `bash scripts/validation/check-doc-traceability.sh` | 0 failures |
| VAL-SEC-005 | Dependency Compose | Root core profile resolution validation | `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` | 0 failures |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Vault internal secret paths/keys diverge | High | Document the template contract and provide runbook recovery procedures |
| Single-node retention creates availability risk | Medium | Document the HA expansion (raft 3-node) transition procedure in ops/runbook |
| Adding a CI gate increases initial failures | Medium | Synchronize the script contract with current configuration before applying it |
| Document links regress | Medium | Refresh README indexes and cross-links in the same change set |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Pass `check-all-hardening.sh 03-security`, root profile validation, and `check-doc-traceability`.
- **Sandbox / Canary Rollout**: Apply changes in stages after vault compose validation.
- **Human Approval Gate**: Operations approval is required for auto-unseal and remote audit transition.
- **Rollback Trigger**: Sustained vault-agent health failure or sustained template render failure.
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] 03-security configuration hardening reflected
- [x] security-hardening validation and CI gate reflected
- [x] Stage 01 through 05 documents and README indexes synchronized
- [ ] Runtime validation evidence secured when the environment allows

## Related Documents

- **PRD**: [../01.requirements/015-security-optimization-hardening.md](../../01.requirements/015-security-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0018-security-optimization-hardening-architecture.md](../../02.architecture/requirements/0018-security-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../03.specs/003-security/spec.md](../../03.specs/003-security/spec.md)
- **Tasks**: [../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/03-security/vault.md](../../05.operations/guides/03-security/vault.md)
- **Policy**: [../../05.operations/policies/03-security/vault.md](../../05.operations/policies/03-security/vault.md)
- **Runbooks**: [../../05.operations/runbooks/03-security/vault.md](../../05.operations/runbooks/03-security/vault.md)
