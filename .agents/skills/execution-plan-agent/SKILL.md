---
name: "execution-plan-agent"
description: "Use when an approved specification needs an executable plan mapping acceptance criteria to exact files, ordered work, risks, and checks."
metadata:
  title: "execution-plan-agent"
  version: "1.1.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-06"
  function_id: "execution-plan-agent"
  scope: "agentic"
  owner_agent: "workflow-supervisor"
---

# execution-plan-agent

## Preconditions

Invoke this procedure explicitly. Invocation does not select a role or grant the
owning role's permissions. Use the already selected role's permission profile and
approved Task scope; route to the owner when incompatible.

An approved specification and corroborated repository baseline must exist; unresolved decisions that alter scope remain blocking.

## Inputs

- Approved specification and repository evidence.
- File ownership, dependencies, risks, verification commands, and rollback boundaries.

## Procedure

1. Map every acceptance criterion to exact files, implementation steps, tests, and task evidence without claiming prospective results.
2. Order work by dependency and reversibility, isolating protected or runtime changes into separately approved tasks.
3. Define RED/GREEN checks, review gates, commit boundaries, and terminal completion criteria.

## Outputs

- An executable Plan co-located at `docs/03.specs/####-<slug>/plan.md` with exact file map, sequence, risks, and verification ladder.

## Gates

- File scope and ownership are explicit.
- Verification commands prove each acceptance criterion and name skipped/CI-only gates.

## Failure Handling

Return to specification when interfaces, authority, or completion criteria cannot be made concrete; do not fill gaps with assumptions.

## Related Documents

- [Workflow supervisor](../../roles/workflow-supervisor.md)
- [Task breakdown](../task-breakdown-agent/SKILL.md)
- [Task checklists](../../governance/task-checklists.md)
