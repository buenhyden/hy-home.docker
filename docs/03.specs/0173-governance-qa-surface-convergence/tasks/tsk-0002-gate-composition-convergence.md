---
title: "Gate Composition Convergence Task"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0002"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Gate Composition Convergence Task

## Objective

Make the workflow contract the single executable composition owner and prove
that each canonical leaf invocation occurs once per public profile and context.

## Inputs

- [SPEC-0173](../spec.md), its [implementation plan](../plan.md), and the RED
  contracts produced by Task 0001.
- `.github/workflow-contract.yml`, `scripts/manifest.yaml`, the gate runner,
  setup dispatchers, CI workflow, pre-commit configuration, and focused tests.
- Baseline duplicate identities for Compose validation and frontend dependency
  setup.

## Work Log

This planning artifact was created on 2026-09-05. No gate composition,
manifest field, workflow, or hook has been changed. During an authorized
execution, record the RED result, the smallest composition edit, and the GREEN
result for every semantic route.

## Verification Evidence

No execution evidence exists in this draft. Acceptance requires focused DAG
tests that normalize `realpath`, arguments, profile, and mode, followed by the
public profile checks named in the Plan.

## Review Evidence

No implementation review has occurred. Independent review must confirm that
no second executable registry or hidden aggregate was introduced.

## Commit Ledger

No implementation commit exists. The planning-package changes are not
implementation or acceptance evidence.

## Rulings

- `.github/workflow-contract.yml` owns executable ordering and routing.
- `scripts/manifest.yaml` remains an inventory and lifecycle owner; it does not
  retain duplicate suite, context, or argument composition.
- Remove duplicate invocations rather than suppressing duplicate diagnostics.

## Deferred Items

- Changing remote required checks, branch protection, or Hosted CI state is
  outside this Task.
- The `validation-changed` and `validation-full` public names remain stable.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Lifecycle and RED contracts Task](tsk-0001-lifecycle-and-red-contracts.md)
