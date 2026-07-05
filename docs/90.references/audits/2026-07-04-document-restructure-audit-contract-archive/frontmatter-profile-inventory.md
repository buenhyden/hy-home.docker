---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/frontmatter-profile-inventory.md -->

# Reference: Frontmatter Profile Inventory

## Overview

This report captures the DRA baseline frontmatter profile from before document
restructure work began. It records baseline counts, keys, status values, and
frontmatter gaps without editing any target document, then carries lifecycle
overlays when later cleanup changes the status distribution.

## Purpose

The restructure design requires frontmatter standardization by document type,
but target edits must be evidence-led. This report gives the future contract
and target-stage batches a reproducible baseline plus the latest lifecycle
overlay when status cleanup occurs.

## Repository Role

This report supports `PLN-DRA-002`, `PLN-DRA-003`, and later target-stage
cleanup batches. It is not a validator, not active policy, and not approval for
a broad Markdown corpus rewrite.

## Scope

### In Scope

- Tracked Markdown frontmatter counts and keys.
- Baseline `status` value distribution under `docs/**` and later lifecycle
  overlays when refreshed.
- Stage 03 status distribution.
- Reference-stage transitional lifecycle evidence.

### Out of Scope

- Adding frontmatter to files.
- Rewriting historical evidence.
- Changing lifecycle contracts.
- Reading secret values or runtime state.

## Definitions / Facts

- **Top frontmatter**: a tracked Markdown file whose first line is `---`.
- **Lifecycle status**: the `status` key owned by Stage 99 frontmatter and
  lifecycle contracts.
- **Duplicate-purpose key**: a metadata key that repeats path, title, owner,
  date, or generated-state information without a profile-specific consumer.
- **Outlier**: a value or key that needs routing before a target edit.
- **Transitional status**: a lifecycle value that keeps a replaced document in
  the active reference chain while it points to the current replacement.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| DRA-FM-001 | `git ls-files '*.md' \| wc -l` | 948 tracked Markdown files. | Corpus baseline after `PLN-DRA-001`. |
| DRA-FM-002 | First-line scan over `git ls-files '*.md'` | 764 tracked Markdown files start with top `---`; 184 do not. | Confirms current frontmatter population. |
| DRA-FM-003 | Frontmatter key extraction from top fenced Markdown files | Top keys: `status` 538, `layer` 176, `name` 79, `description` 60, `model` 30, and provider/archive/generated keys in smaller counts. | Identifies key families and protected profiles. |
| DRA-FM-004 | `rg --no-filename -o '^status: [a-z-]+' docs --glob '*.md' \| sort \| uniq -c` | Baseline: `active` 349, `archived` 20, `completed` 140, `draft` 30, `superseded` 1. 2026-07-05 overlay: `active` 344, `archived` 20, `completed` 179, `draft` 23, `superseded` 3. | Finds transitional lifecycle usage for replacement-pointer review and later cleanup. |
| DRA-FM-005 | `rg -n '^status: superseded' docs --glob '*.md'` | `docs/90.references/learning/roadmap-v1.md:2` uses `status: superseded`. | Records reference-stage replacement-pointer follow-up. |
| DRA-FM-006 | `rg --no-filename -o '^status: [a-z-]+' docs/03.specs --glob '*.md' \| sort \| uniq -c` | Baseline: Stage 03 had `active` 17, `completed` 9, and `draft` 7. 2026-07-05 overlay: Stage 03 has `active` 19, `completed` 16, and `superseded` 2. | Feeds Stage 03 archive candidate report and later lifecycle cleanup evidence. |

## Key Inventory

| Key | Count | Profile Interpretation |
| --- | ---: | --- |
| `status` | 538 baseline; 569 in the 2026-07-05 lifecycle overlay | Primary lifecycle key for target docs and references. |
| `layer` | 176 | Agent/governance profile key. |
| `name`, `description`, `model`, `tools`, `permissionMode`, `conditions`, `pattern` | 224 combined | Provider and agent metadata profiles; do not normalize as document lifecycle keys. |
| `archived_from`, `archived_on`, `archive_reason`, `current_replacement` | 60 combined | Archive tombstone provenance keys. |
| `generated_by` | 1 | Generated reference metadata. |

## Findings

| ID | Surface | Finding | Disposition | Recommended Batch |
| --- | --- | --- | --- | --- |
| DRA-FM-001 | Full tracked Markdown corpus | 184 tracked Markdown files still omit top frontmatter; prior routing profile already classifies README, generated, GitHub-native, root, and archive profiles. | `evidence-preserve` | No broad rewrite in this audit pack. |
| DRA-FM-002 | `docs/90.references/learning/roadmap-v1.md` | `status: superseded` is an allowed transitional lifecycle value. The document points readers to the current `roadmap.md`, so no target edit is required in `PLN-DRA-003`. | `evidence-preserve` | Revisit only if a future reference cleanup changes Stage 90 archive policy. |
| DRA-FM-003 | Stage 03 docs | Baseline Stage 03 had 9 completed files and 7 draft files that needed candidate classification before archive or status cleanup. After the 2026-07-05 lifecycle cleanup, Stage 03 has no draft rows. | `historical-archive` / `evidence-preserve` / `completed` candidates | `PLN-DRA-004` plus 2026-07-05 lifecycle evidence refresh. |
| DRA-FM-004 | Provider/agent frontmatter keys | Provider metadata keys are numerous and profile-specific; they should not be forced into document lifecycle profiles. | `evidence-preserve` | No action unless provider contracts change. |

## Source Rules

- Use `frontmatter-contract.md` and `lifecycle-status.md` as active contracts.
- Treat provider metadata and archive provenance as distinct profiles.
- Do not bulk-add or bulk-normalize frontmatter for README, generated, root, or
  external-platform-native surfaces.
- Record lifecycle outliers or transitional status usages as gaps before
  changing them.

## Sources

- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) - Defines key ownership and lifecycle frontmatter boundaries.
- [Lifecycle status](../../../99.templates/support/lifecycle-status.md) - Defines lifecycle status values.
- [Frontmatter routing profile](../2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md) - Supplies current missing-frontmatter routing decisions.
- [Document restructure task evidence](../../../04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md) - Supplies the pre-audit baseline.

## Maintenance

- **Owner**: Documentation Specialist / QA Engineer.
- **Review Cadence**: Review before any broad frontmatter or lifecycle cleanup.
- **Update Trigger**: Update when Stage 99 frontmatter contracts change, a new
  lifecycle status is approved, or large path moves change the missing set.

## Related Documents

- [Document restructure audit references](./README.md)
- [Template contract drift](./template-contract-drift.md)
- [SDLC spec archive candidates](./sdlc-spec-archive-candidates.md)
- [Restructure gap register](./restructure-gap-register.md)
