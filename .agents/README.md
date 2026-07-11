# Gemini Shared Runtime & Compatibility Surface

This directory is the native runtime surface for Gemini agents and a compatibility surface for agent tooling that reads `.agents/` paths. It is not the source of truth for repository policy.

## Scope

### In Scope

- Gemini reference index under `agents/` pointing to the governance agent catalog
- Gemini reference index under `skills/` pointing to the governance function catalog
- Gemini-native Workspace Rules in `rules/`
- Gemini-native Workflows in `workflows/`

Per the Provider Parity Model (`docs/00.agent-governance/providers/agents-md.md` §5),
both `agents/` and `skills/` are pointer-only reference indexes. However, `.agents/` natively supports defining workspace-specific behavior in `rules/` and `workflows/` to fully leverage the Antigravity IDE.

### Out of Scope

- Core global policy that belongs in `docs/00.agent-governance/`
- Parallel disconnected agent catalogs (must link to `docs/00.agent-governance/agents/`)
- Secrets, tokens, credentials, shell history, or logs

## Authority

- Policy source of truth: `docs/00.agent-governance/`
- Runtime agent/function source of truth: `docs/00.agent-governance/agents/`
- Claude runtime surface: `.claude/` (agents: `.claude/agents/`, skills: `.claude/skills/`)
- Codex hook/context surface: `.codex/`
- Gemini runtime surface: `.agents/` (this directory)

If a `.agents/skills/<name>/skill.md` file exists, it must stay functionally compatible with the corresponding provider-neutral governance function. It must not point to nonexistent runtime paths.

## Provider Behavior

Gemini CLI provider-native hooks and agents are provider facts, but this
repository does not track a `.gemini` hook or agent adapter. This surface is a
behavioral pointer/reminder, not a tracked native hook adapter.

- For changed or new target Markdown, run
  `python3 scripts/validation/check-document-metadata.py --mode check-changed`
  with a safe comparison base.
- Direct agent execution of all-files pre-commit is prohibited. At an approved
  final QA gate, use only
  `scripts/validation/run-agent-precommit-all-files.sh` and record reviewed
  Git-visible, non-ignored repository paths in Stage 04 evidence.

## How to Work in This Area

1. Update canonical governance and runtime files first.
2. Regenerate this surface with `bash scripts/operations/sync-provider-surfaces.sh --write`.
3. Verify no drift with `bash scripts/operations/sync-provider-surfaces.sh --check`.

## Related Documents

- [Agent governance hub](../docs/00.agent-governance/README.md)
- [Subagent protocol](../docs/00.agent-governance/subagent-protocol.md)
- [Claude runtime bootstrap](../.claude/CLAUDE.md)
- [Codex runtime surface](../.codex/README.md)
