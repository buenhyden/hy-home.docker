---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-7.md -->

# Task: Language Policy Task Normalization Batch 7

## Overview

This task records the seventh and final bounded `docs/04.execution/tasks`
normalization pass for the repository language policy goal. It normalizes the
final task leaf document to English-only content and closes the active
`docs/03.specs`, `docs/04.execution/plans`, and `docs/04.execution/tasks`
English-only leaf backlog.

## Inputs

- **User Objective**: Finish work called out under Remaining Risks and Follow-up
  Tasks for the repository language policy goal.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Task Normalization Batch 6](./2026-06-05-language-policy-task-normalization-batch-6.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

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
| `docs/04.execution/tasks` final leaf batch | User-provided language policy objective and continuation request | 1 task file | `docs/04.execution/tasks` leaf backlog was 1 file after task batch 6 | `docs/04.execution/tasks` leaf backlog is 0 files; specs/plans/tasks leaf backlogs are all closed | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the final `docs/04.execution/tasks` leaf document to English. | doc | User constraint / tasks English-only | Task normalization batch 7 | Korean-character scan against final target file | Codex | Done |
| T-002 | Confirm English-only leaf backlog closure for specs, plans, and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Task Files

The following English-only target file now has no Korean text:

- [docs/01-05 Content-vs-Implementation Audit Task](./2026-06-04-docs-implementation-audit.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the final normalized task file | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 0 leaf files remain. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 0 leaf files remain. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/llm-wiki-index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - Korean-character scan against the final normalized task file
  - Korean-character file counts for `docs/03.specs`, `docs/04.execution/plans`,
    and `docs/04.execution/tasks`
  - `rg -n 'Overview \(KR\)' docs README.md AGENTS.md scripts -g '*.md' -g '*.sh'`
  - `git diff --check`
  - `bash scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
- **Eval Commands**: N/A for documentation language normalization.
- **Logs / Evidence Location**: This task and
  `docs/00.agent-governance/memory/progress.md`.

## Remaining Risks

- `docs/03.specs`, `docs/04.execution/plans`, and `docs/04.execution/tasks`
  leaf English-only backlogs are closed.
- Non-README `docs/90.references/**` documents still require a separate category
  consistency scan before hard Korean-character enforcement is added.

## Follow-up Tasks

- Review non-README `docs/90.references/**` documents for category language-rule
  consistency.
- After the references scan, add hard Korean-character enforcement for
  English-only surfaces.

## Related Documents

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](./2026-06-05-language-policy-boundary-audit.md)
- **Task Batch 5 Evidence**: [2026-06-05-language-policy-task-normalization-batch-5.md](./2026-06-05-language-policy-task-normalization-batch-5.md)
- **Task Batch 6 Evidence**: [2026-06-05-language-policy-task-normalization-batch-6.md](./2026-06-05-language-policy-task-normalization-batch-6.md)
- **Task Index**: [README.md](./README.md)
- **Plans Index**: [../plans/README.md](../plans/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
