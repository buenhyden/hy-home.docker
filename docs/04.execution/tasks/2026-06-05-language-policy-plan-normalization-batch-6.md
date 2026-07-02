---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-6.md -->

# Task: Language Policy Plan Normalization Batch 6

## Overview

This task records the sixth bounded `docs/04.execution/plans` implementation
pass for the repository language policy goal. It normalizes 6 additional plan
documents to English-only content while preserving historical execution meaning,
commands, path evidence, checklist state, and verification boundaries.

## Inputs

- **User Objective**: Continue closing remaining risks and follow-up tasks for
  repository language policy normalization.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Plan Normalization Batch 5](./2026-06-05-language-policy-plan-normalization-batch-5.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- `docs/04.execution/plans/**` leaf documents are English-only execution plans.
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
| `docs/04.execution/plans` bounded leaf batch | User-provided language policy objective and continuation request | 6 plan files | `docs/04.execution/plans` leaf backlog was 17 files after plan batch 5 | 6 additional plan files have no Korean text; plan backlog is 11 files | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the sixth bounded `docs/04.execution/plans` leaf batch to English. | doc | User constraint / plans English-only | Plan normalization batch 6 | Korean-character scan against 6 target files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for specs, plans, and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Plan Files

The following English-only target files now have no Korean text:

- [Workflow Optimization Hardening Plan](../plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- [Tooling Optimization Hardening Plan](../plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- [Laboratory Optimization Hardening Plan](../plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- [Workspace Audit Gap Closure Plan](../plans/2026-05-26-workspace-audit-gap-closure.md)
- [Workspace Consistency 2026-05b Plan](../plans/2026-05-29-workspace-consistency-2026-05b.md)
- [Claude Harness Governance Verification Plan](../plans/2026-05-31-claude-harness-governance-verification.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the 6 normalized plan files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain after previous spec closure. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 11 leaf files remain after this batch. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 59 leaf files remain before task normalization. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/llm-wiki-index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - Korean-character scan against the 6 normalized plan files
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
  11 plan leaf files and 59 task leaf files still contain Korean text.
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
- **Plan Batch 4 Evidence**: [2026-06-05-language-policy-plan-normalization-batch-4.md](./2026-06-05-language-policy-plan-normalization-batch-4.md)
- **Plan Batch 5 Evidence**: [2026-06-05-language-policy-plan-normalization-batch-5.md](./2026-06-05-language-policy-plan-normalization-batch-5.md)
- **Task Index**: [README.md](./README.md)
- **Plans Index**: [../plans/README.md](../plans/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
