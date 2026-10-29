---
name: "task-breakdown-agent"
description: "Use when an approved plan needs reversible logical work units with one implementer, acceptance checks, dependencies, and independent review."
metadata:
  title: "task-breakdown-agent"
  version: "1.2.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-10-29"
  function_id: "task-breakdown-agent"
  scope: "agentic"
  owner_agent: "workflow-supervisor"
---

# task-breakdown-agent

## Purpose

### Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

An approved Plan, dependency map, acceptance criteria, and protected-surface decisions must be complete.

## Inputs

- Approved plan and dependency map.
- Exact files, validation gates, role ownership, review requirements, and rollback boundaries.

## Procedure

1. Split work into independently reversible logical units whose combined output satisfies the approved acceptance map.
2. Assign one implementer scope, RED/GREEN evidence, validation set, commit boundary, and independent review to each unit.
3. Order dependencies, isolate protected/runtime work, and define the terminal evidence needed before the task can close.

### Gates

- Each unit maps to one logical commit or explicitly coupled small commit group.
- Implementation and independent review roles remain separate.

## Outputs

- Bounded work units suitable for co-located Task evidence and logical commits.

## Verification

- Every acceptance criterion is covered by at least one work unit.
- Each work unit names one implementer scope, its validation, its commit boundary, and an independent reviewer.
- Protected or runtime work is isolated into its own unit.

## Failure Handling

Return to planning when a unit cannot be made reversible, testable, or independently reviewable without hidden dependencies.

## References

- [Workflow supervisor](../../roles/workflow-supervisor.md)
- [Execution plan function](../execution-plan-agent/SKILL.md)
- [Subagent protocol](../../governance/agentic.md)
