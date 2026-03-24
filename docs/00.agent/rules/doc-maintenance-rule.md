---
title: 'Documentation Maintenance Rule'
layer: agentic
---

# Documentation Maintenance Rule

This rule applies to all tasks involving the creation, modification, or auditing of documentation in the `docs/` or root directories.

## 1. Compliance Standard

- **Frontmatter**: Every file MUST start with:

  ```yaml
  ---
  layer: <layer_name>
  ---
  ```

- **Taxonomy**: Strictly follow the numbered category-based folders: `01.prd, 02.ard, 03.adr, 04.specs, 05.plans, 08.operations, 09.runbooks`.
- **Naming**: Use kebab-case for filenames (e.g., `my-new-spec.md`).

## 2. Skill Guidance

- Proactively use `claude-md-improver` to check for LLM-isms or readability issues.
- Use `agent-md-refactor` to keep index `README.md` files up to date.

## 3. Metadata Keys

Valid `layer` values:

- `common, architecture, backend, frontend, infra, mobile, product, qa, security, entry, meta, ops, agentic`.
