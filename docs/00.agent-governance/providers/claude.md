---
layer: agentic
---

# Claude Provider Notes

Claude-specific guidance for this repository. Shared governance stays in `rules/` and `scopes/`.

## 1. Context & Objective

- Ensure Claude runtime behavior stays aligned with repository governance.
- Keep provider instructions minimal and runtime-specific.

## 2. Requirements & Constraints

- Claude reads `CLAUDE.md`, not `AGENTS.md` directly.
- For AGENTS compatibility, keep `@AGENTS.md` at the top of root `CLAUDE.md`.
- Keep root `CLAUDE.md` short; move details to this file or `.claude/rules/`.
- Target less than 200 lines per `CLAUDE.md` file.

## 3. Implementation Flow

1. Load `@AGENTS.md`.
2. Load this provider file.
3. Load `rules/bootstrap.md` then route into one primary scope.
4. Use stage JIT markers only for required stages.

## 4. Operational Procedures

- Prefer scoped rule files under `.claude/rules/` for large projects.
- Use path-specific rules to reduce irrelevant context.
- Use `@path/to/file` imports for modular instruction management.

## 5. Maintenance & Safety

- Keep imports explicit and conflict-free.
- Avoid embedding personal preferences in shared project files.
- For personal overrides, use user-level Claude memory/settings outside the repository.

## References

- https://code.claude.com/docs/en/memory
