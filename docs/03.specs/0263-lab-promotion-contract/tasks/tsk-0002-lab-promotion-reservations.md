---
title: "LAB Promotion Reservations Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0263-TSK-0002"
parent_ids:
- "SPEC-0263-PLAN-0001"
created: "2026-11-06"
---

# LAB Promotion Reservations Task

## Overview

### Objective

Carry out Plan work unit W7: the resource rule moves from summed limits to
summed reservations plus an external-workload allowance, and the unmeasured
section 5 sub-checks become owner check items.

## Inputs and Authorization

The owner made these decisions on 2026-11-06, after PR #753 merged:

- the resource rule judges declared reservations, not limits;
- the unmeasured section 5 sub-checks become owner check items;
- reservations are declared in the shared resource templates;
- the values are sized from measured usage plus a margin;
- external containers such as k3d count as a fixed allowance in the
  operations policy.

This Task starts, stops and recreates no container. The HOME services pick up
the new reservations only when they are recreated, in an owner window.

## Work Log

### Current contract decision

SPEC-0263 moves to `in-review` for the amendment to version 0.3.0. It returns
to `approved` when the owner approves the amended Spec.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0263 | approved | in-review | #current-contract-decision |

### Measurements

On 2026-11-06, read-only:

- 60 running containers used about 3.18 CPUs and 9358 MiB in total
  (`docker stats --no-stream`).
- The five k3d containers used about 1.0 CPU and 4.1 GiB.
- Of the 97 HOME services in the root render, 97 declare limits and 2
  (`dcgm-exporter`, `ollama`) declare reservations.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 8 | W7 | metadata | `check-document-metadata.py --mode check-changed --base-ref main` on the amendment working tree over `5989bf1c9` | PASS | selected=4 violations=0 | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 8 | pending | - | - | @buenhyden |

## Review and Completion

The amended Spec waits for owner approval. No implementation has started.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Task 0001](tsk-0001-lab-promotion-contract.md)
