---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md -->

# Task: Document Restructure Audit, Contract, and Archive

## Overview

This task records execution evidence for the document restructure audit,
contract, and archive wave. The first work unit creates the task evidence,
captures a current baseline, and preserves protected boundaries before any
audit-report creation, contract edit, archive move, duplicate removal, validator
change, or operations bucket restructure begins.

## Inputs

- **Parent Spec**: [Document restructure design spec](../../03.specs/document-restructure-audit-contract-archive/spec.md)
- **Parent Plan**: [Document restructure implementation plan](../plans/2026-07-04-document-restructure-audit-contract-archive.md)
- **Prior Audit Pack Task**: [Workspace document contract audit pack task](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Prior Remediation Task**: [Document contract remediation batch task](./2026-07-03-document-contract-remediation-batches.md)
- **Template Contract**: [Template contract](../../99.templates/support/template-contract.md)
- **Frontmatter Contract**: [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- **Template Governance**: [Template governance](../../99.templates/support/template-governance.md)
- **Stage Authoring Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- Execute one plan batch at a time and keep each batch in a separate commit.
- Audit before contract edits, and contract before destructive target moves.
- Do not move, delete, or rewrite target-stage documents in `PLN-DRA-001`.
- Do not inspect secret values, credentials, tokens, certificates, private
  keys, raw logs, shell history, or `.env` values.
- Keep guide, policy, and runbook roles separate during future operations
  bucket work.
- Treat README files as routing/index surfaces; durable rules belong in Stage
  99 support contracts.
- Record every future move, removal, archive, validator, or protected-surface
  edit with before/after evidence and rollback guidance before committing it.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md` | Approved Stage 03 spec, Stage 04 plan, and user continuation | Execution evidence | File absent before `PLN-DRA-001` | Task evidence created with baseline and protected boundaries | `git revert` the task-evidence commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `docs/04.execution/tasks/README.md` | Task-stage routing contract | Task index | Document restructure task not listed | Active task linked in structure and related documents | `git revert` the task-evidence commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `docs/90.references/audits/document-restructure/**` | Approved Stage 03 spec, Stage 04 plan, and user continuation | Evidence-only audit pack | Folder absent before `PLN-DRA-002` | Audit pack reports created and indexed | `git revert` the audit-pack commit | No target moves, no secret values, no credentials, no tokens, no private keys, no raw logs, no shell history, and no `.env` values |
| `docs/90.references/audits/README.md`; `docs/90.references/README.md` | Reference-stage index contract | Reference routing | Document restructure audit pack not listed | New audit pack linked from reference indexes | `git revert` the audit-pack commit | Path metadata only; no secret values or runtime logs |
| `docs/99.templates/support/{template-governance.md,template-selection.md,lifecycle-status.md,frontmatter-contract.md,template-contract.md,README.md}` | `PLN-DRA-003` Stage 99 support contract batch | Template support contracts | Disposition and destructive-change rules were recorded as `DRA-GAP-001` and `DRA-GAP-002` | Support docs own archive-centered dispositions, destructive target-change preconditions, lifecycle semantics, archive metadata boundaries, and target cleanup rules | `git revert` the Stage 99 contract batch commit | No target moves, no secret values, no credentials, no tokens, no private keys, no raw logs, no shell history, and no `.env` values |
| `docs/90.references/audits/document-restructure/{template-contract-drift.md,frontmatter-profile-inventory.md,restructure-gap-register.md}` | `PLN-DRA-003` evidence update | Audit register maintenance | Audit pack still showed pre-contract gaps and one `superseded` conflict classification | Gap rows reclassified after the Stage 99 contract update; no target document edited | `git revert` the Stage 99 contract batch commit | Evidence-only updates; no target moves and no secret values |
| `docs/90.references/llm-wiki/llm-wiki-index.md` | LLM Wiki generated index contract | Tracked path index | Prior generated path index from previous batch | Index regenerated after staging current batch changes | Rerun `bash scripts/knowledge/generate-llm-wiki-index.sh` after revert | Path metadata only; no secret values or raw runtime logs |
| `docs/00.agent-governance/memory/progress.md` | Governance memory contract | Progress memory | `PLN-DRA-003` not recorded | Stage 99 contract batch recorded after validation | `git revert` the Stage 99 contract batch commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| Future target documents | Parent plan approval gates | `docs/03.specs/**`, `docs/05.operations/**`, `docs/98.archive/**`, validators, workflows | No target moves, removals, validator changes, or workflow changes through `PLN-DRA-003` | Future batches must add per-surface evidence before edits | Revert only the future batch commit that introduced the change | Redaction boundary must be restated before touching protected surfaces |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-DRA-001 | Create task evidence and current baseline. | doc | Implementation Handoff / Audit pack | PLN-DRA-001 | Baseline snapshot, protected surfaces, validation matrix | Codex | Done |
| T-DRA-002 | Build the evidence-only Stage 90 audit pack. | doc | Audit Pack Design | PLN-DRA-002 | `docs/90.references/audits/document-restructure/**` reports and gap register | Codex | Done |
| T-DRA-003 | Update template, frontmatter, lifecycle, archive, and governance contracts. | doc | Template Contract Baseline | PLN-DRA-003 | Stage 99 support contract diffs and audit register reclassification | Codex | Done |
| T-DRA-004 | Execute approved `docs/03.specs` archive/remove/relink batch. | doc | 03.specs Restructure Model | PLN-DRA-004 | Candidate dispositions, tombstones, link sync, validation | Codex | Planned |
| T-DRA-005 | Execute approved operations bucket restructure batch. | doc | Operations Bucket Restructure Model | PLN-DRA-005 | Guide/policy/runbook candidate dispositions, tombstones, link sync, validation | Codex | Planned |
| T-DRA-006 | Decide validator, CI/CD, QA, and formatting enforcement. | doc/test | CI/CD, QA, and Formatting Contract | PLN-DRA-006 | Stable check implementation or future-hardening decision record | Codex | Planned |
| T-DRA-007 | Close evidence and residual gaps. | doc | Verification / Success Criteria | PLN-DRA-007 | Final validation matrix, gap register, progress, LLM Wiki, commit trail | Codex | Planned |

## Baseline Snapshot

This baseline was captured before creating this task file and before any target
document restructure work.

| Measure | Command | Result |
| --- | --- | ---: |
| Tracked Markdown files | `git ls-files '*.md' \| wc -l` | 947 |
| Tracked `docs/03.specs` Markdown files | `git ls-files 'docs/03.specs/**/*.md' \| wc -l` | 51 |
| Tracked `docs/03.specs/**/spec.md` files | `git ls-files 'docs/03.specs/**/spec.md' \| wc -l` | 26 |
| `docs/03.specs` files with `status: active` | `rg --no-filename -o '^status: [a-z-]+' docs/03.specs --glob '*.md' \| sort \| uniq -c` | 17 |
| `docs/03.specs` files with `status: completed` | Same status scan | 9 |
| `docs/03.specs` files with `status: draft` | Same status scan | 7 |
| Operations `01-*` bucket directories | `find docs/05.operations/guides docs/05.operations/policies docs/05.operations/runbooks -type d -name '01-*' \| sort \| wc -l` | 3 |
| Tracked Markdown files directly under operations `01-*` buckets | `git ls-files 'docs/05.operations/guides/01-*/*.md' 'docs/05.operations/policies/01-*/*.md' 'docs/05.operations/runbooks/01-*/*.md' \| wc -l` | 10 |
| Existing `document-restructure` Stage 90 audit files | `git ls-files 'docs/90.references/audits/document-restructure/**' \| wc -l` | 0 |
| Task evidence file before this batch | `test -f docs/04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md` | Absent |

## Target Boundary Snapshot

The current operations `01-*` target buckets are:

- `docs/05.operations/guides/01-gateway`
- `docs/05.operations/policies/01-gateway`
- `docs/05.operations/runbooks/01-gateway`

Tracked Markdown files directly under those buckets:

- `docs/05.operations/guides/01-gateway/01.setup.md`
- `docs/05.operations/guides/01-gateway/README.md`
- `docs/05.operations/guides/01-gateway/nginx.md`
- `docs/05.operations/guides/01-gateway/traefik.md`
- `docs/05.operations/policies/01-gateway/README.md`
- `docs/05.operations/policies/01-gateway/nginx.md`
- `docs/05.operations/policies/01-gateway/traefik.md`
- `docs/05.operations/runbooks/01-gateway/README.md`
- `docs/05.operations/runbooks/01-gateway/nginx.md`
- `docs/05.operations/runbooks/01-gateway/traefik.md`

`PLN-DRA-001` does not classify, move, delete, archive, or rewrite these
targets. The future audit pack must classify them before any target mutation.

## Phase View

### Phase 1: Evidence Seed

- [x] T-DRA-001 Create task evidence and current baseline.

### Phase 2: Evidence-Only Audit

- [x] T-DRA-002 Build the Stage 90 audit pack before contract or target edits.

### Phase 3: Contract and Target Batches

- [x] T-DRA-003 Update Stage 99 support contracts and minimal Stage 00 rules if needed.
- [ ] T-DRA-004 Execute approved `docs/03.specs` archive/remove/relink batch.
- [ ] T-DRA-005 Execute approved operations bucket restructure batch.
- [ ] T-DRA-006 Decide validator, CI/CD, QA, and formatting enforcement.
- [ ] T-DRA-007 Close evidence and residual gaps.

## Validation Results

| Scope | Command | Result |
| --- | --- | --- |
| Template-token scan | Focused `rg` scan for unresolved template tokens in the audit reports and task evidence. | PASS: no matches. |
| Whitespace | `git diff --check` | PASS: no whitespace errors. |
| LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS: generated LLM Wiki index is fresh. |
| Provider surfaces | `bash scripts/operations/sync-provider-surfaces.sh --check` | PASS: `sync-provider-surfaces: no drift`. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` | PASS: `failures=0`. |
| Implementation alignment | `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS: `stage_docs_total=556`, links checked `4218`, `failures=0`. |
| Repo contract syntax | `bash -n scripts/validation/check-repo-contracts.sh` | PASS: shell syntax is valid. |
| Full repo contracts | `bash scripts/validation/check-repo-contracts.sh` | PASS: `changed_template_docs_total=4`, `target_stage_docs_total=620`, `failures=0`. |

## Implementation Notes

- T-DRA-002 created the evidence-only audit pack under
  `docs/90.references/audits/document-restructure/`.
- The audit pack contains `README.md`, `template-contract-drift.md`,
  `frontmatter-profile-inventory.md`, `sdlc-spec-archive-candidates.md`,
  `operations-bucket-restructure.md`, `ci-qa-formatting-contract.md`, and
  `restructure-gap-register.md`.
- After T-DRA-003, the `DRA-GAP-*` register records 12 rows: 6
  active-canonical rows, 2 historical-archive candidate rows, 0
  duplicate-remove rows, 0 conflict-remove-or-archive candidate rows, and 4
  evidence-preserve rows.
- No `docs/03.specs/**`, `docs/05.operations/**`, Stage 99 support contract,
  validator, workflow, provider runtime, runtime infra, secret material, or
  archive tombstone target was modified in this audit-pack batch.
- The LLM Wiki index was regenerated with 1143 tracked paths after staging the
  new audit reports.
- T-DRA-003 updated Stage 99 support contracts so future archive, remove,
  relink, or tombstone batches must carry exact target paths, replacement
  pointers, link review, rollback guidance, and validation results.
- T-DRA-003 reclassified the `roadmap-v1.md` `superseded` evidence as an
  allowed transitional lifecycle use because the document points to
  `roadmap.md`.
- T-DRA-003 did not move, remove, archive, or relink any `docs/03.specs/**`,
  `docs/05.operations/**`, or `docs/98.archive/**` target document.

## Verification Summary

- **Test Commands**: Listed in `## Validation Results`.
- **Eval Commands**: N/A for task evidence and baseline documentation.
- **Logs / Evidence Location**: This task document, parent plan, progress
  memory, and generated LLM Wiki index.
- **Manual Checks**: Confirmed this batch creates task evidence and index
  routing only. No target-stage document moves, deletions, contract edits,
  validator changes, workflow changes, provider runtime changes, secret reads,
  archive tombstones, or audit-pack reports are included in `PLN-DRA-001`.

## Related Documents

- **Parent Spec**: [Document restructure design spec](../../03.specs/document-restructure-audit-contract-archive/spec.md)
- **Parent Plan**: [Document restructure implementation plan](../plans/2026-07-04-document-restructure-audit-contract-archive.md)
- **Prior Audit Pack Task**: [Workspace document contract audit pack task](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Prior Remediation Task**: [Document contract remediation batch task](./2026-07-03-document-contract-remediation-batches.md)
- **Template Contract**: [Template contract](../../99.templates/support/template-contract.md)
- **Frontmatter Contract**: [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- **Template Governance**: [Template governance](../../99.templates/support/template-governance.md)
- **Stage Authoring Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
