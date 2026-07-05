---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md -->

# Reference: Restructure Gap Register

## Overview

This register consolidates the document restructure audit findings into stable
`DRA-GAP-*` rows. It records implementation closure and preserves future
triggers without applying new target document changes.

## Purpose

Future document restructure batches need a single reference for contract gaps,
candidate archive surfaces, operations bucket review, validation decisions,
closed rows, and out-of-scope residual triggers. This register provides that
handoff.

## Repository Role

This report supports Stage 04 task evidence and later implementation batches.
It is not active policy, not a template contract, not a validator
specification, and not approval to edit Stage 99 support docs, validators,
workflows, provider runtime config, runtime infrastructure, or target document
corpus.

## Scope

### In Scope

- Findings from the document restructure audit reports.
- Stable gap identifiers and recommended implementation batches.
- Dispositions aligned with the approved design:
  `active-canonical`, `historical-archive`, `duplicate-remove`,
  `conflict-remove-or-archive`, and `evidence-preserve`.

### Out of Scope

- Applying any target corpus fixes during this audit pack.
- Reading or printing secret values, credentials, tokens, private keys, raw
  logs, shell history, or `.env` values.
- Editing workflows, scripts, validators, provider adapters, runtime config, or
  remote GitHub settings.

## Definitions / Facts

- **`active-canonical`**: current source of truth or current guide/spec/policy
  that should remain active.
- **`historical-archive`**: completed historical work product that may leave
  the active chain after replacement and tombstone evidence.
- **`duplicate-remove`**: same role is covered by a canonical document and may
  be removed after link synchronization.
- **`conflict-remove-or-archive`**: document contradicts a current contract or
  implementation and needs replacement, tombstone, or gap evidence.
- **`evidence-preserve`**: audit, task, baseline, or historical evidence whose
  wording should remain faithful.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| DRA-GR-001 | Reads of all reports in this pack | Findings were deduplicated into stable `DRA-GAP-*` rows. | Register construction. |
| DRA-GR-002 | Reads of the approved design spec, implementation plan, and task evidence | Confirms audit-only boundaries and batch sequencing. | Prevents target edits in `PLN-DRA-002`. |
| DRA-GR-003 | Validation command list from plan/task evidence | Confirms required validation gates for future batches. | Future batch handoff. |

## Gap Summary

| Disposition | Count | Summary |
| --- | ---: | --- |
| `active-canonical` | 7 | Current template, operations, CI/QA, Stage 03, and current design surfaces remain active; the operations bucket scope correction is closed. |
| `historical-archive` | 0 | Stage 03 review found no current conflicting target that should become a tombstone in this batch. |
| `duplicate-remove` | 0 | No duplicate-remove decision is justified before deeper candidate comparison. |
| `conflict-remove-or-archive` | 0 | No current row requires conflict removal after the Stage 99 contract update; future target batches may add exact file-level decisions. |
| `evidence-preserve` | 5 | Historical audit/spec evidence, provider metadata, transitional reference status, Graphify/dependency-audit decisions, and operations bucket evidence are preserved. |
| **Total** | **12** | Consolidated rows from `PLN-DRA-002`, reclassified and closed or accepted through `PLN-DRA-007`. |

## Gap Register

| ID | Surface | Gap or Finding | Disposition | Recommended Batch | Evidence |
| --- | --- | --- | --- | --- | --- |
| DRA-GAP-001 | Stage 99 support contracts | Closed: Stage 99 support docs now own archive-centered dispositions and destructive target-change preconditions. | `active-canonical` | Done in `PLN-DRA-003` | [Template contract drift](./template-contract-drift.md) |
| DRA-GAP-002 | `archive.template.md` and archive guidance | Closed: archive tombstones remain a format template, while disposition conditions are owned by support contracts. | `active-canonical` | Done in `PLN-DRA-003` | [Template contract drift](./template-contract-drift.md) |
| DRA-GAP-003 | Tracked Markdown frontmatter | Accepted residual: 184 tracked Markdown files omit top frontmatter; prior routing says this is not a broad rewrite trigger. | `evidence-preserve` | Accepted in `PLN-DRA-007`; revisit only if contract changes. | [Frontmatter profile inventory](./frontmatter-profile-inventory.md) |
| DRA-GAP-004 | `docs/90.references/learning/roadmap-v1.md` | Accepted residual: `status: superseded` is an allowed transitional lifecycle value, and this document points to the current `roadmap.md`. | `evidence-preserve` | Accepted in `PLN-DRA-007`; revisit only if Stage 90 archive policy changes. | [Frontmatter profile inventory](./frontmatter-profile-inventory.md) |
| DRA-GAP-005 | Completed `docs/03.specs` files | Closed: completed Stage 03 specs were reviewed and retained as evidence or active inputs; no archive tombstone was justified. | `evidence-preserve` | Done in `PLN-DRA-004` | [SDLC spec archive candidates](./sdlc-spec-archive-candidates.md) |
| DRA-GAP-006 | Draft `docs/03.specs` files | Closed: current and implemented draft rows were reclassified; the agentic-engineering audit-pack design intentionally remains draft. | `active-canonical` / `evidence-preserve` | Done in `PLN-DRA-004` | [SDLC spec archive candidates](./sdlc-spec-archive-candidates.md) |
| DRA-GAP-007 | Current document restructure spec | Closed: current design spec and README are active for this wave. | `active-canonical` | Done in `PLN-DRA-004` | [SDLC spec archive candidates](./sdlc-spec-archive-candidates.md) |
| DRA-GAP-008 | Operations bucket taxonomy | Closed: the full `00-workspace`, `01-*` through `12-*`, and legacy `90-knowledge` surface was reviewed; only the legacy LLM Wiki maintenance bucket required movement. | `active-canonical` / evidence-preserve | Done in `PLN-DRA-005` | [Operations bucket restructure](./operations-bucket-restructure.md) |
| DRA-GAP-009 | Operations guide/policy/runbook roles | Closed: guide, policy, and runbook roles stayed separate while LLM Wiki maintenance moved from `90-knowledge` into `00-workspace`. | `active-canonical` / resolved historical bucket | Done in `PLN-DRA-005` | [Operations bucket restructure](./operations-bucket-restructure.md) |
| DRA-GAP-010 | CI/CD and QA gates | Closed for this wave: existing gates cover the restructure validation set; dependency-audit and Graphify hard gates remain future Security/QA candidates. | `evidence-preserve` / future hardening candidate | Done in `PLN-DRA-006`; future gate work requires a new exact approval. | [CI, QA, and formatting contract](./ci-qa-formatting-contract.md) |
| DRA-GAP-011 | Workflow and validator surfaces | Closed for this wave: workflow and script surfaces stayed protected and unchanged. | `active-canonical` | Done in `PLN-DRA-006`; future mutation must update workflow, ruleset, governance, and repo-contract coupling together. | [CI, QA, and formatting contract](./ci-qa-formatting-contract.md) |
| DRA-GAP-012 | Historical evidence | Accepted residual: prior audit reports and completed work products should not be rewritten for style alone. | `evidence-preserve` | Accepted in `PLN-DRA-007`; preserve unless active-consumption conflict is proven. | [Template contract drift](./template-contract-drift.md), [SDLC spec archive candidates](./sdlc-spec-archive-candidates.md) |

## Future Implementation Batches

| Batch | Rows | Required Approval | Validation Focus |
| --- | --- | --- | --- |
| `PLN-DRA-003` template contracts | DRA-GAP-001, DRA-GAP-002 | Complete | Stage 99 contract diff, provider sync if Stage 00/provider text changes, repo contracts. |
| `PLN-DRA-004` Stage 03 archive/remove | DRA-GAP-005, DRA-GAP-006, DRA-GAP-007, DRA-GAP-012 | Complete | Link synchronization, status cleanup, no tombstone needed, LLM Wiki, doc implementation alignment. |
| `PLN-DRA-005` operations bucket restructure | DRA-GAP-008, DRA-GAP-009 | Complete | Role separation, operations links, LLM Wiki regeneration, doc traceability, repo contracts. |
| `PLN-DRA-006` validator/CI/QA | DRA-GAP-010, DRA-GAP-011 | Complete | Current gates preserved; dependency-audit and Graphify hard gates deferred with future approval requirements. |
| `PLN-DRA-007` closure | DRA-GAP-003, DRA-GAP-004, DRA-GAP-012, all closed rows | Complete | Final evidence, residual trigger posture, progress memory, LLM Wiki, and commit trail. |
| Reference lifecycle cleanup | DRA-GAP-004 | Not required by current contract | Preserve unless a future Stage 90 archive-policy change requires a targeted diff. |

## Remediation Updates

| Date | Rows | Status | Evidence | Residual Action |
| --- | --- | --- | --- | --- |
| 2026-07-04 | DRA-GAP-001, DRA-GAP-002 | Closed by `PLN-DRA-003` | Stage 99 support contract updates in `template-governance.md`, `template-selection.md`, `lifecycle-status.md`, `frontmatter-contract.md`, and `template-contract.md`. | Use `PLN-DRA-004` and `PLN-DRA-005` for exact target archive, remove, or relink work. |
| 2026-07-04 | DRA-GAP-004 | Reclassified | `lifecycle-status.md` clarifies `superseded`; `roadmap-v1.md` already points to `roadmap.md`. | No current target edit. |
| 2026-07-04 | DRA-GAP-005, DRA-GAP-006, DRA-GAP-007 | Closed by `PLN-DRA-004` | Stage 03 candidate review updated status/routing for current, completed, draft, and superseded spec surfaces without removing active evidence. | No Stage 03 tombstone created; future archive requires a new conflict or duplicate row. |
| 2026-07-04 | DRA-GAP-008, DRA-GAP-009 | Closed by `PLN-DRA-005` | LLM Wiki maintenance guide, policy, and runbook moved from legacy `90-knowledge` buckets to `00-workspace`; empty tracked legacy bucket README indexes were removed. | No remaining `90-knowledge` tracked Markdown leaf; future operations cleanup requires a new exact candidate row. |
| 2026-07-04 | DRA-GAP-010, DRA-GAP-011 | Closed by `PLN-DRA-006` | CI/QA decision preserves current hard/local gates and records dependency-audit and Graphify hard gates as future candidates only. | Future workflow/script mutation requires exact approval, threshold/exception design, and rollback guidance. |
| 2026-07-04 | DRA-GAP-003, DRA-GAP-004, DRA-GAP-012 | Accepted residuals by `PLN-DRA-007` | Closure evidence records these as non-blocking trigger conditions rather than active implementation gaps. | Reopen only with a changed contract, changed Stage 90 lifecycle policy, or exact active-consumption conflict evidence. |

## Source Rules

- Preserve the audit reports as evidence and use this register for future
  batch routing.
- Do not treat a gap row as approval to mutate a protected surface.
- Do not move or remove active documents without a replacement, tombstone, and
  link synchronization plan.
- Do not rewrite historical evidence for style-only reasons.

## Sources

- [Template contract drift](./template-contract-drift.md) - Supplies Stage 99 disposition contract findings.
- [Frontmatter profile inventory](./frontmatter-profile-inventory.md) - Supplies frontmatter and lifecycle findings.
- [SDLC spec archive candidates](./sdlc-spec-archive-candidates.md) - Supplies Stage 03 candidate findings.
- [Operations bucket restructure](./operations-bucket-restructure.md) - Supplies operations bucket findings and `PLN-DRA-005` closure evidence.
- [CI, QA, and formatting contract](./ci-qa-formatting-contract.md) - Supplies automation findings.
- [Document restructure implementation plan](../../../04.execution/plans/2026-07-04-document-restructure-audit-contract-archive.md) - Supplies batch boundaries.
- [Document restructure task evidence](../../../04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md) - Supplies execution evidence.

## Maintenance

- **Owner**: Documentation Specialist / Repository Maintainer.
- **Review Cadence**: Review before each future DRA implementation batch.
- **Update Trigger**: Update when a `DRA-GAP-*` row is fixed, reclassified,
  deferred, or split into a narrower follow-up.

## Related Documents

- [Document restructure audit references](./README.md)
- [Document restructure design spec](../../../03.specs/103-document-restructure-audit-contract-archive/spec.md)
- [Document restructure implementation plan](../../../04.execution/plans/2026-07-04-document-restructure-audit-contract-archive.md)
- [Document restructure task evidence](../../../04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md)
