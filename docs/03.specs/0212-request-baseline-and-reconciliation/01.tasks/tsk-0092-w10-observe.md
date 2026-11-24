---
title: "W10 Observe Task"
version: "0.7.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-24"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0092"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-19"
---

# W10 Observe Task

## Scope

### Objective and Parent

Own criterion 148 and work unit W164 under the [Spec](../spec.md) and
[Plan](../plan.md). Bring observation to the 4.2.0 W10-OBSERVE design with
D12: what the scheduled and interactive runs leave behind is observed and
reaches an owner's fix.

### Inputs and Authority

The direct 2026-11-19 request runs W10-OBSERVE from the git-ignored 4.2.0
package. On 2026-11-19 the owner chose to run an approved local
forget-prune, then, when it removed nothing, to fix its grouping and prune
again, and chose a separate on-demand observe command over extending the
daily analysis. W08-CAPTURE supplies the capture store and W10-REVIEW the
review timing records.

## Execution Log

### Work Performed

#### Observation on 2026-11-19

The first scheduled session analysis ran at 03:00:22 KST and completed
with 128 events and 4 candidates, which observes W157. The daily
`hyhome-backup.service` ran at 03:52:57 KST and failed: the state Restic
repository used 8216 MiB against the 8 GiB `BACKUP_STATE_MAX_GIB` budget,
so Restic was skipped and nothing was copied offsite, while pgBackRest
completed. The journal shows the same failure on 2026-11-13, 14, 17, 18
and 19 and success on 15 and 16. Nothing surfaced it for a week.

#### Prune that removed nothing

On the owner's approval the runbook step 7 command ran once at
2026-11-18T21:45:12Z and exited 0 but removed no snapshot. Restic grouped
the state set by host and paths by default, and the backed-up path list
changed as volumes were added, so its 48 snapshots formed 10 groups of
1 to 13; within each group restic kept the last snapshot of each day, week
and month and, because the counts were not used up, the oldest one, so
nothing was removed. The host set's 34 snapshots, one path and one per day,
were all kept for the same reason. A read-only `stats --mode raw-data` before the run
gave 48 state snapshots and 7.165 GiB, and 34 host snapshots and 682 KiB.
The remote prune in `offsite.sh` already groups by host and tags.

#### Grouping fix

`infra/09-platform-ops/restic/backup.sh` now runs the local forget with
`--group-by host,tags`, the existing confirmation test asserts it, and
RUN-0021 step 7 explains why. The author's hand-built preview said 15 of 48
state and 1 of 34 host snapshots would go; the independent review showed
that it contradicted the real run, because restic also keeps the oldest
snapshot while a count is unused. Restic's own `forget --dry-run` with the
fixed grouping, run read-only through the `restic` service, removes 14 of
48 state snapshots (2026-09-22 12:12 to 2026-11-11 01:07) and no host
snapshot, a subset of the approved target.

#### Prune with the fixed grouping

After PR 1111 merged, the approved command ran once from 2026-11-18T22:23:51Z
to 22:24:18Z and exited 0. Restic removed 14 state snapshots, the same IDs
as its dry run, and no host snapshot; prune removed 352 MiB of blobs and
left 6.855 GiB with 344 MiB unused. Raw data fell from 7.165 to 6.519 GiB
over 34 state snapshots; the host set is unchanged. The budget check
measures the repository on disk, which the read-only commands do not show:
by the removed size it should fall from 8216 MiB to about 7860 MiB, under
the 8192 MiB budget with about 330 MiB of headroom, while the daily size
moved by up to 250 MiB over the last week. The next daily run at 03:42 KST
on 2026-11-20 is the observation of whether it is under budget.

#### Observe command

`scripts/operations/observe.py report` reads, without writing, the capture,
analysis and forecast stores, the dispatch run reports and the journal of
`hyhome-backup.service` and the user unit `hy-home-session-analysis.service`
over a time window, and lists each failure with its owner and next step.
Journal lines are counted, never copied, and the report states its own run
time and what it cannot measure (queue wait, context loading inside agents,
token and money cost). ENVIRONMENT-CONSTRAINTS-R161 and R162 and RUN-0021
state it. Run on this host for 2026-11-12 to 19, it reported in 0.131 s
373 events, 10 incomplete sessions under the known capture gaps, 2 complete
analysis runs, 1 forecast outcome, 4 dispatch runs and 5 failed and 2
finished backups, naming RUN-0021 as the backup owner; the same failures
had taken a week and a manual journal read to find.

#### Observe review and fixes

The fresh-context review of `9cfb6e1ff` returned after 229 s with 35 tool
calls and blocked. Its blocker was a test window fixed to 2026-11-18 UTC
while the forecast outcome and the run report took the test's own clock, so
the suite failed from 2026-11-19 UTC. It also found that analysis failures
never reach the runs table, only `analysis-status.json` (high); incomplete
sessions counted over the whole store, not the window (medium); a
restricted journal or a day without any run reading as clean (medium); and
lows on worker-written run report fields, the runbook step named, store
errors, a reversed window and test gaps. The tests now derive the window
from the current time and seed old records outside it; the report reads
the last analysis status, counts only sessions with events in the window
and merges reasons that differ only in counts, treats a journal hint about
hidden lines, an unreadable or symlinked store and a day with no run as
failures, echoes run report values only when they match a run id, a status
or a Task reference, names RUN-0021 step 4, and refuses a reversed window
and an outside-repository run with exit 2. A rerun of the 7-day report
gave the same 5 failed backups in 0.149 s with the capture gaps grouped by
cause. Round 2, sent at 2026-11-18T22:44:04Z, resolved all nine findings
after 102 s with 6 tool calls and approved with four low follow-ups: a
missed-run check that a randomly delayed backup could trip inside 24 hours,
a forecast reference echoed unchecked, a store reported twice, and the
status file and `degraded.log` outside the unavailable rule. The window for
a missed run is now 29 hours, forecast references are echoed only in Task
form, each unavailable store is reported once, a symlinked status file and
an unreadable `degraded.log` are failures, and the tests take the clock in
`setUp`; the follow-up closed with an author check.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0092 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0092 | ready | in-progress | #grouping-fix |

### Blockers and Decisions

Correlation of capture events to a Task, and the queue and context-loading
times, are not recorded by any store and stay unmeasured.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Scheduled analysis | 148 | W164 | `analysis-status.json` and the analysis runs table | 2026-11-19 03:00 KST run | PASS | Scheduled, complete, 128 events, 4 candidates | required | - |
| Daily backup | 148 | W164 | `journalctl -u hyhome-backup.service` | 2026-11-13 to 19 runs | FAIL | 5 of 7 failed over the 8 GiB state budget; Restic and offsite skipped | required | - |
| First prune | 148 | W164 | Runbook step 7 `forget-prune` | Approved command, both local repositories | FAIL | Exit 0, no snapshot removed: 10 path groups under the keep counts | required | - |
| Grouping RED | 148 | W164 | `test_destructive_restic_actions_need_explicit_confirmation` | New grouping assertion on `ae3c60af8` | FAIL | `--group-by host,tags` missing | required | - |
| Grouping GREEN | 148 | W164 | `test_destructive_restic_actions_need_explicit_confirmation` | Fixed `backup.sh` | PASS | Restic gate tests pass, 1 skipped | required | Grouping RED |
| Grouping review | 148 | W164 | Fresh-context `code-reviewer` review | PR 1111 at `d50615a8c` | PASS | Approve with follow-up: preview contradicted the real run (medium), substring test (low), runbook reason (low); 146 s, 1 round; all three fixed | required | - |
| Restic dry run | 148 | W164 | `restic forget --dry-run` with the fixed grouping | Both local repositories, read-only | PASS | State: remove 14 of 48; host: remove 0 of 34 | required | - |
| Hosted lab isolation | 148 | W164 | `test_no_document_or_script_starts_the_root_with_every_profile` | PR 1111 candidate-core at `a2eb4c866` | FAIL | The whole-stack hook rule from PR 1101 quotes its BLOCKED examples; first selected by this backup change | required | - |
| Lab isolation fixed | 148 | W164 | `test_no_document_or_script_starts_the_root_with_every_profile` | Exemption for the blocking hook rule, like `lab.py` | PASS | Lab isolation tests pass | required | Hosted lab isolation |
| Prune after fix | 148 | W164 | Runbook step 7 `forget-prune` | Approved command after PR 1111, host and tags grouping | PASS | 14 state snapshots removed, IDs equal to the dry run; 352 MiB of blobs removed; raw data 7.165 to 6.519 GiB | required | First prune |
| Observe RED | 148 | W164 | `test_observe` | New tests before the module | FAIL | Import error: no observe module | required | - |
| Observe GREEN | 148 | W164 | `test_observe` | `observe.py` | PASS | 6 tests: window counts, owners and next steps, no log text, window and cost, unreadable journal, empty store | required | Observe RED |
| Real observe report | 148 | W164 | `observe.py report` | This host, 2026-11-12 to 19 | PASS | 5 failed backups with RUN-0021 as owner, known capture gaps, 0.131 s | required | - |
| Observe review | 148 | W164 | Fresh-context `code-reviewer` review | `9cfb6e1ff` | FAIL | Block: 1 blocker, 1 high, 2 medium, 5 low; 229 s, 1 round | required | - |
| Observe fix RED | 148 | W164 | `test_observe` | Rewritten tests on `9cfb6e1ff` | FAIL | 7 failures, 1 error | required | - |
| Observe fix GREEN | 148 | W164 | `test_observe` | Fixed `observe.py` | PASS | 11 tests | required | Observe fix RED |
| Observe re-review | 148 | W164 | Fresh-context `code-reviewer` review | `4194f807e`, round 2 | PASS | Approve with follow-up: nine findings resolved, four low follow-ups fixed; 102 s | required | Observe review |
| Follow-up RED | 148 | W164 | `test_observe` | New tests on `4194f807e` | FAIL | 3 failures, 1 error | required | - |
| Follow-up GREEN | 148 | W164 | `test_observe` | Follow-up fix | PASS | 13 tests | required | Follow-up RED |
| Backup under budget | 148 | W164 | Daily `hyhome-backup.service` | 2026-11-20 03:42 KST run | FAIL | Exit 1: local Restic and checks ran, the state repository ended at 8200 MiB (over 8 GiB), and the offsite copy was refused at the R2 cap (9.41 GB after upload against 9 GB); read from the journal on 2026-11-24 by TSK-0111 | required | - |
| Daily backups after | 148 | W164 | `journalctl -u hyhome-backup.service`, lifecycle and size lines only | 2026-11-21 to 24 runs, read 2026-11-24 by TSK-0111 | FAIL | 4 of 4 failed: 11-21 and 11-24 skipped Restic at 8267 and 8269 MiB of state; 11-22 and 11-23 ran local Restic and checks (8075 and 8208 MiB) but the offsite copy was refused at the R2 cap (9.59 GB after upload against 9 GB, owner limit 10 GB; R2 held 7.75 GB) | required | - |

### Resolution Links

Grouping GREEN resolves Grouping RED, Lab isolation fixed resolves Hosted
lab isolation, Prune after fix resolves First prune, Observe GREEN
resolves Observe RED, Observe fix GREEN resolves Observe fix RED, Observe re-review resolves
Observe review, and Follow-up GREEN resolves Follow-up RED.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 148 | pending | Scheduled analysis, Grouping GREEN, Prune after fix, Observe GREEN, Real observe report | On 2026-11-19 the owner chose to accept once the open required rows are resolved; they stay required and open | @buenhyden |

### Remaining Conditions

On 2026-11-19 the owner kept criterion 148 pending: the SDLC accepts it only
after its open required rows are resolved; TSK-0095 lists them with their
next check.

The daily backup must show the state repository under budget and the
offsite copy within the R2 cap. Every run from 2026-11-20 to 24 failed
(Backup under budget, Daily backups after): the state repository grew back
over 8 GiB and the R2 copy hits its 9 GB cap while the locked memory copies
of criterion138 remain. The budget, a further prune or the R2 cap is the
owner's decision; elapsed time does not close this row.

## Handoff

### Promotion Receipt

`backup.sh` and RUN-0021 step 7 hold the grouping rule.

### Next Owner

The owner decides criterion 148 and, if the backup fails again, the budget.
