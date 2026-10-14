---
title: "Local Gate Governance Timeout Task"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
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
- **Evidence of the problem:** SPEC-0233 W6, as recorded in PR #448, shows
  the local changed gate on `5b95ed942` exiting 124 after 1143 s at this node.
  SPEC-0231 W6 and SPEC-0232 W5 stopped at outer 3000 s and 3600 s limits
  around the gate; the runner returns 124 for both kinds of stop, so those two
  runs do not prove the node's limit.
- **Review:** an independent `ci-cd-engineer` review of `682840106` approved
  with notes: the node is local only, nothing pins the 15-minute value, the
  runner has no total budget, and the contract accepts node timeouts of 1 to
  60 minutes.

## Work Log

### W1 Measured Runtime

The node's 19 argv modules ran with `python3 -m unittest` in a detached
scratch worktree of `338c607d8` on 2026-10-13: 763 tests in 1333 s, 1336 s
wall time, about 22.3 minutes. So 15 minutes cannot hold the batch on this
host, and 45 minutes leaves about twice the measured time.

One test failed: `test_registry_high_water_is_not_below_repository_history`
reads every local ref, and the unmerged local branches for SPEC-0234 and this
SPEC-0235 issue numbers above `main`'s Registry high water of 233. That test
passes on the SPEC-0234 branch, whose Registry records 234; it is rerun on
`main` once these branches merge. The failure does not bear on the timing.

### W2 Timeout Change

`leaf.document-governance-library-regressions` in
`.github/workflow-contract.yml` now has `timeout_minutes: 45`; nothing else
changed. The node is in `public_gate.local_only_gate_ids`, so the hosted
`candidate-quality` job, which has its own 30-minute job timeout, never runs
it. The CI gate contract tests (28), the workflow contract and adapter tests
(85) and `check-github-workflow-contract.py` (5 workflows, 7 jobs, 8 actions)
pass.

### W3 Reachability of Class Selections

On 2026-10-14 every local `run-ci-gate.py --profile changed` stopped before
the governance node: `tests.lib.test_surface_ownership` failed
`test_every_test_module_is_reachable_from_the_full_profile`, because commit
`c80915370` (P04, 2026-10-13) registers
`tests.validation.test_opsflow_database_rehearsal.OpsflowDatabaseRehearsalBoundaryTests`,
a class, in the workflow contract, and the test compared module names only.
The gate stops at its first failing node, so W3 could not reach the
governance node on any branch, and the local gate moved to W4. The owner chose on 2026-10-14
(AskUserQuestion) to make the test count a class or method selection as
reaching its module, keeping P04's single-class selection. Only
`tests/lib/test_surface_ownership.py` changes; the duplicate check is kept.

### Direct Push to Main

At 2026-10-13T11:16:06Z, `refs/heads/main` on GitHub moved from `338c607d8`
to `4072f8af8`, this package's first commit, by a direct push from this
machine. It went through no pull request and no `candidate-quality` run.
GitHub's activity log shows that push; this session's own pushes went only to
`claude/gate-timeout` (11:04:05Z and 11:18:25Z), and the forked worker that was
running then issued no push. Which local session or tool pushed it is not
known. The owner chose on 2026-10-13, through AskUserQuestion, to keep the
commit on `main` and record it here. The later commits on
`claude/gate-timeout` go through a pull request. The push also broke PR #448's
first run on the new base (`ci-gate-adapter-pull-request-range`: the checkout
is not the authenticated pull request merge); #448 was rebased onto
`4072f8af8`.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Contract | 1 | W2 | CI gate contract tests (28); workflow contract and adapter tests (85); workflow contract check | Branch on `338c607d8` | PASS | W2 Timeout Change | - |
| Runtime | 2 | W1 | Node module batch on this host: 763 tests, 1336 s | `338c607d8` | PASS | W1 Measured Runtime | - |
| CI review | 1 | W2 | Independent `ci-cd-engineer` review: approve with notes, notes applied | `682840106` | PASS | Inputs and Authorization | - |
| Local gate | 3 | W4 | `run-ci-gate.py --profile changed` | Branch | NOT_RUN | Work Log | - |
| Reachability | 4 | W3 | `tests.lib.test_surface_ownership` RED on `1e7e2ba84` (1 failure), GREEN with the change (8 tests) | Branch on `1e7e2ba84` | PASS | W3 Reachability of Class Selections | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |

## Review and Completion

No criterion is accepted until the owner accepts it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
