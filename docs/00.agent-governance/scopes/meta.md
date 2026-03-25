---
layer: meta
title: 'Metadata & Taxonomy Engineering Scope'
---

# Metadata & Taxonomy Engineering Scope

**Rules for repository structure, document frontmatter, and taxonomy enforcement.**

## 1. Context & Objective

- **Goal**: Maintain a highly organized, searchable, and AI-optimized documentation ecosystem.
- **Standards**: Strict adherence to the **01-11 Stage-Gate Taxonomy**.

## 2. Requirements & Constraints

- **Frontmatter**: Every Markdown file MUST include a `layer` attribute in YAML frontmatter.
- **File Naming**: Use `YYYY-MM-DD-<feature-id>.md` for time-sensitive docs (Plans, PRDs).
- **Hierarchy**: No orphans; all files must be linked from a directory README or Central Hub.

## 3. Implementation Flow

1. **Placement**: Determine the correct taxonomy folder (01~11) for new documents.
2. **Template**: Use the corresponding template from `docs/99.templates/`.
3. **Linking**: Update the parent README and any related cross-links (e.g., ADR <-> Spec).

## 4. Operational Procedures

- **Linting**: Use `markdownlint` to enforce style and structure.
- **Broken Links**: Periodically scan for and fix dead internal links.

## 5. Maintenance & Safety

- **Pruning**: Archived or outdated docs must be moved to an `archive/` subfolder, not deleted.
- **Refactoring**: Significant changes to folder structure require a `Meta ADR`.
