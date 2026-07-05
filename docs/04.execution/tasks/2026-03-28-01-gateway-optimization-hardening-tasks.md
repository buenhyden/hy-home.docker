---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md -->

# Task: 01-Gateway Optimization Hardening

## Overview

This document tracks the `01-gateway` optimization and hardening execution tasks. Based on the parent Plan, it manages configuration changes, validation automation, CI gates, and documentation synchronization as task units.

## Inputs

- **Parent Spec**: [../../03.specs/001-gateway/spec.md](../../03.specs/001-gateway/spec.md)
- **Parent Plan**: [../plans/2026-03-28-01-gateway-optimization-hardening-plan.md](../plans/2026-03-28-01-gateway-optimization-hardening-plan.md)

## Working Rules

- Core behavior changes leave evidence through static validation commands.
- Every task links the changed files to validation commands.
- Documentation changes include the relevant folder README index in the same change set.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-GW-001 | Add `req-retry`, `req-circuit-breaker`, and `gateway-standard-chain` to Traefik middleware | impl | 001-gateway/spec.md / Gateway | PLN-GW-001 | `bash scripts/hardening/check-all-hardening.sh 01-gateway` | Infra | Done |
| T-GW-002 | Apply `gateway-standard-chain@file` to the Traefik dashboard router | impl | 001-gateway/spec.md / Gateway | PLN-GW-002 | `bash scripts/hardening/check-all-hardening.sh 01-gateway` | Infra | Done |
| T-GW-003 | Convert Nginx compose to `template-infra-readonly-low` with required tmpfs and `/ping` healthcheck | impl | 001-gateway/spec.md / Gateway | PLN-GW-003 | `bash scripts/hardening/check-all-hardening.sh 01-gateway` | Infra | Done |
| T-GW-004 | Apply timeout/failover/cache/server_tokens hardening to Nginx config | impl | 001-gateway/spec.md / Gateway | PLN-GW-004 | `bash scripts/hardening/check-all-hardening.sh 01-gateway` | Infra | Done |
| T-GW-005 | Add and document `scripts/hardening/check-all-hardening.sh 01-gateway` | ops | 001-gateway/spec.md / Verification | PLN-GW-005 | `bash scripts/hardening/check-all-hardening.sh 01-gateway` | DevOps | Done |
| T-GW-006 | Add the `infrastructure-hardening` job to the CI workflow | ops | 001-gateway/spec.md / CI | PLN-GW-006 | PR CI run | DevOps | Done |
| T-GW-007 | Synchronize Plan/Task/Operation/Runbook/Guide documents and README indexes | doc | 001-gateway/spec.md / Docs | PLN-GW-007 | `bash scripts/validation/check-doc-traceability.sh` | Docs | Done |
| T-GW-008 | Record Compose and baseline validation command results | test | 001-gateway/spec.md / Validation | PLN-GW-001~007 | root profile validator, hardening checks, runtime lint boundary | Infra | Done |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-GW-001
- [x] T-GW-002
- [x] T-GW-003
- [x] T-GW-004

### Phase 2

- [x] T-GW-005
- [x] T-GW-006
- [x] T-GW-007
- [x] T-GW-008

## Verification Summary

- **Test Commands**:
  - `bash scripts/hardening/check-all-hardening.sh 01-gateway`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: PR CI logs + local command outputs (`infrastructure-hardening/template-security/doc-traceability/root profile validation` pass). Nginx `nginx -t` is runtime-only evidence because the current Nginx leaf is not root-included by default and standalone service-local compose lacks root `infra_net`/backend context.

## Related Documents

- (No reference documents)
