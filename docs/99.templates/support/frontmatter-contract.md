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
| Folder index README | none by default; use headings and path for role | copied template `status: draft`, `type`, `owner`, `updated`, `links` |
| Root, provider, GitHub-native, and utility README | none by default unless a provider or native platform consumes metadata | copied template `status: draft`, `type`, `owner`, `updated`, `links` |
| Repo-support contract README (`_workspace/**/README.md`) | none; role is path-derived | lifecycle `status`, `layer`, `type`, `owner`, `updated`, `links` |
| Generated tracked document | generator-owned metadata such as `generated_by` | human-authored lifecycle keys unless the generator owns them |
| Generated report without metadata consumer | none; omit YAML frontmatter | human-authored lifecycle keys |

Archive tombstones are target stage documents with the archive lifecycle profile:
`status: archived` plus archive-specific provenance keys when that profile
requires them.

## Disposition and Archive Metadata Rules

Restructure dispositions are audit/task decisions, not frontmatter values. Do
not add frontmatter keys such as `disposition`, `document_type`, or
`template_type` to encode archive decisions.

| Decision Surface | Frontmatter Rule |
| --- | --- |
| `active-canonical` | Keep the target's lifecycle `status` and primary document profile. |
| `historical-archive` | Use `status: archived` only on the archive tombstone under `docs/98.archive/**`. |
| `duplicate-remove` | Do not add new metadata to the duplicate solely to delete it; record replacement evidence in task/gap records. |
| `conflict-remove-or-archive` | Use archive provenance keys on the tombstone or record a gap when no replacement exists. |
| `evidence-preserve` | Preserve historical frontmatter unless a future task proves it is active-current guidance drift. |

Archive provenance keys are limited to archive tombstones and approved archive
profiles: `archived_from`, `archived_on`, `archive_reason`, and
`current_replacement`.

## Duplicate-Purpose Key Rules

- Do not use both `type` and path-derived document role for the same purpose.
- Do not use generic `owner`, `updated`, or `links` metadata unless a target
  profile explicitly consumes those keys.
- Do not copy README template metadata examples into final README files.
- Do not add YAML frontmatter to README files just to make them resemble
  target-stage leaf documents. README role is normally derived from path,
  heading, and folder-index profile.
- Do not use template-source `status: draft` as a final target status without
  checking the target lifecycle.

## Legacy Cleanup Rules

- Remove generic metadata snippets that list `title`, `type`, `owner`,
  `updated`, or `links` when they are only illustrative.
- Replace flat template path references with canonical nested template paths.
- If a target document contains copied template instructions instead of
  topic-specific content, record a follow-up gap unless the document is already
  in the approved edit scope.

## Corpus Routing Rules

- Non-README target-stage Markdown under `docs/01` to `docs/05` and `docs/90`
  requires lifecycle `status` frontmatter.
- Archive tombstones under `docs/98.archive` require `status: archived`; archive
  folder README files remain folder indexes and do not need archive tombstone
  metadata.
- Governance memory and Stage 00 rule/provider/scope documents use `layer:`
  frontmatter instead of lifecycle `status`.
- Markdown template sources keep `status: draft`; copied target documents must
  replace that template-source status with the target profile or omit
  frontmatter when the target is a README.
- GitHub-native Markdown surfaces such as pull request templates, security
  policy files, and ruleset evidence files should not receive repository
  frontmatter unless a GitHub-specific consumer is approved.
- `_workspace` README files are repo-support contract surfaces. Do not add
  target-stage lifecycle frontmatter, Stage 00 `layer:` frontmatter, or template
  source metadata to them.
- Generated report files without a metadata consumer should not receive manual
  YAML frontmatter; preserve generator output unless the generator is changed.

## Related Documents

- [support README](./README.md)
- [template contract](./template-contract.md)
- [lifecycle status](./lifecycle-status.md)
- [external source rationale](./external-source-rationale.md)
