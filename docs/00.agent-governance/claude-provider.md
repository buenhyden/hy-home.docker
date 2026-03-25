---
layer: agentic
---

# Claude Provider Notes

## Scope

This file contains Claude Code-specific guidance only. Repository-wide rules live in the shared fragments imported by [`../../CLAUDE.md`](../../CLAUDE.md).

## Memory Hierarchy

Claude Code loads `CLAUDE.md` files in this order (lowest to highest precedence):

| File                       | Scope                 | Notes                                                    |
| -------------------------- | --------------------- | -------------------------------------------------------- |
| `~/.claude/CLAUDE.md`      | Global — all projects | User-wide preferences; personal defaults                 |
| `./CLAUDE.md` (repo root)  | Project — shared      | Checked into git; applies to all team members            |
| `./.claude.local.md`       | Project — personal    | Gitignored; use for local overrides not shared with team |
| `<subdirectory>/CLAUDE.md` | Directory             | Loaded automatically when working within that directory  |

## Claude Code Instructions

- Keep the root `CLAUDE.md` thin and import shared fragments with `@` references.
- Prefer parent-to-child memory hierarchy: root file for universal rules, subdirectory files for local detail.
- Use `.claude.local.md` for personal preferences (API keys, editor settings, personal workflow tweaks). Add `.claude.local.md` to `.gitignore`.
- Preserve context by loading the owning layer router before loading adjacent layers.
- Keep instructions actionable and project-specific. Avoid generic prose or fake local workflows.
- **Thinking Process**: ALWAYS use `<thinking>` tags for planning and internal logic.
- **Validation**: Pass `scripts/validate-docker-compose.sh` for any infra/service changes.
- **Skill Autonomy**: Claude MUST utilize any available skill (e.g., `writing-plans`, `executing-plans`, `doc-coauthoring`) to accelerate delivery and ensure standard compliance without persona-based restrictions.

## Import Syntax

Use `@` references in `CLAUDE.md` to import shared fragments:

```text
@docs/00.agent-governance/README.md
@docs/00.agent-governance/rules/persona-matrix.md
@docs/00.agent-governance/rules/quality-standards.md
```

## Korean Mandate

- **USER interaction**: Summaries and high-level explanations MUST be in Korean.
- **Internal Docs**: All instructions and technical documentation in `docs/00.agent-governance/` MUST be in English.

## References

- Anthropic Claude Code memory: <https://docs.anthropic.com/en/docs/claude-code/memory>
