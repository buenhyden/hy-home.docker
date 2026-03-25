---
layer: agentic
---

# AGENTS.md

**Universal Working Contract for all AI Agents in `hy-home.docker`.**

## 1. Governance & Entry Point

This project uses a **Stage-Gate Taxonomy (01-11)** for documentation and governance.

- **Central Hub**: [docs/00.agent-governance/README.md](docs/00.agent-governance/README.md)
- **Bootstrap**: JIT load via `[LOAD:RULES:BOOTSTRAP]` from `docs/00.agent-governance/rules/bootstrap.md`.

## 2. Shared Directives

- **Language Policy**: Follow [language-policy.md](docs/00.agent-governance/rules/language-policy.md).
- **Git Workflow**: Follow [git-workflow.md](docs/00.agent-governance/rules/git-workflow.md).
- **Context Routing**: Load technical scopes from `docs/00.agent-governance/scopes/` JIT.

## 3. Compliance

Agents MUST verify all work against the [01-11 Stage-Gate Taxonomy](docs/README.md) and technical runbooks.
