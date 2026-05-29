# Gemini Shared Runtime & Compatibility Surface

This directory is the native runtime surface for Gemini agents and a compatibility surface for agent tooling that reads `.agents/` paths. It is not the source of truth for repository policy.

## Scope

### In Scope

- Gemini-specific rules under `rules/`
- Gemini-specific workflows under `workflows/`
- Gemini runtime skill implementations under `skills/`
- Gemini reference index under `agents/` pointing to the governance catalog

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
