# Gemini Shared Runtime & Compatibility Surface

This directory is the native runtime surface for Gemini agents and a compatibility surface for agent tooling that reads `.agents/` paths. It is not the source of truth for repository policy.

## Scope

### In Scope

- Gemini reference index under `agents/` pointing to the governance agent catalog
- Gemini reference index under `skills/` pointing to the governance function catalog

Per the Provider Parity Model (`docs/00.agent-governance/providers/agents-md.md` §5),
both `agents/` and `skills/` are pointer-only reference indexes. Gemini rules and
workflows are not duplicated here; they live in `docs/00.agent-governance/` and are
followed as behavioral contracts.

### Out of Scope

- Active policy that belongs in `docs/00.agent-governance/`
- Parallel disconnected agent catalogs (must link to `docs/00.agent-governance/agents/`)
- Secrets, tokens, credentials, shell history, or logs

## Authority

- Policy source of truth: `docs/00.agent-governance/`
- Runtime agent/function source of truth: `docs/00.agent-governance/agents/`
- Claude runtime surface: `.claude/` (agents: `.claude/agents/`, skills: `.claude/skills/`)
- Codex hook/context surface: `.codex/`
- Gemini runtime surface: `.agents/` (this directory)

If a `.agents/skills/<name>/skill.md` file exists, it must stay functionally compatible with the corresponding provider-neutral governance function. It must not point to nonexistent runtime paths.

## How to Work in This Area

1. Update canonical governance and runtime files first.
2. Keep `.agents/` references aligned with `docs/00.agent-governance/`.
3. Run `bash scripts/validation/check-repo-contracts.sh` after edits.

## Related Documents

- [Agent governance hub](../docs/00.agent-governance/README.md)
- [Subagent protocol](../docs/00.agent-governance/subagent-protocol.md)
- [Claude runtime bootstrap](../.claude/CLAUDE.md)
- [Codex runtime surface](../.codex/README.md)
