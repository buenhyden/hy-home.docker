---
title: "D01 v8 Inventory Reconciliation Task"
version: "0.1.4"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-27"
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

On 2026-11-27 the user directly requested D01 again from
`_workspace/workspace_task_prompts_20261127_progress_v9/`, limited to that
prompt's scope: reuse the accepted result, record only the differences, and
commit, push, PR and merge. Work ran in the primary checkout on branch
`docs/d01-v9-inventory` from clean `main` `180bc0eba`; brief
`d01-v9-inventory` revision 1 bound this file only.

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
| D07 | Rotate AI-011/INFRA-008 and record consumer readback | Done 2026-11-25: TSK-0116 E15, criterion 172 accepted |
| D02 | Old credential refused on `/search`; B route acceptance | Done 2026-11-25: TSK-0117, criterion 173 accepted |
| D06 | Sandbox API/runner default selection (REQ-27) | Done 2026-11-25/26: TSK-0118, criteria 174 and 175 accepted |
| D05 | Criterion 23 acceptance | Done 2026-11-26: SPEC-0204 TSK-0022 completed; TSK-0044 and TSK-0050 completed |
| D09 | Criteria 104/105 | Fresh advisory and artifact reviews |
| D10 | Task lifecycle states of TSK-0098 to TSK-0114 | None |
| D12 | Final A/B and Git acceptance | Other prompts' results |

###### v9 difference pass (2026-11-27)

Criterion171 and the v8 rows above are reused unchanged. Only inputs that
changed between `24b8df116` and `180bc0eba` were re-observed.

| Task | Observed at `180bc0eba` | Versus v8 | State |
| --- | --- | --- | --- |
| T01 | Branch `main`, clean tree, one worktree; after `git fetch`, HEAD, `origin/main` and the v9 package reference all equal `180bc0eba`; Docker context `default`, Compose 5.6.1; `COMPOSE_FILE` unset | 51 merges since `24b8df116` (PR #1209 to #1271) | REUSE; new input recorded |
| T02 definitions | 32 root includes, 0 under `labs/`; 86 definitions with every profile (67 `unless-stopped` services, 19 jobs with `restart: "no"`); 0 without a profile; 61 profiles; `config -q` exit 0; names equal the v9 `SERVICE_INVENTORY.json` set | 89 → 86 and 33 → 32: `terrakube-api`, `terrakube-executor`, `terrakube-ui` moved to the LAB (SPEC-0263 TSK-0004, PR #1227) | REUSE with the Terrakube difference |
| T02 HOME selection | `compose-start.py plan --selection HOME` selects 46 targets (`--dev-data-expected on`: 51) over 16 profiles including `n8n-sandbox`; `n8n-sandbox-api`, `n8n-sandbox-runner-1` and the job `n8n-sandbox-certs` are selected; no Terrakube target | v8 Sandbox row CHANGE_REQUIRED is resolved by PR #1213 (TSK-0118, criteria 174 and 175 accepted) | REUSE; v8 Sandbox row closed |
| T02 routes | 45 Traefik routers: 39 Docker label, 6 file provider (`hermes.yml`, `blog-export.yml`, `hermes-webhook.yml`) | Terrakube 3 routers gone, `ollama-api` added (PR #1215) | REUSE with the route difference |
| T02 running | `hy-home-infra`: 57 running, 9 exited (6 provisioning jobs, `n8n-sandbox-certs` exit 0, `comfyui` 143, `pushgateway` 0), 0 unhealthy, 0 outside the root set; every HOME + DEV data service runs; 13 optional services also run (blog-ingestion, crawl4ai with egress and loopback, dozzle, kafbat-ui, kafka-1, kafka-exporter, mailpit, mlflow, redisinsight, storybook, storybook-mcp); no Terrakube container | - | observation only; not a defect or removal claim |
| T03 | v9 package verifier PASS, 26 check groups, 0 failures; structural only | 1,170 checks (v8) → 26 groups (v9 format) | REUSE; SECOND_REVIEW_NOT_RUN kept |
| T04 | 8 Specs, 8 Plans `approved`; 151 Tasks: completed 88, in-progress 33, draft 24, blocked 2, cancelled 2, statusless 2. TSK-0115 to TSK-0120 keep frontmatter `draft` with criteria 171 to 177 accepted | +7 Tasks (TSK-0115 to TSK-0120, SPEC-0263 TSK-0004) | lifecycle mismatch routed to D10 |
| T05 | Criteria 83, 85 (TSK-0046) and 104, 105 (TSK-0052) still `pending` | unchanged | open; D08 and D09 |
| T06 | No service added; no duplicate data owner; Terrakube left HOME by owner decision and is not reintroduced | Terrakube removal | REUSE |

The 13 optional services running outside the HOME selection are recorded, not
changed: whether each stays started is an owner choice outside D01.

###### v9 next prompts

| Prompt | Open item | Precondition |
| --- | --- | --- |
| D02, D03, D05, D06, D07 | Differences only; no input in their scope changed except the image and Renovate updates already merged | None |
| D04 | Airflow 3.4.0 business DAG, cancellation and recovery | None |
| D08 | Criteria 83 and 85 | None |
| D09 | Criteria 104 and 105; n8n runner constant 2.46.6 against TSK-0118 E28 2.43.6 | None |
| D10 | `draft` frontmatter of TSK-0098 to TSK-0120 with accepted criteria; stale Next Owner rows | Runs before D11 and D12 on shared Spec files |
| D11 | Cleanup; keep `d06e12CodeRunner01` until D09 accepts the native replacement | D09 |
| D12 | Final A/B and Git acceptance | D04, D08, D09, D10 results |
| D13, D14 | Held; not a precondition for any other prompt | Owner selection |

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
| E09 | 171 | W187 | method=observation; tool=git; command=git fetch; git rev-parse HEAD origin/main; git status --short; git worktree list | `main` 180bc0eba, 2026-11-27 | PASS | Equal SHAs, clean tree, one worktree | optional | - |
| E10 | 171 | W187 | method=automated; tool=docker compose 5.6.1; command=config -q; --profile '*' config --services; config --profiles; Python3.12.3 counts of rendered restart, hy-home.role and router labels | `main` 180bc0eba | PASS | exit 0; 86 = 67 + 19; 61 profiles; 39 label routers; names equal v9 inventory | optional | - |
| E11 | 171 | W187 | method=automated; tool=Python3.12.3; command=python3 scripts/operations/compose-start.py plan --selection HOME --dev-data-expected off and on | `main` 180bc0eba | PASS | 46 and 51 targets; Sandbox selected; no Terrakube | optional | - |
| E12 | 171 | W187 | method=observation; tool=docker; command=docker ps -a by compose project | HOME host, 2026-11-27 | PASS | 57 running, 0 unhealthy, 0 outside root | optional | - |
| E13 | 171 | W187 | method=automated; tool=Python3.12.3; command=python3 -I dependencies/verify_bundle.py; python3 -m unittest tests.lib.ops.test_workspace_inventory tests.validation.test_workspace_inventory tests.lib.ops.test_workspace_connections | Package v9; `main` 180bc0eba | PASS | 26 groups, 0 failures; 52 tests OK | optional | - |
| E14 | 171 | W187 | method=review; tool=Python3.12.3; command=frontmatter census of docs/03.specs | `main` 180bc0eba | PASS | Census in the v9 pass | optional | - |

##### Resolution Links

None: no row resolves another.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 171 | accepted | E01,E02,E03,E04,E05,E06,E07 | Owner @buenhyden accepted on 2026-11-25 in this chat; the routed items are tracked by their owners (D07 in TSK-0116, D02 in TSK-0117) | @buenhyden |

##### Remaining Conditions

None for criterion171. The routed items stay with the owners listed above;
this Task does not close them. E09 to E14 re-observe the v9 input and do not
change the 2026-11-25 decision.

#### Handoff

##### Promotion Receipt

None: this Task records observation and routing only and promotes no
long-lived rule.

##### Next Owner

The owner chooses the next prompt from the v9 table above; no prompt is
started automatically. The `draft` frontmatter of this Task stays for D10 to
reconcile.

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
