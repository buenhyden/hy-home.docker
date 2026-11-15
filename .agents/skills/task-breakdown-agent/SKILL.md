---
name: "task-breakdown-agent"
description: "Use when an approved plan needs reversible logical work units with one implementer, acceptance checks, dependencies, and review by risk."
metadata:
  title: "task-breakdown-agent"
  version: "1.3.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-15"
  function_id: "task-breakdown-agent"
  scope: "agentic"
  owner_agent: "workflow-supervisor"
---

# task-breakdown-agent

## Purpose and Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

An approved Plan, dependency map, acceptance criteria, and protected-surface decisions must be complete.

### When Not to Use

None: this skill states no exclusion.

## Procedure

### Steps

1. Split work into independently reversible logical units whose combined output satisfies the approved acceptance map.
2. Assign one implementer scope, RED/GREEN evidence, validation set, commit boundary, and review class (independent for high-risk, author check for low-risk) to each unit.
3. Order dependencies, isolate protected/runtime work, and define the terminal evidence needed before the task can close.

#### Gates

- Each unit maps to one logical commit or explicitly coupled small commit group.
- Implementation and independent review roles remain separate for high-risk units.

### Failure Handling

Return to planning when a unit cannot be made reversible, testable, or independently reviewable without hidden dependencies.

## Inputs and Outputs

### Inputs

- Approved plan and dependency map.
- Exact files, validation gates, role ownership, review requirements, and rollback boundaries.

### Outputs

- Bounded work units suitable for co-located Task evidence and logical commits.

## Verification

### Checks

- Every acceptance criterion is covered by at least one work unit.
- Each work unit names one implementer scope, its validation, its commit boundary, and its review class, with an independent reviewer for a high-risk unit.
- Protected or runtime work is isolated into its own unit.

### Completion and Handoff

Owning role, policies and related documents:

- [Workflow supervisor](../../roles/workflow-supervisor.md)
- [Execution plan function](../execution-plan-agent/SKILL.md)
- [Subagent protocol](../../governance/agentic.md)
