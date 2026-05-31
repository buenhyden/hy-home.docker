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

## 4. Runtime Boundary

- `.codex/hooks.json` provides Codex-local hooks.
- `.codex/agents/` uses Codex-native TOML adapter definitions under
  `.codex/agents/*.toml`. The TOML files bind each Stage 00 agent role to a
  Codex model, reasoning effort, scope, and source catalog path.
- `.codex/agents/*.toml` is the Codex agent adapter surface. Do not define
  Codex-only roles, QA rules, Template Contract rules, or Model Policy values
  in TOML; those belong in Stage 00.
- `.codex/skills/` remains the Codex-compatible skill adapter surface and must
  stay aligned with the Stage 00 function catalog.
- Apply the Model Policy (`subagent-protocol.md`): `workflow-supervisor` uses
  `gpt-5.5` with `xhigh` reasoning effort; default worker agents use
  `gpt-5.4-mini` with `medium` reasoning effort. Never carry
  Anthropic model names (`opus-4.8`/`sonnet-4.6`) in `.codex/`.
- `gpt-5.3-codex` is reserved for a future explicit code-specialized worker override;
  do not use it until the sync script, validator, and policy table all encode the
  same exception.
- Follow the shared `rules/output-style.md`, `rules/provider-capability-matrix.md`, and `rules/workflows.md` as behavioral contracts.
- The canonical delegated-agent catalog is the provider-neutral catalog documented in `docs/00.agent-governance/agents/`.

## 5. QA/CI Tooling

Codex sandbox shells may not inherit the user's full interactive `PATH`. Before running local QA or CI commands, source the workspace tooling shim:

```bash
source scripts/operations/use-qa-ci-tools.sh
```

## 6. Current Hook Contract

- `SessionStart` uses `scripts/hooks/agent-event-hook.sh` to emit project context when the event is supported.
- `PreToolUse` emits Graphify advisory context, Docker Compose guardrails, and template-first guidance.
- `PostToolUse` delegates to `scripts/hooks/post-tool-validate.sh` after file edits for shell formatting, validation, and diff hygiene.
- `Stop` blocks completion when changed target-stage docs fail `check-repo-contracts.sh` or task-owned uncommitted paths remain.
- `SessionEnd` and `PreCompact` route through `agent-event-hook.sh` for lifecycle-safe advisory context.

## 7. Hook Parity Contract

- Codex hook events must stay behaviorally aligned with Claude hook events.
- Codex `PreToolUse` and `PostToolUse` matchers must cover normal file edits and patch-based edits including `apply_patch` and `ApplyPatch`.
- README guidance is provider-neutral (e.g. folder-index README edits route to `docs/99.templates/readme.template.md`).
- Runtime hooks provide advisory context and validation routing only. Policy remains in `docs/00.agent-governance/`.

## 8. Operational Practices

- Keep root files concise and delegate detailed policy to governance docs.
- Prefer repository-local checks over user-global configuration changes.
- Do not mutate user-global `~/.codex` unless explicitly requested.

## Related Documents

- `AGENTS.md`
- `RTK.md`
- `.codex/README.md`
- `.codex/hooks.json`
- `.claude/CLAUDE.md`
- `docs/00.agent-governance/agents/`
- `scripts/hooks/agent-event-hook.sh`
