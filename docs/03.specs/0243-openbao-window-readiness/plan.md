---
title: "OpenBao Maintenance Window Readiness Plan"
version: "0.1.4"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0243-PLAN-0001"
parent_ids:
- "SPEC-0243"
created: "2026-10-14"
---

# OpenBao Maintenance Window Readiness Plan

## Overview

Fix the window text first so every gap is visible and blocked, then build
and review each missing tool or mount in its own pull request.

The 2026-10-22 v28 work compares the existing Task's later observations and
implements local residuals only. The documentation writer owns RUN-0085 and
this Spec/Plan/Task; code and QA workers own disjoint paths recorded in the
Task. Remote PR/CI and operational work retain their separate boundaries.

## Scope

W1 repairs RUN-0085 prerequisites and stops; W2–W5 prepare and rehearse
the restore start, renderer apply, W3a producers and W3b transfer receipts.
W6 covers accepted-pin CA mounts, pre-window rollback overrides, hourly
logrotate and W4 recovery choice; actual window execution, SEC01 image
acceptance and P06 remain separate.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 7 | RUN-0085 window text: prerequisites, W1c, W4 stops and rollback gate, W5 Agent start and Prometheus recreate, stale lines | None | TSK-0001 | Task evidence |
| W2 | 2, 7 | Restore tool server start and a native rehearsal on both images | W1 | TSK-0001 | Task evidence |
| W3 | 3, 7 | W1c apply command and receipt | W1 | TSK-0001 | Task evidence |
| W4 | 4, 7 | W3a input producers | W2, W3 | TSK-0001 | Task evidence |
| W5 | 5, 7 | W3b R2 transfer tool and receipt | W1 | TSK-0001 | Task evidence |
| W6 | 6, 7 | CA mounts at accepted Compose pins, pre-window-image rollback overrides, hourly logrotate timer drop-in, W4 rollback decision | W1 | TSK-0001 | Task evidence |

## Verification Plan

Document checks for W1; unit tests, synthetic native rehearsals and static
Compose validation for W2 to W6; independent `iac-reviewer` and
`security-auditor` reviews of each unit.

Minimum v28 checks cover W3/Finish Bash syntax and synthetic metadata gates,
snapshot identity negatives, synthetic TLS delay/failure, and the existing
native harness's default skip. B2 opt-in native execution and A1 real
ESO/Kubernetes-auth reproduction are separate unexecuted steps. No new remote
environment or HOME asset is created automatically. Changed pins require a new
approved commit/manifest, installation match and independent review before a
later window. A3/B4/D1 recovery, cleanup decisions and missing inputs stay in
this Task rather than a parallel ledger.

## Risks and Recovery

### Risks and Rollback

- **Scope.** Each tool is security-sensitive; one pull request per unit keeps
  reviews bounded.
- **Rollback.** Each unit reverts on its own; pre-window image overrides are
  rollback inputs, while promotion uses the service's accepted Compose pin.
  Reverting source does not authorize a Raft downgrade or restore. The window
  stays blocked until every unit lands.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-openbao-window-readiness.md)
