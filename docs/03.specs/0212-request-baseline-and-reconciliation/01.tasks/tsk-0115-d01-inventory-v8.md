---
title: "D01 v8 Inventory Reconciliation Task"
version: "0.1.2"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-26"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0115"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-25"
---

# D01 v8 Inventory Reconciliation Task

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

Own criterion171/W187 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply D01 of the lifecycle v8 task prompts: freeze the workspace identity,
recount the Compose inventory, census the Spec Packages, reuse accepted
inventory work and route each open item to one next owner. Source, Compose
and runtime state are unchanged.

##### Inputs and Authority

On 2026-11-25 the user directly requested D01 from
`_workspace/workspace_task_prompts_20261125_lifecycle_v8/` (prompt
`01_workspace_inventory_reconciliation.md`), limited to that prompt's scope,
with commit, push, PR and merge after checks, and asked that completed and
merged work not be re-run. Work ran on branch `docs/d01-v8-inventory` in the
linked worktree `.claude/worktrees/d01-v8-inventory` from clean `main`
`24b8df116`; brief `d01-v8-inventory` revision 1 bound this Task, the Spec and
the Plan before the first edit. The package is an ignored input, read only;
no tracked file depends on it. Direct user authorization is authority; this
record is not.

#### Execution Log

##### Work Performed

###### T01 workspace identity

Root `/home/hyunyoun/data/hy-home.docker`, branch `main`, clean tracked and
untracked state, one primary checkout plus this linked worktree. After
`git fetch --prune`, local HEAD, `origin/main` and the package reference all
equal `24b8df116128f27311c460eba9d66b8a6d4d5e97`; `HEAD..origin/main` is
empty. Docker context `default`, Compose 5.6.1. No reset, clean, checkout of
the primary tree or pull was used.

###### T02 Compose inventory

| Axis | Observed | Package claim | State |
| --- | --- | --- | --- |
| Root includes | 33, none under `labs/` | 33 | REUSE |
| Definitions with every profile | 89; names equal the package `SERVICE_INVENTORY.json` set (0 only-package, 0 only-live) | 89 | REUSE |
| Services / jobs | 70 `unless-stopped` / 19 `hy-home.role: job` with `restart: "no"` | 70 / 19 | REUSE |
| Default selection | 0 services without a profile; 61 profiles | - | REUSE |
| `config -q` | exit 0 | - | PASS |
| Retired or moved | Nginx, Kafka Connect, Schema Registry, Open WebUI and Supabase absent from root; Flower behind `airflow-flower` | same | REUSE |
| Running (`hy-home-infra`) | 57 of 70 services, 0 jobs, 0 unhealthy, 0 containers outside the root set | not observed | observation only |
| Not running | comfyui, flower, neo4j, open_notebook, opensearch, opensearch-dashboards, pact-broker, pushgateway, surrealdb, terrakube-api, terrakube-executor, terrakube-ui, wiremock | - | optional profiles not started; not a defect claim |
| Sandbox | `n8n-sandbox-api` and `n8n-sandbox-runner-1` run; POL-0078 keeps profile `n8n-sandbox` out of the default selection (owner decision 2026-11-09); certs is a job | target: API/runner HOME-ready, certs job | CHANGE_REQUIRED, owner D06-T04 (REQ-27) |

The DATA-0096 committed ledger the prompt names was retired by the owner on
2026-11-14 (`3238347e0`) because it was a dated, non-replayable snapshot with
no current consumer. It is not recreated: a new Stage 90 package needs a
consumer named first. Its generator `scripts/operations/workspace-inventory.py`
remains and its tests pass. The counts above are recorded here instead.

###### T03 requirement trace

The package verifier passed 1,170 structural checks (preservation, references,
single ownership, fingerprints); it states that semantic review and runtime are
not covered. The 63/166/73/35 counts are the package's structural bases only.
The TSK-0040 2026-11-07 requirement trace is reused for unchanged rows; no
second independent semantic review was run (SECOND_REVIEW_NOT_RUN).

###### T04 Spec Package census and writers

8 Specs and 8 Plans, all `approved`; 144 Tasks: completed 85, cancelled 2,
in-progress 36, blocked 2, draft 17, statusless multi-item 2 (TSK-0007,
TSK-0049). This equals the package census once its two multi-item Tasks are
counted. Single writers stay as the package routes them: D02 Traefik/DNS/LAN,
D07 credentials and trust, leaf owners for service files, D08 observability,
D10 shared Spec/Plan, Registry and checkers, D12 final A/B acceptance; D01
owns only this inventory record.

###### T05 evidence axes

| Item | Current record | State | Next owner |
| --- | --- | --- | --- |
| Criteria 51–55 | TSK-0040 not-required (owner, 2026-11-10); full-gate FAIL rows kept | REUSE; terminal Task not reopened | none |
| Criteria 86/89 → 104/105 | TSK-0047 not-required, handed to TSK-0052; 104 and 105 pending | open | D09 |
| Criterion 23 | TSK-0022 accepted on 2026-11-26 (D05 lifecycle v8); Hermes delivery, not a generic Hermes Agent link | closed | D05 |
| AI-011 / INFRA-008 | Printed on 2026-11-25; the owner rotated both at 17:13 KST the same day (SPEC-0204 TSK-0022 "SearXNG credential rotation", SPEC-0212 TSK-0116 E15), corrected 2026-11-26 | closed | D07 |
| Criteria 154–170 | TSK-0098 to TSK-0114 keep frontmatter `draft` while several criteria are accepted | lifecycle state mismatch to judge | D10-T03 |
| Criteria 138, 148, 162, 164, 166 | TSK-0114 open boundaries | open | owner per TSK-0114 |

###### T06 service roles

No root source owns users, DB or objects through Supabase, and Open WebUI is
not in root, so no duplicate owner exists; this reuses the TSK-0040
2026-11-07 conclusion. Optional services not running are not classed unused.

###### Next prompts and preconditions

| Prompt | Open item | Precondition |
| --- | --- | --- |
| D07 | Rotate AI-011/INFRA-008 and record consumer readback | Owner access to the secret files and OpenBao |
| D02 | Old credential refused on `/search`; B route acceptance | D07 rotation; owner on 192.168.0.22 |
| D06 | Sandbox API/runner default selection (REQ-27) | Owner choice against POL-0078 2026-11-09 decision |
| D05 | Criterion 23 acceptance | Owner decision |
| D09 | Criteria 104/105 | Fresh advisory and artifact reviews |
| D10 | Task lifecycle states of TSK-0098 to TSK-0114 | None |
| D12 | Final A/B and Git acceptance | Other prompts' results |

##### Blockers and Decisions

The prompt asks to reuse the committed DATA-0096 ledger, which no longer
exists by owner decision; recording counts here follows that decision and
the prompt's minimal-record fallback. No other prompt was run.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 171 | W187 | method=observation; tool=git; command=git fetch --prune; git rev-parse HEAD origin/main; git status --short | `main` 24b8df116, 2026-11-25 | PASS | Equal SHAs, clean tree | required | - |
| E02 | 171 | W187 | method=automated; tool=docker compose 5.6.1; command=config -q; --profile '*' config --services; config --profiles | `main` 24b8df116 | PASS | exit 0; 0 default, 89 with every profile, 61 profiles | required | - |
| E03 | 171 | W187 | method=automated; tool=Python3.12.3; command=classify rendered services by restart and hy-home.role, counts only | `main` 24b8df116 | PASS | 70 services, 19 jobs; names equal package inventory | required | - |
| E04 | 171 | W187 | method=observation; tool=docker; command=docker ps by compose project and health | HOME host, 2026-11-25 | PASS | 57 running, 0 unhealthy, 0 outside root | required | - |
| E05 | 171 | W187 | method=automated; tool=Python3.12.3; command=python3 -I dependencies/verify_bundle.py | Package v8 | PASS | 1,170 checks, 0 failed; semantic review and runtime not covered | required | - |
| E06 | 171 | W187 | method=automated; tool=Python3.12.3; command=python3 -m unittest tests.lib.ops.test_workspace_inventory tests.validation.test_workspace_inventory tests.lib.ops.test_workspace_connections | `main` 24b8df116 | PASS | 52 tests OK | required | - |
| E07 | 171 | W187 | method=review; tool=-; command=- | Frontmatter of every docs/03.specs document | PASS | Census above | required | - |
| E08 | 171 | W187 | method=review; tool=-; command=- | Second independent semantic review of the requirement trace | NOT_RUN | Not run in this pass | optional | - |

##### Resolution Links

None: no row resolves another.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 171 | accepted | E01,E02,E03,E04,E05,E06,E07 | Owner @buenhyden accepted on 2026-11-25 in this chat; the routed items are tracked by their owners (D07 in TSK-0116, D02 in TSK-0117) | @buenhyden |

##### Remaining Conditions

None for criterion171. The routed items stay with the owners listed above;
this Task does not close them.

#### Handoff

##### Promotion Receipt

None: this Task records observation and routing only and promotes no
long-lived rule.

##### Next Owner

The owner chooses the next prompt from the table above; no prompt is started
automatically.

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
