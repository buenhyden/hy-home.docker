---
layer: agentic
runtime: codex
---

# Codex Provider Notes

Codex-specific guidance for this repository.

## 1. Context and Objective

- Keep Codex execution aligned with repository governance.
- Use `AGENTS.md` as the shared entry point for Codex sessions.
- Keep `.codex/` limited to Codex runtime hooks and local context wiring.

## 2. Provider-Specific Rules

- Do not create a root `CODEX.md`; Codex reads the repo entry contract from `AGENTS.md`.
- Keep provider-neutral behavior in `providers/agents-md.md` and shared rules.
- Treat `.codex/hooks.json` as runtime context support, not as a policy source of truth.
- Use `RTK.md` for the repository's token-optimized shell command convention when applicable.
- Do not store secrets, tokens, credentials, personal settings, or shell history under `.codex/`.
- Respect the active sandbox and approval model before mutating files or running high-risk commands.

## 3. Recommended Loading Sequence

1. `AGENTS.md`
2. `docs/00.agent-governance/providers/agents-md.md`
3. `docs/00.agent-governance/providers/codex.md`
4. bootstrap -> persona -> checklists -> one scope -> JIT stage docs
5. `rules/github-governance.md` for PR / merge / review tasks

## 4. Runtime Surface

- `.codex/hooks.json` provides Codex-local hooks.
- The current hooks call `scripts/hooks/agent-event-hook.sh` by event (`SessionStart`, `PreToolUse`, `PostToolUse`, `SessionEnd`, `Stop`, `PreCompact`) when the runtime supports that event.
- The event dispatcher emits Graphify context when `graphify-out/graph.json` exists, emits Docker Compose guardrail context before matching edits, emits README template/readiness guidance before README edits, and delegates post-edit formatting and style validation to `scripts/hooks/post-tool-validate.sh`.
- Hook output is advisory context. Governance remains in `docs/00.agent-governance/`.
- Codex does not maintain a parallel delegated-agent catalog in this repository.
- The canonical delegated-agent catalog is the `.claude` runtime catalog
  documented in `docs/00.agent-governance/agents/` and
  `docs/00.agent-governance/subagent-protocol.md`.

## 5. Hook Parity Contract

- Codex hook events must stay behaviorally aligned with Claude hook events where both runtimes support the event.
- `SessionStart`, `PreToolUse`, `PostToolUse`, `SessionEnd`, `Stop`, and `PreCompact` route through `scripts/hooks/agent-event-hook.sh`.
- Codex `PreToolUse` and `PostToolUse` matchers must cover normal file edits and patch-based edits, including `Write`, `Edit`, `MultiEdit`, `apply_patch`, and `ApplyPatch`.
- Codex hooks must surface template-first guidance before target-stage documentation edits, README template/readiness guidance before README edits, block Stop when changed target-stage docs fail `bash scripts/validation/check-repo-contracts.sh`, and block Stop while task-owned uncommitted paths remain after repository-modifying work.
- README guidance must remain provider-neutral: folder-index README edits route to `docs/99.templates/readme.template.md`, and infra service leaf README edits require Service Readiness evidence without reading secret values.
- Runtime hooks provide advisory context and validation routing only. Policy remains in `docs/00.agent-governance/`.

## 6. Operational Practices

- Keep root files concise and delegate detailed policy to governance docs.
- Prefer repository-local checks over user-global configuration changes.
- Do not mutate user-global `~/.codex` unless explicitly requested.
- Keep `.codex/README.md` synchronized with any tracked `.codex/` runtime files.

## Related Documents

- `AGENTS.md`
- `RTK.md`
- `.codex/README.md`
- `.codex/hooks.json`
- `.claude/CLAUDE.md`
- `docs/00.agent-governance/agents/`
- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `scripts/hooks/agent-event-hook.sh`
- `scripts/hooks/post-tool-validate.sh`
