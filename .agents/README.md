# Agents Compatibility Surface

This directory is a compatibility surface for agent tooling that reads
`.agents/` paths. It is not the source of truth for repository policy or the
delegated agent/function catalog.

## Scope

### In Scope

- Local compatibility rules under `rules/`
- Local compatibility workflows under `workflows/`
- Optional compatibility skill copies under `skills/`

### Out of Scope

- Active policy that belongs in `docs/00.agent-governance/`
- A parallel runtime agent catalog
- Secrets, tokens, credentials, shell history, or logs

## Authority

- Policy source of truth: `docs/00.agent-governance/`
- Runtime agent/function source of truth: `.claude/agents/` and `.claude/skills/`
- Codex hook/context surface: `.codex/`

If a `.agents/skills/<name>/skill.md` file exists, it must stay compatible with
the corresponding `.claude/skills/<name>/skill.md` contract. It must not point
to nonexistent runtime paths such as `.Codex/`.

## How to Work in This Area

1. Update canonical governance and runtime files first.
2. Keep `.agents/` references aligned with `.claude/` and `docs/00.agent-governance/`.
3. Run `bash scripts/validation/check-repo-contracts.sh` after edits.

## Related Documents

- [Agent governance hub](../docs/00.agent-governance/README.md)
- [Subagent protocol](../docs/00.agent-governance/subagent-protocol.md)
- [Claude runtime bootstrap](../.claude/CLAUDE.md)
- [Codex runtime surface](../.codex/README.md)
