---
layer: agentic
---

# CLAUDE.md

Claude-specific operational triggers and guidance for `hy-home.docker`.

## 1. Core Contract

AI agents MUST follow the primary technical contract and "Day 1" commands defined in [AGENTS.md](AGENTS.md).

## 2. Common Commands

| Task | Command |
| --- | --- |
| **Validate** | `bash scripts/validate-docker-compose.sh` |
| **Preflight** | `bash scripts/preflight-compose.sh` |
| **Certs** | `bash scripts/generate-local-certs.sh` |
| **Secrets** | `bash scripts/bootstrap-secrets.sh --env-file .env` |
| **Up** | `docker compose up -d` |
| **Logs** | `docker compose logs -f` |

## 3. Architecture & Gotchas

- **Tiered Structure**: Services are located in `infra/` organized by tier (01-10). The root `docker-compose.yml` includes these via `include`.
- **Validation-First**: ALWAYS run `bash scripts/validate-docker-compose.sh` before deployment. It handles dummy secrets for static analysis.
- **FS Policy**: Work strictly within the Linux filesystem (WSL2 requirement) to avoid permission/performance issues.

## 4. Rule Triggers

Identify your task and load the required rule module:

- **Refactoring**: `[LOAD:RULES:REFACTOR]` (Follows [March 2026 Standard](docs/adr/0003-2026-march-agentic-standard.md))
- **Documentation**: `[LOAD:RULES:DOCS]`
- **Infrastructure**: `[LOAD:RULES:INFRA]` (See [ARCHITECTURE.md](ARCHITECTURE.md))
- **Operations**: `[LOAD:RULES:OPS]` (See [OPERATIONS.md](OPERATIONS.md))
