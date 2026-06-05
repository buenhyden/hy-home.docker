---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md -->

# Task: 02-Auth Optimization Hardening

## Overview

This document tracks the `02-auth` optimization and hardening implementation tasks. It manages Keycloak/OAuth2 Proxy configuration changes, CI gates, and documentation traceability cleanup as task units.

## Inputs

- **Parent Spec**: [../../03.specs/02-auth/spec.md](../../03.specs/02-auth/spec.md)
- **Parent Plan**: [../plans/2026-03-28-02-auth-optimization-hardening-plan.md](../plans/2026-03-28-02-auth-optimization-hardening-plan.md)

## Working Rules

- Secrets keep the file-based (`/run/secrets`) contract.
- Fail-open changes are prohibited, and degraded mode is performed only through documented procedures.
- Documentation changes update the folder README index in the same change set.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-AUTH-001 | Remove inline shell from OAuth2 Proxy compose and switch to entrypoint-based execution | impl | 02-auth/spec.md / Contracts | PLN-AUTH-001 | `bash scripts/hardening/check-all-hardening.sh 02-auth` | Infra | Done |
| T-AUTH-002 | Handle cookie/client/redis secret file injection in the OAuth2 Proxy entrypoint | impl | 02-auth/spec.md / Core Design | PLN-AUTH-001 | `bash scripts/hardening/check-all-hardening.sh 02-auth` | Infra | Done |
| T-AUTH-003 | Create a non-root user in the OAuth2 Proxy Dockerfile and apply `USER` | impl | 02-auth/spec.md / Security | PLN-AUTH-002 | `bash scripts/hardening/check-all-hardening.sh 02-auth` | DevOps | Done |
| T-AUTH-004 | Remove secret length output from Keycloak compose | impl | 02-auth/spec.md / Security | PLN-AUTH-003 | Code review + `docker compose config` | Infra | Done |
| T-AUTH-005 | Add `scripts/hardening/check-all-hardening.sh 02-auth` | ops | 02-auth/spec.md / Verification | PLN-AUTH-004 | Confirm script pass/fail behavior | DevOps | Done |
| T-AUTH-006 | Add the `infrastructure-hardening` job to the CI workflow | ops | 02-auth/spec.md / CI | PLN-AUTH-005 | PR CI logs | DevOps | Done |
| T-AUTH-007 | Create PRD/ARD/ADR/Plan/Task documents and connect links | doc | 02-auth/spec.md / Traceability | PLN-AUTH-006 | Confirm bidirectional relative-path links | Docs | Done |
| T-AUTH-008 | Rework the 02-auth Guide/Operation/Runbook and update README indexes | doc | 02-auth/spec.md / Traceability | PLN-AUTH-006, PLN-AUTH-007 | `bash scripts/validation/check-doc-traceability.sh` | Docs | Done |
| T-AUTH-009 | Run 02-auth validation commands and record results | test | 02-auth/spec.md / Verification | PLN-AUTH-004~005 | Collect execution results | Infra | Done |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-AUTH-001
- [x] T-AUTH-002
- [x] T-AUTH-003
- [x] T-AUTH-004

### Phase 2

- [x] T-AUTH-005
- [x] T-AUTH-006
- [x] T-AUTH-007
- [x] T-AUTH-008
- [x] T-AUTH-009

## Verification Summary

- **Test Commands**:
  - `bash scripts/hardening/check-all-hardening.sh 02-auth`
  - `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
  - `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: PR CI logs + local command output (`infrastructure-hardening/root-profile/template-security/doc-traceability`)

## Related Documents

- (No reference documents)
