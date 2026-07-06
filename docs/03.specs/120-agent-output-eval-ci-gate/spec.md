---
status: completed
---

<!-- Target: docs/03.specs/120-agent-output-eval-ci-gate/spec.md -->

# Agent Output Eval CI Gate Technical Specification

## Overview

This specification defines a lightweight GitHub Actions gate for the existing
agent-output eval fixture catalog and local advisory runner. The gate runs
`bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures` so
CI catches fixture catalog and runner ID drift without scoring arbitrary agent
outputs or calling external eval services.

## Strategic Boundaries & Non-goals

This feature is a deterministic CI freshness gate. It does not make eval scores
required for every agent response, call model APIs, run paid or remote eval
jobs, inspect secrets or raw logs, mutate provider runtime, change Docker
Compose, write credentials, or replace Stage 00 governance and human review.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a bounded follow-up from the
  agent-output eval CI gate gap in the agentic engineering implementation audit
  pack.
- **ARD**: No dedicated ARD exists; this uses the existing GitHub Actions
  workflow and validation-script architecture.
- **Related ADRs**: No new ADR is required because this is an incremental CI
  validation job, not an architecture decision.

## Contracts

- **Config Contract**: `.github/workflows/ci-quality.yml` contains an
  `agent-output-eval-fixture-gate` job with read-only repository permission and
  a five-minute timeout. The job ID is also listed in
  `scripts/validation/check-repo-contracts.sh`,
  `.github/rulesets/main-protection.md`, and
  `docs/00.agent-governance/rules/github-governance.md`.
- **Data / Interface Contract**: The job invokes
  `scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures`, which
  compares runner fixture IDs to
  `docs/90.references/data/governance/agent-output-eval-fixtures.md`.
- **Governance Contract**: The gate is limited to catalog freshness. Any future
  required scoring gate, model-based eval, remote job, or new fixture family
  needs separate Stage 03/04 design and approval.

## Core Design

- **Component Boundary**: CI workflow job only; the existing runner remains the
  implementation surface.
- **Key Dependencies**: GitHub Actions, Bash, Python 3 standard library,
  fixture catalog, and the local runner.
- **Tech Stack**: GitHub Actions YAML, Bash, Python 3.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Fixture IDs remain defined in the Stage 90 data
  reference and mirrored in the runner.
- **Migration / Transition Plan**: Add the CI job, add Stage 03/04 evidence,
  update audit-pack residual-gap language, refresh generated indexes, validate,
  and commit as one logical CI/eval unit.

## Interfaces & Data Structures

### Core Interfaces

```text
bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: QA Engineer / Agentic Workflow Specialist.
- **Inputs**: Tracked fixture catalog and runner source.
- **Outputs**: CI pass/fail signal for fixture catalog drift.
- **Success Definition**: Pull requests and pushes to `main` fail when the
  fixture catalog and runner fixture IDs drift.

## Tools & Tool Contract (If Applicable)

- **Tool List**: GitHub Actions, Bash, Python 3.
- **Permission Boundary**: `contents: read`; no write token, no secrets access,
  no runtime state, no remote API beyond GitHub Actions job execution.
- **Failure Handling**: CI fails fast when fixture IDs are missing, duplicated,
  or inconsistent between the catalog and runner.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Treat CI fixture freshness as a structural
  loop gate, not as semantic approval of an agent output.
- **Policy Constraints**: Do not paste raw agent transcripts, secrets,
  credentials, private keys, `.env` values, raw logs, or shell history into CI
  artifacts.
- **Versioning Rule**: CI workflow, repo-contract job taxonomy, Stage evidence,
  audit wording, generated indexes, and progress memory are committed together.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records validation commands and
  CI surface approval evidence.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  closure of the lightweight eval CI fixture gate gap.
- **Retrieval Boundary**: Graphify remains advisory; CI behavior is verified
  against tracked workflow, runner, fixture catalog, and Stage docs.

## Guardrails (If Applicable)

- **Input Guardrails**: Read only tracked repository files required for fixture
  ID consistency.
- **Output Guardrails**: Emit fixture freshness status only; do not echo scored
  content.
- **Blocked Conditions**: Required semantic scoring gates, model calls, remote
  eval jobs, protected runtime reads, secrets access, or GitHub write-token
  behavior are out of scope.
- **Escalation Rule**: Any future scoring gate or security-sensitive eval
  expansion requires separate Stage 03/04 work.

## Evaluation (If Applicable)

- **Eval Types**: Fixture catalog consistency check and workflow syntax check.
- **Metrics**: `fixtures_expected`, `fixtures_found`, `fixtures_check`, and
  action workflow validation.
- **Datasets / Fixtures**: Current `AOE-DOC-001`, `AOE-PROVIDER-001`, and
  `AOE-INFRA-001` fixtures.
- **How to Run**: Use the verification commands below.

## Edge Cases & Error Handling

- **Missing Python 3**: The GitHub-hosted Ubuntu runner includes Python 3; local
  validation should fail clearly if unavailable.
- **Catalog-only fixture addition**: The gate fails until the runner knows the
  new fixture ID.
- **Runner-only fixture addition**: The gate fails until the catalog documents
  the fixture.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: CI gate blocks a change because fixture IDs drift.
- **Fallback**: Update the runner and fixture reference in the same commit, then
  rerun the gate.
- **Human Escalation**: Required before adding required scoring, model-based
  eval, or remote evaluation jobs.

## Verification

```bash
bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures
actionlint .github/workflows/ci-quality.yml
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-AOC-001**: CI has a dedicated read-only fixture freshness job and the
  required-job taxonomy is synchronized across workflow, ruleset proposal,
  governance docs, and repo-contract validator.
- **VAL-AOC-002**: The job runs the existing deterministic runner in
  `--check-fixtures` mode only.
- **VAL-AOC-003**: Stage 03/04 evidence, audit-pack wording, generated indexes,
  and progress memory are synchronized.
- **VAL-AOC-004**: Local workflow/documentation validation passes.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-06-agent-output-eval-ci-gate.md](../../04.execution/plans/2026-07-06-agent-output-eval-ci-gate.md)
- **Tasks**: [../../04.execution/tasks/2026-07-06-agent-output-eval-ci-gate.md](../../04.execution/tasks/2026-07-06-agent-output-eval-ci-gate.md)
- **Parent Runner Spec**: [../116-agent-output-eval-runner/spec.md](../116-agent-output-eval-runner/spec.md)
- **Fixture Reference**: [../../90.references/data/governance/agent-output-eval-fixtures.md](../../90.references/data/governance/agent-output-eval-fixtures.md)
- **Automation Candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
