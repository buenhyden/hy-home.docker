---
layer: agentic
---

# Template Contract

## Overview

This document defines the non-copyable contract for template source files under
`docs/99.templates/templates/`.

## Surface Boundaries

- Template forms and template rules are separate surfaces.
- Copyable forms live under `docs/99.templates/templates/`.
- Non-copyable rules live under `docs/99.templates/support/`.
- README files are indexes and routing surfaces; durable rules belong in support documents.

## Template Source Rules

- Copyable source files live only under `docs/99.templates/templates/`.
- Markdown template files use the `*.template.md` suffix.
- Machine-readable contract templates use `*.template.yaml`,
  `*.template.graphql`, or `*.template.proto`.
- Markdown template sources start with `status: draft` frontmatter.
- Machine-readable templates use comments for `Target:` and cross-link ownership
  instead of YAML frontmatter.
- Every Markdown template includes target path guidance, target-relative link
  guidance, and `## Related Documents`.
- Non-Markdown contract templates do not include Markdown `## Related Documents`;
  their parent Markdown spec or API spec owns cross-links.

## Placeholder Rules

- Placeholder text must be visually obvious.
- Target documents must not keep unresolved placeholders.
- Template-time example links are calculated from the copied target path, not
  from the template source path.
- Example commands in templates must be deleted or replaced before target
  documents are saved.

## Numbered SDLC Path Rules

- PRD template target guidance uses
  `docs/01.requirements/NNN-<feature-or-system>.md`.
- Spec template and spec-child target guidance uses
  `docs/03.specs/NNN-<feature-id>/...`.
- `NNN` is a zero-padded three-digit routing prefix and is part of the
  canonical path, not a frontmatter key.
- Plan and Task template target guidance remains date-prefixed under
  `docs/04.execution/`.
- Template source files must not publish date-prefixed PRD targets or
  unnumbered Spec targets except inside explicit historical migration tables.

## Target Document Rules

- Target documents inherit from exactly one primary template role.
- Purpose-specific child templates may supplement a parent spec when the target
  path and role require them.
- Target document frontmatter follows [frontmatter contract](./frontmatter-contract.md), not the template source metadata.
- Intentional template deviation must be recorded in Stage 04 task evidence.
- Archive, duplicate-remove, conflict-remove-or-archive, and evidence-preserve
  decisions are governed by [template governance](./template-governance.md) and
  [template selection](./template-selection.md), not by copying additional
  instructions into target documents.
- A target document must not keep copied template instructions or unresolved
  examples as a substitute for topic-specific content.

## Related Documents

- [support README](./README.md)
- [template governance](./template-governance.md)
- [frontmatter contract](./frontmatter-contract.md)
- [template selection](./template-selection.md)
