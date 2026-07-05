---
status: active
---

<!-- Target: docs/03.specs/099-template-system-numbered-sdlc-paths/README.md -->

# Template System Numbered SDLC Paths

> Stage 03 design entrypoint for the numbered PRD and Spec path migration.

## Overview

This folder contains the approved design for migrating the PRD and Spec corpus
to numbered target paths while updating the Stage 99 template system,
governance references, validators, and cross-links.

The design covers the full active and historical corpus under
`docs/01.requirements/` and `docs/03.specs/`. It replaces date-prefixed PRD
filenames and unnumbered Spec folders with deterministic three-digit prefixes,
then hands off implementation through Stage 04 plan and task evidence.

## Audience

This README is for:

- Documentation Specialists
- Agentic Workflow Specialists
- QA Engineers
- Repository Maintainers

## Scope

### In Scope

- Design for renaming every PRD file under `docs/01.requirements/`.
- Design for renaming every Spec folder under `docs/03.specs/`.
- Design for Stage 99 template/support contract updates.
- Design for Stage 00 governance, validator, README, and cross-link fallout.
- Validation and commit boundaries for the implementation wave.

### Out of Scope

- Runtime Docker Compose, secret, credential, remote GitHub, or deployment
  changes.
- Rewriting target document bodies for style-only reasons.
- Creating redirect-style duplicate documents after a move.
- Moving SDLC artifacts outside canonical `docs/01` through `docs/05` stages.

## Structure

```text
099-template-system-numbered-sdlc-paths/
├── README.md  # This file
└── spec.md    # Numbered SDLC path migration design
```

## How to Work in This Area

1. Read [spec.md](./spec.md) before mutating PRD, Spec, template, governance,
   or validator surfaces.
2. Create a Stage 04 implementation plan before moving files or folders.
3. Use `git mv` for path changes so history remains reviewable.
4. Keep path moves, contract edits, validator edits, and generated-index
   updates in logical commits.

## Related Documents

- **Spec**: [spec.md](./spec.md)
- **Template selection**: [../../99.templates/support/template-selection.md](../../99.templates/support/template-selection.md)
- **Template contract**: [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- **Frontmatter contract**: [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Stage authoring matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
