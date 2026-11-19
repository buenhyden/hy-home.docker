---
title: "W08 Session Analysis Task"
version: "0.4.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-19"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0085"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-18"
---

# W08 Session Analysis Task

## Scope

### Objective and Parent

Own criterion 141 and work units W156 and W157 under the [Spec](../spec.md)
and [Plan](../plan.md). Bring scheduled session analysis to the 4.2.0
W08-ANALYSIS design: a real scheduled run over the captured sessions that
produces reviewable candidates linked to their sources.

### Inputs and Authority

The direct 2026-11-18 request runs W08-ANALYSIS from the git-ignored 4.2.0
package, with designs D07, D12 and D16, on the capture of
[TSK-0084](tsk-0084-w08-capture.md). Decision Q06 asks only for missing
values. On 2026-11-18 the owner chose deterministic analysis with no model
call, a daily run at 03:00 KST, and a status record plus the journal for
alerts. The per-call budget the owner also gave has no use without a model
step.

## Execution Log

### Work Performed

#### Gap analysis

No analysis or schedule existed for this workspace. The host has the
backup and Renovate system timers, and a user timer for another workspace,
`Project-Template`, which is outside this request and was left untouched.
The host time zone is Asia/Seoul.

#### W156 design

`scripts/operations/session_analysis.py` keeps `analysis.sqlite3` and
`analysis-status.json` in the private capture directory. A run takes the
single lease with a fencing token, or skips with exit 75 while another run
holds it. It reads the capture store read-only after the last completed
window, keys the window by workspace, start, end and policy edition, and
does nothing for a window without new events. Three deterministic rules
produce candidates: a normalized prompt seen three or more times, sessions
whose capture is not complete grouped by reason, and capture failures
grouped by reason. Each candidate records its source event IDs, frequency,
conditions, hypothesis, proposal, expected benefit, risk and test plan; a
repeated candidate accumulates while pending and keeps its decision once
decided. The commit checks the fencing token first, so a run that lost its
lease writes nothing. A busy read retries once after 5 s; SIGTERM records a
cancellation; any failure releases the lease and records its reason.
`install-timer` writes a user service without `Restart` and a timer at
`*-*-* 03:00:00 Asia/Seoul` with `Persistent=true`. `decide` records a
decision and adopts nothing. ENVIRONMENT-CONSTRAINTS-R143 to R148 and
RUN-0021 state the behavior.

The first real run exposed two capture defects, fixed here: Claude's
`[Request interrupted by user]` markers were stored as prompts, and a
session not yet reconciled was reported with an unknown reason. Nine such
capture rows and the first analysis output were deleted and the analysis
ran again.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0085 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0085 | ready | in-progress | #w156-design |

### Blockers and Decisions

On 2026-11-18 the owner decided the five candidates, recorded with
`decide --owner buenhyden`: the pasted result block repeated three times
and both Claude capture-gap reasons are accepted for a later, separately
approved Task; the repeated continuation prompt and `/compact` are
rejected. A decision adopts nothing. W08-CAPTURE removed 25 test sessions
from the capture store; none was a source of these candidates.

The installed timer first fires at 2026-11-19 03:00 KST. A missed-window
catch-up by `Persistent=true` needs the host to miss a firing, which has
not happened.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Analysis RED | 141 | W156 | `test_session_analysis` | New tests on `d324097bb` | FAIL | Import error: no analysis module | required | - |
| Analysis GREEN | 141 | W156 | `test_session_analysis` | Analysis module | PASS | 9 tests: linkage and no-op, duplicate, fencing, cancellation and failure, catch-up, decision kept, gaps and failures, unreconciled, timer | required | Analysis RED |
| Contract checks | 141 | W156 | analysis, capture, script manifest, routing and surface suites | Analysis change | PASS | 172 tests | required | - |
| Real manual run | 141 | W156 | `session_analysis.py run` | Real capture store | PASS | 474 events, 5 candidates; top candidate a prompt repeated 74 times in 2 sessions | required | - |
| Real scheduled run | 141 | W157 | systemd transient timer firing `run --trigger scheduled` | Real stores at 14:09:45 KST | PASS | Complete, no new events since the last window, not analysed twice | required | - |
| Real duplicate run | 141 | W157 | CLI run while another owner holds the lease | Real analysis store | PASS | Exit 75 skipped; the next run after release completed | required | - |
| Daily timer | 141 | W157 | `install-timer` and `systemctl --user list-timers` | User systemd | PASS | `hy-home-session-analysis.timer` next at 2026-11-19 03:00 KST | required | - |
| Candidate decisions | 141 | W157 | `session_analysis.py decide` | Five pending candidates in the real analysis store | PASS | 3 accepted, 2 rejected by buenhyden; no candidate left pending | required | - |
| Missed-window catch-up | 141 | W157 | `Persistent=true` firing after a missed run | User systemd | NOT_RUN | No firing has been missed yet | required | - |
| First 03:00 run | 141 | W157 | `journalctl --user -u hy-home-session-analysis.service`, `list-timers` | 2026-11-19 | PASS | Finished at 03:00:22 KST, 128 events, 4 candidates; next at 2026-11-20 03:00 | required | - |
| Missed-window catch-up observed | 141 | W157 | `Persistent=true` firing after a missed run | User systemd: the timer stamp set to 2026-11-18 02:00 KST, then the timer restarted, 2026-11-19 | PASS | Fired at once at 09:59:26 KST, `trigger` scheduled, `state` complete, 86 events, 4 candidates; next run still 2026-11-20 03:00 | required | Missed-window catch-up |

### Resolution Links

Analysis GREEN resolves Analysis RED.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 141 | accepted | Analysis GREEN, Real scheduled run, Real duplicate run, Daily timer, First 03:00 run, Missed-window catch-up observed | Owner @buenhyden accepted on 2026-11-19 in this chat once the catch-up was observed | @buenhyden |

### Remaining Conditions

The owner accepted criterion 141 on 2026-11-19 after the catch-up run was
observed (Missed-window catch-up observed).

The first daily run at 2026-11-19 03:00 KST is observed (First 03:00 run);
a catch-up after a missed firing was observed on 2026-11-19. The three accepted candidates need their own
approved Task before anything changes.

## Handoff

### Promotion Receipt

`session_analysis.py`, its user timer, ENVIRONMENT-CONSTRAINTS-R143 to R148
and RUN-0021 hold the W156 behavior.

### Next Owner

The implementer owns W157. The owner decides criterion 141 and approves
any Task for the accepted candidates.
