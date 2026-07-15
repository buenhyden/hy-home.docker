---
layer: agentic
runtime: claude
---

# Claude Provider Notes

Claude Code-specific guidance for this repository.

## 1. Context and Objective

- Keep Claude execution aligned with repository governance.
- Keep `CLAUDE.md` minimal and modular.

## 2. Provider-Specific Rules

- Keep direct bootstrap, provider, and memory imports in root `CLAUDE.md`.
- Keep provider-neutral behavior in `providers/agents-md.md` and shared rules.
- Use `@path` imports for modular instruction loading.
- Use project memory hierarchy intentionally (enterprise/project/local) and avoid duplicating the same rule across layers.
- Keep canonical Hookify rules at
  `docs/00.agent-governance/rules/hooks/hookify.*.md`. The repository does not
  yet track a Claude-local Hookify projection; do not cite or create one until
  the registered provider renderer owns it.
- Claude exposes provider-native Markdown adapters for the Stage 00 canonical
  agent and function catalog (`providers/agents-md.md` §5). `.claude/agents/`
  and `.claude/skills/` are runtime adapters, not separate governance.
- Apply the Model Policy (`subagent-protocol.md`): `workflow-supervisor` uses `opus-4.8`, all worker agents use `sonnet-4.6`.
- Define the Claude-native output style under `.claude/output-styles/` implementing `rules/output-style.md`, and follow `rules/provider-capability-matrix.md` and `rules/workflows.md`.

## 3. Root Import Boundary

The root `CLAUDE.md` owns the executable import list. It loads bootstrap, this
provider overlay, the memory index, and progress in that order; do not copy the
list into another governance surface.

## 4. Instruction Precedence (Claude-Specific)

Claude Code loads instruction files in a defined precedence order. Within this repository:

- `CLAUDE.md` is the root shim; it imports bootstrap, this overlay, and memory.
- `docs/00.agent-governance/` governance files are the policy SSOT and override provider defaults.
- `.claude/` is the Claude runtime baseline.
- `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`, and `.claude/skills/` are the runtime enforcement layer for Claude-specific behavior.
- Claude agents and skills must maintain catalog parity with `docs/00.agent-governance/agents/`.
- The `.agents/` directory is the cross-provider compatibility and shared-skill
  surface, distinct from Claude-native `.claude/` and Gemini-native `.gemini/`.
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
- README guidance must remain provider-neutral: folder-index README edits route to `docs/99.templates/templates/common/readme.template.md`, and infra service leaf README edits require Service Readiness evidence without reading secret values.
- Runtime hooks provide advisory context and validation routing only. Policy remains in `docs/00.agent-governance/`.

## 6. Operational Practices

- Keep instructions short, specific, and executable.
- Prefer path-scoped instruction files instead of large monolithic root files.
- For changed or new target Markdown, run
  `python3 scripts/validation/check-document-metadata.py --mode check-changed`
  with the task's safe comparison base. Claude hooks may surface validation
  guidance, but the command result is the evidence boundary.
- Direct agent execution of all-files pre-commit is prohibited. At the approved
  final QA gate, use only
  `scripts/validation/run-agent-precommit-all-files.sh` and record the reviewed
  Git-visible, non-ignored repository paths in Stage 04 evidence.
- After instruction updates, start a fresh run or reload context so new guidance is effective.

## Related Documents

- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `scripts/hooks/agent-event-hook.sh`
- `scripts/hooks/post-tool-validate.sh`

## References

- <https://docs.anthropic.com/en/docs/claude-code/memory>
