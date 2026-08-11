---
status: archived
artifact_id: task-0129-01
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-7.md
archived_at: 2026-08-11
archive_reason: "Move baseline completed source to stable typed target docs/98.archive/changes/chg-0129-language-policy-plan-normalization-batch-7/task.md; migrate 4 resolved inbound link(s) with it."
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: bcef1126b19d15038a6d5c0fb35ee69825d3f7a1
preservation_class: git-history
---
<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-7.md -->

# Task: Language Policy Plan Normalization Batch 7

## Overview

This task records the seventh bounded `docs/04.execution/plans` implementation
pass for the repository language policy goal. It normalizes 7 additional tier
optimization-hardening plan documents to English-only content while preserving
historical execution meaning, commands, path evidence, checklist state, and
verification boundaries.

## Inputs

- **User Objective**: Continue closing remaining risks and follow-up tasks for
  repository language policy normalization.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Plan Normalization Batch 6](../chg-0128-language-policy-plan-normalization-batch-6/task.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)

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
| `docs/04.execution/plans` bounded leaf batch | User-provided language policy objective and continuation request | 7 plan files | `docs/04.execution/plans` leaf backlog was 11 files after plan batch 6 | 7 additional plan files have no Korean text; plan backlog is 4 files | `git revert` or equivalent patch | No secret values, tokens, private keys, certificate contents, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the seventh bounded `docs/04.execution/plans` leaf batch to English. | doc | User constraint / plans English-only | Plan normalization batch 7 | Korean-character scan against 7 target files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for specs, plans, and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Plan Files

The following English-only target files now have no Korean text:

- [Gateway Optimization Hardening Plan](../chg-0015-01-gateway-optimization-hardening/plan.md)
- [Auth Optimization Hardening Plan](../chg-0016-02-auth-optimization-hardening/plan.md)
- [Security Optimization Hardening Plan](../chg-0017-03-security-optimization-hardening/plan.md)
- [Data Optimization Hardening Plan](../chg-0018-04-data-optimization-hardening/plan.md)
- [Messaging Optimization Hardening Plan](../chg-0019-05-messaging-optimization-hardening/plan.md)
- [Observability Optimization Hardening Plan](../chg-0020-06-observability-optimization-hardening/plan.md)
- [AI Optimization Hardening Plan](../chg-0022-08-ai-optimization-hardening/plan.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the 7 normalized plan files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain after previous spec closure. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 4 leaf files remain after this batch. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 59 leaf files remain before task normalization. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/llm-wiki-index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - Korean-character scan against the 7 normalized plan files
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
  4 plan leaf files and 59 task leaf files still contain Korean text.
- Non-README `docs/90.references/**` documents were not bulk-polished in this
  batch.
- Hard Korean-character enforcement for English-only surfaces should wait until
  the active plan/task normalization backlog is closed.

## Follow-up Tasks

- Close the final 4 `docs/04.execution/plans/**` leaf documents in the next
  bounded batch.
- Normalize `docs/04.execution/tasks/**` leaf documents to English while
  preserving historical evidence meaning.
- Review non-README `docs/90.references/**` documents for category language-rule
  consistency.
- After active normalization, add hard Korean-character enforcement for
  English-only surfaces.

## Related Documents

- **Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](../chg-0118-language-policy-boundary-audit/task.md)
- **Plan Batch 5 Evidence**: [2026-06-05-language-policy-plan-normalization-batch-5.md](../chg-0127-language-policy-plan-normalization-batch-5/task.md)
- **Plan Batch 6 Evidence**: [2026-06-05-language-policy-plan-normalization-batch-6.md](../chg-0128-language-policy-plan-normalization-batch-6/task.md)
- **Task Index**: [README.md](../../../03.specs/README.md)
- **Plans Index**: [../plans/README.md](../../../03.specs/README.md)
- **Documentation Protocol**: [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
