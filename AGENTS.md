---
layer: agentic
---

# AGENTS.md

**Universal Working Contract for all AI Agents in `hy-home.docker`.**

## 1. Entry Point & Governance

This project implements a single-source-of-truth governance model based on the **Stage-Gate Taxonomy (01-11)**.

1. **Identity Hub**: Establish identity and load core rules from **[docs/00.agent-governance/README.md](docs/00.agent-governance/README.md)**.
2. **Persona Protocol**: Adopt the required specialist persona via `[LOAD:RULES:PERSONA]`.
3. **Language Protocol**:

   - **Governance**: READ/WRITE all internal 00-11 stage-gate docs in **English**.
   - **Interaction**: ALWAYS respond to the USER in **Korean** via `notify_user` or chat.

## 2. Operating Constraints

- Relative Paths: Always use relative paths; never use `file://` URIs or absolute paths.
- Validation: Architectural changes MUST pass `scripts/validate-docker-compose.sh`.
- Security: Never commit secrets. Adhere to **[rules/security.md](docs/00.agent-governance/scopes/security.md)**.
- Lazy Loading: If context is missing, use JIT markers (e.g., `[LOAD:PRD]`, `[LOAD:SPEC]`).

## 3. Primary Dispatcher

For detailed technical scopes, refer to **`docs/00.agent-governance/scopes/`**.
