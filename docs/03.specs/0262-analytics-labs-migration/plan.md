---
title: "Analytics Labs Migration Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0262-PLAN-0001"
parent_ids:
- "SPEC-0262"
created: "2026-11-04"
---

# Analytics Labs Migration Plan

## Overview

### Goal and Boundary

Move the services into LAB entrypoints, then reconcile every reference and
record the checks.

The files named in the Spec; no runtime or remote state changes.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved SPEC-0262; it assumes no authority beyond it, and no runtime or remote state changes.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1 has no dependencies; W2 and W3 start after W1; W4 starts after W1-W3.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Write the LAB entrypoints, move assets, drop root includes and unused secrets | None | TSK-0001 | compose config; LAB isolation tests |
| W2 | 3 | Update tests, hardening, catalogs, ledger, READMEs and Stage 01/02 statements | W1 | TSK-0001 | unit tests; hardening |
| W3 | 4 | Move the Stage 05 documents to `15-labs` and update their claims | W1 | TSK-0001 | operations catalog; metadata; links |
| W4 | 5 | Record local results | W1-W3 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to restore the root
includes.

## Verification Plan

### Verification Matrix

Run `docker compose config` for the root and each LAB, the full unit suite,
`check-all-hardening.sh`, `check-document-metadata.py` in `check-changed` and
`check-active` modes, `check-document-links.py --mode all`,
`check-document-corpus-lifecycle.py`, `check-operations-catalog.py` and
`check-script-manifest.py`.

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix; the Task records each run.

## Risks

### Risks and Mitigations

A LAB cannot reach its HOME dependency without an approved endpoint; the
Task records this as an owner decision.

### Escalation

A LAB that cannot reach its HOME dependency without an approved endpoint stops at the owner decision the Task records.

## Promotion Map

### Durable Meaning

The LAB entrypoints and the Stage 05 documents under `15-labs` hold the durable meaning.

### Owner and Receipt

Owner @buenhyden. The receipt is TSK-0001, named in the Work Breakdown Task column.

- [Task](tasks/tsk-0001-analytics-labs-migration.md)
