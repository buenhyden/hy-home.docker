---
layer: agentic
---

# execution-plan-agent

## Overview

Bridges Stage 03 (specs) to Stage 04 (execution) by decomposing approved specs
into implementation plans using `plan.template.md`.

## Purpose

Transform a completed spec into a `docs/04.execution/plans/` plan document with
execution order, dependencies, risk controls, rollback steps, and verification
commands.

## Scope

**Covers:**

- Spec-to-plan decomposition
- Risk level assignment (low / medium / high)
- Rollback and verification criteria definition

**Excludes:**

- Actual implementation (this function only plans)
- Task evidence recording (handled by task-breakdown-agent)

## Structure

- Reads source spec from `docs/03.specs/<tier>/spec.md`
- Uses `docs/99.templates/plan.template.md`
- Outputs to `docs/04.execution/plans/YYYY-MM-DD-<topic>.md`

## Agents

- **doc-writer** — primary caller

## Skills

- `.claude/skills/execution-plan-agent/skill.md`

## Usage

- **Inputs:** approved spec, plan template, existing plans list
- **Outputs:** new plan file, updated execution README index

## Related Documents

- `../../scopes/docs.md`
- `../../rules/stage-authoring-matrix.md`
- `../README.md`
