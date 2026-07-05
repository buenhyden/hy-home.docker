---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-06-agent-output-eval-runner.md -->

# Agent Output Eval Runner Implementation Plan

## Overview

This plan implements a local advisory runner for the existing agent-output eval
fixture catalog.

## Context

The repository already has a fixture pack for scoring common agent outputs, but
the scoring process was manual. A small local runner can make fixture selection,
catalog drift checks, and heuristic output scoring repeatable without adopting
CI gates or model-based eval jobs.

## Goals & In-Scope

- **Goals**:
  - Add a local advisory runner for agent-output eval fixtures.
  - Support fixture listing, fixture catalog checks, and output scoring from a
    file or stdin.
  - Keep scoring deterministic and non-authoritative.
  - Add repo-contract coverage for fixture catalog/runner ID drift.
  - Add Stage 03/04 evidence and update the automation candidate.
- **In Scope**:
  - `scripts/validation/run-agent-output-eval-fixtures.sh`
  - `docs/90.references/data/governance/agent-output-eval-fixtures.md`
  - `scripts/validation/check-repo-contracts.sh`
  - `scripts/README.md`
  - Stage 03/04 indexes, Stage 90 audit references, generated LLM Wiki output,
    Graphify output, and progress memory.

## Non-Goals & Out-of-Scope

- No CI workflow behavior change or required PR gate.
- No model calls, eval API calls, remote jobs, paid jobs, or telemetry capture.
- No provider runtime, Docker Compose, deployment, remote GitHub, credential,
  secret, token, raw-log, shell-history, or `.env` mutation.
- No claim that heuristic scores replace Stage 00 governance, active user
  instructions, repository validators, or human review.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-AOR-001 | Add local advisory runner. | `scripts/validation/run-agent-output-eval-fixtures.sh` | VAL-AOR-001, VAL-AOR-002 | `--list`, `--check-fixtures`, and stdin scoring smoke pass. |
| PLN-AOR-002 | Update fixture reference. | `docs/90.references/data/governance/agent-output-eval-fixtures.md` | VAL-AOR-001, VAL-AOR-004 | Fixture catalog names runner and required context paths. |
| PLN-AOR-003 | Wire repo-contract freshness and script inventory. | `check-repo-contracts.sh`, `scripts/README.md` | VAL-AOR-003 | Full repo contracts pass. |
| PLN-AOR-004 | Add evidence and close candidate. | Stage 03/04 indexes, Stage 90 audit docs, progress | VAL-AOR-004 | Documentation validation passes. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-AOR-001 | Runner | List and check fixture catalog. | `bash scripts/validation/run-agent-output-eval-fixtures.sh --list`; `bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures` | Fixtures are listed and `fixtures_check=pass`. |
| VAL-PLN-AOR-002 | Runner | Score a sample output through stdin. | `printf ... \| bash scripts/validation/run-agent-output-eval-fixtures.sh --fixture AOE-DOC-001 --stdin` | Output includes `result=pass`. |
| VAL-PLN-AOR-003 | Syntax | Check changed shell scripts. | `bash -n scripts/validation/run-agent-output-eval-fixtures.sh scripts/validation/check-repo-contracts.sh` | No syntax errors. |
| VAL-PLN-AOR-004 | Hygiene | Check whitespace and conflict markers. | `git diff --check`; `git diff --cached --check` | No output. |
| VAL-PLN-AOR-005 | Docs | Check generated and docs contracts. | LLM Wiki freshness, doc traceability, doc implementation alignment | All pass. |
| VAL-PLN-AOR-006 | Contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Heuristic score is treated as authoritative | Medium | Output explicitly says the runner is advisory and validators/human review remain authoritative. |
| Sensitive output is scored and echoed | High | Runner reports block reasons and criteria, not raw output text; sensitive-looking values are block patterns. |
| Fixture catalog and runner drift | Medium | Repo contracts run `--check-fixtures`. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Runner list/check/scoring smoke and repo-contract pass.
- **Sandbox / Canary Rollout**: N/A; no runtime service changes.
- **Human Approval Gate**: Required before CI gate adoption or model-based eval
  execution.
- **Rollback Trigger**: Revert the runner/output/evidence commit if the runner
  creates false freshness failures.

## Completion Criteria

- Runner exists and supports `--list`, `--check-fixtures`, and output scoring.
- Fixture reference names the runner and exact required context paths.
- Repo contracts check runner/catalog alignment.
- Scripts README, Stage 03/04 indexes, and audit references are synchronized.
- Generated LLM Wiki and Graphify outputs are refreshed or skip evidence is
  recorded.

## Related Documents

- **Spec**: [../../03.specs/116-agent-output-eval-runner/spec.md](../../03.specs/116-agent-output-eval-runner/spec.md)
- **Task**: [../tasks/2026-07-06-agent-output-eval-runner.md](../tasks/2026-07-06-agent-output-eval-runner.md)
- **Fixture reference**: [../../90.references/data/governance/agent-output-eval-fixtures.md](../../90.references/data/governance/agent-output-eval-fixtures.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
