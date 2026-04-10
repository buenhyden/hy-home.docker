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
- `.claude/agents/`, `.claude/skills/`, and the shared governance docs define the repo-local behavior Gemini must follow when operating in this workspace.
- GitHub-native instruction files are not part of this repository's active instruction hierarchy.

## 5. Operational Practices

- Use `/memory list` to inspect loaded context files.
- Use `/memory show` to inspect merged effective context.
- Use `/memory refresh` after editing instruction files.
- Keep imports explicit and remove stale references quickly.

## Related Documents

- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/bootstrap.md`

## References

- <https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html>
- <https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html>
- <https://google-gemini.github.io/gemini-cli/docs/cli/commands.html>
