---
title: "REQ-0027 Approval Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0261-PLAN-0001"
parent_ids:
- "SPEC-0261"
created: "2026-11-04"
---

# REQ-0027 Approval Plan

## Overview

### Goal and Boundary

Approve REQ-0027, then compare and promote the dependent documents in one batch.

The files named in the Spec; no runtime or remote state changes.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved SPEC-0261; it assumes no authority beyond it, and no runtime or remote state changes.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1 has no dependencies; W2 and W3 start after W1; W4 starts after W1-W3.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Approve REQ-0027 and reword its draft sentence | None | TSK-0001 | metadata check-changed |
| W2 | 2 | Compare AD-0031 and AD-0032 with Compose; promote if matching | W1 | TSK-0001 | metadata check-changed |
| W3 | 3 | Compare the nine Stage 05 documents with source; promote if matching | W1 | TSK-0001 | metadata check-changed; check-active |
| W4 | 4 | Record local results | W1-W3 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to
restore.

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

A promotion could mark an unproven document active; W2 and W3 promote only
after comparing concrete claims and keep the rest draft.

### Escalation

The Spec states: "This Task pushes and merges nothing."

## Promotion Map

### Durable Meaning

The REQ-0027 approval and the promoted AD-0031, AD-0032 and Stage 05 documents hold the durable meaning.

### Owner and Receipt

Owner @buenhyden. The receipt is TSK-0001, named in the Work Breakdown Task column.

- [Task](tasks/tsk-0001-req-0027-approval.md)
