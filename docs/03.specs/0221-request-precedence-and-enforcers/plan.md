---
title: "Request Precedence and Enforcers Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0221-PLAN-0001"
parent_ids:
- "SPEC-0221"
created: "2026-10-09"
---

# Request Precedence and Enforcers Plan

## Overview

Inventory the rules that block a request, fix the local gate first because it
let failures through to CI, then change the precedence and approval text,
then add the contract check that holds it, then record the conflict table and
validate. Each unit is one commit.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 4 | Inventory of blocking rules and the conflict table | None | TSK-0001 | Task evidence |
| W2 | 2, 3 | Local changed paths since `origin/main`; candidate preflight leaf and tests | W1 | TSK-0001 | Task evidence |
| W3 | 4 | Bootstrap precedence and Approval Boundaries text | W1 | TSK-0001 | Task evidence |
| W4 | 1 | Agent-governance contract check and tests | W3 | TSK-0001 | Task evidence |
| W5 | 5 | Changed gate, staged style check, candidate quality, merge | W2, W4 | TSK-0001 | Task evidence |

## Verification Plan

Gate contract, plan and changed-path tests; entrypoint tests of the preflight
script with stub validators; the agent-governance contract on the repository
and on a mutated copy; the changed gate with the new preflight, the staged
style check, and the remote candidate.

## Risks and Rollback

- The preflight needs a fetched `origin/main`; without it it fails rather than
  passing, and the changed-path view falls back to the working tree.
- The auto-mode safety check refuses agent edits to role and governance
  rule text; the owner applies those edits from prepared copies.
- The memory-file exemption trusts `HOME`; it admits only one `.md` level
  in this repository's directory, so a wrong `HOME` widens nothing else.
- Rollback: revert the logical commits; no runtime or data state changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-request-precedence-and-enforcers.md)
