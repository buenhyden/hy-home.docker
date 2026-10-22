---
title: "Local Gate Governance Timeout Task"
version: "0.4.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0235-TSK-0001"
parent_ids:
- "SPEC-0235-PLAN-0001"
created: "2026-10-13"
---

# Local Gate Governance Timeout Task

## Overview

### Objective

Let the local changed gate finish on the owner's host by raising two local
only node timeouts and letting the reachability test accept a class
selection, as SPEC-0235 states.

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
The gate stops at its first failing node, so the local gate could not reach
the governance node on any branch; that local gate, formerly W3, became W4,
and W5 once the metadata node's timeout was added as W4. The owner chose on 2026-10-14
(AskUserQuestion) to make the test count a class or method selection as
reaching its module, keeping P04's single-class selection. Only
`tests/lib/test_surface_ownership.py` changes; the duplicate check is kept.
Limits: two class entries from one module count as a duplicate, and a
misspelt class name is caught only when unittest runs it.

An independent `ci-cd-engineer` review on 2026-10-14 found the code sound
(dropped, duplicated and misspelt modules still fail; 8 tests OK) and asked
for these document corrections, which are applied.

### W4 Metadata Node Timeout

With W3 in place, replays of the SPEC-0232 and SPEC-0233 merges through the
local changed gate on 2026-10-14 passed every earlier node, then exited 124
after about 1200 s inside `leaf.local-document-metadata-tests`, whose
timeout was 10 minutes. The node's six argv modules, run alone with
`python -m unittest` on `main` `f1af4b59e`, took 148 tests in 719 s (OK) with
a host load average of about 9 on 12 cores. So 10 minutes cannot hold the
batch on this host. The owner chose on 2026-10-14 (AskUserQuestion) to set
it to 30 minutes, about 2.5 times the measured time. The node is in
`public_gate.local_only_gate_ids`, so hosted `candidate-quality` never runs
it, and no test pins the old value.

An independent `ci-cd-engineer` review of `6ce05b26a` passed with notes: the
contract changes in one line, the contract accepts 1 to 60 minutes, the
runner uses `timeout_minutes * 60` per node, and the package pairs are
consistent. Its wrapping and evidence notes are applied. The changed gate on
this branch exited 0 in 557 s, but its path selection reached neither
timeout node, so it does not bear on criterion 3.

### W5 Local Gate and Candidate

Hosted `candidate-quality` passed on PR #469 head `5ad493be1` (run
`38510455397`), and #469 merged as `7f4c364f8`. On 2026-10-14 the SPEC-0233
change was replayed through the local changed gate in a scratch clone whose
base was its PR parent `958349408` with the three SPEC-0235 changes (both
timeouts and the reachability test) and nothing else, whose head added the
merge diff of PR #447, and from which every other ref was removed. The gate
reached both nodes and exited 0 after 2455 s: the metadata node ran 148
tests in 749 s, past the old 10-minute limit, and the governance node 763
tests in 1103 s, all OK. SPEC-0233 W6 records the same run.

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

### Lifecycle Reconciliation 2026-10-22

#### Parent Approval 2026-10-22

The owner's current request explicitly authorizes status and lifecycle
processing for implemented Specs, Plans and Tasks. After comparing the current
contract, implementation, existing acceptance and verification scope, today's
decision approves this package's Spec and Plan at their first stable version,
`1.0.0`. This records no parent approval or execution transition retroactively
at the time of the original implementation.

#### Reconciliation Readiness 2026-10-22

Readiness to start the current document reconciliation was reviewed under
the approved parents. Every criterion/Work Unit pair in the Plan has existing
PASS evidence, all acceptance decisions are accepted, and no FAIL is unresolved.
Historical Evidence and Criterion Acceptance are reused unchanged. This current
readiness review moves the Task from `draft` to `ready`.

#### Reconciliation Execution Review 2026-10-22

After the readiness review, current document closure work started and the
following scope and evidence were checked.

The two workflow contract nodes retain their 45- and 30-minute limits, and
the reachability implementation still resolves class/method selections to their
module. The existing W5 replay reached and passed both nodes. Initial NOT_RUN,
failure and direct-push records are preserved. Existing criterion 1–5 acceptance
and the dated hosted results are reused.

#### Reconciliation Completion Decision 2026-10-22

After the current readiness and execution reviews, today's decision completes
this Task's document closure for its approved contract. Existing PASS evidence,
accepted decisions, resolution relationships and unobserved results remain
unchanged. This decision supplies no new test or operational PASS. The canonical
reader derives archive readiness; no archive approval or Stage 98 move occurs.
Before merge, the coordinator combines and records structural and metadata
validation and independent review of this change.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0235 | draft | approved | #parent-approval-2026-10-22 |
| SPEC-0235-PLAN-0001 | draft | approved | #parent-approval-2026-10-22 |
| SPEC-0235-TSK-0001 | draft | ready | #reconciliation-readiness-2026-10-22 |
| SPEC-0235-TSK-0001 | ready | in-progress | #reconciliation-execution-review-2026-10-22 |
| SPEC-0235-TSK-0001 | in-progress | completed | #reconciliation-completion-decision-2026-10-22 |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Contract | 1 | W2 | CI gate contract tests (28); workflow contract and adapter tests (85); workflow contract check | Branch on `338c607d8` | PASS | W2 Timeout Change | - |
| Runtime | 2 | W1 | Node module batch on this host: 763 tests, 1336 s | `338c607d8` | PASS | W1 Measured Runtime | - |
| CI review | 1 | W2 | Independent `ci-cd-engineer` review: approve with notes, notes applied | `682840106` | PASS | Inputs and Authorization | - |
| Reachability | 4 | W3 | `tests.lib.test_surface_ownership` RED on `1e7e2ba84` (1 failure), GREEN with the change (8 tests) | `a35f1e0af` on `1e7e2ba84` | PASS | W3 Reachability of Class Selections | - |
| CI review W3 | 4 | W3 | Independent `ci-cd-engineer` review: code sound, document notes applied | `a35f1e0af` | PASS | W3 Reachability of Class Selections | - |
| Metadata runtime | 5 | W4 | Metadata node module batch on this host: 148 tests, 719 s | `f1af4b59e` | PASS | W4 Metadata Node Timeout | - |
| Contract W4 | 5 | W4 | CI gate contract and reachability tests (36); workflow contract check (5 workflows); changed metadata 0 violations | `6ce05b26a` | PASS | W4 Metadata Node Timeout | - |
| CI review W4 | 5 | W4 | Independent `ci-cd-engineer` review: pass with notes, notes applied | `6ce05b26a` | PASS | W4 Metadata Node Timeout | - |
| Local gate | 3 | W5 | `run-ci-gate.py --profile changed` | Branch | NOT_RUN | Work Log | - |
| Local gate replay | 3 | W5 | Local changed gate replay of the SPEC-0233 diff with the SPEC-0235 changes: both nodes reached, exit 0, 2455 s | `958349408` to `338c607d8` | PASS | W5 Local Gate and Candidate | - |
| Candidate | 3 | W5 | Hosted `candidate-quality` on PR #469, run `38510455397` | `5ad493be1` | PASS | W5 Local Gate and Candidate | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | accepted | Contract, CI review | Owner accepted 2026-10-14 |
| 2 | accepted | Runtime | Owner accepted 2026-10-14 |
| 3 | accepted | Local gate replay, Candidate | Owner rule 2026-10-14: replay counts, accept on pass |
| 4 | accepted | Reachability, CI review W3 | Owner accepted 2026-10-14 |
| 5 | accepted | Metadata runtime, Contract W4, CI review W4 | Owner accepted 2026-10-14 |

## Review and Completion

On 2026-10-14 the owner answered (AskUserQuestion) that a replay through the
local changed gate counts as evidence and that a gate criterion is accepted if
it passes. The W5 replay passed, so criterion 3 is accepted under that rule.
The same day the owner, answering the review question (AskUserQuestion),
accepted criteria 1, 2, 4 and 5.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
