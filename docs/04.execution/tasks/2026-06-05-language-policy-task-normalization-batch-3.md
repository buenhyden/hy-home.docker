---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-3.md -->

# Task: Language Policy Task Normalization Batch 3

## Overview

This task records the third bounded `docs/04.execution/tasks` normalization pass
for the repository language policy goal. It normalizes 7 additional task leaf
documents to English-only content while preserving historical execution meaning,
commands, path evidence, checklist state, and verification boundaries.

## Inputs

- **User Objective**: Finish work called out under Remaining Risks and Follow-up
  Tasks for the repository language policy goal.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Task Normalization Batch 2](./2026-06-05-language-policy-task-normalization-batch-2.md)
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
| `docs/04.execution/tasks` bounded leaf batch | User-provided language policy objective and continuation request | 7 task files | `docs/04.execution/tasks` leaf backlog was 27 files after task batch 2 | 7 additional task files have no Korean text; task backlog is 20 files | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the third bounded `docs/04.execution/tasks` leaf batch to English. | doc | User constraint / tasks English-only | Task normalization batch 3 | Korean-character scan against 7 target files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for specs, plans, and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Task Files

The following English-only target files now have no Korean text:

- [Gateway Documentation Standardization Task](./2026-03-26-01-gateway-tasks.md)
- [Auth Documentation Standardization Task](./2026-03-26-02-auth-tasks.md)
- [Security Documentation Standardization Task](./2026-03-26-03-security-tasks.md)
- [Data Tier Documentation Standardization Task](./2026-03-26-04-data-tasks.md)
- [Messaging Infrastructure Documentation Standardization Task](./2026-03-26-05-messaging-tasks.md)
- [Observability Documentation Standardization Task](./2026-03-26-06-observability-tasks.md)
- [Standardize infra_net Implementation Task](./2026-04-01-standardize-infra-net.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the 7 normalized task files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 20 leaf files remain after this batch. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/llm-wiki-index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - Korean-character scan against the 7 normalized task files
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
  20 task leaf files still contain Korean text.
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
- **Task Batch 1 Evidence**: [2026-06-05-language-policy-task-normalization-batch-1.md](./2026-06-05-language-policy-task-normalization-batch-1.md)
- **Task Batch 2 Evidence**: [2026-06-05-language-policy-task-normalization-batch-2.md](./2026-06-05-language-policy-task-normalization-batch-2.md)
- **Task Index**: [README.md](./README.md)
- **Plans Index**: [../plans/README.md](../plans/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
