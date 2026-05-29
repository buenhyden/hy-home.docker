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
- Claude is the canonical runtime in the Provider Parity Model (`providers/agents-md.md` §5); `.claude/agents/` and `.claude/skills/` hold the full source content that Codex mirrors and Gemini points to.
- Apply the Model Policy (`subagent-protocol.md`): `workflow-supervisor` uses `opus-4.8`, all worker agents use `sonnet-4.6`.
- Define the Claude-native output style under `.claude/output-styles/` implementing `rules/output-style.md`, and follow `rules/provider-capability-matrix.md` and `rules/workflows.md`.

## 3. Recommended CLAUDE.md Import Sequence

The following `@`-imports belong in the root `CLAUDE.md` file. Step 3 refers to this file being loaded by `CLAUDE.md`, not a circular self-reference.

1. `@AGENTS.md`
2. `@docs/00.agent-governance/providers/agents-md.md`
3. `@docs/00.agent-governance/providers/claude.md`
4. bootstrap -> persona -> checklists -> one scope -> JIT stage docs
5. `rules/github-governance.md` for PR / merge / review tasks

## 4. Instruction Precedence (Claude-Specific)

Claude Code loads instruction files in a defined precedence order. Within this repository:

- `CLAUDE.md` is the root shim; it delegates to `AGENTS.md` and provider overlays.
- `docs/00.agent-governance/` governance files are the policy SSOT and override provider defaults.
- `.claude/` is the Claude runtime baseline.
- `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`, and `.claude/skills/` are the runtime enforcement layer for Claude-specific behavior.
- Claude agents and skills must maintain catalog parity with `docs/00.agent-governance/agents/`.
- The `.agents/` directory acts as the cross-provider compatibility surface and Gemini shared surface, distinct from the Claude-specific `.claude/` runtime.
- `.claude/hooks/*.sh` are thin wrappers that dispatch hook events through `scripts/hooks/agent-event-hook.sh`.
- Claude `PreToolUse` Graphify advisory context and Docker Compose edit guardrails must route through the shared dispatcher, not inline shell snippets in `.claude/settings.json`.
- GitHub-native instruction files are not part of this repository's active instruction hierarchy.
- Personal `settings.local.json` may not override team policy in `settings.json`.

## 5. Hook Parity Contract

- Claude hook events must stay behaviorally aligned with Codex hook events where both runtimes support the event.
- `SessionStart`, `PreToolUse`, `PostToolUse`, `SessionEnd`, `Stop`, and `PreCompact` route through thin `.claude/hooks/*.sh` wrappers and then the provider-neutral dispatcher in `scripts/hooks/agent-event-hook.sh`.
- Claude `PreToolUse` and `PostToolUse` matchers must cover normal file edits and patch-based edits, including `Write`, `Edit`, `MultiEdit`, `apply_patch`, and `ApplyPatch`.
- Claude `PostToolUse` must delegate changed-file style normalization and style validation to `scripts/hooks/post-tool-validate.sh` before repository contract checks. The shared script trims text-file whitespace/newline drift, runs `shfmt` for changed hook/script shell files when available, and runs optional `shellcheck`/`yamllint` style checks when those tools are available.
- Claude hooks must surface template-first guidance before target-stage documentation edits, README template/readiness guidance before README edits, and block Stop when changed target-stage docs fail `bash scripts/validation/check-repo-contracts.sh`.
- Claude Stop/SessionEnd guidance must require agents to create logical Conventional Commits for completed repository-modifying work unless a higher-priority instruction or incomplete verification prevents committing; Stop blocks while task-owned uncommitted paths remain.
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
