---
title: "W10 Review Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-19"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0091"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-19"
---

# W10 Review Task

## Scope

### Objective and Parent

Own criterion 147 and work unit W163 under the [Spec](../spec.md) and
[Plan](../plan.md). Bring review to the 4.2.0 W10-REVIEW design with D05:
review effort proportional to risk, severity that follows reachability, and
review cost that is recorded rather than guessed.

### Inputs and Authority

The direct 2026-11-19 request runs W10-REVIEW from the git-ignored 4.2.0
package. On 2026-11-19 the owner chose to add a medium review class and to
run fresh-context reviews of PRs 1105 and 1108 together and of PR 1109,
all merged without one. W01-CONTRACT supplies the existing review risk,
review scope and evidence-only rules, and RUNTIME-CLOSE the reviewer
permission evidence.

## Execution Log

### Work Performed

#### Gap analysis

Kept as they are: the review packet in the diff review prompt, review of
only the affected slice after a correction, no new review for an
evidence-only commit, the specialist review limited to an actual boundary,
and the reviewer permission evidence in TSK-0078 and TSK-0079 (the Claude
reviewer has no write or shell tool and a sensitive path read was refused;
the Codex desktop reviewer subagent inherits a writable sandbox, still
open there). Three gaps were found. Review had two classes, so an ordinary
code change fell between an author check and an independent review; no
rule kept a reachable defect's severity when only a specific input
triggers it; and nothing recorded review waits or rounds. The author's own
PRs 1105, 1108 and 1109 changed operations code and merged with an author
check only, which the unclear-class rule should have raised; the automated
security review of PR 1109 found a real defect the author's checks missed.

#### W163 design

Workflows 1.6.0 and GitHub governance 1.12.0 (R123) add the medium class:
a change that changes executable code or tests and meets no high-risk
condition gets one primary review by a read-only reviewer in a fresh
context who did not write it, against the diff review checklist; an
unclear class takes the higher one; a review run after merge is recorded
as such. `code-review-dimensions` 1.4.0 keeps a reachable defect's
severity when only a specific input triggers it and labels a suspicion
without a reproducible input a suggestion. Each review's evidence row
records dispatch and return times and rounds, and a number not observed is
reported as unmeasured.

#### Late reviews

Two read-only `code-reviewer` subagents, each in its own fresh context,
were dispatched at 2026-11-18T21:07:17Z with a packet naming the code,
tests, criteria, rules, runbook section, Task and recorded check results.
Neither had a shell; both read files only. The PRs 1105 and 1108 review
returned after 135 s with 13 tool calls and blocked criterion 145: a NaN
minute value is stored as NULL and then crashes every `score` (high);
`INSERT OR REPLACE` bypasses the append-only triggers (medium); and lows on
pooled calibration across types, future end times and active minutes over
the elapsed time, uncaught errors, and missing tests. The PR 1109 review
returned after 246 s with 13 tool calls and blocked criterion 146: a
rename into an owned path passes the ownership check, a unit that changes
nothing breaks integration and, with a dependent, leaks its leases and
worktree, and a worker's background children outlive its released lease
(all high); the final patch is writable by workers, integration ignores
cancel and has no timeout, and a worker that removes its worktree's `.git`
makes the dispatcher stage files in the main repository (medium); and lows
on a new run clearing a pending cancel, owning `.`, `cleanup` errors and
non-UTF-8 names. Every high finding came with a concrete input; none was
reported as needing only a suspicion. Queue wait and context loading inside
each reviewer were not observed.

#### Fixes and re-reviews

Every finding was reproduced with a failing test before its fix. The
forecast fix (`759509c3f`) refuses non-finite values, an end in the future
and active minutes over the elapsed time, adds `BEFORE INSERT` triggers so
`REPLACE` aborts, labels calibration `empirical` only for one task type,
returns exit 2 on store errors, and states in R152 and RUN-0021 that a
dropped trigger or replaced store file is not prevented. The dispatcher fix
(`27d140727`) diffs with `--no-renames`, skips empty patches, releases
leases and the worktree on a setup error, kills a finished worker's group
before reading its result, writes the integrated patch afresh with its
SHA-256, runs integration checks with a timeout and cancel, runs Git
through the recorded worktree directory, honours a cancel newer than the
run start, refuses owning `.`, and releases a dead run's leases in
`cleanup`.

Round 2, the affected slice only, was sent to the same reviewers at
2026-11-18T21:23:05Z. The forecast reviewer approved after 60 s with 6 tool
calls, noting a sub-second end-time edge and a missing `empirical` test,
both fixed in `3339e367e`. The dispatcher reviewer resolved all ten round-1
findings after 120 s with 6 tool calls but blocked on a defect the fix
introduced: a unit id such as an absolute path let the new `rmtree`
fallback delete any directory (high), plus a command that cannot start
leaking its worktree and leases (medium) and a group killed after its
leader was reaped (low). `a70090601` refuses ids that are not plain tokens,
limits `rmtree` to a run's own worktree folder, guards the worker start,
and detects exits with `waitid(WNOWAIT)` so the group is killed first.
Round 3, dispatched at 2026-11-18T21:26:42Z, approved after 43 s with 6
tool calls with one follow-up, command entries Popen cannot start, fixed in
`0f82a56cd` by plan validation and a guarded integration start; that last
change closed with an author check, not another round. A real two-worker
run on the fixed dispatcher passed in 39.1 s with integration passed and
no worktree left.

#### Review cost and yield

Before this Task the three PRs had an author check only, which found none
of these defects; the automated security review of PR 1109 found one.
The fresh-context reviews found 21 defects across three rounds (dispatcher
14: 4 high, 4 medium, 6 low; forecast 7: 1 high, 1 medium, 5 low), and
each one the author tested reproduced, so no false block was observed. Two
findings were introduced by the author's own fixes and caught by the next
round. Review time was 135 s and 60 s for the forecast and 246 s, 120 s and
43 s for the dispatcher, 604 s in total over five rounds; the reported
subagent token totals were 79 thousand and 111 thousand. Queue wait,
context loading and the author's fix time were not observed separately.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0091 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0091 | ready | in-progress | #w163-design |

### Blockers and Decisions

None. Advisory and unfixed: the forecast API's `forecasted_at` can still
backdate a forecast (the CLI does not expose it), and integration check
output is discarded rather than logged.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Policy checks | 147 | W163 | Governance contract and provider renderer | Workflows 1.6.0, GitHub governance 1.12.0, skill 1.4.0 | PASS | Contract 0 failures; renderer drift 0 | required | - |
| Forecast review | 147 | W163 | Fresh-context `code-reviewer` review | PRs 1105 and 1108 packet, main `24b7e60b9` | FAIL | Block: 1 high, 1 medium, 4 low; 135 s, 1 round | required | - |
| Dispatcher review | 147 | W163 | Fresh-context `code-reviewer` review | PR 1109 packet, main `24b7e60b9` | FAIL | Block: 3 high, 3 medium, 4 low; 246 s, 1 round | required | - |
| Forecast fix RED | 147 | W163 | `test_task_forecast` | New finding tests on `0a1b8ae38` | FAIL | 7 failures, 1 error | required | - |
| Forecast fix GREEN | 147 | W163 | `test_task_forecast` | `3339e367e` | PASS | 12 tests | required | Forecast fix RED |
| Forecast re-review | 147 | W163 | Fresh-context `code-reviewer` review | Fix slice, round 2 | PASS | Approve; all six findings resolved; 60 s | required | Forecast review |
| Dispatcher fix RED | 147 | W163 | `test_work_dispatch` | New finding tests on `0a1b8ae38` and `27d140727` | FAIL | 6 failures, 4 errors; then 2 failures, 2 errors for round 2; then 3 errors for round 3 | required | - |
| Dispatcher fix GREEN | 147 | W163 | `test_work_dispatch` | `0f82a56cd` | PASS | 26 tests | required | Dispatcher fix RED |
| Dispatcher re-review | 147 | W163 | Fresh-context `code-reviewer` review | Fix slices, rounds 2 and 3 | PASS | Round 2 block on 1 new high, round 3 approve with one follow-up, fixed; 120 s and 43 s | required | Dispatcher review |
| Real dispatch after fixes | 147 | W163 | `work_dispatch.py run` | Three-unit plan, two workers, `0f82a56cd` | PASS | 39.1 s; integration passed with SHA-256; one worktree left | required | - |

### Resolution Links

Forecast fix GREEN resolves Forecast fix RED, Dispatcher fix GREEN
resolves Dispatcher fix RED, and each re-review resolves its first review.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 147 | pending | Policy checks, Forecast re-review, Dispatcher re-review, Forecast fix GREEN, Dispatcher fix GREEN, Real dispatch after fixes | Awaits the owner's decision | @buenhyden |

### Remaining Conditions

None beyond the owner's decision; the advisory items above are recorded.

## Handoff

### Promotion Receipt

Workflows, GitHub governance and `code-review-dimensions` hold the W163
rules.

### Next Owner

The owner decides criterion 147, and criteria 145 and 146 with these
reviews in view.
