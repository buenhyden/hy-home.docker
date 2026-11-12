---
title: "Completed Spec Package Deletion Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0250-PLAN-0001"
parent_ids:
- "SPEC-0250"
created: "2026-11-03"
---

# Completed Spec Package Deletion Plan

## Overview

### Goal and Boundary

Prepare the checks first, then delete the packages and reserve their numbers,
then unlink current documents, and finally update governance and record the
evidence.

Document-governance libraries and tests, the Registry, the Stage 03 README,
current documents that linked into deleted packages, the documentation
protocol, and this package.

Parent Spec:

- [Spec](spec.md)

### Assumptions

The plan works under the approved SPEC-0250; it assumes no authority beyond it.

## Dependencies

### Prerequisites

The plan needs only the approved Spec and the document-governance libraries, tests, Registry and documents named in its Goal and Boundary; it names no further external contract.

### Dependency Order

W1 has no dependency. W2 starts after W1; W3 and W4 start after W2. W5 starts after W1 to W4.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 3 | Drop the SPEC-0211 Resolves correction; read only present packages in generation 7 admission; excuse terminal Task links into reserved packages | None | TSK-0001 | governance and lifecycle unit suites |
| W2 | 1 | Delete the fully terminal packages except the proof carriers; reserve their numbers; drop their README rows | W1 | TSK-0001 | corpus lifecycle; metadata check-changed |
| W3 | 2, 3 | Unlink current documents; drop the RUN-0098 parent; repoint test fixtures | W2 | TSK-0001 | links alignment |
| W4 | 2 | Describe the deletion rule in the documentation protocol and Stage 03 README | W2 | TSK-0001 | review against code |
| W5 | 4 | Record local results | W1–W4 | TSK-0001 | the checks above |

### Change and Rollback

Revert the
branch to restore the deleted packages; no outside state changes.

## Verification Plan

### Verification Matrix

Run `tests/lib/document_governance`, `tests/validation/lifecycle`, the gate,
CI routing and CI gate plan suites, `test_ci_gate_evidence` under system
python3, `check-document-metadata.py` in `check-changed` and `check-active`
modes, `check-document-corpus-lifecycle.py`, `check-document-links.py` in
`alignment` and `commands` modes, `check-script-manifest.py`, and the provider
renderer `--check`.

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix, which lists the local, `check-changed` and `check-active` runs; the Task records each run.

## Risks

### Risks and Mitigations

A check that relied on a deleted package fails in its unit suite or in corpus
lifecycle, which W5 runs. Deleted bodies stay in version history.

### Escalation

Work stops and returns to the owner when a required check fails or an approval is missing, per the stop rules in [docs/03.specs/AGENTS.md](../AGENTS.md).

## Promotion Map

### Durable Meaning

The lasting meaning lives in the Registry reserved numbers, the deletion rule W4 adds to the documentation protocol and the Stage 03 README.

### Owner and Receipt

Owner @buenhyden. The receipt is the local result recorded in TSK-0001 (W5).

- [Task](tasks/tsk-0001-finished-spec-package-deletion.md)
