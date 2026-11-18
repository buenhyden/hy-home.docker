---
name: "execution-plan-agent"
description: "Use when an approved specification needs an executable plan mapping acceptance criteria to exact files, ordered work, risks, and checks."
metadata:
  title: "execution-plan-agent"
  version: "1.4.1"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-18"
  function_id: "execution-plan-agent"
  scope: "agentic"
  owner_agent: "workflow-supervisor"
---

# execution-plan-agent

## Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

An approved specification and corroborated repository baseline must exist; unresolved decisions that alter scope remain blocking.

### When Not to Use

Interfaces, authority or completion criteria that cannot be made concrete are outside this skill; they return to the specification.

## Procedure

### Steps

1. Reconcile read-only discovery with the latest request using the
   [request brief](../../governance/agentic.md#request-brief). For a registered
   brief, consume the same request binding, exact paths, affected questions
   and acceptance criteria in the Plan and worker envelope.
2. Map every acceptance criterion to exact files, implementation steps,
   tests and task evidence without claiming prospective results.
3. Order work by dependency and reversibility, isolating protected or runtime changes into separately approved tasks.
4. Define RED/GREEN checks, review gates, commit boundaries, and terminal completion criteria.

#### Gates

- File scope and ownership are explicit.
- Verification commands prove each acceptance criterion and name skipped/CI-only gates.

#### Inputs

- Approved specification and repository evidence.
- File ownership, dependencies, risks, verification commands, and rollback boundaries.

### Failure Handling

Return to specification when interfaces, authority, or completion criteria cannot be made concrete; do not fill gaps with assumptions.

## Outputs

### Artifacts

- An executable Plan co-located at `docs/03.specs/####-<slug>/plan.md` with exact file map, sequence, risks, and verification ladder.

### Handoff

Owning role, policies and related documents:

- [Workflow supervisor](../../roles/workflow-supervisor.md)
- [Task breakdown](../task-breakdown-agent/SKILL.md)
- [Task checklists](../../../docs/00.workspace/03.quality/task-checklists.md)

## Verification

### Checks

- Every acceptance criterion maps to at least one Work Unit with exact files and a verification command.
- `scripts/validation/check-document-metadata.py --mode check-changed` reports no violation for the Plan.
- Skipped and CI-only gates are named in the Plan.

### Limits

The local checks do not prove skipped or CI-only gates; the Plan names them.
