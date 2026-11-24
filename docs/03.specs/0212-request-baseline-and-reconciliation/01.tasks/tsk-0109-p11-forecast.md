---
title: "P11 Task Forecast Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-24"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0109"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-24"
---

# P11 Task Forecast Task

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

Own criterion165/W181 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply the D11 forecast delta to the existing Docker forecast store without
rebuilding the computations TSK-0089 implemented.

##### Inputs and Authority

The direct P11-FORECAST1.2.0 request authorizes this workspace, scoped
implementation, bounded observations and normal commit, push, PR and merge.
Inputs are the matching package README/P11, D11, the Docker profile and
finding D23-13; no other workspace is required. Start was clean `main`
8ba09206 on branch `codex/p11-forecast-1-2-0` in the linked worktree
`.worktrees/p11`. Brief p11-forecast revision 1 bound this scope before the
first edit. Direct user authorization is authority; this record is not.

#### Execution Log

##### Work Performed

Retained without rework: the append-only revisions and their triggers, the
last revision fixed before the start, finite and ordered quantiles, the
future-end and active-over-elapsed refusals, censoring of failed and
cancelled tasks, and the Wilson and pinball computations. Discovery against
D11 and D23-13 found these gaps. `score` grouped by task type only, so an
elapsed and an active forecast of one type were scored together, and
without `--type` everything was pooled. `sample_size` was a self-reported
number: the one real forecast declared 10 while the store held no completed
comparable task. An outcome did not store the revision it was scored
against. A task that ended waiting on a permission or decision had no state,
open forecasts were not counted, and R151's assumptions and reference class
were not enforced. No P07-P10 Task had recorded a forecast.

`forecast` now refuses an empty `assumptions` or `reference_class` and a
non-integer or negative `sample_size`, and stores `comparable_prior`: the
completed tasks of the same type and time basis that ended before the
forecast time. The CLI prints it with `uncalibrated prior` below 20 and the
probability meaning of P30/P50/P80. `observe` accepts `blocked` and stores
`forecast_revision`. `score` takes `--time-basis`, lists each task type and
time basis group with completed, censored and open counts, counts `blocked`
apart and `open` forecasts, and labels a selection that mixes time bases
`mixed time bases; score one basis`, never empirical. Existing rows keep
their values; the two new columns are added empty to an earlier store, and an
earlier outcome is still scored against the revision fixed before its start.
ENVIRONMENT-CONSTRAINTS 2.5.0 changes R151, R153 and R154, and the harness
maintenance guide 2.5.0 documents the commands.

This Task is itself the first real consumer. Its forecast was recorded in the
real store before any edit, at 2026-11-23T23:55:52Z: type `harness-change`,
elapsed basis, P30 60, P50 90 and P80 150 minutes, with its assumptions and
reference class, declared sample 0. The outcome is recorded after the merge.

##### Blockers and Decisions

No Q01-Q04 question is reopened. A forecast error is not a gate; the P12
dispatcher keeps R155 (per-task P80 values are never summed) and P13 reads
the groups for under- and over-estimation. The declared `sample_size` is
kept for an outside reference class, and the store count is reported beside
it. `observe.py` already counts outcome statuses generically and needs no
change for `blocked`.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 165 | W181 | method=review; tool=-; command=- | P11 1.2.0 package, D11, D23-13; current task_forecast and its observe consumer; real forecast store read only | PASS | Gaps listed in Work Performed; computations and append-only contract retained | required | - |
| E02 | 165 | W181 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_task_forecast tests.validation.test_observe | New regressions on 8ba09206 | FAIL | Witnessed RED: 4 new tests, 3 failures (subtests) and 3 errors: mixed bases, comparable prior, revision link with blocked and open, required assumptions | required | - |
| E03 | 165 | W181 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_task_forecast tests.validation.test_observe | Change | PASS | Exit0; 29 tests | required | E02 |
| E04 | 165 | W181 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.validation.test_task_forecast tests.validation.test_observe tests.validation.test_work_dispatch tests.validation.test_session_analysis tests.lib.hooks.test_session_capture | Change | PASS | Exit0 | required | - |
| E05 | 165 | W181 | method=automated; tool=ruff; command=ruff check and ruff format on the changed Python files | Change | PASS | Exit0 | required | - |
| E06 | 165 | W181 | method=observation; tool=Python3.12.3 CLI; command=task_forecast.py forecast with and without assumptions | A temporary capture directory | PASS | With them: comparable_prior 0, `uncalibrated prior` and the probability meaning printed; without them: FORECAST_REFUSED exit 2 | required | - |
| E07 | 165 | W181 | method=automated; tool=Python3.12.3; command=check-agent-governance-contract.py --mode repository --section all; check-script-manifest.py; provider_surface_renderer.py --check; check-document-metadata.py --mode check-changed; check-document-links.py --mode all --changed | Changed-profile selection on the candidate | PASS | Governance failures0; manifest valid; renderer drift0; metadata violations0; links failures0 | required | - |
| E08 | 165 | W181 | method=observation; tool=Python3.12.3 CLI; command=task_forecast.py forecast SPEC-0212-TSK-0109 | Real store, 2026-11-23T23:55:52Z, before the first edit | PASS | Revision 1 recorded with type harness-change, elapsed basis, P30 60, P50 90, P80 150, assumptions and reference class | required | - |

##### Resolution Links

E03 resolves the witnessed failures in E02.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 165 | pending | E01,E03,E04,E05,E06,E07,E08 | Implementation, focused regressions and a real pre-start forecast are recorded; the real outcome of this Task and owner acceptance in P16 remain | @buenhyden |

##### Remaining Conditions

The outcome of SPEC-0212-TSK-0109 is recorded in the real store after the
merge and scored with `score --type harness-change --time-basis elapsed`.
One sample stays an insufficient sample; calibration needs 20 comparable
completed tasks.

#### Handoff

##### Promotion Receipt

`task_forecast.py` owns the behavior; ENVIRONMENT-CONSTRAINTS R151, R153 and
R154 own the rules; the harness maintenance guide owns the commands. This
Task owns execution evidence only.

##### Next Owner

The owner decides criterion165 in P16. The next input for this workspace is
P12-PARALLEL; it is not executed automatically. Keep the package through P17.

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
