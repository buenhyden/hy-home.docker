---
status: active
---

<!-- Target: docs/04.execution/plans/2026-07-04-document-restructure-audit-contract-archive.md -->

# Document Restructure Audit, Contract, and Archive Implementation Plan

> **For agentic workers:** Execute this plan one batch at a time. Create task
> evidence before any audit, contract, archive, operation-bucket, validator, or
> destructive move/delete work. Keep each batch in a separate logical commit.

## Overview

This plan turns the approved Stage 03 document restructure design into
executable work. The work starts with evidence-only audit reports, then updates
template and frontmatter contracts, and only then applies archive-centered
restructuring to historical `docs/03.specs` work products and historical
`docs/05.operations/{guides,policies,runbooks}` `01-*` buckets.

This plan does not perform the target restructure by itself. Implementation
tasks must record approved surfaces, before/after evidence, rollback paths,
redaction boundaries, validation results, and final dispositions.

## Context

The repository already completed a workspace document contract audit pack and a
first remediation pass. The next approved wave is narrower but more
destructive: classify historical work products, archive completed history by
default, remove duplicate or conflicting active guidance when a canonical
replacement exists, and strengthen Stage 99 support contracts so README files
remain routing/index surfaces rather than policy owners.

The approved design is in
`docs/03.specs/document-restructure-audit-contract-archive/spec.md`. It uses
external documentation-structure, SDLC, CI/CD, QA, and formatting sources as
supporting rationale while keeping repository-local Stage 00 and Stage 99
documents as policy owners.

## Goals & In-Scope

- **Goals**:
  - Create a Stage 90 audit pack under
    `docs/90.references/audits/document-restructure/`.
  - Classify template/frontmatter drift, `docs/03.specs` historical work
    products, operations bucket documents, and CI/QA/formatting coverage with
    stable dispositions.
  - Update Stage 99 support contracts for archive-centered restructure rules
    before destructive target moves.
  - Archive completed historical work products by default and remove duplicate
    or conflicting active guidance only with replacement/gap evidence.
  - Keep guide, policy, and runbook roles separate while restructuring
    historical operations `01-*` buckets.
  - Record all residual gaps, protected-surface decisions, validation results,
    and follow-up ownership.
- **In Scope**:
  - `docs/04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md`
  - `docs/90.references/audits/document-restructure/**`
  - `docs/99.templates/support/*.md` when contract changes are needed
  - minimal `docs/00.agent-governance/**` updates only for agent-facing or
    stage-authoring rules
  - approved historical work-product moves/removals under `docs/03.specs/**`
  - approved historical bucket moves/removals under
    `docs/05.operations/guides/{01-*...}`,
    `docs/05.operations/policies/{01-*...}`, and
    `docs/05.operations/runbooks/{01-*...}`
  - `docs/98.archive/**` archive tombstones and provenance records
  - validators or CI/QA documentation only when audit evidence and approval
    justify them
  - `docs/90.references/llm-wiki/llm-wiki-index.md`
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not rewrite the full Markdown corpus as a style cleanup.
  - Do not move or delete active guidance without audit disposition, canonical
    replacement, tombstone, or gap evidence.
  - Do not merge guide, policy, and runbook roles into one document type.
  - Do not add CI hard gates until a separate validator/CI batch proves the
    rule is stable and approved.
  - Do not make external sources direct repository policy owners.
- **Out of Scope**:
  - runtime Docker Compose changes unless a later infra-specific task is
    explicitly approved
  - secret values, credentials, tokens, certificates, private keys, shell
    history, raw logs, and `.env` values
  - remote GitHub setting mutation
  - provider runtime configuration changes
  - generated output rewrites unless the generator is intentionally changed in
    an approved batch
  - completed historical evidence rewrites that are not active guidance

## Work Breakdown

| Task ID | Description | Files / Docs Affected | Source Criteria | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-DRA-001 | Create task evidence and current baseline. | Stage 04 task evidence, progress memory | VAL-DRA-001, VAL-DRA-002 | Task evidence records approved surfaces, redaction boundaries, baseline path counts, and no target moves yet. |
| PLN-DRA-002 | Build the evidence-only audit pack. | `docs/90.references/audits/document-restructure/**`, audit indexes | VAL-DRA-002, VAL-DRA-003 | Audit reports exist, classify every target row with a stable disposition, and do not mutate target-stage documents. |
| PLN-DRA-003 | Update template, frontmatter, lifecycle, archive, and governance contracts. | Stage 99 support docs; minimal Stage 00 rules if needed | VAL-DRA-003, VAL-DRA-004 | Contract changes define archive-centered restructure rules and keep README policy out of README files. |
| PLN-DRA-004 | Execute approved `docs/03.specs` archive/remove/relink batch. | `docs/03.specs/**`, `docs/98.archive/**`, related README links | VAL-DRA-002, VAL-DRA-003 | Historical specs are archived/removed only after active links, replacements, and tombstones are synchronized. |
| PLN-DRA-005 | Execute approved operations bucket restructure batch. | `docs/05.operations/{guides,policies,runbooks}/01-*`, `docs/98.archive/**`, related README links | VAL-DRA-002, VAL-DRA-003 | Guide/policy/runbook roles remain separate and duplicate/conflicting active guidance is removed or archived with evidence. |
| PLN-DRA-006 | Decide validator, CI/CD, QA, and formatting enforcement. | `.github/workflows/**`, `scripts/validation/**`, Stage 99 support, audit reports | VAL-DRA-004, VAL-DRA-005 | Stable local checks are added only with approval; risky CI hard gates remain documented future work. |
| PLN-DRA-007 | Close evidence and residual gaps. | task evidence, audit gap register, progress memory, LLM Wiki | VAL-DRA-001 through VAL-DRA-005 | Final dispositions, validation results, residual gaps, and commit trail are recorded. |

## Batch Approval Gates

| Batch | Required Approval Before Editing | Protected Boundary |
| --- | --- | --- |
| Audit pack | Approval for evidence-only Stage 90 report creation | Do not move, delete, or normalize target-stage documents in the audit batch. |
| Stage 99 contracts | Approval for template/support contract changes | Do not make README files durable policy owners. |
| Stage 00 governance | Approval when an agent-facing rule or stage-authoring rule changes | Keep provider-local surfaces as adapters to Stage 00 and Stage 99 owners. |
| `docs/03.specs` archive/remove | Approval after candidate report identifies exact files and dispositions | Preserve replacement links, tombstones, and gap rows before removing active guidance. |
| Operations bucket restructure | Approval after candidate report identifies exact guide/policy/runbook files | Do not merge guide, policy, and runbook roles. |
| Validator/CI/QA/formatting | Explicit script/workflow/CI approval | Do not add credential-dependent or noisy hard gates without rollback guidance. |
| Infra/runtime | Separate infra approval | Do not change Compose, images, hardening scripts, or runtime provider config in documentation batches. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-DRA-PLAN-001 | Hygiene | Check whitespace in the current diff. | `git diff --check` | Zero exit status. |
| VAL-DRA-PLAN-002 | LLM Wiki | Verify generated tracked path index freshness. | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-DRA-PLAN-003 | Provider Surface | Verify generated provider surfaces after governance/provider-adjacent edits. | `bash scripts/operations/sync-provider-surfaces.sh --check` | PASS or approved generated drift committed in the same batch. |
| VAL-DRA-PLAN-004 | Traceability | Validate execution and operations traceability. | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-DRA-PLAN-005 | Implementation Alignment | Validate active docs against tracked implementation surfaces. | `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS with `failures=0`. |
| VAL-DRA-PLAN-006 | Repo Contract Syntax | Validate repo-contract script syntax. | `bash -n scripts/validation/check-repo-contracts.sh` | Zero exit status. |
| VAL-DRA-PLAN-007 | Repo Contracts | Validate repository documentation and Docker contracts. | `bash scripts/validation/check-repo-contracts.sh` | PASS, or any failure is recorded as out-of-scope residual drift with owner and follow-up. |
| VAL-DRA-PLAN-008 | Archive Links | Verify active documents do not link directly to deprecated active paths after archive moves. | `bash scripts/validation/check-doc-implementation-alignment.sh` plus targeted `rg` from task evidence | No unreviewed active links point to removed or archived targets. |
| VAL-DRA-PLAN-009 | Candidate Dispositions | Confirm every moved/removed target has a disposition row. | `rg -n 'DRA-GAP-|DRA-[0-9]{3}' docs/90.references/audits/document-restructure` | Every touched target has evidence, disposition, and batch owner. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Destructive cleanup removes active guidance. | High | Require audit disposition, replacement or gap row, tombstone/provenance, and link synchronization before delete/move. |
| Historical evidence is rewritten as if it were current drift. | High | Classify `evidence-preserve` separately and create explanatory audit notes instead of rewriting old records. |
| README files become contract documents. | Medium | Keep README edits limited to routing/index updates and move durable rules into Stage 99 support docs. |
| Operations roles collapse during bucket cleanup. | Medium | Keep guide, policy, and runbook targets separate and validate each role against its template contract. |
| Validator changes become noisy or unstable. | Medium | Keep new checks manual/advisory until a stable repo-local command proves low false-positive risk. |
| External-source rationale overrides repo policy. | Medium | Cite external sources only as rationale and keep Stage 00/99 as policy owners. |
| LLM Wiki or generated surfaces drift after moves. | Medium | Regenerate tracked indexes and provider surfaces in the same logical batch when paths change. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Run the verification plan for every batch before
  committing.
- **Sandbox / Canary Rollout**: N/A for pure documentation evidence. For
  validators, scripts, workflows, or infra-adjacent changes, run the narrow
  local check before full repo contracts.
- **Human Approval Gate**: Required before destructive move/delete batches,
  workflow/script/validator changes, remote GitHub mutation, provider runtime
  changes, secret-adjacent edits, or runtime infra changes.
- **Rollback Trigger**: Revert the latest logical batch commit if validation
  fails because of that batch or if an active link target is lost.
- **Prompt / Model Promotion Criteria**: N/A. Provider or agent-facing text
  changes must defer to Stage 00/99 owners and must not alter credentials or
  runtime model selection.

## Completion Criteria

- [ ] Task evidence exists before target-stage mutation begins.
- [ ] Stage 90 audit reports classify template/frontmatter drift, historical
      specs, operations buckets, CI/QA/formatting coverage, and residual gaps.
- [ ] Stage 99 support contracts define archive-centered template/frontmatter
      and destructive-change rules before archive/remove batches run.
- [ ] Approved historical `docs/03.specs` targets are archived/removed/relinked
      with tombstone or gap evidence.
- [ ] Approved operations `01-*` bucket targets are archived/removed/relinked
      without collapsing guide/policy/runbook roles.
- [ ] Validator, CI/CD, QA, and formatting decisions are either implemented
      with stable checks or recorded as future hardening candidates.
- [ ] LLM Wiki, progress memory, task evidence, and audit gap register reflect
      the final state.
- [ ] Required validation commands pass or any residual failure is recorded as
      out-of-scope with owner and follow-up.

## Related Documents

- **Spec**: [Document restructure design spec](../../03.specs/document-restructure-audit-contract-archive/spec.md)
- **Spec README**: [Document restructure design README](../../03.specs/document-restructure-audit-contract-archive/README.md)
- **Task Evidence Target**: `docs/04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md` created by `PLN-DRA-001`
- **Prior Audit Pack Plan**: [Workspace document contract audit pack plan](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Prior Remediation Plan**: [Document contract remediation batch plan](./2026-07-03-document-contract-remediation-batches.md)
- **Template Contract**: [Template contract](../../99.templates/support/template-contract.md)
- **Frontmatter Contract**: [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- **Template Governance**: [Template governance](../../99.templates/support/template-governance.md)
- **Template Selection**: [Template selection](../../99.templates/support/template-selection.md)
- **Lifecycle Status**: [Lifecycle status](../../99.templates/support/lifecycle-status.md)
- **Stage Authoring Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Repository Contract Validator**: [repo contract validator](../../../scripts/validation/check-repo-contracts.sh)
