---
status: active
---

<!-- Target: docs/90.references/audits/document-restructure/restructure-gap-register.md -->

# Reference: Restructure Gap Register

## Overview

This register consolidates the document restructure audit findings into stable
`DRA-GAP-*` rows. It assigns recommended implementation batches without
applying target document changes.

## Purpose

Future document restructure batches need a single reference for contract gaps,
candidate archive surfaces, operations bucket review, validation decisions, and
out-of-scope residuals. This register provides that handoff.

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
| `active-canonical` | 5 | Current template, operations, CI/QA, and current design surfaces remain active. |
| `historical-archive` | 2 | Completed Stage 03 work products and prior template-system designs need archive review. |
| `duplicate-remove` | 0 | No duplicate-remove decision is justified before deeper candidate comparison. |
| `conflict-remove-or-archive` | 2 | Stage 99 disposition contract gap and one reference lifecycle outlier need future cleanup. |
| `evidence-preserve` | 3 | Historical audit/spec evidence, provider metadata, Graphify/dependency-audit decisions, and operations bucket evidence need preservation or future approval. |
| **Total** | **12** | Consolidated rows from `PLN-DRA-002`. |

## Gap Register

| ID | Surface | Gap or Finding | Disposition | Recommended Batch | Evidence |
| --- | --- | --- | --- | --- | --- |
| DRA-GAP-001 | Stage 99 support contracts | Approved archive-centered dispositions are not yet explicitly owned by Stage 99 support docs. | `conflict-remove-or-archive` candidate | `PLN-DRA-003` | [Template contract drift](./template-contract-drift.md) |
| DRA-GAP-002 | `archive.template.md` and archive guidance | Tombstone format exists, but conditions for historical archive, duplicate removal, and conflict archive are still design-level. | `active-canonical` with contract gap | `PLN-DRA-003` | [Template contract drift](./template-contract-drift.md) |
| DRA-GAP-003 | Tracked Markdown frontmatter | 184 tracked Markdown files omit top frontmatter; prior routing says this is not a broad rewrite trigger. | `evidence-preserve` | No target rewrite; revisit only if contract changes. | [Frontmatter profile inventory](./frontmatter-profile-inventory.md) |
| DRA-GAP-004 | `docs/90.references/learning/roadmap-v1.md` | `status: superseded` is outside current lifecycle vocabulary. | `conflict-remove-or-archive` candidate | Future reference lifecycle cleanup, not Stage 03/05 restructure. | [Frontmatter profile inventory](./frontmatter-profile-inventory.md) |
| DRA-GAP-005 | Completed `docs/03.specs` files | 9 completed Stage 03 files are historical archive or preserve candidates. | `historical-archive` / `evidence-preserve` candidates | `PLN-DRA-004` | [SDLC spec archive candidates](./sdlc-spec-archive-candidates.md) |
| DRA-GAP-006 | Draft `docs/03.specs` files | 7 draft Stage 03 files need status review before archive/completion decisions. | `historical-archive` / `active-canonical` / `evidence-preserve` candidates | `PLN-DRA-004` | [SDLC spec archive candidates](./sdlc-spec-archive-candidates.md) |
| DRA-GAP-007 | Current document restructure spec | Current design spec and README remain active for this wave. | `active-canonical` | No move in this wave. | [SDLC spec archive candidates](./sdlc-spec-archive-candidates.md) |
| DRA-GAP-008 | Operations `01-gateway` buckets | 3 bucket directories and 10 direct Markdown files require future candidate comparison. | `active-canonical` / restructure review | `PLN-DRA-005` | [Operations bucket restructure](./operations-bucket-restructure.md) |
| DRA-GAP-009 | Operations guide/policy/runbook roles | Leaf docs are active and role-specific; no duplicate-remove decision is justified yet. | `active-canonical` | Preserve roles in `PLN-DRA-005`. | [Operations bucket restructure](./operations-bucket-restructure.md) |
| DRA-GAP-010 | CI/CD and QA gates | Existing gates cover docs and repo contracts; new dependency-audit or Graphify hard gates require separate approval. | `evidence-preserve` / future hardening candidate | `PLN-DRA-006` only if approved. | [CI, QA, and formatting contract](./ci-qa-formatting-contract.md) |
| DRA-GAP-011 | Workflow and validator surfaces | Workflow/script changes are protected surfaces and should not be bundled with archive moves. | `active-canonical` | Keep separate if `PLN-DRA-006` proceeds. | [CI, QA, and formatting contract](./ci-qa-formatting-contract.md) |
| DRA-GAP-012 | Historical evidence | Prior audit reports and completed work products should not be rewritten for style alone. | `evidence-preserve` | Preserve unless active-consumption conflict is proven. | [Template contract drift](./template-contract-drift.md), [SDLC spec archive candidates](./sdlc-spec-archive-candidates.md) |

## Future Implementation Batches

| Batch | Rows | Required Approval | Validation Focus |
| --- | --- | --- | --- |
| `PLN-DRA-003` template contracts | DRA-GAP-001, DRA-GAP-002 | Stage 99 support contract approval | Stage 99 contract diff, provider sync if Stage 00/provider text changes, repo contracts. |
| `PLN-DRA-004` Stage 03 archive/remove | DRA-GAP-005, DRA-GAP-006, DRA-GAP-007, DRA-GAP-012 | Exact file list and archive/remove approval | Link synchronization, tombstones, LLM Wiki, doc implementation alignment. |
| `PLN-DRA-005` operations bucket restructure | DRA-GAP-008, DRA-GAP-009 | Exact guide/policy/runbook candidate approval | Role separation, operations links, doc traceability, repo contracts. |
| `PLN-DRA-006` validator/CI/QA | DRA-GAP-010, DRA-GAP-011 | Workflow/script/validator and Security/QA approval | `bash -n`, local QA gates, repo contracts, rollback guidance. |
| Reference lifecycle cleanup | DRA-GAP-004 | Reference-stage lifecycle decision | Lifecycle contract, targeted file diff, repo contracts. |

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
- [Operations bucket restructure](./operations-bucket-restructure.md) - Supplies operations `01-*` findings.
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
- [Document restructure design spec](../../../03.specs/document-restructure-audit-contract-archive/spec.md)
- [Document restructure implementation plan](../../../04.execution/plans/2026-07-04-document-restructure-audit-contract-archive.md)
- [Document restructure task evidence](../../../04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md)
