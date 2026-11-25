---
title: "D06 v8 Sandbox HOME Selection Task"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-25"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0118"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-25"
---

# D06 v8 Sandbox HOME Selection Task

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

Own criterion174/W190 and criterion175/W191 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply D06 of the lifecycle v8 task prompts: add the n8n Assistant sandbox API
and runner to the HOME selection (D06-T04 item 4), keep the certs job
one-shot, update the privileged exception, and record the D06 items left
open.

##### Inputs and Authority

On 2026-11-25 the user directly requested D06 from
`_workspace/workspace_task_prompts_20261125_lifecycle_v8/` (prompt
`06_ai_ollama_local_cloud_sandbox.md`), limited to that prompt's scope, with
commit, push, PR and merge after checks. The package treats the sandbox API
and runner joining HOME as decided, which conflicted with the POL-0078 row
that kept `n8n-sandbox` out of the default selection (owner decision
2026-11-09) and with the privileged exception that cited the opt-in profile
as a mitigation. Asked in this chat, the owner chose to add the profile to
HOME. Work ran on branch `feat/sandbox-home-selection` in the linked worktree
`.claude/worktrees/sbx` from `main` `20b188aab`; brief `d06-sandbox-home`
bound the paths before the first edit. Direct user authorization is
authority; this record is not.

#### Execution Log

##### Work Performed

###### Change

- POL-0078: `n8n-sandbox` joins the HOME row; the profile row now says it is
  in the HOME selection since the owner decision of 2026-11-25, with certs as
  a one-shot job.
- `infra/common-optimizations.exceptions.json`: the runner's privileged
  exception no longer cites an opt-in profile as mitigation and is re-reviewed
  on 2026-11-25; its recorded impact (a sandbox break-out reaches host-level
  rights, the internet and, through NAT, the host LAN) is unchanged.
- The n8n Compose file is unchanged. A first attempt reworded its section
  comment, which still says opt-in, but the update ledger and the
  2026-11-11 advisory review pin that file's exact bytes; rebinding a dated
  security review to input it never examined would misstate it, so the edit
  was reverted (E05). POL-0078 owns the selection.

###### Verification

The read-only HOME plan grows from 16 profiles and 48 targets to 17 and 51:
`n8n-sandbox-api`, `n8n-sandbox-runner-1` and the job `n8n-sandbox-certs`.
The running runner is privileged as declared, publishes no host port, mounts
no host Docker socket (only its TLS volume, two secret files and its own
Docker data volume), joins only `n8n_sandbox_runner_net` and
`n8n_sandbox_outbound_net`, has 4 GiB, 3 CPU and 4096 pids limits and is
healthy; the API publishes no host port and is healthy. No container was
started or recreated.

###### Left open

| Item | State | Owner |
| --- | --- | --- |
| Stale "opt-in" comment on the n8n Compose sandbox section | Kept; changes with the next reviewed n8n Compose update | n8n Compose owner |
| Server B OpenClaw native Ollama provider (`api: ollama`, baseUrl without `/v1`) | NOT_RUN (E11) | Owner on server B |
| A real n8n Code node run with its actor, broker and job ID | NOT_RUN (E12) | Owner in the n8n UI |
| Inner probe on `runner-no-egress` | NOT_RUN (E13): container creation on vfs exceeded 300 s | D06 follow-up |
| Hermes user config keeps an `ollama-cloud` provider entry (`https://ollama.com/v1`) and `--provider custom -m lfm2.5:8b` answered without reaching local Ollama (E08) | User-global config; not changed under repository authority | Owner |
| D06-T06 tool comparison | Not started: no dataset, owner, rights, time field or goal exists, so no experiment is created (T06 item 2) | Owner names a dataset |

###### D06 runtime checks (criterion175)

On 2026-11-25 the owner accepted criterion174, approved the D06-T03/T04
tests, asked to run D06-T01 and to review D06-T05/T06.

- D06-T01: Ollama 0.40.16, `OLLAMA_NO_CLOUD=1`, loopback port only,
  `MAX_LOADED_MODELS=1`, `NUM_PARALLEL=2`, `MAX_QUEUE=16`. From the n8n
  worker network, `lfm2.5:8b` chat cold-loaded in 29.4 s and answered warm
  in 1.1 s; `embeddinggemma-2:740m` returned 768 dimensions. The Hermes
  Agent v0.23.4 process on server A answered through the `lfm` alias, and
  the Ollama log shows its `/v1/chat/completions` request with 200. A stream
  aborted during load logged 499 and "aborting load"; the next request
  loaded and finished with `stop`.
- D06-T03: the task runner runs as 1000:1000 with a read-only root, all
  capabilities dropped, no-new-privileges, 256 MiB, 256 pids, a 300 s task
  timeout and concurrency 1, on the internal network
  `n8n_worker_runner_net` whose only other member is `n8n-worker`. From the
  runner container only the broker answers; Ollama and `mng-pg` time out,
  and the internet, metadata and host LAN are unreachable. The JS runner
  disallows code generation from strings and allows no builtin or external
  module; the Python runner allows no stdlib or external module and blocks
  environment access. The broker token file is readable by the runner uid,
  but neither runner can load a file module to read it.
- D06-T04: the inner dockerd uses `vfs`; one 920 MB sandbox image occupies
  10.3 GB. An inner container on `runner-bridge` reaches the internet, while
  metadata, the host LAN address and the router time out and HOME service
  names do not resolve. The exception's recorded impact is kept as is.
  Timed-out CLI runs left four of this pass's probe containers in Created
  state and grew the volume to 17.8 GB; they were removed by exact ID,
  restoring zero containers and 10.3 GB with the runner and API healthy.
- D06-T05: SPEC-0204 TSK-0008 (completed) records provenance, rights, ACL,
  deletion and revocation, reindexing and restore for the Wiki preparation
  contract, and its valid and invalid fixtures still pass. No Wiki product
  is built.

##### Blockers and Decisions

The owner chose the HOME selection over keeping the privileged runner opt-in;
the security impact stays recorded in the exception.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 174 | W190 | method=automated; tool=Python3 venv; command=compose-start.py --root "$PWD" plan --selection HOME --dev-data-expected on | Change | PASS | 17 profiles, 51 targets including the three sandbox services | required | - |
| E02 | 174 | W190 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.ops.test_compose_start tests.validation.test_p02_service_contracts tests.validation.test_service_wiring_contracts | Change | PASS | 100 OK | required | - |
| E03 | 174 | W190 | method=automated; tool=Python3 venv, bash; command=check-document-metadata.py; check-operations-catalog.py; check-conftest-policy.sh --mode corpus; check-supply-chain-policy.py --check; check-all-hardening.sh | Change | PASS | 0 violations; catalog pass; 45/45; supply chain pass; all hardening checks passed | required | - |
| E05 | 174 | W190 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.supply_chain.test_update_gates | PR #1213 head f26032a58 (hosted candidate-core) | FAIL | The comment edit changed the n8n Compose hash pinned by the update ledger and the advisory review; the Compose file and ledger were restored to main | required | - |
| E06 | 174 | W190 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.supply_chain.test_update_gates | Compose file and ledger identical to main | PASS | update-gates suite OK | required | E05 |
| E04 | 174 | W190 | method=observation; tool=docker; command=docker inspect n8n-sandbox-runner-1 and n8n-sandbox-api | HOME, 2026-11-25 | PASS | Privileged runner without host port or host socket, two sandbox networks, 4 GiB/3 CPU/4096 pids, healthy; API without host port, healthy | required | - |
| E07 | 175 | W191 | method=automated; tool=docker, wget; command=/api/chat and /api/embed from n8n-worker to ollama:11434 | HOME, 2026-11-25 | PASS | lfm2.5:8b cold load 29.4 s, warm 1.1 s; embedding 768 dimensions | required | - |
| E08 | 175 | W191 | method=automated; tool=Hermes Agent v0.23.4; command=hermes chat -q with -m lfm | Server A, 2026-11-25 | PASS | Reply OK; Ollama log shows its /v1/chat/completions 200; an earlier run with --provider custom -m lfm2.5:8b answered without reaching Ollama | required | - |
| E09 | 175 | W191 | method=automated; tool=curl; command=stream aborted during load, then a new request | Server A loopback, 2026-11-25 | PASS | 499 and aborting load, then 200 with stop | required | - |
| E10 | 175 | W191 | method=automated; tool=docker, node, python inner containers; command=runner reachability and file probes, inner runner-bridge probe, removal of four probe containers | HOME, 2026-11-25 | PASS | Code Runner reaches only the broker; inner container reaches only the internet; cleanup back to zero containers and 10.3 GB | required | - |
| E11 | 175 | W191 | method=observation; tool=OpenClaw; command=- | Server B | NOT_RUN | Native Ollama provider run on server B needs the owner | required | - |
| E12 | 175 | W191 | method=observation; tool=n8n UI; command=- | HOME n8n | NOT_RUN | A real Code node execution with actor, broker and job ID needs the owner | required | - |
| E13 | 175 | W191 | method=automated; tool=docker inner container; command=probe on runner-no-egress | HOME, 2026-11-25 | NOT_RUN | Container creation on vfs exceeded 300 s | required | - |
| E14 | 175 | W191 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_wiki_preparation_contracts | main 20b188aab+ | PASS | 17 OK | required | - |

##### Resolution Links

E06 resolves E05.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 174 | accepted | E01,E02,E03,E04,E06 | Owner @buenhyden accepted on 2026-11-25 in this chat after the HOME selection change and its checks | @buenhyden |
| 175 | pending | E07,E08,E09,E10,E11,E12,E13,E14 | Server A runtime checks pass; the server B OpenClaw run, a real Code node run and the no-egress inner probe are not run | @buenhyden |

##### Remaining Conditions

None for criterion174. Criterion175 needs E11, E12 and E13 resolved and owner
acceptance; the items under Left open stay with their owner.

#### Handoff

##### Promotion Receipt

POL-0078 and the exception register carry the change.

##### Next Owner

The owner decides acceptance and whether to run the left-open D06 items.

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
