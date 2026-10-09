---
title: "npm Risk Acceptance Extension Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0222-PLAN-0001"
parent_ids:
- "SPEC-0222"
created: "2026-10-09"
---

# npm Risk Acceptance Extension Plan

## Overview

Confirm that no patch exists, move the expiry from code to an approved window
in the contract data, restate the quality standard as a rule, and validate
before the current acceptance expires.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Contract window, record and tests | None | TSK-0001 | Task evidence |
| W2 | 2 | Quality standard extension rule | W1 | TSK-0001 | Task evidence |
| W3 | 3 | Changed gate, staged style check, candidate quality, merge | W1, W2 | TSK-0001 | Task evidence |

## Verification Plan

Contract tests for the window and pinned fields; adapter tests for expiry and
patch availability; the agent-governance contract; the changed gate, the
staged style check and the remote candidate.

## Risks and Rollback

- Merging after 2026-10-10T15:00:00Z leaves the audit leaf failing until it
  merges; the adapter keeps failing closed rather than passing.
- A published patch makes the audit fail even inside the window, which is the
  signal to upgrade.
- Rollback: revert the commits; the old record expires and the leaf fails
  closed.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-npm-risk-acceptance-extension.md)
