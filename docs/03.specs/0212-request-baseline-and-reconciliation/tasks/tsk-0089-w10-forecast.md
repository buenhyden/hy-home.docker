---
title: "W10 Forecast Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0089"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-18"
---

# W10 Forecast Task

## Scope

### Objective and Parent

Own criterion 145 and work unit W161 under the [Spec](../spec.md) and
[Plan](../plan.md). Bring task forecasting to the 4.2.0 W10-FORECAST
design with D09: completion-time quantiles fixed before work and scored
against what happened.

### Inputs and Authority

The direct 2026-11-18 request runs W10-FORECAST from the git-ignored 4.2.0
package. On 2026-11-18 the owner chose a private local store and elapsed
time as the default basis. W07-BRIEF supplies the request identity this
reuses as the task reference. Parallel completion distributions belong to
W10-PARALLEL.

## Execution Log

### Work Performed

#### Gap analysis

No forecasting existed; the repository's quantile mentions are metric
dashboards. The package tool `score_forecasts.py` was read as reference and
not installed.

#### W161 design

`scripts/operations/task_forecast.py` keeps `forecast.sqlite3` in the
private capture directory. `forecast` appends a revision with P30, P50 and
P80 minutes, the time basis, assumptions, reference class and sample size,
and refuses inversion, a negative value, another unit or basis, and a task
that already has an outcome. SQLite triggers refuse any update or delete of
a forecast or outcome, so a number cannot be replaced afterwards.
`observe` records one completed or cancelled outcome with optional active,
runner-wait and user-wait minutes, and refuses a task without a forecast
fixed before its start, an end before the start, or an active-basis result
without active minutes. `score` uses the last pre-start revision and reports
per quantile the sample size, the share of actuals at or under the forecast
and the mean pinball loss, counts cancelled tasks apart as censored, and
labels fewer than 20 completed tasks `insufficient sample`. No cost or token
count is recorded. ENVIRONMENT-CONSTRAINTS-R151 to R155 and RUN-0021 state
the behavior.

#### Real forecast

Before pushing this change, the store received forecast
`W10-FORECAST-PR-CI` for the pull request's hosted checks, elapsed minutes
P30 6, P50 9, P80 16, from ten completed `ci-quality` runs on PRs 1096 to
1104 with a median of 4.6 minutes and code PRs at 6.7 and 15.3. A direct
update of that row in the real store was refused by the trigger.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0089 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0089 | ready | in-progress | #w161-design |

### Blockers and Decisions

The outcome of the real forecast is recorded after the hosted checks end.
Calibration needs at least 20 completed tasks of one type; none has it.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Forecast RED | 145 | W161 | `test_task_forecast` | New tests before the module | FAIL | Import error: no forecast module | required | - |
| Forecast GREEN | 145 | W161 | `test_task_forecast` | Forecast module | PASS | 6 tests: inversion and units, revisions and immutability, pre-start rule, single outcome, active basis, coverage, pinball and censoring | required | Forecast RED |
| Real store immutability | 145 | W161 | direct `UPDATE` on the real forecast store | `W10-FORECAST-PR-CI` revision 1 | PASS | Refused: forecasts are append-only | required | - |
| Real outcome | 145 | W161 | `task_forecast.py observe` and `score` | `W10-FORECAST-PR-CI` after the hosted checks | NOT_RUN | Hosted checks not yet run | required | - |

### Resolution Links

Forecast GREEN resolves Forecast RED.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 145 | pending | Forecast GREEN, Real store immutability | Awaits the real outcome and the owner's decision | @buenhyden |

### Remaining Conditions

The real outcome of `W10-FORECAST-PR-CI` is recorded after its checks end.

## Handoff

### Promotion Receipt

`task_forecast.py`, ENVIRONMENT-CONSTRAINTS-R151 to R155 and RUN-0021 hold
the W161 behavior.

### Next Owner

The implementer records the real outcome. The owner decides criterion 145.
