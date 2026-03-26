---
layer: agentic
---

# Gemini Provider Notes

Gemini CLI-specific guidance for this repository.

## 1. Context & Objective

- Keep Gemini context loading predictable and token-efficient.
- Align Gemini behavior with shared governance in `AGENTS.md` and `docs/00.agent-governance`.

## 2. Requirements & Constraints

- Root `GEMINI.md` should stay thin and import shared instructions.
- Prefer hierarchical context loading (global/workspace/JIT) over broad static context.
- Recommended `.gemini/settings.json` policy:
  - `"context.fileName": ["GEMINI.md", "AGENTS.md"]`
- Sandboxing is not always enabled by default; configure explicitly as needed.

## 3. Implementation Flow

1. Load `@AGENTS.md`.
2. Load this provider file.
3. Load `rules/bootstrap.md` and `rules/persona.md`.
4. Load one primary layer scope and only required stage docs.

## 4. Operational Procedures

- Use `/memory list` to inspect loaded context files.
- Use `/memory show` to inspect effective merged context.
- Use `/memory refresh` after editing instruction files.
- Use `@path` imports to modularize large context files.

## 5. Maintenance & Safety

- Keep context files concise and non-contradictory.
- Remove stale instructions quickly to avoid context pollution.
- Keep provider guidance runtime-specific; do not duplicate shared policies.

## References

- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md
- https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html
- https://google-gemini.github.io/gemini-cli/docs/cli/commands.html
