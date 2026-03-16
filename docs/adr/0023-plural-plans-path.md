---
title: 'ADR 0004: Adoption of Plural plans Path'
status: 'Accepted'
date: '2026-03-15'
layer: 'architecture'
---

# ADR 0023: Adoption of Plural plans Path

## Context

The previous refactor established `docs/plans/`. However, updated organizational standards mandate the use of `docs/plans/` (plural) for consistency with other plural category roots like `specs`, `runbooks`, and `rules`.

## Decision

Rename `docs/plans/` to `docs/plans/` and update all internal references.

## Consequences

- **Positive**: Consistency across the documentation root.
- **Negative**: Temporary risk of broken internal links during migration.
