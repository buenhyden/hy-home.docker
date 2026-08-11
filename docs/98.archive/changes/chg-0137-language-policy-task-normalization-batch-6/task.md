---
status: archived
artifact_id: task-0137-01
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-6.md
archived_at: 2026-08-11
archive_reason: "Move baseline completed source to stable typed target docs/98.archive/changes/chg-0137-language-policy-task-normalization-batch-6/task.md; migrate 4 resolved inbound link(s) with it."
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: d94e869ec4ed857e90da085a1ec69dea878b10c9
preservation_class: git-history
---
<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-6.md -->

# Task: Language Policy Task Normalization Batch 6

## Overview

This task records the sixth bounded `docs/04.execution/tasks` normalization
pass for the repository language policy goal. It normalizes 6 additional
workspace audit and governance verification task leaf documents to English-only
content while preserving historical execution meaning, commands, path evidence,
approval boundaries, checklist state, and verification boundaries.

## Inputs

- **User Objective**: Finish work called out under Remaining Risks and Follow-up
  Tasks for the repository language policy goal.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Task Normalization Batch 5](../chg-0136-language-policy-task-normalization-batch-5/task.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- `docs/04.execution/tasks/**` leaf documents are English-only execution
  evidence records.
- Preserve commands, paths, service names, agent names, evidence IDs, Docker
  profiles, environment variables, image names, upstream terms, runtime values,
  no-touch boundaries, checklist state, approval boundaries, and historical
  audit numbers exactly.
- Treat stale Graphify output as advisory only; corroborate against tracked
  source files and validators.
- Keep this task evidence English-only because `docs/04.execution/tasks/**`
  is an English-only execution evidence surface.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/04.execution/tasks` bounded leaf batch | User-provided language policy objective and continuation request | 6 task files | `docs/04.execution/tasks` leaf backlog was 7 files after task batch 5 | 6 additional task files have no Korean text; task backlog is 1 file | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the sixth bounded `docs/04.execution/tasks` leaf batch to English. | doc | User constraint / tasks English-only | Task normalization batch 6 | Korean-character scan against 6 target files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for specs, plans, and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Task Files

The following English-only target files now have no Korean text:

- [Workspace Audit 2026-05 Task](../chg-0051-workspace-audit/task.md)
- [Workspace Audit Gap Closure Task](../chg-0050-workspace-audit-gap-closure/task.md)
- [Workspace Documentation Consistency Task](../chg-0052-workspace-doc-consistency/task.md)
- [Workspace Doc & Governance Consistency Task](../chg-0053-workspace-consistency-2026-05b/task.md)
- [Claude Harness Governance Verification Task](../chg-0054-claude-harness-governance-verification/task.md)
- [Governance Surgical Re-Verification Task](../chg-0062-governance-surgical-reverification/task.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the 6 normalized task files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 1 leaf file remains after this batch. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/llm-wiki-index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - Korean-character scan against the 6 normalized task files
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
  1 task leaf file still contains Korean text.
- Non-README `docs/90.references/**` documents were not bulk-polished in this
  batch.
- Hard Korean-character enforcement for English-only surfaces should wait until
  the active task normalization backlog is closed.

## Follow-up Tasks

- Normalize the final `docs/04.execution/tasks/**` leaf document.
- Review non-README `docs/90.references/**` documents for category language-rule
  consistency.
- After active normalization, add hard Korean-character enforcement for
  English-only surfaces.

## Related Documents

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](../chg-0118-language-policy-boundary-audit/task.md)
- **Task Batch 4 Evidence**: [2026-06-05-language-policy-task-normalization-batch-4.md](../chg-0135-language-policy-task-normalization-batch-4/task.md)
- **Task Batch 5 Evidence**: [2026-06-05-language-policy-task-normalization-batch-5.md](../chg-0136-language-policy-task-normalization-batch-5/task.md)
- **Task Index**: [README.md](../../../03.specs/README.md)
- **Plans Index**: [../plans/README.md](../../../03.specs/README.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
