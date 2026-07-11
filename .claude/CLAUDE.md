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
- Domain agents: `.claude/agents/*.md` (14 workers, `model: sonnet`)
- Runtime skills: `.claude/skills/<skill>/skill.md` (22 skills)
- Output style: `.claude/output-styles/hy-home.md` (implements `rules/output-style.md`; set in `settings.json`)
- Runtime hooks: `.claude/hooks/*.sh` dispatch to `scripts/hooks/agent-event-hook.sh`
- Hookify rules: `.claude/hookify.*.local.md` keep Hookify's `.local.md` naming but are tracked team-shared rules in this repository, not personal overrides.
- Shared team permissions: `.claude/settings.json`

## Execution Rules

- `workflow-supervisor` owns orchestration, routing, and final coordination.
- All domain/task agents remain specialized workers and use `model: sonnet`.
- Runtime skills are invoked from their nested canonical paths only.
- In Claude Code, use the delegated-agent facility and pass the primary scope path explicitly.
- Keep runtime behavior aligned with `docs/00.agent-governance/agents/` and `docs/00.agent-governance/subagent-protocol.md`.
- For changed or new target Markdown, run
  `python3 scripts/validation/check-document-metadata.py --mode check-changed`
  with a safe comparison base.
- Direct agent execution of all-files pre-commit is prohibited. At an approved
  final QA gate, use only
  `scripts/validation/run-agent-precommit-all-files.sh` and record the reviewed
  Git-visible, non-ignored repository paths in Stage 04 evidence.

## Related Documents

- `../AGENTS.md`
- `../CLAUDE.md`
- `../docs/00.agent-governance/README.md`
- `../docs/00.agent-governance/subagent-protocol.md`
