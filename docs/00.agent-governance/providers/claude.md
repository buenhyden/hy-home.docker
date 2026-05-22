---
layer: agentic
---

# Claude Provider Notes

Claude Code-specific guidance for this repository.

## 1. Context and Objective

- Keep Claude execution aligned with repository governance.
- Keep `CLAUDE.md` minimal and modular.

## 2. Provider-Specific Rules

- Keep `@AGENTS.md` at the top of root `CLAUDE.md`.
- Keep provider-neutral behavior in `providers/agents-md.md` and shared rules.
- Use `@path` imports for modular instruction loading.
- Use project memory hierarchy intentionally (enterprise/project/local) and avoid duplicating the same rule across layers.
- Keep `.claude/hookify.*.local.md` filenames for Hookify compatibility; in this repository those files are tracked team-shared rules, not personal local overrides.

## 3. Recommended Loading Sequence

1. `@AGENTS.md`
2. `@docs/00.agent-governance/providers/agents-md.md`
3. `@docs/00.agent-governance/providers/claude.md`
4. bootstrap -> persona -> checklists -> one scope -> JIT stage docs
5. `rules/github-governance.md` for PR / merge / review tasks

## 4. Instruction Precedence (Claude-Specific)

Claude Code loads instruction files in a defined precedence order. Within this repository:

- `CLAUDE.md` is the root shim; it delegates to `AGENTS.md` and provider overlays.
- `docs/00.agent-governance/` governance files are the policy SSOT and override provider defaults.
- `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`, and `.claude/skills/` are the runtime enforcement layer for Claude-specific behavior.
- `.claude/hooks/*.sh` are thin wrappers that dispatch hook events through `scripts/hooks/agent-event-hook.sh`.
- Claude `PreToolUse` Graphify advisory context and Docker Compose edit guardrails must route through the shared dispatcher, not inline shell snippets in `.claude/settings.json`.
- GitHub-native instruction files are not part of this repository's active instruction hierarchy.
- Personal `settings.local.json` may not override team policy in `settings.json`.

## 5. Hook Parity Contract

- Claude hook events must stay behaviorally aligned with Codex hook events where both runtimes support the event.
- `SessionStart`, `PreToolUse`, `PostToolUse`, `SessionEnd`, `Stop`, and `PreCompact` route through thin `.claude/hooks/*.sh` wrappers and then the provider-neutral dispatcher in `scripts/hooks/agent-event-hook.sh`.
- Claude `PreToolUse` and `PostToolUse` matchers must cover normal file edits and patch-based edits, including `Write`, `Edit`, `MultiEdit`, `apply_patch`, and `ApplyPatch`.
- Claude `PostToolUse` must delegate changed-file style normalization and style validation to `scripts/hooks/post-tool-validate.sh` before repository contract checks.
- Claude hooks must surface template-first guidance before target-stage documentation edits, README template/readiness guidance before README edits, and block Stop when changed target-stage docs fail `bash scripts/validation/check-repo-contracts.sh`.
- Claude Stop/SessionEnd guidance must remind agents to create logical Conventional Commits for completed repository-modifying work unless a higher-priority instruction or incomplete verification prevents committing.
- README guidance must remain provider-neutral: folder-index README edits route to `docs/99.templates/readme.template.md`, and infra service leaf README edits require Service Readiness evidence without reading secret values.
- Runtime hooks provide advisory context and validation routing only. Policy remains in `docs/00.agent-governance/`.

## 6. Operational Practices

- Keep instructions short, specific, and executable.
- Prefer path-scoped instruction files instead of large monolithic root files.
- After instruction updates, start a fresh run or reload context so new guidance is effective.

## Related Documents

- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `scripts/hooks/agent-event-hook.sh`
- `scripts/hooks/post-tool-validate.sh`

## References

- <https://docs.anthropic.com/en/docs/claude-code/memory>
