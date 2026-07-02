---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-1.md -->

# Task: Language Policy Plan Normalization Batch 1

## Overview

This task records the first `docs/04.execution/plans` implementation pass for
the repository language policy goal. It normalizes a small bounded set of plan
documents to English-only content after the `docs/03.specs` leaf backlog was
closed.

## Inputs

- **User Objective**: Continue applying the repository language policy across
  AI-agent, human-facing, and mixed documentation surfaces.
- **Requested Skills**: `document-release`, `humanize-korean`.
- **Previous Evidence**: [Language Policy Normalization Batch 3](./2026-06-05-language-policy-normalization-batch-3.md)
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
| `docs/04.execution/plans` bounded leaf batch | User-provided language policy objective | 10 plan files | `docs/04.execution/plans` leaf backlog was 57 files after spec closure | 10 additional plan files have no Korean text; plan backlog is 47 files | `git revert` or equivalent patch | No secret values, token, private key, certificate contents, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Normalize the first bounded `docs/04.execution/plans` leaf batch to English. | doc | User constraint / plans English-only | Plan normalization batch 1 | Korean-character scan against 10 target files | Codex | Done |
| T-002 | Recalculate remaining English-only backlog for plans and tasks. | doc | Language policy boundary audit | Follow-up closure | Backlog file counts in this task | Codex | Done |
| T-003 | Refresh progress and generated index evidence for the new task path. | doc | Documentation release workflow | Evidence closure | LLM Wiki index check | Codex | Done |

## Normalized Plan Files

The following English-only target files now have no Korean text:

- [02-Auth Documentation Standardization Plan](../plans/2026-03-26-02-auth-standardization.md)
- [Open WebUI Implementation Plan](../plans/2026-03-27-08-ai-open-webui-plan.md)
- [Home Docker Revalidation Deferred Follow-up Plan](../plans/2026-05-25-home-docker-revalidation-deferred-follow-up.md)
- [Home Docker Workspace Audit Improvement Plan](../plans/2026-05-25-home-docker-workspace-audit-improvement.md)
- [Large-Scale Authored SSoT Review Plan](../plans/2026-05-25-large-scale-authored-ssot-review.md)
- [LLM Wiki Agent-first Completion Plan](../plans/2026-05-10-llm-wiki-agent-first-completion.md)
- [Agent Governance Phase 1 Revalidation Plan](../plans/2026-06-02-agent-governance-phase-1-revalidation.md)
- [Agent Governance Phase 2 Strategy Integration Plan](../plans/2026-06-02-agent-governance-phase-2-strategy-integration.md)
- [Agent Governance Phase 3 Approved Surface Activation Plan](../plans/2026-06-02-agent-governance-phase-3-approved-surface-activation.md)
- [Agent Governance Phase 4 Closure Reconciliation Plan](../plans/2026-06-02-agent-governance-phase-4-closure-reconciliation.md)

## Validation Results

| Command | Result |
| --- | --- |
| Korean-character scan against the 10 normalized plan files | PASS: no matches after normalization. |
| Korean-character file count under `docs/03.specs` excluding `README.md` | 0 leaf files remain after previous spec closure. |
| Korean-character file count under `docs/04.execution/plans` excluding `README.md` | 47 leaf files remain after this batch. |
| Korean-character file count under `docs/04.execution/tasks` excluding `README.md` | 59 leaf files remain before task normalization. |
| Repository-wide legacy overview-heading scan | PASS: no legacy overview-heading matches remain. |
| `git diff --check` | PASS. |
| `bash scripts/validation/check-repo-contracts.sh` | PASS. |
| `bash scripts/validation/check-doc-traceability.sh` | PASS. |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS after regenerating `docs/90.references/llm-wiki/llm-wiki-index.md` for the new task path. |

## Verification Summary

- **Test Commands**:
  - `rg -n` Korean-character scan against the 10 normalized plan files
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
  47 plan leaf files and 59 task leaf files still contain Korean text.
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
- **Spec Closure Evidence**: [2026-06-05-language-policy-normalization-batch-3.md](./2026-06-05-language-policy-normalization-batch-3.md)
- **Task Index**: [README.md](./README.md)
- **Plans Index**: [../plans/README.md](../plans/README.md)
- **Documentation Protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
