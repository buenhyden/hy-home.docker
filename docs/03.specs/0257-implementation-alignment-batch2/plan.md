---
title: "Implementation Alignment Batch 2 Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0257-PLAN-0001"
parent_ids:
- "SPEC-0257"
created: "2026-11-04"
---

# Implementation Alignment Batch 2 Plan

## Overview

Apply the batch 2 findings SPEC-0255 deferred, in one branch.

## Scope

The files named in the Spec; no runtime or remote state changes.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Map each missing operations path to its domain folder by category and file name | None | TSK-0001 | path scan |
| W2 | 2 | Grafana Compose link and `infra/09-platform-ops` audience | None | TSK-0001 | links alignment |
| W3 | 3 | Empty the two dangling Registry entries | None | TSK-0001 | metadata check-active |
| W4 | 4 | Add the missing secret names to their guides | None | TSK-0001 | secret-name scan |
| W5 | 5 | Record local results | W1–W4 | TSK-0001 | the checks above |

## Verification Plan

Run `check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-operations-catalog.py`, and
`check-document-links.py` in `alignment`, `navigation`, `language`,
`traceability` and `entrypoint` modes.

## Risks and Recovery

### Risks and Rollback

W1 rewrites a path only when exactly one file matches its category and name;
any other case is left and reported. Revert the branch to restore the text.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-implementation-alignment-batch2.md)
