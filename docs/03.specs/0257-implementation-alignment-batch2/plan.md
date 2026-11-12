---
title: "Implementation Alignment Batch 2 Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0257-PLAN-0001"
parent_ids:
- "SPEC-0257"
created: "2026-11-04"
---

# Implementation Alignment Batch 2 Plan

## Overview

### Goal and Boundary

Apply the batch 2 findings SPEC-0255 deferred, in one branch.

The files named in the Spec; no runtime or remote state changes.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved Spec and assumes no authority beyond it.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1 to W4 have no dependency; W5 records the results after W1 to W4.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Map each missing operations path to its domain folder by category and file name | None | TSK-0001 | path scan |
| W2 | 2 | Grafana Compose link and `infra/09-platform-ops` audience | None | TSK-0001 | links alignment |
| W3 | 3 | Empty the two dangling Registry entries | None | TSK-0001 | metadata check-active |
| W4 | 4 | Add the missing secret names to their guides | None | TSK-0001 | secret-name scan |
| W5 | 5 | Record local results | W1–W4 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to restore the text.

## Verification Plan

### Verification Matrix

Run `check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-operations-catalog.py`, and
`check-document-links.py` in `alignment`, `navigation`, `language`,
`traceability` and `entrypoint` modes.

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix; the Task records each run.

## Risks

### Risks and Mitigations

W1 rewrites a path only when exactly one file matches its category and name; any other case is left and reported.

### Escalation

The Spec states: "This Task pushes and merges nothing."

## Promotion Map

### Durable Meaning

The corrected paths, links, Registry entries and secret names live in the documents and guides named in the Spec.

### Owner and Receipt

The owner is @buenhyden; the receipt is the Task named in the Work Breakdown.

- [Task](tasks/tsk-0001-implementation-alignment-batch2.md)
