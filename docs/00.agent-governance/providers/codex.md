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
- The current hook emits graphify context when `graphify-out/graph.json` exists.
- The post-edit hook delegates to `scripts/post-tool-validate.sh` for path-aware repository validation.
- Hook output is advisory context. Governance remains in `docs/00.agent-governance/`.

## 5. Operational Practices

- Keep root files concise and delegate detailed policy to governance docs.
- Prefer repository-local checks over user-global configuration changes.
- Do not mutate user-global `~/.codex` unless explicitly requested.
- Keep `.codex/README.md` synchronized with any tracked `.codex/` runtime files.

## Related Documents

- `AGENTS.md`
- `RTK.md`
- `.codex/README.md`
- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `scripts/post-tool-validate.sh`
