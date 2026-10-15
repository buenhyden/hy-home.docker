---
title: "Task Lifecycle Generation 6 Plan"
version: "1.0.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0231-PLAN-0001"
parent_ids:
- "SPEC-0231"
created: "2026-10-13"
---

# Task Lifecycle Generation 6 Plan

## Overview

Change the contract first, then the reader behind failing fixtures, then the
archive consumers, then migrate the active corpus and the text that states
the rules. Each unit is one logical commit on one branch with one writer.

## Scope

W1–W3 separate parent authority from Task execution, implement generation 6
Evidence/acceptance rules and share one archive-readiness predicate. W4–W6
migrate active records with source proof, align REQ-0026/AD-0030/ADR-0048 and
governance, then validate integration while preserving generation 4 terminal
bodies and frozen archive meaning.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Registry generation 6 lifecycles, Evidence, Criterion Acceptance and Execution Items contracts; schemas; Task template | None | TSK-0001 | Task evidence |
| W2 | 1, 2 | Generation 6 reader: parent authority, single and multi-item Tasks, Evidence `Resolves`, criterion acceptance, completion | W1 | TSK-0001 | Task evidence |
| W3 | 3 | Shared archive readiness predicate in Stage 03 occupancy and preservation | W2 | TSK-0001 | Task evidence |
| W4 | 4 | Generation migration proof and normalizations; mechanical migration of active Stage 03 documents | W2, W3 | TSK-0001 | Task evidence |
| W5 | 5 | Governance, template and README text; REQ-0026, AD-0030 and ADR-0048; repeated `### Usage` headings | W4 | TSK-0001 | Task evidence |
| W6 | 6 | Changed gate, candidate quality and integration | W1, W2, W3, W4, W5 | TSK-0001 | Task evidence |

## Verification Plan

RED then GREEN fixtures for every contract rule in the document governance
library tests; a before and after reader run over the active corpus; a byte
comparison of generation 4 historical Tasks and archive bodies; the metadata,
corpus lifecycle and archive recovery checks; the changed gate and the remote
candidate.

## Risks and Recovery

### Risks and Rollback

- Other writers keep active Tasks open on parallel branches; a branch that
  still writes generation 5 Evidence after this merges fails the reader and
  needs the same mechanical rewrite. The migration helper is a one-off and is
  not kept as a tracked tool.
- The generation migration proof binds Git revisions and needs exactly one
  first-parent merge that brings generation 6 onto a generation 5 `main`. The
  pull request is merged with a merge commit, never squashed or rebased, and
  local checks run on a synthetic merge of the branch into `main`.
- Rollback: revert the merge commit; generation 5 documents are restored with
  it.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-task-lifecycle-generation-6.md)
