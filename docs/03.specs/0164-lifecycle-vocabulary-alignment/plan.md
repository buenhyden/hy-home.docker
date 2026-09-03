---
title: Lifecycle Vocabulary Alignment Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0164-PLAN-0001
parent_ids: [SPEC-0164]
created: 2026-09-03
updated: 2026-09-03
---

# Lifecycle Vocabulary Alignment Plan

## Objective

Correct each lifecycle mismatch in its own commit, contract before documents
except where enforcement would leave the gate red.

## Dependencies

- SPEC-0162 made `invalid-status` and `invalid-transition` reachable, so a
  corrected vocabulary is now actually decided on rather than declared.
- SPEC-0163 required each README to satisfy its own profile's sections, which
  is the same shape of fix applied here to status.

## Execution Sequence

1. Correct the three bindings whose vocabulary the documents cannot hold, and
   make `invalid-template-status` reachable. Verify: registry loads, a template
   seeding a terminal status reports.
2. Remove `point-in-time`, proven identical to `living`. Verify: the identity
   is asserted in the change, so a future divergence stops the merge.
3. Give the 51 lifecycle-bound documents a state. Verify: 0 remain without one.
4. Require `status` wherever a lifecycle is declared. Verify: deleting a status
   reports `missing-required-key` for each bound profile.

Step 3 precedes step 4 because requiring first would fail 51 documents.

## Risk and Rollback

Each step is one commit with a green full gate. Step 2 is irreversible in
meaning if the machines were not identical, which is why the equality is
asserted in code rather than checked by eye. Step 3 touches the most files but
adds one key each, in a position the shared frontmatter order determines.

## Verification

`python3 scripts/validation/run-ci-gate.py --profile full` after every step,
plus a negative test per corrected contract.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-vocabulary-alignment.md)
