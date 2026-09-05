---
title: "Lifecycle Reconciliation and RED Contracts Task"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0001"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Lifecycle Reconciliation and RED Contracts Task

## Objective

Reconcile the completed SPEC-0172 outcome with the current document-lifecycle
contract, then establish failing tests for the ownership and residue boundaries
that SPEC-0173 will change.

## Inputs

- [SPEC-0173](../spec.md) and its [implementation plan](../plan.md).
- The current SPEC-0172 package, Stage 03 index, Stage 98 catalog, registry,
  lifecycle validator, and Git recovery rules.
- The baseline invocation, script, test, fixture, document, and provider
  findings recorded in the Plan.

## Work Log

This planning artifact was created on 2026-09-05. No implementation command
has run and no production file belongs to this Task yet. During an authorized
execution, record each lifecycle transition and each RED test result before
changing the corresponding implementation.

## Verification Evidence

No execution evidence exists in this draft. The Plan defines the exact
lifecycle, metadata, recovery, and focused test commands; record command,
exit code, and relevant diagnostic only after separate execution approval.

## Review Evidence

No implementation review has occurred. Independent review starts only after
the Task's focused checks pass and must identify the reviewed commit.

## Commit Ledger

No implementation commit exists. The planning-package changes are not
implementation or acceptance evidence.

## Rulings

- Preserve the completed SPEC-0172 Spec as durable evidence under the Stage 98
  route required by the current policy.
- Treat terminal Plan and Task bodies as transient artifacts recoverable from
  Git; do not create archive copies that compete with the completed Spec.
- Correct the stale Stage 00 preservation sentence so Stage 00, the current
  Stage 03 index, and the Registry agree on terminal Plan/Task removal.
- Add RED contracts before changing gate, script, test, fixture, document, or
  provider behavior.

## Deferred Items

- Hosted execution, remote control-plane mutation, provider entitlement,
  deployment, release, push, pull request, and merge are outside this Task.
- No SPEC-0172 lifecycle transition or transient-body removal occurs during
  the planning-only phase.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Stage 03 index](../../README.md)
