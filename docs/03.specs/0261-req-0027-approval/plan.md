---
title: "REQ-0027 Approval Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0261-PLAN-0001"
parent_ids:
- "SPEC-0261"
created: "2026-11-04"
---

# REQ-0027 Approval Plan

## Overview

Approve REQ-0027, then compare and promote the dependent documents in one batch.

## Scope

The files named in the Spec; no runtime or remote state changes.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Approve REQ-0027 and reword its draft sentence | None | TSK-0001 | metadata check-changed |
| W2 | 2 | Compare AD-0031 and AD-0032 with Compose; promote if matching | W1 | TSK-0001 | metadata check-changed |
| W3 | 3 | Compare the nine Stage 05 documents with source; promote if matching | W1 | TSK-0001 | metadata check-changed; check-active |
| W4 | 4 | Record local results | W1-W3 | TSK-0001 | the checks above |

## Verification Plan

Run `check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-operations-catalog.py`, and
`check-document-links.py` in `alignment`, `navigation`, `language`,
`traceability` and `entrypoint` modes.

## Risks and Recovery

### Risks and Rollback

A promotion could mark an unproven document active; W2 and W3 promote only
after comparing concrete claims and keep the rest draft. Revert the branch to
restore.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-req-0027-approval.md)
