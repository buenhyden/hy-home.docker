---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/template-contract-drift.md -->

# Reference: Template Contract Drift

## Overview

This report compares the approved document restructure design with current
Stage 99 template and support surfaces. It records contract gaps that should be
handled before destructive archive, remove, or relink batches.

## Purpose

The restructure design requires audit-first and template-contract-first
execution. This report identifies where current template support documents
already cover archive/frontmatter rules and where the archive-centered
disposition model still needs an explicit support contract.

## Repository Role

This report supports `PLN-DRA-002` and the `PLN-DRA-003` template contract
batch. It is not active policy, not a template source, and not approval to
move, remove, archive, or relink target documents.

## Scope

### In Scope

- Stage 99 support documents and templates.
- Archive, frontmatter, lifecycle, and destructive-change contract coverage.
- Existing source evidence from prior document-contract remediation reports.

### Out of Scope

- Moving target documents or creating archive tombstones.
- Rewriting historical specs, plans, tasks, or progress rows.
- Runtime, provider, workflow, or secret changes.

## Definitions / Facts

- **Disposition model**: the approved classification set
  `active-canonical`, `historical-archive`, `duplicate-remove`,
  `conflict-remove-or-archive`, and `evidence-preserve`.
- **Template support contract**: a durable Stage 99 support document that owns
  reusable document rules.
- **README routing surface**: a folder or category index that should point to
  rules but not own durable rules.
- **Archive tombstone**: a minimal `docs/98.archive/**` document using
  `status: archived` and provenance metadata.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| DRA-TCD-001 | `git ls-files 'docs/99.templates/support/*.md' 'docs/99.templates/templates/**/*.md' 'docs/99.templates/templates/**/*.yaml' 'docs/99.templates/templates/**/*.graphql' 'docs/99.templates/templates/**/*.proto' \| wc -l` | 37 Stage 99 support/template files are tracked. | Establishes template-system surface size. |
| DRA-TCD-002 | `rg -n 'historical-archive\|duplicate-remove\|conflict-remove-or-archive\|evidence-preserve\|archive-centered\|destructive\|tombstone\|frontmatter\|status: archived\|status: completed' docs/99.templates/support docs/99.templates/templates --glob '*.md'` | At audit capture, contracts mentioned frontmatter, archive tombstones, and template source rules, but not the full approved disposition model. | Identified the `PLN-DRA-003` contract gap. |
| DRA-TCD-003 | Reads of `template-contract.md`, `frontmatter-contract.md`, `template-governance.md`, `template-selection.md`, `lifecycle-status.md`, and `archive.template.md` | Existing contracts cover template-source frontmatter, target status, archive tombstones, and lifecycle values. | Separates covered rules from missing restructure-specific rules. |
| DRA-TCD-004 | Read of `docs/03.specs/document-restructure-audit-contract-archive/spec.md` | The approved design requires archive-centered dispositions before target moves. | Binds findings to the approved Stage 03 design. |

## Findings

| ID | Surface | Finding | Disposition | Recommended Batch |
| --- | --- | --- | --- | --- |
| DRA-TCD-001 | Stage 99 support docs | Current support docs define frontmatter, lifecycle, archive tombstone, selection, and template-source boundaries. | `active-canonical` | No change in audit pack. |
| DRA-TCD-002 | `template-governance.md`; `template-selection.md`; `lifecycle-status.md` | Closed in `PLN-DRA-003`: the approved disposition model is now owned by Stage 99 support docs. | `active-canonical` | Done |
| DRA-TCD-003 | `archive.template.md` | Closed in `PLN-DRA-003`: archive tombstones remain a format template, while disposition conditions are owned by Stage 99 support docs. | `active-canonical` | Done |
| DRA-TCD-004 | README files | README files should remain indexes and should not receive durable archive/destructive-change rules. | `active-canonical` | Enforce in `PLN-DRA-003` and later README relink batches. |

## Source Rules

- Use Stage 99 support docs as the durable rule owner.
- Use README files only for routing and index updates.
- Do not copy external-source or Stage 03 design prose into templates as
  policy without adapting it to Stage 99 support-contract language.
- Do not create tombstones or move documents until an implementation batch
  records exact target paths, replacement pointers, link synchronization, and
  rollback guidance.

## Remediation Updates

| Date | Rows | Status | Evidence | Residual Action |
| --- | --- | --- | --- | --- |
| 2026-07-04 | DRA-TCD-002, DRA-TCD-003 | Closed by `PLN-DRA-003` | Stage 99 support docs now define archive-centered disposition mapping, destructive target-change preconditions, archive metadata boundaries, and target-document cleanup rules. | Apply these rules in future Stage 03 and Stage 05 target batches only after exact file-list approval. |

## Sources

- [Document restructure design spec](../../../03.specs/document-restructure-audit-contract-archive/spec.md) - Supplies the approved disposition model and implementation handoff.
- [Template contract](../../../99.templates/support/template-contract.md) - Defines template-source and target-document boundaries.
- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) - Defines lifecycle and archive frontmatter ownership.
- [Template governance](../../../99.templates/support/template-governance.md) - Owns template-system governance rules.
- [Template selection](../../../99.templates/support/template-selection.md) - Owns template routing.
- [Lifecycle status](../../../99.templates/support/lifecycle-status.md) - Owns lifecycle status semantics.
- [Archive template](../../../99.templates/templates/common/archive.template.md) - Supplies the tombstone format.
- [Historical evidence preservation](../2026-07-03-workspace-document-contract-audit-pack/historical-evidence-preservation.md) - Supplies the prior preserve-old-evidence decision.

## Maintenance

- **Owner**: Documentation Specialist / Repository Maintainer.
- **Review Cadence**: Review after any Stage 99 support contract changes.
- **Update Trigger**: Update when the disposition model is added to Stage 99
  support docs or when archive/remove rules change.

## Related Documents

- [Document restructure audit references](./README.md)
- [Restructure gap register](./restructure-gap-register.md)
- [Template contract](../../../99.templates/support/template-contract.md)
- [Template governance](../../../99.templates/support/template-governance.md)
