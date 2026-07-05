---
status: active
---
<!-- Target: docs/03.specs/03-security/spec.md -->

# 03-Security Optimization Hardening Specification

## Overview

This document defines the optimization/hardening implementation contract for `infra/03-security/vault`. It specifies template secret path normalization, the `vault-agent` healthcheck/output volume, hardening verification automation, and phased HA expansion policy.

## Strategic Boundaries & Non-goals

- This specification owns the Vault/Vault Agent operating hardening contract.
- KMS/HSM auto-unseal and actual remote audit sink implementation are deferred to the next phase.

## Related Inputs

- **PRD**: [../../01.requirements/015-security-optimization-hardening.md](../../01.requirements/015-security-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0018-security-optimization-hardening-architecture.md](../../02.architecture/requirements/0018-security-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/0003-vault-as-secrets-manager.md](../../02.architecture/decisions/0003-vault-as-secrets-manager.md)
  - [../../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - `vault` and `vault-agent` keep inheriting `template-stateful-med`.
  - `vault-agent` provides a PID file (`/tmp/vault-agent.pid`)-based healthcheck.
  - Agent rendering output is written to the `/vault/out` persistent volume.
- **Data / Interface Contract**:
  - Template secret paths follow the `secret/data/hy-home/<tier>/<service>` convention.
  - Per-service key contract:
    - `04-data/mng-db`: `password`
    - `02-auth/keycloak`: `db_password`, `admin_username`, `admin_password`
    - `02-auth/oauth2-proxy`: `client_secret`, `cookie_secret`
    - `06-observability/grafana`: `admin_password`, `db_password`, `grafana_client_secret`
- **Governance Contract**:
  - Enforce `scripts/hardening/check-all-hardening.sh 03-security` through the CI `infrastructure-hardening` job.

## Core Design

- **Component Boundary**:
  - Vault: KV-v2 secret storage, policy, and audit
  - Vault Agent: AppRole authentication and template rendering
- **Key Dependencies**:
  - `01-gateway/traefik` (external TLS termination)
  - Secret-consuming tiers (`02-auth`, `04-data`, `06-observability`)
- **Tech Stack**:
  - `hashicorp/vault:2.0.3`
  - Docker Compose + `common-optimizations.yml`

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - KV-v2 path: `secret/data/hy-home/...`
- **Migration / Transition Plan**:
  - Remove placeholder templates, then lock the path/key contract.
  - Apply the auto-unseal/remote audit transition procedure in Phase 2.

## Interfaces & Data Structures

### Core Interfaces

```typescript
interface VaultTemplateContract {
  sourcePath: string;
  destinationPath: string;
  secretKey: string;
  placeholderForbidden: true;
}
```

## Edge Cases & Error Handling

- Missing AppRole role_id/secret_id causes agent rendering failure.
- Path/key mismatches cause empty template output or errors.
- Template refresh fails while Vault is sealed.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: `vault-agent` healthcheck failure or missing rendered output
- **Fallback**: follow the runbook to inspect seal state, AppRole files, and template paths, then restart
- **Human Escalation**: page Security Operator and Infra on-call together

## Verification

```bash
HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 03-security
bash scripts/validation/check-template-security-baseline.sh
bash scripts/validation/check-doc-traceability.sh
```

Runtime verification where the environment allows:

```bash
docker compose --profile security up -d vault vault-agent
docker compose --profile security exec vault vault status
docker inspect --format '{{json .State.Health}}' vault
docker inspect --format '{{json .State.Health}}' vault-agent
docker compose --profile security exec vault-agent ls -la /vault/out
```

## Success Criteria & Verification Plan

- **VAL-SPC-SEC-001**: `check-all-hardening.sh 03-security` has zero failures.
- **VAL-SPC-SEC-002**: `.ctmpl` placeholder path detection returns zero findings.
- **VAL-SPC-SEC-003**: CI `infrastructure-hardening` job runs successfully.
- **VAL-SPC-SEC-004**: documentation traceability check passes.
- **VAL-SPC-SEC-005**: root security/core profile validation passes.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/03-security/vault.md](../../05.operations/guides/03-security/vault.md)
- **Policy**: [../../05.operations/policies/03-security/vault.md](../../05.operations/policies/03-security/vault.md)
- **Runbook**: [../../05.operations/runbooks/03-security/vault.md](../../05.operations/runbooks/03-security/vault.md)
