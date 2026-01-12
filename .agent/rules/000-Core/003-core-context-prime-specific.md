---
trigger: always_on
glob: "**/*"
description: "Context Prime: Guidelines for AI context loading and project understanding."
---
# Context Prime Standards

## 1. Standard Context Loading

- **Project Overview**: ALWAYS read `README.md` first to understand goals and architecture.
- **AI Guidelines**: Read project-specific AI instructions (e.g., `.agent/rules`, `CLAUDE.md`, `.cursorrules`).
- **Structure**: Use `git ls-files | head -50` (or list command) to grasp the directory layout.

## 2. Development Context

- **Configuration**: Check package managers (`package.json`, `pyproject.toml`, `Cargo.toml`) early to identify dependencies.
- **Testing**: Identify the test framework (pytest, jest, etc.) to know how to verify changes.

## 3. Output

- **Goal**: Establish a clear understanding of project constraints, technical architecture, and development workflow before making changes.


## See Also

- [020-core-project-structure-specific.md](./020-core-project-structure-specific.md) - Project structure patterns
- [025-core-project-definition-specific.md](./025-core-project-definition-specific.md) - Project definition
