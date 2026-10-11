---
title: "P05 n8n Independent Outbox Notifier Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0013"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P05 n8n Independent Outbox Notifier Task

## Objective

Own criterion19/W40-W45: one independent DEV manifest-publication notifier
using P04's outbox and the existing n8n queue worker with restricted Mailpit
capture. Preserve at-least-once and uncertain delivery semantics. Issuance
defines source ownership and prerequisite boundaries; it imports no workflow,
creates no resources and changes no credentials or runtime.

## Inputs and Authorization

The user's full P05 execution prompt and current coordination request authorize
assessment, formal Task issuance and independent worker instructions. Prompt
SHA256 is `669a86c89a761a9a33172ebf9223eb9953d9bea062d76a2e025c4045912c7823`;
historical baseline is `860ac1c3633eac9ad416fb1abd8a61a6e617ebd8`.
Actual clean local main/HEAD is
`4e26a5a8022a7307c7461af60337442912955df1`; fresh fetch/ls-remote confirms
initial remote main `6da5e3bf380d5002e0e28181136fde8c016e49ce`. A later
ls-remote/fetch confirms remote main at the same4e26a5a80, including P03/P04
issuance; that publication was external to this assessment. Open PR list is
empty. CI Quality Gates run38105014827 completed successfully at4e26a5a80;
Push on main run38105014631 was still in progress at observation. These are
remote observations, not P05 native, SEC security or HOME acceptance.

Read bootstrap/provider, SPEC-0204/0212, TSK-0012 and the selected service
owners. Preserve completed registration, DEV/MNG, Influx retirement,
RedisInsight/exporter, k6/OTLP, common controls, Stage05 and P00. Preserve
OpenBao PR409/410 TLS/wrapping/readiness/audit/snapshot source. Do not reopen
historical Tasks0001-0004 or replace SMTP/history Task0005. New Task0013 owns
only this P05 increment; no new Spec number is issued.

The latest full P05 prompt requests logical commits and an owning-Spec PR after
implementation, latest-head required CI and independent review. Older SEC01/
SMTP01/CLN01 keep local-main/no-PR delivery. Dev is unused. Reconcile the
unpublished documentation prefix and P04 dependency before a P05-only PR;
do not implicitly push main. Already-authorized source and review need no
repeated approval. Before private/runtime actions, establish exact target,
effects, consumer, validation and recovery here; missing inputs defer only
their dependent lane. Unsupported overall budgets remain unknown.

### Worker and Exact Ownership

One P05 writer uses `codex/p05-n8n-outbox-notifier` in
`/home/hyunyoun/data/hy-home.docker/.worktrees/p05-n8n-outbox-notifier`, from
the issuance commit after reviewed local-main integration. Record actual
branch/HEAD/clean status and input hashes before changes. This issuance creates
no implementation chat. Other writers are active: never reset, stash, clean,
stage or force-push their changes.

After checking for existing consumers/implementations, own these new paths:

- This Task, its execution evidence and logical commit ledger.
- `infra/07-workflow/n8n/workloads/README.md` and one canonical subtree
  `infra/07-workflow/n8n/workloads/manifest-outbox-notifier/`.
- Within that subtree, Korean `README.md`; `tools/__init__.py` and
  `tools/build_workflow.py`; inactive public
  `workflows/manifest-outbox-mailpit.json`; synthetic `fixtures/`; and a
  value-free `outbox-contract.json` binding the reviewed P04 schema/version/hash.
  The contract is a consumer binding, not a second SQL authority.
- If necessary for the verified SMTP gap, a narrowly scoped n8n custom node
  under `nodes/OpsflowSmtp/`, with `OpsflowSmtp.node.ts`, `transport.ts`,
  reviewed package/lock/build metadata and focused synthetic transport tests.
  It uses n8n's native SMTP credential API and only this notifier operation;
  no standalone mail service, arbitrary Code credential access or broad module
  allowlist is introduced. Runtime registration/mount/build is a shared proposal.
- `tests/lib/ops/test_n8n_outbox_workflow.py`,
  `tests/validation/test_n8n_outbox_contract.py` and opt-in
  `tests/validation/test_n8n_outbox_rehearsal.py`.

Every new folder, including workloads/tools/workflows/fixtures/nodes and node
children, receives Korean README navigation. Use one deterministic builder
and generated JSON; no production reference/ duplicate. Building is a pure
function with explicit CLI output; importing the builder never writes files.
Existing parent README edits are proposals, not a second writer lease.

P04 exclusively owns canonical SQL/migrations and publication contracts in
`infra/07-workflow/airflow/workloads/manifest-pipeline/sql`. Do not copy the
supplied DAG/SQL or create another opsflow schema/provisioner. With an active
P04 writer, the standalone prompt fallback routes installation through that
owner. If reassignment becomes necessary, the coordinator records the exact
canonical-file handover first; no parallel installation or implicit takeover.
P05 proposes SQL changes and consumes the reviewed version/hash read-only.

SEC01 owns n8n main/worker/runners versions, existing Dockerfiles and immutable
image/security decisions. P03 owns endpoint/network contracts; P02 catalog/
schema/tools; P01 OpenBao helpers and subject0085; SMTP01 canonical COMM-002/
COMM-003 and its retirement executor; CLN01 consumer/deletion assessment.
Root/leaf Compose/environment, existing n8n custom-bind integration, gateway,
Alloy, backup, catalogs/support, m0021/inventory, Registry, Spec/Plan, existing
README/subject0053 documents, manifest/workflow and shared tests remain read-only
to P05 until a specific exclusive lease. Submit base blob IDs, exact hunks,
consumer/test map and rollback in ignored integration proposals; the named
owner/coordinator integrates once after reviewing both sides.

### Start Now and Wait Boundaries

W40/W41 may start now: public reuse audit, deterministic inactive JSON,
provisional state fixtures, RED/GREEN graph/validation/privacy/transport tests,
bounded custom-node source and common-file proposals. P04 SQL is not frozen
yet. Label draft interface assumptions and bind them later in W42; do not
call mocked claim/ack a real database test. Full SEC/P03/P01/P06 completion is
not a global source prerequisite.

W42 final binding waits for P04 W36's independent SQL/security review and exact
migration/interface hash. Record claim result fields/types, ack/retry boolean
semantics, views, role grants, clock/lease, retry/dead and requeue rules.
Reference defaults are a draft ten-minute lease, five attempts and bounded
backoff; any change is a versioned P04 migration and reviewed P05 consumer
update. Historical/backfill publication must not create a fresh notification.
W43 native execution follows P04 W38's genuine publication/outbox fixture.

Before native import/execution, SEC01 supplies exact compatible main/worker/
runner image digest/ID, installed node schemas and relevant security receipt.
Source currently selects2.42.6 while HOME still runs2.41.6. Verify Postgres2.6,
EmailSend2.1 or reviewed replacement, IF2.2, Code2 if retained, StopAndError1
and schedule trigger on that selected image; node fields are not arbitrary.
Existing version/provider work is reused rather than repeated.

P03 supplies exact DEV DB and Mailpit endpoints/ports, TLS/CA/timeout contracts
and the process actually executing DB/mail nodes. Current source declares
queue mode and OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true, but manual/scheduled
worker execution still needs native proof. Add DEV/capture access only to that
verified executor; runners need no DB/mail networks for a boolean-only Code
check. Preserve existing MNG metadata, broker pair, networks and mounts.

Current mail_net is an ordinary bridge shared with Stalwart; Mailpit is also
on edge_net. Mailpit-only access cannot be inferred from the network name or
loopback publication. Propose a dedicated bounded capture path/network if
needed, with P03/coordinator review, keeping existing other consumers intact.
The notifier SMTP implementation must restrict the actual Mailpit host/port,
synthetic sender/recipient allowlist, run-derived Message-ID and small text
payload; reject arbitrary SMTP hosts, relay, CC/BCC, attachments, file/URL
reads and header injection. Prove denied Stalwart/external destinations and
zero unintended effects. Existing accepts-any/insecure capture settings are
DEV behavior, not production SMTP authentication evidence. Do not mount/copy
real canonical COMM-002 into Mailpit credentials or create another Supabase
SMTP password. P05 adds no external SMTP, Slack or webhook integration.

P02 reviews value-free notifier credential references/classification. Credentials
use the existing official n8n UI/API path and its encryption-key-protected
native store, with operator-resolved local IDs in an ignored/private import
artifact. Never invent IDs, export decrypted values, UPDATE credential data in
SQL or assume .env changes refresh stored credentials. Notifier has only
claim/ack/retry function EXECUTE; no owner/superuser/direct table writes or
other database access. No provision/admin/ingest credential enters workflow.
Encrypted native credentials remain inside the shared main/worker application
trust boundary; they are not worker-only Docker secret mounts. Verify actual
project/workflow access without claiming that network placement limits which
n8n administrators can decrypt or use stored credentials.
OpenBao remains the eventual management source; protected native execution
copies may support bounded DEV proof before P01/P06 final delivery. Current
edition and native external-store support must be verified, not assumed.

### Required Workflow and Failure Semantics

Import inactive with credential placeholders resolved only in the private
artifact. First prove authenticated manual execution, then exactly one
one-minute polling schedule; no parallel Airflow email or Wiki schedule.
Empty claim returns no mail/ack/retry action. Validate a single closed claim
row's id/run/source/count/token types; runtime lease tokens remain private
capabilities and never enter tracked evidence. Parameterized SQL uses the
same current id/token for ack/retry, never string interpolation.

The provided generator has no stable Message-ID. Official selected n8n tag
resolves to commit `34ab9c7bf3d0c6d2ec3422e12e0b970aea5717c7`;
EmailSend v2 source lacks a Message-ID/custom-header option and explicit
connection/greeting/socket timeout settings. Source hashes are send.operation.ts
`f45a85c4d3839033bdcb434be00fe242fc15ec6de1b7e6bae7fc64843b8f59bb` and utils.ts
`cfbb16fbd8c5320eabb910535ebe939eeb8d780ec750e0834f88b49b5dc2e68a`.
These are upstream source observations, not installed-image proof. A narrow
credential-aware node may close the gap with explicit bounded transport and
redacted output. Unsupported JSON options or broad Code/nodemailer/secret
access are not a solution. Existing custom bind can shadow image-installed
nodes, so actual registration and identical main/worker artifacts must be proven.

Freeze workflow execution budget (reference120seconds), DB and SMTP transport
timeouts below the current lease with failure/cancellation tests. A workflow
timeout alone does not establish socket cancellation. Close transports and
return only bounded run/state/error outcomes; no raw SMTP response, recipient
data, credential, payload or driver error enters execution exports/logs.
Keep successful/error/manual data-saving disabled, clear pinData, and test
synthetic leakage markers through both positive and failure paths.

Ack only the expected recipient's positive SMTP acceptance for the claimed
event; reject empty/unknown/rejected outcomes. Validate ack===true. Also verify
retry===true before reporting retry/dead transition; false is stale/lost lease,
not a successful requeue. DB error waits for fresh claim/lease reconciliation.
SMTP acceptance and PG ack are not atomic: response loss or ack loss can cause
duplicate mail. Stable Message-ID supports diagnosis/dedup but does not prove
exactly-once or recipient delivery. Never restart an old execution at SMTP
with its expired claim; retry the whole fresh-claim workflow.

P04 owns any controlled dead requeue function/migration. P05 owns its operator
procedure and tests: identify cause, preserve accepted/uncertain receipts,
apply only the reviewed function under its named operator role, then fresh
claim. No direct outbox UPDATE, table-wide reset or notifier privilege expansion.

### Native, Recovery and Delivery Boundaries

Before each native/private action record exact Docker context/project, image,
workflow/credential reference, DB/role, capture target, resource/time budget,
operational writer, effects, independent review, backup, owned empty restore
target, identity-bound cleanup and rollback here. Synthetic isolated resources
precede the selected operational DEV batch; no production fault injection or
shared-volume initialization. Missing target defers only that operation.

Prove native inactive import, schema/credential binding, manual and scheduled
worker placement, actual P04 outbox consumption and Mailpit capture, two
notifiers/one event, lease expiry/old ack denial, empty queue, DB and SMTP
outage, send-response loss/ack loss, attempts cap/dead/fresh requeue, restart
and exact notifier credential rotation through the official n8n path. Coordinate
rotation with P04's role owner; do not broadly rotate passwords/encryption keys.
Test stale native execution copies separately from file/management source.

Recovery pairs a consistent n8n MNG metadata backup with the exact encryption
key, custom artifacts/data and needed queue state, restored only to reviewed
empty isolated targets with egress/schedules disabled. Coordinate DEV pointer/
outbox reconciliation with P04's own recovery proof. Prove credentials decrypt,
nodes register, and fresh claims preserve accepted/uncertain states without
silently re-notifying accepted events. A file copy, image revert or Mailpit
capture alone proves neither service recovery nor external delivery.

Rollback stops this polling schedule and makes only this workflow inactive,
drains/reconciles selected execution, and preserves outbox/receipts. Use compatible
metadata/key restoration when required; no full-stack up/down, prune, MNG
reset, broad chown, encryption-key replacement or private material deletion.

## Work Log

### Assessment and Next Work Units

At initial assessment4e26a5a80, coordinator/main/P04 worktrees were clean.
Later P04 began its workload and three dedicated source/test paths. No frozen
SQL commit or native acceptance was handed off; untracked code is not that
proof. P01/P02/P03 and old SEC/SMTP worktrees were separately observed and
preserved. P02's later local HEAD was ea927d004d4e59c5e44af566abc3f5c2b6372c05.
These local branch/uncommitted changes are not remote acceptance receipts.
SMTP PR413 is merged source; existing Tasks still leave actual cutover,
COMM-003 retirement and full recovery unaccepted. CLN retains PG-020 and
unknown consumers. SEC full image/security/HOME acceptance remains pending.

Safe inspect of six selected containers exited0: n8n main/worker run
hyhome/n8n2.41.6-local, both runners2.41.6, Mailpit1.31.2 and dev-pg18.6.
All reported running/healthy; worker networks are mng_data_net+n8n_net and
Mailpit edge_net+mail_net. Source selects n8n2.42.6 and Mailpit1.31.4.
This read-only metadata does not prove installed node schema, credential
consumption, manual offload, SMTP capture or an opsflow database/role resource.

1. W40: fresh source/owner audit and RED cases; read supplied six reference
   files but do not copy P04's DAG/SQL into P05.
2. W41: pure deterministic inactive builder/JSON and narrow SMTP node source,
   with closed graph/input, privacy, empty queue, Message-ID/timeouts and
   ack/retry/uncertainty tests; at least80percent meaningful coverage.
3. W42: freeze reviewed P04 schema/interface hash, function-only role and
   lease/requeue/recovery contract; revise draft consumer fixtures if needed.
4. W43: reviewed exact-image native inactive import and official private
   credential binding, then manual real-worker/DEV-to-Mailpit execution after
   P04 publication proof and shared proposal integration.
5. W44: one polling activation, concurrency/negative/failure/restart/rotation
   and separately empty paired metadata/key restoration, with operational
   writer/resources/cleanup/rollback evidence.
6. W45: subject0053 and service README proposals, registered affected gates,
   final independent code/security/SQL/IaC/docs reviews, CI and owning-Spec PR.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Git and owner baseline | 1, 19 | W40 | status/worktrees/fetch/open PR list | Local/remote4e26a5a80 | PASS | Baseline only; no remote or runtime write by this assessment | pending |
| Existing source contracts | 1, 8, 19 | W40 | Workflow version, SMTP and service wiring unittest | Clean4e26a5a80 | PASS | 45 tests, 3.023s, exit0; command below | pending |
| Supplied reference audit | 19 | W40 | Six public files, four static tests and JSON generator parity | Prompt669a86c89a76 | PASS | 4 tests, 0.02s, exit0; generator semantic parity; no native proof | pending |
| New notifier source | 19 | W41 | RED/GREEN builder/workflow/transport/privacy | Issuance commit pending | NOT_RUN | Independent worker implementation pending | pending |
| Frozen P04 binding | 19 | W42 | Reviewed SQL/version/hash and roles | P04 W36 pending | NOT_RUN | P04 remains sole SQL owner | pending |
| Native import and manual execution | 19 | W43 | Exact image, credential and worker/SMTP proof | P04 W38 and relevant readiness pending | NOT_RUN | No import/credential/network/DB action | pending |
| Scheduled failures and recovery | 19 | W44 | Polling, outages, restart/rotation and empty restoration | No exact action selected | NOT_RUN | No operational acceptance | pending |
| Delivery | 8, 19 | W45 | Latest-head CI/review/PR/merge | No P05 PR | NOT_RUN | Issuance only; future delivery | pending |

Actual existing-source command, exit0:

```sh
/tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests \
  tests.lib.ops.test_smtp_contract \
  tests.validation.test_service_wiring_contracts -q
```

All six supplied files were extracted only under ignored
`.agent-work/p05-reference-audit/reference/`. Existing isolated reference QA
Python ran `python -m pytest <reference>/tests -q` with that PYTHONPATH and
automatic plugins disabled. The explicit generator exited0 and its JSON
semantically matched the supplied inactive JSON. These tests inspect files;
they do not install Airflow/n8n, apply SQL, authenticate SMTP or test native
credentials. No shared QA environment was changed.

Worker verification selects new unit/contract modules plus affected existing
modules above, reproducible custom-node build/transport tests if used, and
opt-in native rehearsal with exact public/private inputs and cleanup. Record
commands, SHA/blob hashes, RED/GREEN exits, coverage, skipped native classes,
failures/corrections and actual receipts. Coordinator integrates registration
into existing manifest/workflow before final scripts/qa.py changed and
run-ci-precommit.sh --mode local-staged; proposal-only registration is not PASS.
Run document metadata/links and git diff --check. Keep SOURCE / UNIT / STATIC /
ISOLATED / HOME / MIGRATION / ROTATION / RECOVERY / DELIVERY separate. Do not
close native acceptance using reference test results or container health.

## Review and Completion

Issuance stays draft; the worker records in-progress when implementation starts.
Criterion19 requires real native notification/failure/rotation/recovery proof;
source-only delivery is reported separately and does not complete this Task.
Existing criterion10 remains the P04/P05 umbrella and cannot close on one side.

Keep logical commits for validation/builder, bounded SMTP implementation,
P04 contract binding, native/failure/restore evidence and operational docs.
Coordinate shared hunks after final image/SQL/endpoints freeze, then retest the
combined head. P04 dependency delivery comes before the P05-only owning-Spec
PR merge; preserve logical commits rather than folding unrelated work into it.
Required CI and independent reviews apply to its latest head; a head change
reruns affected checks/review. Record PR/head/merge SHA and actual runtime
state separately. Retire branches/worktrees only after delivery and evidence
preservation; never delete dirty/undelivered work to satisfy a Stop hook.

Hand P04 ack/retry/duplicate/requeue and restore findings with final consumer
SHA/interface hash; P02 native execution-copy/reference/rotation classification;
P03 actual executor/endpoint/network denials; SEC01 installed node/image
compatibility; P01/P06 future management/native credential refresh boundary;
P07 measured polling/resource facts; P08 final subject0053 paths; P10 the full
publication-to-capture failure/recovery fixture. Each handoff names final SHA,
actual versus NOT_RUN lanes, proposal base blobs and next exact commands/inputs.
Wiki implementation/schedules, learning-app planning, LAB runtime, raw Git
collection, external workspace and blog-data writes remain excluded.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Request reconciliation](../../0212-request-baseline-and-reconciliation/spec.md)
- [P04 SQL/publication owner](tsk-0012-p04-airflow-manifest-pipeline.md)
- [SEC01 image/security](tsk-0009-sec01-stable-security-integration.md)
- [SMTP01 owning Task](tsk-0005-cross-tier-contracts-second-round.md)
- [CLN01 consumer assessment](tsk-0007-cln01-material-retirement.md)
- [P02 catalog](tsk-0010-p02-secret-catalog-and-views.md)
- [P03 integration](tsk-0011-p03-service-integration-contracts.md)
- [n8n guide](../../../05.operations/guides/0053-n8n.md)
- [n8n source](../../../../infra/07-workflow/n8n/README.md)
- [Mailpit source](../../../../infra/11-quality/mailpit/README.md)
- [Official external secret stores](https://docs.n8n.io/external-secrets/)
- [Official queue execution](https://docs.n8n.io/hosting/scaling/queue-mode/)
- [Selected SMTP node source](https://github.com/n8n-io/n8n/blob/34ab9c7bf3d0c6d2ec3422e12e0b970aea5717c7/packages/nodes-base/nodes/EmailSend/v2/send.operation.ts)
