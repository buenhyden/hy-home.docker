---
title: "Evaluation Migration and Recovery Acceptance"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0009"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Evaluation Migration and Recovery Acceptance

## Objective

Implement Plan W9: move the four evaluation subsystem sources from evals to
.agents/evaluations, preserve actual consumers and historical continuity, and
add recovery review evaluation using the existing model-free engine.

## Inputs

- [Approved Spec](../spec.md) and [approved Plan](../plan.md), including the
  owner-selected migration and exact historical-baseline amendment.
- [W7 evidence](tsk-0007-workflow-and-handoff.md): committed cf540281f;
  evaluator fixtures 10/10 and regressions 38/38, ET 54/54 PASS.
- [W8 task](tsk-0008-native-hooks.md) owns disjoint native/hook files.
- Exact file ownership is the Plan W9 map. Root owns this Task, Spec, Plan and
  commits. Mechanical migration precedes evaluator changes; writers hand off
  shared files explicitly. No index changes by workers or overlapping writers.
- Approved local changes, checks, independent review and logical commits only.

## Work Log

Read-only consumer audit selected .agents/evaluations for all four dedicated
subsystem files, retaining ordinary tests and fixtures in tests. No duplicate
source or permanent redirect is needed. Preserve executable modes.

The old evaluation README is absent from metadata's historical base corpus.
Use the existing lifecycle helper for one exact trusted historical-path mapping;
retain type, identity, lifecycle and introduced-body checks. No new migration
engine, schema, profile, unrestricted inventory exclusion or state override.

## Verification Evidence

NOT_RUN: equivalent pre/post move E, focused migration RED/GREEN, recovery
paired regressions, E/ET/G/C/L, consumer/registry/manifest/workflow tests,
renderer parity and changed metadata against the actual pre-move predecessor.

Recovery rubric is fixed before scoring: state/ownership, backup or justified
rebuild, consistency, retention/capacity, key custody, dependency order, versions,
isolation, RPO/RTO objectives versus observations, application acceptance,
stop/partial-result conditions and three distinct responsible people. Use the
existing 0.50 safety-fixture threshold plus mandatory completeness/refusal
conditions. Synthetic no-skill examples are not native efficacy observations.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R15/R20/R31/R32/R33/R36/R38/R39 | W9 | NOT_RUN | Existing evaluation subsystem and its registered consumers |

## Review Evidence

Independent migration, evaluation and documentation review pending. Evaluation
responses are input data, never automatically loaded execution instructions.

## Commit Ledger

Root records actual draft, ready and in-progress predecessors before GO.
No W9 implementation has begun.

## Rulings

- Register exactly four canonical evaluation files; reject unknown siblings.
- Replace the existing README profile path and exclude only the code-owned
  catalog from document inventory, retaining its executable contract checks.
- Add fixture and typed threshold together; retain score interfaces and existing
  failure detection. Remove obsolete current criteria, not historical evidence.
- Preserve all-six-suite impact, existing workflow identities and test ownership.
- Project-only skill stocktake reuses the existing disposition table; no global
  cache, personal usage data, new framework or speculative packaging modes.

## Deferred Items

W10 owns final branch acceptance. Native, editor, hosted, paid-budget and actual
recovery observations remain separate and unclaimed by static fixtures.
