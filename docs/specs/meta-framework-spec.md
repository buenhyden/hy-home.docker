---
title: 'Meta-Framework & Documentation Spec'
status: 'Draft'
version: 'v1.1.0'
owner: 'Antigravity'
layer: 'architecture'
---

# Meta-Framework & Documentation Spec

## 1. Root File Cleanup

- **README.md**: Retain Overview, Features, Tech Stack, and Quick Start. Move Troubleshooting to `docs/guides/troubleshooting.md`. Remove "Project Structure" (covered by `docs/README.md`).
- **ARCHITECTURE.md**: Retain Invariants and Runtime Topology. Move change governance details to `docs/agentic/rules/governance-rule.md`.
- **COLLABORATING.md/CONTRIBUTING.md**: Move content to `docs/manuals/collaboration-guide.md` and `docs/guides/contributing-guide.md`. Replace with short pointers to those files.

## 2. Agent Rule Refactor

- Create `docs/agentic/rules/refactor-rule.md`:
  - Definition of refactoring workflow.
  - Required skills (`agent-md-refactor`, `claude-md-improver`).
  - Automated checks.
- Create `docs/agentic/rules/doc-maintenance-rule.md`:
  - Rules for updating `docs/`.
  - Forced `layer` metadata check.

## 3. Lazy Loading Implementation

Update `docs/agentic/gateway.md` with:

```markdown
| Intent | Entry Point |
| --- | --- |
| Refactoring Documentation | [rules/refactor-rule.md](rules/refactor-rule.md) |
| Standard Doc Update | [rules/doc-maintenance-rule.md](rules/doc-maintenance-rule.md) |
```
