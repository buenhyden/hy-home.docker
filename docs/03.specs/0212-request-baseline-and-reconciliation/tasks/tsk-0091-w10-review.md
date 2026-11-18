---
title: "W10 Review Task"
version: "0.1.0"
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

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0091 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0091 | ready | in-progress | #w163-design |

### Blockers and Decisions

The review findings are being fixed under this Task with regression tests.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Policy checks | 147 | W163 | Governance contract and provider renderer | Workflows 1.6.0, GitHub governance 1.12.0, skill 1.4.0 | PASS | Contract 0 failures; renderer drift 0 | required | - |
| Forecast review | 147 | W163 | Fresh-context `code-reviewer` review | PRs 1105 and 1108 packet, main `24b7e60b9` | FAIL | Block: 1 high, 1 medium, 4 low; 135 s, 1 round | required | - |
| Dispatcher review | 147 | W163 | Fresh-context `code-reviewer` review | PR 1109 packet, main `24b7e60b9` | FAIL | Block: 3 high, 3 medium, 4 low; 246 s, 1 round | required | - |

### Resolution Links

None yet.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 147 | pending | Policy checks, Forecast review, Dispatcher review | Awaits the fixes and the owner's decision | @buenhyden |

### Remaining Conditions

The review findings must be fixed or recorded, and the fixes reviewed.

## Handoff

### Promotion Receipt

Workflows, GitHub governance and `code-review-dimensions` hold the W163
rules.

### Next Owner

The author resolves the review findings; the owner decides criterion 147.
