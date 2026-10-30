---
title: "Hermes Blog Ingestion Transport Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-30"
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

The replacement checkout's full suite subsequently passed 107 tests with the
pinned validator and synthetic localhost tests. Independent final adapter,
replay and workflow correctness and security reviews found no remaining Critical
or Important findings. The workflow URL preprocessing accepts a subset of the
Gateway's valid inputs; it is not equivalent to the Gateway's full URL parser.
The replacement branch integrates `6a` without rewriting the existing history;
its draft PR is not yet published. PR #684's malformed merge CI remains FAIL,
and hosted acceptance, n8n Native and criterion completion are not established.

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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bounded design and ownership | 23 | W79 | Existing exporter and isolated worker boundaries | Current direct request and reviewed inventory handoff | PASS | Source admission; File ownership and dependencies | required | - |
| Source/runtime duplicate inventory | 23 | W79 | Latest main/HEAD/worktrees, host Cron and n8n workflow identities | Redacted observed metadata; remote hy-home.n8n operation unknown | PASS | Observed inventory — 2026-10-30 | required | - |
| Publisher staging and Outbox | 23 | W80 | Single/multiple idea, replay, conflict, restart, paths/hashes and permissions | Synthetic fixtures and reviewed validator | PASS | W80 synthetic evidence | required | - |
| Delivery and reconciliation | 23 | W81 | Durable receipts, lost response, bounded retry and immutable request binding | Fake adapters | PASS | W80 synthetic evidence | required | - |
| Exact Gateway compatibility | 23 | W82 | Approved API revision/fixtures and inactive n8n source | Pinned source tested; actual timestamp provenance absent | NOT_RUN | Gateway source admission after Blog-data PR #620 | required | - |
| Native worker to Gateway | 23 | W83 | DNS/TCP/TLS/auth/timeout, outage/recovery and durable persistence | Exact approved server-B and secret targets absent; BLOCKED | NOT_RUN | Gateway contract and native gates | required | - |
| Existing email/workload regression | 23 | W83 | Preserve Cron/email and existing n8n/Docker workloads | Read-only baseline plus later approved Native scenario | NOT_RUN | Design admission — 2026-10-30 | required | - |
| Source/static/review | 8, 23 | W83 | Focused tests, coverage, docs gates and independent review | Final Task-owned diff | NOT_RUN | Review and Completion | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 23 | pending | Bounded design and ownership | Basic source and safe synthetic checks may proceed; exact API and actual worker/Gateway evidence remain required. | SPEC-0204 TSK-0022 |

## Review and Completion

Local source verification and the user-authorized Git integration are in progress.
No commit, push, merge or deployment is claimed here. The Gateway contract
and timestamp mapping, API compatibility, Native delivery evidence, and the
required local CI toolchain remain separate pending work. Local source readiness
does not imply operating readiness; resume the external-contract and operational
lanes from these recorded boundaries.

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

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Workflow requirement](../../../01.requirements/0008-workflow.md)
- [Workflow architecture](../../../02.architecture/descriptions/0007-workflow-architecture.md)
- [n8n guide](../../../05.operations/guides/08-workflows-and-automation/0053-n8n.md)
- [n8n policy](../../../05.operations/policies/08-workflows-and-automation/0053-n8n.md)
- [n8n runbook](../../../05.operations/runbooks/08-workflows-and-automation/0053-n8n.md)
