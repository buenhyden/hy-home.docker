---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-3.md -->

# Task: Language Policy Normalization Batch 3

## Overview

This task records the fourth implementation pass for the repository language
policy goal. It closes the remaining `docs/03.specs` leaf normalization backlog
and records the updated plan/task backlog for the next English-only surfaces.

## Inputs

- **User Objective**: Finish remaining risks and follow-up tasks from the
  language policy normalization work.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Batch Evidence**: [Language Policy Normalization Batch 2](./2026-06-05-language-policy-normalization-batch-2.md)
- **Boundary Audit Evidence**: [Language Policy Boundary Audit](./2026-06-05-language-policy-boundary-audit.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- `docs/03.specs/**` leaf documents are English-only technical contracts.
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
| Remaining `docs/03.specs` leaf backlog | User-provided follow-up closure objective | 9 spec files | `docs/03.specs` leaf backlog was 9 files after batch 2 | `docs/03.specs` leaf backlog is 0 files | `git revert` or equivalent patch | No secret values, token, private key, certificate contents, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the remaining `docs/03.specs` leaf backlog to English. | doc | User constraint / specs English-only | Language normalization batch 3 | Korean-character scan against all `docs/03.specs` non-README files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for plans and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Spec Files

The following English-only target files now have no Korean text:

- [AI Tier Spec](../../03.specs/08-ai/spec.md)
- [Laboratory Tier Spec](../../03.specs/11-laboratory/spec.md)
- [Infra Secrets Docs Refresh Spec](../../03.specs/infra-secrets-docs-refresh/spec.md)
- [Tooling Tier Spec](../../03.specs/09-tooling/spec.md)
- [Workspace Consistency 2026-05b Spec](../../03.specs/workspace-consistency-2026-05b/spec.md)
- [Workspace Documentation Consistency 2026-05 Spec](../../03.specs/workspace-doc-consistency-2026-05/spec.md)
- [Messaging Tier Spec](../../03.specs/05-messaging/spec.md)
- [Data Tier Spec](../../03.specs/04-data/spec.md)
- [Workflow Tier Spec](../../03.specs/07-workflow/spec.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against all `docs/03.specs` non-README files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain after this batch. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 57 leaf files remain before plan normalization. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 59 leaf files remain before task normalization. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - `rg -n` Korean-character scan against all `docs/03.specs` non-README files
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
  57 plan leaf files and 59 task leaf files still contain Korean text.
- Non-README `docs/90.references/**` documents were not bulk-polished in this
  batch.
- Hard Korean-character enforcement for English-only surfaces should wait until
  the active plan/task normalization backlog is closed.

## Follow-up Tasks

- Normalize `docs/04.execution/plans/**` leaf documents to English.
- Normalize `docs/04.execution/tasks/**` leaf documents to English while
  preserving historical evidence meaning.
- Review non-README `docs/90.references/**` documents for category language-rule
  consistency.
- After active normalization, add hard Korean-character enforcement for
  English-only surfaces.

## Related Documents

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](./2026-06-05-language-policy-boundary-audit.md)
- **Batch 2 Task**: [2026-06-05-language-policy-normalization-batch-2.md](./2026-06-05-language-policy-normalization-batch-2.md)
- **Task Index**: [README.md](./README.md)
- **References Index**: [../../90.references/README.md](../../90.references/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
