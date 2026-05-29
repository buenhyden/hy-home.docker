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
- `.agents/` is Gemini's shared surface and moderate-shim, where Gemini-specific rules, workflows, and skills reside.
- `.agents/agents/` provides the Gemini reference index to the governance agent catalog.
- GitHub-native instruction files are not part of this repository's active instruction hierarchy.

## 5. Runtime Surface

- `.agents/` is Gemini's shared runtime surface and moderate-shim.
- `.agents/rules/` contains Gemini-specific rules.
- `.agents/workflows/` contains Gemini-specific workflows.
- `.agents/skills/` contains Gemini's runtime skill implementations.
- `.agents/agents/` provides the Gemini reference index pointing to the governance catalog.
- The `.agents/` directory is git-tracked.

## 6. Hook Parity Contract

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
