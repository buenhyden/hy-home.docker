---
status: completed
---

<!-- Target: docs/03.specs/116-agent-output-eval-runner/spec.md -->

# Agent Output Eval Runner Technical Specification

## Overview

This specification defines a local advisory runner for the existing agent-output
eval fixture catalog. The runner lists fixtures, checks fixture catalog
freshness, and heuristically scores saved agent outputs against docs, provider,
and infrastructure fixture criteria without calling models or mutating runtime
state.

## Strategic Boundaries & Non-goals

This feature is local validation tooling only. It does not add CI gates, call
model/eval APIs, execute remote jobs, inspect secrets, read raw logs, change
provider runtime, mutate Docker Compose, or make fixture scores authoritative
over Stage 00 governance, active user instructions, repository validators, or
human review.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from the agent-output
  eval row in the agentic engineering automation candidates reference.
- **ARD**: No dedicated ARD exists; the implementation stays within the
  existing Stage 90 fixture catalog and validation-script boundaries.
- **Related ADRs**: No new ADR is required because this is a local advisory
  runner, not an architecture decision.

## Contracts

- **Config Contract**: `scripts/validation/run-agent-output-eval-fixtures.sh`
  provides `--list`, separate or combined `--check-fixtures` and
  `--check-regressions`, and `--fixture ... --classification
  synthetic-fixture --stdin/--output`
  modes.
- **Data / Interface Contract**: The runner uses
  `docs/90.references/data/governance/agent-output-eval-fixtures.md` as the
  fixture catalog source and embeds deterministic scoring heuristics for the
  exact eight fixture IDs and ten semantic regressions.
- **Governance Contract**: `scripts/validation/check-repo-contracts.sh` must run
  `run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions` so
  fixture catalog, typed thresholds, and regression calibration cannot drift.

## Core Design

- **Component Boundary**: A Bash wrapper invokes an embedded Python scorer,
  matching existing validation script patterns.
- **Key Dependencies**: Stage 90 fixture catalog, Stage 00 boundaries, local
  validation scripts, task evidence documents.
- **Tech Stack**: Bash and Python 3 standard library.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Each fixture has an ID, label, surface, required
  context paths, criteria, required score threshold, and block patterns.
- **Migration / Transition Plan**: Add the runner, update fixture reference and
  script inventory, wire repo-contract catalog checks, add Stage 03/04 evidence,
  and close the local-runner follow-up while leaving CI gate adoption separate.

## Interfaces & Data Structures

### Core Interfaces

```text
bash scripts/validation/run-agent-output-eval-fixtures.sh --list
bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions
printf '%s\n' '<synthetic output>' | bash scripts/validation/run-agent-output-eval-fixtures.sh --fixture AOE-DOC-001 --classification synthetic-fixture --stdin
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: QA Engineer / Agentic Workflow Specialist.
- **Inputs**: Explicitly classified synthetic text or repository-relative files
  under the two typed synthetic fixture/evidence roots, plus a selected fixture
  ID.
- **Outputs**: Advisory score summary, block failures, criterion scores, and
  required context reminders.
- **Success Definition**: Maintainers can locally score common agent-output
  surfaces without model calls, CI changes, or protected-surface mutations.

## Tools & Tool Contract (If Applicable)

- **Tool List**: Bash, Python 3, repo-contract validator.
- **Permission Boundary**: Read only non-symlink regular UTF-8 files under the
  typed synthetic roots using same-descriptor validation; reject absolute,
  outside, special-file, diagnostic, log, auth, token, secret, and shell-history
  classes.
- **Failure Handling**: Fixture and regression checks fail independently on
  exact catalog/calibration drift; scoring exits non-zero for block conditions
  or required-criterion failure.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Treat runner scores as advisory local
  heuristics; validators and human review remain authoritative.
- **Policy Constraints**: Do not include secret values, raw logs, shell history,
  credentials, tokens, `.env` values, or unsupported remote/provider claims in
  scored outputs.
- **Versioning Rule**: Runner, fixture reference updates, contracts, and evidence
  are committed as one logical unit.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records runner checks and
  validation results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  closure of the local agent-output eval runner follow-up.
- **Retrieval Boundary**: Graphify remains advisory and must be corroborated
  against tracked fixture, script, and Stage docs.

## Guardrails (If Applicable)

- **Input Guardrails**: Require `synthetic-fixture` classification. Path input is
  repository-relative and confined to typed synthetic roots; stdin is bounded
  and passes the same sensitive-content rejection before scoring.
- **Output Guardrails**: Print criterion scores and reasons, not raw protected
  values.
- **Blocked Conditions**: Sensitive-looking key/value content, private keys,
  unsupported Gemini native parity claims, runtime mutation without approval,
  raw log/shell-history inclusion claims, and docs-only live-state claims.
- **Escalation Rule**: CI gate adoption, model-based evals, remote jobs, or new
  fixture classes require a separate approved Stage 03/04 plan.

## Evaluation (If Applicable)

- **Eval Types**: Fixture catalog check, list mode, stdin scoring smoke test,
  shell syntax, repo-contract integration.
- **Metrics**: fixture IDs expected/found, result status, score total/max, block
  failure count, required criterion threshold failures.
- **Datasets / Fixtures**: Current `AOE-DOC-001`, `AOE-PROVIDER-001`, and
  `AOE-INFRA-001` fixtures.
- **How to Run**: Use the verification commands below and linked task evidence.

## Edge Cases & Error Handling

- **Piped stdin**: The executable Bash wrapper delegates stdin directly to the
  bounded Python scorer.
- **Block failures**: Block conditions produce `result=fail` and non-zero exit.
- **Weak output**: Missing required criteria produces `result=fail` and a
  non-zero exit without printing input values.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Runner fixture IDs drift from the Stage 90 fixture catalog.
- **Fallback**: Update the runner and fixture reference together, then run
  `--check-fixtures --check-regressions`.
- **Human Escalation**: Required before making fixture scores required CI gates
  or replacing human review.

## Verification

```bash
bash scripts/validation/run-agent-output-eval-fixtures.sh --list
bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions
printf '%s\n' '<synthetic output>' | bash scripts/validation/run-agent-output-eval-fixtures.sh --fixture AOE-DOC-001 --classification synthetic-fixture --stdin
bash -n scripts/validation/run-agent-output-eval-fixtures.sh scripts/validation/check-repo-contracts.sh
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-AOR-001**: Runner lists and checks exactly eight fixture IDs and ten
  regression IDs.
- **VAL-AOR-002**: Runner can score classified synthetic stdin or confined file
  input without model calls or repository mutation.
- **VAL-AOR-003**: Repo contracts check fixture/catalog/threshold/regression
  alignment.
- **VAL-AOR-004**: Stage 03/04 evidence, fixture reference, script inventory,
  and automation candidate closure are in sync.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-06-agent-output-eval-runner.md](../../04.execution/plans/2026-07-06-agent-output-eval-runner.md)
- **Tasks**: [../../04.execution/tasks/2026-07-06-agent-output-eval-runner.md](../../04.execution/tasks/2026-07-06-agent-output-eval-runner.md)
- **Fixture reference**: [../../90.references/data/governance/agent-output-eval-fixtures.md](../../90.references/data/governance/agent-output-eval-fixtures.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
