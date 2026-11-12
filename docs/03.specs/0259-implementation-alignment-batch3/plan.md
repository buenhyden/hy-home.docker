---
title: "Implementation Alignment Batch 3 Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0259-PLAN-0001"
parent_ids:
- "SPEC-0259"
created: "2026-11-04"
---

# Implementation Alignment Batch 3 Plan

## Overview

### Goal and Boundary

Fix the verified labels and sentence, accept ADR-0038, and promote matching
draft documents in one batch.

The files named in the Spec; no runtime or remote state changes.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved SPEC-0259; it assumes no authority beyond it, and no runtime or remote state changes.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1, W2 and W3 have no dependencies; W4 starts after W1-W3.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Relabel Stage 02 deleted-Spec link lines | None | TSK-0001 | links alignment |
| W2 | 2 | RUN-0105 declared versus observed audit sentence | None | TSK-0001 | metadata check-changed |
| W3 | 3 | Accept ADR-0038; review and promote draft documents | None | TSK-0001 | metadata check-changed; check-active |
| W4 | 4 | Record local results | W1-W3 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to restore.

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

A promotion could mark an unproven document active; W3 promotes only after the
reference check and keeps the rest draft.

### Escalation

The Spec states: "This Task pushes and merges nothing."

## Promotion Map

### Durable Meaning

The labels, the ADR-0038 acceptance and the document promotions land in the files named in the Spec.

### Owner and Receipt

Owner @buenhyden. The receipt is TSK-0001, named in the Work Breakdown Task column.

- [Task](tasks/tsk-0001-implementation-alignment-batch3.md)
