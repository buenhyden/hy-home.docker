---
title: "W10 Observe Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-19"
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
1 to 13, none above the keep counts; the host set's 34 snapshots formed one
group under the counts. A read-only `stats --mode raw-data` before the run
gave 48 state snapshots and 7.165 GiB, and 34 host snapshots and 682 KiB.
The remote prune in `offsite.sh` already groups by host and tags.

#### Grouping fix

`infra/09-platform-ops/restic/backup.sh` now runs the local forget with
`--group-by host,tags`, the existing confirmation test asserts it, and
RUN-0021 step 7 explains why. A preview that applies restic's keep rule to
the read-only snapshot list with that grouping removes 15 of 48 state and
1 of 34 host snapshots, dated 2026-09-22 to 2026-11-11.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0092 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0092 | ready | in-progress | #grouping-fix |

### Blockers and Decisions

The prune with the fixed grouping runs once after this change merges, and
the observe command follows.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Scheduled analysis | 148 | W164 | `analysis-status.json` and the analysis runs table | 2026-11-19 03:00 KST run | PASS | Scheduled, complete, 128 events, 4 candidates | required | - |
| Daily backup | 148 | W164 | `journalctl -u hyhome-backup.service` | 2026-11-13 to 19 runs | FAIL | 5 of 7 failed over the 8 GiB state budget; Restic and offsite skipped | required | - |
| First prune | 148 | W164 | Runbook step 7 `forget-prune` | Approved command, both local repositories | FAIL | Exit 0, no snapshot removed: 10 path groups under the keep counts | required | - |
| Grouping RED | 148 | W164 | `test_destructive_restic_actions_need_explicit_confirmation` | New grouping assertion on `ae3c60af8` | FAIL | `--group-by host,tags` missing | required | - |
| Grouping GREEN | 148 | W164 | `test_destructive_restic_actions_need_explicit_confirmation` | Fixed `backup.sh` | PASS | Restic gate tests pass, 1 skipped | required | Grouping RED |

### Resolution Links

Grouping GREEN resolves Grouping RED.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 148 | pending | Scheduled analysis, Grouping GREEN | Awaits the prune, the observe command and the owner's decision | @buenhyden |

### Remaining Conditions

The fixed prune must run and bring the state repository under budget, and
the observe command must be built and run.

## Handoff

### Promotion Receipt

`backup.sh` and RUN-0021 step 7 hold the grouping rule.

### Next Owner

The author runs the approved prune after merge and builds the observe
command; the owner decides criterion 148.
