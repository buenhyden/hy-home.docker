---
layer: common
---

# Common Engineering Scope

**Universal engineering standards, naming conventions, and shared patterns across all layers.**

## 1. Context & Objective

- **Goal**: Ensure consistency, maintainability, and readability across the entire `hy-home.docker` codebase.
- **Standards**: Priority on Clean Code, SOLID principles, and `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Language**: Use English for all code, comments, and internal documentation.
- **Naming**:
  - Variables/Functions: `camelCase`
  - Classes/Types: `PascalCase`
  - Constants: `SCREAMING_SNAKE_CASE`
  - Files: `kebab-case.ext`
- **Formatting**: Follow repository-configured lint/format behavior mediated by
  `.pre-commit-config.yaml`; direct `pre-commit run` and ad hoc formatter
  commands are prohibited for agents. The approved final QA all-files gate uses
  only `scripts/validation/run-agent-precommit-all-files.sh`.

## 3. Implementation Flow

1. **DRY Check**: Before implementing a new utility, check for existing logic in `common/` or shared libs.
2. **Type Safety**: Prefer strict typing and avoid `any` or loose types.
3. **Documentation**: Add JSDoc/Docstrings for all public APIs and complex logic.

## 4. Operational Procedures

- **Linting and Formatting**: Hooks run automatically on commit. Agents must not
  run `pre-commit run`, `npm run lint`, `npm run format`, or equivalent commands
  directly. At an approved final QA gate, the controlled wrapper may run the
  configured all-files suite from an initially clean linked worktree with a
  tracked task and reviewed prefixes; its edits require explicit review and
  manual task evidence. Evidence covers only Git-visible, non-ignored repository
  paths and does not claim ignored/outside-write detection or
  process/filesystem sandboxing.

## 5. Maintenance & Safety

- **Refactoring**: Proactively extract shared logic into common utilities when spotted in multiple layers.
- **Cleanup**: Remove only the imports, variables, generated artifacts, or dead paths made stale by your own change; report unrelated cleanup opportunities instead of editing them.

## 6. File Ownership SSOT

| Path Pattern                 | Owner Agent     | Read-Only For                  |
| ---------------------------- | --------------- | ------------------------------ |
| `common/`, `lib/`, `shared/` | `code-reviewer` | read; changes by layer agent   |
| `docs/03.specs/`             | `code-reviewer` | `infra-implementer` (read)     |
| `.pre-commit-config.yaml`    | `code-reviewer` | all — direct runs prohibited; controlled final-QA wrapper only |

## 7. Subagent Bridge

```text
# code-reviewer agent preamble
@import docs/00.agent-governance/scopes/common.md
# Review pattern — read → assess → report
# Clean Code · SOLID · no plaintext secrets
```

Spawn via the active runtime's delegated-agent facility. Do not embed common standards inline in agent files.

## Related Documents

- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/postflight-checklist.md`
