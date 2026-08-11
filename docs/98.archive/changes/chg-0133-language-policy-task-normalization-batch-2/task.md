---
status: archived
artifact_id: task-0133-01
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-2.md
archived_at: 2026-08-11
archive_reason: "Move baseline completed source to stable typed target docs/98.archive/changes/chg-0133-language-policy-task-normalization-batch-2/task.md; migrate 5 resolved inbound link(s) with it."
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: 5ee0b42bd2d0a36c668eab4806c083630e388666
preservation_class: git-history
---
<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-2.md -->

# Task: Language Policy Task Normalization Batch 2

## Overview

This task records the second bounded `docs/04.execution/tasks` normalization
pass for the repository language policy goal. It normalizes 12 additional task
leaf documents to English-only content while preserving historical execution
meaning, commands, path evidence, checklist state, and verification boundaries.

## Inputs

- **User Objective**: Continue applying repository language policy rules across
  AI-agent, human-facing, and mixed documentation surfaces.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Task Normalization Batch 1](../chg-0132-language-policy-task-normalization-batch-1/task.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- `docs/04.execution/tasks/**` leaf documents are English-only execution
  evidence records.
- Preserve commands, paths, service names, agent names, evidence IDs, Docker
  profiles, environment variables, image names, upstream terms, runtime values,
  no-touch boundaries, checklist state, and historical audit numbers exactly.
- Treat stale Graphify output as advisory only; corroborate against tracked
  source files and validators.
- Keep this task evidence English-only because `docs/04.execution/tasks/**`
  is an English-only execution evidence surface.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/04.execution/tasks` bounded leaf batch | User-provided language policy objective and continuation request | 12 task files | `docs/04.execution/tasks` leaf backlog was 39 files after task batch 1 | 12 additional task files have no Korean text; task backlog is 27 files | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the second bounded `docs/04.execution/tasks` leaf batch to English. | doc | User constraint / tasks English-only | Task normalization batch 2 | Korean-character scan against 12 target files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for specs, plans, and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Task Files

The following English-only target files now have no Korean text:

- [Infra / Secrets / Docs Refresh Task](../chg-0028-infra-secrets-docs-refresh/task.md)
- [Docs Taxonomy Agent-first Migration Task](../chg-0030-docs-taxonomy-agent-first-migration/task.md)
- [Home Docker Revalidation Deferred Follow-up Task](../chg-0047-home-docker-revalidation-deferred-follow-up/task.md)
- [Home Docker Workspace Audit Improvement Task](../chg-0048-home-docker-workspace-audit-improvement/task.md)
- [Large-scale Authored SSoT Review Task](../chg-0049-large-scale-authored-ssot-review/task.md)
- [Agent Governance Missing Items Implementation Task](../chg-0115-agent-governance-missing-items-implementation/task.md)
- [Agent Governance Phase 1 Revalidation Task](../chg-0056-agent-governance-phase-1-revalidation/task.md)
- [Agent Governance Phase 2 Strategy Integration Task](../chg-0057-agent-governance-phase-2-strategy-integration/task.md)
- [Agent Governance Phase 3 Approved Surface Activation Task](../chg-0058-agent-governance-phase-3-approved-surface-activation/task.md)
- [Agent Governance Phase 4 Closure Reconciliation Task](../chg-0059-agent-governance-phase-4-closure-reconciliation/task.md)
- [Docs Implementation Reconciliation Task](../chg-0060-docs-implementation-reconciliation/task.md)
- [Harness Engineering Task](../chg-0117-harness-engineering/task.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the 12 normalized task files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 27 leaf files remain after this batch. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/llm-wiki-index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - Korean-character scan against the 12 normalized task files
  - `rg -n 'Overview \(KR\)' docs README.md AGENTS.md scripts -g '*.md' -g '*.sh'`
  - `git diff --check`
  - `bash scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
- **Eval Commands**: N/A for documentation language normalization.
- **Logs / Evidence Location**: This task and
  `docs/00.agent-governance/memory/progress.md`.

## Remaining Risks

- Full English-only normalization remains incomplete for execution evidence:
  27 task leaf files still contain Korean text.
- Non-README `docs/90.references/**` documents were not bulk-polished in this
  batch.
- Hard Korean-character enforcement for English-only surfaces should wait until
  the active task normalization backlog is closed.

## Follow-up Tasks

- Continue `docs/04.execution/tasks/**` leaf normalization in bounded batches.
- Review non-README `docs/90.references/**` documents for category language-rule
  consistency.
- After active normalization, add hard Korean-character enforcement for
  English-only surfaces.

## Related Documents

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](../chg-0118-language-policy-boundary-audit/task.md)
- **Task Batch 1 Evidence**: [2026-06-05-language-policy-task-normalization-batch-1.md](../chg-0132-language-policy-task-normalization-batch-1/task.md)
- **Task Index**: [README.md](../../../03.specs/README.md)
- **Plans Index**: [../plans/README.md](../../../03.specs/README.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
