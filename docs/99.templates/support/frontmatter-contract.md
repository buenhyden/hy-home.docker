---
layer: agentic
---

# Frontmatter Contract

## Overview

This document defines frontmatter key ownership for template sources and target
documents. Frontmatter is a Markdown-adjacent preprocessing convention, not core
CommonMark syntax, so the repository treats it as a small structured metadata
surface.

## Role Matrix

| Surface | Required Keys | Disallowed Duplicate-Purpose Keys |
| --- | --- | --- |
| Markdown template source | `status: draft` | `type`, `owner`, `updated`, `links`, `document_type`, `template_type` |
| Machine-readable template source | none; use comments | YAML frontmatter fences, `type`, `owner`, `updated`, `links` |
| Stage 99 support document | `layer: agentic` | `status`, `type`, `owner`, `updated`, `links` |
| Target stage document | path-derived role plus lifecycle `status` | `type`, `document_type`, `template_type` |
| Generated tracked document | generator-owned metadata such as `generated_by` | human-authored lifecycle keys unless the generator owns them |

Archive tombstones are target stage documents with the archive lifecycle profile:
`status: archived` plus archive-specific provenance keys when that profile
requires them.

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
