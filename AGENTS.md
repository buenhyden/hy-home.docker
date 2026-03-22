---
layer: agentic
---

# AGENTS.md

**Canonical working contract for all AI agents in `hy-home.docker`.**

`hy-home.docker` is a modular, self-hosted platform stack built on Docker Compose `include` files and profiles. This repository serves as the primary orchestration layer for local and homelab infrastructure.

## 1. Technical Prerequisites

Before executing any commands, verify the following are installed and configured:

- **Docker Engine**: 24.x+
- **Docker Compose**: v2.20+
- **Host Tools**: `bash`, `git`, `mkcert`, `python3`, `openssl`
- **FS Policy**: On WSL2, the repository MUST stay inside the Linux filesystem (non-NTFS).

## 2. Day 1 Commands (Setup & Validation)

Copy-paste ready commands for common bootstrap stages:

| Phase | Command | Purpose |
| --- | --- | --- |
| **Setup** | `cp .env.example .env` | Initialize environment defaults |
| **Certs** | `bash scripts/generate-local-certs.sh` | Bootstrap local TLS (mkcert) |
| **Secrets** | `bash scripts/bootstrap-secrets.sh` | Generate file-backed Docker secrets |
| **Validate** | `bash scripts/validate-docker-compose.sh` | Pre-deploy configuration check |
| **Preflight**| `bash scripts/preflight-compose.sh` | Runtime prerequisite check |
| **Execute** | `docker compose up -d` | Bring up default profiles |

## 3. Rule Triggers

Identify your task and load the required rule module via [Discovery Hub](docs/agentic/gateway.md):

- **Refactoring**: `[LOAD:RULES:REFACTOR]`
- **Documentation**: `[LOAD:RULES:DOCS]`
- **Infrastructure**: `[LOAD:RULES:INFRA]`
- **Operations**: `[LOAD:RULES:OPS]`

## 4. Execution Baseline

1. **Load Gateway**: ALWAYS load [docs/agentic/gateway.md](docs/agentic/gateway.md) at session start.
2. **Skill Autonomy**: Use any tool in your bundle. No skills are restricted.
3. **Draft Plans**: Use pluralized paths for implementation plans ([docs/plans/](docs/plans/)).
4. **Validation**: NEVER update infrastructure without running `bash scripts/validate-docker-compose.sh`.
5. **Safety & Ethics**: Adhere to [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) standards.
