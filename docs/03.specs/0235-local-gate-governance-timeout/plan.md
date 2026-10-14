---
title: "Local Gate Governance Timeout Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0235-PLAN-0001"
parent_ids:
- "SPEC-0235"
created: "2026-10-13"
---

# Local Gate Governance Timeout Plan

## Overview

Measure the node's batch, change one value, then prove the local gate passes
the node.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 2 | Measure the node's module batch on this host | None | TSK-0001 | Task evidence |
| W2 | 1 | Set the node timeout to 45 minutes; contract tests; ci-cd review | W1 | TSK-0001 | Task evidence |
| W3 | 4 | Reachability test admits class selections; ci-cd review | W2 | TSK-0001 | Task evidence |
| W4 | 3 | Full local changed gate and hosted candidate | W2, W3 | TSK-0001 | Task evidence |

## Verification Plan

Run the node's argv module list with `python3 -m unittest` and record the
elapsed time; run the CI gate contract tests and the workflow contract check;
run the local changed gate with no outer limit; read hosted
`candidate-quality`.

## Risks and Rollback

- **A hung test waits longer.** A real hang now takes 45 minutes to surface
  locally instead of 15. Hosted CI is unaffected because the node is local
  only.
- **Rollback.** Revert the one-line change.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-local-gate-governance-timeout.md)
