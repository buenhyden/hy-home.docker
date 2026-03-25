---
layer: agentic
---

# AGENTS.md

**Universal Working Contract for all AI Agents in `hy-home.docker`.**

## 1. Governance & Entry Point

This project uses a **Stage-Gate Taxonomy (01-11)** for documentation and governance.

- **Central Hub**: [docs/00.agent-governance/README.md](docs/00.agent-governance/README.md)
- **Core Rules**: [docs/00.agent-governance/rules/bootstrap.md](docs/00.agent-governance/rules/bootstrap.md)
- **Persona Protocol**: Load via `[LOAD:RULES:PERSONA]` from `docs/00.agent-governance/rules/persona-matrix.md`.

## 2. Language & Response Policy

- **Documentation**: All internal governance and agent-facing docs MUST be in **English**.
- **Interaction**: ALWAYS respond to the **USER** in **Korean** (via `notify_user` or chat).
- **Human-Facing Docs**: `docs/` READMEs and guides are in **Korean** for human readability.

## 3. Operating Constraints

- **Paths**: Use relative paths only; no `file://` or absolute URIs.
- **Validation**: Architectural changes must pass `scripts/validate-docker-compose.sh`.
- **Security**: No secrets in code. Refer to [security.md](docs/00.agent-governance/scopes/security.md).
- **Lazy Loading**: Use JIT markers (e.g., `[LOAD:PRD]`, `[LOAD:SPEC]`) to ingest context from `docs/01-11`.

## 4. Technical Scopes

For detailed constraints by layer, refer to:
- [Architecture](docs/00.agent-governance/scopes/architecture.md)
- [Backend](docs/00.agent-governance/scopes/backend.md)
- [Frontend](docs/00.agent-governance/scopes/frontend.md)
- [Infrastructure](docs/00.agent-governance/scopes/infra.md)
- [Documentation](docs/00.agent-governance/scopes/docs.md)
