---
status: archived
artifact_id: task-0121-01
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-2.md
archived_at: 2026-08-11
archive_reason: "Move baseline completed source to stable typed target docs/98.archive/changes/chg-0121-language-policy-normalization-batch-2/task.md; migrate 4 resolved inbound link(s) with it."
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: 198ca4908d4416a2cd3ebf81faa755b930577798
preservation_class: git-history
---
<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-2.md -->

# Task: Language Policy Normalization Batch 2

## Overview

This task records the third implementation pass for the repository language
policy goal. It continues bounded `docs/03.specs` leaf normalization and closes
the next five English-only spec targets without changing runtime facts,
commands, paths, or validation IDs.

## Inputs

- **User Objective**: Finish remaining risks and follow-up tasks from the
  language policy normalization work.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Batch Evidence**: [Language Policy Normalization Batch 1](../chg-0120-language-policy-normalization-batch-1/task.md)
- **Boundary Audit Evidence**: [Language Policy Boundary Audit](../chg-0118-language-policy-boundary-audit/task.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- `docs/03.specs/**` leaf documents are English-only technical contracts.
- Preserve commands, paths, service names, agent names, evidence IDs, Docker
  profiles, environment variables, image names, upstream terms, and runtime
  values exactly.
- Treat stale Graphify output as advisory only; corroborate against tracked
  source files and validators.
- Keep this task evidence English-only because `docs/04.execution/tasks/**`
  is an English-only execution evidence surface.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/03.specs` bounded leaf batch | User-provided follow-up closure objective | 5 spec files | `docs/03.specs` leaf backlog was 14 files after batch 1 | 5 additional `docs/03.specs` leaf files have no Korean text | `git revert` or equivalent patch | No secret values, token, private key, certificate contents, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the second bounded `docs/03.specs` leaf batch to English. | doc | User constraint / specs English-only | Language normalization batch 2 | Korean-character scan against 5 target files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for specs, plans, and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Spec Files

The following English-only target files now have no Korean text:

- [Harness Agent-first Engineering Spec](../../../03.specs/spec-0094-harness-agent-first-engineering/spec.md)
- [Auth Tier Spec](../../../03.specs/spec-0002-auth/spec.md)
- [Security Tier Spec](../../../03.specs/spec-0003-security/spec.md)
- [Observability Tier Spec](../../../03.specs/spec-0007-observability/spec.md)
- [Workspace Audit 2026-05 Spec](../../../03.specs/spec-0090-workspace-audit-2026-05/spec.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the 5 normalized target files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 9 leaf files remain after this batch. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 57 leaf files remain before plan normalization. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 59 leaf files remain before task normalization. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/llm-wiki-index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - `rg -n` Korean-character scan against the 5 normalized target files
  - `rg -n 'Overview \(KR\)' docs README.md AGENTS.md scripts -g '*.md' -g '*.sh'`
  - `git diff --check`
  - `bash scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
- **Eval Commands**: N/A for documentation language normalization.
- **Logs / Evidence Location**: This task and
  `docs/00.agent-governance/memory/progress.md`.

## Remaining Risks

- Full English-only normalization remains incomplete: 9 `docs/03.specs` leaf
  files, 57 plan leaf files, and 59 task leaf files still contain Korean text.
- Non-README `docs/90.references/**` documents were not bulk-polished in this
  batch.
- Hard Korean-character enforcement for English-only surfaces should wait until
  the active normalization backlog is closed.

## Follow-up Tasks

- Continue the remaining 9 `docs/03.specs` leaf files in bounded batches.
- Normalize `docs/04.execution/plans/**` leaf documents to English.
- Normalize `docs/04.execution/tasks/**` leaf documents to English while
  preserving historical evidence meaning.
- Review non-README `docs/90.references/**` documents for category language-rule
  consistency.
- After active normalization, add hard Korean-character enforcement for
  English-only surfaces.

## Related Documents

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](../chg-0118-language-policy-boundary-audit/task.md)
- **Batch 1 Task**: [2026-06-05-language-policy-normalization-batch-1.md](../chg-0120-language-policy-normalization-batch-1/task.md)
- **Task Index**: [README.md](../../../03.specs/README.md)
- **References Index**: [../../90.references/README.md](../../../90.references/README.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
