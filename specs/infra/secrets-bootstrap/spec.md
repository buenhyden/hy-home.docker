---
title: 'Infra Secrets Bootstrap Script'
status: 'Implementation'
version: '1.0'
owner: 'Platform / DevOps'
prd_reference: '/docs/prd/infra-baseline-prd.md'
api_reference: 'N/A'
arch_reference: '/ARCHITECTURE.md'
tags: ['spec', 'implementation', 'infra', 'secrets', 'bootstrap']
---

# Implementation Specification (Spec) — Infra Secrets Bootstrap

> **Status**: Implementation
> **Related PRD**: [/docs/prd/infra-baseline-prd.md](/docs/prd/infra-baseline-prd.md)
> **Related ADR**: [/docs/adr/adr-0002-secrets-first-management.md](/docs/adr/adr-0002-secrets-first-management.md)
> **Related Architecture**: [/ARCHITECTURE.md](/ARCHITECTURE.md)

_Target Directory: `specs/infra/secrets-bootstrap/spec.md`_

## 0. Pre-Implementation Checklist (Governance)

### 0.1 Architecture / Tech Stack

| Item | Check Question | Required | Alignment Notes | Where |
| --- | --- | --- | --- | --- |
| Secrets Policy | Are secrets file-based under `secrets/**/*.txt` and injected at `/run/secrets/*`? | Must | ADR-0002 | Section 9 |
| Source of Truth | Is root `docker-compose.yml` authoritative for required secrets? | Must | Root-only orchestration | Section 2 |

### 0.2 Quality / Testing / Security

| Item | Check Question | Required | Alignment Notes | Where |
| --- | --- | --- | --- | --- |
| Leak Prevention | Does the script avoid printing secret values by default? | Must | Only BasicAuth password on first generation | Section 6 |
| Idempotency | Can the script run multiple times safely? | Must | Skip existing unless `--force` | Section 6 |
| Input Validation | Are CLI args and prerequisites validated? | Must | Fail-fast `set -euo pipefail` | Section 6 |

## 1. Technical Overview & Architecture Style

This feature adds a bootstrap utility `scripts/bootstrap-secrets.sh` that reads the root Compose `secrets:` definition (file-based secrets) and generates missing files under `secrets/**` with correct formats for services that expect non-plain secrets (Traefik htpasswd, Airflow Fernet key, Supabase JWT keys).

## 2. Coded Requirements (Traceability)

| ID | Requirement Description | Priority | Parent PRD REQ |
| --- | --- | --- | --- |
| REQ-SEC-001 | Script MUST parse secrets from root `docker-compose.yml` (`secrets:`..`include:`). | High | REQ-PRD-BASE-FUN-03 |
| REQ-SEC-002 | Script MUST generate missing secret files idempotently (no overwrite unless `--force`). | High | REQ-PRD-BASE-FUN-03 |
| REQ-SEC-003 | Script MUST support `--dry-run`, `--list`, `--only`, `--strict`, `--validate-compose`. | High | REQ-PRD-BASE-FUN-03 |
| SEC-SEC-001 | Script MUST NOT leak secret values to stdout/stderr by default. | Critical | REQ-PRD-BASE-FUN-02 |
| SEC-SEC-002 | Secret files MUST be created with restrictive permissions. | Critical | REQ-PRD-BASE-FUN-02 |

## 3. Secret Types & Generation Rules

All secrets are identified from root `docker-compose.yml`. Generation rules are based on how the value is consumed in compose/service configs.

### 3.1 Manual integration secrets (placeholder)

| Secret | File | Default Content | Notes |
| --- | --- | --- | --- |
| `slack_webhook` | `secrets/common/slack_webhook.txt` | `CHANGE_ME_SLACK_WEBHOOK_URL` | Required for Alertmanager Slack |
| `smtp_username` | `secrets/common/smtp_username.txt` | `CHANGE_ME_SMTP_USERNAME` | Required for Alertmanager SMTP |
| `smtp_password` | `secrets/common/smtp_password.txt` | `CHANGE_ME_SMTP_PASSWORD` | Required for Alertmanager SMTP |
| `supabase_openai_api_key` | `secrets/data/supabase_openai_api_key.txt` | `CHANGE_ME_OPENAI_API_KEY` | Optional feature in Supabase Studio |

`--strict` MUST fail if any `CHANGE_ME_*` placeholder remains.

### 3.2 Traefik BasicAuth (htpasswd usersFile)

- Secrets:
  - `traefik_basicauth_password`
  - `traefik_opensearch_basicauth_password`
- Format: `htpasswd -nbB admin "<password>"` output (bcrypt)
- Password generation: `openssl rand -hex 16`
- Output policy: password MUST be printed **only on first generation** (stderr) because it is not recoverable from bcrypt hashes.

### 3.3 Airflow Fernet key

- Secret: `airflow_fernet_key`
- Format: urlsafe base64 of 32 random bytes
- Generation: `python3 -c 'import base64,os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())'`

### 3.4 OAuth2 Proxy cookie secret

- Secret: `oauth2_proxy_cookie_secret`
- Format: base64-encoded 32 random bytes
- Generation: `python3 -c 'import base64,os; print(base64.b64encode(os.urandom(32)).decode())'`

### 3.5 Supabase derived JWT keys (HS256)

- Input: `supabase_jwt_secret` (generated as a random URL-safe string)
- Derived:
  - `supabase_anon_key`: HS256 JWT with role `anon`
  - `supabase_service_key`: HS256 JWT with role `service_role`
- Required claims:
  - `role`, `aud="authenticated"`, `iat`, `exp` (10 years)
- Implementation: bash base64url + `openssl dgst -sha256 -hmac` (no external JWT libraries).

### 3.6 Default secret generation

- Default: `openssl rand -hex 32`
- Exception:
  - `n8n_encryption_key`: `openssl rand -hex 16`
  - `supabase_secret_key_base`: `python3 -c 'import secrets; print(secrets.token_urlsafe(64))'`
  - `minio_app_username`: from env var `MINIO_APP_USERNAME` (prefer `.env`, fallback `.env.example`, else `minio_user`)
  - `minio_root_username`: fixed `minio_root`

## 4. Interfaces

### 4.1 CLI

`scripts/bootstrap-secrets.sh` MUST implement:

- `--env-file <path>`
- `--compose-file <path>`
- `--dry-run`
- `--force`
- `--strict`
- `--only <secret_name>`
- `--list`
- `--validate-compose`

Exit codes:
- `0`: success
- `1`: invalid args/prereqs or strict validation failure

## 5. Edge Cases & Error Handling

- Missing `openssl` / `python3` / `htpasswd` MUST result in a clear error and exit `1`.
- Secrets with missing `file:` path MUST be reported and skipped (error in `--validate-compose` mode).
- Existing secrets MUST NOT be overwritten unless `--force` is set.

## 6. Verification Plan (Static)

- `bash scripts/bootstrap-secrets.sh --env-file .env.example --validate-compose`
- `bash scripts/bootstrap-secrets.sh --env-file .env.example --strict` (after manual placeholders are replaced)

## 9. Operations & Security

- Secrets are stored only in `secrets/**/*.txt` and injected at runtime as `/run/secrets/*`.
- The script MUST avoid printing secrets, and MUST create files with restrictive permissions (0600).
