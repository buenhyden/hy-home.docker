---
title: Template Contract Enforcement Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0165-PLAN-0001
parent_ids: [SPEC-0165]
created: 2026-09-03
updated: 2026-09-03
---

# Template Contract Enforcement Plan

## Objective

Make every template rule correct and reachable, then register the catalog.

## Dependencies

- SPEC-0164 gave `template-source` a lifecycle it can hold, so status is no
  longer a reason to keep the exclusion.

## Execution Sequence

1. Open the excluded route and record every finding by cause. Verify: 36
   findings across four distinct rules.
2. Correct the three misfiring rules and remove the exclusion. Verify: 34
   templates pass; each corrected rule still reports its own defect.
3. Register the catalog and enforce completeness. Verify: dropping one row
   reports the role by name.

## Risk and Rollback

Each step is one commit with a green full gate. The risk in step 2 is silencing
a rule that was right; it is bounded by measuring how templates actually use
each key before deciding, and by keeping a narrower check where the old one was
dropped.

## Verification

`python3 scripts/validation/run-ci-gate.py --profile full` after every step,
plus a negative test per corrected rule.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-template-contract.md)
