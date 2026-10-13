---
title: "Local Gate Governance Timeout Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0235-TSK-0001"
parent_ids:
- "SPEC-0235-PLAN-0001"
created: "2026-10-13"
---

# Local Gate Governance Timeout Task

## Objective

Let the local changed gate finish on the owner's host by raising one local
only node timeout, as SPEC-0235 states.

## Inputs and Authorization

- **Request:** on 2026-10-13 the owner chose "Raise the timeout to 45 min" in
  AskUserQuestion, then asked to review, correct and extend it before
  proceeding.
- **Baseline:** `main` `338c607d8`.
- **Evidence of the problem:** SPEC-0233 W6 records the local changed gate on
  `5b95ed942` exiting 124 after 1143 s at this node; SPEC-0231 W6 and SPEC-0232
  W5 record earlier timeouts.

## Work Log

### W1 Measured Runtime

The node's 19 argv modules are run with `python3 -m unittest` in a detached
scratch worktree of `338c607d8`. The result is recorded below when the run
ends.

### W2 Timeout Change

`leaf.document-governance-library-regressions` in
`.github/workflow-contract.yml` now has `timeout_minutes: 45`; nothing else
changed. The node is in `public_gate.local_only_gate_ids`, so the hosted
`candidate-quality` job, which has its own 30-minute job timeout, never runs
it. The CI gate contract tests (28), the workflow contract and adapter tests
(85) and `check-github-workflow-contract.py` (5 workflows, 7 jobs, 8 actions)
pass.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Contract | 1 | W2 | CI gate contract tests (28); workflow contract and adapter tests (85); workflow contract check | Branch on `338c607d8` | PASS | W2 Timeout Change | - |
| Runtime | 2 | W1 | Node module batch on this host | `338c607d8` | NOT_RUN | W1 Measured Runtime | - |
| Local gate | 3 | W3 | `run-ci-gate.py --profile changed` | Branch | NOT_RUN | Work Log | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |

## Review and Completion

No criterion is accepted until the owner accepts it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
