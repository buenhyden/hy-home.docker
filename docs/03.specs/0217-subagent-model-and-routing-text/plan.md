---
title: "Subagent Model and Routing Text Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0217-PLAN-0001"
parent_ids:
- "SPEC-0217"
created: "2026-10-08"
---

# Subagent Model and Routing Text Plan

## Overview

Change the description renderer with its test, then move the Claude model
selections, regenerating the projections after each so every commit keeps
renderer parity.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Render descriptions from Overview and Use When; add the test; regenerate | None | TSK-0001 | Task evidence |
| W2 | 2, 3 | Move Claude profiles to Opus 5.5 and Sonnet 5.5; regenerate | W1 | TSK-0001 | Task evidence |

## Verification Plan

Run the description test before and after the renderer change, then
`provider_surface_renderer.py --check`,
`check-agent-governance-contract.py`, the entrypoint test module and a search
for the earlier model IDs. Remote PR `candidate-quality` owns candidate
acceptance.

## Risks and Rollback

Descriptions with routing text make automatic delegation more likely than the
earlier boilerplate did. Sonnet 5.5 recalibrates effort levels, so the same
`high` or `low` value can behave differently; the effort values stay as they
are until an effort sweep says otherwise. Revert the commits and regenerate to
restore the earlier models and descriptions.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-subagent-model-and-routing-text.md)
