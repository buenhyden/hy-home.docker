---
title: "Models, Runners and Wiki Preparation Task"
version: "0.1.15"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-09"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0042"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-02"
---

# Models, Runners and Wiki Preparation Task

## Overview

This draft Task is the bounded P03 evidence and handoff record for SPEC-0212.

### Objective

Implement P03.01–P03.05 as a bounded local source and isolated-test unit.
This Task records model-path, Open Notebook registration, external-runner,
tool-policy and Wiki-preparation evidence. It is distinct from the completed
historical P03 integration task in SPEC-0204 and from the completed offline
Wiki preparation package in SPEC-0204-TSK-0008.

## Inputs and Authorization

The direct user approval of the P03 plan on 2026-11-02 authorizes local source,
documentation, isolated synthetic tests and a normal local logical commit. The
implementation starts from clean commit `ac78f975c9c3` on
`codex/p02-integration-network-auth-valkey`; its source identity is an
observation, not a required future constant. No HOME service, host setting,
real credential, model download, external repository, external workspace,
remote CI or push is authorized.

The selected current contract is local-only: no Ollama-mediated cloud path or
direct-cloud path is enabled, and no automatic fallback is introduced. Open
Notebook source planning targets `gemma4:e2b` for chat and
`embeddinggemma-2:740m` for 768-dimensional embeddings. That selection is not
evidence that either model is locally present, registered, invoked, stored or
available to an operator.

## Work Log

### Issued writer leases

Each writer must re-read the current file fingerprint before editing. A changed
shared path pauses only its dependent slice; it does not authorize a second
writer to overwrite another slice.

| Scope | Writer | Review role | Boundary |
| --- | --- | --- | --- |
| Notebook model-registration utility and its unit tests | `p03_model_impl` (initial) / `p03_model_resume` (current) | independent code/security review | `p03_model_resume` integrates the current correction for `scripts/lib/ops/notebook_models.py`, its CLI/HTTP helper and owned tests. It does not change images, locks, Secret values or shared resource originals. |
| External runner Compose/runner source | `p03_infra_impl` (initial) / `p03_runner_resume` (current) | independent IaC/security review | `p03_runner_resume` integrates the current exact Runner source paths under the existing pre-edit boundary. Preserve declared volumes; remove only unneeded RW service mounts and retain the fixed image UID/GID `1000:1000`. |
| Runner validation source | `p03_runner_qa` (initial) / `p03_runner_resume` (current) | independent QA/security review | `p03_runner_resume` owns the current synthetic runner contract tests and uses synthetic values/owned isolated resources only. |
| Hermes destination-policy source and tests | `p03_hermes_impl` (original) / `p03_tool_fix` (corrective follow-up) | independent security review | `p03_tool_fix` alone integrates the cancellation/process-group corrective patch after the reviewer finding; actual Hermes installation and live policy are P11-owned. |
| This Task, P03 living documents, research, curation and evidence axes | `p03_docs_impl` (initial) / `p03_docs_resume` (current) | independent document review | `p03_docs_resume` integrates current evidence corrections and does not claim source/test/runtime outcomes before receipts exist. |
| DATA-0096 generation and CI registration | `p03_ci_impl` (initial) / `p03_ci_resume` (current) | independent CI review | `p03_ci_resume` generates public data only from validated input; it does not expose private metadata or raw logs. |

Acceptance owner, writer, reviewer, data owner and operational accepter are
separate. P05 owns general queue/notification behavior, P06 secret issuance,
P08 images/locks, P09 common resource originals, P11 Hermes installation and
P12 end-to-end acceptance. A handoff is not an operating authorization.

### Official applicability

The P03 source investigation must recheck the recorded official sources for
n8n task runners and runner hardening, Ollama authentication and local cloud
controls, Open WebUI and Open Notebook configuration, Docker resource limits,
and OWASP SSRF defense. A source page or release record does not prove the
installed product supports an option. Current version-specific product facts,
failed lookup and date uncertainty belong in the public research ledger.

Open Notebook 1.15.0 registration must use its supported API/UI behavior, not
an environment fallback as evidence of saved registration. Its known limits are
explicit: cancellation is not proof that an asynchronous server job stopped;
embedding evidence requires terminal job polling; a shared provider password
is not a tenant ACL; conflicting duplicate credentials/models are rejected;
and null defaults cannot be assumed reversible through the API. A recovery
attempt needs matching SurrealDB data, app SQLite state and encryption key.

### Evidence axes and residual boundaries

Every evidence row distinguishes source, static validation, isolated test,
historical operator acceptance, this execution's operation, credential
rotation, independent restore, hosted CI and final acceptance. Static routes,
fixtures and a successful HTTP response cannot become stored product
registration, live model functionality, installation or recovery evidence.

| Criterion | Work Unit | Current disposition | Required local evidence | Retained residual / owner |
| --- | --- | --- | --- | --- |
| 61 | W66 | SOURCE_READY | Final reviewed model-path contracts and negative local/cloud/fallback tests | Model presence, inference, cost/privacy transfer and operator acceptance remain NOT_RUN. |
| 62 | W67 | SOURCE_READY | Final reviewed registration utility and synthetic persisted-state/terminal-job tests | Native fixture, actual registration, model download and independent restore remain NOT_RUN. |
| 63 | W68 | TEST_RESIDUAL | Runner isolation/denial contracts, source render and bounded normal-JS diagnostic | P09 owns common resource originals; P06 owns token issuance; denial/peer/cancel/recovery, HOME execution and candidate Compose remain NOT_RUN. |
| 64 | W69 | IMPLEMENT_GAP | Tool destination/redirect/DNS/budget and authority-negative tests | P11 owns installed Hermes policy and live delivery. |
| 65 | W70 | REUSE_ACCEPTED | Current Wiki preparation mapping and synthetic rights/ACL/citation/revoke/no-evidence/failure evaluation | SPEC-0204-TSK-0008 remains the completed preparation authority; Wiki runtime is OUT_OF_SCOPE. |

### Implementation Contract

The following bounded contracts define the source work and do not create an
operating acceptance result.

#### P03.01–P03.02: model paths and Notebook registration

Keep local-only Ollama use as the default. Separate local, Ollama-mediated
cloud and direct-cloud URL, credential, model and network contracts. Cloud
paths stay disabled and no implicit retry/fallback crosses a path boundary.
`scripts/operations/notebook-models.py` and its library expose `plan`,
`apply` and `verify`; `plan` is read-only, `apply` is restricted to an owned
isolated fixture, and `verify` reports selection/association without values.

The `--owned-isolated` flag and this Task are structural controls, not an
authenticator. A controller still needs trusted user authorization and an exact
verified owned target before an actual write; P03 does not infer either fact.

Registration is idempotent only for an exact matching provider, credential and
model association. It rejects duplicate or conflicting stored registrations
instead of bulk syncing, deleting other providers or guessing a rollback.
Existing Open WebUI authentication, Chroma/RAG, embeddings and persistence are
preserved. `/health`, a database healthcheck or a mounted directory remains
liveness evidence only.

#### P03.03–P03.04: Runner and tool authority

Retain the external n8n runners, their declared volumes, fixed image UID/GID
`1000:1000` and aligned image/version declaration. Remove only an unneeded RW
service mount; bind required temporary writable paths and use read-only root,
minimum network reach, one concurrent task and existing resource controls; do
not change P09 resource originals. A user Code node must not see broker tokens, other task
data, host files, Docker socket or unapproved egress. Shell/image changes are
not made solely to claim hardening.

Tool policy validates destination before credential read. The Hermes tool
accepts exactly the approved POST webhook endpoint and rejects userinfo,
alternate host/path/port, query/fragment, redirect, DNS rebinding and any
model/retrieved instruction that tries to expand authority. It retains the
existing 3 retries, 15-second request limit, 60-second total limit, 4MiB
request and 1MiB response limits. Actual Hermes installation stays P11-owned.

#### P03.05: Wiki preparation

Reuse SPEC-0204-TSK-0008 and its offline contracts. Record the current source
mapping and a small synthetic evaluation set for rights, ACL, citation,
revocation, no-evidence and failure/recovery results. Do not create a Wiki
application, DB, search engine, crawler, model store, external workspace or
LAB runtime. The old architecture's cloud fallback, obsolete embedding tag and
bind-mount claims must be corrected only where current tracked source proves a
different contract.

### Fixture parity and wrong-token refusal (2026-11-08)

The `wrong_token_registration` residual is a wait bound, not a missing refusal.
In the pinned `n8nio/runners` image, `task-runner-launcher` exchanges its auth
token for a grant token through `retry.LimitedRetry` (60 seconds, 5 seconds
apart). Each failed attempt is logged only at DEBUG. When the retries run out,
the launcher logs at ERROR `request to fetch grant token received status code
403`. The binary contains those strings, and the upstream
`n8n-io/task-runner-launcher` source (`internal/http/fetch_grant_token.go`,
`internal/retry/retry.go`) produces them. The fixture waited 30 seconds, so the
ERROR line could never appear. The bound is now 90 seconds, and a regression
checks that the real error line maps to `http_403`.

Two of the five fixture differences are removed. The fixture runner network now
matches HOME's shape: it is internal, uses the isolated IPv4 gateway mode, and
takes the first free `/24` in `10.251.0.0/16` with its upper half as the dynamic
range. The worker joins it at `.2`, and its broker binds only that address
(`N8N_RUNNERS_BROKER_LISTEN_ADDRESS`), with the readiness probe on the same
address. `NativeFixture` gains per-role network options and fixed attachment
addresses; other callers are unchanged.

Three differences stay, by design: the shared `ctl` network, the fixture-only
tmpfs mounts and the resource caps. None of them crosses the runner boundary
under test. A native rerun is needed to turn the wrong-token row into PASS
evidence; it is NOT_RUN until approved.

### Native rerun after fixture parity (2026-11-08)

With approval, the rehearsal ran at merged `b62de97d7` (attempt
`opsflow-native-a2ed7b00be6e8fd3a2c1587b`) and FAILED after 539 seconds: the
worker broker never became ready. Its probe returned `target_rejected`, because
the shared `node_status_probe` admits only a fixed URL set and the change above
moved the readiness URL from `127.0.0.1` to the fixed runner address without
admitting it. The unit tests mocked `wait_until`, so they never ran the probe.
Cleanup PASS with zero labelled containers and networks.

The fix admits only `http://10.251.<octet>.2:5679/healthz`, the broker's fixed
address on a pool `/24`. A new regression accepts two such URLs and rejects the
HOME subnet, `.3`, an out-of-range octet, another port and another path; two of
its cases fail on the unfixed helper. The pre-merge rerun from that branch
(attempt `opsflow-native-eb34b488ee66c95ee3cb00ae`, 816 seconds) passed with
`native=PARTIAL`: every denial, timeout, cancel and restart scenario PASS, and
`peer_nonbroker_port` and `wrong_token_registration` now PASS as well. The wrong
token produced `http_403` in the runner log within the 90-second bound, with no
registration. `fixture_differences` lists only the three by-design entries.
Candidate Compose, paired network, manual worker and private workflows stay
NOT_RUN. Cleanup PASS with no re-sweep removal and zero residue.

### D06 model consumers and Open WebUI drift (2026-11-08)

A direct user request on 2026-11-08 re-ran the model, runner and Wiki scope as
D06 on `main` `2f86dd9e3`, Docker context `default`. Ollama runs with
`OLLAMA_NO_CLOUD=1` and eight local models. Their capabilities are completion
(`gemma4:e2b`, `gemma4:e4b`, `lfm2.5:8b`, `bonsai-2:9b`, `minicpm-v4.6:1b`),
embedding (`embeddinggemma-2:740m`) and decision (`d1:3b`, `tev1:0.8b`).

**Actors (T01).** Only Open WebUI, Open Notebook (stopped) and `n8n-worker`
wire Ollama in source; MLflow, Airflow, ComfyUI and Crawl4AI carry no LLM
connection, and none is added. From inside each container at 09:01 UTC:
`n8n-worker` listed eight models, embedded with `embeddinggemma-2:740m`
(768 dimensions) and generated with `gemma4:e2b` (HTTP 200, 24 s including
the load); `n8n` main and the worker runner could not reach `ollama:11434`.
`tev1:0.8b` refuses generation as a decision-only model.

**Cloud (T02).** A request for `gpt-oss:120b-cloud` through local Ollama
returned `403 ollama cloud is disabled: remote model is unavailable`. Open
WebUI, however, stored `openai.enable = true` with
`https://api.openai.com/v1` and an empty key; it sits on the non-internal
`ai_net` and `edge_net`. Its saved `rag.embedding_model` was
`qwen3-embedding:4b`, a model that left Ollama about two weeks earlier, so
any RAG upload would fail to embed; there were no files and no knowledge
entries. Open WebUI v0.12.0 reads a saved `config` row before the Compose
value (`Config.get`), so a Compose change alone does not reach either row. The
owner chose the installed `embeddinggemma-2:740m` and disabling the OpenAI
path. Compose now sets both, `OpenWebuiLocalModelContractTests` failed before
the change, and GDE-0057 and the Open WebUI README say the saved rows change
together with Compose. The HOME row update follows the merge.

**HOME apply after #826 (`70e7788fb`), 12:33Z.** With the owner's approval:

1. A SQLite backup API copy of `webui.db` was written to
   `webui.db.pre-d06-20261108` in the same volume, mode 0600. Its integrity
   check returned `ok`, with 368 config rows.
2. In one transaction, `rag.embedding_model` was set to
   `"embeddinggemma-2:740m"` and `openai.enable` to `false`; each update
   changed one row.
3. A dry run showed that only `open-webui` would be recreated. Then
   `docker compose up -d --no-deps open-webui` recreated container
   `30f9657dffca` from image `sha256:3a4f953b…` (`v0.12.0-cuda`), healthy.

Results:

- **Settings.** The environment now carries `RAG_EMBEDDING_MODEL=embeddinggemma-2:740m`
  and `ENABLE_OPENAI_API=false`, and the saved rows hold the same values, so
  `Config.get` resolves to them whichever source it reads.
- **Embedding.** From the container, Ollama returns a 768-dimension embedding
  for `embeddinggemma-2:740m`.
- **Logs.** Since the restart the log has no `api.openai.com` or OpenAI error
  line.
- **NOT_RUN.** No in-app RAG upload ran, because it needs a user session. An
  attempt to import `open_webui.config` in the container printed nothing.
  No documents needed re-embedding: there were 0 files and 0 knowledge bases.
- **Rollback.** Stop `open-webui`, copy `webui.db.pre-d06-20261108` back over
  `webui.db` (removing `-wal`/`-shm`), revert #826 and recreate.

**Other items.** T03: the runner sandbox native rerun passed earlier on
2026-11-08 (criterion 63 rows above). T04: no n8n agent workflow is active
(the only active workflow is Hermes Blog Ingestion), so there is no n8n agent
tool to scope; the Hermes agent's own tool policy belongs to SPEC-0265.
T05: the Wiki preparation stays REUSE_ACCEPTED (criterion 65). T06: no
evaluation data set, owner or baseline exists, so the comparison is BLOCKED
until those are named.

### D06 T06 evaluation resume conditions (2026-11-09)

The T06 contract covers search, vector and graph stores, the crawler, image
generation and MLflow, and says that without real data the outcome names the
needed data, owner and resume conditions instead of a completed evaluation. A
read-only HOME census found no evaluable data:

- Qdrant holds 0 collections and 0 vectors.
- Open WebUI holds 0 knowledge bases, 0 files and 1 chat.
- MLflow holds 2 runs, in `hyhome-acceptance` and `Default`; no evaluation
  experiment exists.
- Crawl4AI logged no crawl request in 72 hours and no ComfyUI output was found.
- Neo4j, OpenSearch and Open Notebook are stopped or not selected on HOME.

Twelve Hermes `report.md` files dated 2026-11-07 to 2026-11-09 are the only
time-ordered corpus. Three days are too few for a time-based split, and their
rights and personal-data review has no owner.

T06 stays BLOCKED. It resumes when the owner names (1) the tool question to
decide, (2) a versioned data set with its rights and personal-data review, (3) a
data owner, and (4) a baseline with a time-ordered split, and when an MLflow
experiment is designated for the results. No comparison was run.

### D06 T06 owner direction and Open WebUI Qdrant (2026-11-09)

The owner set the T06 direction on 2026-11-09: use Qdrant as the Open WebUI
vector store, run an MLflow evaluation of the Ollama models, add Crawl4AI as a
fallback for the Hermes source collection, keep Neo4j on hold, and stop ComfyUI
(stopped on HOME the same day; a HOME selector start would start it again, because
the `ai` profile includes it).

Open WebUI now sets `VECTOR_DB=qdrant` over `ai_net`. The entrypoint loads the key
from `QDRANT_API_KEY_FILE`, because v0.12.0 reads `QDRANT_API_KEY` only from the
environment. Open WebUI held 0 knowledge bases and 0 files, so nothing migrates.
It receives the Qdrant read-write key (AI-008); Qdrant offers only that key and
the read-only one. The HOME apply is a separate approved step.

### Open WebUI Qdrant HOME apply (2026-11-09)

With owner approval, `open-webui` was recreated on `main` `294ad4df8`. It reported
unhealthy until application startup finished after about three minutes, then
healthy; the 15-second start period is short for this image. A probe through the
Open WebUI vector client inserted two synthetic documents with real 768-dimension
Ollama embeddings, returned the matching one first, and deleted its collection.
The shared `open-webui_knowledge` collection now exists and holds no probe data
from the failed earlier attempt. File upload and answer generation in the UI were
not exercised. ComfyUI is stopped and, per the owner, leaves the `ai` profile.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Issued baseline and leases | 61 | W66 | `git status --short`; `git rev-parse --short=12 HEAD`; governing source/Task readback | Empty initial worktree; `ac78f975c9c3` | PASS | Inputs and Authorization; Issued writer leases; shared baseline also bounds W67–W70 without accepting them | required | - |
| Initial model-path attempt | 61 | W66 | Earlier scoped unittest, trace and Ruff receipt | Earlier synthetic loopback fixtures and protected synthetic password file | PASS | 2026-11-02: 21 PASS in 4.102 seconds for CLI `39483be42b3894d483df344fcc03a72e0158bf3f3e55ba7f1c57aba68be70979`, core `8af2e895d97191bed15e745430fbf09d75ec2b84b4ed2c22330fc2766a7735c1`, HTTP `42f89d0a2ae1c247ac3460b8c44e270b2a76251f2f477a362365b083122176b7`, unit test `c731c5f8770070196482325d6b2a5205ba77996a1483cc2cde156a636c63666e`, validation `b72b55b51c311fcb57ee750edaa800e10750a1d057290b057579586e9de5005c`. It is historical attempt evidence only. | optional | - |
| Prior reviewed model-path packet | 61 | W66 | Independent production code review and isolated suite | Prior CLI/core/HTTP/policy source and owned synthetic fixtures | PASS | `p03_code_review`, 2026-11-02: 48/48 isolated tests PASS in 7.196 seconds; reviewed CLI `13eaef9e4a0613ca9c034b334358249efbb7ab0bdc6aa44799d68f571fc61c10`, core `0454e2894a2495851ac95cd0021618aca735bfbda29b0f8495343df647f28b22`, HTTP `87a16f423e3bdc6e5650f858095f72deb161f6eb90ae98a153134467e622bbaf`, policy `dfe205b314113fe3604e25bc0d6101a0338b33bf0a65bf7b45cd605a8c55842f`, core tests `77041f1962f1c06373cb34e248a056cb0009d82d39ca5cd940dc2d2ac581fa52`, and HTTP/CLI tests `27a7b78407c782f07fbe1633ba1132005eeec97dc0d2b14810939331928040e2`. It is a prior frozen source packet; later exact-integer-dimension changes require a new code review. | optional | - |
| Prior reviewed Notebook registration source packet | 62 | W67 | Independent production code review and isolated suite | Prior registration CLI/core/HTTP/policy source and owned synthetic fixtures | PASS | `p03_code_review`, 2026-11-02: the same reviewed 48/48 isolated suite and prior exact source packet. It proves bounded synthetic registration/conflict/readback behavior only and is superseded for current acceptance by the exact-integer-dimension source delta. | optional | - |
| Current final model source review | 61 | W66 | Independent code review of final exact-integer-dimension source and tests | Frozen current owner packet | PASS | `p03_code_review`, 2026-11-02: APPROVED with no remaining finding. Production core suite 26/26 PASS; formatter/linter and diff check PASS. Reviewed CLI `13eaef9e4a0613ca9c034b334358249efbb7ab0bdc6aa44799d68f571fc61c10`, core `0f608559560a84973bf344554d8421df95484c90fd46566e042a2eaa075cf922`, HTTP `87a16f423e3bdc6e5650f858095f72deb161f6eb90ae98a153134467e622bbaf`, policy `dfe205b314113fe3604e25bc0d6101a0338b33bf0a65bf7b45cd605a8c55842f`, core tests `89241a8d24a490a805549419cbab18491a279e68e589164fda40e33a3960881c`. Synthetic source/isolated scope only. | required | - |
| D06 HOME model actors and cloud refusal | 61 | W66 | In-container calls from each n8n actor and a cloud-model request | HOME Ollama, `n8n`, `n8n-worker`, worker runner, 2026-11-08 | PASS | Worker: 8 models, 768-dim embedding, `gemma4:e2b` generation 200; main and runner cannot reach Ollama; cloud model 403 with `OLLAMA_NO_CLOUD=1` | required | - |
| D06 T06 data census | 65 | W70 | Read-only Qdrant metric, Open WebUI database, MLflow API, Crawl4AI log and Hermes report census | HOME, 2026-11-09 | NOT_RUN | Evaluation BLOCKED: no evaluable data set, owner or baseline; resume conditions in D06 T06 evaluation resume conditions. | required | - |
| Open WebUI Qdrant HOME apply | 65 | W70 | `open-webui` recreate, health and vector-client index, search and delete probe | HOME, `main` `294ad4df8` | PASS | Healthy after a 3-minute start; correct top result; probe collection removed. UI file flow NOT_RUN. | required | - |
| Open WebUI Qdrant source | 65 | W70 | `test_openwebui_oidc_entrypoint` RED then GREEN and root render | Compose, entrypoint and AI-008 catalog consumer | PASS | 4 new assertions failed before and pass after; live indexing NOT_RUN. | required | - |
| Open WebUI Qdrant CI | 65 | W70 | GitHub `candidate-quality` on #840 | Runs 42547867536 and 42549318802 | FAIL | Service inventory was stale, then `QDRANT_API_KEY_FILE` lacked a secret-file support row. | required | - |
| Open WebUI Qdrant CI rerun | 65 | W70 | GitHub `candidate-quality` on #840 | Inventory refreshed; support row added | NOT_RUN | Awaiting the rerun; the failing checks pass locally (254 tests OK, 31 skipped; operations catalog PASS). | required | - |
| D06 Open WebUI saved model settings | 61 | W66 | Read-only `webui.db` `config` rows against the installed models | Open WebUI v0.12.0, 2026-11-08 | FAIL | `rag.embedding_model` names absent `qwen3-embedding:4b`; `openai.enable` true with `api.openai.com` and an empty key; 0 files, 0 knowledge | required | - |
| D06 Open WebUI local-model source | 61 | W66 | `OpenWebuiLocalModelContractTests` RED then GREEN | Compose `embeddinggemma-2:740m`, `ENABLE_OPENAI_API=false` | PASS | Failed on the old model, passes after; HOME row update follows the merge | required | - |
| D06 Open WebUI saved model settings recheck | 61 | W66 | Read-only `webui.db` `config` rows against the installed models | Open WebUI v0.12.0 after the HOME apply, 2026-11-08 12:33Z | PASS | `rag.embedding_model` is installed `embeddinggemma-2:740m`; `openai.enable` false; backup kept as `webui.db.pre-d06-20261108` | required | D06 Open WebUI saved model settings |
| D06 Open WebUI HOME apply | 61 | W66 | Row update, `--no-deps` recreate, health, embedding call and log check | Merge `70e7788fb`; container `30f9657dffca`; image `sha256:3a4f953b` | PASS | Healthy; env and rows agree; 768-dim embedding; 0 OpenAI log lines; in-app RAG upload NOT_RUN | required | - |
| Current final Notebook registration source review | 62 | W67 | Independent code review of final exact-integer-dimension source and tests | Frozen current owner packet | PASS | `p03_code_review`, 2026-11-02: same approved final packet and 26/26 production core suite; exact-integer dimension input is now enforced. Native product fixture, real registration, model invocation and restore remain separate NOT_RUN axes. | required | - |
| Notebook native census | 62 | W67 | Owned native Notebook application fixture | Exact pinned SurrealDB 2.7.0 digest unavailable; pull forbidden | NOT_RUN | The exact Notebook digest is cached; Docker context is default and engine is 29.9.2, but the required SurrealDB digest is absent. No pull or Notebook fixture resource acquisition occurred. This does not affect the separate Worker native rehearsal. | required | - |
| Worker-model native queue rehearsal | 62 | W67 | `env -u DOCKER_HOST -u DOCKER_CONTEXT -u DOCKER_TLS_VERIFY -u DOCKER_CERT_PATH -u DOCKER_CONFIG P03_WORKER_MODEL_NATIVE_REHEARSAL=1 OPSFLOW_N8N_NATIVE_IMAGE=sha256:1fda18a541144ae5519ac97bcaffa4e24fad0e71d424606d230464bec8fce153 OPSFLOW_N8N_NATIVE_CONTEXT=default python3 -m unittest tests.validation.test_p03_models_native.WorkerModelQueueNativeTests` | Cached pinned images and controlled synthetic Ollama; no live credential/model service | PASS | Exit 0; 1/1 PASS in 378.496 seconds. It verified Main→Valkey→Worker dispatch, Worker-loopback controlled-Ollama chat request, exact execution/event association and persisted readback after Worker stop. Source/test fingerprints: worker `4ca3f96caf470a2fa68197b14456057784717af0b71e66e0e3fac475802bf9d0`, native test `4531d811c7a9009bfbcab27a5dea315f47463927da17bee7ac465529efa5849d`, API adapter `90c4a86b240ddc6248027f5a188c1f0096bb39bedcd2b66769c79598a9fc43f6`. No real-model inference is claimed; post-run owned containers, networks and temporary directories were all zero. | required | - |
| Runner source/static review | 63 | W68 | Focused static source contracts and independent IaC review | Frozen Compose/launcher/Notebook source and public validation helpers | PASS | Independent post-change IaC review: root Compose `44effd451ffd74ba718587ffe7539d18f68c181b8a71debc9fa819bfe1e6b6e3`, n8n `63c92c3175c49cdd6610b5fb25f96cee7800fb7b67c8811ccb8d8008b384470e`, launcher `ea2779cdebf547308c515770d354f6fa7ccf76e7712beff4a3636d307140c6ed`, Notebook `9b103c904679a7f03c6659876740d5321efd1324f995c8fc55cdc6a59edd531d`; focused source tests 13 PASS + one explicit native opt-in SKIP in 0.469 seconds and diff check PASS. This is bounded source/static evidence only. | optional | - |
| P03 Runner owned native scenario | 63 | W68 | Exact cached images, owned Main/runner fixture and REST execution operation | No HOME service, credential or stored workflow | FAIL | 2026-11-02: after 259.016 seconds the owned fixture reached Main liveness/readiness and runner AppArmor enforce, seccomp 2 and NoNewPrivs 1, then the REST execution operation failed before the first Code scenario. Cleanup passed with zero residual resources. This is an isolated scenario failure/`TEST_RESIDUAL`, not a candidate Compose or HOME result. Credential/proc/host/socket/nonbroker/cancel/restart/manual-Worker/candidate-Compose/private-workflow probes remain NOT_RUN. The raw-only response theory is superseded; the final source accepts raw or exactly one exact-ID `data` envelope with string flatted data, but that correction has not been rerun. | required | - |
| P03 Runner interim isolated diagnostic | 63 | W68 | Rerun exact owned scenario after persistence correction | Exact cached images and owned fixture only | ERROR | Exact execution identity matched `1/1`; response had one `data` envelope with string flatted data, then the first normal JavaScript reached terminal `ERROR`. This was later identified as a short-timeout fixture artifact; it is retained as a historical diagnostic, not a candidate Compose/HOME failure. Cleanup passed with zero owned container, network and temporary-resource residue. It preserves the official `--disallow-code-generation-from-strings` flag; the prior removal inference was false and superseded. | optional | - |
| P03 Runner final normal-JS diagnostic | 63 | W68 | Root-authorized owned normal-JS-only diagnostic | Exact cached images and owned fixture only | PASS | At task timeout 300 seconds, request timeout 330 seconds, grant 120 seconds and idle timeout 0, exact execution ID matched `1/1`, the response had one `data` envelope with string flatted data, terminal status was success and no error category appeared. Cleanup passed with zero owned container, network and temporary-resource residue. Final runner test hashes: isolation `173a22374c55f3e0282a67412dae8e7ad53ebbfac314284eae039381aa17cda2`, helper `cdbb9a457fee7925f8b64a5ac740f5f4f5559e77d6d42d47ceecba6a260e8e28`, boundary `32d4e303c2f05f6d6bb88229c79b951e961551b42c8dc86e308c0df0516e872a`, consumer `a75262b0925fe66eecdc242f37098285f2c2a6e1f87d991da265e9ab9d8c316b`. It does not resolve the broader failed native scenario; denial/peer/cancel/recovery, candidate Compose and Worker/private compatibility remain NOT_RUN. | required | - |
| P03 Runner full application rehearsal | 63 | W68 | Synthetic Main/broker/application-control rehearsal | Owned synthetic fixture; no HOME credential, service or stored workflow | ERROR | Elapsed 345.371 seconds. Normal JavaScript/Python output assertions reached the first expected module denial, but its per-scenario receipt was not serialized before abort. The terminal `javascript_module_denied` result is only safely classified `class=other`, `category=unclassified`; the strict gate stopped. Later denial, controlled timeout, ancestor/peer, cancel and restart scenarios are NOT_RUN. Kernel controls were true; cleanup passed with retained/external residue zero. Frozen hashes: isolation `06da0caff4c9c9136d3706ba007c77c31df21a07814d5c51adf8f526f89aa008`, helper `50f6ed699d70e843c8c17a79aec4c7d4238e045da329d99aa60d916108fe20a2`, boundary `4125d3657db81e40b1d366a8e4100cfede9381ae4a84828f7a7cc559eb7044b3`, consumer `a75262b0925fe66eecdc242f37098285f2c2a6e1f87d991da265e9ab9d8c316b`. Fixture is non-equivalent; candidate Compose, manual Worker, paired network and private workflows remain NOT_RUN. | required | - |
| Runner receipt-persistence source fix | 63 | W68 | Static runner receipt contracts | No Docker invocation; native execution intentionally not retried | PASS | The independently approved source-only fix persists immutable completed-stage copies, initializes later stages NOT_RUN, preserves unknown denial as FAIL/unclassified/attributed=false, and does not weaken the classifier. Static 21=20 PASS+1 native skip in 0.563 seconds; CI adapter exit 0 matches. Hashes: helper `bb40ff19fcf80cb34e0ab7123bb575697eba9e280bca40b412f504a1b6488626`, boundary `71267b8b967d59f649581e3abb0162d78733ef7609d74238ba59bb2b0d416d18`, isolation `06da0caff4c9c9136d3706ba007c77c31df21a07814d5c51adf8f526f89aa008`, consumer `a75262b0925fe66eecdc242f37098285f2c2a6e1f87d991da265e9ab9d8c316b`. Historical native ERROR remains; current post-fix native is NOT_RUN. | required | - |
| Runner outcome-module style split | 63 | W68 | Static current Runner source contracts | Pure move only; no Docker invocation | PASS | Current source moves unchanged value-free classifiers into `_p03_runner_outcomes.py`; the helper reexports the same objects and no cycle, default, timing, category or acceptance behavior changes. Independent suite: 22 total, 21 PASS and one native skip; coverage outcomes 98%, helper 83%, boundary 99%, consumer 96%. Hashes: outcomes `f56803a167a42892ea0fcd0bec8026c1d1f9615ee51ed7f04fe58df76db34fa6`, helper `10fbf43307cf72d3a1fff6f42dfe5f32c68ab4466be13e6bd6d27784c0f979b4`, boundary `120ab7c919d1299b0cca28efebb7f71e743444aea9423fd122f9467150b2a076`, isolation `06da0caff4c9c9136d3706ba007c77c31df21a07814d5c51adf8f526f89aa008`, consumer `a75262b0925fe66eecdc242f37098285f2c2a6e1f87d991da265e9ab9d8c316b`. Current native remains NOT_RUN. | required | - |
| P03 Runner post-fix native rehearsal | 63 | W68 | Synthetic Main/broker/application-control rehearsal after the receipt-persistence fix | `main` `279d23d39`; reviewed n8n image `sha256:1fda18a5…`, runner `sha256:3168a82b…`, both cached; owner approval 2026-11-08; no HOME service, credential or stored workflow | FAIL | Attempt `opsflow-native-0ac6ab2aff5713cc94d7a98b`, 2026-11-07T20:17:47Z–20:25:56Z, 487.902 seconds. Main liveness and readiness 200. `javascript_ok` and `python_ok` PASS; `javascript_module_denied` FAIL with terminal status `error`, `error_class=unknown`, `error_category=unclassified`, `attributed=false`, and the strict gate stopped (`terminal denial was not safely attributed`). The receipt now keeps each completed stage, so the persistence fix holds. The 18 later scenarios, candidate Compose, manual Worker, paired network and private workflows are NOT_RUN. Cleanup PASS with zero residual containers and networks. | required | - |
| Runner denial attribution diagnosis | 63 | W68 | Static read of the classifier and the pinned runner image | `main` `cf2ab5798`; runner `sha256:3168a82b…` inspected offline with `--network none`; owner decision 2026-11-08 to diagnose statically first | PASS | Cause of the post-fix FAIL: the JS runner denies `require('node:fs')` with `DisallowedModuleError` and the text `Module '<name>' is disallowed` (`js-task-runner/errors/disallowed-module.error.js`), and the Python runner uses `Import of standard library module '<name>' is disallowed`, `Import of external package '<name>' is disallowed` and `Relative imports are disallowed.` (`constants.py`). None matched the three `module_access_denied` needles, so the classifier returned `unclassified`. The runner enforced the denial; the fixture could not name it. Further finding, not changed: the Python runner removes `open` from builtins by default (`BUILTINS_DENY_DEFAULT`), so the four Python file scenarios will end in `NameError`, and `javascript_candidate_secret_file_denied` will stop at the module denial before any file read; their allowed categories are filesystem-only. | required | - |
| Runner denial classifier source fix | 63 | W68 | `test_runner_import_denials_are_attributed_to_module_access` before and after the needle change | `main` `23a6b7983` then this branch | PASS | Owner-approved 2026-11-08. RED: 4 failures (all four runner texts `unclassified`). After adding `module '`, `import of external package` and `relative imports are disallowed`: `test_p03_runner_boundaries` and `test_p03_runner_isolation` 21 tests OK, 1 native skip; the name-access and `open` texts stay outside `module_access_denied`. Hashes: outcomes `83f6926eb3f206c86564c2ec61a2879aed8c3397f323683d079e2daeef832412`, boundary `9a14ec7de589a378aa9487e75976302bb98fcb6a64b416598e0f6c89705bb7a0`. Native rerun NOT_RUN. | required | - |
| Runner earlier-layer file denial source change | 63 | W68 | `test_earlier_runner_layer_denials_count_for_file_scenarios` before and after | `main` `eec8313e6` then this branch | PASS | Owner decision 2026-11-08: a file probe refused one layer early counts as denied. New category `builtin_denied` (`name 'open' is not defined`); the four Python file scenarios and the ancestor environment probe accept it, and `javascript_candidate_secret_file_denied` accepts `module_access_denied`, each besides the two filesystem categories. Other scenarios unchanged. Trade-off recorded: these scenarios no longer prove mount or permission isolation by themselves. RED: 1 failure; after: `test_p03_runner_boundaries` and `test_p03_runner_isolation` 22 tests OK, 1 native skip. Hashes: outcomes `1f149de62bd983d32661b033256ba628c013fa4b93aa8591ebd669af603c2c2a`, fixture `ef4cf2ccdccbfdfd910f44466f3caf69c8ff23f0e6213c78748aede22c81ef7f`, boundary `e59fac16e5360759e23ac89eff162e020790a1d3ac159c75618003757e4c91dd`. Native rerun NOT_RUN; approved for after merge. | required | - |
| P03 Runner native rehearsal after the denial fixes | 63 | W68 | Synthetic Main/broker/application-control rehearsal | `main` `6d942a7eb`; same reviewed images, both cached; owner approval 2026-11-08 | FAIL | Attempt `opsflow-native-3d6a3e38b9fdb288bd3d38d5`, ended 2026-11-07T23:43:36Z, 465.455 seconds, unittest exit 1. `javascript_ok` and `python_ok` PASS; `javascript_module_denied` now PASS (`module_access_denied`, attributed); `javascript_environment_denied` FAIL (`error_category=unclassified`, `attributed=false`) and the strict gate stopped; `wrong_token_registration` TEST_RESIDUAL; 16 later scenarios NOT_RUN. Cleanup PASS, zero residual containers and networks. | required | - |
| Runner environment denial attribution fix | 63 | W68 | `test_runner_without_process_global_is_attributed_to_environment` before and after | `main` `6d942a7eb` then this branch | PASS | Static read of the runner image (`--network none`): `js-task-runner.js` `buildContext` gives the sandbox no `process` global, so `process.env.<name>` fails with `ReferenceError: process is not defined` and no value is read. Added the needle `process is not defined` to `environment_access_denied`. The same read found the timeout text `Task execution timed out after N seconds`, which `timed out` already matches, and the peer, cancel and restart steps use no attribution gate. RED: 1 failure; after: 23 tests OK, 1 native skip. Hashes: outcomes `7d5f578938c0dbf422378582d0fef1c22dd71e14cb69b6043abac640b8dbc94e`, boundary `dbfa354475e3583c64fdaf6578945b63a7ab50b624cca11729360f2e4999368e`. Native rerun NOT_RUN. | required | - |
| P03 Runner native rehearsal setup under host load | 63 | W68 | Synthetic Main/broker/application-control rehearsal | `main` `a7a6e282c`; same reviewed images; owner approval 2026-11-08 | ERROR | Attempt `opsflow-native-62c01101f117937c3530c8ec`, 170.276 seconds, ended 2026-11-08T00:12:00Z, unittest exit 1, stopped in fixture setup at `secret-prep` with `owned container identity is ambiguous`; no scenario ran. Host 5-minute load was 16.9. The receipt reported `cleanup: PASS`, but the `secret-prep` container (state `created`, never started) remained: `docker run` completed after the fixture's identity checks, so cleanup never adopted it. Its bound temporary secret directory was already removed. The next approved attempt refused to start (`an owned native attempt already exists`, 0.544 seconds); the container was inspected and removed by exact name and attempt label. Fixture defect recorded, not changed: cleanup does not sweep containers it failed to adopt. | required | - |
| P03 Runner native rehearsal after the attribution fixes | 63 | W68 | Synthetic Main/broker/application-control rehearsal | `main` `a7a6e282c`; same reviewed images, both cached; owner approval 2026-11-08 | PASS | Attempt `opsflow-native-b675571b1b5b82639cdddc46`, 870.315 seconds, ended 2026-11-08T00:32:01Z, unittest exit 0, receipt `native=PARTIAL`. PASS: `javascript_ok`, `python_ok`, `javascript_module_denied` and `python_module_denied` (`module_access_denied`), `javascript_environment_denied` (`environment_access_denied`), the four Python file scenarios and `ancestor_environment_probe` (`builtin_denied`), `javascript_candidate_secret_file_denied` (`module_access_denied`), `timeout` (`controlled_workflow_timeout`), `cancellation` and `restart_next_good_task`. TEST_RESIDUAL: `peer_nonbroker_port` (error, unclassified; not reachable) and `wrong_token_registration` (`NOT_OBSERVED_WITHIN_3S`). NOT_RUN: candidate Compose, paired candidate network, manual Worker actor and private workflow compatibility. `fixture_equivalence=NON_EQUIVALENT` (shared internal control network, fixture tmpfs, fixture resource caps). Cleanup PASS; zero labeled containers and networks afterwards. | required | - |
| P03 Runner HOME apply | 63 | W68 | Recreate `n8n`, `n8n-worker`, `n8n-task-runner` and `n8n-task-runner-worker` with the root Compose and `docker-compose.ollama-local.yml` | `main` `53880ad86`, HOME; owner approval 2026-11-08 | PASS | Before (`~/storage/backups/spec0212-w68-home-20261108/pre-state.txt`): broker `0.0.0.0` on main and worker, both runners on the shared `n8n_net`; no execution activity in the previous 10 minutes. A `--dry-run` recreated only the four containers and created only `n8n_main_runner_net` and `n8n_worker_runner_net`; the existing `hy-home-infra_n8n_ollama_net` (`internal=true`) was kept. Applied 00:54:53–00:56:48 UTC; all four `healthy`. After: `n8n-task-runner` only on `n8n_main_runner_net` (`10.250.22.128`), `n8n-task-runner-worker` only on `n8n_worker_runner_net` (`10.250.23.128`); main at `10.250.22.2`, worker at `10.250.23.2` with broker `N8N_RUNNERS_BROKER_LISTEN_ADDRESS` set to those addresses (SPEC-0267 W1 decision). The worker listens on `10.250.23.2:5679` only; its runner connected and offers tasks. Main opens no `5679` listener and its runner waits for the broker, as it did before the change (Loki, 2026-11-02 start), because main runs `EXECUTIONS_MODE=queue` with `OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true`. From `storybook-mcp` on `edge_net`: `n8n-worker:5679` does not resolve, `10.250.23.2:5679` times out, `n8n:5679` is refused. The worker runner resolves only `n8n-worker` (not `n8n`, `mng-pg` or `ollama`). The worker reaches Ollama (`/api/version` 200); the n8n route answers 302; `n8n-monitor` scrape up; Gatus 8 endpoints, none failing. A Code node execution through the HOME worker runner was not run. | required | - |
| P03 Runner HOME Code node execution | 63 | W68 | Owner-run UI workflow: Manual Trigger, JS Code node, Python Code node | HOME after the runner isolation apply | PASS | The owner ran the test on 2026-11-08 and reported it done. Logs: `n8n-worker` started and finished executions 122–125 (first at 01:34:18Z); the worker broker logged `Registered runner "JS Task Runner"` and `Registered runner "Python Task Runner"`; the worker runner logged no error other than Node's `ExperimentalWarning` for `localStorage`. This covers the manual Worker actor path in HOME: manual executions are offloaded to the worker. | required | - |
| P03 Runner fixture parity and wrong-token bound | 63 | W68 | `test_p03_runner_boundaries`, `test_p03_runner_isolation` and every `NativeFixture` consumer | Clean `main` `6361e93b5` plus this change | PASS | Four new or changed assertions fail on the base; all suites pass after. Native rerun NOT_RUN | required | - |
| P03 Runner native rerun at merged parity change | 63 | W68 | `P03RunnerNativeRehearsal` | `b62de97d7`, cached images | FAIL | Worker broker readiness `target_rejected` by the probe URL allowlist; cleanup PASS, residue 0 | required | - |
| P03 Runner native rerun after the probe target fix | 63 | W68 | `P03RunnerNativeRehearsal` | Branch `fix/p03-broker-probe-target` on `b62de97d7`, cached images | PASS | Probe target regression RED then GREEN; `native=PARTIAL`; all scenarios PASS including `peer_nonbroker_port` and `wrong_token_registration` (`http_403`, not registered); three by-design fixture differences; cleanup PASS, residue 0 | required | P03 Runner native rerun at merged parity change |
| Initial Hermes exact-destination attempt | 64 | W69 | Scoped workload tests, native local TLS transport and Ruff/diff check | Synthetic policy/credential inputs; no live Hermes target | PASS | 2026-11-02T12:49:13+09:00: plugin 42/42, synthetic local TLS 19/19 and scoped workload 356/356 PASS in 17.552 seconds; helper branch coverage 84%. Source SHA-256: `tools.py` `e4fe7697d717c0a986c6ba4831dfbc5162863bf5f7918df1da5efb4c1e9ea9c2`, transport `e5c78be6a8e698e8ee6fe6b776d58cb75684cccfbe11c088065558b6d2c29358`, plugin test `c72f2ff2e5dc4f04dc618eeeaf7ee2221ac4077de91fd73dd1b8a0d76ba19b9c`, transport test `5e01dca94333e10e67882a0391a6ed0edc97b0eccf76d1121474f95c1dd4401e`. Historical attempt evidence only. | optional | - |
| Hermes cancellation safety review | 64 | W69 | Independent security review | Initial Hermes source packet | FAIL | Independent review found that parent `SystemExit`/`SIGTERM` can orphan the child and allow a request after cancellation. The initial PASS does not close W69. | required | - |
| Current Hermes corrective packet | 64 | W69 | Corrected scoped tests, native local TLS transport and Ruff/diff check | Frozen synthetic policy/credential inputs; no live Hermes target | PASS | 2026-11-02T05:08:00Z: source SHA-256 `tools.py` `e4fe7697d717c0a986c6ba4831dfbc5162863bf5f7918df1da5efb4c1e9ea9c2`, transport `adb3ab26f7cc37645d345c84c52eb34051c66362626226f8623fe01422a83fad`, plugin test `c72f2ff2e5dc4f04dc618eeeaf7ee2221ac4077de91fd73dd1b8a0d76ba19b9c`, transport test `971dac2a153d868081b1c670451d921644b4c2dad94292404fb629d486f3bd51`; corrected gate 65/65 including three TLS cases and actual SIGTERM, scoped workload 360/360 in 20.108 seconds, branch coverage 84%, Ruff/format/diff PASS. Writer evidence, independently reviewed below. | optional | - |
| Hermes corrective re-review | 64 | W69 | Independent security review | Frozen corrective transport `adb3ab26f7cc37645d345c84c52eb34051c66362626226f8623fe01422a83fad` and test `971dac2a153d868081b1c670451d921644b4c2dad94292404fb629d486f3bd51`; tools/plugin test unchanged | PASS | `p03_tool_review`, 2026-11-02: 23/23 PASS in 3.304 seconds. The parent-death `SystemExit`/`SIGTERM` race is closed for local source/isolated scope through the Linux exact-parent guard before credential stdin, signal restoration and process reaping; no delayed side effect was measured. Actual installation, policy/DNS/certificate, credential and live delivery remain P11 `NOT_RUN`. | required | Hermes cancellation safety review |
| Public P03 model connection extraction | 61 | W66 | Public-source connection tests and exact route test | Public tracked sources; no stored registration or live inference | PASS | 2026-11-02T05:04:33Z: connection suite 23/23 and exact workflow-route suite 2/2. Extractor `d0e781629fc1a23a3da8047766f7d2cf90da6ccb79f678b67d3c2d991127502a`, dispatch `12b3b9b2b486d7efd63e0b677025127098e0a672101c816b9bd4526ed7766175`, connection tests `2a6c9e36a87b850f1fc39abf2a945336717599296a456de7ab366912c15d6d06`. Source-only rows remain `UNKNOWN`. | optional | - |
| Public P03 Hermes gate | 64 | W69 | Combined connection/Hermes gate and owned loopback Hermes gate | Synthetic gate inputs; no live credential or service | PASS | Combined connection/Hermes gate 28/28 and corrected owned loopback Hermes gate 65/65 at 2026-11-02T05:08:00Z. Gate `19ddc2cdf2bc98ffde78e874acfefe9a8209585f3e5da7a47819f72fabf08f0d`, tests `4d25af2dae82a2e6c46b58acedad05af971ae54df8283a5b4a33146e9a119eb5`. This does not replace required independent Hermes re-review. | optional | - |
| Final CI model adapter | 61 | W66 | Clean-environment registered model adapter | Current synthetic selectors; exactly two declared native opt-in classes skipped | PASS | `p03_ci_resume`, 2026-11-02: format-frozen adapter exited 0 with 74 PASS and only `NotebookModelsNativeExecutionTests` and `WorkerModelQueueNativeTests` skipped. Reviewed final extractor `4fae84b87866e1c3b28d9467b1a1d796da5407d02fa65d1fc5cf630e1bee60c1`, dispatch `e3f8e6e9368d1643d58fcb34951a8bd5f4f9bf76aaf243121eeee98edbbf3e5a` and tests `5011bfdea45631c7d089b71be7655e11e78cd8e2be01ea7f4dcc1d3991fe2331`. This is local CI-adapter evidence only; native model/runtime remains NOT_RUN. | optional | - |
| Final CI Runner adapter | 63 | W68 | Registered runner adapter | Current source selector; one declared native opt-in rehearsal skipped | PASS | `p03_ci_resume`, 2026-11-02: frozen-path adapter exited 0 with 15 PASS and exact one native opt-in `P03RunnerNativeRehearsal` skip; the broader focused writer receipt was 16 PASS plus the same skip. It confirms selector registration/source checks only and does not promote native overall PARTIAL to candidate Compose/HOME PASS. | optional | - |
| Final CI Hermes gate | 64 | W69 | Registered owned-loopback Hermes wrapper | Synthetic endpoint and policy only; no live credential/service | PASS | `p03_ci_resume`, 2026-11-02: fixed wrapper 65/65 PASS with no skips. Final wrapper `454e4883ff9253c5b0c8977c2e155b746296d55e593167989262238d81b36d5c`, test `1801d47c64206d4bd4be5d53cb8118b2b5755f5be0346daa694980389e162b73`. This does not replace P11 installation/delivery evidence. | optional | - |
| Final CI organization packet | 61 | W66 | Independent CI route/discovery review | Current public source and registered selectors; no hosted execution | PASS | `p03_code_review`, 2026-11-02: workspace 24/24, workflow 47/47, discovery 71 unique IDs, Runner 22=21 PASS+1 native skip; Ruff and diff PASS. Initial gitleaks blocked the non-secret high-entropy suite identifier `p03-hermes-contracts`; CI changed only gate/suite identity to `leaf.p03-hermes`/`p03-hermes`, without argv, environment, entrypoint, route or leak-policy change. Current workflow `673e4926795605bd4334e4875cb904382eccc5f08b0add0a4f0d30b77b4dcc9a`, manifest `8d703b7601af47d1955154dc7f8e478c2f12023f7c44a4088d17056a5c855ece`, workspace test `2f9c84ad0f1fe0135cbde965590c39687bdf847f81b3b404e8df61a8f6116383`, workflow test `e205d8ac5517f988ed6645e4cb9b40498c76eae28e4d8d0e0cfad4a73639c5f6`. Hosted CI remains NOT_RUN. | required | - |
| Current operations catalog projection | 61 | W66 | Generated inventory block and catalog validation | Current Compose projection; no runtime observation | PASS | Renderer changed only 13 projected P03 fields: n8n Network/Env, each Runner Network/Persistence/Env/Security, n8n-worker Network/Env, and open_notebook Env. `check-operations-catalog.py` and diff check PASS; source document `m0021-local-docker-service-consolidation.md` `0a870fd75457a2249e8b14058b0b5b090d09f456aa8599e2d380a64818a528a7`. | required | - |
| Final registered local gates | 61 | W66 | Manifest, workflow/direct contracts, workspace extraction, catalog, links, metadata and Registry | Final local tracked packet; no hosted execution | PASS | Manifest PASS; workflow 47/47 plus direct contracts 5/7/9 PASS; workspace extractor 24/24 PASS; catalog PASS; links 1182 documents/9607 links with 0 failures and one historical warning; metadata selected 32 with 0 violations; Registry 126/126 PASS. These are local gate results only and do not replace hosted CI, live operation, rotation, restore or final acceptance. | required | - |
| Historical pre-index manifest/workflow attempt | 61 | W66 | Script manifest and workflow contract validation before final index | New executable paths were untracked | NOT_RUN | This historical pre-index attempt failed only because new paths were untracked. It is superseded by the `Final registered local gates` PASS row; hosted CI remains NOT_RUN. | optional | - |
| Wiki preparation mapping/evaluation | 65 | W70 | Existing TSK-0008 provenance and six documented offline cases | Completed preparation package; rights/ACL/citation/revocation/no-evidence/failure-recovery descriptions | PASS | `infra/09-platform-ops/project-registration/wiki-preparation/fixtures/README.md`, 2026-11-02 P03 source mapping. This is documentation/source evidence only; no new helper execution or runtime acceptance is claimed. | required | - |
| Current direct operation | 61 | W66 | HOME service/model/credential/installation operation | No approved target, operator or window | NOT_RUN | Out of this local source unit; the same status is retained in the criterion decisions for W67–W70. | optional | - |
| Credential rotation and independent restore | 62 | W67 | Actual credential and state recovery | No P06/P09 data-owner approval or recovery window | NOT_RUN | P06/P09 owner handoff | optional | - |
| Hosted CI | 61 | W66 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit; the same status is retained in the criterion decisions for W67–W70. | optional | - |
| Final acceptance | 61 | W66 | P12 end-to-end acceptance | No approved operating acceptance | NOT_RUN | P12 handoff; the same status is retained in the criterion decisions for W67–W70. | optional | - |

P03 hands the exact source fingerprint, intent, tests and recovery boundary to
P05 for general queue behavior, P06 for Secret custody, P08 for image/lock and
product-support decisions, P09 for common resources, P11 for actual Hermes
installation and P12 for user-level acceptance. P03 does not reopen P02's
remaining supply-chain residuals or its pre-existing audit findings.

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 61 | pending | Current final model source review | SOURCE_READY: final local-only source and isolated proof are independently reviewed. Current model inference and operation remain NOT_RUN. | SPEC-0212 TSK-0042 |
| 62 | pending | Current final Notebook registration source review, Worker-model native queue rehearsal, Notebook native census | SOURCE_READY: final synthetic registration proof and one controlled Worker queue/model path are evidenced; Notebook native fixture, real model inference/persistence, 768-vector retrieval, whole-dataset restore and operating acceptance remain NOT_RUN. | SPEC-0212 TSK-0042 |
| 63 | pending | P03 Runner full application rehearsal, Runner outcome-module style split, Final CI Runner adapter, P03 Runner post-fix native rehearsal, Runner denial attribution diagnosis, Runner denial classifier source fix, Runner earlier-layer file denial source change, P03 Runner native rehearsal after the denial fixes, Runner environment denial attribution fix, P03 Runner native rehearsal setup under host load, P03 Runner native rehearsal after the attribution fixes, P03 Runner HOME apply, P03 Runner HOME Code node execution, P03 Runner fixture parity and wrong-token bound, P03 Runner native rerun after the probe target fix | TEST_RESIDUAL: the synthetic fixture rehearsal passed on 2026-11-08 (`native=PARTIAL`) with every denial, timeout, cancel and restart scenario attributed; after the 2026-11-08 fixture parity rerun `peer_nonbroker_port` and `wrong_token_registration` also PASS; the fixture is non-equivalent only by the shared `ctl` network, tmpfs and caps, and candidate Compose, paired network, manual Worker and private workflows are NOT_RUN. File denials are proved at the builtin and module layer only (owner decision). The fixture cleanup gap for unadopted containers is open. Runner isolation is applied in HOME (2026-11-08); a HOME Code node execution through the worker runner passed (executions 122–125). Remaining residuals move to SPEC-0269. | SPEC-0212 TSK-0042 |
| 64 | pending | Hermes cancellation safety review, Current Hermes corrective packet, Hermes corrective re-review | SOURCE_READY: the corrective local source packet and independent re-review pass. Installation, live policy/DNS/certificate, rotation, restore and final acceptance remain P11/P12 NOT_RUN. | SPEC-0212 TSK-0042 |
| 65 | pending | Wiki preparation mapping/evaluation | REUSE_ACCEPTED for completed offline preparation plus current source mapping; product implementation and executable E2E evidence remain OUT_OF_SCOPE/NOT_RUN | SPEC-0212 TSK-0042 |

## Review and Completion

Independent code, security, IaC, CI and document review must cover the exact
changed fingerprints. The final model exact-integer-dimension and extractor
delta reviews are complete in their bounded source/isolated scopes. The Hermes
corrective local-source review is also complete in its bounded scope;
Hermes installation,
policy/DNS/certificate, credentials and delivery remain P11 `NOT_RUN`. The
runner normal-JS diagnostic is PARTIAL rather than candidate-runtime acceptance,
and the CI packet still needs its final indexed validations before a normal local
commit. `graphify update .`,
changed-document metadata, links, Registry/DATA validation and final diff
inspection remain final integration checks.

The local source unit keeps direct operation, credential rotation, independent
restore, hosted CI and P12 final acceptance as `NOT_RUN`. P03 may hand off
exact fingerprints, intent, tests, recovery boundary and resume condition; it
does not create the operating authority for P04/P05/P06/P07/P08/P09/P11/P12.

## Related Documents

These links identify the canonical parent, historical scope and operating
documents; they do not transfer acceptance or operating authority.

- [SPEC-0212 plan](../plan.md)
- [P02 service connection contracts](tsk-0041-service-connection-contracts.md)
- [Historical P03 integration](../../0204-service-integration-security-and-operations/tasks/tsk-0011-p03-service-integration-contracts.md)
- [Completed Wiki preparation](../../0204-service-integration-security-and-operations/tasks/tsk-0008-llm-wiki-preparation.md)
- [Open Notebook guide](../../../05.operations/guides/09-ai-and-search/0073-open-notebook.md)
- [Open Notebook policy](../../../05.operations/policies/09-ai-and-search/0073-open-notebook.md)
