---
title: "P05 n8n Independent Outbox Notifier Task"
version: "0.4.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0013"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P05 n8n Independent Outbox Notifier Task

## Overview

### Objective

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

One P05 writer now uses `codex/p05-n8n-outbox-integrated` in
`/home/hyunyoun/data/hy-home.docker/.worktrees/p05-n8n-outbox-integrated`, from
the observed clean local main `4c83f14b11a77e13e582eb85d0bf256685472a95`.
The user's common-gate handoff explicitly authorizes preservation, a new
worktree, source-only P04 reconciliation, default checks and logical commits.
The old issuance worktree and its 28 staged paths remain preserved unchanged.
This phase authorizes no push, PR, runtime or shared-file mutation.
Other writers are active: never reset, stash, clean,
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

### 현재 후속 증거 인계 — 2026-10-22

현재 builder/transport는 lease_until을 포함한 six-field claim과 SQL004의
schema-v3 quarantine 계약을 소비한다. 후속
[Task0018](tsk-0018-workflow-lease-and-connect-safety.md)은 그 safety correction과
isolated SQL 증거를, [Task0019](tsk-0019-n8n-native-notification.md)는 최종 검토
소스의 W74 attempt 11에서 native/cleanup PASS와 여섯 terminal execution을
보고한다. 아래 2026-10-13 source-binding/preflight의 NOT_RUN은 당시 입력의
기록이며 이 후속 supporting evidence와 구분한다.

W74는 독립 synthetic fixture다. 같은 data의 Airflow→n8n W65 vertical, HOME,
실제 provider delivery, credential rotation 또는 criterion 19 owner 수락으로
승격하지 않는다. Criterion 19는 pending을 유지한다. Frozen Evidence에서
source review PASS가 document/shared-gate FAIL을 `Resolves`로 가리키더라도
review만으로 metadata나 registration 실패가 해소되지는 않는다. 실제 integrated
checks와 현재 입력의 등록 gate 결과를 별도로 평가하며 과거 결과는 보존한다.
이번 조정은 공개 소스 대조이며 새 native 실행이나 수락을 수행하지 않았다.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0013 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0013 | ready | in-progress | #w40-w41-source-execution |

### W40 W41 Source Execution

The historical source-start request started W40/W41 in the issued P05 worktree.
Its clean
starting HEAD and branch were `f7543e0697e2473cbbbeb254792e7a1d5b4b8423`
and `codex/p05-n8n-outbox-notifier`. Read-only `git ls-remote origin
refs/heads/main` returned `4e26a5a8022a7307c7461af60337442912955df1`;
`gh pr list --repo buenhyden/hy-home.docker --state open` returned no open PRs.
Both commands exited0. At that observation, local main was at issuance HEAD;
it was not pushed. P04's Task and workload/tests were dirty and preserved;
no reviewed SQL hash or publication receipt had been handed off.
W42-W44 were NOT_RUN.

The implementation is split between the builder/graph/fixture/test owner and
the bounded native SMTP-node owner; they share this Task, separate exact file
scopes and no operational permission. Independent reviewers receive read-only
scope. Applicable cost/token/time/retry ceilings and native budget enforcement
are UNKNOWN; no account or runtime limits are inferred. The controller owns
this Task and new workload navigation, and serializes final review/index/commit.
The `test-authoring` skill and `test-design`, `diff-review`, `commit-message`
and `handoff` prompt contracts apply to their respective outputs.

The provisional consumer contract is explicitly unbound. It contains no
invented P04 commit/hash, native credential ID, installation receipt or role
grant. The generated workflow stays inactive; custom-node registration,
network grants and suite registration are shared-owner proposals.

Fresh baseline regression command from this worktree:

```sh
rtk proxy /tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests \
  tests.lib.ops.test_smtp_contract \
  tests.validation.test_service_wiring_contracts -q
```

Result: 45 tests PASS, 2.940s, exit0 on issuance HEAD. This is UNIT evidence;
no native import, SMTP capture, schedule, credential or restoration ran.

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

### Historical W41 Source Results

The controller resumed ownership of both source/test lanes after delegated
tool/escalation calls stalled; existing edits were preserved and the transfers
were acknowledged before further writes. The builder's initial test landed,
but its worker did not observe RED. The controller then ran its five tests:
exit1 with five expected missing-builder errors, before writing the builder.
Eight graph/binding/preflight tests subsequently exited1 with four expected
missing generated JSON/contract/preflight errors before those artifacts existed.
The node owner observed the initial missing-dist RED (exit1).

Final source snapshot SHA256 is
`496e59646b17d6031f2687635bc0b9aaaba4818a1263e5a48572b6e148b088e5`,
over the 27 new owned source/document/test paths, using SHA256 of the
sorted JSON path-to-SHA256 map. The final map is preserved in ignored
`.agent-work/p05-final-source-freeze.json`. Core source hashes are:

- builder: `cb5f7611cd43a155986894441fdd67b45e872b69c3dc44a9ca482c5248cdc0e0`.
- transport: `d6cb1df02693a66806385842fcc58c668f54c0cf596ddd9d92dc15ab779083aa`.
- native node: `eb4c88949d5b9547a2572754c46275e921e60232f5032c82ddf293701915f146`.

The source has one deterministic builder, inactive JSON, supplied-reference
draft binding, public synthetic cases and fail-closed structural preflight.
It copies no P04 SQL/DAG and grants no native operation. DB statement/socket
deadline and cancellation remain UNBOUND in the consumer contract; no fictitious
Postgres JSON option claims enforcement. Actual credential IDs remain placeholders.

Corrections observed during implementation/review:

- Supplied-reference claim uses a 64-hex run, its four explicit sources and
  row_count1..5000; an early UUID/slug/count draft was corrected on both sides.
- A native error retains its node descriptor. The custom node now attaches only
  a static minimal descriptor and static code; tests reject literal claim and
  credential-reference leakage.
- Pre-send cancellation is cancelled; in-flight cancellation is uncertain,
  because DATA might already have been accepted. Owned sockets are destroyed.
- The API development dependency's Axios audit found two HIGH entries. A scoped
  exact override corrected the lock; both full and production audit now report
  zero findings. This does not remediate installed n8n images.
- A longer valid Message-ID is MIME-folded. The offline protocol test initially
  failed on a one-line assumption; it now unfolds header whitespace and asserts
  the same exact run-derived ID. No delivery assertion was weakened.
- Trailing line-terminator negative cases pass the existing node regex guards
  and the Python/JavaScript claim guards. No regex vulnerability is claimed.
- Final evidence checks caught an undeclared criterion8/W41 pair and a
  `BLOCKED` Result outside the registered domain. Both new rows now use the
  assigned criterion19/W41 pair; failed metadata is `FAIL` with pending
  acceptance and its blocking cause retained in Location. The existing Spec
  Package loader then validated all 25 canonical packages, exit0.

The following commands ran in that issuance worktree, all exit0:

```sh
rtk proxy /tmp/hy-home-p09-qa/bin/coverage run \
  --data-file .agent-work/p05-builder.coverage --branch \
  --source=infra/07-workflow/n8n/workloads/manifest-outbox-notifier/tools \
  -m unittest tests.lib.ops.test_n8n_outbox_workflow \
  tests.validation.test_n8n_outbox_contract \
  tests.validation.test_n8n_outbox_rehearsal -q
rtk proxy /tmp/hy-home-p09-qa/bin/coverage report \
  --data-file .agent-work/p05-builder.coverage --fail-under=80 -m
```

Result: 15 tests PASS; combined statement/branch coverage98percent. Preflight
tests inspect structural gaps and do not run a native rehearsal. In
`infra/07-workflow/n8n/workloads/manifest-outbox-notifier/nodes/OpsflowSmtp`:

```sh
rtk npm run test:coverage
rtk npm audit --json
rtk npm audit --omit=dev --json
rtk npm pack --dry-run --ignore-scripts --json
```

Result: 24 tests PASS, lines97.33percent, branches94.83percent,
functions87.88percent, each above80; both audits zero findings; pack dry-run
includes only public README/package/compiled artifacts. Tests use stubs and
actual Nodemailer over an in-memory Duplex byte stream; no TCP/DNS/SMTP service
connection, real credential or database is used. Source API compatibility is
not installed-image compatibility. Package/lock owns exact pins.

Ruff check and format/check passed on the six owned Python files; the second
format pass was unchanged. The local-staged official precommit controller
passed on all 28 owned paths, including JSON, Markdown, Python format/lint and
hardcoded-secret detection. It does not replace the document-contract gate.

Metadata against the actual Registry failed with ten classification findings
on exactly two required README paths under `nodes/OpsflowSmtp/`. The Registry's
lowercase subpath profile does not classify this prescribed camel-case path.
The immutable upstream version references now carry scoped advisory and
compatibility explanations, with package/lock retaining pin ownership.

The same check against a proposed Registry containing only the two exact
`package-readme.additional_paths` entries passed: nine selected documents,
zero violations, exit0. The explicit lifecycle comparison base was issuance
HEAD `f7543e0697e2473cbbbeb254792e7a1d5b4b8423`. This candidate-only result does
not mean the actual Registry or remote-main delivery gate passed. Reports are
`.agent-work/p05-metadata-current.log` and `p05-metadata-proposed.log`.

The authoritative changed-profile explain route selects document-contract,
document-graph/lifecycle, agent-governance and existing static operations gates.
The new Python and node test routes are not yet registered in its shared DAG.
No full changed-profile PASS, native PASS or latest-head CI is claimed.
At that issuance point, logical commits and PR publication were pending the
required shared Registry integration. HEAD was the issuance SHA;
all owned changes were preserved in that worktree.

Final document links passed on 1202 documents and 11635 links: zero failures,
one existing Stage98 historical-provenance warning, exit0. New README links
route through the Stage03 navigation entry, and folder routers link only to
direct child READMEs. Working-tree and cached `git diff --check` passed.

Independent code review reported no source findings and approved the W40/W41
source slice with follow-up. It directly observed the final 15 Python tests
and an earlier 21-node test pass; final 24-node/coverage/audit receipts were
controller-reported. Independent security review approved the same frozen
source with no remaining findings. Both reviewed the final digest above and
exclude shared integration, private credentials, runtime and delivery. The
final Task result record is checked separately from the 27-file source map.
Neither disposition completes criterion19 or grants native execution.

### Historical Shared Integration Proposals

Exact hunks and node gate commands are in ignored
`.agent-work/p05-integration-proposals/`; they are proposals, not acceptance
evidence or applied source. Their six base blobs at issuance HEAD are:

| Shared path | Base blob | Proposed change | Applied |
| --- | --- | --- | --- |
| docs/99.templates/registry.json | 00ea622af93736ce4e2e23854caa714601c63955 | Two exact camel-case node README paths; candidate metadata PASS, actual gate blocked | no |
| .github/workflow-contract.yml | 7dc037023853a003ef38a53d21e2c8d1ac0dd3b4 | Dedicated Python modules; typed node build/coverage/audit setup request | no |
| infra/07-workflow/n8n/README.md | e45d694458dcbb4f35cb540cc55b64f881eda1e3 | Workload navigation | no |
| docs/05.operations/guides/0053-n8n.md | 2e76cfcee57535b3e5430880877b18244af875e9 | Inactive source and native prerequisites | no |
| docs/05.operations/policies/0053-n8n.md | 9777813a5ad646392153ada772c4079bdf5adcd3 | Function-only role, capture/privacy boundary | no |
| docs/05.operations/runbooks/0053-n8n.md | e0443146d2c4de5c1f1ac494a7d15bc42f01618c | Uncertainty, fresh claim, paired restore and rollback | no |

The current script manifest permits only scripts/ and .agents/evaluations/;
the workload-local generator is outside that inventory. Manifest is NO_CHANGE;
no schema extension is introduced merely to register it. Shared image/custom
bind, DEV/capture networks, endpoint/credentials and native gate registration
still wait for their exact owner contracts. Preserve P04 dirty work and deliver
its dependency before final P05 PR integration.

### Integrated Source Work Log

The current integration baseline is local main
`4c83f14b11a77e13e582eb85d0bf256685472a95`, after P04 and P06 source
integration. Common validator/Registry commit
`085d9bf795f31d9083f290cfdbcdc1a17ba72db3` already registers exactly the
two prescribed OpsflowSmtp package README paths. No external Registry is used
for this phase's metadata check. Prior candidate-only PASS and actual FAIL
above describe the preserved issuance worktree, not the new integrated gate.

Before migration, the sole writer fixed old HEAD
`f7543e0697e2473cbbbeb254792e7a1d5b4b8423`, its index SHA256
`44c772f1fc8c6efa37758a35430ed0b04b1e6bf899c2d1c4b3c31d6b0c86e433`
and all 28 public owned file hashes. The binary staged patch SHA256 is
`44db414ba98c88746df1dadcd3c4c69f519bf634cbe39b7f406cdcb0f130f33d`.
The patch and receipt are preserved in each worktree's ignored
`.agent-work/p05-integrated-handoff/`. New worktree creation at the exact
baseline, apply-check and indexed apply each exited0. The canonical Task had
no concurrent main change since issuance; its source results remain historical
above, and this section records the current phase. Other worktrees and shared
paths were not staged or changed.

The canonical P04 SQL files are read-only inputs. Observed SHA256 values are
001 `57a744cf33581bafd73f610b9c18c83d64c9457486a02e02398df56b444ee584`
and 002 `0a00944569aa05b7a0eec6a555cc3357197b26257ee76a1779c7e258eb9a0b73`.
Their claim result includes `lease_until`; the consumer explicitly projects
only id/run_id/source/row_count/lease_token. The added regression failed with
the original SELECT-star query (exit1), then all 16 Python synthetic tests
passed after the projection fix (exit0). Contract source references assert
those hashes and six upstream fields while all native binding fields remain
null. This is source compatibility, not W42/W43 native acceptance.

Actual producer publication, function ACLs, exact image/package/UID/TLS,
credential/S3/backup and empty recovery targets remain unaccepted. Native
import, notification, polling, DEV/HOME changes, rotation and recovery are
NOT_RUN. P01 W23 and P06 pilot holds remain. Request/token/time/concurrency/
retry ceilings and shared budget allocation remain UNKNOWN.

The integrated 27-file source digest is
`55856ce4aa2f121d63102731a460b12d054651ac6ff2cab1f3743554d7774b10`; its map is frozen in ignored
`.agent-work/p05-integrated-source-freeze.json`. Task result-only changes are
outside that source map. Both independent reviewers checked that exact map:
code review reports no findings and APPROVE WITH FOLLOW-UP; security review
reports no findings and approves the source-only scope. Neither disposition
accepts installation, credentials, native execution or combined-head delivery.
Security inspected the exact source; its independent hash command was blocked
by sandbox/escalation tooling, so hash equality relies on the controller's
frozen map and passing source-contract test. The separate read-only interface
audit confirms ack/retry signatures and strict current-lease semantics; retry
true may mean retry or dead, so the public result stays delivery-uncertain.

Actual default Registry metadata passed on nine selected documents, zero
violations, exit0, using explicit base4c83f14b11 and no external Registry.
The all-document link check passed: 1213 documents, 11699 links, zero failures,
one existing Stage98 historical-provenance warning, exit0. Reports are ignored
`.agent-work/p05-integrated-metadata.log` and `p05-integrated-links.log`.
Final source input preceded this result-only record; final Task metadata and
its own staged gate are required again before the documentation commit.

Python synthetic coverage command remains the one recorded above, now from
the integrated worktree: 16 tests PASS, combined coverage98percent, exit0;
the original five-field projection regression first failed as recorded.
The six owned Python files passed Ruff lint and format/check. The existing
workflow-version/SMTP/wiring regression command passed all45 tests in3.366s,
exit0, on the integrated baseline.

In the OpsflowSmtp package, `npm ci --ignore-scripts --no-audit --no-fund`
installed the exact lock. `npm run test:coverage` built the TypeScript and
passed24 offline tests, with lines97.33percent, branches94.83percent and
functions87.88percent. `npm audit --json` and `npm audit --omit=dev --json`
both exited0 with zero findings; `npm pack --dry-run --ignore-scripts --json`
exited0 with eight public README/package/compiled files and no publication.
All transport tests remain stubs or in-memory protocol bytes: no DB/TCP/DNS/
service SMTP connection, runtime credential or installed-image acceptance.

The official `run-ci-precommit.sh --mode local-staged` passed all28 owned
paths before partition, exit0, including metadata-independent Markdown/JSON/
Python style and secret detection. Every logical unit then separately passed
Commitizen and that same staged gate immediately before its ordinary commit.
The first ordinary node commit was blocked by the installed Git secret guard
on a synthetic long password marker. No commit or bypass occurred. Replacing
only that test marker with `dummy` preserved nonempty-password rejection and
zero transport calls; Node build/24 tests/coverage and both independent source
reviews then passed again for the final digest above, followed by the per-unit
staged gate. No real secret, dependency or production behavior changed.
Working-tree and cached `git diff --check` passed. A full registered changed
profile, hosted/latest-head CI, PR, push and merge are NOT_RUN; their combined
head cannot be accepted before the coordinator registers the new gates.

Refreshed shared proposals are in ignored
`.agent-work/p05-integration-proposals/proposal-index.json`; all five patch
apply-checks exited0 without application. Registry is NO_CHANGE_ALREADY_INTEGRATED
at085d9bf795, current blob `d792252f37995e09a7d24d739953b2873b1a88af`.
The three Python modules and workload prefix appear in both changed-path and
changed-root routing proposal tables. The exact node lock/build input hashes
and setup/coverage/audit/pack command arrays request one typed Node integration
and the same prefix in both routes. The coordinator owns adapters, budgets,
registration, application, regression checks and combined-head acceptance.

| Shared path | Current base blob | Applied |
| --- | --- | --- |
| .github/workflow-contract.yml | 0788cfe0197a279660c4effb9d6f4d83ba8e17f9 | no |
| infra/07-workflow/n8n/README.md | e45d694458dcbb4f35cb540cc55b64f881eda1e3 | no |
| docs/05.operations/guides/0053-n8n.md | 2e76cfcee57535b3e5430880877b18244af875e9 | no |
| docs/05.operations/policies/0053-n8n.md | 9777813a5ad646392153ada772c4079bdf5adcd3 | no |
| docs/05.operations/runbooks/0053-n8n.md | e0443146d2c4de5c1f1ac494a7d15bc42f01618c | no |

### Commit Ledger

| Commit | Logical unit | Scope | Verification |
| --- | --- | --- | --- |
| 9aee10677c5d1aa8481a843ca92d7db9a713c6d3 | Bounded SMTP capture node | 13 node/package/test/navigation paths | Node coverage/audits/build/pack, independent source reviews, Commitizen and per-unit staged gate PASS |
| 673dd0fc72ae9aa6505fc15a2ff9f097da967f63 | Inactive workflow and source contracts | 14 builder/workflow/fixture/contract/test/navigation paths | 16 Python tests, coverage, default metadata/links, independent source reviews, Commitizen and per-unit staged gate PASS |

This final Task record is a separate documentation commit; its full SHA is
resolved from branch HEAD in the final machine receipt, without a self-reference.
Next action is coordinator integration of the fixed source commits and refreshed
typed Node/Python/workload proposals, followed by combined-head gates.
Native notification and DEV/HOME changes remain NOT_RUN.

### Coordinator Common Integration — 2026-10-11

The coordinator adopts worker HEAD
`53212d0b494f72658c52a4992fb4067936cf87da` and preserves all three logical
commits in the dedicated `codex/p05-common-integration` worktree. The 27 public
source files retain digest
`55856ce4aa2f121d63102731a460b12d054651ac6ff2cab1f3743554d7774b10`.
The old notifier worktree's 28 staged paths and binary patch digest
`44db414ba98c88746df1dadcd3c4c69f519bf634cbe39b7f406cdcb0f130f33d`
remain unchanged. The unrelated shared checkout's 24 paths remain untouched.

At baseline `4c83f14b11a77e13e582eb85d0bf256685472a95`, direct remote main
has the same SHA and GitHub reports no open PRs. These are remote observations;
the worker source commits and current common changes are local only. The four
public n8n README/Guide/Policy/Runbook proposal bases matched exactly before
application. The coordinator applies those navigation and source-only usage
changes, with preserved IDs/created timestamps. Registry is already integrated
and unchanged. No source manifest records are needed for workload-local tools
outside its governed script roots.

Actual workflow registration adds the three Python modules to the existing
repository-integrity leaf and routes the workload/tests in both changed-path
and changed-root tables. The exact OpsflowSmtp package prefix additionally
selects a typed package aggregate. Five fixed npm operations use only that
package directory: install, dependency audit, production dependency audit,
coverage/build and dry-run pack. Audits precede candidate build/test scripts.
Existing workflow jobs, action pins, permissions, audit acceptance and
P02/P03/P04/P06 registrations are retained. CI-only package leaves are excluded
from unauthenticated local execution; no hosted result is inferred from a local
plan or direct npm invocation.

Fresh coordinator commands from the dedicated worktree passed, exit0:

```sh
env PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.lib.ops.test_n8n_outbox_workflow \
  tests.validation.test_n8n_outbox_contract \
  tests.validation.test_n8n_outbox_rehearsal -q
```

This passed16 synthetic tests in0.191s. From the exact OpsflowSmtp directory,
Node v26.10.0 ran `npm ci --ignore-scripts --no-audit --no-fund`,
`npm run test:coverage`, `npm audit`, `npm audit --omit=dev`, and
`npm pack --dry-run --ignore-scripts --json`; each exited0. The24 offline tests
measured lines97.33percent, branches94.83percent and functions87.88percent.
Both audits reported zero findings; pack selected eight public files without
publishing. The transport tests stayed offline; npm used public dependency operations.
No application DB/SMTP connection or runtime node installation occurred.

The first workflow-validator invocation used nonexistent
`check-workflow-contract.py` and exited2; no validator ran. The corrected
`check-github-workflow-contract.py` exited0 on the initial registered candidate.
An unauthenticated `run-ci-gate.py --profile changed --explain` exited0 and
selected nine local leaves. Its exclusion of CI-only package leaves is expected,
not successful hosted package execution.

Initial typed-adapter RED/GREEN and127 gate tests passed on the pre-review
candidate, with86percent combined branch-enabled coverage. Subsequent independent
security review blocked that input: candidate coverage ran before audit and
inherited a repository-root FD. That receipt is superseded for final acceptance.
The correction removes root capability/environment forwarding to npm, uses the
fixed package directory FD, runs audits first, and rejects coverage mutation of
explicitly frozen source/control inputs. It does not promise whole-checkout
immutability or constrain arbitrary external hosts. Final corrected-input tests,
metadata, staged gate, independent review and local-main delivery are recorded
separately in the coordinator receipt after they actually finish.

The corrected frozen-input gate command executed by the delegated CI engineer
was `/tmp/hy-home-p09-qa/bin/python -m unittest
 tests.lib.gate.test_ci_gate_adapters tests.lib.gate.test_ci_gate_contract
 tests.validation.test_ci_gate_plan tests.validation.test_ci_gate_execution_context
 -v`, with PYTHONDONTWRITEBYTECODE=1. It passed128, exit0; log
`/tmp/p05-node-gate-4modules-security-final.log`. Branch-enabled coverage of
adapter/contract/runner measured combined86percent (individual83/88/86), and
`coverage report --fail-under=80` exited0. Raw data and report are
`/tmp/p05-node-gate-security-final.coverage` and
`/tmp/p05-node-gate-coverage-report-final.log`. This is synthetic harness testing,
not hosted CI or native consumer authentication. The exact aggregate order is
validated with a negative reorder regression; missing-child diagnostic
precedence is retained. Lockfile and adapter mutation regressions fail closed.
Final security re-review passed with no P1/P2 findings. Scoped Ruff0.15.12 lint,
format check and `git diff --check` passed on the frozen seven implementation/
regression files. Independent combined-head quality review and final staged/
metadata/local-main receipts remain separate below or in the coordinator ledger.

Workflow SHA256 is
`a7df8a8200c6865ec766f7701f54d9de3271a292d988657f1a95f802ead25ea7`.
Adapter SHA256 is
`7f5f64dcedd4f79cabdfa5de1f1f355521315c570cc298046b7d9cbdf4d2f4d6`;
contract SHA256 is
`89e00e59aa8bf0f8bd4524e7239cd0f9e6b9c59152df2041192c259175d9d740`;
runner SHA256 is
`77d5a3e418e32cd4026283d2b655adb29f4739e51889407811f9e6b5103cc7ba`.
The frozen map in the ignored receipt includes the remaining four tests.
Fresh all-document links passed1213 documents/11701 links, exit0, with zero
failures and one pre-existing archive capture warning. No frozen source or
package lock/build input was rewritten by the npm checks.

Receipt paths under ignored `.agent-work/` retain public commands, input hashes,
failed attempts, corrected results and final commit/main ancestry. This section
keeps native W42/W43/W44 and criterion19 in-progress. P04 SQL hashes remain the
same read-only bindings and native identity/version fields stay null. Exact
SEC01 package/image, P03 UID/executor/TLS/endpoint, P02 credential delivery,
P04 producer/function grants/S3 policy and paired backup/empty-restore acceptance
are still required. No import, schedule activation, DEV/HOME change, migration,
rotation, private deletion or recovery ran. P01 W23 and P06 pilot holds remain.

### Segmented Local Source Validation — 2026-10-11

Frozen source input is `5b1a92db48fd508feff4cee0753b3b4468dd41dc`, following
common/worker integration `c7d56a383ad8b77dd615327d11605b3e15d2146e`.
The registered local execution plan has33 nodes; public explain exposes10.
The front-door run exited124 after nodes0–9 passed. First canonical continuation
exited1 at node18; nodes10–17 passed. Permission-corrected continuation exited1
at node26; nodes18–25 passed. Final continuation26–32 exited0 with ordinary
Python, debug true/optimization0 and clean unchanged post-input. Thus all33
nodes have segmented successful receipts; the original124 and both suffix1
failures remain failures. No fresh aggregate exit0 or hosted PASS is claimed.

Only two coordinator-checkout entrypoint modes changed775 to755, matching their
tracked100755 modes: Open WebUI and Gatus. File content hashes and index were
unchanged, with Git clean and no HOME/runtime effect. The only source delta
from c7d56a383 is the synthetic workflow fixture's canonical working directory,
seven changed lines in the existing test. RED: one test/four subcase failures,
exit1,1.769s; GREEN:39 tests,exit0,7.492s; Ruff/staged checks exit0 and independent
review ACCEPT. The registered workflow contract SHA256 remains
`bdb1941e522865a9a381b0913f4a8e266dfb613cbb832ca35889ff26ac3ecfc5`.

Receipts are `.agent-work/p04-p07-registered-suffix-final-fixture-result.json`,
`.agent-work/p04-p07-checkout-permissions-repair.json` and
`.agent-work/p05-fixture-cwd-receipt.json`; final output is
`.agent-work/p04-p07-registered-suffix-final-fixture.log`. Earlier aggregate and
suffix logs remain preserved. These SOURCE/UNIT/STATIC checks do not complete
operational criteria. Local-main source integration awaits final documentation
checks and review; its delivery SHA is not yet known. Current direct-user
local-main delivery uses no dev, remote push, PR or hosted execution.

Combined P04/P05 synthetic checks passed196 in19.313s, exit0; separate P06/P07
checks passed62 in16.592s, exit0. Earlier24 offline Node tests and source audits
retain their original input/version attribution and are not SMTP/native receipts.
P04 retains sole ownership of SQL/outbox contracts; no copy or new provisioning
was introduced. The final repository leaf passed494 tests/127.874s, exit0.
Criterion19/W42–W44 remains open: actual frozen native SQL consumption, import,
credential binding, queue-worker capture, scheduling and recovery are NOT_RUN.
Source/common commits are preserved; no fresh coverage or production acceptance
is inferred. Final Task checks and local-main source delivery remain pending.

### Owner decision 2026-10-29

On 2026-10-29 the owner split criterion 19. Its native evidence covered
manual execution only: TSK-0019 W74 attempt 11 proved inactive import, the
actual queue worker and external runner, Mailpit capture, Message-ID,
unknown-outcome isolation, reconciliation, restart and generation-2 metadata
and database restoration, and TSK-0018 W73 proved stale-lease rejection and
ambiguous-send quarantine. No native run covered one-minute scheduled
execution, concurrent claims, retry and dead-letter, or credential rotation.
Those obligations move to new criterion 22, which this Task owns through
W42–W45; their rows now name criterion 22 and stay open. Criterion 19 is
accepted for the narrowed text.

The Evidence and Criterion Acceptance tables move to the current shape so the
decision can be recorded: each row gains `Required`, and each criterion row
gains its current owner. `Independent source reviews` named the earlier
`Document and shared gate integration` FAIL in `Resolves` with a different
check, which the current shape does not allow, so its `Resolves` is now `-`
and `Rerun of Document and shared gate integration` resolves that FAIL with
the same check on today's `main`.

### Criterion 22 harness source 2026-10-30

The owner chose to build the criterion 22 harness, register it in the gate and
merge it after independent review. The opt-in native class
`OpsflowN8nNativeRehearsal` in `tests/validation/test_opsflow_native_rehearsal.py`
now runs seven further steps after the existing manual run: scheduled
execution, concurrent claims, retry and dead letter, empty queue, database
credential rotation, paired restore decrypt in the fresh generation, and wrong
key fail-closed after a correct-key control on the same path. The helpers live
in `tests/validation/_opsflow_native_criterion22.py`, and the Docker-free guards
in `tests/validation/test_opsflow_native_criterion22.py` join the default gate
through `.github/workflow-contract.yml`. The work budget rises from 25 to 40
minutes. SMTP credential rotation stays NOT_RUN, because Mailpit has no
authentication to rotate.

Security review approved; its medium finding (no correct-key control for the
explicit-key path) and the shared `/tmp` probe path were fixed. Code review
asked for changes, all applied: the race and retry outputs join a boolean onto
text, which PostgreSQL renders as `true` or `false`, so the parsers and stubs
had expected the wrong `t` or `f`; the session check after rotation now waits
for terminated backends; and two minor test defects were removed. The concurrent
claim and retry scenarios drive the database contract as the notifier role in
`psql`, with the retry backoff fast-forwarded by the superuser, and the receipt
records this as `driver` and `backoff` facts. Accepting criterion 22 on that
reading is the owner's decision. After the fixes the offline set ran 67 tests,
OK, one skipped (the opt-in native class), and the workflow contract and its
gate tests passed. This is source only: no Docker command ran, W42 still waits
for P04 W36, and criterion 22 stays pending until one approved native run
returns its receipt.

### Owner native attempt 2026-10-30

The owner ran the opt-in native class once from `main` at `032818766`, before
the criterion 22 harness merged, so the run carried none of the criterion 22
steps. Attempt `opsflow-native-1b407daf3eb9138fa67527cb` used image
`sha256:1fda18a541144ae5519ac97bcaffa4e24fad0e71d424606d230464bec8fce153`, the
same image as TSK-0019 attempt 11, and source binding `03892eb1a9a4`. Main
readiness and liveness, the worker broker and Mailpit all answered 200. The
first manual execution did not turn terminal within 60 seconds, so the run
stopped with `native` ERROR after 598.7 seconds. Cleanup passed: all eight
containers were confirmed absent and nothing was retained.

The harness for that step is unchanged since attempt 11, and the receipt kept
no execution status or log, so the cause is unknown. The harness now records
`execution_timeout_facts` when a queued execution times out: the last status
seen and whether known main and worker log lines exist, as booleans only. One
further native run is needed.

### Owner native attempt with criterion 22 steps 2026-10-30

The owner ran the native class again from `main` at `4de81f1a4`, with the
criterion 22 harness and timeout diagnostics. Attempt
`opsflow-native-5c855b474d846df902d87001` used the same image and source
binding. This time the earlier steps passed: executions 1 to 4 turned
terminal and every health probe answered 200. In `scheduled_execution`, the
scheduled delivery itself passed: one trigger-mode execution within 60
seconds, with the worker as the only member of the DEV network. The next
publication then failed in PostgreSQL, so that step was recorded FAIL, the
later six steps NOT_RUN, and `native` ERROR after 715.6 seconds. Cleanup
passed and nothing was retained.

The cause is a harness defect, not the notifier. `003_business_date.sql`
adds a unique index on source and UTC business date, and `publish_next` gave
every publication a time on 2026-10-16, the day of the earlier
`hy-home.docker` publication. Each criterion 22 publication now takes its own
UTC day from 2026-10-17, still rising, and the offline test pins those dates.
The first attempt's manual-execution timeout did not recur, so it remains
unexplained. One further native run is needed.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Git and owner baseline | 1, 19 | W40 | status/worktrees/fetch/open PR list | Local/remote4e26a5a80 | PASS | Baseline only; no remote or runtime write by this assessment | required | - |
| Existing source contracts | 1, 8, 19 | W40 | Workflow version, SMTP and service wiring unittest | Clean4e26a5a80 | PASS | 45 tests, 3.023s, exit0; command below | required | - |
| Supplied reference audit | 19 | W40 | Six public files, four static tests and JSON generator parity | Prompt669a86c89a76 | PASS | 4 tests, 0.02s, exit0; generator semantic parity; no native proof | required | - |
| New notifier source | 19 | W41 | RED/GREEN builder/workflow/transport/privacy | Source snapshot 496e59646b17 | PASS | 15 Python and 24 offline node tests; coverage and audit above; native acceptance is separate | required | - |
| Document and shared gate integration | 19 | W41 | Metadata, links, precommit and gate routing | Actual Registry at issuance; exact proposal only | FAIL | Links/precommit pass; actual metadata has ten findings on two node README paths; candidate-only metadata passes; shared CI registration pending | required | - |
| Independent source reviews | 19 | W41 | Code/specification and source-security review | Source snapshot 496e59646b17 | PASS | Code approved with follow-up; security approved; no remaining source findings; runtime/delivery excluded | required | - |
| Integrated source checks | 19 | W41 | Default Registry metadata, synthetic tests/coverage/audit/build/pack, links and staged gate | Source snapshot 55856ce4aa2f; base4c83f14b11 | PASS | Integrated work log and ignored receipts above; native and combined-head acceptance excluded | required | - |
| Integrated independent reviews | 19 | W41 | Code and security review | Source snapshot 55856ce4aa2f | PASS | No source findings; code approved with follow-up; security approves source-only scope | required | - |
| Frozen P04 binding | 22 | W42 | Reviewed SQL/version/hash and roles | P04 W36 pending | NOT_RUN | P04 remains sole SQL owner | required | - |
| Native import and manual execution | 22 | W43 | Exact image, credential and worker/SMTP proof | P04 W38 and relevant readiness pending | NOT_RUN | No import/credential/network/DB action | required | - |
| Scheduled failures and recovery | 22 | W44 | Polling, outages, restart/rotation and empty restoration | No exact action selected | NOT_RUN | No operational acceptance | required | - |
| Delivery | 8, 22 | W45 | Latest-head CI/review/PR/merge | Integrated source phase | NOT_RUN | Two source commits recorded above; final Task commit and combined-head registration/CI remain separate; native holds are unchanged | required | - |
| Segmented source checks | 8 | W45 | Registered local nodes0–32 across preserved runs; final continuation26–32 exit0 | c7d56a383 then5b1a92db; unchanged registered contract | PASS | Segmented Local Source Validation; original aggregate124 and suffix1/1 preserved; final docs/delivery pending | required | - |
| Rerun of Document and shared gate integration | 19 | W41 | Metadata, links, precommit and gate routing | `main` at merged PR #640 with the notifier source and node READMEs | PASS | `check-document-metadata.py --mode check-contracts` 0 violations; `check-document-links.py --mode all` PASS; PR #640 `candidate-quality` run 40874942142 success, which runs pre-commit and gate routing | required | Document and shared gate integration |
| Criterion 22 harness source | 22 | W44 | Offline scenario guards, gate registration and independent review | Worktree on `main` at merged PR #654 | PASS | Criterion 22 harness source 2026-10-30; 67 tests OK with the native class skipped; no native run | required | - |
| Owner native attempt | 22 | W43 | Opt-in native class, first manual execution | `main` at `032818766` before the criterion 22 harness; attempt `opsflow-native-1b407daf3eb9138fa67527cb` | FAIL | Owner native attempt 2026-10-30; queued execution did not turn terminal in 60 s; cleanup PASS | required | - |
| Owner native attempt with criterion 22 steps | 22 | W44 | Opt-in native class, criterion 22 scenarios | `main` at `4de81f1a4`; attempt `opsflow-native-5c855b474d846df902d87001` | FAIL | Owner native attempt with criterion 22 steps 2026-10-30; scheduled delivery passed, next publication hit the business-date index; harness fixed; cleanup PASS | required | - |

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
into existing manifest/workflow before final registered changed-profile QA and
run-ci-precommit.sh --mode local-staged; proposal-only registration is not PASS.
Run document metadata/links and git diff --check. Keep SOURCE / UNIT / STATIC /
ISOLATED / HOME / MIGRATION / ROTATION / RECOVERY / DELIVERY separate. Do not
close native acceptance using reference test results or container health.

W40 corrected a stale verifier route: `scripts/qa.py` does not exist at the
issuance HEAD (attempt exited2). The current controller is
`scripts/validation/run-ci-gate.py --profile changed --explain`; executable
local leaves use its `--local-only` route and hosted aggregate acceptance stays
separate. No shared harness was created or replaced to satisfy the stale text.

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 19 | accepted | Git and owner baseline, Supplied reference audit, New notifier source, Integrated source checks, Integrated independent reviews, Rerun of Document and shared gate integration | Owner accepted on 2026-10-29 for the narrowed criterion: this Task's source rows plus native manual execution, isolation, reconciliation, restart and restoration in TSK-0018 W73 and TSK-0019 W74. | SPEC-0204 TSK-0013 |
| 22 | pending | - | - | SPEC-0204 TSK-0013 |

## Review and Completion

The Task remains in-progress; W41 source evidence does not complete criterion19.
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
- [n8n guide](../../../05.operations/guides/08-workflows-and-automation/0053-n8n.md)
- [n8n source](../../../../infra/07-workflow/n8n/README.md)
- [Mailpit source](../../../../infra/11-quality/mailpit/README.md)
- [Official external secret stores](https://docs.n8n.io/external-secrets/)
- [Official queue execution](https://docs.n8n.io/hosting/scaling/queue-mode/)
- [Selected SMTP node source](https://github.com/n8n-io/n8n/blob/34ab9c7bf3d0c6d2ec3422e12e0b970aea5717c7/packages/nodes-base/nodes/EmailSend/v2/send.operation.ts)

### W42 image-owned package bridge source increment — 2026-10-12

The coordinator assigned one writer at `codex/p05-install-completion`, clean
baseline `241a470d246191751a7a5655a86d5ec4f679a0ff`, with an explicit lease for
both n8n Dockerfiles and existing entrypoints, a worker-only workload overlay,
this Task and the two existing offline validation modules. SEC01 version/digest
selection and other workers' changes are preserved. No root Compose, secret,
CI, catalog, workflow builder, TypeScript transport or old staged P05 change
is overwritten. The Task remains in-progress; criterion 19 is not accepted.

The selected [exact upstream loader](https://github.com/n8n-io/n8n/blob/n8n%402.42.6/packages/cli/src/load-nodes-and-credentials.ts)
loads the default custom directory before additional directories; each custom
loader uses the `CUSTOM` package name and replaces that loader slot. An added
custom-directory env alone would hide default nodes and change the tracked
`n8n-nodes-opsflow.opsflowSmtp` identity. That proposed route is rejected.
[Community module loading](https://github.com/n8n-io/n8n/blob/n8n%402.42.6/packages/cli/src/modules/community-packages/community-packages.module.ts)
uses the instance settings nodes directory and
[package scanning](https://github.com/n8n-io/n8n/blob/n8n%402.42.6/packages/core/src/nodes-loader/scan-directory-for-packages.ts)
selects the canonical package through an API compatibility guard.
The [folder utility](https://github.com/n8n-io/n8n/blob/n8n%402.42.6/packages/%40n8n/config/src/utils/utils.ts)
uses `N8N_USER_FOLDER`, then the existing HOME, then cwd, with `.n8n` appended.
The bridge does not modify HOME or read credentials for this discovery check.

Both Dockerfiles use the latest stable Current Node builder identified by SEC01
on 2026-10-12 from the [official release channel](https://nodejs.org/en/blog)
and [release directory](https://nodejs.org/download/release/v26.11.1/),
`node:26.11.1-alpine3.24@sha256:143494b1da2945f061539253adc65e4f1569ddf07da2d384c022c791a9d90a4a`.
SEC01 supplied a successful immutable index inspection and amd64 manifest
`sha256:7b6a85d8b6e3c3d931431979884a97b99bad974cc686097915cec3c07d462ad7`.
This is an attributed SEC01 observation; the P05 writer did not repeat it. The
[exact upstream Dockerfile](https://github.com/n8n-io/n8n/blob/n8n%402.42.6/docker/images/n8n/Dockerfile)
uses an earlier Node builder and does not exempt this new input from latest
stable evaluation. Exact new-builder compatibility remains unexecuted.
This new build input requires SEC01 supply-chain/image acceptance; its immutable
reference is not a vulnerability scan or selected runtime proof. The existing
package/lock is installed without dependency lifecycle scripts, compiled through
the explicit TypeScript CLI, and pruned without lifecycle scripts. Only package
metadata, compiled output and production dependencies enter the final immutable
`/opt/hyhome/n8n-custom/opsflow` artifact with a complete SHA256SUMS receipt.
The declared n8n service and runner versions/digests are unchanged.

Both entrypoints verify image-owned, non-writable, non-symlink artifact metadata,
receipt uniqueness/completeness, every deployed hash and canonical package/API
identity before publishing exactly one symlink under the configured n8n nodes
package directory. Unknown files/directories, foreign/dangling links, unsafe
parents, tampering and mismatch fail with a static code, without deletion or
replacement. Atomic symlink creation plus exact recheck accommodates two starters.
There is no runtime npm install, download or database package registration.
Existing custom mounts and all sibling community packages remain untouched.
The optional overlay attaches only `n8n-worker` to DEV and capture networks;
main and task runners receive neither attachment. Network membership is not a
firewall, authentication or native capture proof; actual Mailpit/egress/UID/TLS
acceptance still requires the P03 and coordinator runtime boundary.

Witnessed pre-change RED: the worker-placement class failed once because its
optional overlay was absent; the image-bridge class failed twice because the
unmasked locked artifact and bridge were absent. First GREEN failed on a synthetic
fixture's writable mode; strict source checks were retained and fixture modes
were corrected. The first three-module regression failed once because an older
credential-only probe included the new bridge without any image artifact. Its
boundary now ends at the bridge marker; the bridge has separately executed
negative fixtures. These failures are not native service failures.

Actual `rtk proxy python3 -m unittest -v
 tests.validation.test_service_runtime_compatibility
 tests.validation.test_workflow_version_bundle
 tests.validation.test_n8n_outbox_contract` ran 41 tests: 38 passed and three
explicit image-native opt-in tests were skipped, exit 0. The ten-test P05 module
includes seven prior contracts and three new image/placement fixtures. Synthetic
inputs substitute only the image path/owner and ancestor paths, never deployed
files. Covered behaviors include sibling/default-node preservation, repeat and
concurrent exact-link creation, unknown asset preservation, altered hashes,
symlinked dependencies, duplicate receipts, extra unlisted files, writable
packages, unsafe folder paths and the official fallback selection. This is not
actual package discovery inside the selected image.

The initial registered-run controller incorrectly selected four internal leaves
as public roots and exited 1 before executing any child. Corrected invocation
used the real registered `ci.opsflow-smtp-node-package` root with unmodified
node argv/order/env/timeout: setup, dependency audit, production audit, compiled
source coverage, then pack. All five nodes completed, aggregate exit 0.
The existing host tool was Node v26.10.0; it is not the image Node receipt.
There were 24 Node tests PASS; compiled Opsflow source coverage was line 97.33%,
branch 94.83%, function 87.88%, with both audits reporting zero vulnerabilities.
Pack dry-run included eight files and preserved canonical package name/version.
These are source-package receipts, not image supply-chain or HOME acceptance.

SOURCE is implemented; UNIT/source-package checks passed. Final STATIC/review/
commit admission is pending coordinator acceptance of the exact frozen unit.
ISOLATED native discovery, HOME, P04 publication/outbox consumption, actual SMTP
capture, MIGRATION, ROTATION and RECOVERY remain NOT_RUN for this increment.
No Docker pull/build/start, workflow import/schedule, credential, DB or runtime
state change occurred. When separately deployed, the bridge may create bounded
`.n8n/nodes/node_modules` directory scaffolding and its exact one-package link.
Rollback first deactivates the selected workflow and stops affected consumers,
restores the reviewed image, and removes only that exact link after ownership
validation. Directory cleanup requires an operator receipt identifying newly
created directories and matching filesystem identity; only those directories
may be removed while empty. Pre-existing, nonempty and unknown assets are
preserved; the source bridge provides no automatic cleanup executor.

The first staged gate exited 2: Markdown formatter changed one blank line and
hadolint reported DL3003 for a build-directory `cd`. The second retry still
reported that blank line because the admission wrapper restores candidate bytes;
the source was explicitly corrected and Docker WORKDIR now owns that switch.
No lint exemption was added. Final staged checks are recorded after review.
A copied public package production-prune probe exited 0 (165 packages removed,
169 artifact files, no symlinks) and its closed hash receipt/bridge passed with
fixture path/owner substitutions. A direct compiled-export probe without the
n8n loader environment exited 1: `n8n-workflow` is a runtime peer after pruning.
The exact upstream loader initializes NODE_PATH from its module resolution paths;
selected-image peer resolution and actual discovery remain NOT_RUN. No dependency
was silently copied from host global installations into the final artifact.

Final source admission used the frozen eight-path candidate at
`241a470d246191751a7a5655a86d5ec4f679a0ff` with pre-receipt staged diff SHA256
`3e12d2e145860f29f8c12b7612d0344cca7dfe5e7007e457460e9384cbb578a5`.
Independent final code/security review approved the source-only patch with no
Critical or Important findings. Its Minor directory-scaffolding wording finding
was corrected above; this receipt delta does not change production/test inputs.
Native image, loader discovery, runtime API peer, DB, SMTP, HOME and recovery
acceptance remain open. The bridge source itself has no measured coverage claim;
the registered Node coverage numbers above apply only to the existing Opsflow
package compiled source.

The actual `infra-validate` skill helper exited 2 with 11 PASS, four BLOCKED and
two NOT_RUN: the whole input graph rejected an external absolute path, so its
Compose plugin/render/structure prerequisites remained blocked. No exception,
script alteration or PASS relabel was used. Separately, the coordinator used
existing bounded `port_inventory._run_config` on the public root Compose plus
this optional overlay, explicit `.env.example` and a child environment limited
to PATH/DOCKER_CONFIG/COMPOSE_DISABLE_ENV_FILE. Actual Docker Compose config
exited 0; no actual `.env` or private inputs were read and HOME was not modified.
The coordinator command was `docker compose --project-directory <this worktree>
--env-file <this worktree>/.env.example --profile '*'
-f <this worktree>/docker-compose.yml
-f <this worktree>/infra/07-workflow/n8n/workloads/manifest-outbox-notifier/compose.workflow.override.yml
config --format json`. The resulting public model had 124 services at observation;
this count is not a fixed inventory contract. Only the queue worker gained DEV
and capture memberships, retaining its original management/queue memberships.
Main and both task runners retained their original networks. This is attributed
coordinator STATIC evidence, not a P05 author rerun or native resource action.
Render SHA256 is `2bf962df6569b44e42cdb9f4fde09d45ef36ef5d34d3e819139eb92354453d0a`;
base Compose SHA256 is `2cd210e4e35671fedc1cfd497d23bdf627def6cf35cf852fbba74ca24b958721`;
overlay SHA256 is `7d2280fb5e3e28ab490bb68d8625347f8818659aa063129e8642dcf044d096b9`.

After the last source hardening, the P05 ten-test module passed, exit 0. Final
source staged checks passed, exit 0; metadata selected this Task with zero
violations, lifecycle violations were zero, and all-document links had zero
failures and one existing archive-capture warning, each exit 0. The isolated
production-pruned export also passed with the explicit locked fixture API
`n8n-workflow` version 2.42.3 supplied through NODE_PATH, exit 0. The explicit
Docker builder compiler command was checked against existing locked host
dependencies and exited 0. Neither result proves the selected image runtime or
latest builder. Final receipt-only metadata/lifecycle/staged checks and commit
admission are completed separately after focused review.

### Current P05 Source Binding and Native Preflight — 2026-10-13 KST

The current direct P05 prompt authorizes this bounded source correction,
logical commit, owning-Spec PR and merge after independent review and latest
candidate checks. This supersedes the earlier source-only/no-PR instruction
for this increment; completed work and historical receipts above are preserved.
The acceptance owner remains criterion19/W42-W44 in this Task. No new workflow,
SQL migration, service, secret, image version or scanner rule is introduced.

Fresh `git fetch origin main` exited 0. Initial local HEAD and fetched remote
main both resolve to `603a7637f77df1b5d63c971453853388a39c7df6`, and
`git status --short` was empty. `gh pr list --state open --json
number,title,headRefName,headRefOid,url` returned an empty list, exit 0.
All observed other worktrees were clean and preserved, including the concurrent
P04 `codex/p04-native-acceptance` at the same input SHA. This writer exclusively
owns `codex/p05-current-acceptance` at
`.worktrees/p05-current-acceptance`. Its initially created `/tmp` worktree was
moved here because the patch hook rejects paths outside the project root.
No other writer's worktree, index or shared file was changed.

Compared with the supplied baseline
`23e37362b72e98028a4675f282819c0346ae59dc`, current main already contains
the root-model dedicated capture overlay, its topology regression and Korean
navigation, plus Stage05 document-path moves. Those existing changes are
NO_CHANGE. Initial inspection is a fresh result, not a rerun of historical PASS.

| Surface / consumer | Current classification | Target, owner and rollback |
| --- | --- | --- |
| Builder, inactive workflow JSON, custom node, locked package, image bridge and worker-only DEV/capture overlay | SOURCE_APPLIED / NO_CHANGE | Existing P05 source; no duplicate workflow, dependency or network grant |
| P04 SQL v1 and notifier grants | SOURCE_APPLIED / NO_CHANGE | P04 sole SQL/data owner; consume reviewed source read-only, no migration |
| P05 null SQL binding and tests that required provisional state | CONFIRMED_GAP | P05 alone binds reviewed source; revert this increment's logical commit |
| Root Compose, public environment, versions, OpenBao, backup, Registry and gate contracts | NO_CHANGE | Retain their existing owners and configuration |
| Installed main/worker/runners and discovery/import | RUNTIME_UNVERIFIED | HOME still runs 2.41.6; selected 2.42.7 artifact absent locally |
| Actual DEV publication, roles, queue/SMTP execution, credential mapping and restore | CONSUMER_DEPENDENT | P04 W38, SEC01, P03 and P02/native operator receipts required |
| Current ROOT-image vulnerability scan | RUNTIME_UNVERIFIED | No current image warning established here; no image/scanner changes |
| LAB runtime/data/testing, Wiki implementation and learning applications | OUT_OF_SCOPE | Completed Wiki preparation remains NO_CHANGE; no actions |

#### Reviewed P04 SQL Handoff

Two independent read-only assessments verified that SQL commit
`79dde32059dbf6eae8dacd9f5f2a04aee29f31a5` is contained in this main and
that both files match P04's existing independently reviewed receipt at
[Latest Source Handoff](tsk-0012-p04-airflow-manifest-pipeline.md#latest-source-handoff).
That receipt approves the exact source/security fix range; it does not prove
PostgreSQL execution or native publication. The earlier statements above that
P04 W36 source review is pending are superseded for this source binding only.

| Canonical P04 input | Bound value |
| --- | --- |
| `001_opsflow.sql` migration SHA256 / interface | `57a744cf33581bafd73f610b9c18c83d64c9457486a02e02398df56b444ee584` / v1 |
| `002_checks.sql` source SHA256 | `0a00944569aa05b7a0eec6a555cc3357197b26257ee76a1779c7e258eb9a0b73` |
| `claim_notification()` result | `id bigint, run_id text, source text, row_count integer, lease_token uuid, lease_until timestamptz` |
| `ack_notification(bigint,uuid)` / `retry_notification(bigint,uuid)` | Strict boolean result; same current id/token, no SQL interpolation |
| Consumer projection | Existing five fields; intentionally excludes `lease_until` from SMTP input |
| Notifier capability | DB CONNECT, `ops_flow` USAGE and only claim/ack/retry EXECUTE; no owner, superuser, membership, direct table/column/sequence access |

`binding.sql_sha256` binds the exact `001` migration bytes; both source hashes
remain in `source_reference`. `status=reviewed` means reviewed SQL source only.
`native_execution` and upstream `native_acceptance` stay `NOT_RUN`. The existing
preflight still requires native receipts/exact targets and current operator
authorization even for a complete source binding. No P04 SQL, builder, generated
workflow, node implementation, fixtures, Dockerfile, Compose or secret changed.
W42 source handoff is PASS; transport/role/native portions remain unverified.

#### Fresh Verification and Acceptance Separation

All source commands used the stated input SHA plus this bounded diff. Package
builds use the unchanged lock in the owned worktree, without lifecycle scripts.
The two binding regressions first failed for stale `provisional` and the extra
`reviewed_p04_sql_binding` prerequisite, exit 1; after the minimum contract
correction all 19 P05 tests passed, exit 0. Missing/malformed binding and the
native-authorization refusal cases remain covered.

| Command / observation | Exit / result | Actual scope |
| --- | --- | --- |
| `python3 -m unittest tests.validation.test_n8n_outbox_contract.OutboxContractTests.test_tracked_interface_binds_reviewed_p04_source_without_native_authority tests.validation.test_n8n_outbox_rehearsal.OutboxRehearsalPreflightTests.test_reviewed_source_contract_still_cannot_satisfy_native_prerequisites -v` | 1 / RED, two expected failures | Existing binding defect reproduced before production edit |
| `python3 -m unittest tests.lib.ops.test_n8n_outbox_workflow tests.validation.test_n8n_outbox_contract tests.validation.test_n8n_outbox_rehearsal -v` | 0 / GREEN, 19 tests | SOURCE/UNIT/negative checks; no native rehearsal |
| `python3 infra/07-workflow/n8n/workloads/manifest-outbox-notifier/tools/build_workflow.py --output infra/07-workflow/n8n/workloads/manifest-outbox-notifier/workflows/manifest-outbox-mailpit.json --check` | 0 / PASS | Generated bytes unchanged; one inactive workflow |
| `npm ci --ignore-scripts --no-audit --no-fund` then `npm run test:coverage` in OpsflowSmtp | 0 / PASS, 24 tests | Host compiled-source coverage: line 97.33%, branch 94.83%, function 87.88%; memory-only SMTP |
| `npm audit` and `npm audit --omit=dev` | 0 / PASS, zero findings each | Locked package dependency audit, not selected ROOT-image security acceptance |
| `npm pack --dry-run --ignore-scripts --json` after build | 0 / PASS | Eight package entries include compiled node/transport; no package publication |
| Public root-plus-overlay `docker compose config --format json` with `--profile workflow-n8n --profile mail-dev` | 0 / STATIC PASS | Five selected services; worker-only DEV and internal capture memberships |
| Explicit-socket Docker inspect of four named n8n containers, filtered to name/image/id/state | 0 / metadata observed | Running main/worker 2.41.6, runners 2.41.6; no Env/logs/data inspected |
| `docker image inspect hyhome/n8n:2.42.7-local` in an empty client configuration | 1 / absent | NATIVE_CUSTOM_NODE_DISCOVERY and IMPORT NOT_RUN, not failed execution |
| `git diff --check` | 0 / PASS | Owned source candidate |

The initial host test invocation used `npm ci --bin-links=false`, making
`npm run test:coverage` fail with `tsc: not found`, exit 127. Reinstalling the
same lock with the documented normal local bin links resolved this harness
setup error; no compiler/script pin was changed. The first Compose config
invocation omitted profiles, so extraction failed with `KeyError: n8n` despite
render exit 0. The corrected named profiles above passed. Neither initial
attempt is relabelled PASS.

Compose render used only tracked `.env.example`, explicit root/overlay inputs,
a fresh client directory and a child environment limited to PATH, HOME,
DOCKER_CONFIG and COMPOSE_DISABLE_ENV_FILE. It read no private `.env`; no raw
render was persisted or printed. Only image/network assertions, input hashes
and counts were returned. The pre-move render SHA256 is
`357932b4fe8d1b38f045ea6220d3e2af99c41e2984f90ce0f731ad140888116f`;
root/overlay/public-environment SHA256 are respectively
`82ddbf764c969648345ea99d2866840398e5097fce284e0b60fc40d84d80ebbd`,
`80f11033f1ec282e7967c7a86aec0611ec3eac3f14ba18ec1f222a4a238d1d56` and
`57d67fe51aec15adc50e723dea785039c83524ed3bf6a50f7e6ce80a6308506e`.
Paths embedded in a render affect its hash; it is not an immutable image ID.

Observed main/worker image ID is
`sha256:1de3d197f8b6bad00af0b6945a2ede5ec321c93ab5344bf09b9919311650d492`;
both runners use
`sha256:443eaee69319997627e2129ed8d512c4f4ea2418a744393cf26e843237399299`.
Equal declared image IDs do not prove custom package discovery, execution
placement, peer API compatibility, endpoint/TLS or socket timeout acceptance.

| Acceptance lane | Current result / remaining owner |
| --- | --- |
| SOURCE / UNIT / STATIC | PASS for the scoped correction and existing synthetic tests |
| P04_SQL_HANDOFF | PASS for reviewed v1 source only; P04 W38 is still required |
| NATIVE_CUSTOM_NODE_DISCOVERY / IMPORT | NOT_RUN: selected image absent; SEC01 artifact/security handoff pending |
| ACTUAL_DEV_CLAIM / SMTP_ACCEPT / CAS_ACK | NOT_RUN: genuine P04 publication, native credentials and executor/endpoint receipts pending |
| RETRY / DEAD / LEASE_EXPIRY / duplicate pollers / queue outage | Native NOT_RUN; source and memory transport assertions are not DB concurrency proof |
| RESTART / RESTORE / ISOLATED / HOME / MIGRATION / RECOVERY | NOT_RUN: paired metadata/key backup receipt and approved empty restore target not supplied; existing HOME metadata observation alone is not acceptance |
| ROTATION | NOT_RUN: no exact native credential renewal target or operation selected |
| DELIVERY | Pending this increment's source review, local admission and remote PR checks; runtime delivery remains NOT_RUN |

The next native target must identify the selected SEC01 main/worker/runner
artifacts, P04 `opsflow_dev/ops_flow` publication/role, private native credential
references, executor-only DEV access, `mailpit:1025` capture, DB transport
budget, and independent n8n encryption-key/metadata backup plus an owned empty
restore target. No private value, constant credential, public webhook or
unbounded polling is added. Until these facts are supplied, preserve inactivity.
P04/Airflow owns publication/backfill and does not send this external notification;
P05 remains the sole outbox notification consumer. SMTP acceptance is only
`accepted_by_smtp`; send-before-ack crashes may cause duplicate transmission.

Source rollback reverts only this increment's contract/tests/README/Task diff.
There is no runtime or data mutation to roll back. Future native rollback
deactivates only this workflow, stops its polling, reconciles selected execution
and preserves outbox/accepted/uncertain receipts. Image/source revert cannot
undo DB formats, credential rotation or restore metadata/key consistency.

#### Independent Review and Current Gate Blocker

Independent code and security reviewers approved the exact six-path source
candidate at the stated input with no remaining Critical, Important or Minor
findings. The code reviewer independently reran three binding/preflight tests,
3/3 PASS, exit 0, and checked both SQL blobs against the reviewed ancestor.
The security reviewer verified source-only binding, accurate CONNECT/USAGE/
EXECUTE wording, unchanged dependency and runtime boundaries, and
`git diff --check`, exit 0. These are agent source reviews, not GitHub account
approvals or native/runtime acceptance.

Scoped document metadata selected three changed documents with zero violations,
exit 0. Registered local link checks examined 1,272 documents and 11,441 links:
zero failures and one existing warning concerning 2,870 legacy archive links
without capture sources, exit 0. Host tools were Python 3.12.3, Node 26.10.0
and npm 11.19.1; the Node build is not the selected Docker builder/runtime.
Python Commitizen from the existing `/tmp/hyhome-coord-qa/bin/cz` accepted
`fix(p05): Bind reviewed P04 outbox SQL source`, exit 0. The ambient `cz`
executable was npm's different tool and rejected the check arguments; no
commit-message guard was bypassed.

`python3 scripts/validation/run-ci-gate.py --profile changed --local-only`
exited 1. Candidate preflight, metadata, version projection and local links
passed, but the selected source/fixture suite ran 265 tests in 111.015 seconds
with one failure:
`tests.lib.supply_chain.test_update_gates.UpdateEvidencePackageTests.test_current_root_census_excludes_relocated_lab_history`.
The same single test fails on the preserved clean main at
`603a7637f77df1b5d63c971453853388a39c7df6`, exit 1. A fresh fetch still
returned that remote main. No P05 input is involved in the mismatch.

| SEC01 source-census handoff path | Actual current source SHA256 | Ledger's recorded SHA256 |
| --- | --- | --- |
| `infra/01-gateway/nginx/docker-compose.yml` | `d719e16568e1d898bfc0978c405910e118b3bb58cf7f09dfe6615610546624bb` | `fea2ab70f28d48a36bb0b44a2626e0191c0b8598f26fa047c3bf4a2ab92d4500` |
| `infra/01-gateway/traefik/docker-compose.yml` | `ad9f88fd18c43746e049988a6f4b32475086bfac7d162d9b3ab6a2dd80f13acc` | `c7f4c8efdba12b87728fb68c4c572f2c9b9b812865cd35e485107702388d8141` |
| `infra/04-data/opensearch/docker-compose.yml` | `ba27ea5a56c57885cdcd00f642044d80b7f1d6b6a636974d277261033a993a1d` | `6f23979c299a0af280cbcdab69af8f924ed9fa07ed4b899e28b030cc9eab8bd2` |

The mismatch is in the existing SEC01
`infra/09-platform-ops/security-updates/update-ledger.json` source receipt.
P05 does not modify that common owner, Compose inputs, scanner or test rule to
silence it. The named owner can reconcile current source metadata using the
existing `expected_from_root` helper under its own receipt; no image change or
security acceptance follows from a checksum refresh. The stopped runner's
later selected leaves remain NOT_RUN. Direct adapter invocation rejects an
unadmitted environment and is not used as an alternate gate route.

Read-only remote protection inspection found zero required approving reviews,
no CODEOWNER review requirement and no named required status contexts; the
ruleset list was empty. This does not waive the user's latest-candidate CI
requirement. CODEOWNERS routes the changed infra, Task and tests to
`@buenhyden`. DELIVERY remains BLOCKED for merge until the actual candidate
gate passes. A source-only draft PR may carry this reviewed increment and the
exact upstream blocker; it is not runtime or overall P05 completion.

The first `bash scripts/validation/run-ci-precommit.sh --mode local-staged`
exited 1 solely because Ruff required one line wrap in the new binding test.
After that explicit formatting-only correction, the same six-path staged
controller passed, exit 0, including Markdown, JSON, Python lint/format and
secret detection. The independent code reviewer also approved this result-only
Task delta and separately recomputed the three stale SEC01 source hashes.
The logical commit unit is `fix(p05): Bind reviewed P04 outbox SQL source`;
its exact object and hosted checks are observable through the owning PR.

#### Hosted Candidate Receipt and Latest Main Refresh

The source unit is commit `18dd539765b2b906fc96837e6f9585d2103bae18`.
Its branch push and [PR435](https://github.com/buenhyden/hy-home.docker/pull/435)
creation both exited 0. The first hosted
[candidate run38328314501](https://github.com/buenhyden/hy-home.docker/actions/runs/38328314501)
completed SUCCESS at that exact head against input main603a7637, with
candidate-quality passing in 6m51s. CodeQL actions/Python/JavaScript-TypeScript
and GitGuardian checks also completed SUCCESS. Actual GitHub reviews were
empty and the observed required approving-review count remained zero; the
independent agent reviews above are not account approvals.

During CI, remote main advanced to
`f1d257867ea116c89b76b37394de3ce3a6ed8ff5`. Fresh fetch/diff found only a
P01 result receipt in Task0006. No P05 implementation, P04 SQL, Compose input,
ledger or source dependency changed. Latest main was merged into this branch
without rewriting the reviewed source unit; that commit remains available for
source rollback. The six-path owning-PR source delta remains unchanged except
this result-only Task receipt.

The independent code reviewer reapplied the existing typed execution boundary:
quality policy section4 assigns candidate acceptance to the hosted `changed`
profile and excludes local-only leaves. The clean-main-reproduced SEC01 census
failure remains FAIL/baseline debt under its own owner. It does not create a
new standing P05 merge gate or grant P05 ownership of the shared ledger. This
is not a waiver or a PASS substitution: focused P05 tests, staged admission,
independent source/security review and hosted candidate results are distinct.
The earlier blanket merge-blocked assessment above is superseded for this
bounded source increment once the refreshed candidate passes. Overall/native
P05 acceptance remains open.

PR435 may become ready after evidence-delta review and current-index admission,
then merge only after a fresh hosted candidate SUCCESS for the refreshed head
and latest main. No local aggregate rerun, shared-source correction, image
change, scanner change or native operation is included in this refresh.
Post-refresh head/run/merge identities are observable in this same PR; they
cannot be inferred from the first run's PASS.

#### Bounded Nodemailer security source correction — 2026-10-26

The v30 local-source request authorizes this four-path P05 correction from
HEAD `0d2392f93b975faa36f03b2361d80f3ddb72e487`: the OpsflowSmtp package,
lock, README and this Task. Existing workflow, SQL, node/transport code,
credentials, services and image inputs are unchanged. This is dependency source
preparation; it installs no package into a service and sends no mail.

The preserved pre-change audit at
`/tmp/hyhome-v30-opensearch-root-only-checks/npm-audit-1.json`, SHA256
`c93519e6032f02784bcf5c63cd6e26ace9e6da8736331b097adc54155b8009a1`,
reported Nodemailer 10.1.0 as a direct Moderate finding containing three
address-parser advisories:
[GHSA-8c8m-p3m8-cjg8](https://github.com/advisories/GHSA-8c8m-p3m8-cjg8),
[GHSA-m943-m63m-w62w](https://github.com/advisories/GHSA-m943-m63m-w62w)
and [GHSA-85x2-q946-cp5h](https://github.com/advisories/GHSA-85x2-q946-cp5h).
All affected ranges end before 10.1.4. The existing fixed from/to/envelope
accept no user-supplied address; exploitability in this bounded caller is not
proven. Removing the affected dependency still avoids carrying the parser defect.

The exact 10.1.4 pin uses the
[official 2026-10-18 release](https://github.com/nodemailer/nodemailer/releases/tag/v10.1.4),
which exceeds the seven-day stability window. Latest 10.2.1 was released on
October 22, reaches that window on October 29 and includes broader SMTP changes;
no claim of latest-version completion follows from this security correction.
`npm install --package-lock-only --ignore-scripts --no-audit --no-fund` changed
only the root dependency pin and Nodemailer version/resolved URL/integrity;
all other locked package entries compare equal. Existing createTransport,
sendMail, close, owned-socket, nonpool, envelope and timeout contracts remain.

The exact package and lock SHA256 are respectively
`ddfa26a5890a8fa5af87304920f24d1c8bd87be475a8b1c4650c9c9d4d7d06a5` and
`3f9ca8952964b5e63af3a85a7ecc8fb6b417c940e914c5042239647043c53eb1`.
Checks used Node 24.22.0, the existing Python 3.14.8 environment and private
0600 logs with an empty temporary npm user/global configuration and owned cache.
No dependency lifecycle script, force/fix action, new dependency or override was
introduced. Evidence lives at `/tmp/hyhome-v30-smtp-security-aax_21mz`;
`checks.json`, `registered-checks.json` and `contracts.json` retain actual argv,
UTC start/end, exit and raw-output SHA256 for each command.

| Actual command / check | Exit / result | Bound scope |
| --- | --- | --- |
| `npm ci --ignore-scripts --no-audit --no-fund` | 0 / PASS | Exact lock installation into local ignored node_modules only |
| `npm run test:coverage` | 0 / PASS, 27 tests, zero skipped | Existing offline node/transport and in-memory SMTP tests; production lines 97.38%, branches 95.12%, functions 88.24% |
| `npm audit` and JSON observation | 1 / FAIL | Zero Moderate, three High dependency entries; Nodemailer absent |
| `npm audit --omit=dev` and JSON observation | 0 / PASS, zero findings | Production dependency audit only |
| `npm pack --dry-run --ignore-scripts --json` after README correction | 0 / PASS, eight entries | Compiled artifacts present; no archive publication |
| Existing P05 workflow, source contract and rehearsal-preflight modules plus two fixed-operation adapter tests | 0 / PASS, 22 tests | Source registration and fail-closed native prerequisite contracts |
| Existing `tests.validation.test_smtp_lock_inheritance` whole module | 0 / PASS, ten tests | Synthetic lock inheritance and identity denials |

Full audit remains FAIL through the existing locally development-installed
`n8n-workflow` 2.43.4 → `@n8n/expression-runtime` 0.34.2 → exact Zod 3.25.76
chain for [GHSA-mrhx-c7xc-m3w5](https://github.com/advisories/GHSA-mrhx-c7xc-m3w5).
The three High entries are dependency fanout, not three independent advisories.
That installation classification is specific to this package lock; the packed
artifact excludes node_modules. However, n8n-workflow is also an exact peer
supplied by the n8n host. Host-peer/runtime applicability and exploitability
remain UNKNOWN; the local production audit does not clear the host or runtime.
The npm suggestion to downgrade n8n-workflow to 1.75.1 is incompatible with the
selected native peer contract and is not applied. A Zod major override is also
not applied. An upstream compatible API fix and independent caller/runtime
assessment remain required; the existing security disposition is not extended.

The post-change full-audit JSON SHA256 is
`074e82195fac4d123a56ae84bb6448280c96469d5b9ea1fdd3d1f853b036788e`;
production-audit JSON is
`90c5406b46cbaa8d9447baa7686b930a0dbdd46081460f33682bfc75d9dd4fef`.
Source/unit correction is verified within these inputs. Independent source and
security review, staged admission and the registered final aggregate remain
pending this candidate's coordinator handoff. Native loader discovery, service
installation, actual SMTP/DB execution, HOME, migration, rotation and recovery
remain NOT_RUN for this increment. Earlier failures and historical receipts
above remain unchanged; no source result accepts those lanes.
