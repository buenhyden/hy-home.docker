---
title: "Prompt v9 Residual Corrections Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0232-PLAN-0001"
parent_ids:
- "SPEC-0232"
created: "2026-10-13"
---

# Prompt v9 Residual Corrections Plan

## Overview

Four independent source edits, a governance review, then the gates.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Validate-only PostToolUse hook and its text | None | TSK-0001 | Task evidence |
| W2 | 2 | Remove the n8n 2.42.6 candidate rehearsal | None | TSK-0001 | Task evidence |
| W3 | 3 | Registry assertion for frozen payloads | None | TSK-0001 | Task evidence |
| W4 | 4 | Three-step `AGENTS.md` | None | TSK-0001 | Task evidence |
| W5 | 5 | Rules review, changed gate and candidate quality | W1, W2, W3, W4 | TSK-0001 | Task evidence |
| W6 | 6 | Tombstone identity for classified operations paths | None | TSK-0001 | Task evidence |
| W7 | 7 | PostToolUse failure as model context | W1 | TSK-0001 | Task evidence |

## Verification Plan

New and changed tests with a RED state on `main`, the update-gate and SEC01
routing tests for the removed rehearsal, an independent `rules-engineer`
review of the policy text, the changed gate and the remote candidate.

## Risks and Rollback

- Trailing whitespace an agent leaves now fails the hook instead of being
  fixed; the agent fixes it or runs `--write`.
- Rebuilding an n8n candidate needs a new rehearsal written for that version.
- Rollback: revert the commits.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-v9-residual-corrections.md)
