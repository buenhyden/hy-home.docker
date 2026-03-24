---
layer: agentic
---

# AGENTS.md

**Canonical working contract for all AI agents in `hy-home.docker`.**

`hy-home.docker` is a modular, self-hosted platform stack. This file establishes the base protocol for all AI interactions.

## 1. Identity Protocol (Always Load First)
- **Primary Hub**: Always load **[docs/00.agent/README.md](docs/00.agent/README.md)** at the start of every session to establish identity and governance.
- **Provider Context**: Load the matching provider file (e.g., `docs/00.agent/claude-provider.md`) for specialized tool/memory guidance.

## 2. Operating Protocol (Always, Ask, Never)

### ALWAYS
- Refer to the **[Gateway Dispatcher](docs/00.agent/README.md)** for session-specific context.
- Run `bash scripts/validate-docker-compose.sh` before any infrastructure changes.
- Use relative paths for all documentation links.
- Follow the established documentation taxonomy (01~99).

### ASK FIRST
- Before creating new top-level directories.
- Before introducing new major dependencies.
- Before executing potentially destructive shell commands.

### NEVER
- Commit secrets or `.env` files to version control.
- Modify infrastructure without prior validation.
- Bypass the documentation governance defined in `docs/00.agent/`.

## 3. Lazy-Loading Dispatcher
Use the following markers to load specialized rules JIT:
- `[LOAD:RULES:BOOTSTRAP]` — Core governance, taxonomy, and standards.
- `[LOAD:RULES:PERSONA]` — Persona-based task matrix.


## 4. Governance
All agent governance, persona mappings, and behavioral standards are defined in **[docs/00.agent/](docs/00.agent/README.md)**.
