---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-05-agent-output-eval-fixtures.md -->

# Agent Output Eval Fixtures Implementation Plan

## Overview

This plan implements a small Stage 90 fixture pack for evaluating common agent
outputs. It closes `AEA-AUTO-003` at the reference-fixture level while leaving
scripted eval execution or CI gating as future work.

## Context

The implementation audit found strong validation and CI loops but no explicit
agent-output eval loop artifact. OpenAI evaluation guidance frames eval work as
objective, dataset, metrics, run/compare, and continuous evaluation. This
repository can start with a small stable fixture pack before adding any runner.

## Goals & In-Scope

- **Goals**:
  - Add a Stage 03 spec and Stage 04 evidence for agent-output eval fixtures.
  - Add a Stage 90 governance data reference with docs, provider, and infra
    fixture scenarios.
  - Update audit gaps, indexes, LLM Wiki, and progress memory.
- **In Scope**:
  - `docs/03.specs/110-agent-output-eval-fixtures/spec.md`
  - `docs/04.execution/plans/2026-07-05-agent-output-eval-fixtures.md`
  - `docs/04.execution/tasks/2026-07-05-agent-output-eval-fixtures.md`
  - `docs/90.references/data/governance/agent-output-eval-fixtures.md`
  - Related README indexes and audit references.

## Non-Goals & Out-of-Scope

- No model calls, eval API calls, or remote jobs.
- No CI workflow, hook, provider runtime, or validation-script behavior change.
- No runtime Compose, infra, deployment, secret, credential, token, or `.env`
  changes.
- No formal eval score threshold for PR merge readiness.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-AOE-001 | Add Stage 03/04 evidence. | Spec, plan, task, Stage 03/04 README indexes | VAL-AOE-002 | Parent links and indexes are valid. |
| PLN-AOE-002 | Add fixture reference data. | `docs/90.references/data/governance/agent-output-eval-fixtures.md`, data indexes | VAL-AOE-001 | Fixture catalog covers docs, provider, and infra tasks. |
| PLN-AOE-003 | Update audit and progress closure. | Audit reports, automation candidates, progress memory | VAL-AOE-003 | `AEA-AUTO-003` points to implemented fixture pack. |
| PLN-AOE-004 | Refresh generated navigation and validate. | LLM Wiki index and validation evidence | VAL-AOE-004 | Final validation passes. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Hygiene | Check whitespace and conflict markers. | `git diff --check`; `git diff --cached --check` | No output. |
| VAL-PLN-002 | Generated index | Check LLM Wiki freshness. | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Fresh index. |
| VAL-PLN-003 | Docs | Check traceability and implementation alignment. | `bash scripts/validation/check-doc-traceability.sh`; `bash scripts/validation/check-doc-implementation-alignment.sh` | `failures=0`. |
| VAL-PLN-004 | Contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |
| VAL-PLN-005 | Graph | Report Graphify health. | `bash scripts/knowledge/report-graphify-health.sh` | Advisory status recorded if present. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Fixtures are mistaken for CI policy | Medium | State that fixtures are advisory reference data until a future spec adopts a runner or gate. |
| Fixture scoring becomes stale | Medium | Tie sources to Stage 00 and Stage 90 research; update through Stage 03/04 when needed. |
| Sensitive data appears in examples | High | Use synthetic task descriptions only and forbid secret values, raw logs, shell history, and `.env` values. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Manual fixture scoring can be recorded in task
  evidence when relevant.
- **Sandbox / Canary Rollout**: N/A; no runtime service or provider runtime
  change.
- **Human Approval Gate**: Future CI or scripted adoption requires a separate
  approved spec and plan.
- **Rollback Trigger**: Revert the logical commit if the fixture pack conflicts
  with repository contracts.
- **Prompt / Model Promotion Criteria**: N/A for this reference-only fixture
  pack.

## Completion Criteria

- [x] Stage 03 spec exists and links to plan/task/reference.
- [x] Stage 04 plan and task evidence exist.
- [x] Stage 90 fixture reference covers docs, provider, and infra scenarios.
- [x] Audit candidate `AEA-AUTO-003` is closed as reference-fixture coverage.
- [x] Generated index and validation evidence are refreshed.

## Related Documents

- **Spec**: [../../03.specs/110-agent-output-eval-fixtures/spec.md](../../03.specs/110-agent-output-eval-fixtures/spec.md)
- **Task**: [../tasks/2026-07-05-agent-output-eval-fixtures.md](../tasks/2026-07-05-agent-output-eval-fixtures.md)
- **Fixture reference**: [../../90.references/data/governance/agent-output-eval-fixtures.md](../../90.references/data/governance/agent-output-eval-fixtures.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
