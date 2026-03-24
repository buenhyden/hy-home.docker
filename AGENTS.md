---
layer: agentic
---

# AGENTS.md

**Canonical working contract for all AI agents in `hy-home.docker`.**

`hy-home.docker` is a modular, self-hosted platform stack. This file establishes the base protocol for all AI interactions.

## 1. Operating Protocol (Always, Ask, Never)

### ALWAYS

- Load the **[Agent Gateway](docs/00.agent/01.gateway.md)** at the start of every session.
- Run `bash scripts/validate-docker-compose.sh` before any infrastructure changes.
- Use relative paths for all documentation links.
- Follow the **[SDD/TDD documentation flow](docs/README.md)**.

### ASK FIRST

- Before creating new top-level directories.
- Before introducing new major dependencies.
- Before executing potentially destructive shell commands (e.g., `docker system prune`).

### NEVER

- Commit secrets or `.env` files to version control.
- Modify infrastructure without prior validation.
- Bypass the established documentation taxonomy (01~99).

## 2. Day 1 Commands

| Task | Command | Purpose |
| --- | --- | --- |
| **Setup** | `cp .env.example .env` | Initialize environment |
| **Certs** | `bash scripts/generate-local-certs.sh` | Bootstrap local TLS |
| **Validate** | `bash scripts/validate-docker-compose.sh` | Pre-deploy check |
| **Preflight**| `bash scripts/preflight-compose.sh` | Runtime check |
| **Execute** | `docker compose up -d` | Deploy stack |

## 3. Discovery & Lazy Loading

For specific tasks, use the **[Dispatcher](docs/00.agent/01.gateway.md)** to load the required rule modules:
- `[LOAD:RULES:REFACTOR]` — Doc/System Refactoring
- `[LOAD:RULES:DOCS]` — Documentation Maintenance
- `[LOAD:RULES:INFRA]` — Infrastructure Lifecycle
- `[LOAD:RULES:OPS]` — Operations & Incidents
