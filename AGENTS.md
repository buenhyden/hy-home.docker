---
layer: agentic
---

# AGENTS.md

Universal working contract for all coding agents in `hy-home.docker`.

## Entry Protocol

1. Load `[LOAD:RULES:BOOTSTRAP]` from `docs/00.agent-governance/rules/bootstrap.md`.
2. Load `[LOAD:RULES:PERSONA]` from `docs/00.agent-governance/rules/persona.md`.
3. Identify task layer and load exactly one primary scope from `docs/00.agent-governance/scopes/`.
4. Use JIT loading for stage docs in `docs/01` to `docs/11` plus `docs/90` and `docs/99` only when needed.

## Mandatory Constraints

- Keep root instruction files thin; put detailed rules in `docs/00.agent-governance`.
- Treat `docs/01` to `docs/99` as project SSoT; do not mutate those stages unless explicitly requested.
- Run all relevant programmatic checks listed by the active scope/rules before completion.
- If multiple instruction files apply by directory depth, the most specific in-scope file wins.
- System, developer, and direct user instructions always override repository instruction files.

## Canonical References

- Governance hub: `docs/00.agent-governance/README.md`
- Shared standards: `docs/00.agent-governance/rules/standards.md`
- Quality/security gate: `docs/00.agent-governance/rules/quality-standards.md`
- Git workflow: `docs/00.agent-governance/rules/git-workflow.md`
