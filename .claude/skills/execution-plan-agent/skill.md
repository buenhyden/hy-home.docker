---
name: execution-plan-agent
description: >
  Bridge Stage 03 (specs) to Stage 04 (execution) in the hy-home.docker
  documentation lifecycle. Decomposes approved specs into implementation plans
  using plan.template.md, with risk, rollback, and verification criteria.
---

# execution-plan-agent

Creates implementation plans from approved specs in `docs/03.specs/`.

## Trigger Examples

- "Create an execution plan for the observability spec"
- "Decompose docs/03.specs/007-observability/spec.md into a plan"
- "Turn the Vault spec into a plan with rollback criteria"

## Purpose

Transform a completed, approved spec into a `docs/04.execution/plans/` plan
document that defines execution order, dependencies, risk controls, rollback
steps, and verification commands. Does not implement; only plans.

## Bootstrap

1. Read `AGENTS.md` and `docs/00.agent-governance/rules/stage-authoring-matrix.md`.
2. Read the target spec file in `docs/03.specs/`.
3. Read `docs/99.templates/templates/sdlc/plan.template.md` for the plan structure.
4. Check `docs/04.execution/plans/` for any existing plan for the same spec.

## Working Rules

- One plan per spec. Do not duplicate existing plans.
- Plan filename: `docs/04.execution/plans/YYYY-MM-DD-<topic>.md`.
- Plan must include: Goals, Work Breakdown, Verification Plan, Risks, Rollback.
- Risk level must be assigned: low / medium / high.
- Medium and high risk items require explicit user approval before implementing.
- Link back to source spec in Related Documents.

## Inputs

| Input | Source |
| ----- | ------ |
| Approved spec | `docs/03.specs/<tier>/spec.md` |
| Plan template | `docs/99.templates/templates/sdlc/plan.template.md` |
| Existing plans | `docs/04.execution/plans/` |

## Outputs

- New plan file at `docs/04.execution/plans/YYYY-MM-DD-<topic>.md`
- Updated `docs/04.execution/README.md` Completed Evidence and Related Documents

## Related Skills

- `task-breakdown-agent` — downstream plan → task decomposition
- `requirements-to-design-agent` — upstream stage 01→02 handoff
