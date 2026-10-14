---
title: "OpenBao Maintenance Window Readiness Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
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

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 7 | RUN-0085 window text: prerequisites, W1c, W4 stops and rollback gate, W5 Agent start and Prometheus recreate, stale lines | None | TSK-0001 | Task evidence |
| W2 | 2, 7 | Restore tool server start and a native rehearsal on both images | W1 | TSK-0001 | Task evidence |
| W3 | 3, 7 | W1c apply command and receipt | W1 | TSK-0001 | Task evidence |
| W4 | 4, 7 | W3a input producers | W2, W3 | TSK-0001 | Task evidence |
| W5 | 5, 7 | W3b R2 transfer tool and receipt | W1 | TSK-0001 | Task evidence |
| W6 | 6, 7 | CA mount overrides, hourly logrotate unit, W4 rollback decision | W1 | TSK-0001 | Task evidence |

## Verification Plan

Document checks for W1; unit tests, synthetic native rehearsals and static
Compose validation for W2 to W6; independent `iac-reviewer` and
`security-auditor` reviews of each unit.

## Risks and Rollback

- **Scope.** Each tool is security-sensitive; one pull request per unit keeps
  reviews bounded.
- **Rollback.** Each unit reverts on its own; the window stays blocked until
  every unit lands.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-openbao-window-readiness.md)
