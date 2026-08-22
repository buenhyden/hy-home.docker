---
profile_id: governance-role
layer: docs
---

# Documentation Ownership

## Scope

This role boundary owns canonical documentation structure, language, links,
metadata, and traceability. Root instructions are limited to `AGENTS.md` and
`CLAUDE.md`; generated provider files remain adapter-owned.

## Responsibilities

- Select the correct Stage 99 profile before authoring.
- Preserve the Stage 01/02/03/05/90/98/99 ownership boundary.
- Update affected indexes and cross-links with the canonical source.
- Route implementation and verification evidence to the co-located Task.
- Report out-of-scope gaps in that Task instead of creating a second authority.

## Permissions

The `doc-writer` may edit approved documentation. All other roles are read-only
unless their Task explicitly includes a documentation update. Policy changes
require `rules-engineer` review.

## Related Documents

- [Documentation protocol](../policies/documentation-protocol.md)
- [Stage authoring matrix](../policies/stage-authoring-matrix.md)
- [Document writer](./doc-writer.md)
