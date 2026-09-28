---
title: "Document Governance Dead Code Removal Plan"
version: "0.4.0"
type: "sdlc/plan"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0186-PLAN-0001"
parent_ids:
- "SPEC-0186"
created: "2026-09-28"
---

# Document Governance Dead Code Removal Plan

## Objective

Remove the three validator code paths that [SPEC-0186](spec.md) names, each
only after proving it is unreachable, without changing validator output on
the current tree.

## Dependencies

- SPEC-0184 is integrated into the local `main`.
- The branch starts from that `main`.

## Execution Sequence

1. W0: Record the pre-change changed-profile summaries in the Task
   (criterion 4).
2. W1: Remove `load_artifact_contract` and any test that only exercises it
   (criteria 1, 5).
3. W2: Remove the Stage 98 README base read in `archive.py` and its fallback
   test (criteria 2, 5).
4. W3: Prove Foundation-wave reachability; if nothing reaches it, remove the
   wave, its Stage 04 path constants, and the `docs/04.execution/**` consumer
   glob (criteria 3, 5).
5. W4: Rerun the gate members and both unit suites, compare summaries, and
   record the evidence (criteria 4, 5).

Each of W1 through W3 is one commit.

## Risk and Rollback

Each removal is one commit, so reverting one commit restores one path. A
candidate that turns out to be reachable is kept and recorded, not forced.

## Verification

- `git grep` for each removed symbol returns nothing.
- `python3 -m unittest discover -s tests/lib -t .` and
  `python3 -m unittest discover -s tests/validation -t .` pass.
- Changed-profile members, except `check-conftest-policy.sh`, return 0, with
  summaries equal to W0.

## Rulings

None yet.
