---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-05-qa-gate-recommendation-ci-summary.md -->

# QA Gate Recommendation CI Summary Implementation Plan

## Overview

This plan implements the PR/CI summary integration for the changed-path QA gate
recommendation report. It closes the remaining `AEA-AUTO-001` follow-up by
publishing advisory recommendations in GitHub Step Summary.

## Context

`scripts/validation/recommend-qa-gates.sh` already gives local agents
changed-path-based QA recommendations. The implementation audit kept a future
gap to surface that report in PR or CI summaries. The lowest-risk integration
is a summary-only step inside the existing `docs-implementation-alignment` job,
which avoids changing the required job set.

## Goals & In-Scope

- **Goals**:
  - Publish QA gate recommendations to `GITHUB_STEP_SUMMARY`.
  - Preserve the existing CI job taxonomy and required status-check list.
  - Add repo-contract regression coverage for the summary step.
  - Add Stage 03/04 evidence and close `AEA-AUTO-001`.
- **In Scope**:
  - `.github/workflows/ci-quality.yml`
  - `scripts/validation/check-repo-contracts.sh`
  - Stage 03/04 evidence, audit references, indexes, generated navigation, and
    progress memory.

## Non-Goals & Out-of-Scope

- No PR comment bot, artifact upload, deployment, remote GitHub setting change,
  or branch-protection mutation.
- No new CI job ID or required status check.
- No execution of recommended gates from the summary step.
- No secret, credential, token, raw log, shell history, or `.env` handling.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-QGS-001 | Add summary-only workflow step. | `.github/workflows/ci-quality.yml` | VAL-QGS-001, VAL-QGS-002 | Workflow still has the same job IDs and publishes summary output. |
| PLN-QGS-002 | Add repo-contract regression literals. | `scripts/validation/check-repo-contracts.sh` | VAL-QGS-003 | Repo contracts require the summary step literals. |
| PLN-QGS-003 | Add Stage 03/04 evidence and update indexes. | Spec, plan, task, README indexes | VAL-QGS-004 | Links and template contracts pass. |
| PLN-QGS-004 | Update audit/progress/generated evidence. | Stage 90 audit docs, LLM Wiki, Graphify, progress | VAL-QGS-004 | Final validation summary is recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | CLI | Check recommendation script output for workflow path. | `bash scripts/validation/recommend-qa-gates.sh --files .github/workflows/ci-quality.yml` | Recommends repo contracts and remote/manual workflow responsibility. |
| VAL-PLN-002 | Syntax | Check changed shell scripts. | `bash -n scripts/validation/check-repo-contracts.sh scripts/validation/recommend-qa-gates.sh` | No syntax errors. |
| VAL-PLN-003 | Hygiene | Check whitespace and conflict markers. | `git diff --check`; `git diff --cached --check` | No output. |
| VAL-PLN-004 | Docs | Check generated and docs contracts. | LLM Wiki freshness, doc traceability, doc implementation alignment | All pass. |
| VAL-PLN-005 | Contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Summary step changes required CI semantics | Medium | Add the step inside an existing required job and avoid new job IDs. |
| Missing base ref causes workflow failure | Medium | Use PR base SHA, push before SHA, `HEAD~1`, then explicit-file fallback. |
| Summary output is mistaken for executed QA evidence | Medium | Label output as recommendations and keep task evidence clear that gates are advisory. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Local script fixture and repo-contract literals.
- **Sandbox / Canary Rollout**: N/A; no runtime service changes.
- **Human Approval Gate**: Future PR comment automation or remote protection
  changes require separate approval.
- **Rollback Trigger**: Revert the workflow/validator/evidence commit if the
  summary step misbehaves.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] Workflow summary step added without new job ID.
- [x] Repo contracts guard the summary-step literals.
- [x] Stage 03/04 evidence and indexes are updated.
- [x] Audit candidate `AEA-AUTO-001` is closed for PR/CI summary integration.
- [x] Final validation passes.

## Related Documents

- **Spec**: [../../03.specs/111-qa-gate-recommendation-ci-summary/spec.md](../../03.specs/111-qa-gate-recommendation-ci-summary/spec.md)
- **Task**: [../tasks/2026-07-05-qa-gate-recommendation-ci-summary.md](../tasks/2026-07-05-qa-gate-recommendation-ci-summary.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
- **CI quality workflow**: [../../../.github/workflows/ci-quality.yml](../../../.github/workflows/ci-quality.yml)
