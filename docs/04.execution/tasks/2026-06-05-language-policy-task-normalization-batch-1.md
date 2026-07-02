---
status: active
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
- **Previous Evidence**: [Language Policy Plan Normalization Batch 8](./2026-06-05-language-policy-plan-normalization-batch-8.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

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

- [Tooling Tasks](./2026-03-26-09-tooling-tasks.md)
- [Communication Tasks](./2026-03-26-10-communication-tasks.md)
- [Laboratory Tasks](./2026-03-26-11-laboratory-tasks.md)
- [AI Open WebUI Tasks](./2026-03-27-08-ai-open-webui-tasks.md)
- [Infra Team Agent Cross-Validation Task](./2026-04-10-infra-team-agent-cross-validation.md)
- [Harness Agent-first Engineering Task](./2026-05-09-harness-agent-first-engineering.md)
- [Scripts Lifecycle Contract Cleanup Task](./2026-05-09-scripts-lifecycle-contract-cleanup.md)
- [LLM Wiki Agent-first Completion Task](./2026-05-10-llm-wiki-agent-first-completion.md)
- [Requirements Standardization Task](./2026-05-17-requirements-standardization.md)
- [Scripts CI QA Cleanup Task](./2026-05-17-scripts-ci-qa-cleanup.md)
- [Operations Purpose Remediation Task](./2026-05-18-docs-05-operations-purpose-remediation.md)
- [Docs Bounded Consistency Audit Task](./2026-05-18-docs-bounded-consistency-audit.md)
- [Execution Stage Remediation Task](./2026-05-18-execution-stage-remediation.md)
- [Targeted Docs Precision Remediation Task](./2026-05-18-targeted-docs-precision-remediation.md)
- [Agent Hook Completion and Style Automation Task](./2026-05-22-agent-hook-completion-style-automation.md)
- [Data Analytics Execution Traceability Task](./2026-05-22-data-analytics-execution-traceability.md)
- [Lifecycle README Debt Closure Task](./2026-05-22-lifecycle-readme-debt-closure.md)
- [Spec Execution Implementation Audit Task](./2026-05-22-spec-execution-implementation-audit.md)
- [Workspace Docs Agent Governance Remediation Task](./2026-05-22-workspace-docs-agent-governance-remediation.md)
- [Workspace Governance Bounded Reaudit Task](./2026-05-22-workspace-governance-bounded-reaudit.md)

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
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/data/llm-wiki/index.md` for the new task path. |

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

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](./2026-06-05-language-policy-boundary-audit.md)
- **Final Plan Batch Evidence**: [2026-06-05-language-policy-plan-normalization-batch-8.md](./2026-06-05-language-policy-plan-normalization-batch-8.md)
- **Task Index**: [README.md](./README.md)
- **Plans Index**: [../plans/README.md](../plans/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
