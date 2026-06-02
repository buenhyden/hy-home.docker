---
layer: meta
title: 'Metadata & Taxonomy Engineering Scope'
---

# Metadata & Taxonomy Engineering Scope

**Rules for repository structure, document frontmatter, and taxonomy enforcement.**

## 1. Context & Objective

- **Goal**: Maintain a highly organized, searchable, and AI-optimized documentation ecosystem.
- **Standards**: Strict adherence to the `01.requirements - 05.operations/incidents` Stage-Gate Taxonomy, plus `90.references`, `98.archive`, and `99.templates`.

## 2. Requirements & Constraints

- **Frontmatter**: Every Markdown file MUST include a `layer` attribute in YAML frontmatter.
- **File Naming**: Use `YYYY-MM-DD-<feature-id>.md` for time-sensitive docs (Plans, PRDs).
- **Hierarchy**: No orphans; all files must be linked from a directory README or Central Hub.

## 3. Implementation Flow

1. **Placement**: Determine the correct taxonomy folder (`01.requirements - 05.operations/incidents`, `90.references`, `98.archive`, or `99.templates`) for new documents.
2. **Template**: Use the corresponding template from `docs/99.templates/`.
3. **Linking**: Update the parent README and any related cross-links (e.g., ADR <-> Spec).

## 4. Operational Procedures

- **Linting**: Use `markdownlint` to enforce style and structure.
- **Broken Links**: Periodically scan for and fix dead internal links.

## 5. Maintenance & Safety

- **Pruning**: Implementation-conflicting whole-document old material must be moved to `docs/98.archive/` tombstones, not preserved in active stage folders.
- **Refactoring**: Significant changes to folder structure require a `Meta ADR`.

## Related Documents

- [Agent governance hub](../README.md)
- [Bootstrap rule](../rules/bootstrap.md)
- [Persona protocol](../rules/persona.md)
- [Task checklists](../rules/task-checklists.md)
- [Agentic rule](../rules/agentic.md)
