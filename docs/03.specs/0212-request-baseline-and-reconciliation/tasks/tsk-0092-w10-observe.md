---
title: "W10 Observe Task"
version: "0.2.0"
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
| Grouping review | 148 | W164 | Fresh-context `code-reviewer` review | PR 1111 at `d50615a8c` | PASS | Approve with follow-up: preview contradicted the real run (medium), substring test (low), runbook reason (low); 146 s, 1 round; all three fixed | required | - |
| Restic dry run | 148 | W164 | `restic forget --dry-run` with the fixed grouping | Both local repositories, read-only | PASS | State: remove 14 of 48; host: remove 0 of 34 | required | - |
| Hosted lab isolation | 148 | W164 | `test_no_document_or_script_starts_the_root_with_every_profile` | PR 1111 candidate-core at `a2eb4c866` | FAIL | The whole-stack hook rule from PR 1101 quotes its BLOCKED examples; first selected by this backup change | required | - |
| Lab isolation fixed | 148 | W164 | `test_no_document_or_script_starts_the_root_with_every_profile` | Exemption for the blocking hook rule, like `lab.py` | PASS | Lab isolation tests pass | required | Hosted lab isolation |

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
