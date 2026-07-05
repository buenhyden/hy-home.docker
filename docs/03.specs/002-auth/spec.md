---
status: active
---
<!-- Target: docs/03.specs/002-auth/spec.md -->

# 02-Auth Optimization Hardening Specification

## Overview

This document defines the optimization/hardening implementation contract for `infra/02-auth`. It specifies Keycloak/OAuth2 Proxy runtime configuration, secret injection, fail-closed operating principles, and verification/documentation traceability criteria.

## Strategic Boundaries & Non-goals

- This specification owns authentication infrastructure operating quality and security hardening.
- Application-specific RBAC business logic, new IdP adoption, and protocol changes are out of scope.

## Related Inputs

- **PRD**: [../../01.requirements/014-auth-optimization-hardening.md](../../01.requirements/014-auth-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0014-auth-optimization-hardening-architecture.md](../../02.architecture/requirements/0014-auth-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md](../../02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md)
  - [../../02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md](../../02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md)

## Contracts

- **Config Contract**:
  - Keycloak: keep `template-infra-high` and `/run/secrets/*`-based DB/Admin secret injection
  - OAuth2 Proxy root-active dev leaf: `template-infra-readonly-med`, `dev.Dockerfile`, `docker-entrypoint.dev.sh`, `mng-valkey` session store
  - OAuth2 Proxy local/full leaf: `template-infra-readonly-med`, `Dockerfile`, `docker-entrypoint.sh`, `oauth2-proxy-valkey` session store
- **Data / Interface Contract**:
  - OIDC issuer: `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`
  - Callback: `https://auth.${DEFAULT_URL}/oauth2/callback`
  - Session store: root-active dev leaf uses `redis://mng-valkey:6379`; local/full leaf uses `redis://oauth2-proxy-valkey:6379`
- **Governance Contract**:
  - Passing `scripts/hardening/check-all-hardening.sh 02-auth` is required for the CI merge gate.
  - Guide/Operation/Runbook documents keep reciprocal links.

## Core Design

- **Component Boundary**:
  - Keycloak: token issuance and IdP management
  - OAuth2 Proxy: ForwardAuth authentication gate
- **Key Dependencies**:
  - `mng-pg` (Keycloak DB)
  - `mng-valkey` (OAuth2 session)
  - Traefik middleware/routers
- **Tech Stack**:
  - Keycloak 26.6.4-1
  - OAuth2 Proxy 7.15.2
  - Docker Compose + common optimization templates

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Keycloak realm/user/client state is stored in PostgreSQL.
  - OAuth2 Proxy sessions are stored in the Valkey keyspace.
- **Migration / Transition Plan**:
  - Move the secret injection path from Compose inline shell to the entrypoint.
  - Standardize domain/issuer/callback values through environment variables.

## Interfaces & Data Structures

### Core Interfaces

```typescript
interface AuthHardeningContract {
  service: "keycloak" | "oauth2-proxy";
  failClosed: true;
  secretsSource: "/run/secrets";
  healthEndpoint: string;
}
```

## API Contract (If Applicable)

The authentication layer does not directly provide application APIs. The external exposure contract is limited to gateway/auth endpoint behavior.

- `/oauth2/auth`
- `/oauth2/start`
- `/oauth2/callback`
- `/ping`

## Edge Cases & Error Handling

- Keycloak issuer unavailable: OAuth2 Proxy authentication fails with the default fail-closed behavior.
- Cookie domain mismatch: login loops occur.
- Immediately after secret rotation: existing sessions are invalidated.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: sustained OIDC provider timeout/5xx responses
- **Fallback**: decide degraded mode, with limited bypass or maintenance guidance according to policy/runbook procedure
- **Human Escalation**: page Infra on-call and Security reviewer together

## Verification

Required verification commands:

```bash
bash scripts/hardening/check-all-hardening.sh 02-auth
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh
bash scripts/validation/check-template-security-baseline.sh
bash scripts/validation/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-AUTH-001**: `check-all-hardening.sh 02-auth` has zero failures.
- **VAL-SPC-AUTH-002**: root `auth`/`core` profile Compose validation and the CI `infrastructure-hardening` job run successfully.
- **VAL-SPC-AUTH-003**: 02-auth Guide/Operation/Runbook are connected through reciprocal links.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/02-auth/README.md](../../05.operations/guides/02-auth/README.md)
- **Policy**: [../../05.operations/policies/02-auth/README.md](../../05.operations/policies/02-auth/README.md)
- **Runbook**: [../../05.operations/runbooks/02-auth/README.md](../../05.operations/runbooks/02-auth/README.md)
