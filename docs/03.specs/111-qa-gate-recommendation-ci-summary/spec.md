---
status: active
---

<!-- Target: docs/03.specs/111-qa-gate-recommendation-ci-summary/spec.md -->

# QA Gate Recommendation CI Summary Technical Specification

## Overview

This specification defines the CI summary integration for the existing
changed-path QA gate recommendation script. The integration publishes advisory
recommendations to GitHub Step Summary without adding a new required job,
executing the recommended gates, or mutating repository/runtime state.

## Strategic Boundaries & Non-goals

This feature is intentionally report-only. It does not change required CI job
IDs, remote branch protection, provider runtime behavior, deployment behavior,
or secret handling.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from automation
  candidate `AEA-AUTO-001`.
- **ARD**: No dedicated ARD exists; the architecture boundary is the existing
  CI quality workflow and local QA recommendation script.
- **Related ADRs**: No new ADR is required because this is a small CI summary
  integration inside the existing CI quality workflow.

## Contracts

- **Config Contract**: `.github/workflows/ci-quality.yml` must publish QA gate
  recommendations through `GITHUB_STEP_SUMMARY` from the existing
  `docs-implementation-alignment` job.
- **Data / Interface Contract**: The summary step must choose a comparable base
  ref for pull request, push, or workflow-dispatch events and run
  `scripts/validation/recommend-qa-gates.sh --base <ref>` when possible.
- **Governance Contract**: The summary is advisory only. It must not add a new
  required job, weaken workflow permissions, use `pull_request_target`, or
  execute the recommended gates.

## Core Design

- **Component Boundary**: The CI integration is a shell step in
  `.github/workflows/ci-quality.yml`; the recommender logic remains in
  `scripts/validation/recommend-qa-gates.sh`.
- **Key Dependencies**: Git history from `actions/checkout` with `fetch-depth:
  0`, GitHub Step Summary, and the existing recommendation script.
- **Tech Stack**: GitHub Actions YAML and Bash.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: The summary output is Markdown containing a
  text block of the existing script output.
- **Migration / Transition Plan**: Add the summary step, add repo-contract
  literals to guard the integration, update Stage 03/04 evidence, and close
  `AEA-AUTO-001`.

## Interfaces & Data Structures

### Core Interfaces

```text
pull_request -> base ref = github.event.pull_request.base.sha
push -> base ref = github.event.before when not all-zero
workflow_dispatch -> base ref = HEAD~1 when available
fallback -> explicit file recommendation for .github/workflows/ci-quality.yml
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: QA Engineer / CI-CD Engineer.
- **Inputs**: GitHub event type, comparable base ref, changed paths, and
  tracked recommendation script.
- **Outputs**: Advisory GitHub Step Summary and local task evidence.
- **Success Definition**: CI surfaces the same recommendation report that local
  agents can run, while existing required jobs and permissions remain intact.

## Tools & Tool Contract (If Applicable)

- **Tool List**: GitHub Actions, Bash, `git`, `recommend-qa-gates.sh`,
  `check-repo-contracts.sh`.
- **Permission Boundary**: The step uses `contents: read` only and does not
  write repository content, post comments, upload artifacts, or access secret
  values.
- **Failure Handling**: If no comparable base ref exists, publish a small
  fallback recommendation instead of failing the workflow for summary-only
  reasons.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Treat the summary as advisory local-gate
  guidance, not completion evidence by itself.
- **Policy Constraints**: No remote mutation, no branch-protection claim, no
  secret output, no new CI gate ID.
- **Versioning Rule**: Workflow, validator, and evidence changes must be
  committed as one logical unit.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records validation results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  `AEA-AUTO-001` summary integration closure.
- **Retrieval Boundary**: Graphify remains advisory and must be corroborated
  against tracked workflow and Stage docs.

## Guardrails (If Applicable)

- **Input Guardrails**: Use Git refs and changed paths only.
- **Output Guardrails**: Publish recommendations in a text block; do not print
  secret values, raw logs, shell history, or `.env` values.
- **Blocked Conditions**: New required job, expanded workflow permissions,
  `pull_request_target`, remote mutation, or execution of recommended gates.
- **Escalation Rule**: Remote branch protection or PR comment automation
  requires separate approval and evidence.

## Evaluation (If Applicable)

- **Eval Types**: Workflow static contract, recommender CLI behavior,
  documentation validation, repo contracts.
- **Metrics**: zero repo-contract failures and preserved CI job set.
- **Datasets / Fixtures**: Explicit file fixture for
  `.github/workflows/ci-quality.yml` and changed-path base-ref mode.
- **How to Run**: use the verification commands below and linked task evidence.

## Edge Cases & Error Handling

- **All-zero push before SHA**: fall back to `HEAD~1` when available.
- **Workflow dispatch on a shallow or single-commit checkout**: publish a
  fallback explicit-file recommendation.
- **Script output changes**: summary remains valid because it embeds the
  script output as text.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: The summary step becomes a de facto gate.
- **Fallback**: Keep it in an existing required job and do not add failure
  conditions beyond shell/runtime errors.
- **Human Escalation**: Required before posting PR comments, changing branch
  protection, or adding required job IDs.

## Verification

```bash
bash scripts/validation/recommend-qa-gates.sh --files .github/workflows/ci-quality.yml
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-QGS-001**: Workflow summary step references
  `GITHUB_STEP_SUMMARY` and `recommend-qa-gates.sh --base`.
- **VAL-QGS-002**: Required CI job set remains unchanged.
- **VAL-QGS-003**: Repo contracts guard the summary-step literals.
- **VAL-QGS-004**: Documentation validation and repository contracts pass.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-05-qa-gate-recommendation-ci-summary.md](../../04.execution/plans/2026-07-05-qa-gate-recommendation-ci-summary.md)
- **Tasks**: [../../04.execution/tasks/2026-07-05-qa-gate-recommendation-ci-summary.md](../../04.execution/tasks/2026-07-05-qa-gate-recommendation-ci-summary.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
- **CI quality workflow**: [../../../.github/workflows/ci-quality.yml](../../../.github/workflows/ci-quality.yml)
