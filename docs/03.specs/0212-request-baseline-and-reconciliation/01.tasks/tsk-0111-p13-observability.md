---
title: "P13 Observability Task"
version: "0.1.2"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0111"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-24"
---

# P13 Observability Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion167/W183 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply the D13 delta to the existing observe report, session analysis and
work dispatcher without a new telemetry store, and record the real backup
results in their owner Task, TSK-0092.

##### Inputs and Authority

The direct P13-OBSERVABILITY1.2.0 request authorizes this workspace, scoped
implementation, read-only observation of the real stores and journals and
normal commit, push, PR and merge. Inputs are the matching package
README/P13, D13, the Docker profile and its findings on criterion148; no
other workspace is required. Start was clean `main` 086a9ad7 on branch
`codex/p13-observability-1-2-0` in the linked worktree `.worktrees/p13`.
Brief p13-observability revision 1 bound this scope before the first edit.
This Task's forecast was recorded before the start (revision 1, P30 45, P50
70, P80 110 elapsed minutes, no comparable prior). Direct user authorization
is authority; this record is not.

#### Execution Log

##### Work Performed

Retained without rework: the capture, analysis, forecast and dispatch stores,
the analysis timer, the observe report's owners, next steps, fixed-shape
echo of worker-writable fields and its failure-not-zero rules. A read-only
report on the real stores for 2026-11-19 to 24 found four gaps against D13:
the analysis unit renamed in P10 made its earlier runs look missing (a false
missed-run failure), a dispatch run refused before any worker started counted
as an ordinary failure, the dispatch reports' provider cost, time and unit
states were not linked, and analysis candidates stopped at the review
decision with no link to a Task, its check or an effect. Dispatch run folders
holding worker logs and patches were never removed.

`observe.py` now counts the analysis unit's runs under its earlier fixed name
for the current unit; counts a unit that failed before it started as
`blocked` and a run with only such units as `blocked`; shows dispatch run and
unit seconds, the wait from run start to each unit start, and per known
provider the CLI's own cost estimate, turns and units without a cost; and
shows the candidate `chain` from source events through review, promotion,
Task link and effect, with effects not yet observed counted apart. Billed
cost stays unmeasured. `session_analysis.py` adds `link` (an accepted
candidate to `SPEC-####-TSK-####` and its evidence row) and `effect`
(`improved`, `unchanged` or `worsened` with a sample of one or more); a
linked candidate without an effect stays until 90 days after its decision.
`work_dispatch.expire_runs` removes worker logs and patches 30 days after a
finished run's report and the run folder after 90, keeping a folder with a
process record for `cleanup`; each daily analysis run calls it. The harness
maintenance guide 2.7.0 documents the commands and report fields.

###### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0111 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0111 | ready | in-progress | #work-performed |
| SPEC-0212-TSK-0111 | in-progress | completed | #criterion-decisions |

##### Blockers and Decisions

No Q01-Q04 question is reopened. The real journal shows every daily backup
from 2026-11-20 to 24 failed: the state repository is back over its 8 GiB
budget and the offsite copy is refused at the R2 9 GB cap while the locked
criterion138 memory copies remain. TSK-0092 now records those runs as FAIL
instead of the NOT_RUN it held; criterion148 stays pending and open. Raising
the budget or the cap, or another approved prune, is the owner's decision
and is not done here. The three accepted candidates were promoted on
2026-11-23 but carry no Task link yet, so the chain shows them unlinked;
no link is invented.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 167 | W183 | method=review; tool=-; command=- | P13 1.2.0 package, D13, Docker profile and findings on criterion148; current observe, session_analysis, work_dispatch, TSK-0092 | PASS | Gaps listed in Work Performed; stores, timer and report rules retained | required | - |
| E02 | 167 | W183 | method=observation; tool=Python3.12.3 CLI; command=observe.py report --since 2026-11-19T00:00:00+00:00 --until 2026-11-24T12:00:00+00:00 | Real stores and journals on 086a9ad7, read-only | FAIL | Analysis unit reported with no run in the window although the analysis store holds 8 complete runs (renamed unit); a pre-spawn brief refusal counted as failed; 5 failed backups | required | - |
| E03 | 167 | W183 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_session_analysis | Link and effect regressions on 086a9ad7 | FAIL | Witnessed RED: 2 errors, no link function | required | - |
| E04 | 167 | W183 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_session_analysis | Change | PASS | Exit0; 29 tests | required | E03 |
| E05 | 167 | W183 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_work_dispatch tests.validation.test_session_analysis | Run expiry regressions before expire_runs and its daily call | FAIL | Witnessed RED: 1 error (no expire_runs), then 1 failure (the daily run left a 100-day run) | required | - |
| E06 | 167 | W183 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_work_dispatch tests.validation.test_session_analysis | Change | PASS | Exit0 | required | E05 |
| E07 | 167 | W183 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_observe | Five new observe tests on 086a9ad7 | FAIL | Witnessed RED: 3 failures and 2 errors: renamed unit, blocked run, unit time and cost, candidate chain, billed cost | required | - |
| E08 | 167 | W183 | method=observation; tool=Python3.12.3 CLI; command=observe.py report --since 2026-11-19T00:00:00+00:00 --until 2026-11-24T12:00:00+00:00 | Worktree change, real stores, read-only | FAIL | Found a defect: a failing dispatch run was named after its provider ("claude failed") because the provider label reused the run-name variable | required | - |
| E09 | 167 | W183 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_observe | Run-name assertion added | FAIL | Witnessed RED: 1 failure | required | - |
| E10 | 167 | W183 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_observe | Fixed change | PASS | Exit0; 18 tests; with the analysis, dispatch and surface-ownership suites also passing; ruff check and format clean on the six changed Python files | required | E07,E09 |
| E11 | 167 | W183 | method=observation; tool=Python3.12.3 CLI; command=observe.py report --since 2026-11-19T00:00:00+00:00 --until 2026-11-24T12:00:00+00:00 | Fixed change, real stores, read-only | PASS | Analysis unit 6 finished runs, no missed-run failure; runs blocked 1, failed 1, succeeded 1, cancelled 1; units blocked 3, succeeded 3, cancelled 1; claude 3 units, 0.012474 USD CLI estimate, 9 turns; start wait n 4, median 5.0 s, max 9.2 s; chain 14 candidates, 3 accepted and promoted, 0 linked; 5 backup failures remain; 0.1 s | required | E02,E08 |

##### Resolution Links

E04 resolves E03, E06 resolves E05, E10 resolves E07 and E09, and E11
resolves E02 and E08. The daily backup failures of 2026-11-20 to 24 are
recorded as criterion148 rows in TSK-0092 and stay open there.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 167 | accepted | E01,E04,E06,E10,E11 | Owner @buenhyden accepted on 2026-11-24 in this chat during P16 (TSK-0114). Effects stay unobserved until a candidate is linked and compared. | @buenhyden |

##### Remaining Conditions

No candidate has a Task link or an observed effect yet, so the chain shows
effects as unobserved rather than as results. Criterion148 stays failing in
TSK-0092 until the owner decides the state budget, a prune or the R2 cap and
a later daily backup succeeds. The first daily analysis run on the merged
code migrates the analysis store and runs the dispatch expiry.

#### Handoff

##### Promotion Receipt

`observe.py`, `session_analysis.py` and `work_dispatch.py` own the behavior;
the harness maintenance guide owns the commands and fields. This Task owns
execution evidence only.

##### Next Owner

The owner decides criterion167 in P16 and the backup budget for
criterion148. The next input for this workspace is P14-DOCKER; it is not
executed automatically. Keep the package through P17.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
