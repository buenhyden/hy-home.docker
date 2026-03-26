---
layer: agentic
---

# AGENTS.md

Universal entry shim for agent execution in `hy-home.docker`.

## Bootstrap Sequence

1. Load `[LOAD:RULES:BOOTSTRAP]` from `docs/00.agent-governance/rules/bootstrap.md`.
2. Load `[LOAD:RULES:PERSONA]` from `docs/00.agent-governance/rules/persona.md`.
3. Load `[LOAD:RULES:CHECKLISTS]` from `docs/00.agent-governance/rules/task-checklists.md`.
4. Resolve task layer and load exactly one primary scope from `docs/00.agent-governance/scopes/`.
5. For documentation authoring workflows, load `[LOAD:RULES:STAGE-MATRIX]` from `docs/00.agent-governance/rules/stage-authoring-matrix.md`.
6. Use JIT loading for stage docs (`docs/01` to `docs/11`, `docs/90`, `docs/99`) only when required by the active task.

## Hard Constraints

- Keep root instruction files thin; detailed policy must live in `docs/00.agent-governance/`.
- Treat `docs/01` to `docs/99` as read-only by default; modify only with explicit user instruction.
- Run relevant checks listed by active rules and scope before completion.
- If multiple instruction files apply, the most specific in-scope file wins.
- System, developer, and direct user instructions always override repository instruction files.

## Canonical Governance

- Hub: `docs/00.agent-governance/README.md`
- Shared standards: `docs/00.agent-governance/rules/standards.md`
- Documentation protocol: `docs/00.agent-governance/rules/documentation-protocol.md`
- Quality gate: `docs/00.agent-governance/rules/quality-standards.md`
- Git workflow: `docs/00.agent-governance/rules/git-workflow.md`
