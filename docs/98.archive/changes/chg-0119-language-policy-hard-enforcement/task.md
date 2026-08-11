---
status: archived
artifact_id: task-0119-01
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/tasks/2026-06-05-language-policy-hard-enforcement.md
archived_at: 2026-08-11
archive_reason: "Move baseline completed source to stable typed target docs/98.archive/changes/chg-0119-language-policy-hard-enforcement/task.md; migrate 6 resolved inbound link(s) with it."
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: e84bcb4b5b2ce406797a6053d81bab958f12117e
preservation_class: git-history
---
<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-hard-enforcement.md -->

# Task: Language Policy Hard Enforcement

## Overview

This task records the validation hardening pass for the repository language
policy goal. It adds a repository contract gate that fails when closed
English-only documentation surfaces regain Korean text.

## Inputs

- **User Objective**: Finish work called out under Remaining Risks and Follow-up
  Tasks for the repository language policy goal.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Reference Normalization](../chg-0131-language-policy-reference-normalization/task.md)
- **Validation Script**: [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh)
- **Scripts Index**: [scripts README](../../../../scripts/README.md)

## Working Rules

- Enforce only the closed English-only surfaces:
  `docs/03.specs`, `docs/04.execution/plans`, `docs/04.execution/tasks`, and
  `docs/90.references`.
- Exclude `README.md` files from this gate because the active language boundary
  closure targeted leaf/reference files, not human-facing stage indexes.
- Exclude generated `docs/90.references/llm-wiki/llm-wiki-index.md` because it is
  path-only generated output maintained by its generator.
- Keep the enforcement local and script-backed; do not change remote CI,
  protected branch settings, credentials, or third-party resources.
- Treat stale Graphify output as advisory only; corroborate against tracked
  source files and validators.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `scripts/validation/check-repo-contracts.sh` | User continuation request for remaining risks and follow-up tasks | Add hard Korean-character gate for closed English-only doc surfaces | Closed surfaces had zero files with Korean text, but validation did not fail future drift | Repo contract check now fails if Korean text appears in closed English-only surfaces under approved exclusions | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |
| `scripts/README.md` | Script inventory contract | Update repo contract check purpose text | Repo Contract Check purpose did not mention closed English-only surface enforcement | Purpose text includes closed English-only doc surface contracts | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Add a hard validation section for closed English-only doc surfaces. | test | Language policy boundary audit | Hard enforcement follow-up | `bash scripts/validation/check-repo-contracts.sh` | Codex | Done |
| T-002 | Update script inventory language for the expanded repo contract check. | doc | Script usage contract | Inventory alignment | `bash scripts/validation/check-repo-contracts.sh` script usage contract | Codex | Done |
| T-003 | Refresh generated index evidence for the new task path and script updates. | doc | Documentation release workflow | Evidence closure | LLM Wiki generator and freshness check | Codex | Done |

## Enforcement Scope

The new repo contract section scans these closed English-only surfaces for
Korean characters:

- `docs/03.specs`
- `docs/04.execution/plans`
- `docs/04.execution/tasks`
- `docs/90.references`

Approved exclusions:

- Any `README.md`
- `docs/90.references/llm-wiki/llm-wiki-index.md`

## Validation Results

| Command | Result |
| --- | --- |
| `bash -n scripts/validation/check-repo-contracts.sh` | PASS. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS after regenerating the LLM Wiki index for the changed script and new task path. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regeneration. |

## Verification Summary

- **Test Commands**:
  - `bash -n scripts/validation/check-repo-contracts.sh`
  - `git diff --check`
  - `bash scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
- **Eval Commands**: N/A for repository validation hardening.
- **Logs / Evidence Location**: This task and
  `docs/00.agent-governance/memory/progress.md`.

## Remaining Risks

- None for the requested Remaining Risks and Follow-up Tasks scope.

## Follow-up Tasks

- None for this language-policy closure scope.

## Related Documents

- **Reference Normalization Evidence**: [2026-06-05-language-policy-reference-normalization.md](../chg-0131-language-policy-reference-normalization/task.md)
- **Final Task Normalization Evidence**: [2026-06-05-language-policy-task-normalization-batch-7.md](../chg-0138-language-policy-task-normalization-batch-7/task.md)
- **Task Index**: [README.md](../../../03.specs/README.md)
- **Scripts README**: [scripts README](../../../../scripts/README.md)
- **Repo Contract Check**: [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh)
