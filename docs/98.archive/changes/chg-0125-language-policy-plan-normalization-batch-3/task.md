---
status: archived
artifact_id: task-0125-01
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-3.md
archived_at: 2026-08-11
archive_reason: "Move baseline completed source to stable typed target docs/98.archive/changes/chg-0125-language-policy-plan-normalization-batch-3/task.md; migrate 5 resolved inbound link(s) with it."
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: a039288bfeb8b1b32e5cc01e4a511c929a1a05b0
preservation_class: git-history
---
<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-3.md -->

# Task: Language Policy Plan Normalization Batch 3

## Overview

This task records the third bounded `docs/04.execution/plans` implementation
pass for the repository language policy goal. It normalizes 7 additional plan
documents to English-only content while preserving historical execution meaning,
commands, path evidence, and verification boundaries.

## Inputs

- **User Objective**: Close remaining risks and follow-up tasks for the
  repository language policy work in bounded, commit-sized units.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Plan Normalization Batch 2](../chg-0124-language-policy-plan-normalization-batch-2/task.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- `docs/04.execution/plans/**` leaf documents are English-only execution plans.
- Preserve commands, paths, service names, agent names, evidence IDs, Docker
  profiles, environment variables, image names, upstream terms, runtime values,
  no-touch boundaries, and historical audit numbers exactly.
- Treat stale Graphify output as advisory only; corroborate against tracked
  source files and validators.
- Keep this task evidence English-only because `docs/04.execution/tasks/**`
  is an English-only execution evidence surface.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/04.execution/plans` bounded leaf batch | User-provided language policy objective and remaining-risk closure request | 7 plan files | `docs/04.execution/plans` leaf backlog was 38 files after plan batch 2 | 7 additional plan files have no Korean text; plan backlog is 31 files | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the third bounded `docs/04.execution/plans` leaf batch to English. | doc | User constraint / plans English-only | Plan normalization batch 3 | Korean-character scan against 7 target files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for plans and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Plan Files

The following English-only target files now have no Korean text:

- [Security Tier Documentation Standardization Implementation Plan](../chg-0004-03-security-standardization/plan.md)
- [Observability Standardization Plan](../chg-0007-06-observability-standardization/plan.md)
- [Docs Taxonomy and AI Agent-first Contract Migration Plan](../chg-0030-docs-taxonomy-agent-first-migration/plan.md)
- [Targeted Documentation Precision Remediation Plan](../chg-0037-targeted-docs-precision-remediation/plan.md)
- [Lifecycle README Debt Closure Plan](../chg-0040-lifecycle-readme-debt-closure/plan.md)
- [Workspace Docs and Agent Governance Remediation Plan](../chg-0042-workspace-docs-agent-governance-remediation/plan.md)
- [Workspace Governance Bounded Re-audit Implementation Plan](../chg-0043-workspace-governance-bounded-reaudit/plan.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the 7 normalized plan files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain after previous spec closure. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 31 leaf files remain after this batch. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 59 leaf files remain before task normalization. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/llm-wiki-index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - `rg -n` Korean-character scan against the 7 normalized plan files
  - `rg -n 'Overview \(KR\)' docs README.md AGENTS.md scripts -g '*.md' -g '*.sh'`
  - `git diff --check`
  - `bash scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
- **Eval Commands**: N/A for documentation language normalization.
- **Logs / Evidence Location**: This task and
  `docs/00.agent-governance/memory/progress.md`.

## Remaining Risks

- Full English-only normalization remains incomplete for execution surfaces:
  31 plan leaf files and 59 task leaf files still contain Korean text.
- Non-README `docs/90.references/**` documents were not bulk-polished in this
  batch.
- Hard Korean-character enforcement for English-only surfaces should wait until
  the active plan/task normalization backlog is closed.

## Follow-up Tasks

- Continue `docs/04.execution/plans/**` leaf normalization in bounded batches.
- Normalize `docs/04.execution/tasks/**` leaf documents to English while
  preserving historical evidence meaning.
- Review non-README `docs/90.references/**` documents for category language-rule
  consistency.
- After active normalization, add hard Korean-character enforcement for
  English-only surfaces.

## Related Documents

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](../chg-0118-language-policy-boundary-audit/task.md)
- **Plan Batch 1 Evidence**: [2026-06-05-language-policy-plan-normalization-batch-1.md](../chg-0123-language-policy-plan-normalization-batch-1/task.md)
- **Plan Batch 2 Evidence**: [2026-06-05-language-policy-plan-normalization-batch-2.md](../chg-0124-language-policy-plan-normalization-batch-2/task.md)
- **Task Index**: [README.md](../../../03.specs/README.md)
- **Plans Index**: [../plans/README.md](../../../03.specs/README.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
