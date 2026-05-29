---
layer: agentic
---

# Gemini Provider Notes

Gemini CLI-specific guidance for this repository.

## 1. Context and Objective

- Keep Gemini context loading predictable and token-efficient.
- Align Gemini behavior with shared governance in `AGENTS.md` and `docs/00.agent-governance`.

## 2. Provider-Specific Rules

- Keep root `GEMINI.md` thin and import shared governance.
- Prefer hierarchical context loading over broad static context.
- Recommended `.gemini/settings.json` configuration:
  - `"context.fileName": ["GEMINI.md", "AGENTS.md"]`

## 3. Recommended Loading Sequence

1. `@AGENTS.md`
2. `@docs/00.agent-governance/providers/agents-md.md`
3. `@docs/00.agent-governance/providers/gemini.md`
4. bootstrap -> persona -> checklists -> one scope -> JIT stage docs
5. `rules/github-governance.md` for PR / merge / review tasks

## 4. Instruction Precedence (Gemini-Specific)

Gemini merges context from multiple files. Within this repository:

- `GEMINI.md` is the root shim; it delegates to `AGENTS.md` and provider overlays.
- `docs/00.agent-governance/` governance files are the policy SSOT and override Gemini defaults.
- `.agents/` is Gemini's shared surface and reference-index shim; it holds pointer-only agent and skill indexes, while rules and workflows remain in governance.
- `.agents/agents/` provides the Gemini reference index to the governance agent catalog.
- GitHub-native instruction files are not part of this repository's active instruction hierarchy.

## 5. Runtime Surface

Per the Provider Parity Model (`providers/agents-md.md` §5), Gemini uses a
reference-index model — no full duplication and no provider-local policy directories.

- `.agents/` is Gemini's shared runtime surface and reference-index shim.
- `.agents/agents/<name>.md` are reference-index pointers to `docs/00.agent-governance/agents/agents/`.
- `.agents/skills/<name>/skill.md` are reference-index pointers to `docs/00.agent-governance/agents/functions/`.
- `.agents/` contains no `rules/` or `workflows/` directories; Gemini rules and workflows live in governance (`rules/`, `rules/workflows.md`) and are followed as behavioral contracts.
- Gemini agent model identifiers follow the Model Policy in `subagent-protocol.md` (supervisor `gemini-3.1-pro`, worker `gemini-3.5-flash`).
- The `.agents/` directory is git-tracked.

## 6. Hook Parity Contract

- Gemini follows the shared `rules/output-style.md`, `rules/provider-capability-matrix.md`, and `rules/workflows.md` as behavioral contracts.
- While Gemini CLI does not natively support the same programmatic hooks as Claude or Codex, Gemini agents MUST manually follow the same behavioral contracts documented for hooks.
- **Pre-edit validation**: Review requirements and guardrails before mutating files.
- **Post-edit validation**: Validate style (formatting, trimming) and run repository contract checks before declaring completion.
- **Template-first guidance**: Use `docs/99.templates/` before creating new target-stage documentation.
- **Commit discipline**: Create logical Conventional Commits for completed repository-modifying work.
- **README guidance**: Follow the provider-neutral README readiness rules.

## 7. Operational Practices

- Use `/memory list` to inspect loaded context files.
- Use `/memory show` to inspect merged effective context.
- Use `/memory refresh` after editing instruction files.
- Keep imports explicit and remove stale references quickly.

## Related Documents

- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `.agents/README.md`

## References

- <https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html>
- <https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html>
- <https://google-gemini.github.io/gemini-cli/docs/cli/commands.html>
