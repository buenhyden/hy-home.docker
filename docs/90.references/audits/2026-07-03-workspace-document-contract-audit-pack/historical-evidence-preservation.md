---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/historical-evidence-preservation.md -->

# Reference: Historical Evidence Preservation

## Overview

This reference records the T-006 preservation decision for `WDC-GAP-012`
through `WDC-GAP-015`. It closes the historical-evidence batch without
rewriting completed specifications, plans, tasks, archive tombstones, legacy
archive material, or historical progress rows.

## Purpose

The document-contract remediation plan needed a decision for gaps that point at
old baselines, completed execution evidence, archive records, and migration
history. This reference separates active contract drift from durable evidence
that should remain truthful to the repository state it originally recorded.

## Repository Role

This reference supports Stage 04 task evidence and the document-contract gap
register. It is not active template policy, not a replacement for Stage 99
contracts, not approval to rewrite historical files, and not a migration plan
for archive tombstones.

## Scope

### In Scope

- `WDC-GAP-012`: tracked README and README score baselines in audit reports.
- `WDC-GAP-013`: requirement section-profile counts used as baseline evidence.
- `WDC-GAP-014`: archive and legacy archive-heading records.
- `WDC-GAP-015`: old template-path mentions in completed specs, plans, tasks,
  and progress entries.
- Metadata-only review of tracked Markdown surfaces named by the gap register.

### Out of Scope

- Rewriting completed Stage 03 specifications or Stage 04 plans/tasks for
  style-only reasons.
- Rewriting `docs/98.archive/**` tombstones or `archive/**` legacy material.
- Editing old progress rows except by adding the current work-log entry.
- Reclassifying future active-guidance conflicts without new evidence.
- Reading secret values, `.env` values, credentials, tokens, certificates,
  private keys, raw logs, or shell history.

## Definitions / Facts

- **Historical evidence**: a tracked document row, baseline, tombstone, or
  progress entry that records what was true when the artifact was produced.
- **Active guidance**: a current contract, template, governance page, README,
  task, or script that readers or automation should follow today.
- **Preservation decision**: a decision to keep historical evidence unchanged
  because changing it would make the record less faithful and would not improve
  current workspace behavior.
- **Reclassification trigger**: proof that a specific historical artifact is
  still consumed as active guidance and conflicts with the current contract.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| HEP-001 | Reads of `frontmatter-inventory.md` and `readme-profile-inventory.md` | README totals, score distributions, and missing-frontmatter counts are audit baselines. | Confirms `WDC-GAP-012` is evidence, not a target rewrite. |
| HEP-002 | Read of `section-profile-inventory.md` | Requirement and archive section counts record the state of the corpus at inventory time. | Confirms `WDC-GAP-013` and `WDC-GAP-014` are baseline evidence. |
| HEP-003 | Read of `template-application-gaps.md` | Older specs, plans, tasks, and progress rows preserve old flat-template path history. | Confirms `WDC-GAP-015` is migration history. |
| HEP-004 | Historical evidence preservation scan across Stage 03, Stage 04, archive, and progress surfaces | Matches are completed, archived, tombstoned, or progress-log evidence. | Confirms no current-guidance rewrite was needed in T-006. |

## Preservation Matrix

| Gap | Source Surface | Decision | Reason | Future Cleanup Trigger |
| --- | --- | --- | --- | --- |
| `WDC-GAP-012` | `frontmatter-inventory.md`; `readme-profile-inventory.md` | Preserve. | These rows record audit baselines such as tracked Markdown totals, README totals, score distributions, and missing-frontmatter counts. | A new inventory run supersedes the old baseline. |
| `WDC-GAP-013` | `section-profile-inventory.md`; `docs/01.requirements/**/*.md` counts | Preserve. | Requirement section-profile counts were used as comparison evidence for the already completed PRD heading remediation. | A future requirements audit proves a current active PRD still conflicts with the template. |
| `WDC-GAP-014` | `docs/98.archive/**/*.md`; `archive/Windows-Network-IP.md` | Preserve. | Archive tombstones and legacy archive material document migration and historical structure. | A future archive/tombstone task proves active links or active guidance require cleanup. |
| `WDC-GAP-015` | `docs/03.specs/**`; `docs/04.execution/**`; `docs/00.agent-governance/memory/progress.md` | Preserve. | Old template-path mentions inside completed work products and progress rows are part of the evidence trail. | A future task proves a specific entry is active guidance consumed today. |

## Findings

- The four historical rows do not justify target-corpus remediation in this
  batch.
- Completed specs, plans, and tasks should remain faithful to the contract and
  template state in effect when they were produced.
- Archive tombstones and legacy archive documents should not be rewritten as a
  side effect of document-contract cleanup.
- Historical progress rows may mention old paths or prior states; those rows
  remain useful precisely because they preserve change history.
- Future cleanup should be narrow and evidence-led: identify the exact active
  consumer, the conflicting artifact, and the replacement contract before
  editing historical material.

## Source Rules

- Prefer current Stage 99 contracts and Stage 00 governance for active rules.
- Prefer historical reports, completed tasks, archive tombstones, and progress
  rows as evidence of past state, not as current instructions.
- Do not normalize old template paths inside completed evidence unless a future
  approved task proves active-consumption conflict.
- Keep preservation decisions separate from archive migration work.

## Sources

- [Frontmatter inventory](./frontmatter-inventory.md) - Supplies
  `WDC-GAP-012` audit-baseline evidence.
- [README profile inventory](./readme-profile-inventory.md) - Supplies
  `WDC-GAP-012` README baseline evidence.
- [Section profile inventory](./section-profile-inventory.md) - Supplies
  `WDC-GAP-013` and `WDC-GAP-014` baseline evidence.
- [Template application gaps](./template-application-gaps.md) - Supplies
  `WDC-GAP-015` old-template-path evidence.
- [Gap register](./gap-register.md) - Supplies dispositions and future
  implementation boundaries.
- [Document contract remediation task](../../../04.execution/tasks/2026-07-03-document-contract-remediation-batches.md) -
  Supplies T-006 execution evidence.

## Maintenance

- **Owner**: Documentation Specialist / Repository Maintainer.
- **Review Cadence**: Review only when a new inventory run, archive migration,
  or active-guidance conflict references one of the preserved surfaces.
- **Update Trigger**: Update when a future task reclassifies one of the
  historical rows with concrete active-consumption evidence.

## Related Documents

- [Document contract audit references](./README.md)
- [Gap register](./gap-register.md)
- [Document contract remediation task](../../../04.execution/tasks/2026-07-03-document-contract-remediation-batches.md)
