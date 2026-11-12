---
title: "SPEC-0209 and SPEC-0231 Retirement Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0260-PLAN-0001"
parent_ids:
- "SPEC-0260"
created: "2026-11-04"
---

# SPEC-0209 and SPEC-0231 Retirement Plan

## Overview

### Goal and Boundary

Move the migration proof source to the generation 6 revision first, prove it
with tests, then delete the two packages and update the documents.

The files named in the Spec; no runtime or remote state changes.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved SPEC-0260; it assumes no authority beyond it, and no runtime or remote state changes.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1 has no dependencies; W2 starts after W1; W3 starts after W1-W2.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Read migration proofs from the generation 6 revision; add tests | None | TSK-0001 | spec package tests |
| W2 | 3 | Delete both packages, reserve 209 and 231, update the index and the documentation protocol | W1 | TSK-0001 | metadata check-changed; links |
| W3 | 4 | Record local results | W1–W2 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to restore both
packages and the loader; no outside state changes.

## Verification Plan

### Verification Matrix

Run `check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-document-links.py` in
`alignment`, `navigation`, `language`, `traceability`, `entrypoint` and
`commands` modes, the spec package, Registry and identity history tests, and
the full `tests/lib/document_governance` discovery.

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix; the Task records each run.

## Risks

### Risks and Mitigations

A proof read from the wrong revision would admit the wrong Tasks; W1's tests
fail closed when the proof is absent.

### Escalation

The Spec states: "This Task pushes and merges nothing."

## Promotion Map

### Durable Meaning

The retirement of SPEC-0209 and SPEC-0231 lands in the generation 6 proof source, the spec package index and the documentation protocol.

### Owner and Receipt

Owner @buenhyden. The receipt is TSK-0001, named in the Work Breakdown Task column.

- [Task](tasks/tsk-0001-spec-0209-0231-retirement.md)
