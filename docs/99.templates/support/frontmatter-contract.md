---
layer: agentic
---

# Frontmatter Contract

## Overview

This document defines frontmatter key ownership for template sources and target
documents. Frontmatter is a Markdown-adjacent preprocessing convention, not core
CommonMark syntax, so the repository treats it as a small structured metadata
surface.

## Field Families

| Family | Surface | Allowed Pattern |
| --- | --- | --- |
| Template source | `docs/99.templates/templates/**/*.template.md` | `status: draft` only unless a future validator explicitly accepts more keys. |
| Machine-readable template | `*.template.yaml`, `*.template.graphql`, `*.template.proto` | No YAML frontmatter; use comments for target guidance. |
| Stage documents | `docs/01` through `docs/05` and `docs/90` leaf docs | `status: draft`, `status: active`, `status: completed`, or `status: superseded`. |
| Archive tombstones | `docs/98.archive/**` | `status: archived` plus archive-specific provenance keys when required. |
| Governance and support | Stage 00 and Stage 99 governance/support README-style documents | `layer: agentic` when the file is a governance/support entrypoint. |
| Generated files | generated tracked docs | `generated_by` only when generated tooling owns the file. |

## Duplicate-Purpose Key Rules

- Do not use both `type` and path-derived document role for the same purpose.
- Do not use generic `owner`, `updated`, or `links` metadata unless a target
  profile explicitly consumes those keys.
- Do not copy README template metadata examples into final README files.
- Do not use template-source `status: draft` as a final target status without
  checking the target lifecycle.

## Legacy Cleanup Rules

- Remove generic metadata snippets that list `title`, `type`, `owner`,
  `updated`, or `links` when they are only illustrative.
- Replace flat template path references with canonical nested template paths.
- If a target document contains copied template instructions instead of
  topic-specific content, record a follow-up gap unless the document is already
  in the approved edit scope.

## Related Documents

- [support README](./README.md)
- [template contract](./template-contract.md)
- [lifecycle status](./lifecycle-status.md)
- [external source rationale](./external-source-rationale.md)
