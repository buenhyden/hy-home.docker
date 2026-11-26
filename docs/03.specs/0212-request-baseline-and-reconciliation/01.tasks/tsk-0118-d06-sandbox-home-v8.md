---
title: "D06 v8 Sandbox HOME Selection Task"
version: "0.5.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-26"
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
| Stale "opt-in" comment on the n8n Compose sandbox section | Reworded to "in HOME" with the E25 Compose change; ledger and review hashes re-bound | Done |
| Server B OpenClaw native Ollama provider (`api: ollama`, baseUrl without `/v1`) | PASS (E24) through the B loopback proxy and `ollama-api` | Done |
| JS Code node can generate code from strings (E17) | Fixed (E25) and verified live (E26) | Done |
| Probe workflow `d06e12CodeRunner01` | Kept unpublished in the n8n database for reruns (owner, 2026-11-26) | n8n owner |
| Hermes user config keeps an `ollama-cloud` provider entry (`https://ollama.com/v1`) and `--provider custom -m lfm2.5:8b` answered without reaching local Ollama (E08) | Owner decision 2026-11-26: local and cloud Ollama run as separate providers; the `ollama-cloud` entry stays and HOME Ollama keeps `OLLAMA_NO_CLOUD=1`. The bypass finding stays recorded; user-global config is not changed under repository authority | Owner |
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
  starts with `--disallow-code-generation-from-strings` and allows no
  builtin or external module, but a Code node can still generate code from
  strings (E17, corrected 2026-11-26); the Python runner allows no stdlib or
  external module and blocks environment access. The broker token file is readable by the runner uid,
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

###### Follow-up on 2026-11-26

The owner decided that Hermes runs local and cloud Ollama as separate
providers, asked to rerun E13, to build and run a probe workflow for E12,
and reported that OpenClaw on server B fails with base URL
`https://ollama.hy.home.arpa` (E11). The owner then approved two n8n
restarts for E12 and chose a Basic-auth route with a new credential and a
server B loopback proxy for E11. Work ran on branch `feat/ollama-api-route`
in `.claude/worktrees/ollama-api` from `main` `d9a96ebe9`; brief
`d06-ollama-api-e11` bound the paths before the first edit.

- E13 rerun: an inner container on `runner-no-egress` reached neither
  metadata, the host LAN, the router nor the internet, and `n8n-worker` and
  `mng-pg` did not resolve; it finished in 54 s and cleanup left zero
  containers and 10.3 GB. The earlier 300 s timeout did not recur.
- E12: the probe workflow (Webhook, a JS and a Python Code node) was
  imported with the n8n CLI, published, n8n restarted, and its webhook was
  called from inside the container. Execution 207 was queued as job 207 and
  run by `n8n-worker` through the external runners. JS: `require('fs')`
  blocked, the broker URI not visible, `new Function` allowed. Python: the
  static check rejected `import os` ("Import of standard library module 'os'
  is disallowed"), so the run ended in error and the webhook returned 500.
  The workflow was unpublished and n8n restarted to zero published
  workflows. A first import attempt never received its input and waited
  7 h 22 min; it was stopped and its empty temporary file is gone.
- E17 root cause: the runner's `runCode` and `buildContext` call
  `vm.createContext` without `codeGeneration`, and Node then allows string
  code generation in that context whatever the process flag says. The same
  node binary in the runner image shows the main context blocked, a default
  context allowed and a `codeGeneration: {strings: false}` context blocked.
  `fs` and module loading stay blocked, so the Code node's boundary is the
  module allowlist, not the flag.
- E11 root cause: `https://ollama.hy.home.arpa` sits behind `sso-auth`, so
  an unattended client gets a 302 to Keycloak. The new `ollama-api` router
  accepts only requests with `Authorization: Basic` on inference and lookup
  paths (`/api/chat`, `generate`, `embed`, `embeddings`, `tags`, `show`,
  `version`, `ps`, `/v1/`) through `ollama-api-auth` (htpasswd `INFRA-009`
  from `AI-012` and `AI-013`); model management stays behind SSO
  (POL-0056-R24). The update ledger and the 2026-11-11 reviews were
  re-bound for the three changed Compose files with declared images
  unchanged. The agent cannot read or edit
  `secrets/SENSITIVE_ENV_VARS.md.example`, so the owner adds the three
  template rows, creates the password and hash, recreates Traefik and
  Ollama, and connects server B (runbook OPS-0056 Remote Program Access).

On 2026-11-26 the owner set up the `ollama-api` credential and the server B
proxy; OpenClaw on B answered through `ollama-api` (E24). The owner first
accepted E17 as an upstream limitation, but a required FAIL stays open until a
PASS on the same Check, so the owner chose a fix instead:
`infra/07-workflow/n8n/n8n-runner-vm-hardening.cjs`, loaded by the JS runner
with `--require` and mounted read-only, wraps `vm.createContext` so every
context gets `codeGeneration.strings = false`. n8n's expression engine already
expects code generation to be off in the main context. The probe workflow stays
for reruns.

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
| E12 | 175 | W191 | method=observation; tool=n8n UI; command=- | HOME n8n | NOT_RUN | A real Code node execution with actor, broker and job ID needs the owner; superseded by E16 (webhook run on the same path, owner-approved restarts) | optional | - |
| E13 | 175 | W191 | method=automated; tool=docker inner container; command=probe on runner-no-egress | HOME, 2026-11-25 | NOT_RUN | Container creation on vfs exceeded 300 s | required | - |
| E14 | 175 | W191 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_wiki_preparation_contracts | main 20b188aab+ | PASS | 17 OK | required | - |
| E15 | 175 | W191 | method=automated; tool=docker inner container; command=probe on runner-no-egress | HOME, 2026-11-26 | PASS | Metadata, host LAN, router and internet unreachable; n8n-worker and mng-pg do not resolve; 54 s; zero containers and 10.3 GB after cleanup | required | E13 |
| E16 | 175 | W191 | method=automated; tool=n8n CLI, wget, psql; command=import and publish d06e12CodeRunner01, restart n8n, GET /webhook/d06e12-probe inside n8n, read execution 207 status and probe fields | HOME, 2026-11-26 | PASS | Execution 207 queued as job 207 and run by n8n-worker through the external runners; JS fs blocked and broker URI hidden; Python import os rejected by the static check; unpublished and restarted to zero published workflows | required | - |
| E17 | 175 | W191 | method=automated; tool=node in n8n-task-runner-worker; command=new Function in a Code node and in main, default and codeGeneration strings false vm contexts | HOME, 2026-11-26 | FAIL | Code node and default vm context allow code generation from strings; only main and strings false contexts block it | required | - |
| E18 | 175 | W191 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_compose_baseline_gates.OllamaPortContractTests tests.validation.test_compose_baseline_gates.RouteAuthContractTests tests.lib.supply_chain.test_update_gates tests.lib.supply_chain.test_ledger_rebind | Change on d9a96ebe9 | PASS | Ollama route test errors on main (KeyError ollama-api.rule) and passes with the change; route-auth and 57 supply-chain tests OK | required | - |
| E19 | 175 | W191 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_secret_metadata_sync | Change on d9a96ebe9 | FAIL | 2 failures: INFRA-009 htpasswd path has no row in secrets/SENSITIVE_ENV_VARS.md.example, which the owner adds | required | - |
| E20 | 175 | W191 | method=automated; tool=Python3 venv, bash; command=check-document-metadata.py --mode check-changed and check-active; check-document-links.py --mode all --changed; check-document-corpus-lifecycle.py; check-operations-catalog.py; check-supply-chain-policy.py --check; check-template-security-baseline.sh; check-conftest-policy.sh --mode corpus | Change on d9a96ebe9 | PASS | 0 metadata violations; links pass; lifecycle 0 violations; catalog pass after re-rendering the ollama and traefik inventory rows; supply chain pass; 0 template findings; 45/45 | required | - |
| E21 | 175 | W191 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_secret_metadata_sync | Change plus owner template rows for INFRA-009, AI-012 and AI-013 | PASS | 107 OK together with the Ollama route, route-auth and update-gate suites | required | E19 |
| E22 | 175 | W191 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_secret_catalog_contract | PR #1215 head 4bb792e4b (hosted candidate-core) | FAIL | 2 failures: the new entries pointed evidence_ref at TSK-0118 while the catalog contract requires the SPEC-0204 catalog Task, and AI-012 sat before AI-011 so the rendered view order differed from the template | required | - |
| E23 | 175 | W191 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_secret_catalog_contract | Entries ordered AI-010 to AI-013, evidence_ref on SPEC-0204 TSK-0010 | PASS | 106 OK together with the secret metadata and catalog library suites | required | E22 |
| E24 | 175 | W191 | method=observation; tool=OpenClaw; command=- | Server B through the loopback proxy, 2026-11-26 08:17 to 08:20 KST | PASS | Server A route checks: no credential 302, wrong 401, correct 200, /api/pull 302. Traefik logs 192.168.0.22 on router ollama-api@docker: /api/tags, /api/show and /api/chat 200 (chat 8.5 s with load); Ollama logs the same /api/chat 200 at 23:20 UTC | required | E11 |
| E25 | 175 | W191 | method=automated; tool=Python3 venv, node; command=python -m unittest tests.validation.test_p03_runner_isolation tests.lib.supply_chain.test_update_gates tests.lib.supply_chain.test_ledger_rebind | Change on 61a39d6cc | PASS | New hardening test sees blocked in default and codeGeneration-only contexts and plain code running; the same probe without the module prints allowed; 11 runner tests (1 opt-in native skip) and 57 supply-chain tests OK | required | - |
| E26 | 175 | W191 | method=automated; tool=node in n8n-task-runner-worker; command=new Function in a Code node and in main, default and codeGeneration strings false vm contexts | HOME main 84501d8bd, runner recreated with the hardening module, 2026-11-26 | PASS | Probe execution 211 (job 211, n8n-worker): JS node returns codegen blocked, fs blocked, broker URI hidden; with the runner's launch flags main, default and strings false contexts all block; probe unpublished and n8n back to zero published workflows | required | E17 |

##### Resolution Links

E06 resolves E05; E15 resolves E13; E21 resolves E19; E23 resolves E22; E24 resolves E11; E26 resolves E17.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 174 | accepted | E01,E02,E03,E04,E06 | Owner @buenhyden accepted on 2026-11-25 in this chat after the HOME selection change and its checks | @buenhyden |
| 175 | accepted | E07,E08,E09,E10,E14,E15,E16,E18,E20,E21,E23,E24,E25,E26 | Owner @buenhyden accepted on 2026-11-26 in this chat, conditional on the live E17 rerun passing, which E26 records | @buenhyden |

##### Remaining Conditions

None for criterion174 or criterion175. The items under Left open stay with
their owner.

#### Handoff

##### Promotion Receipt

POL-0078 and the exception register carry the change.

##### Next Owner

Both criteria are accepted. The owners named under Left open carry those items.

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
