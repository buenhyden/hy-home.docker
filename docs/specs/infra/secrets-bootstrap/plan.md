---
goal: 'Bootstrap file-based Docker secrets for first-time local setup.'
version: '1.0'
date_created: '2026-02-27'
last_updated: '2026-02-27'
owner: 'Platform / DevOps'
status: 'Implementation'
tags: ['implementation', 'planning', 'infra', 'secrets', 'bootstrap']
stack: 'python'
---

# Infra Secrets Bootstrap Implementation Plan

> **Status**: Implementation
> **Reference Spec**: [Infra Secrets Bootstrap Spec](/specs/infra/secrets-bootstrap/spec.md)

_Target Directory: `specs/infra/secrets-bootstrap/plan.md`_

## 1. Context

This repository enforces Secrets-First policy (Docker secrets mounted as files under `/run/secrets/*`). New contributors need a deterministic bootstrap that creates all required `secrets/**/*.txt` files referenced by the root `docker-compose.yml` without leaking values to stdout/stderr.

## 2. Goals

- Provide an idempotent script to generate all secret files declared in root `docker-compose.yml` (`secrets:` section).
- Generate secrets in correct formats where required (htpasswd, Airflow Fernet key, Supabase JWT keys).
- Keep manual integration secrets as placeholders + warnings (non-strict), and enforce via `--strict` (strict).
- Optionally validate Compose statically via `docker compose config -q`.

## 3. Non-Goals

- Do not start containers or require a running Docker daemon.
- Do not modify service compose files or introduce new secret sources (no `.env` secret injection).
- Do not print secret values (except Traefik BasicAuth password on first generation as an explicit exception).

## 4. Work Breakdown

| Task | Description | Files Affected | Validation |
| ---- | ----------- | -------------- | ---------- |
| TASK-001 | Add spec + plan | `specs/infra/secrets-bootstrap/{spec.md,plan.md}` | Markdown review |
| TASK-002 | Implement script | `scripts/bootstrap-secrets.sh` | `--list`, `--dry-run`, `--only`, `--strict` |
| TASK-003 | Update docs | `secrets/README.md`, `scripts/README.md`, `README.md` | Doc links + consistency |
| TASK-004 | Static verification | N/A | `bash scripts/bootstrap-secrets.sh --env-file .env.example --validate-compose` |

## 5. Verification Plan

| ID | Level | Command | Pass Criteria |
| --- | --- | --- | --- |
| VAL-SEC-001 | Static | `bash scripts/bootstrap-secrets.sh --env-file .env.example --validate-compose` | Exit `0` |
| VAL-SEC-002 | Static | `bash scripts/bootstrap-secrets.sh --env-file .env.example --strict` | Exit `0` when placeholders replaced |
| VAL-SEC-003 | Idempotency | Run `bash scripts/bootstrap-secrets.sh` twice | Second run reports “unchanged” |

## 6. References

- PRD: `/docs/prd/infra-baseline-prd.md`
- ADR: `/docs/adr/adr-0002-secrets-first-management.md`
- Secrets registry: `/secrets/README.md`
