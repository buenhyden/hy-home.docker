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
- GitHub-native instruction files are not part of this repository's active instruction hierarchy.
- Personal `settings.local.json` may not override team policy in `settings.json`.

## 5. Operational Practices

- Keep instructions short, specific, and executable.
- Prefer path-scoped instruction files instead of large monolithic root files.
- After instruction updates, start a fresh run or reload context so new guidance is effective.

## Related Documents

- `docs/00.agent-governance/providers/agents-md.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/bootstrap.md`

## References

- <https://docs.anthropic.com/en/docs/claude-code/memory>
