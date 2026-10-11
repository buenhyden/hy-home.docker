---
title: "P10 Opsflow Acceptance Task"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0016"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P10 Opsflow Acceptance Task

## Objective

Own criterion 21 and W63–W69: acceptance of one bounded Opsflow vertical slice,
from a manifest input through authenticated Airflow publication, DEV transaction
and outbox, reader query, n8n claim, SMTP capture and acknowledgement, followed
by failure handling and an independently bounded restore. This Task prepares the
acceptance contract and evidence ladder before any native or HOME action.

The slice remains independent of the unimplemented Wiki application. It does not
create a Wiki core, client, search resource, collection, workspace, schedule or
blog-data write. Learning applications and LAB runtime services, configuration,
secrets, data, images and execution are excluded. P08 may move typed LAB
documents only into the corresponding Stage05 family `labs/` paths.

## Inputs and Authorization

The direct P10 request authorizes an owning Task, source/test preparation,
logical commits, review and reviewed local-main delivery. The historical analysis
baseline is `860ac1c3633eac9ad416fb1abd8a61a6e617ebd8`; it is context, not a
runtime target. The initial P10 worktree branch is
`codex/p10-opsflow-acceptance` at local HEAD
`43917df47f94f0ddd7e1dbbf7bb7cc87701a56c8`. Fresh `origin/main` and the
actual remote observation are `c26c3b93f4e73034ddad4d08ba9da8eaa9fec0c7`.

Git history was checked for the maximum issued Task number 15 and no issued
Task 16 or P10 ref. The shared root's 24 foreign paths remain preserved; no
secret values were read. Recheck the exact input refs, dirty paths and relevant
owner heads before every implementation unit. Never reset, stash, clean or
stage another worker's changes.

The direct delivery lane is local `main`, without `dev` or a required PR.
The supplied prompt's future PR language does not authorize a remote action in
this lane. A later explicit remote lane must recheck its current ruleset, CI and
independent review at the actual head. No secret value, raw environment file,
credential, production client or external SMTP send is permitted in preparation.

One owner may prepare only this Task, the acceptance test
`tests/validation/test_opsflow_e2e_acceptance.py`, and
`tests/fixtures/opsflow-acceptance/{README.md,manifest.valid.json,cases.json}`.
The fixture README is Korean and describes synthetic input only. A new helper
requires a completed reuse audit and an additional exact lease; it must be pure,
value-free and unable to provision, import, schedule or mutate a runtime.
Write a RED test before the corresponding implementation and retain both
receipts. Shared registration, README/index, manifest, workflow and CI edits are
coordinator proposals until one named writer takes a bounded lease.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0016 | draft | ready | #inputs-and-authorization |

### W63 admission, reuse and source-receipt inventory

Inventory existing P04 publication, P05 notification, P01 issuer/recovery,
P02 catalog, P03 endpoint and P06 migration contracts before adding a test or
fixture. Record each source receipt as SOURCE, UNIT, STATIC, ISOLATED, HOME,
MIGRATION, ROTATION, RECOVERY or DELIVERY rather than promoting a synthetic
result to native acceptance. Existing P04 SQL/DAG/parser, P05 workflow/node,
P01 issuer, P02 catalog, P03 contracts, P06 migration, P07 controls and P08
moves remain owned by their current Tasks.

Current source preparation is permitted while those owners retain operational
acceptance. No global SEC01, P01 or P06 completion gate blocks a scoped,
pre-migration DEV source fixture. An exact image, service identity, endpoint,
role, backup set, operator, recovery boundary and cleanup plan are still needed
before an affected runtime lane starts.

At admission, committed SEC continuation `6f230c56`, SEC integration
`6aff7433`, SMTP `39ff7f91`, and the current P01/P03/P04/P05/P06/P07 heads are
ancestors of local `main` `43917df` and remote `main` `c26c3b93`; P08 `43917df`
is local only. Dirty SEC integration paths and the foreign Task0008 edit in the SMTP worktree
remain uncommitted and preserved. Task-reported historical tests are inputs to this inventory, not
fresh P10 tests; every P10 source, unit and runtime test remains NOT_RUN until
its own receipt is recorded.

### Dated prerequisite snapshot — 2026-10-11

These are public owner-record observations at local main `43917df47`, not fresh
native tests or automatic knowledge of other chats. GitHub observation proves
remote main `c26c3b93f` and no open PR; matching committed ancestry proves source
inclusion, not operational acceptance. P10 consumes committed public inputs only.

- SEC01: continuation branch `codex/sec01-home-continuation` has clean HEAD
  `6f230c56eb97c3cd587d636ba6492b24de13e53d`, included in both observed main
  refs. Its integration checkout is detached at
  `6aff7433c755feacf659f7654a5ad3b9e70f401d` with ten dirty foreign paths.
  Task0009 remains in-progress; the global latest/security ledger and complete
  HOME deployment/recovery are not accepted. Those dirty bytes are not P10
  inputs. A fresh provider lookup may pass the latest-version dimension when
  no newer stable release exists; it cannot substitute for scans, authentication,
  HOME or restoration evidence.
- SMTP01: integration HEAD `39ff7f91562906ae87194693a0e3895f33a8acd3`
  is included in both observed main refs. Only its foreign Task0008 file is
  dirty there. Canonical COMM-002 source wiring is integrated. Task0005 records
  an attributed assignee report of comparison, backup and duplicate unlink;
  its independent operational retirement acceptance remains DEFER/pending.
  The later coordinator-owned two-file isolated restore has an actual exit-0
  SUCCEEDED receipt dated 2026-10-11T00:13:36Z, with outcome SHA256
  `74794448811aa3632b707ec8043e67e84033510d6731cb96a3335717a0690699`.
  This is bounded historical-snapshot restoreability only, not application
  recovery, SMTP authentication/send, HOME activation, production RPO/RTO,
  offsite custody or external-consumer absence. P10 did not rerun that restore.
- CLN01: its source/helper is included in current main, while Task0007 is
  draft and source-bounded. Fresh source/runtime/job/backup-restore/external
  consumer proof, private apply, actual deletion and real recovery remain
  blocked or NOT_RUN. COMM-003 stays held for the SMTP01 executor; cross-executor lock/order
  compatibility remains unresolved and owner-gated; PG-020 remains retained as an initialization/recovery consumer.

P10 neither edits nor stages the shared root's 24 foreign paths, SEC dirty
source/evidence or SMTP Task0008. The owners must deliver current relevant
artifact/connection/backup facts before the dependent P10 runtime lane starts.

### W64 synthetic acceptance preparation

Prepare one value-free manifest and fault cases that model the accepted path:
manifest validation, immutable object identity, DEV transaction/outbox state,
reader visibility, notifier claim, capture acknowledgement, retry/dead state
and independent recovery reconciliation. Tests reject duplicate or conflicting
inputs, unsafe paths, invalid source/date, bounded-size violations, negative
roles, secret-path aliases, plan collisions and premature deletion.

Fixtures must contain no operational credential, actual recipient, real object
data, connection string or operational identifier. Synthetic IDs, hashes and
bounded synthetic bytes may model the existing public contracts. They prove only caller-side acceptance contracts.
They do not provision PostgreSQL roles, a bucket, an Airflow DAG, an n8n import,
an SMTP account or an OpenBao identity.

### W65 isolated vertical slice

After W64 and the selected exact contracts are reviewed, run one isolated
vertical slice in dependency order: P04 native publication first, then P05
native notifier consumption. The selected Airflow image/DAG import, worker
execution, PostgreSQL schema/function privileges, concurrent replay and object
read/validation must use unique synthetic resources. The n8n import, claim,
SMTP capture, acknowledgement and error path must consume the frozen P04
contract rather than recreate it.

An isolated lane requires its exact image digest/version, Compose projection,
DEV role/schema, object prefix/policy, network boundary, credential delivery
reference, resource budget, cleanup and rollback plan. It does not wait for an
unrelated global SEC/P01/P06 completion claim, but it does stop if its selected
owner contract or resource review is missing. Optional native skips remain
NOT_RUN, never PASS.

### W66 selected HOME acceptance

HOME starts only after a named host, selected services, image digest, operator,
approved rollout boundary, backups, resource budget and reversal path are
recorded in the owning Tasks. Verify running image and in-service version,
authenticated readiness, actual worker/reader/notifier behavior and MNG/DEV
separation. Reject wrong issuer/audience, expired identity, direct-backend
access, cross-project A-to-B access and empty key material.

Do not perform a full-stack startup or broad cleanup. Credential rotation
retains its selected feature owner and exact operational boundary. The final
report consumes SEC01 whole-image gates; unrelated global completion is not a
start gate for one admitted isolated consumer. This Task cannot select a HOME
target by inference.

### W67 failure, backup and empty-target restore

Inject faults only into an isolated or named approved scope: object timeout or
wrong credential, validation failure, object-stored/database-unavailable,
replay/backfill, deadlock retry, lost acknowledgement, expired lease and
notifier dead/requeue. Verify actual backup-set completeness for opsflow
database/roles/extension metadata, retained objects, outbox, n8n metadata and
encryption key, OpenBao snapshot and independently held custody material.

Have the owning recovery executor restore one exact snapshot identifier into a
named empty target under its reviewed runtime lease; P10 observes and verifies
the resulting acceptance. P10 may execute a restore only after an exact lease
is transferred. It owns synthetic acceptance fault/reconciliation tests and
collects feature receipts without creating a second restore executor. Reconcile the
reader view/latest pointer, idempotency, outbox lease and capture acceptance
before declaring recovery. P01 and P06 operational migration, authentication,
rotation and recovery lanes remain gated by their owners; this Task does not
invent snapshot custody, a backup set or an image digest.

The complete P10 backup-set, snapshot selection and new empty-target inputs are
currently UNKNOWN. The narrower two-file SMTP snapshot/restore receipt above
is an existing input; it cannot establish the full opsflow recovery set.
Investigate them through the named owner records and read-only inventory before
asking for a new operational action; their absence leaves this runtime lane
NOT_RUN and does not stop W63/W64 source preparation.

### W68 P08 path handoff and dry run

After P08 final path delivery, bind each affected operation document to its
exact old/new path, source and target hash, artifact ID, anchors, README coverage
and generated-owner evidence. Run only the reviewed relative working-directory
dry run or selected command environment. Distinguish a typed LAB document move
from LAB runtime work. If P08 has no final hash handoff, retain this lane as
NOT_RUN.

### W69 final owner report and delivery

At the actual final head, report every owner criterion and the separate SOURCE,
UNIT, STATIC, ISOLATED, HOME, MIGRATION, ROTATION, RECOVERY and DELIVERY result.
Run affected syntax/schema/Registry/link/secret-leak checks, selected unit and
native acceptance, staged gates and independent review. Record exact commands,
input SHA, exit status, failures/corrections, rollback proof and local-main
receipt. Tests do not establish deployment, deletion, migration or recovery
without their actual evidence.

### Dependency Matrix

| Owner | Required handoff before dependent runtime | P10 preparation boundary |
| --- | --- | --- |
| SEC01 / TSK-0009 | Selected image tag/digest/USER/Entrypoint/Cmd, package and security receipt | Whole-image completion stays open; one accepted artifact may admit its bounded lane. |
| SMTP01 / TSK-0005 | Canonical COMM-002 and selected capture/cutover/retirement receipt | COMM-003 execution remains with SMTP01; no private value comparison in preparation. |
| CLN01 / TSK-0007 | Fresh five-axis consumer proof and recovery-aware disposition | No duplicate deletion executor or release of PG-020/COMM-003 holds. |
| P04 / TSK-0012 | Reviewed publication/outbox schema, exact Airflow image and DEV/S3 resource contract | May model the interface; P04 owns publication acceptance; its proof precedes the notifier lane. |
| P05 / TSK-0013 | Frozen P04 version/hash, exact n8n image/node and SMTP capture contract | May model claim/ack faults; native notifier follows P04 publication. |
| P01 / TSK-0006 | Named issuer/recovery target and custody/restore evidence | No issuer or snapshot operation is performed here. |
| P02 / TSK-0010 | Reviewed catalog IDs, classifications and secret-reference contract | No catalog row, identity or destination is invented. |
| P03 / TSK-0011 | Selected endpoint, UID/mode, TLS and network facts | No public endpoint or network is changed. |
| P06 / TSK-0014 | Accepted consumer wave and recovery/rotation evidence | Pre-migration DEV preparation can proceed; copier and deletion remain owner-gated. |
| P07 / SPEC-0218 | Selected capacity/least-privilege baseline where relevant | No resource or permission change is accepted by a fixture. |
| P08 / TSK-0015 | Final path/hash and README coverage handoff | W68 waits; no document move is inferred. |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Task admission | 21 | W63 | Verify Task identity, current refs, ownership and preservation boundary | Local 43917df; remote/origin c26c3b93 | PASS | Inputs and Authorization | accepted |
| Source receipt inventory | 21 | W63 | Enumerate owner receipts and unresolved runtime inputs | Current owner Tasks and source heads | NOT_RUN | W63 admission, reuse and source-receipt inventory | pending |
| Synthetic acceptance preparation | 21 | W64 | RED/GREEN fixtures and isolated contract test | Leased test/fixture paths | NOT_RUN | W64 synthetic acceptance preparation | pending |
| Isolated vertical slice | 21 | W65 | P04 publication then P05 notifier against reviewed exact contracts | Named isolated resources and owner handoffs | NOT_RUN | W65 isolated vertical slice | pending |
| Selected HOME acceptance | 21 | W66 | Selected host rollout and authenticated service evidence | Named host, resources, backups and rollback | NOT_RUN | W66 selected HOME acceptance | pending |
| Fault, backup and restore | 21 | W67 | Fault receipt, complete set and exact empty-target restore | Named fault scope and snapshot custody | NOT_RUN | W67 failure, backup and empty-target restore | pending |
| P08 path handoff | 21 | W68 | Hash-bound path/README handoff and command-directory dry run | P08 final receipt | NOT_RUN | W68 P08 path handoff and dry run | pending |
| Final owner report | 21 | W69 | Exact-head checks, review and local-main delivery evidence | Final candidate and owner receipts | NOT_RUN | W69 final owner report and delivery | pending |

## Review and Completion

This ready Task issues an acceptance boundary only. It has no source test,
runtime, data, secret, migration, deletion, rotation, restore, HOME or delivery
result beyond the Git admission observation. An independent reviewer must inspect
each exact source or operational change without editing it. The Task remains
incomplete until W63–W69 have their actual evidence, while missing runtime facts
leave only their dependent lane NOT_RUN.

Use small logical commits by owning acceptance surface. Preserve existing worker
commits and use one writer for every shared file. Roll back source/test work by
reverting the reviewed logical commit; roll back a runtime lane only through its
pre-recorded target-specific recovery plan. Do not treat this Task issuance or a
synthetic test as a production readiness or restoration receipt.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [P04 Task](tsk-0012-p04-airflow-manifest-pipeline.md)
- [P05 Task](tsk-0013-p05-n8n-outbox-notifier.md)
- [P06 Task](tsk-0014-p06-openbao-consumer-migration.md)
- [P08 Task](tsk-0015-p08-operations-document-layout.md)
