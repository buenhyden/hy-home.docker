---
title: "Implementation Alignment Fixes Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0255-PLAN-0001"
parent_ids:
- "SPEC-0255"
created: "2026-11-04"
---

# Implementation Alignment Fixes Plan

## Overview

### Goal and Boundary

Correct the verified audit findings that no open branch owns, in one batch;
the findings that touch files open elsewhere wait for a second batch.

The files named in the Spec; no runtime or remote state changes.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved Spec and assumes no authority beyond it.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1, W2 and W3 have no dependency; W4 records the results after W1 to W3.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | AD-0026 network rows and the GDE-0077 anchor | None | TSK-0001 | links alignment |
| W2 | 2 | Rewrite present-tense pointers to deleted Specs | None | TSK-0001 | metadata check-changed |
| W3 | 3 | POL-0004 globs, REQ-0005 ownership, POL-0021 database list, SonarQube README key, secret names, provenance and audience fixes | None | TSK-0001 | metadata check-changed; links |
| W4 | 4 | Record local results | W1–W3 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to restore the previous text; no outside state changes.

## Verification Plan

### Verification Matrix

Run `check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-operations-catalog.py`, and
`check-document-links.py` in `alignment`, `navigation`, `language` and
`traceability` modes.

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix; the Task records each run.

## Risks

### Risks and Mitigations

A wrong subnet or member would mislead an operator; W1 copies each value from Compose.

### Escalation

The Spec states: "This Task pushes and merges nothing."

## Promotion Map

### Durable Meaning

The corrected values live in AD-0026, GDE-0077, POL-0004, REQ-0005, POL-0021 and the other documents named in the Spec.

### Owner and Receipt

The owner is @buenhyden; the receipt is the Task named in the Work Breakdown.

- [Task](tasks/tsk-0001-implementation-alignment-fixes.md)
