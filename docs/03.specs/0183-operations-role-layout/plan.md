---
title: "Operations Role Layout Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0183-PLAN-0001"
parent_ids:
- "SPEC-0183"
created: "2026-09-26"
---

# Operations Role Layout Plan

## Objective

Deliver the [Spec](spec.md) acceptance contract as reviewable local commits on
branch `refactor/operations-role-layout`, without runtime or remote action.

## Dependencies

- Baseline `0deb430ea` with a recorded full-gate result.
- [ADR-0043](../../02.architecture/decisions/0043-operations-role-layout.md)
  as the structural decision.
- The move map produced from each document's `artifact_id` before any write.

## Execution Sequence

1. W1: Record the baseline, the inventory, and the per-document disposition
   ledger in the Task. Criteria: 2, 5.
2. W2: Add the Spec package, ADR-0043, and the Stage 03 and ADR index rows.
   Criteria: none directly; authority for W3 onward.
3. W3: Write regression tests for the role-first contract and observe them
   fail on the catalog tree. Criteria: 4.
4. W4: In one commit, change the Registry, the operations validator, the
   archive tombstone identity, the affected tests, move the 225 documents,
   replace the catalog and domain READMEs with three role indexes, and rewrite
   every active consumer. Criteria: 1, 2, 3, 4, 5.
5. W5: Correct the confirmed stale statements in `scripts/README.md` and the
   incidents README. Criterion: 6.
6. W6: Apply confirmed role-boundary and implementation-drift corrections
   found by the read-only audits, each bounded to documented evidence.
   Criterion: 5.
7. W7: Add MIG-0005 and bump the `migration` identity space. Criterion: 7.
8. W8: Run the changed and full gate profiles, the named focused checks, and
   independent review; record results and the commit ledger. Criterion: 8.

## Risk and Rollback

The W4 commit is large but mechanical; reverting it restores the catalog tree
and its validator in one step. W5 to W7 are independent and revert alone. No
runtime state changes, so no runtime rollback exists or is needed.

## Verification

- `python3 scripts/validation/check-operations-catalog.py`
- `python3 scripts/validation/check-document-links.py --mode all`
- `python3 scripts/validation/check-script-manifest.py` and
  `--check-generated`
- `PYTHONPATH=. python3 tests/validation/test_script_manifest.py`
- Focused unit tests for the Registry, taxonomy, links, archive, heading, and
  operations validator.
- `python3 scripts/validation/run-ci-gate.py --profile changed` and
  `--profile full`
- `git diff --check` and `git diff --cached --check` before each commit.

## Rulings

- The gate identifier `leaf.operations-catalog`, the entrypoint
  `check-operations-catalog.py`, and the module name stay; they name the
  operations document gate, and renaming them would change the workflow
  contract without behavior benefit.
- Stage 98 frozen bodies, sealed Tombstones, and Migrations are not rewritten.
- Documents are moved with `git mv` so rename detection keeps their history.
