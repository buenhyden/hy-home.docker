---
title: Formatting Authority Convergence Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0166-PLAN-0001
parent_ids: [SPEC-0166]
created: 2026-09-03
updated: 2026-09-03
---

# Formatting Authority Convergence Plan

## Objective

Move formatting authority into the repository, in an order where each commit is
green on its own.

## Dependencies

- The retired-route scan reads physical lines, so it must stop depending on
  line breaks before any formatter runs. Applying `ruff format` first was tried
  as a measurement and failed two tests with 17 findings.

## Execution Sequence

1. Replace the scan's typographic exemption with a stated marker. Verify: an
   unmarked reference still reports; a marker on the previous line does not
   exempt the line below.
2. Pin Python formatting, reformat once, wire `ruff-format` into pre-commit, and
   remove the Prettier configuration. Verify: `ruff format --check` reports 106
   of 106 formatted; `prettier --check` matches nothing.
3. Record the ownership rules in the quality policy. Verify: the policy states
   rules and points at the executable sources rather than restating them.

## Risk and Rollback

Step 2 is the large one: 88 files, roughly 7,800 lines. It is reversible as a
single commit and is safe only because step 1 precedes it. Step 1 is the risky
one in kind rather than size, because a wrong exemption weakens a real check;
it is bounded by testing the marker in both directions.

## Verification

`python3 scripts/validation/run-ci-gate.py --profile full` after every step.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-formatting-authority.md)
