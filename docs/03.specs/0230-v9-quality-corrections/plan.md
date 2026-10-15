---
title: "Prompt v9 Quality Corrections Plan"
version: "1.0.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0230-PLAN-0001"
parent_ids:
- "SPEC-0230"
created: "2026-10-13"
---

# Prompt v9 Quality Corrections Plan

## Overview

Change the stale workflow, repair the two failing checks, then validate.

## Scope

W1 makes the stale workflow label without closing threads; W2 aligns
registered selectors and the three unchanged-image census digests; W4 aligns
the opt-in PostToolUse normalizer with its registered whitespace owners.
W3 verifies the source corrections without reopening historical threads or
changing repository settings, image versions or the recorded census.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Mark-only stale inputs, notice, names and contract entry | None | TSK-0001 | Task evidence |
| W2 | 2 | Selector list and ledger input digests | None | TSK-0001 | Task evidence |
| W3 | 3 | Changed gate and candidate quality | W1, W2 | TSK-0001 | Task evidence |
| W4 | 4 | PostToolUse normalizer agreement with its registered owner | None | TSK-0001 | Task evidence |

## Verification Plan

The pinned `action.yml` description of `days-before-close`, a diff of the
image and build lines behind the refreshed digests, the workflow contract and
update-gate tests, the changed gate and the remote candidate.

## Risks and Recovery

### Risks and Rollback

- Stale threads now stay open until the owner closes them.
- A later image change to the three Compose files still needs its own ledger
  review; this refresh does not cover one.
- Rollback: revert the commits.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-v9-quality-corrections.md)
