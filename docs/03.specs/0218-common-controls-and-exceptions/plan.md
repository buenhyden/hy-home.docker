---
title: "Common Controls and Exceptions Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0218-PLAN-0001"
parent_ids:
- "SPEC-0218"
created: "2026-10-09"
---

# Common Controls and Exceptions Plan

## Overview

Convert the schema and validator first, then fix leaves one control at a
time, each proven by a real run, then record budgets and the remaining
exceptions. Each unit is one commit.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Schema v2, effective-control validator, quick-win retirement | None | TSK-0001 | Task evidence |
| W2 | 3 | Healthchecks the images can run | W1 | TSK-0001 | Task evidence |
| W3 | 3 | Secrets group only where a secret is read | W1 | TSK-0001 | Task evidence |
| W4 | 4 | Conftest URL-credential rule and LAB corpus | None | TSK-0001 | Task evidence |
| W5 | 2, 3 | DB templates drop all capabilities; proven leaf sets; data-group exceptions | W3 | TSK-0001 | Task evidence |
| W6 | 3 | GPU template security base and GPU exceptions | W1 | TSK-0001 | Task evidence |
| W7 | 3 | PID limits as initial budgets | W5 | TSK-0001 | Task evidence |
| W8 | 5 | Documents, ledger and changed gate | W1, W2, W3, W4, W5, W6, W7 | TSK-0001 | Task evidence |

## Verification Plan

Unit tests for the validator, the Conftest verify run, real LAB runs through
`lab.py` with synthetic inputs, exact-image runs for root services that are
not running, read-only checks of running HOME containers, and the
changed-profile local gate in a clean worktree.

## Risks and Rollback

The template changes reach HOME services only when they are recreated. The
group removal could break a service that reads or writes through group 1000;
mounts of the running services were checked, and the data-directory writers
keep the group. Rollback is a revert of the merge; recreated services then
return to their previous definitions on the next recreation.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-common-controls-and-exceptions.md)
