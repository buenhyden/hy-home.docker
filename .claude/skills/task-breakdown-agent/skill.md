---
name: task-breakdown-agent
description: >
  Decompose an approved implementation plan into task evidence documents in
  docs/04.execution/tasks/. Tracks per-step status, validation results, and
  deviation notes using task.template.md.
---

# task-breakdown-agent

Creates and updates task evidence documents from implementation plans.

## Trigger Examples

- "Create a task doc for the 2026-05-26-workspace-audit plan"
- "Track execution status for plan 2026-05-22-spec-execution-implementation-audit"
- "Update the task evidence for the observability plan"

## Purpose

Maintain a task document that records what was actually done, what was
verified, and what deviated from the plan. The task is the audit trail;
the plan is the intention.

## Bootstrap

1. Read `AGENTS.md` and `docs/00.agent-governance/rules/stage-authoring-matrix.md`.
2. Read the source plan file in `docs/04.execution/plans/`.
3. Read `docs/99.templates/task.template.md` for the task structure.
4. Check `docs/04.execution/tasks/` for any existing task for the same plan.

## Working Rules

- One task per plan. Update in place; do not create duplicates.
- Task filename matches the plan: `docs/04.execution/tasks/YYYY-MM-DD-<topic>.md`.
- Task must not contain new requirements, architecture decisions, or spec content.
- Record actual commands run, actual output received, and pass/fail per step.
- Deviation from plan must be noted with reason.
- Mark steps Done, Deferred, or Blocked — never leave rows empty.

## Inputs

| Input | Source |
| ----- | ------ |
| Source plan | `docs/04.execution/plans/YYYY-MM-DD-<topic>.md` |
| Task template | `docs/99.templates/task.template.md` |
| Verification commands | Plan's Verification Plan section |

## Outputs

- New or updated task file at `docs/04.execution/tasks/YYYY-MM-DD-<topic>.md`
- Updated `docs/04.execution/README.md` Completed Evidence entry

## Related Skills

- `execution-plan-agent` — upstream plan creation
- `ops-runbook-agent` — when completed task evidence graduates to runbook
