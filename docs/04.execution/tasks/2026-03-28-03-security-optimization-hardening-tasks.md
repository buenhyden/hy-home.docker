---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md -->

# Task: 03-Security (Vault) Optimization Hardening

## Overview

This document tracks the `03-security` optimization and hardening implementation tasks. It manages Vault configuration hardening, validation automation, documentation synchronization, and auth validation regression recovery as task units.

## Inputs

- **Parent Spec**: [../../03.specs/03-security/spec.md](../../03.specs/03-security/spec.md)
- **Parent Plan**: [../plans/2026-03-28-03-security-optimization-hardening-plan.md](../plans/2026-03-28-03-security-optimization-hardening-plan.md)

## Working Rules

- Placeholder secret paths (`secret/data/example`) are not allowed.
- Hardening and traceability scripts are retained as evidence.
- Auto-unseal and remote audit work are documentation-only in this phase.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-SEC-001 | Apply `vault-agent` healthcheck, `/vault/out` volume, and capability adjustments to Vault compose | impl | 03-security/spec.md / Contracts | PLN-SEC-001 | root security profile validation | Infra | Done |
| T-SEC-002 | Normalize Vault Agent template paths/keys and remove placeholders | impl | 03-security/spec.md / Contracts | PLN-SEC-002 | `bash scripts/hardening/check-all-hardening.sh 03-security` | Infra | Done |
| T-SEC-003 | Add `scripts/hardening/check-all-hardening.sh 03-security` | ops | 03-security/spec.md / Governance | PLN-SEC-003 | Confirm script pass/fail behavior | DevOps | Done |
| T-SEC-004 | Add the CI `infrastructure-hardening` job | ops | 03-security/spec.md / Governance | PLN-SEC-004 | Static workflow review | DevOps | Done |
| T-SEC-005 | Refresh the scripts README index | doc | 03-security/spec.md / Related Docs | PLN-SEC-005 | Confirm README entries | Docs | Done |
| T-SEC-006 | Reflect the root-profile-based security validation boundary | ops | 03-security/spec.md / Governance | PLN-SEC-006 | `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh` | DevOps | Done |
| T-SEC-007 | Create PRD/ARD/ADR/Plan/Task and refresh Spec/Guide/Ops/Runbook docs | doc | 03-security/spec.md / Related Docs | PLN-SEC-007 | Confirm document links/indexes | Docs | Done |
| T-SEC-008 | Reflect README indexes (Stage 01-05 plus 03-security children) | doc | 03-security/spec.md / Related Docs | PLN-SEC-007 | Confirm README updates | Docs | Done |
| T-SEC-009 | Run static validation commands and record results | test | 03-security/spec.md / Verification | PLN-SEC-001~007 | Run 5 validation commands | Infra | Done |
| T-SEC-010 | Run runtime validation where available and record evidence | test | 03-security/spec.md / Verification | PLN-SEC-001~007 | Live `vault/vault-agent` health/runtime checks run in an approved runtime session | Infra | Deferred |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-SEC-001
- [x] T-SEC-002
- [x] T-SEC-003
- [x] T-SEC-004
- [x] T-SEC-005
- [x] T-SEC-006

### Phase 2

- [x] T-SEC-007
- [x] T-SEC-008
- [x] T-SEC-009
- [x] T-SEC-010 (Deferred runtime evidence recorded)

## Verification Summary

- **Test Commands**:
  - `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh`
  - `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
  - `bash scripts/hardening/check-all-hardening.sh 03-security`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: Local execution output + CI quality gates (`infrastructure-hardening`, `template-security-baseline`, `docs-traceability`)
- **Deferred Runtime Evidence**: T-SEC-010 requires an approved live Vault runtime session; static implementation and hardening gates are complete.

## Related Documents

- **PRD**: [../01.requirements/015-security-optimization-hardening.md](../../01.requirements/015-security-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0018-security-optimization-hardening-architecture.md](../../02.architecture/requirements/0018-security-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../plans/2026-03-28-03-security-optimization-hardening-plan.md](../plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **Guide**: [../../05.operations/guides/03-security/vault.md](../../05.operations/guides/03-security/vault.md)
- **Policy**: [../../05.operations/policies/03-security/vault.md](../../05.operations/policies/03-security/vault.md)
- **Runbook**: [../../05.operations/runbooks/03-security/vault.md](../../05.operations/runbooks/03-security/vault.md)
