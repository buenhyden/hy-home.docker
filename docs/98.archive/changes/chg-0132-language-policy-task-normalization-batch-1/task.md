---
status: archived
artifact_id: task-0132-01
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-1.md
archived_at: 2026-08-11
archive_reason: "Move baseline completed source to stable typed target docs/98.archive/changes/chg-0132-language-policy-task-normalization-batch-1/task.md; migrate 5 resolved inbound link(s) with it."
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: 9ae867fe47eb9185ecce5bef9092fab45b88ec85
preservation_class: git-history
---
<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-1.md -->

# Task: Language Policy Task Normalization Batch 1

## Overview

This task records the first bounded `docs/04.execution/tasks` normalization
pass for the repository language policy goal. It normalizes 20 low-risk task
leaf documents to English-only content by translating one remaining overview or
evidence sentence in each file while preserving historical execution meaning,
commands, path evidence, checklist state, and verification boundaries.

## Inputs

- **User Objective**: Continue applying repository language policy rules across
  AI-agent, human-facing, and mixed documentation surfaces.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Plan Normalization Batch 8](../chg-0130-language-policy-plan-normalization-batch-8/task.md)
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
| `docs/04.execution/tasks` bounded leaf batch | User-provided language policy objective and continuation request | 20 task files | `docs/04.execution/tasks` leaf backlog was 59 files after closing the plan backlog | 20 additional task files have no Korean text; task backlog is 39 files | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the first bounded `docs/04.execution/tasks` leaf batch to English. | doc | User constraint / tasks English-only | Task normalization batch 1 | Korean-character scan against 20 target files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for specs, plans, and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Task Files

The following English-only target files now have no Korean text:

- [Tooling Tasks](../chg-0112-09-tooling/task.md)
- [Communication Tasks](../chg-0113-10-communication/task.md)
- [Laboratory Tasks](../chg-0114-11-laboratory/task.md)
- [AI Open WebUI Tasks](../chg-0013-08-ai-open-webui/task.md)
- [Infra Team Agent Cross-Validation Task](../chg-0026-infra-team-agent-cross-validation/task.md)
- [Harness Agent-first Engineering Task](../chg-0027-harness-agent-first-engineering/task.md)
- [Scripts Lifecycle Contract Cleanup Task](../chg-0029-scripts-lifecycle-contract-cleanup/task.md)
- [LLM Wiki Agent-first Completion Task](../chg-0031-llm-wiki-agent-first-completion/task.md)
- [Requirements Standardization Task](../chg-0032-requirements-standardization/task.md)
- [Scripts CI QA Cleanup Task](../chg-0033-scripts-ci-qa-cleanup/task.md)
- [Operations Purpose Remediation Task](../chg-0034-docs-05-operations-purpose-remediation/task.md)
- [Docs Bounded Consistency Audit Task](../chg-0035-docs-bounded-consistency-audit/task.md)
- [Execution Stage Remediation Task](../chg-0036-execution-stage-remediation/task.md)
- [Targeted Docs Precision Remediation Task](../chg-0037-targeted-docs-precision-remediation/task.md)
- [Agent Hook Completion and Style Automation Task](../chg-0038-agent-hook-completion-style-automation/task.md)
- [Data Analytics Execution Traceability Task](../chg-0039-data-analytics-execution-traceability/task.md)
- [Lifecycle README Debt Closure Task](../chg-0040-lifecycle-readme-debt-closure/task.md)
- [Spec Execution Implementation Audit Task](../chg-0041-spec-execution-implementation-audit/task.md)
- [Workspace Docs Agent Governance Remediation Task](../chg-0042-workspace-docs-agent-governance-remediation/task.md)
- [Workspace Governance Bounded Reaudit Task](../chg-0043-workspace-governance-bounded-reaudit/task.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the 20 normalized task files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 39 leaf files remain after this batch. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/llm-wiki-index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - Korean-character scan against the 20 normalized task files
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
  39 task leaf files still contain Korean text.
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
- **Final Plan Batch Evidence**: [2026-06-05-language-policy-plan-normalization-batch-8.md](../chg-0130-language-policy-plan-normalization-batch-8/task.md)
- **Task Index**: [README.md](../../../03.specs/README.md)
- **Plans Index**: [../plans/README.md](../../../03.specs/README.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
