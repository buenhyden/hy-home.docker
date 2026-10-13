---
title: "Generation 6 Reader Corrections Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0233-PLAN-0001"
parent_ids:
- "SPEC-0233"
created: "2026-10-13"
---

# Generation 6 Reader Corrections Plan

## Overview

Fix the three reader gaps with failing fixtures first, complete the corpus
rows the first fix requires, add the missing rule fixtures, then correct the
text and run the gates.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Exactly one acceptance row; corpus rows | None | TSK-0001 | Task evidence |
| W2 | 2 | Item closure and mode equivalence | None | TSK-0001 | Task evidence |
| W3 | 3 | Completed-archive departure gate | None | TSK-0001 | Task evidence |
| W4 | 4 | Missing rule fixtures | None | TSK-0001 | Task evidence |
| W5 | 5 | SDLC, ADR and README text; rules review | W1, W2, W3 | TSK-0001 | Task evidence |
| W6 | 6 | Changed gate and candidate quality | W1, W2, W3, W4, W5 | TSK-0001 | Task evidence |

## Verification Plan

Each new behavior test fails against the `main` reader and passes after the
fix; the generation 6, Spec package, archive and metadata suites; the active
metadata and corpus lifecycle checks; the governance contract; an
independent `rules-engineer` review; the changed gate and the remote
candidate.

## Risks and Rollback

- A Task that lacked an acceptance row now fails until one is added; the
  active corpus had two such criteria, both in SPEC-0204.
- A completed item now waits for its criteria decisions.
- Rollback: revert the commits.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-generation-6-reader-corrections.md)
