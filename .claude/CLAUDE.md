---
layer: agentic
runtime: claude
---

# Claude Runtime Bootstrap

Claude runtime instructions for `hy-home.docker`.
This file keeps Claude-specific runtime routing local to `.claude/` while the shared governance source of truth remains in `AGENTS.md` and `docs/00.agent-governance/`.

## Runtime Imports

@../AGENTS.md
@../docs/00.agent-governance/providers/claude.md

## Local Runtime Structure

- Runtime supervisor: `.claude/agents/workflow-supervisor.md` (`model: opus`)
- Domain agents: `.claude/agents/*.md` (8 workers, `model: sonnet`)
- Runtime skills: `.claude/skills/<skill>/skill.md` (18 skills)
- Runtime hooks: `.claude/hooks/*.sh` dispatch to `scripts/hooks/agent-event-hook.sh`
- Hookify rules: `.claude/hookify.*.local.md` keep Hookify's `.local.md` naming but are tracked team-shared rules in this repository, not personal overrides.
- Shared team permissions: `.claude/settings.json`

## Execution Rules

- `workflow-supervisor` owns orchestration, routing, and final coordination.
- All domain/task agents remain specialized workers and use `model: sonnet`.
- Runtime skills are invoked from their nested canonical paths only.
- In Claude Code, use the delegated-agent facility and pass the primary scope path explicitly.
- Keep runtime behavior aligned with `docs/00.agent-governance/agents/` and `docs/00.agent-governance/subagent-protocol.md`.

## Related Documents

- `../AGENTS.md`
- `../CLAUDE.md`
- `../docs/00.agent-governance/README.md`
- `../docs/00.agent-governance/subagent-protocol.md`
