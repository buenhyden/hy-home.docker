---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-06-agent-output-eval-ci-gate.md -->

# Agent Output Eval CI Gate Implementation Plan

## Overview

This plan implements the lightweight CI fixture-freshness gate for the existing
agent-output eval fixture catalog and local advisory runner.

## Context

The repository already has an agent-output eval fixture pack and a local
advisory runner. The remaining low-risk automation gap is CI adoption for
fixture catalog drift, not semantic scoring of every agent response.

## Goals & In-Scope

- **Goals**:
  - Add a read-only GitHub Actions job for agent-output eval fixture freshness.
  - Reuse the existing deterministic runner in `--check-fixtures` mode.
  - Add Stage 03/04 evidence and update audit-pack residual-gap wording.
  - Keep the gate narrow enough to avoid model calls, secrets, runtime state,
    or required semantic scoring.
- **In Scope**:
  - `.github/workflows/ci-quality.yml`
  - `scripts/validation/check-repo-contracts.sh`
  - `.github/rulesets/main-protection.md`
  - `docs/00.agent-governance/rules/github-governance.md`
  - Stage 03/04 spec, plan, and task evidence.
  - Stage 90 audit-pack wording and generated indexes.
  - Progress memory.

## Non-Goals & Out-of-Scope

- No model-based evals, eval APIs, remote jobs, paid jobs, or telemetry capture.
- No required scoring gate for arbitrary agent outputs.
- No provider runtime, Docker Compose, deployment, remote GitHub setting,
  credential, secret, token, raw-log, shell-history, or `.env` mutation.
- No replacement for Stage 00 governance, active user instructions, repository
  validators, or human review.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-AOC-001 | Add CI fixture gate and synchronize required-job taxonomy. | `.github/workflows/ci-quality.yml`, `scripts/validation/check-repo-contracts.sh`, `.github/rulesets/main-protection.md`, governance rules | VAL-AOC-001, VAL-AOC-002 | Workflow contains a read-only job that runs `--check-fixtures`, and repo contracts accept the job. |
| PLN-AOC-002 | Add Stage evidence. | `docs/03.specs/120-*`, Stage 04 plan/task | VAL-AOC-003 | Spec/plan/task link to parent runner and fixture reference. |
| PLN-AOC-003 | Synchronize audit residual gap wording. | Stage 90 implementation audit pack | VAL-AOC-003 | Audit docs distinguish fixture freshness CI from future semantic scoring gates. |
| PLN-AOC-004 | Validate and close. | Generated indexes, progress memory | VAL-AOC-004 | Local checks pass or record explicit tool absence. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-AOC-001 | Runner | Check fixture catalog freshness. | `bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures` | `fixtures_check=pass`. |
| VAL-PLN-AOC-002 | Workflow | Check GitHub Actions workflow syntax when available. | `actionlint .github/workflows/ci-quality.yml` | No findings, or explicit local skip if `actionlint` is unavailable. |
| VAL-PLN-AOC-003 | Hygiene | Check whitespace and conflict markers. | `git diff --check` | No output. |
| VAL-PLN-AOC-004 | Docs | Check generated and docs contracts. | LLM Wiki freshness, doc traceability, doc implementation alignment | All pass. |
| VAL-PLN-AOC-005 | Contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Fixture freshness is mistaken for semantic agent-output approval. | Medium | Spec, task, and audit wording explicitly keep semantic scoring advisory and future-gated. |
| CI job grows into a high-latency eval surface. | Medium | Run only the existing `--check-fixtures` mode with a five-minute timeout. |
| Workflow introduces broad permissions. | High | Use job-level `contents: read` and no write token or secrets. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Existing runner `--check-fixtures`.
- **Sandbox / Canary Rollout**: N/A; no runtime service changes.
- **Human Approval Gate**: Required before required semantic scoring or
  model-based eval jobs.
- **Rollback Trigger**: Revert the CI/evidence commit if the job produces
  unexpected workflow failures unrelated to fixture drift.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] CI job added with read-only permission and bounded timeout.
- [x] CI job runs only deterministic fixture freshness checks.
- [x] Stage 03/04 evidence and audit-pack wording are synchronized.
- [x] Generated indexes and progress memory are updated.
- [x] Verification passed or an unavailable optional local tool is recorded.

## Related Documents

- **Spec**: [../../03.specs/120-agent-output-eval-ci-gate/spec.md](../../03.specs/120-agent-output-eval-ci-gate/spec.md)
- **Task**: [../tasks/2026-07-06-agent-output-eval-ci-gate.md](../tasks/2026-07-06-agent-output-eval-ci-gate.md)
- **Parent Runner Spec**: [../../03.specs/116-agent-output-eval-runner/spec.md](../../03.specs/116-agent-output-eval-runner/spec.md)
- **Fixture Reference**: [../../90.references/data/governance/agent-output-eval-fixtures.md](../../90.references/data/governance/agent-output-eval-fixtures.md)
