---
status: active
---

<!-- Target: docs/03.specs/110-agent-output-eval-fixtures/spec.md -->

# Agent Output Eval Fixtures Technical Specification

## Overview

This specification defines a small, non-executing fixture pack for evaluating
common agent outputs in `hy-home.docker`. The fixtures cover documentation,
provider-surface, and infrastructure documentation tasks so future agents can
score output quality consistently before this becomes a scripted eval harness.

## Strategic Boundaries & Non-goals

The fixture pack is reference data, not an automated grader. It does not add CI
jobs, model calls, remote evaluation runs, provider runtime changes, workflow
changes, or protected runtime mutations.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from automation
  candidate `AEA-AUTO-003`.
- **ARD**: No dedicated ARD exists; the architecture boundary is the existing
  Stage 00 governance, Stage 90 research, and Stage 04 evidence model.
- **Related ADRs**: No new ADR is required because this adds reference fixtures
  and execution evidence without changing architecture decisions.

## Contracts

- **Config Contract**: No executable configuration is introduced. The fixture
  pack lives under `docs/90.references/data/governance/`.
- **Data / Interface Contract**: Each fixture must define an input scenario,
  required source context, expected output properties, scoring criteria, block
  conditions, and verification evidence.
- **Governance Contract**: Fixtures are advisory quality references. They must
  not override Stage 00 policy, user instructions, protected-surface approvals,
  or repository validation gates.

## Core Design

- **Component Boundary**: Stage 03/04 documents define the implementation
  contract and evidence. Stage 90 data stores the fixture catalog.
- **Key Dependencies**: Stage 00 documentation protocol, provider capability
  matrix, loop/harness research, implementation audit gaps, and QA validation
  scripts.
- **Tech Stack**: Markdown reference data only.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: A fixture has `{id, surface, input scenario,
  required context, expected output, scoring criteria, block conditions,
  evidence}`.
- **Migration / Transition Plan**: Add the fixture reference, update indexes,
  close `AEA-AUTO-003` as a reference fixture pack, and leave scripted eval
  execution as future work.

## Interfaces & Data Structures

### Core Interfaces

```text
Fixture ID: AOE-<surface>-###
Surface: docs | provider | infra
Scenario: task input shape
Required Context: repo-local sources to inspect
Expected Output: observable output properties
Scoring Criteria: manual or future-scriptable checks
Block Conditions: conditions that fail the fixture
Evidence: validation commands or docs evidence to record
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation Specialist, Agentic Workflow Specialist, QA
  Engineer, or Infrastructure Reviewer.
- **Inputs**: User task, changed files, repo-local source docs, validation
  commands, and selected fixture.
- **Outputs**: Task evidence, final summary, validation results, and optional
  fixture score.
- **Success Definition**: The fixture reference can be used to evaluate common
  docs, provider, and infrastructure outputs without changing runtime behavior.

## Tools & Tool Contract (If Applicable)

- **Tool List**: shell, `rg`, `git diff --check`, documentation validators,
  LLM Wiki generator, repo contracts.
- **Permission Boundary**: Fixtures must not require secret values, remote
  mutation, paid jobs, provider runtime changes, workflow changes, deployments,
  or live service inspection.
- **Failure Handling**: If fixture evidence conflicts with Stage 00 policy or
  active user instructions, Stage 00/user instructions win and the fixture is
  recorded as not applicable.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Agent outputs must cite concrete changed
  files, validation results, protected-surface boundaries, and skipped-check
  rationale.
- **Policy Constraints**: No secret values, no raw logs, no shell history, no
  remote mutation claims without evidence, and no unverified provider feature
  claims.
- **Versioning Rule**: Fixture changes require a logical commit and generated
  index refresh.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: The active task file records selected fixtures and
  validation results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  the fixture pack closure.
- **Retrieval Boundary**: Graphify remains advisory; fixture selection and
  scoring must be corroborated against tracked source files.

## Guardrails (If Applicable)

- **Input Guardrails**: Use only repository paths, task descriptions, and
  redacted metadata as fixture inputs.
- **Output Guardrails**: Score only observable output properties and validation
  evidence.
- **Blocked Conditions**: Secret-value exposure, unsupported remote-action
  claims, unverified provider parity claims, or runtime mutation without
  approval.
- **Escalation Rule**: Stop and request approval before changing protected
  runtime, workflow, provider, credential, remote GitHub, or secret surfaces.

## Evaluation (If Applicable)

- **Eval Types**: Manual checklist scoring now; future scripted fixture runner
  remains optional.
- **Metrics**: Fixture pass/fail plus criterion score where useful.
- **Datasets / Fixtures**: `agent-output-eval-fixtures.md` defines docs,
  provider, and infrastructure fixture scenarios.
- **How to Run**: Select a fixture, inspect required context, compare the final
  output and evidence against criteria, and record the result in task evidence.

## Edge Cases & Error Handling

- **Mixed-surface tasks**: Evaluate against every relevant fixture and use the
  strictest protected-surface condition.
- **Historical documents**: Preserve historical evidence unless the active
  chain would otherwise contradict current implementation.
- **External facts**: Revalidate current provider or framework facts before
  scoring output that depends on them.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Fixture criteria become stale relative to Stage 00 rules.
- **Fallback**: Treat the fixture as stale reference data and update it through
  a separate Stage 03/04 change.
- **Human Escalation**: Required when fixture scoring would imply protected
  mutation, policy adoption, or external action.

## Verification

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-AOE-001**: Stage 90 data reference defines docs, provider, and
  infrastructure fixtures with scoring criteria and block conditions.
- **VAL-AOE-002**: Stage 03/04 evidence and parent README indexes link the new
  fixture pack.
- **VAL-AOE-003**: Audit gap references point to the fixture pack and leave
  scripted or CI eval execution as future work.
- **VAL-AOE-004**: Documentation validation and repository contracts pass.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-05-agent-output-eval-fixtures.md](../../04.execution/plans/2026-07-05-agent-output-eval-fixtures.md)
- **Tasks**: [../../04.execution/tasks/2026-07-05-agent-output-eval-fixtures.md](../../04.execution/tasks/2026-07-05-agent-output-eval-fixtures.md)
- **Fixture reference**: [../../90.references/data/governance/agent-output-eval-fixtures.md](../../90.references/data/governance/agent-output-eval-fixtures.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
- **Loop research**: [../../90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md)
