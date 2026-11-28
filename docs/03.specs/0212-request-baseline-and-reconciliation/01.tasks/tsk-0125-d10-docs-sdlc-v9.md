---
title: "D10 v9 Task Lifecycle and Document Contract Task"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0125"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-28"
---

# D10 v9 Task Lifecycle and Document Contract Task

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

Own criterion182/W198 in the [Spec](../spec.md) and [Plan](../plan.md). Apply
D10 of the v9 task prompts: fix the active document contract that kept every
Task made from the current template in `draft`, give the related SPEC-0212
Tasks the status their evidence supports, and remove retired inputs from an
active check, reusing the accepted document system.

##### Inputs and Authority

On 2026-11-28 the user directly requested D10 from
`_workspace/workspace_task_prompts_20261127_progress_v9/` (prompt
`10_docs_specs_sdlc_ci.md`), limited to that prompt's scope, with commit,
push, PR and merge after checks. D01 v8 (TSK-0115) routed the `draft`
frontmatter of TSK-0098 to TSK-0120 and their stale Next Owner rows to D10,
and TSK-0044 named D10 the owner of the P03 global CI admission residual.
Work ran in the primary checkout on branch `docs/d10-task-lifecycle` from
`main` `771ef9e3c`; brief `d10-v9` bound this Task and the Spec and Plan
rows. Direct user authorization is authority; this record is not.

#### Execution Log

##### Work Performed

###### Census

| Task | Finding | Verdict |
| --- | --- | --- |
| T01 contract | The metadata gate refuses a Task status change without a lifecycle event chain, read from `Lifecycle Events` under Execution Log, Work Performed (Registry `task_lifecycle_events`, `section_forms`). The document-core Task template had no such table and the Task role design no such table entry, so no Task made from it had reached `completed`: TSK-0098 to TSK-0124 were all `draft`, including 19 whose criteria were accepted | CHANGE_REQUIRED (below) |
| T02 Stage 05 and CI admission | Terrakube has no HOME service, include or active Stage 05 instruction (D09 v9 census). The TSK-0044 P03 global CI admission residual, reproduced in a throwaway worktree with a change to `check-p03-hermes.py`: the changed profile selects `leaf.local-diff-hygiene`, `leaf.repository-integrity-regressions` and `leaf.p03-hermes`, and `leaf.p03-hermes` is admitted (exact optional invocation binding since `a6e797d0b`, 2026-11-20). `--explain` printed nothing because it lists only public validator rows, which made a non-empty plan look like "no gate selected" and produced the 2026-11-26 NOT_RUN | CHANGE_REQUIRED (below); the residual is resolved |
| T03 Spec, Plan, Task | SPEC-0212 Spec and Plan `approved`; Tasks allowed to run under it. TSK-0098 to TSK-0124: 19 with every criterion accepted, 8 executing with pending criteria. Stale Next Owner text in TSK-0115, TSK-0116 and TSK-0120 | CHANGE_REQUIRED (below) |
| T04 retired inputs | The three retired overlays are gone. `_workspace_model_connections.py` still derived the n8n-worker to Ollama reachability row only from `docker-compose.ollama-local.yml`, so the current edge in the n8n leaf was never modelled | CHANGE_REQUIRED (below) |
| T05 agents, QA, CI | No active rule forces unrelated documents or D13 and D14 to finish; branch protection and required checks unchanged | REUSE |
| T06 quality tools | k6, Pact Broker and WireMock unchanged; no bottleneck found by D09 v9 (TSK-0052) | REUSE |

###### Changes

- Task template: a `Lifecycle Events` table with the registered headers under
  Execution Log, Work Performed, and an author prompt that every status change
  is one row and `completed` needs PASS evidence and an accepted decision.
- Task role design 4.1.0: table `task.lifecycle_events`; the Registry pins its
  new hash and version.
- Tasks moved to `completed` with a draft to ready to in-progress to completed
  chain (all assigned criteria accepted): TSK-0098 to TSK-0105, TSK-0107,
  TSK-0109, TSK-0111 to TSK-0113 and TSK-0115 to TSK-0120.
- Tasks moved to `in-progress` (executed, criteria pending): TSK-0106,
  TSK-0108, TSK-0110, TSK-0114 and TSK-0121 to TSK-0124.
- Next Owner of TSK-0115, TSK-0116 and TSK-0120 refreshed. The TSK-0116
  text naming the renderer policy write and KV deletion as owner steps for D07
  and D11 was stale: its own E26 and E27 record both done on 2026-11-25
  (correction in TSK-0126).
- The connection model reads the n8n-worker to Ollama edge from the n8n leaf.
- `ci_gate_runner.py --explain` names, on stderr, the admitted invocations its
  rows do not show; stdout rows are unchanged. The TSK-0044 residual rows stay
  as recorded (terminal Task); E06 to E08 here resolve them.

##### Blockers and Decisions

None that need an owner choice. Terminal Task bodies were not rewritten; the
lifecycle tables were added to the Tasks this change completes. The P03 global
CI admission residual is recorded under Verification Evidence.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 182 | W198 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.document_governance.test_registry | Template before the change | FAIL | RED: the template had no `###### Lifecycle Events` under Work Performed | required | - |
| E02 | 182 | W198 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.document_governance.test_registry | Template after the change | PASS | GREEN | required | E01 |
| E03 | 182 | W198 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.ops.test_workspace_model_connections | Fixture with the edge in the n8n leaf, before the code change | FAIL | RED: no reachability row | required | - |
| E04 | 182 | W198 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.ops.test_workspace_model_connections | After the code change | PASS | GREEN | required | E03 |
| E05 | 182 | W198 | method=automated; tool=Python3; command=check-document-metadata.py --mode check-changed --base-ref origin/main | Branch `docs/d10-task-lifecycle` | PASS | selected=882 violations=0 | required | - |
| E06 | 182 | W198 | method=automated; tool=Python3; command=run-ci-gate.py --profile changed --explain --job candidate-core | Throwaway worktree at `origin/main` `771ef9e3c` with an uncommitted change to `scripts/validation/check-p03-hermes.py` | PASS | Plan `leaf.local-diff-hygiene`, `leaf.repository-integrity-regressions`, `leaf.p03-hermes` (`scripts/validation/check-p03-hermes.py`); parity passed, so `leaf.p03-hermes` is admitted; this exercises the admission that TSK-0044 recorded as FAIL on 2026-11-02 and NOT_RUN on 2026-11-26 | required | - |
| E07 | 182 | W198 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_ci_gate_plan | `ci_gate_runner.py` before the explain change | FAIL | RED: test_explain_reports_admitted_invocations_its_rows_do_not_show, stderr empty | required | - |
| E08 | 182 | W198 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_ci_gate_plan | After the explain change | PASS | GREEN; stdout rows unchanged | required | E07 |

##### Resolution Links

E02 resolves E01, E04 resolves E03 and E08 resolves E07. E06 exercises the
TSK-0044 P03 global CI admission that row recorded as FAIL and NOT_RUN.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 182 | pending | E01,E02,E03,E04,E05,E06,E07,E08 | Awaiting owner acceptance after the hosted checks | @buenhyden |

##### Remaining Conditions

- The owner accepts criterion182 once the hosted checks pass.
- TSK-0106, TSK-0108, TSK-0110, TSK-0114 and TSK-0121 to TSK-0124 stay
  `in-progress` until the owner decides their criteria; each then records its
  `in-progress` to `completed` row.

#### Handoff

##### Promotion Receipt

None: this Task changes a template, a role-design contract, one library
branch and Task status records; no document is promoted.

##### Next Owner

The owner decides criterion182 and the pending criteria named above. No other
prompt is started automatically; D11 and D12 run on the shared Spec files
after this change.

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
