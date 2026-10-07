---
title: "LAB Isolation and Service Selection Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0215-PLAN-0001"
parent_ids:
- "SPEC-0215"
created: "2026-10-08"
---

# LAB Isolation and Service Selection Plan

## Overview

Lock the root closure first, then tighten each LAB and add the controller,
then record selection and disposition, then correct documents. Each unit is
one commit.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Root closure tests and `lab_net` retirement | None | TSK-0001 | Task evidence |
| W2 | 2, 3 | LAB boundaries and the lease controller | W1 | TSK-0001 | Task evidence |
| W3 | 4 | Budget, selection and disposition rules | W2 | TSK-0001 | Task evidence |
| W4 | 4, 5 | HA wording, LAB guides and final validation | W3 | TSK-0001 | Task evidence |

## Verification Plan

Run focused tests RED before GREEN, render the root and every LAB, exercise
the controller against a fake Docker binary and once against real Docker with
a synthetic LAB data root, then the registered changed-profile local gate and
the pinned staged lint. Remote PR `candidate-quality` owns candidate
acceptance.

## Risks and Rollback

MongoDB and OpenSearch cluster state moves from project named volumes to
`LAB_DATA_DIR` binds; existing named volumes are left untouched and are not
migrated. Reverting the commits restores the previous files; no HOME state is
changed. RedisInsight loses the unused `lab_net` attachment, which reached no
LAB service.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-lab-isolation-and-service-selection.md)
