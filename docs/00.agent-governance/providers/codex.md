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
- Treat ambiguity as blocking before Codex changes planning, implementation,
  model/reasoning values, hook/config state, or completion status.

## 3. Recommended Loading Sequence

1. `AGENTS.md`
2. `docs/00.agent-governance/providers/agents-md.md`
3. `docs/00.agent-governance/providers/codex.md`
4. bootstrap -> persona -> checklists -> one scope -> JIT stage docs
5. `rules/github-governance.md` for PR / merge / review tasks

## 4. Runtime Boundary

- `.codex/hooks.json` provides Codex-local hooks.
- `.codex/agents/` uses Codex-native TOML adapter definitions under
  `.codex/agents/*.toml`. Each strict adapter contains `name`, `description`,
  `developer_instructions`, `model`, `model_reasoning_effort`, and
  `sandbox_mode`; canonical scope, function, and catalog metadata stays in the
  typed Stage 00 contracts.
- `.codex/agents/*.toml` is the Codex agent adapter surface. Do not define
  Codex-only roles, QA rules, Template Contract rules, or Model Policy values
  in TOML; those belong in Stage 00.
- `.codex/agents/*.md` is retired. Do not recreate Codex Markdown agent prompts;
  Stage 00 plus validated `.codex/agents/*.toml` adapters are the Codex agent
  source of truth.
- Shared skill discovery uses `.agents/skills/*/SKILL.md`; `.codex/skills/` is
  not a separate policy or projection surface.
- Shared skills are rendered from typed Stage 00 function sources through
  `scripts/operations/sync-provider-surfaces.sh`; provider skill bodies are
  never used as policy input.
- Apply the model and reasoning selected by the agent's work profile in
  `contracts/provider-models.yaml`: GPT-5.6 for supervision and complex work,
  and GPT-5.6 Terra for read-heavy/repetitive work. OpenAI's raw status is
  `listed`, not `stable`; local entitlement and runtime acceptance still need
  revalidation. Never carry Anthropic or Gemini model names into `.codex/`.
- GPT-5.3 Codex Spark remains non-default preview/catalog context. It cannot be
  introduced as an override until the contract, renderer, validator, and task
  evidence all encode the same approved exception.
- `model` and `model_reasoning_effort` values are configuration outputs of the
  Stage 00 policy. Codex must not introduce new aliases, downgrade reasoning
  gates, or copy speculative model names from prompt context unless Stage 00,
  the provider sync script, and validators all permit the value.
- Follow the shared `rules/output-style.md`, `rules/provider-capability-matrix.md`, and `rules/workflows.md` as behavioral contracts.
- The canonical delegated-agent catalog is the provider-neutral catalog documented in `docs/00.agent-governance/agents/`.

## 5. QA/CI Tooling

Codex sandbox shells may not inherit the user's full interactive `PATH`. Before running local QA or CI commands, source the workspace tooling shim:

```bash
source scripts/operations/use-qa-ci-tools.sh
```

For each change type, Codex completion evidence must distinguish:

- local checks that were run,
- CI-only gates that must be observed remotely,
- hook or script evidence collected locally,
- skipped checks and the reason they are not applicable.

Docs-only and governance-only changes still require diff hygiene, repository
contracts, traceability checks, and provider sync when provider surfaces are
touched.

For changed or new target Markdown, run
`python3 scripts/validation/check-document-metadata.py --mode check-changed`
with a safe comparison base. Codex hooks provide routing and advisory context;
the checked command output is the validation evidence. Direct agent execution
of all-files pre-commit remains prohibited. At an approved final QA gate, use
only `scripts/validation/run-agent-precommit-all-files.sh` and record the
reviewed Git-visible, non-ignored repository paths in Stage 04 evidence.

## 6. Current Hook Contract

- `SessionStart` uses `scripts/hooks/agent-event-hook.sh` to emit project context when the event is supported.
- `PreToolUse` emits Graphify advisory context, Docker Compose guardrails, and template-first guidance.
- `PostToolUse` delegates to `scripts/hooks/post-tool-validate.sh` after file edits for shell formatting, validation, and diff hygiene.
- `Stop` blocks completion when changed target-stage docs fail `check-repo-contracts.sh` or task-owned uncommitted paths remain.
- `PreCompact` routes through `agent-event-hook.sh`. Codex does not expose the
  repository's `SessionEnd` semantic event, so no native `SessionEnd` entry is
  generated or counted as parity.
- `UserPromptSubmit` and `Stop` omit ignored matcher keys. Hook commands resolve
  the quoted project root so execution is robust from subdirectories and paths
  containing spaces.

## 7. Hook Parity Contract

- Codex hook events must stay behaviorally aligned with Claude hook events.
- Codex `PreToolUse` and `PostToolUse` matchers must cover normal file edits and patch-based edits including `apply_patch` and `ApplyPatch`.
- README guidance is provider-neutral (e.g. folder-index README edits route to `docs/99.templates/templates/common/readme.template.md`).
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
- `docs/01.requirements/024-agent-governance-standardization.md`
- `docs/02.architecture/requirements/0027-agent-governance-canonical-adapter.md`
- `docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md`
- `docs/00.agent-governance/agents/`
- `scripts/hooks/agent-event-hook.sh`

## References

- <https://learn.chatgpt.com/docs/agent-configuration/subagents>
- <https://learn.chatgpt.com/docs/hooks>
- <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
- <https://developers.openai.com/api/docs/models/gpt-5.6-terra>
