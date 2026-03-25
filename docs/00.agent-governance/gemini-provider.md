---
layer: agentic
---

# Gemini Provider Notes

## Scope

This file contains Gemini CLI-specific guidance only. Repository-wide rules live in the shared fragments imported by [`../../GEMINI.md`](../../GEMINI.md).

## Context File Hierarchy

Gemini CLI loads context files in this order (lowest to highest precedence):

| File                       | Scope                 | Notes                                                                     |
| -------------------------- | --------------------- | ------------------------------------------------------------------------- |
| `~/.gemini/GEMINI.md`      | Global — all projects | User-wide preferences; personal defaults                                  |
| `./GEMINI.md` (repo root)  | Project — shared      | Checked into git; applies to all team members                             |
| `<subdirectory>/GEMINI.md` | Directory             | JIT-loaded when a tool accesses a file in that directory or its ancestors |

## Gemini CLI Guidance

- Keep the root `GEMINI.md` thin and use `@file`-style imports for shared fragments.
- Use hierarchical context discovery: root file for universal rules, subdirectory files for local task context.
- Prefer on-demand loading through the owning layer router instead of broad repository ingestion when the task is localized.
- MCP server integrations are configured in `.gemini/settings.json` under the `mcpServers` key.
- **Skill Autonomy**: Gemini MUST utilize any available skill (e.g., `writing-plans`, `executing-plans`, `doc-coauthoring`) to accelerate delivery and ensure standard compliance.

## Import Syntax

Use `@file` references in `GEMINI.md` to import shared fragments:

```text
@file:docs/00.agent-governance/README.md
@file:docs/00.agent-governance/rules/persona-matrix.md
```

## Korean Mandate

- **USER interaction**: Summaries and high-level explanations MUST be in Korean.
- **Internal Docs**: All instructions and technical documentation in `docs/00.agent-governance/` MUST be in English.

## References

- Gemini CLI context files (GEMINI.md): <https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md>
- Gemini CLI settings: <https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/settings.md>
- Gemini CLI MCP integration: <https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md>
