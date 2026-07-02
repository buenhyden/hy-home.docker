---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-2.md -->

# Task: Language Policy Plan Normalization Batch 2

## Overview

This task records the second `docs/04.execution/plans` implementation pass for
the repository language policy goal. It normalizes another bounded set of plan
documents to English-only content while preserving historical execution meaning
and existing verification boundaries.

## Inputs

- **User Objective**: Continue applying the repository language policy across
  AI-agent, human-facing, and mixed documentation surfaces.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Plan Normalization Batch 1](./2026-06-05-language-policy-plan-normalization-batch-1.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- `docs/04.execution/plans/**` leaf documents are English-only execution plans.
- Preserve commands, paths, service names, agent names, evidence IDs, Docker
  profiles, environment variables, image names, upstream terms, runtime values,
  and historical audit numbers exactly.
- Treat stale Graphify output as advisory only; corroborate against tracked
  source files and validators.
- Keep this task evidence English-only because `docs/04.execution/tasks/**`
  is an English-only execution evidence surface.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/04.execution/plans` bounded leaf batch | User-provided language policy objective | 9 plan files | `docs/04.execution/plans` leaf backlog was 47 files after plan batch 1 | 9 additional plan files have no Korean text; plan backlog is 38 files | `git revert` or equivalent patch | No secret values, token, private key, certificate contents, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the second bounded `docs/04.execution/plans` leaf batch to English. | doc | User constraint / plans English-only | Plan normalization batch 2 | Korean-character scan against 9 target files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for plans and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Plan Files

The following English-only target files now have no Korean text:

- [Agent Governance Decision Items Implementation Plan](../plans/2026-06-02-agent-governance-decision-items-plan.md)
- [11-laboratory Implementation Plan](../plans/2026-03-26-11-laboratory-standardization.md)
- [Data Analytics Execution Traceability Plan](../plans/2026-05-22-data-analytics-execution-traceability.md)
- [Operations Purpose Remediation Plan](../plans/2026-05-18-docs-05-operations-purpose-remediation.md)
- [Docs Bounded Consistency Audit Plan](../plans/2026-05-18-docs-bounded-consistency-audit.md)
- [10-communication Standardization Plan](../plans/2026-03-26-10-communication-standardization.md)
- [Execution Stage Remediation Plan](../plans/2026-05-18-execution-stage-remediation.md)
- [Agent Hook Completion Style Automation Plan](../plans/2026-05-22-agent-hook-completion-style-automation.md)
- [Docs Implementation Reconciliation Plan](../plans/2026-06-02-docs-implementation-reconciliation.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the 9 normalized plan files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain after previous spec closure. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 38 leaf files remain after this batch. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 59 leaf files remain before task normalization. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/data/llm-wiki/index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - `rg -n` Korean-character scan against the 9 normalized plan files
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
  38 plan leaf files and 59 task leaf files still contain Korean text.
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

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](./2026-06-05-language-policy-boundary-audit.md)
- **Plan Batch 1 Evidence**: [2026-06-05-language-policy-plan-normalization-batch-1.md](./2026-06-05-language-policy-plan-normalization-batch-1.md)
- **Task Index**: [README.md](./README.md)
- **Plans Index**: [../plans/README.md](../plans/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
