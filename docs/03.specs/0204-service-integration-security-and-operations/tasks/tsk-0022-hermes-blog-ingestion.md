---
title: "Hermes Blog Ingestion Transport Task"
version: "0.5.5"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-01"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0022"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-30"
---

# Hermes Blog Ingestion Transport Task

## Overview

### Objective

Implement the independently testable, source-only Publisher/Outbox slice of
criterion 23 without duplicating existing Hermes export or n8n crawling.
Gateway contract adoption and actual operation remain separate required lanes.
W79-W83 belong here; Task0013 and SPEC0247 retain their own files/acceptance.

## Inputs and Authorization

The owner's 2026-10-30 request authorizes basic implementation and safe checks.
Existing Cron changes, real secret use, workflow activation, Compose recreation,
public ports and remote Git each retain their exact approval conditions. No
secret value, auth file, raw log or broad Hermes home read is implied.
Revert Task-owned source only; retain original output and Outbox evidence.
No deployment, data deletion or queue reset is a rollback step.

### Source admission

- Reuse structured exporter `84d3f689378b`; do not create a new schedule.
- Approved jobs: `6eabd835f969` (strategy-news), `25674fbc0bf3`
  (devops-brief), `8d0925bc571d` (solo-dev-ideas).
- Exclude private infrastructure job `3c3f81a925e0` even if found under a root.
- Candidate root: `/home/hyunyoun/storage/research/hermes-report-export/out`.
- Reports are narrowly resolved beneath
  `/home/hyunyoun/.hermes/cron/output/<approved-job-id>/`; approved idea
  files resolve only beneath `/home/hyunyoun/storage/research/solo-dev-ideas`.
  Synthetic roots must preserve the same structural restrictions. No n8n mount
  of `.hermes` or home-wide access grant is part of this implementation.
- Reviewed dependency:
  `/home/hyunyoun/data/hy-home.docker/.worktrees/feature/hermes-offline-publisher-pr/scripts/validation/check-hermes-candidate.py`,
  SHA-256 `8c988c715286edd53d2f7e5931cb349e6a5bed49be8ec2f8e7be98f2810c7297`.
  Invoke `validate(data)` for structural validation after source review and
  digest verification. Publisher independently reads bytes through bounded
  directory descriptors with no-follow checks and verifies restricted roots
  and SHA-256. Missing or changed dependency fails closed. The dependency is
  on an unpublished SPEC0247 branch; it is not a tracked runtime artifact.
  This file remains SPEC0247-owned and is never edited/copied by Task0022.
- The active sidecar's `validate_candidates.py` has the weaker
  `validate_candidate(data, source_root)` API; its mere presence is insufficient
  adoption of the stronger reviewed contract.

### File ownership and dependencies

| Writer | Exclusive surface | Dependency and handoff |
| --- | --- | --- |
| Staging implementer | Workload `publisher/{__init__,files,candidates,outbox,cli}.py`, staging tests | W79 frozen roots/validator; actual Outbox API handed to delivery writer |
| Delivery implementer | Workload `publisher/delivery.py`, delivery tests | W80 immutable record/transaction interface, reviewed before shared integration |
| HTTP transport implementer | Workload `publisher/http_transport.py`, `tests/test_http_transport.py` | Independent W82 groundwork only; no edits to delivery, CLI or workflow; synthetic loopback endpoint and fake credentials |
| Gateway adapter implementer | Workload Gateway adapter source and its dedicated tests | Pin and verify the exact Gateway contract/fixture revision below; establish timestamp provenance before mapping; coordinate any shared delivery integration explicitly |
| n8n integration implementer | Workload `workflow.json` and workflow-specific tests | Consume the pinned contract and adapter handoff; remain inactive; no credential IDs, activation or production changes |
| Workflow source writer | Inactive `workflow.json`, workflow tests, workload READMEs and workloads README link | Contract-based source; Native import and actual forwarding remain NOT_RUN |
| Documentation writer | Spec criterion 23/contract, Plan W79-W83, this Task; later source-only RUN-0053 section | Implemented commands and measured evidence; no guessed operational procedure |
| Controller | Read-only inventory, test registration proposals, review coordination and final evidence | Exact worker handoffs, single-writer shared integration |

All paths above use workload
`infra/07-workflow/n8n/workloads/hermes-blog-ingestion/`. Other dirty paths,
Task0013, Manifest Outbox Notifier, SPEC0247 and other worktrees are excluded.
No global service/profile activation is required.

## Work Log

### Design admission — 2026-10-30

Selected canonical doc-writer and explicitly loaded bootstrap/provider,
documentation/approval policy, Stage99 Spec/Plan/Task profiles, governing
REQ-0027/AD-0031/ADR-0046 and workflow REQ-0008/AD-0007 with n8n Stage05 peers.
The isolated checkout has no `graphify-out/graph.json`; no graph query could
precede navigation there. The controller owns the prior main graph query.
The writing-plans skill supplies implementation sequencing; the user's existing
Spec/Task system owns location and existing source authorization permits work.

Chosen approach: reuse completed sidecar exports, stage lossless snapshots in
SQLite and test an adapter-independent delivery engine. A restricted host
process avoids a Compose change. Rejected alternatives: a duplicate exporter
Cron, broad Hermes mounts, LLM resummary as a gate, repurposing Manifest
Outbox Notifier, or inventing a Gateway contract. SQLite is local Publisher
state; Valkey remains existing n8n queue coordination and PostgreSQL retains
n8n metadata. No new service, database, Qdrant index or SeaweedFS fallback is
provisioned. SeaweedFS remains a design alternative only if the direct approved
private route proves unavailable.

### Observed inventory — 2026-10-30

Controller read-only inventory refreshed remote main with `ls-remote`:
`e065bce168f054c9a75fef97e0c4e029fbca7baa`; initial root main matched and was
clean. Isolated branch `codex/hermes-ingestion-transport` starts at that base.
Two existing offline-validator trees at `edb6aa461` and `ffbfbfe63` had dirty
state and were preserved. The supplied earlier `15478359edc0` was not reused
as a current baseline. The initial root Graphify query preceded source reads;
its graph was stale advisory, while this isolated tree had no graph JSON.

Hermes gateway and Dashboard were active for host user `hyunyoun`. Dashboard
`10.250.1.128:9119` returned HTTP 302; LAN `192.168.0.13:9119` refused TCP.
The server-A host reported Ubuntu 24.04. No VPN-named interface was observed;
this does not establish VPN absence. Exporter `84d3f689378b` was active every
five minutes with `no_agent` and an okay current-day result. Existing candidate
news run `56780cdef19b495c8cf46df55da4e59c` contained 14 items; business-idea
run `7022eeab2ec44945b3cb6f277bc371fe` contained eight. Both passed the
stronger CLI validator in read-only checks with `--source-root
/home/hyunyoun/.hermes --item-root /home/hyunyoun`; these validator resolution
roots are not a grant for broad mounts or reads. No native Outbox staging had
been performed when this inventory was recorded. Email `reported_sent` was
producer self-report only; no live inbox delivery was established or changed.

Observed main/worker local images were `2.43.6-local`; both external runners
reported `2.43.6`, all healthy. These are dated observations, not a new pin
selection. Main readiness and worker broker `127.0.0.1:5679/healthz` passed;
worker `localhost` IPv6 connection failed and is retained as a distinct result.
PostgreSQL, Valkey, Traefik and OpenBao Agent were healthy by their observed
health signal, not by a new functional secret-consumption test.

Observed `n8n_net` is a bridge, `internal=false`, subnet `10.250.11.0/24`.
Main belongs to edge/management/n8n/observability networks; worker belongs to
management/n8n and its existing internal Ollama network; runners use n8n only.
No Hermes or Docker socket mount was present. No network/Compose change was
made. A safe no-password local PostgreSQL read-only transaction inspected
metadata only: six workflows, all inactive, no Hermes/news workflow, 18 success
and 54 error executions with no running/waiting row. Counts are inventory,
not workflow regression success. `/home/hyunyoun/data/hy-home.n8n` was absent
locally; remote operation remains unknown and duplication cannot be ruled out
solely from local absence. No secret value was read during this inventory.

Implementation and verification remain separate: existing Hermes exporter and
n8n queue infrastructure exist and were observed; Task0022 Publisher source and
synthetic tests are in progress. Gateway API compatibility, Native n8n import,
actual worker-to-server-B delivery, live email receipt and regression execution
are not established by these read-only checks. Developing Blog-data drafts are
uncommitted/unapproved interface evidence; required `scheduled_at` semantics
are absent from producer candidates and must not be fabricated.

### Gateway contract and native gates — earlier observation

A read-only inspection of the shared diff in the “Hermes 수집 API 구축” chat
found a provisional, uncommitted `ingestion-v1.schema.json`. It requires
`scheduled_at`, `generated_at`, `collected_at` and item `body`/`source_text`.
Observed Hermes candidate v1 has `generated_at`, but no authoritative
`scheduled_at` or `collected_at`. This draft is useful gap evidence, not an
owner-approved cross-repository interface revision. Exact fixed version,
fixtures and timestamp mapping remain BLOCKED; never invent missing timestamps
or adopt the provisional draft as the confirmed contract.

The owner supplied [public build manifest](https://buenhyden.github.io/build-manifest.json)
and confirmed the Gateway API is developing in the separate “Hermes 수집 API 구축”
chat. Public GET identified Blog-data main
`03e805f8094de3922113cea916feae30b945e6ef`, web build 2026-10-26; this is not
an ingestion API or fixture. No exact request/status/receipt/reconciliation
contract is available here. Gateway-dependent W82 remains BLOCKED; no forwarding
workflow or Gateway adapter is authored until its exact approved API/fixtures
are adopted. The allowed inactive
preparation stub contains only headerAuth Webhook → StopAndError
`GATEWAY_CONTRACT_NOT_BOUND`, no HTTP node/endpoint/body mapping and no
real credential ID. It is partial SOURCE preparation, never a compatibility
or Native import/activation result.

Planned topology: approved candidate/report/idea files → restricted Publisher
and durable Outbox → authenticated internal n8n webhook → schema/identity
validation → Gateway HTTP → durable receipt/reconciliation → Outbox result.
The internal event wire shape remains undecided until the Gateway contract;
no independent n8n JSON/status vocabulary is created. For a future container,
review overlays and existing `n8n_net`, narrow read-only mounts and non-root
UID first. Keep Traefik SSO, external routes and firewall unchanged.

Actual server-B private IP/DNS/OS, VPN route, TLS chain, firewall and service
authentication are not confirmed. Worker-origin DNS/TCP/TLS/auth/timeout and
Gateway durable receipt tests remain BLOCKED. Do not read/use real secrets to
resolve them without separate concrete authorization. Existing n8n PostgreSQL,
selected Valkey and OpenBao consumers are reused through their current owners.

### Follow-up source admission — earlier observation, 2026-10-30

The owner requested a fresh check of the developing Gateway and continuation of
independent integration work. The separate Gateway chat remains active; its
latest report records 30 Gateway tests passing, while overall QA has two
failures and four blocked checks, and its local branch is being prepared. The
checked Blog-data `dev` revision `18a2b6d7a1666a14b4717404e9223a32139a5b0e`
and `main` revision `7c8b1e8b60085212d50e977756d46d596eff607b` both returned
404 for `docs/03.specs/0149-hermes-headless-ingestion/contracts/openapi-v1.json`.
No fixed accessible contract and fixtures or authoritative timestamp mapping
were established. These observations do not establish API compatibility.
The Gateway chat subsequently records the operator's QA baseline designation
and Docker build work in progress. A QA baseline designation does not by itself
provide an accessible fixed contract and fixtures to this worktree or prove
cross-repository compatibility.

Within W82, a separately owned generic HTTP transport source and synthetic
tests may proceed without defining a Gateway request, response, status or wire
protocol. Bound payload and response sizes and timeouts, reject redirects,
verify TLS certificates by default, and retain value-free errors and
conservative ambiguous outcomes. Targets require HTTPS except explicit loopback
HTTP used only by isolated tests. Plaintext to an internal n8n route requires a
future separately reviewed exact boundary; this admission does not grant it.
Reconciliation must refuse replay or report NOT_RUN until actual idempotency
semantics are established. Tests may bind an isolated local socket and use fake
credentials; no real secret, live service or external network is authorized by
this unit. No CLI dispatch, workflow activation, Compose or network changes
are included. The Gateway adapter, fixture compatibility and n8n forwarding
remain blocked pending the exact accessible owner-approved contract.

An independent security review found that the first experimental transport's
idle timeouts did not bound slow DNS, headers or bodies; the writer removed
that experiment. Its four mock passes and skipped loopback test do not establish
the current implementation. A replacement obtains inputs before invocation,
without an authentication callback, and bounds DNS, TLS, request, headers and
body after child subprocess startup. Timeout kills and reaps the child and
classifies the result as ambiguous. Subprocess creation and caller secret
acquisition are outside that deadline. Independent security review found no
additional Critical or Important findings. Under limited approval, isolated
synthetic localhost tests passed 9/9 on an earlier revision, including redirect
and self-signed certificate rejection; this is not a live service test or the
final revision's suite result. A subsequent code review identified a pre-send
connect failure classification issue; the correction permits NOT_SENT retry
and preserves AMBIGUOUS after a request, and independent security re-review
passed. The final revision's complete suite reported 74 PASS and one optional
validator SKIP out of 75; Ruff check and format passed. A separately approved
synthetic localhost HTTP/TLS run on the final revision passed 11/11. Private CA and actual
operational connectivity remain unverified. Exact Gateway contract and
fixtures were inaccessible at that observation and Gateway workflow integration
was not yet implemented; Native operation remains pending. Focused tests using
the fixed validator passed 14/14. The measured 93% coverage excludes the child
subprocess; it is not a complete coverage figure for the transport child.

### Gateway source admission after Blog-data PR #620

Blog-data PR #620 merged to `dev` at fixed revision
`a6d0957ad380f179f73bdd2a60ff23792d53f7ae`. The contract inputs to obtain and
verify at that revision are `scripts/lib/ingestion/contracts/openapi-v1.json`,
`scripts/lib/ingestion/contracts/ingestion-v1.schema.json`,
`scripts/lib/ingestion/contracts/responses-v1.schema.json`, and
`tests/workspace/fixtures/ingestion/synthetic-report.json`. Earlier 404 and
inaccessible-contract observations in this log refer to earlier revisions and are
historical, not evidence about this merged revision. Record actual retrieved
contents and digests before claiming adoption or compatibility.

W82 proceeds in separately owned adapter and inactive workflow lanes: read the
fixed API and fixture, write contract-backed tests, implement exact request,
receipt and idempotency handling, then connect the inactive workflow through an
explicit integration handoff. Actual producer provenance for every required
timestamp remains a prerequisite; do not manufacture values. Source tests and
an inactive workflow do not authorize production network or secret use, workflow
activation, Compose changes, or Native verification. The current PR branch was
fast-forwarded to `4bb1d7c`. Its latest candidate check FAILed on a malformed
merge commit message. Correction is deferred pending discussion of alternatives;
preserve history and do not rewrite it.

The user specified `collected_at` as the actual Hermes article collection time;
`generated_at` is execution finish time and `scheduled_at` is the exact
execution `scheduled_instant`. The eight existing candidates and their database
records do not contain the actual article collection time, so actual conversion
and delivery are BLOCKED until authoritative provenance is available. Gateway
adapter and transport review was in progress at that observation. n8n Native
workflow execution, authenticated relay and live operation are NOT_RUN; the
previous stub's `responseNode` configuration produced a configuration error as
recorded below. The API and fixture are pinned to the four Blog-data PR #620
dev blobs above, which does not itself establish compatibility. Work in review
includes an adapter and receipt/Outbox handling, pinned fixture/schema tests,
content-type validation, an explicit offline replay wrapper and a real
adapter/Outbox response-loss test. The inactive n8n source uses a reserved
domain, with pure Node tests; at that observation independent review was still
in progress. Native operation, credentials, URL
runner, queue logging, HTTP 400 branch and alerting remain NOT_RUN.

The user chose a replacement PR while preserving the existing PR. The existing
PR's candidate failed on the malformed merge commit; replacement recovery is
being prepared. This selection does not establish a new passing candidate.

The fixed Blog-data `dev` revision above supplies the contract and fixtures for
the current source scope. Adapter/replay synthetic tests, including real Outbox
handling after a lost response, passed 6/6. The inactive workflow source screens
input and returns a fixed 400 for invalid input, a stricter boundary than the
Gateway contract. Independent code and security reviews were performed. The
full suite ran 105 tests with one skipped before the final IF test change; that
receipt does not cover the later change. Import into n8n, Queue execution,
credentials, TLS, actual logs and alerts, and runtime operation remain NOT_RUN.
Actual conversion remains BLOCKED because the user-defined original article
collection time is absent. PR #684's malformed-history candidate remains FAIL;
the replacement selection preserves #684 and does not establish hosted acceptance.

The latest inactive workflow source removes reliance on the URL global and
delegates URL authority validation to the Gateway, avoiding rejection of valid
IDN or IPv6 authorities. It applies a stricter 24-hour prefilter, a fail-safe
fixed 400 IF branch, and a success MIME check. Pure Node tests with an empty VM
passed 13/13. This is source evidence;
Native Queue, credentials, alerts and runner execution remain NOT_RUN, and
actual delivery remains BLOCKED by missing article collection time.

Read-only timestamp reinvestigation found that the installed scheduler's Run
Time header is generated after the agent runs and the filename records save
time. Execution database entries establish the run interval and `generated_at`
as the finish, not individual article collection times. The examined 14 news
items and eight idea items contain collection-evidence strings without such
timestamps. The eight idea references for the examined candidate were missing
at inspection; nine files in the corresponding date directory had later
modification times and none matched those references' hashes. The raw report
hash matched. The reason the referenced files are absent is unknown; do not
infer deletion or replace them with unrelated files. Actual article
`collected_at` remains BLOCKED and no timestamp may be guessed. These are
read-only observations, not Native operation or delivery evidence.

Replacement PR #689 hosted run `41042875715` first attempt failed when its skip
parser encountered an interleaved unrelated `BrokenPipe` message. A re-run was
requested and is in progress; no hosted pass is claimed. Main has advanced
since the prior baseline and must be verified against the actual candidate.

The pinned Gateway runtime restricts timestamp fractions to one through three
digits. Actual candidates carry six fractional digits in `generated_at`;
after exact matching, the Gateway wire value is truncated to milliseconds.
The local original retains microseconds, while the wire representation loses at
most 999 microseconds. This conversion does not supply or substitute the actual
article `collected_at`. For the two investigated runs, the corresponding
`request_id` follows `cron:<job_id>:<run_id>` and is associated with the
session. The read-only investigation followed exact request-to-session and
tool-call relationships and matched requested URLs and successful results to
candidate source URLs: 11 of 14 news items and two of eight idea items matched;
the remainder did not. The observed timestamp is message creation after tool
execution and is shared across a batch, so it does not establish per-item fetch
time or the user-defined actual `collected_at`. Original collection timestamps
remain BLOCKED. Original Outbox data retains microseconds; downstream wire
precision is limited as described above. The first CI re-run and a limited
synthetic n8n import test are in progress; neither is claimed as PASS. HEAD and
main may change during these checks and must be matched to their results.

An isolated import/export smoke attempt used one exact-image n8n container with
no network, a read-only filesystem, dropped capabilities and only the approved
read-only bind. The Docker client exited 130 after five minutes; a stop of the
exact temporary labelled container returned 0. The container remains with
daemon status `removing`, `Dead=true`, `Pid=0` and exit code 137. The reason is
unknown and further diagnosis is pending; no forced removal or daemon restart
was performed. Existing n8n main, worker and runners were observed up and
healthy. The import is BLOCKED, not a PASS or Native workflow execution receipt.

The replacement checkout's full suite subsequently passed 107 tests with the
pinned validator and synthetic localhost tests. Independent final adapter,
replay and workflow correctness and security reviews found no remaining Critical
or Important findings. The workflow URL preprocessing accepts a subset of the
Gateway's valid inputs; it is not equivalent to the Gateway's full URL parser.
The replacement branch integrates `6a` without rewriting the existing history;
its draft PR is not yet published. PR #684's malformed merge CI remains FAIL,
and hosted acceptance, n8n Native and criterion completion are not established.

### Publisher delivery CLI review — removed attempt

A proposed explicit single-record Publisher `deliver` CLI and synthetic test
were reviewed with a fake authorization value and mocked HTTP responses. They
exercised durable receipt handling, absent authorization, mismatched
`generated_at`, and an ambiguous response followed by a second invocation.
The attempt was removed after independent security review: it did not prove
the user-required actual article collection-time provenance or a reviewed
binding from the requested relay endpoint to the intended Gateway destination.
It is not implemented source, SOURCE/SYNTHETIC acceptance, or an operational
command.

A later delivery interface needs value-safe authorization input, a reviewed
transport topology, error redaction, immutable Outbox binding, and no POST replay from `uncertain` before explicit idempotent
replay authorization and relay/Gateway binding evidence. It must not introduce
automatic delivery service, workflow activation, Cron modification, Compose
recreation, or external ingress as part of its source scope.

The earlier timestamp evidence remains unchanged: run database and report times
establish scheduling/execution timing, while linked tool messages establish
only post-tool, sometimes batch-shared timestamps. They do not establish each
article's actual `collected_at`. Native worker-to-relay, relay-to-Gateway,
TLS/authentication, durable receipt, outage/recovery and existing email/workflow
regression remain NOT_RUN.

### n8n Native admission follow-up — blocked import

The operational n8n 2.43.6 package's `safeParseWorkflowStructure` accepted the
tracked workflow bytes with `success: true`. This is a parser-only source check:
it does not import, activate, execute, enqueue, or call the Gateway. On two
isolated exact-image containers, `n8n import:workflow --help` produced no
output within 45 seconds, so no import command was run. Both new temporary
containers were stopped and removed normally; the earlier dead temporary
container is no longer present. The existing n8n main, worker and two task
runners remained healthy by their observed health signals.

Native workflow import therefore remains BLOCKED. Queue execution, credential
binding, relay/Gateway networking, TLS/authentication, durable persistence,
alerts, outage/recovery and email/workflow regression remain NOT_RUN. This
bounded observation authorizes none of activation, Compose recreation, port or
network changes.

### Publisher endpoint binding follow-up — source and synthetic evidence

The delivery path now obtains the configured relay endpoint's SHA-256 from the
transport and writes it with the contract revision, destination, and immutable
request bytes in the Outbox. Every later send or replay compares that stored
digest with both the request and the configured transport before dispatching.
An endpoint replacement therefore fails closed as an `invalid_binding` outcome
instead of silently reusing a request for a different endpoint. The first
Outbox open adds the nullable digest column for existing local databases; it
does not change any Cron, workflow, Compose, network, credential, or remote
resource.

Independent correctness and security review of this change found no unresolved
Critical or Important finding. The focused suite ran 115 tests: 113 passed and
two were skipped. This is SOURCE/SYNTHETIC evidence only. A SHA-256 digest of
an endpoint string proves neither DNS/TLS routing nor that the endpoint belongs
to the intended Blog-data tenant. Tenant ownership, credential scope, certificate
identity, and a durable Gateway receipt still require the separately approved
operational validation lane.

The owner selected the report-level `collected_at` rule: use the latest actual
collection time among all items in that report. Admission is all-or-nothing:
every included item needs its own authoritative actual collection time, and a
single missing value keeps the complete report deferred. The current source
inventory contains 153 items without that evidence. They cannot be
request-bound or delivered as `collected_at`; execution finish, report-save,
and tool-message timestamps are not substitutes.

The present Hermes evidence is also insufficient for cached or batched tool
work. A session message is written after the tool returns and can represent a
batch, so it cannot attribute a completion time to an individual source URL.
A cache hit additionally cannot establish a new network retrieval from that
message alone. The producer must persist a per-item collection record at the
tool boundary, keyed by Cron `run_id` and immutable source identity (at least
the canonical source URL and content digest). It must record the actual per-item source fetch time in an unambiguous
timezone and whether the result was fetched or served from cache. Provider batch
response or materialization time alone is not evidence of an individual fetch;
a cache hit needs verifiable provenance of the original fetch. The structured candidate must carry that
record or a digest-bound reference to it. Only then may the Publisher verify
all included item records, calculate their maximum as report `collected_at`,
and bind the request. This preserves the owner's collection-time requirement
without inventing a timestamp from scheduler, cache, or batch metadata.

The current Outbox code serializes legacy schema inspection and the nullable
endpoint-digest migration in one SQLite transaction. A synthetic concurrent
two-caller open of the same legacy Outbox now verifies that both callers retain
the unbound request rather than racing the column addition. It changes
no running Publisher, Cron, workflow, Compose configuration, network,
credential, or remote resource. The focused synthetic suite now reports 117
tests: 115 passed and two optional tests skipped, including rollback and retry.

### n8n inactive workflow import — isolated Native PASS

The earlier 45-second `--help` delay was traced to an I/O wait followed by
`EACCES` on the temporary n8n configuration directory, not to workflow parsing or import.
An exact n8n 2.43.6 container with `network=none`, read-only root filesystem,
non-root execution, a synthetic key, and a tmpfs owned by UID/GID 1000 with
mode 0700 imported the tracked inactive workflow into SQLite successfully
(exit 0, 31 seconds). The temporary container count is zero afterwards; the
existing main, worker, and two task runners remained healthy.

This is a narrowly isolated N8N_NATIVE import receipt. Queue execution,
activation, credentials, relay/Gateway network reachability, TLS/authentication,
durable Gateway persistence, alerting, outage/recovery, and regression of
existing email and workflows remain NOT_RUN. The synthetic key and isolated
database prove none of those operational properties.

### State, failures and later MCP

Outbox stores immutable original bytes and SHA-256 digests under
`(job_id, run_id)`, private directory 0700/files 0600. Replays deduplicate;
conflicts preserve original rows and an immutable conflict record. Delivery
states pending/sending/uncertain/delivered/failed/conflict distinguish
transport uncertainty. The delivery processor converts interrupted sending to uncertain after it acquires the lock; status alone does not.
A fake adapter may prove logic; only contract-defined durable receipts with
matching identity/request digest permit delivery. Reconcile before retry after
response loss; unknown results retain uncertainty. Bounded no-send retries
and permanent failure preserve diagnostic categories without raw content.

Metrics design reuses current Prometheus/Grafana: processed outcomes,
pending/uncertain count, retry count and oldest pending age; no payload/source,
credential or per-report labels. Alert thresholds require observed operating
cadence and operator agreement before activation. MCP is later read-only
`search_collected_news`, `search_business_ideas`, `list_review_candidates`,
`get_ingestion_status`, gated on stable HTTP and actual Hermes authentication /
n8n Queue persistent-session verification. No Blog-data MCP setting changes or
Vault mutation/publication authority follow from a search result.

### W80 synthetic evidence

The staging suite recorded RED before implementation and then 49 tests PASS
in 2.6 seconds on synthetic fixtures. Measured line coverage was 448/494
(90.69%); CLI coverage was 35/61 (57.38%), with subprocess execution not
tracked by that coverage run. This supports the source slice only and does not
prove production staging or delivery. Final frozen source verification passed 62 synthetic tests in 5.942 seconds using
`/tmp/hyhome-p04-qa-tools/bin/python -m coverage run --branch -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p test_*.py`.
Coverage for `*/publisher/*.py` was 93% (550 statements, 26 missed,
172 branches, 25 partial); CLI was 96%. Ruff check and format passed for
13 files. Independent code and security review of the final affected source
approved it with no unresolved critical or important findings. These synthetic
results do not establish the Gateway contract or Native delivery. A separate local source smoke
loaded the exact-SHA validator and staged actual news run `56780cdef19b495c8cf46df55da4e59c`
and business-idea run `7022eeab2ec44945b3cb6f277bc371fe` into a fresh private
temporary Outbox: two staged, exact replay duplicate, candidate/source bytes and
SHA preserved, idea snapshot count matched, and restart retained
`awaiting_contract`. Its own temporary directory was cleaned; no outbound call
was made. This is local Native staging PASS, not network or delivery evidence.
The prior metadata validation
failed with 146 cascading findings when the Work Breakdown table was separated;
the table was subsequently repaired. A further scoped check also failed with
146 findings, led by unsupported `BLOCKED` Evidence Result values and archive
type mismatches; the two Result values were corrected to `NOT_RUN` with blocked
reasons retained in Input. A subsequent registered check also failed with 146 findings, led by Criterion
Acceptance citing a combined Evidence value instead of one row; the reference
was corrected to the single evidence name. A subsequent registered
`check-document-metadata.py --mode check-changed` run with five explicit
changed paths passed (exit 0; selected=5, violations=0, legacy_exceptions=0,
transition_overrides=0). Its bounded snapshot began before subsequent
result-only Task updates; it does not establish validation of final unchanged
bytes or cover other README files.
Document-link alignment passed (1,171 documents, 9,487 links), with 232 existing
legacy warnings. Full links mode separately returned FAIL (1,171 documents,
9,489 links): `docs/05.operations/runbooks/01-common/0004-harness-agent-first-engineering.md:50`
references missing `graphify-out/GRAPH_REPORT.md`; 232 archive-link warnings
were also reported. Clean main full links passed (1,171 documents, 9,485
links, 232 warnings); the candidate FAIL was observed while its ignored graph
was being generated. The settled candidate full-links rerun passed (1,171 documents, 9,489
links, 232 existing legacy warnings), resolving the earlier candidate FAIL;
the baseline and alignment checks remain separate observations. `graphify update .` passed with 26,411 nodes and 49,331
edges while optional SQL and HCL parsers were unavailable. Existing P05 n8n
contract/rehearsal source tests passed 14 tests in 1.594 seconds. These are
distinct checks and do not establish Native delivery behavior.

CI gate attempts are separate from the Python 3.12.3 synthetic test PASS above:
`python3 scripts/validation/run-ci-gate.py --profile changed --requirements`
failed (exit 1, `ci-gate-requirements-context`) because hosted PR context is
required; this invocation did not run the gate. The `--profile changed
--local-only` attempt with Python 3.12.3 failed (exit 1,
`ci-gate-local-toolchain`) because hosted Python is 3.14.8; no selected gate
executed. The same local-only attempt with `python3.14` failed before the
runner with `ModuleNotFoundError: yaml`. No package was installed or bypass
used. CI remains NOT_RUN; explanatory output is not a gate PASS.

For the later local attempt, an isolated CPython 3.14.8 and 36 lockfile
dependencies were prepared from the existing cache. The local-only gate failed
before selected checks executed because that Python build lacks
`fcntl.F_ADD_SEALS`; this gate remains BLOCKED and no bypass was used. The
document metadata check selected eight documents and passed before this final
result-only update. The full document-link check passed with 232 legacy
warnings. The separate remote candidate gate is NOT_RUN.

After the portability changes, branch coverage with the opt-in reviewed
SPEC0247 validator at the exact path above passed 64 tests with no skips in
3.419 seconds: 550 statements, 25 missed, 172 branches, 24 partial, total
93%, CLI 96%; Ruff check and format passed for 13 files. An independent
reviewer ran the default environment with 64 tests OK and one skipped optional
real-validator test, and approved the final test changes. The portable
synthetic validator does not prove schema or Gateway compatibility. The earlier
62-test result remains a historical receipt. The registered eight-document metadata check subsequently passed (exit 0;
selected=8, violations=0, no exceptions or overrides). This evidence-only Task
update followed that check.

### Final read-only freshness observation

`git ls-remote origin refs/heads/main` returned
`4d540c870a746a10dfd0104351ea450106f8891f`. The `e065bce168f054c9a75fef97e0c4e029fbca7baa`
base is its ancestor; `git diff --name-only` between them lists only
`docs/03.specs/0182-home-residual-backlog/tasks/tsk-0003-recovery-and-auth-acceptance.md`,
outside this Task's owned files. No rebase, merge or remote Git mutation was
performed. Local source tests and documentation checks bind the e065 base and
remain source-only; latest-main integration and hosted checks are pending.
The final `graphify update .` passed with 26,414 nodes and 49,344 edges; the
optional SQL and HCL parsers remained unavailable.

### Follow-up integration observation — earlier revision

PR #684 candidate-quality run `41030161941` passed for its then-current head
`be0ee1b` and base `e0d68d`; changed head and main have not yet been revalidated
by that run. A later hy-home.docker main `b0c71ff` includes a separate 0182
PITR change. In Blog-data main `7c8b1e` and dev `18a2b`, the paths
`scripts/lib/ingestion/contracts/openapi-v1.json`, `ingestion-v1.schema.json`,
`responses-v1.schema.json` in that same contracts directory, and
`tests/workspace/fixtures/ingestion/synthetic-report.json` each returned 404.
The contract contents and a fixed accessible revision remain unavailable. The
last Gateway chat observation reported a synthetic container pass and ongoing
overall QA; the chat host is currently unavailable for a newer observation.

Upstream n8n 2.43.6 source indicates that the current stub's `responseNode`
setting without a connected response node causes a configuration error when
processing a request. Native import and activation remain NOT_RUN; this is not
an active workflow. PR CodeQL identified TLS 1.0/1.1 in the synthetic test
server; the test server was corrected to require TLS 1.2 or newer. Limited
loopback HTTP/TLS tests for that final revision passed 11/11 and independent
security re-review found no additional findings. Hosted candidate and CodeQL
checks for the new revision remain NOT_RUN. The user requested commit and push of the completed
scope followed by the contract wait; that request does not establish completed
Git integration or operational delivery.

### Current producer and isolated Queue evidence — 2026-10-30

PR #689 is merged. That merge does not close criterion 23: current evidence
still distinguishes source implementation from operating acceptance.

Hermes does not yet record a per-item actual collection timestamp at the
direct fetch boundary. The final tool-result conversion/call-ID linkage and
immutable source-item binding required to carry that record into the structured
candidate are also not implemented. Consequently, the existing 153 candidate
items remain held: neither scheduler time, batch completion time nor cache
materialization time is substituted for collection time. The publisher must
continue to reject dispatch until every included item has a bound direct-fetch
record and can derive report `collected_at` as the latest item record.

The isolated n8n environment passed owner and project setup, synthetic workflow
import/publish, and main/worker/task-runner health checks. Its synthetic webhook
returned HTTP 404; the database showed `active=true` with an `activeVersionId`,
but no webhook execution was recorded. Thus no Queue execution, worker/runner
round trip, or Gateway delivery was observed. Queue and Gateway evidence remain
NOT_RUN. All isolated test resources were removed and the observed production
n8n services remained healthy. A previously reported shell-pipeline “PASS” was
invalid and is explicitly excluded from this evidence.

### Isolated Queue publication and dispatch follow-up — 2026-10-30

The isolated n8n setup now uses the default workflow-publication API rather
than assuming an imported active version has registered a webhook. The
synthetic Webhook node has a stable `webhookId`, so n8n registers its configured
static path. This resolves the prior 404: the isolated webhook is registered
before its request is made. The tracked workflow's exact
path was also checked by the native helper in this isolated setup.

An isolated Queue run completed through the synthetic n8n main and worker with
an external JavaScript task runner. The fake Gateway returned `201` and the
test recorded the expected synthetic persisted-receipt evidence. This is an
N8N_NATIVE receipt for the isolated topology only. It does not execute the
tracked workflow against its configured endpoint, use a production credential,
or establish any server-B DNS, TCP, TLS, authentication, timeout, durable
receipt, outage/recovery, email, or existing-workload property. Those remain
NOT_RUN.

The direct-fetch timestamp experiment writes evidence only in a temporary
location and is not integrated into Hermes, its structured exporter, or the
Publisher. It therefore supplies no source admission for a candidate and does
not change the all-items collection-time hold. Likewise, an Outbox evidence
snapshot is retained for later verification only: it is not dispatch authority
and cannot cause a send, replay, activation, or credential use.

### Publisher evidence-bound staging follow-up — source/synthetic only

The current Publisher change makes the candidate/source snapshot and its opaque
companion evidence one atomic Outbox operation.  It keeps the existing identity
and digest checks under the delivery lock, so a restart or a concurrent caller
cannot expose a successfully staged snapshot without its selected evidence
bytes.  Repeating the same input remains idempotent; a different candidate,
source, or evidence for the same identity remains a conflict.  This is durable
local preservation only, not producer authentication.

The three approved Hermes job identities were tested with evidence present but
unverified.  None can be promoted to a request: `bind_request` rejects every
record while provisional evidence exists, and the per-job policy also requires
verified evidence.  Consequently all three delivery boundaries remain
`blocked`; the change cannot dispatch, replay, activate a workflow, or obtain a
credential.  The source-focused suite reported 134 tests, 132 passed and two
optional tests skipped, including restart and concurrent staging cases.  This
does not replace the separately recorded Gateway contract and Native evidence.

The experimental direct-fetch producer currently writes only beneath a
temporary directory and relies on same-UID local-writer trust.  It has no
reviewed durable producer identity, no authenticated handoff to the exporter,
and no recovery rule for a crash between fetch and evidence persistence.
Accordingly it is not an admission source for the Outbox, is not connected to
the Publisher execution path, and dispatch remains NOT_RUN.  A complete design
must eliminate that crash gap and bind each verified item record to the
candidate before calculating the report maximum `collected_at`.

Hosted CI evidence is limited to a pass for an earlier PR head.  It is not a
result for the present uncommitted Publisher change and must not be used as its
acceptance or merge evidence.  The current revision requires its own complete
checks after the final committed PR head is known.

### Post-PR #693 dispatch readiness — 2026-10-31

The owner assigned the Hermes direct-fetch receipt producer and exporter
integration to the server-A Hermes lane, and the Blog-data TLS entry point and
server settings to the server-B Blog-data lane. This repository defines their
contracts and acceptance conditions and does not change either side.

Observed state: origin/main and HEAD were `325dcb63c967` with a clean tree.
PR #693 merged at 2026-10-30T14:37:38Z with head `a1f0b33bd`; no PR was open. The
retained `codex/hermes-collection-provenance` worktree was clean. SPEC-0247 is
`approved` with its Task `completed`; PR #685 (validator) and PR #692 merged
2026-10-30. The user-reported 136 tests (135 passed, 1 skip) reproduced locally
on `325dcb63c`; the skip was the optional pinned-validator test. Hosted CI
Quality Gates succeeded for PR head `a1f0b33bd` and for main `325dcb63c`; those
runs are revision-specific and are not evidence for this branch.

Validator pin: the Publisher pinned `8c988c71…`, which is the pre-merge draft
from `edb6aa461` still present only under a temporary restore directory. Main's
`scripts/validation/check-hermes-candidate.py` is `957d047c…` (one commit,
`1003fbe8a`). The diff tightens staged-source traversal to directory handles
with `O_NOFOLLOW`, adds `regulation`, `expected_revenue` and
`profitability_claim` to idea items, requires `uncertainty` for devops items,
and validates idea/date paths more strictly. Over 120 parseable local scratch
exports, no file accepted or blocked differently in a relaxing direction: 30
accepted and 9 blocked by both, 58 invalid by both, and 23 accepted by the draft
but rejected by main for the changed field sets. The pin now names the main
bytes; the draft digest, changed bytes, symlinks and missing files are rejected
by tests, and the optional skip became a required compatibility test.

Gateway contract: Blog-data `dev` `1a4cd60` publishes OpenAPI 1.1.0. The input
schema and synthetic report are byte-identical to the pinned `a6d0957` files.
`POST /v1/ingestions` request, 200/201 receipt and error definitions are
unchanged, so the pinned revision and existing Outbox bindings stay. Only
`candidates` gained `matching`, `review_count` and `latest_review`, and review
definitions and `/v1/candidates/{id}/reviews` were added; those matter only to
later read tools. The API has no full-text search parameter.

Source added: Companion Evidence v1 structural verification
(`publisher/evidence.py`) with synthetic candidate/evidence fixtures, and a
`dispatch` command reusing `process_one`, `GatewayAdapter`,
`GatewayReplayTransport` and `HttpTransport`. For the three Hermes jobs the
policy gate returns `blocked` before evidence parsing or credential I/O, and the
existing Outbox and transport gates still block any record with bound evidence.
Synthetic loopback tests opened the gate only by patching policy and run times:
they observed 201 durable receipt and no resend, 401 and 409 `failed` without
retry, 503 and dropped responses `uncertain`, no reconciliation without
`--allow-replay`, then an identical-byte replay accepted with 200. Credential
files must be owner-only with an unshared parent; symlinks are rejected. The
full workload suite passed 151/151 with no skip, and Ruff check/format passed.
Independent security review found no Critical or Important issue; its Minor
findings on credential inode/parent checks and HTTPS URL parsing were fixed.
Independent code review found three Important issues, all fixed with tests:
microsecond `generated_at` was rejected by evidence parsing; a 401/403/409
received while reconciling an uncertain record left the retry budget open, so a
later replay could re-POST (shared `delivery.py` now exhausts the budget); and
the evidence-blocking test never reached evidence handling. The CLI now mirrors
both the policy and Outbox evidence gates before parsing or credential I/O, so
production dispatch reads no credential. Without `--allow-replay`, uncertain
records consume attempts without I/O and stay uncertain after five; this is
documented rather than changed. Separate counts for rejected evidence are not
added. A follow-up review of the fix range is recorded in Review and Completion.

Network observation from server A: `192.168.0.22` answered ICMP, while TCP
22/80/443/8787 did not connect within 3 seconds. No approved TLS entry or DNS
name exists yet, so the tracked workflow keeps `https://gateway.invalid` and
`active:false`. No Hermes live candidate root was found outside scratch
directories at that point (superseded below by the live exporter root); the
recorded 153 held items remain a 2026-10-30 observation and no collection
time was estimated. No Cron, secret, workflow, container, network
or remote Git state was changed.

### Handoff: Hermes producer lane (server A)

Deliver per run a Companion Evidence v1 file exactly as defined in the workload
README `Companion Evidence v1 계약` section; candidate producer v1.0.0 fields stay unchanged.

1. Record each item at the direct-fetch boundary: tool call identifier, final
   HTTPS URL, 2xx status, SHA-256 of the decoded response body, receive time
   with offset (millisecond precision), `complete` status and cache provenance. A cache hit records the original fetch time and cache
   key digest, never the materialization time.
2. Persist the record atomically (temp file, fsync, rename) before the fetched
   bytes are used, closing the crash gap between fetch and evidence.
3. Bind records to `job_id`, `run_id`, `scheduled_at` (the execution
   `scheduled_instant`) and the SHA-256 of the exported candidate bytes, one
   record per candidate item in the same order; items without a source URL
   make the whole run unverifiable.
4. Producer authentication is decided (2026-10-31): a restricted producer
   account outside the LLM tool and exporter account holds an Ed25519 key and
   signs each finished Companion (workload README, Producer authentication).
   Provide that account, the public key and custody/rotation evidence for
   review; adding the key to `producer-keys.json` is the trust-anchor step.
5. Write to `<evidence-root>/SHA256(job_id NUL run_id).json` and validate
   against `tests/fixtures/companion-*-v1.json` plus `publisher/evidence.py`.

Also re-align the exporter with the SPEC-0247 validator: either regenerate or
retire pre-change exports, and change `schema_version` whenever the item field
set changes. Mapping from the current `acquisition_receipt.py` to Companion v1: one
Companion per run built from that run's receipts in candidate item order;
`canonical_url` to `source_url` and `fetched_url`; `content_digest` to
`body_sha256`, with the definition fixed to the decoded response body;
`acquisition_completed_at` to `fetched_at`; `acquisition_mode` to `cache.hit`,
with the origin receipt's time kept as `fetched_at` for cache hits;
`tool_call_id` unchanged; only `success` maps to `complete`, so
`partial_failure` blocks the run. Sign the finished Companion from the
restricted producer account and write the `.sig` before the Companion.

Acceptance: real runs verify with zero rejections; crash injection between fetch
and write yields no unbound item; a forged record from the exporter account is
rejected by the approved mechanism.

### Handoff: Blog-data Gateway lane (server B)

1. Keep the Gateway on loopback `127.0.0.1:8787`; expose it only through an
   approved TLS terminator on `192.168.0.22` with a DNS name resolvable from the
   n8n worker on server A and a certificate chain the worker trusts. Server B is
   Windows 11 with WSL2: report where Docker Engine runs, whether WSL uses NAT or
   mirrored networking, the Windows firewall rule for 443 limited to source
   `192.168.0.13`, and the CA the worker must trust.
2. Restrict the entry to server A (`192.168.0.13`) and the paths
   `POST /v1/ingestions` and `GET /v1/ingestions/{id}`; later read tools need
   `GET /v1/candidates` and `GET /v1/summary` only.
3. Issue a producer-bound ingest credential for n8n and, separately, a read
   credential for later tools; deliver both through the operator secret path,
   never in workflow JSON or logs, with a rotation and revocation procedure.
4. Report the DNS name, port, CA or chain fingerprint, timeout expectations and
   rate limits so the HTTP Request node and Native checks can be bound exactly.

Acceptance: from the n8n worker, DNS/TCP/TLS succeed, an invalid token returns
401, a wrong certificate fails, and a synthetic tenant ingestion returns 201 then
200 for the identical request and 409 for a changed body, all durably visible
through `GET /v1/ingestions/{id}`.

### Live candidate and Hermes-lane alignment — 2026-10-31

A read-only scan of the live exporter root
(`~/storage/research/hermes-report-export/out`, Cron `84d3f689378b` every five
minutes) found 14 candidates for the three admitted jobs with 193 items (news
57, devops 96, ideas 40), 119 of them carrying a source URL, plus five blocked
private-infra candidates. The earlier 153-item figure is superseded by this
observation and none of these items has a direct-fetch record. Under main's
pinned validator eight admitted candidates pass and six fail: three devops
exports from 2026-10-28 to 2026-10-30 lack `uncertainty`, and three idea exports
lack `regulation`, `expected_revenue` and `profitability_claim`. All six still
declare `schema_version` 1.0.0, so the producer changed its field set without a
version change. The Hermes-lane handoff note reports 18 of 19 passing with its
own inline validator, which therefore differs from the SPEC-0247 validator.
Those files were not modified here.

The same note lists receipt minimum fields beyond the first v1 draft. Because no
producer emits v1 yet, the contract now also requires per-item `tool_call_id`
and `status` (only `complete` verifies) and defines `body_sha256` over the
decoded HTTP response body. The Hermes note's trust-boundary position (same-UID
JSON plus SHA-256 is not authentication; prefer a restricted producer account,
protected handoff and independent verifier) matches the admission condition
above. The controller ran the suite: 151/151 with the added rejection subtests.

### Producer authentication and gate unification — 2026-10-31

Start state: origin/main `31b92f95e`, local main fast-forwarded and clean; the
earlier Codex worktree no longer exists and no PR was open. Main's validator
is still `957d047c…`. This slice changes no Manifest Outbox, other workflow or
Ollama overlay.

Producer review. The Hermes lane added `acquisition_receipt.py` (source only,
not wired to Cron). It writes one receipt per acquisition with temp file, fsync
and hard-link publication, and a per-receipt "companion" bound to a candidate
digest. Differences from the consumer contract: it is not a per-run Companion
v1 document; `partial_failure` is accepted as bindable; its digest definition
says raw response bytes; and producer identity is a self-declared string written
by the same account, so it is not authentication. The required mapping is in
the Hermes handoff below.

Contract drift cross-check. Both validators ran on one copy of the live export
root (19 files, manifest digest `8d412898b839bdc4`): main `957d047c` passes 8,
blocks 5 private-infra candidates and fails 6; the Hermes inline validator
`f454020c` passes 18 and fails 1 idea candidate whose idea source is gone. The
two disagree on five pre-change 1.0.0 candidates (three devops lacking
`uncertainty`, two ideas lacking `regulation`, `expected_revenue` and
`profitability_claim`) and on the private-infra verdict. Policy decided here: a
field-set change requires a new `schema_version`; same-version candidates with a
different field set are not compatible; pre-change files stay in place and are
never staged; Hermes may re-export from source under a new version without an
Outbox conflict because those runs were never staged; and the Hermes pre-save
check must judge identically to `957d047c`.

Authentication design (single decision). A restricted producer account, separate
from the Hermes LLM tools and exporter, holds an Ed25519 key and signs the final
Companion v1 after the candidate is fixed. The detached signature
(`hermes-companion-signature/1`, message `hermes-companion-evidence/1` NUL plus
the Companion bytes) is written before the Companion and stored with it by
`stage --evidence-root`; Outbox keeps it immutable. The Publisher reads only
public keys from the tracked `producer-keys.json` (job scope, validity window,
retroactive `revoked_at`, unique `key_id`). HMAC was rejected because the
verifier would hold the forging key on the same account. The tracked store is
empty, so every Hermes job remains blocked.

Gate unification. `trust.authorize` is now the one decision consumed by
`dispatch` (before credential I/O), `process_one`, `Outbox.bind_request`, and
`GatewayReplayTransport` send and reconcile, which re-authorize and compare the
request's trust token; `HttpTransport.send` requires that token for
evidence-required jobs as defense in depth. No gate opens alone, and a key
revoked after request binding closes binding, processing and replay. Request
bytes, idempotency key, destination, contract revision and endpoint binding are
unchanged. The Publisher HTTP timeout moved from 10 to 45 seconds so that it
outlasts the workflow `executionTimeout` (30 seconds) and its Gateway request
(20 seconds) while staying under the Traefik v3 default `readTimeout` (60
seconds); a test asserts that order and that no workflow node retries.

Ingress design (not applied). The existing `n8n` router keeps SSO. When the
production path is fixed, a separate router admits only that exact webhook path,
POST and an A-internal source, authenticated by n8n `headerAuth`; `/webhook/*` is
not opened. Publisher-to-A and Worker-to-B trust and tokens stay separate, and an
A-host probe is not Worker evidence.

Independent security and code reviews found no Critical issue. Their Important
findings were fixed: the runtime check requires `python3 -I` and that the key
store, every publisher module and the `cryptography` package, with all
ancestors, are neither owned nor writable by the running account (a checkout
therefore cannot be a trust anchor; an isolated run from this checkout returns
`store_unprotected`), a replay test now drives a genuinely uncertain bound record and shows
reconcile reaching the network with a valid key and not after revocation,
trust-blocked in-flight records count as `uncertain` with exit 1, and a trust
failure inside request binding returns `blocked` instead of a terminal
`failed`. Minor fixes: every store entry is validated, duplicate public keys
are rejected, 401 after a lost response is tested, the pre-signature Outbox
migration is tested, and stale docstrings were corrected. Not changed: rejection
codes are not yet written as events, and `cryptography` (system package 41.0.7
here) is not declared as a dependency.

A re-review of the fix range confirmed the four Important fixes and raised the
remaining library/interpreter gap, closed by the runtime check above; the
Publisher must also run as a dedicated account distinct from the Hermes tools so
that the Gateway credential is unreadable to them. Remaining Minor notes: no
test injects a trust change between `process_one` and `bind_request`, such a
race on an uncertain record is counted `blocked`, and root execution always
blocks.

Synthetic results on the controller: the workload suite passed 165/165 with no
skip, adding real-signature dispatch (201, no resend, 401/403/409 without retry,
outage and dropped responses reconciled only by identical replay) and trust
negatives (forged key, tampered bytes, unknown key, malformed envelope, other
run, other candidate digest, revoked, expired, not-yet-valid, wrong job scope,
duplicate key id, bad public key, missing store, unsigned same-account JSON,
immutable signature, restart, revocation after binding). Ruff passed. These
results do not replace the earlier 151/151 for the prior revision. Server B
TCP 22/443/8443 still did not connect from server A.

### Protected install and ingest-only contract — 2026-10-31

PR #696 carried the producer verifier above; the owner merged it at head
`7629bbad4` as `82dadf586` (2026-10-31T03:37:58Z) before this slice was pushed.
This slice is a separate follow-up PR from `feat/hermes-protected-install`; it
does not re-implement `trust.authorize`,
the key store format or the 165 earlier tests.

- Runtime protection was weaker than its comment: it accepted any file not owned
  by the running uid (so a Hermes-owned file passed) and checked only the
  `cryptography` directory, not files under it or the interpreter. It now
  requires every component of the interpreter, `sys.prefix`/`pyvenv.cfg`, each
  import path, every loaded module file (signature modules imported first),
  each Publisher module and the key store to be root-owned, free of group/other
  write and unwritable by a non-root runner. The key store moved to
  `publisher/producer-keys.json` so an installed copy sits beside its verifier.
- `cryptography` is declared in `pyproject.toml` and locked with hashes in
  `requirements.lock` (cryptography 46.0.7, cffi 2.1.1, pycparser 3.12;
  `uv pip compile` for CPython 3.12 x86-64 manylinux). `install.py` installs one
  immutable `/opt/hermes-publisher/releases/<commit>` from `git archive` of a
  commit (commit id from the pax header, which the installer cannot verify, so
  the checkout, archive and installer must be root-only), taking only an
  explicit Publisher module allowlist,
  the store and the lock, with `--require-hashes --only-binary :all:` into a new
  venv, removing pip and sealing every path root-owned without group/other
  write. `verify-install` reports `{"keys": N, "runtime": "protected"}` or a
  value-free code.
- `tests/install-check.sh` installs the commit in a disposable root container
  and, as separate `hermes-publisher` and `hermes` accounts, proved 17/17: a
  non-root-owned archive and a prefix under a Hermes-owned directory are
  refused, the dedicated account loads the release, the installed files match
  the archive manifest, producer modules are not installed, neither account can
  write code, store, library, venv config or interpreter, non-isolated runs and
  root runs are refused, PYTHONPATH is ignored, and a Hermes-owned library
  sub-file, group-writable store, Publisher-owned module, Hermes-owned
  `pyvenv.cfg`, other-writable import directory and Hermes-owned interpreter
  each fail closed and recover once restored; reinstalling a release is
  refused. The container used the image Python, not the A host interpreter.
- Independent review found no Critical issue; its Important findings were
  fixed with failing tests first: installer takeover of a non-root prefix,
  non-root archive, producer modules in releases, the credential child running
  the unresolved venv `bin/python`, its `ssl`/`http.client` files unchecked, and
  a manifest check that could not fail. The runtime check is a tripwire over a
  sealed release: bytecode caches, `.pth` files and code that ran before it are
  protected by root ownership, not by the check.
- Dispatch output adds value-free `reasons` counts per rejection code.
  `uncertain`, permanent rejection and exhausted retry keep exit code 1.
- Timeout semantics were corrected: Traefik v3 `readTimeout` (60 s default)
  bounds only reading the request and no upstream response or write timeout is
  configured, so the Publisher 45 s attempt (queue wait included) is the outer
  bound over `executionTimeout` 30 s (from worker start) and Gateway 20 s. The
  check now asserts no shorter Traefik upstream timeout and no workflow retry or
  schedule.
- B contract: A sends only `POST /v1/ingestions` with an ingest-only token and
  holds no GET or read permission; response loss reconciles only by explicit
  identical-byte, identical-key re-POST (`--allow-replay`). MCP read is a later,
  separate path and token. `blog-ingest.hy.home.arpa` must resolve to
  `192.168.0.22` inside the n8n worker; host `/etc/hosts` does not reach
  containers, so an internal DNS record or worker `extra_hosts` is required
  (DNS/Compose approval, not applied). Server B is Windows 11 + WSL2 NAT: the
  Windows 443 listener, WSL forwarding and a firewall rule limited to
  `192.168.0.13` are canonical; the existing Windows Vault is not migrated.
- The Hermes producer receives the canonical contract from `trust.py`: `DOMAIN`,
  envelope fields, raw 32-byte public key, key id pattern, exact job scope,
  validity window and retroactive revocation. Admission needs protected
  generation/custody evidence and an out-of-band SHA-256 fingerprint of the raw
  public key; private and synthetic keys never enter the repository or
  Publisher. Unsigned rows staged earlier stay blocked; signatures are immutable.
- `publisher/acquirer.py` and `publisher/producer_sealer.py` had been committed
  on this branch as `f044fb85c` by another lane, outside this Task (the sealer
  handles a private key; an automated review flagged SSRF in the fetcher's
  redirect handling). With owner approval the commit was moved to the local
  branch `hermes/acquirer-sealer` and is not part of this follow-up PR. `install.py`
  installs only an explicit Publisher module allowlist in any case; review and
  placement of producer code belong to the Hermes producer lane.
- CI does not run this workload's suite (no gate entry, `cryptography` absent
  from the controller lock); the 168 tests and the install check are local
  evidence only.

Approval units still open, none performed: A host `hermes-publisher` account;
`/opt/hermes-publisher` install; outbox and credential file placement; systemd
service/timer; producer key admission PR; A exact-path ingress router; worker
DNS/`extra_hosts`; workflow URL/credential binding and publication.

### Hermes host direct path with the Gateway on server A — 2026-10-31

Owner redirect: Hermes (server-A host process) submits directly to the existing
n8n webhook; n8n forwards to the Blog-data Gateway hosted on server A; Windows
server B later pulls from a Blog-data Export API and acknowledges. The owner
chose to park the unmerged `feat/hermes-research-feed` branch (A-owned pull feed,
commit `c253024ea`, never pushed) and to deliver repository changes plus a
disposable synthetic E2E only. Open draft PR #698 (another lane, documentation
only, failing `candidate-quality`) supplied the prompt and is not merged by this
slice.

Disposition of existing parts:

| Part | Disposition | Reason |
| --- | --- | --- |
| `workflow.json` | MODIFY | Path `hermes-blog-ingestion-contract-hold` → `hermes-blog-ingestion`, URL `https://gateway.invalid/...` → `http://blog-ingestion:8787/v1/ingestions`; both old values were accident guards, now carried by `active:false` and absent credentials |
| Publisher `stage`/`dispatch`, Outbox, trust, install | NO_CHANGE | Recovery path to the same webhook via `--endpoint`; no second Outbox |
| Blog-data Gateway | IMPLEMENT (hosting only) | `blog-ingestion` service, own profile, image built locally from pinned Blog-data `cbf06c3514970f8ffa86dafa18064bfd3931e06a`, `pull_policy: never` |
| `n8n_blog_ingest_net` | IMPLEMENT | Root network, internal, isolated gateway mode, `10.250.20.0/24`; members `n8n-worker` and Gateway only |
| Exact-path Traefik router | IMPLEMENT (proposal) | `traefik/hermes-webhook.yml` outside the live `dynamic/` directory |
| Server-B TLS entry, `blog-ingest.hy.home.arpa`, WSL2 notes | RETIRE | Gateway no longer runs on B; history above is kept |
| Windows Export/ACK | BLOCKED | Blog-data has no Export or ACK API at the pinned commit |
| Hermes `submit_research_report` plugin | BLOCKED (Hermes lane) | Contract: POST the Gateway v1 report to the webhook with header `X-Hermes-Ingest-Token` |

Facts measured for this slice: the Gateway at the pinned commit serves only
`POST /v1/ingestions`, `GET /v1/ingestions/{id}`, `/v1/candidates`, `/v1/summary`,
reviews and capture; its body limit is 1 MiB and its config stores only token
SHA-256 digests. Operations catalog rules forbid new services and shared root
networks in overlays, so the Gateway is a base service (SPEC-0219 storybook
precedent). Traefik is published only on `192.168.0.13:443`. One SSO-protected
request from the A host to that address appeared in the live Traefik access log
as `192.168.0.13` (302), not the `edge_net` gateway, so the proposed allowlist is
`192.168.0.13/32`; the independent review caught the earlier loopback-based
assumption. The live Traefik runs `v3.7.14` while Compose pins `v3.7.16`
(drift noted, not changed here). Two builds of the same Blog-data commit produced
different image IDs, so the operational build records its own ID.

Disposable E2E (`tests/e2e-ingress.sh`, Traefik published on the LAN address as in
production, Blog-data `cbf06c3`, image
`sha256:03bfcbb2…`, `hyhome/n8n:2.43.6-local` with the upstream entrypoint,
Compose-pinned Traefik), 16/16 PASS: native import and publication of the tracked workflow;
host POST 201 with `persisted:true`; identical replay 200 duplicate; same key
with changed content 409; missing webhook token 403; invalid shape 400
`INVALID_REQUEST` without echo; body above 1 MiB 413 at Traefik; GET on the path,
another webhook path and the n8n UI all stay behind the SSO stand-in (401);
non-host source 403; a host process dialling the LAN address observed as that address; Gateway
stopped → 500, never 2xx; after Gateway restart the replay is a persisted 200
duplicate (SQLite survived); the host cannot reach the Gateway on the isolated
network; a burst above the route limit returns 429. Synthetic tokens only; all
disposable containers, networks and volumes were removed. Not covered: Hermes
plugin, real tokens, live Traefik, worker/Valkey queue mode, runner restart and
a 7-day Windows outage (no Export API).

Trust boundary: on the direct path only the webhook token identifies the
producer; it does not replace Publisher Ed25519 Companion verification. Direct
submissions therefore stop at Gateway `received` and review; capture is not
configured on A. A signed-report contract for the direct path needs a versioned
Blog-data/Hermes decision first.

Approval units added, none performed (RUN-0053 "서버 A Gateway 배치와 직접 제출
경로"): local image build; data/config paths with token digests; Gateway start and
`n8n-worker` recreation; two n8n credentials; workflow publication; Traefik route
copy after measuring the live host source; Gateway backup connection.

### Attestation, Resource Export and Windows pull — 2026-11-01

Owner decisions for this slice: a separate host attester signs Blog-data
attestations (not OpenBao Transit, not deferred), and PR #700 (Hermes plugin,
Hermes workspace) stays with its owner. Base `main` `bc78e354a` (PR #699 merged);
Blog-data `dev` `cadea2e683fb3e03e0e7a9f27133421c981bbea8` (PR #637 head) is the
accepted Gateway source; Blog-data `main` is not used.

| Part | Disposition | Reason |
| --- | --- | --- |
| Gateway image pin | MODIFY | `cbf06c3` (no Export) → `dev` `cadea2e`; source binding rehashed, tech-stack and inventory regenerated |
| `blog_export_net` | IMPLEMENT | Root network, internal, isolated, `10.250.21.0/24`; members Traefik and the Gateway only; no published port |
| Export and attestation routes | IMPLEMENT (proposal) | `traefik/blog-export.yml`: B `GET` list/manifest/file and `POST` ACK, A-host `POST` attestation; nothing else routed |
| Attester | IMPLEMENT | `publisher/attestation.py` + `cli attest`: rebuilds the dispatch bytes from producer-signed evidence, own account and key, never reads the Outbox |
| E2E build | MODIFY | Sparse set read from the Dockerfile's `.dockerignore` allowlist (`tests/gateway-image.sh`); Gateway hardening rendered from Compose |
| Upgrade/restore check | IMPLEMENT | `tests/e2e-upgrade.sh` |
| `workflow.json`, webhook route, Publisher dispatch/Outbox, trust | NO_CHANGE | Reused as merged in PR #699 |
| Hermes plugin source | NO_CHANGE (Hermes lane) | PR #700 merged as `3727ff0e7` during this slice; all four files match the installed `~/.hermes/plugins/research-report` by SHA-256; read-only check: POST to the allowlisted URL, header `X-Hermes-Ingest-Token`, no redirects, durable local outbox, strips `companion_evidence` — consistent with `workflow.json` |
| PR #698 (draft) | Superseded, not merged | Describes the pre-#699 `contract-hold` path and an Export API "to be added"; this slice and PR #699 implement the current design |
| "Export/ACK API absent" statements | RETIRE | README, RUN-0053, spec and policy row corrected; dated history above is kept |

Measured facts: the `dev` Gateway adds `attest`, `export_read` and `export_ack`
scopes, at most one non-`read` scope per credential, and
`POST /v1/ingestions/{id}/attestations`, `GET /v1/exports`, `/v1/exports/{id}`,
`/v1/exports/{id}/files/{seq}`, `POST /v1/exports/{id}/acks`; DB schema 3 upgrades
schemas 0-2 in place. The attestation message is
`blog-data-attestation/1\0` + canonical `{producer, job_id, run_id, fire_id,
source_sha256, content_sha256}`; the Python signer reproduces Blog-data's own
`attestationMessage` byte for byte (vector fixture computed inside the built
image). Only jobs `6eabd835f969`, `25674fbc0bf3`, `8d0925bc571d` become `ready`.
The served certificate is mkcert with SAN `*.hy.home.arpa`, so
`blog-export.hy.home.arpa` needs no new certificate. OpenBao has no Transit
engine. Plugin reports carry no producer-signed evidence, so they stay
`ingested` and are never attested.

Disposable E2E `tests/e2e-ingress.sh`, 51/51 PASS after review fixes (Blog-data
`cadea2e`, image `sha256:31900db2…`, `hyhome/n8n:2.43.6-local`, Traefik `v3.7.16`): the earlier
16 scenarios plus image template check, Compose-rendered hardening, wrong webhook
token 403, trailing-slash and case-changed paths 401, no export before
attestation, `export_read` cannot attest 403, signature over changed items 422,
unregistered key 422, trusted attestation 201 `ready`, replay 200, unapproved job
201 `held` `UNKNOWN_JOB` with file 409, six Resource files matching manifest
SHA-256/length/UTF-8, missing/wrong token 401, cross-scope 403 both ways, ACK 201,
replay 200, different ACK 409, summary/ingest/GET-attest/dot-segment/webhook on
the export host 404, and after a Gateway restart the acknowledged export, ACK
replay and attestation replay all persist; the host reaches neither isolated
network; and a Publisher-adapter body rebuilt by `verified_request` from synthetic
producer-signed evidence persists through n8n and its attestation yields `ready`
exports, so the `attest` signing path matches the Gateway's stored fingerprint.
`tests/e2e-upgrade.sh` 10/10 PASS: `cbf06c3` writes a schema-2 store and
backs it up online; `cadea2e` upgrades it to schema 3 with the receipt intact,
replays as a duplicate, attests it into a `ready` export; both backups restore
into fresh volumes. Workload unit suite 193 tests (attestation 16, export route 4).

Not covered: the real Windows receiver (`receive-hermes-exports.ps1` needs
Windows PowerShell 5.1 on B), the per-router source split in one-host E2E (static
test only), live Traefik `v3.7.14`, real tokens and keys, and the production
attester account.

Approval units added, none performed (RUN-0053 15-step sequence): image build;
pre-change SQLite backup; config with four single-scope tokens and the attester
public key; Gateway start; worker recreation; attester account, key and token;
n8n credentials; workflow publication; webhook route; Traefik recreation onto
`blog_export_net` and export route copy after measuring both sources; Windows
dry run; real receive and ACK; backup connection.

### Remaining blocked conditions and recovery

- DELIVERY stays BLOCKED until both handoffs are accepted and a reviewed key is
  added to `publisher/producer-keys.json` and installed as a protected release;
  the gates already consume one trust decision,
  so no further gate change is planned for admission.
- Then: bind the workflow URL and credential reference, publish the workflow
  through the approved procedure, and run the W83 Native scenarios (outage and
  recovery, lost response, bad token/certificate, worker/runner path, sensitive
  input blocks, Cron/email regression, source/Outbox/Gateway preservation).
- Recovery keeps source, Outbox and Gateway data; `failed` records are never
  reopened automatically; uncertain records resolve only by explicit
  identical-byte, identical-key replay, because A holds no read token (RUN-0053).

### Server A operational rollout — 2026-11-01

Owner decisions: keep Export closed and design the trust adapter separately (no
`export` block, so an authorized attestation would get 403 `EXPORT_DISABLED`;
with no `attest` token issued, every attempt stops at 401 first); approve RUN-0053
Gateway start, Worker network join, n8n credentials and publication, and both
Traefik routes. Base `main` `6e6df4005`. Blog-data `dev` moved to
`a43d824334e636ddeab034982b36c0700a9d8f93` (PR #640): the ingestion and Export
API are unchanged, the renderer is `resource-export/2`, and the RFC 8032 test key
is now refused as an attestation key. No Export existed, so no `ready` manifest
or Markdown was re-rendered.

Read-only survey before change: no Gateway container, volume, data directory or
production image; `n8n_blog_ingest_net` absent; `blog_export_net` held only
Traefik (v3.7.16, recreated earlier the same day). The installed plugin matched
`hermes-plugin/` byte for byte (`research-report` 0.1.0, doctor OK) but had no
webhook URL (default `https://n8n.local/...`) and no secret file; its one
`delivered` Outbox record went to a local stand-in at `127.0.0.1:18787`, not to
n8n. Cron `6eabd835f969`, `25674fbc0bf3` and `8d0925bc571d` reference
`submit_research_report`; `3c3f81a925e0` does not. `publisher/producer-keys.json`
is empty, no producer or attester account exists, and the only producer-side
sealer is the unreviewed, untested branch `hermes/acquirer-sealer` (`f044fb85c`).

| Unit | Result | Evidence |
| --- | --- | --- |
| 1. Source pin | PASS | Compose, wiring test and registry pin `a43d824…`; source binding rehashed `4a5f070d…` → `497a9a7b…`, previous binding archived |
| Synthetic E2E at the new pin | PASS | `e2e-ingress.sh` 51/51; `e2e-upgrade.sh` 10/10 (`cbf06c35` schema 2 → `a43d824` schema 3) |
| 2. Image | PASS | `gateway-image.sh` sparse build of `a43d824…`; image ID `sha256:e513b938721f38c201ade72b7d2fef2bb50c32aa78061b099e8f1fa4fe1c7804`; no registry digest; templates, profile registry and research map present; in-image `template_version` `resource-export/2+f45cc9bbc0a4` |
| 3. Backup | NOT_APPLICABLE | No earlier store existed |
| 4. Paths and config | PASS | `${DEFAULT_WORKFLOW_DIR}/blog-ingestion/data` 0700 and `config.json` 0600, both UID 10001, on local ext4; credentials `ingest` and `read` only (SHA-256 digests), no `attest`, `export_read`, `export_ack`, `capture` or `export` block. Raw tokens sit in owner-only files outside Git |
| 5. Gateway start | PASS | `up -d --no-deps --no-build --pull never blog-ingestion`: healthy, user 10001, read-only root, caps dropped, no published port, `export_enabled:false`, DB schema 3; unauthenticated summary 401, `read` token 200 with empty totals |
| 6. Worker network | PASS (deviation) | `docker network connect n8n_blog_ingest_net n8n-worker` instead of recreation: the worker runs with the extra `docker-compose.ollama-local.yml`, which a root-only recreation would drop. Worker → Gateway 401; n8n main cannot reach the Gateway |
| 7. Attester | BLOCKED | No producer key, producer account or attester key; Export closed by owner decision |
| 8. n8n credentials | PASS | Two `httpHeaderAuth` credentials imported from stdin (`HermesIngress001`, `GatewayIngest001`); stored ciphertext, neither token present in the export |
| 9. Workflow | PASS | Tracked `workflow.json` imported as `HermesBlogIngest` and published; the CLI publication needed one `docker restart n8n` (only active workflow). Internal webhook without or with a wrong token: 403 |
| 10. Webhook route | PASS | `hermes-webhook.yml` moved into `dynamic/` with `gateway-standard-chain@file` after the allowlist (POL-0013), registered in `RouteAuthContractTests` and the POL-0079 table; source re-measured `192.168.0.13`; host POST reaches n8n header auth (403), GET, other webhook paths and the UI stay on SSO (302) |
| 11. Export route | PASS (A side) | `blog-export.yml` moved into `dynamic/` with the same chain and registration; from A: Export read and ACK 403 (allowlist), attestation reaches the Gateway (401), every other path 404. B's source is measured at its dry run |
| Hermes URL | NOT_RUN (owner) | `~/.hermes/.env` is outside this agent's permitted paths; the secret file `~/.hermes/secrets/research-webhook.secret` (0600) exists and matches the n8n credential |
| 12–15 | NOT_RUN | Windows dry run, real receipt, ACK and restart/restore checks wait for real Cron submissions and the trust design |

Rollback: delete either route file; `docker compose ... stop blog-ingestion`
(data directory kept); `docker network disconnect n8n_blog_ingest_net n8n-worker`;
`n8n unpublish:workflow --id=HermesBlogIngest` then restart n8n. Lanes:
SOURCE PASS, INTEGRATION PASS, TRUST BLOCKED, RECEIVER NOT_RUN, OPERATIONAL NOT_RUN.

Blog-data handoff: RUN-0009 at `dev` `a43d824` still shows
`"base_url": "https://ingestion.hy.home.arpa"`; the live router is
`https://blog-export.hy.home.arpa`, so that example needs correcting in Blog-data.
`allowed_template_versions` takes `resource-export/2+f45cc9bbc0a4`.

Review: an independent read-only review found one Critical issue — the moved
routes failed `RouteAuthContractTests` and POL-0013 (no standard chain, no
named authentication). Fixed test-first: the route tests now require
`gateway-standard-chain@file` right after the allowlist (RED→GREEN), the four
routers carry it live, the E2E Traefik receives the real chain parts, and the
routers are listed with their authentication. Important findings (stale
evidence rows, section placement) and the binding wording were corrected.

### Trust adapter design — 2026-11-01

Owner-approved design for the component that opens Export. Decisions marked
as the owner's were answered directly; the read endpoints, n8n screen key,
job limit placement and `cli attest` move are the controller's calls,
accepted with the design. Handoff prompts for the Blog-data and Hermes
workspaces carry the matching contract and test steps. Implementation in this
repository starts once the Blog-data `attestation/2` contract is merged on
`dev`, so its final field names and bounds are pinned, not guessed.

#### Intent

Hermes Cron reports reach the Blog-data Gateway on server A as `received`
through the direct path (Hermes plugin → n8n → Gateway, PR #699/#703). Nothing
may become an Export `ready` (and so reach the Windows Vault) unless a
component that is not the LLM has proven, per item, that the cited source is
real and says what the item quotes. Export is closed today (no `export` block in
the Gateway config) because no such component exists.

The owner wants to stop three things:

1. Sources or acquisition times invented by the LLM.
2. Content changed between submission and the Vault.
3. Unapproved jobs mixed in.

#### Goals

- Per-item verification: an item reaches `ready` only when its source URL was
  fetched by the verifier, its quotes appear verbatim in that page, and its
  numbers/dates/Latin-script proper nouns appear in those quotes or the page.
- Partial reports pass partially: verified items go to the Vault, the rest stay
  `held` with reason `SOURCE_UNVERIFIED` on server A (owner decision).
- Acquisition time is the verifier's clock at fetch, never an LLM-written value.
  The Vault note shows the verifier's per-item `fetched_at` and `final_url`
  (owner decision); the LLM-written `collected_at` is shown only as the report's
  writing time.
- One signature binds report content, the verified item list and the evidence.
- Rendering stays Blog-data's: Resource templates and the profile registry
  (`resource-export/2+…`); the verifier pre-checks required profile fields and
  does not sign items that would fail rendering.

#### Non-goals

- No model-based judgement (owner decision: no judge model). An item whose quotes
  are real but whose summary misreads them is left to human review: Blog-data
  writes Hermes notes as `draft` ("before a person checks the source"), and the
  owner accepted that this review covers the gap.
- No change to the direct submission path's shape, the Publisher Outbox or its
  dispatch. The n8n "Screen Ingestion" allowlist gains `source_quotes` only
  (one-key change, republished as an approved ops unit).
- No new service on Windows B; no Hermes migration to Docker.

#### Anti-goals (failure even if it works)

- A report reaches `ready` with a time or source the verifier did not observe.
- Any manual "trusted=true", force flag or bypass path.
- The signing key readable by Hermes, n8n, the Publisher or the repository.
- Fetched page text treated as instructions anywhere.

#### Decided shape

##### Blog-data contract change (Blog-data lane, `dev` PR first)

- Item schema gains `source_quotes`: 1–3 strings per item, original language,
  bounded length (builder picks bounds with Blog-data; suggest ≤ 500 chars each).
  Optional at ingest so existing producers keep working; an item without quotes
  can never be verified.
- `attestation/2`: the signed message adds `verified_items` (sorted by
  `item_id`, each `{item_id, fetched_at, final_url}`) and `evidence_sha256` to
  the v1 fields `{producer, job_id, run_id, fire_id, source_sha256,
  content_sha256}`, under a new prefix `blog-data-attestation/2\0`. Body gains
  the same two fields.
- Gateway: candidates whose `item_id` is not in `verified_items` are `held` with
  new reason `SOURCE_UNVERIFIED`. An empty list is valid and holds every item,
  so a report with nothing verified is closed on record. Unknown or duplicate
  ids are 422. Default: v1 is refused once v2 ships (no production v1 exists);
  `publisher.cli attest` moves to v2.
- Renderer: the note's acquisition time and source URL come from the attested
  `fetched_at`/`final_url`; `collected_at` is labelled as report writing time.
  Template revision and `template_version` change.
- Read surface for the attester (scope `read`, producer-scoped):
  `GET /v1/attestation-queue` lists report ids received and not yet attested;
  `GET /v1/ingestions/{id}/request` returns the stored request bytes so the
  attester recomputes `content_sha256` itself instead of trusting a fingerprint.
- New test vectors in `attestation-v2.vectors.json`; hy-home pins the merged
  `dev` commit and rebuilds the image.

##### Hermes lane (small plugin/prompt PR, not a rewrite)

- `submit_research_report` schema accepts and forwards `source_quotes`.
- The three research Cron prompts ask for verbatim quotes per item.

##### Verifier + attester on server A (this repo)

- One dedicated system account (e.g. `hermes-attester`), no login shell, not
  sharing a group with Hermes, n8n or the Publisher account.
- systemd timer every few minutes; reads the attestation queue and stored
  requests from the Gateway with one credential holding `attest` + `read`,
  registered under producer `hermes`. It reaches them through a new A-host-only
  Traefik route (approved ops unit). It never reads Hermes files or the
  Publisher Outbox.
- Transient fetch failures (timeout, 5xx, connection) are retried for a window
  (default 6 hours from first attempt, builder may tune); then the attester signs
  whatever is verified, possibly an empty list. Local state records attempts so a
  report is never re-fetched after it is signed.
- Per item:
  1. Fetch `source_url`: https only; refuse private, loopback, link-local and
     the hy.home.arpa zone after DNS resolution (re-check each redirect);
     ≤ 5 redirects, size cap, timeout; record final URL, status, response
     SHA-256 and fetch time (UTC, verifier clock).
  2. Extract text (HTML → text, stdlib or an already-locked dependency);
     normalise whitespace, quotes and Unicode (NFKC).
  3. Every quote must appear in the normalised text.
  4. Every number, date and Latin-script proper noun in the item's title/body
     must appear in the quotes or the page text. Numbers, dates and units are
     normalised to values before comparison (owner decision): Korean and English
     forms such as `10월 31일`/`Oct 31`, `30억`/`3 billion`, `30%`/`30 percent`
     match; an expression the rules cannot parse holds the item.
  5. Required Resource profile fields present.
- Evidence file per report (JSON, canonical) stored only on server A in the
  attester's directory: per-item fetch records, check results, verifier version.
  Default: hashes only, no page body retained.
- Sign `attestation/2` with an Ed25519 key readable only by that account
  (reuse `publisher/attestation.py` key-custody rules: `load_signing_key`).
- Unapproved jobs: the attester's own job allowlist and Blog-data
  `research-map` both limit `ready` to news `6eabd835f969`, devops `25674fbc0bf3`,
  business idea `8d0925bc571d`.
- Idempotent: an already-attested report is skipped; Gateway replay answers 200.

##### Operations

- Gateway config gains the `export` block with the attester public key only
  when the above is deployed and verified; that is the moment Export opens.
- Key rotation/revocation follows RUN-0053 (remove key, restart Gateway).
- Monitoring reuses existing signals: attester journal outcome counts
  (`attested`, `held_items`, `rejected`, `retry`) and the Gateway export list.

#### Left to the builder

- Exact quote/size/time bounds, HTML-to-text method, proper-noun extraction
  rule, timer interval, file layout under the attester account.
- Whether verifier and attester are one module or two inside the workload.
- Test design: synthetic pages served locally in tests (no real fetches in CI).

#### Order

1. Blog-data `dev` PR (`source_quotes`, `attestation/2`, `SOURCE_UNVERIFIED`,
   renderer fields, read endpoints).
2. Hermes plugin/prompt PR (quotes); source and rehearsal may run in parallel.
3. hy-home PR: new Blog-data pin, n8n screen allowlist, A-host read route,
   verifier + attester, synthetic E2E.
4. Ops units, each approved: Gateway re-pin, workflow republish, read route,
   account, key, token, Gateway `export` block, timer; only then the Hermes
   plugin/prompt rollout.

### Item-level attester implementation — 2026-11-01

Built on branch `feat/hermes-trust-adapter`, source and synthetic evidence only:

- Blog-data pin `b372de374ec589b1bec2ff8096ae2f7272461248` (attestation/2, schema 4,
  `resource-export/3+4b681da87f80`); the v1 attester and `cli attest` were removed.
- `publisher/source_fetch.py` (SSRF-guarded fetch), `publisher/source_check.py` (page text
  and per-item checks: required fields, 1-3 `source_quotes`, numbers, names) and
  `publisher/attester.py` (`GatewayReader`, `run`; 6 h transient retry, signed body stored
  before sending, evidence and state files, quarantined reports skipped), plus
  `publisher.cli attest-queue` and `deploy/hermes-attester.{service,timer}`.
- The n8n screen accepts `source_quotes`; Traefik gains the `blog-attestation-read`
  router (queue and per-report request GETs from the attester host only).
- Disposable E2E `tests/e2e-ingress.sh`: RESULT 53 PASS, 0 FAIL. It ingests a report with
  `source_quotes` through Traefik, n8n and the Gateway, then runs the real `attester.run`
  with the real `GatewayReader` over the throwaway Traefik and a fake fetcher (no network).
  Item A became `ready`, item B `held` with `SOURCE_UNVERIFIED`; a second run sent nothing and
  the stored body resent as a 200 duplicate. `tests/e2e-upgrade.sh` passes 11/11.
  A quarantined report cannot be produced through public interfaces, so that case is
  covered by unit tests only. TLS verification is skipped only in the test harness.
- Production units (image build, backup then schema 4 switch, workflow republish, route
  pull, attester account/key/token/`export` block, timer, Hermes plugin rollout) are
  NOT_RUN; RUN-0053 lists them as separate approval units.
- Residual gap: the production POST closure (`cli attest-queue` sending through
  `HttpTransport`) is exercised by neither the unit tests nor the E2E, whose harness uses
  its own send function. It is first exercised by the real timer run.
- Final-review fixes: the attestation route has its own 262144-byte body cap (ACK stays
  16384) and the attester treats HTTP 413 like 401/403; unencodable URLs are permanently
  unverified; IPv4-compatible and NAT64 addresses are refused; the service unit uses
  `StateDirectory` and an empty capability set; the timer no longer sets `Persistent`.

### First real Cron submission — 2026-11-01 08:00 KST

Cron `25674fbc0bf3`, `6eabd835f969` and `8d0925bc571d` ran at 08:04–08:07 and
delivered email and Telegram, but no report reached the Gateway. Five
`submit_research_report` calls each failed in about 0.01 s with
`Tool handler returned unsupported result type: dict`: the Hermes tool registry
accepts only a `str` result (or its multimodal envelope), and the plugin handler
returned a dict on every path. Nothing reached the plugin Outbox, Traefik or n8n.
`hermes plugins doctor` checks discovery, import and registration only, so it
passed. Fix: the registered handler returns `json.dumps(...)` of the unchanged
result, plugin 0.2.1, with handler-result contract tests. The installed plugin is
updated only after merge, and the hash comparison is repeated then.

### Attester release role — 2026-11-01

Preparing deploy unit 7 found two defects. `install.py` shipped only Publisher
modules, so no release could run `attest-queue`; and `cli.py` imported
`attestation` and `attester` at top level, so a Publisher release built from
`main` could not import its CLI (reproduced by `tests/install-check.sh`:
`ImportError: cannot import name 'attestation'`). No release was installed in
production, so nothing live broke. Fix: `install.py --role attester` installs a
separate release under `/opt/hermes-attester` with `attestation`, `attester`,
`source_check` and `source_fetch`; the Publisher role is unchanged; `cli.py`
imports the attester modules only inside `attest-queue` and a Publisher release
answers `operation_rejected`; the unit runs `/opt/hermes-attester/current`.
Secret ownership is corrected to `hermes-attester` 0700/0600, as the auth-header
reader requires. Evidence: `tests/test_release_roles.py` 7/7 (RED then GREEN),
`tests/install-check.sh` 21/21 PASS including four attester-role checks.
Operations so far on server A: Gateway on `b372` schema 4, workflow
republished, attester account, key and `attest`+`read` credential created,
`export_enabled:true`; release install and timer NOT_RUN.

### Attester live on server A — 2026-11-01

After PR #708 merged (`c2825bbe8`), the owner ran the install in a terminal.
The release archive was `git archive c2825bbe8`, root-owned under `/root`;
`install.py` and both units were taken from that archive, not the checkout.
`install.py --role attester --python /usr/bin/python3.12` installed
`/opt/hermes-attester/releases/c2825bbe8a54c2844d79efeec5c09ee63b2a7658`
(hash-locked `cffi`, `cryptography`, `pycparser`; pip removed), and
`/opt/hermes-attester/current` points at it. A manual
`systemctl start hermes-attester.service` returned
`{"attested": 0, "held_items": 0, "rejected": 0, "retry": 0, "skipped": 0}`
with `Result=success`. The Gateway answered, the credential and key loaded, and
the queue was empty. `hermes-attester.timer` was enabled only after that run
passed and fires every five minutes. A real item verification, Export `ready`,
and the Windows pull and ACK remain NOT_RUN until a Cron report arrives.
Rollback: disable the timer, remove the two units and the `current` link,
`daemon-reload`. Releases are left in place.

### First manual Cron submission — 2026-11-01

The owner ran `hermes cron run 25674fbc0bf3` (devops-daily-brief) at 10:16 KST.
Email went out; the Gateway answered 403 `FORBIDDEN`. Traefik passed the source
allowlist, n8n header auth passed, and n8n execution 92 forwarded the Gateway's
403 unchanged. Cause: `scripts/lib/ingestion/http.mjs:184` rejects a request
whose `producer` differs from the token's producer (`hermes`); the model wrote
`producer: "hermes-cron-devops-brief"` because the tool schema gives it no
value. Fix: plugin 0.2.2 sets `producer` to `hermes` before validation, so the
model cannot choose the authenticated identity
(`ProducerPinTests`, RED then GREEN; workload suite 296 OK). Install with
`plugin-update.sh` and re-run one job to verify. Separate finding, not fixed:
the worker's JavaScript task runner kept failing to register ("No matching task
offer", expired grant token, broker 403). Execution 90 timed out and 91 took
30 s, so the plugin's first two 15 s attempts ended as Traefik 499 before the
third reached the Gateway.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bounded design and ownership | 23 | W79 | Existing exporter and isolated worker boundaries | Current direct request and reviewed inventory handoff | PASS | Source admission; File ownership and dependencies | required | - |
| Source/runtime duplicate inventory | 23 | W79 | Latest main/HEAD/worktrees, host Cron and n8n workflow identities | Redacted observed metadata; remote hy-home.n8n operation unknown | PASS | Observed inventory — 2026-10-30 | required | - |
| Publisher staging and Outbox | 23 | W80 | Single/multiple idea, replay, conflict, restart, paths/hashes and permissions | Synthetic fixtures and reviewed validator | PASS | W80 synthetic evidence | required | - |
| Delivery and reconciliation | 23 | W81 | Durable receipts, lost response, bounded retry and immutable request binding | Fake adapters | PASS | W80 synthetic evidence | required | - |
| Exact Gateway compatibility | 23 | W82 | Approved API revision/fixtures and inactive n8n source | Pinned source tested; actual timestamp provenance absent | NOT_RUN | Gateway source admission after Blog-data PR #620 | required | - |
| Inactive n8n workflow import | 23 | W83 | Isolated owner/project setup, default publication API, static-webhook registration, exact-path helper and main/worker/runner health | Synthetic environment passed; registered webhook accepted its request | PASS | Isolated Queue publication and dispatch follow-up — 2026-10-30 | required | - |
| Isolated Queue worker to fake Gateway | 23 | W83 | Queue round trip through external JavaScript runner and synthetic persisted receipt | Fake Gateway returned 201 with recorded synthetic receipt | PASS | Isolated Queue publication and dispatch follow-up — 2026-10-30 | required | - |
| Native worker to Gateway | 23 | W83 | Tracked workflow plus server-B DNS/TCP/TLS/auth/timeout, outage/recovery and durable persistence | No tracked-workflow or server-B execution; isolated fake-Gateway receipt is non-operational | NOT_RUN | Isolated Queue publication and dispatch follow-up — 2026-10-30 | required | - |
| Existing email/workload regression | 23 | W83 | Preserve Cron/email and existing n8n/Docker workloads | Read-only baseline plus later approved Native scenario | NOT_RUN | Design admission — 2026-10-30 | required | - |
| Validator pin realignment | 23 | W83 | Draft/main diff, local corpus verdicts, pinned-byte, draft/changed/symlink rejection tests | Main `957d047c…`, local scratch exports | PASS | Post-PR #693 dispatch readiness — 2026-10-31 | required | - |
| Gateway 1.1.0 compatibility | 23 | W82 | Ingestion POST request/receipt/error definitions vs pinned 1.0.0 | Blog-data dev `1a4cd60` | PASS | Post-PR #693 dispatch readiness — 2026-10-31 | required | - |
| Companion evidence and dispatch | 23 | W83 | Evidence binding rejections, gate closure, loopback 201/200/401/409/503/drop, replay, credential privacy | Synthetic fixtures and loopback Gateway | PASS | Post-PR #693 dispatch readiness — 2026-10-31 | required | - |
| Producer authentication verifier | 23 | W83 | Ed25519 signature, key store lifecycle and shared gate decision with negative tests | Synthetic keys; tracked store empty | PASS | Producer authentication and gate unification — 2026-10-31 | required | - |
| Producer contract cross-check | 23 | W83 | Same snapshot through main `957d047c` and Hermes `f454020c` validators | Live export copy, manifest `8d412898b839bdc4` | PASS | Producer authentication and gate unification — 2026-10-31 | required | - |
| Protected install | 23 | W83 | Hash-locked dependency, root-owned immutable release, verify-install as separate accounts, weakened-path negatives | Disposable container, commit of this slice | PASS | Protected install and ingest-only contract — 2026-10-31 | required | - |
| Protected install on server A | 23 | W83 | Real `hermes-publisher` account loads `/opt/hermes-publisher` release with `python3 -I` | Blocked: account, path and service need separate approval | NOT_RUN | Protected install and ingest-only contract — 2026-10-31 | required | - |
| Producer trust anchor | 23 | W83 | Real restricted producer account and reviewed key in `publisher/producer-keys.json` | Blocked: no producer account, key or signed run delivered | NOT_RUN | Handoff: Hermes producer lane (server A) | required | - |
| Server-B TLS entry | 23 | W83 | DNS/TCP/TLS/auth from n8n worker | Superseded: the Gateway runs on server A | NOT_APPLICABLE | Hermes host direct path with the Gateway on server A — 2026-10-31 | required | - |
| Direct path source | 23 | W83 | Workflow path/URL, Gateway service isolation, exact-path route | Workload suite, wiring and Compose baseline tests | PASS | Hermes host direct path with the Gateway on server A — 2026-10-31 | required | - |
| Direct path disposable E2E | 23 | W83 | Host → Traefik → native n8n → built Gateway → SQLite, failure and boundary cases | Synthetic tokens, disposable containers | PASS | Hermes host direct path with the Gateway on server A — 2026-10-31 | required | - |
| Direct path operational | 23 | W83 | Live Gateway, credentials, publication, Traefik route, Hermes plugin | Gateway, Worker network, credentials, publication and route applied 2026-11-01; Hermes URL and a real Cron submission pending | NOT_RUN | Hermes host direct path with the Gateway on server A — 2026-10-31 | required | - |
| Windows Export and ACK | 23 | W83 | B pull, Vault write, verified ACK | Blocked: receiver on server B not run; route live since 2026-11-01, Export closed until the trust adapter exists | NOT_RUN | Attestation, Resource Export and Windows pull — 2026-11-01 | required | - |
| Gateway `dev` pin and image | 23 | W83 | Exact `dev` commit, Dockerfile allowlist build, templates present, export API live | Blog-data `a43d824`, production image ID `sha256:e513b938…`, `resource-export/2+f45cc9bbc0a4` | PASS | Server A operational rollout — 2026-11-01 | required | - |
| Attester source | 23 | W83 | attestation/2 vectors, SSRF-guarded fetch, item checks, queue attester retry/resend/quarantine, deploy units | Synthetic keys, fixtures and fake fetcher; `publisher.cli attest-queue` replaces `attest` | PASS | Attestation, Resource Export and Windows pull — 2026-11-01 | required | - |
| Attestation/Export/ACK disposable E2E | 23 | W83 | Item-level attest → ready/held → pull → hash check → ACK, forged, scope, read-route and restart cases | Synthetic tokens and keys, fake fetcher, disposable containers at `b372de374e`; 53 PASS, 0 FAIL | PASS | Item-level attester implementation — 2026-11-01 | required | - |
| Schema-4 upgrade and restore | 23 | W83 | Previous-pin store backed up, upgraded in place to schema 4, both backups restored | Disposable volumes, `e2e-upgrade.sh` 11/11 | PASS | Attestation, Resource Export and Windows pull — 2026-11-01 | required | - |
| Production attester | 23 | W83 | Real `hermes-attester` account, key, `attest`+`read` token, `export` block, timer and a real item verification | Account, key, token, `export` block, release `c2825bbe8` and timer live; manual run succeeded on an empty queue; no real item verified yet | NOT_RUN | Item-level attester implementation — 2026-11-01 | required | - |
| Hermes plugin source handoff | 23 | W83 | Plugin source merged and matched to the installed copy | PR #700 `3727ff0e7`; four files SHA-256 equal to the installed copy; real submission not run | PASS | Attestation, Resource Export and Windows pull — 2026-11-01 | required | - |
| Source/static/review | 8, 23 | W83 | Focused tests, docs gates and independent review | Protected-install follow-up slice: 169 tests, Ruff, links/metadata/lifecycle/markdownlint, install check 17/17, independent review with Important findings fixed | PASS | Review and Completion | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 23 | pending | Bounded design and ownership | Basic source and safe synthetic checks may proceed; exact API and actual worker/Gateway evidence remain required. | SPEC-0204 TSK-0022 |

## Review and Completion

2026-10-31 dispatch-readiness slice: a follow-up independent code review of the
fix range confirmed all five prior findings fixed with no Critical or Important
remainder. Its Minor port/length URL check and isolated symlink credential test
were applied; untested hard-link, foreign-owner and FIFO credential cases, the
count-based retry exhaustion and the Python 3.11+ timestamp parsing assumption
(local 3.12.3) remain noted. Reviewers had no shell; the suite (151/151),
Ruff and document checks were run by the controller. With owner approval the
slice was pushed as PR #694; head `c346db86e` passed CI Quality Gates and the
owner merged it at 2026-10-31T01:15:45Z as `7b041d0b1`, whose main CI Quality
Gates also passed. This integrates source only; criterion 23 stays pending.

Earlier slices (before PR #694) recorded no commit, push, merge or deployment
from this Task; PR #694 above is the first integrated Task slice. The later
evidence-alignment slice was committed locally at the time of that entry and
then, with owner approval, merged as PR #695 (`31b92f95e`, 2026-10-31T02:15:09Z).
No deployment is claimed. Producer authentication, server-B TLS,
Native delivery evidence and operating acceptance remain separate pending work. Local source readiness
does not imply operating readiness; resume the external-contract and operational
lanes from these recorded boundaries.

2026-10-31 protected-install slice: an independent whole-branch review of
`7629bbad4..` found no Critical issue; all five Important findings were fixed
with failing tests first and re-verified (169 tests, install check 17/17 on the
final head). Deferred minors: skipped non-existent `sys.path` entries, about
14 ms per runtime check (50-60 ms per record), no archive member size cap,
undocumented fail-closed symlinked `/opt`, and a Traefik timeout check limited
to two files. PR #696 had already merged at `7629bbad4`, so this slice is a follow-up PR;
its CI and merge are recorded on that PR.
CI does not run this workload's suite, so these results are local evidence.

2026-10-31 direct-path slice: an independent review found no Critical issue.
Important findings were fixed: the host-source proof used loopback (now LAN
address, measured live as `192.168.0.13`; the first LAN-address run failed 403
as predicted), the retry contract omitted 429/500/502/504 and the 404 seen while
the workflow is unpublished, the shared webhook/Gateway token erases the
Publisher signature guarantee downstream (documented; splitting needs a
producer decision), two tests could pass vacuously, and a wrong Grafana row.
Deferred minors: buffering before rate limiting, `edge_net` peers reaching n8n
directly, any published workflow reaching the Gateway, missing wrong-token and
path-variant cases (and live Traefik `v3.7.14` vs tested `v3.7.16`), the Compose
service shape never started, and unbumped README versions. During the fix a
probe file was briefly written to the live Traefik directory with an ignored
extension and removed in the same command; the directory and logs were
confirmed unchanged.

Design self-review checked scope, dependencies, immutable Outbox interfaces,
coverage of failure cases, and protected runtime exclusions against the direct
request. Basic source implementation is currently authorized and active.
Design and implementation sequencing are concrete; source work may proceed in
the assigned isolated worktree. This Task starts as draft under the registered
profile; no fabricated completed transition is recorded. The controller records
actual implementation/test/review receipts and any registered lifecycle changes.
Close only with required criterion evidence or an explicit owner disposition.
Report SOURCE and SYNTHETIC independently from API_COMPATIBILITY, N8N_NATIVE,
SERVER_B_NATIVE and DELIVERY. No workflow activation, secret use, Compose
recreation or external port is claimed.

2026-11-01 attestation and Resource Export slice: an independent review (no
shell) found no Critical issue and two Important ones, both fixed test-first.
I-1, a group-readable signing key was accepted for any group and its parent was
unchecked: `load_signing_key` now pins ancestors without symlinks, refuses a
parent writable by others, and allows group read only for the attester's own
group (`test_group_read_only_for_the_attester_group`,
`test_writable_or_linked_parent_directory_is_refused` RED→GREEN). I-2, the E2E
signed only the direct-path shape: it now sends a `verified_request` body
through n8n and attests it (51/51). Minors applied: rate limit before
buffering on the ACK and attestation routes (route test RED→GREEN), read route
120/min, TLS failures stop as `rejected`, stale `read`-scope and key-mode text,
the Traefik-recreation note, the host-wide attestation allowlist caveat and
producer-key expiry. Deferred minors: `--gateway` is an argument rather than a
pinned constant; the Blog-data signature binds content, not report ID, so equal
content under another key could be attested again (duplicate exports only); the
E2E publishes its throwaway Traefik on the LAN address while it runs and keeps
its built images; the Windows receiver's 429 handling is untested.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Workflow requirement](../../../01.requirements/0008-workflow.md)
- [Workflow architecture](../../../02.architecture/descriptions/0007-workflow-architecture.md)
- [n8n guide](../../../05.operations/guides/08-workflows-and-automation/0053-n8n.md)
- [n8n policy](../../../05.operations/policies/08-workflows-and-automation/0053-n8n.md)
- [n8n runbook](../../../05.operations/runbooks/08-workflows-and-automation/0053-n8n.md)
