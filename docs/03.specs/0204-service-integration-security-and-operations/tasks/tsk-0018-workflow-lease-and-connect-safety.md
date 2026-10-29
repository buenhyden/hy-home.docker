---
title: "Workflow Lease and Database Connect Safety Task"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0018"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-16"
---

# Workflow Lease and Database Connect Safety Task

## Overview

### Objective

Correct the reproduced cross-database CONNECT and stale/ambiguous SMTP claim
boundaries. Existing TSK-0012 and TSK-0013 retain criterion 18 and 19 acceptance;
this Task owns only the bounded corrective work and fresh evidence.

## Inputs and Authorization

The complete 2026-10-16 infrastructure request authorizes these confirmed
source corrections, focused tests, and disposable native restore rehearsals.
The coordinator assigned this writer the isolated worktree
`/tmp/hyhome-infra-spec0204`, branch `feature/spec-0204-workflow-safety`, from
`e6807a7d16d8b9e180ff58456ab64e4ee721ca69`. Other writers own n8n version/package
files and Task0017. This writer owns shared provisioner/monitor CONNECT guards,
reviewed operator-only cluster SQL, workflow SQL004, notifier builder/generated
JSON/transport/contracts/fixtures, affected tests/docs and Plan registration.
Old migrations 001 through 003 and historical Task evidence remain unchanged.
No HOME deployment, live ACL change, credential access, external SMTP or
production restore is authorized by this source unit.

## Work Log

### 현재 source 진행과 lifecycle 구분 — 2026-10-22

공개 소스 대조에서 아래 frozen project.py, monitor.py, SQL004, builder 및 SMTP
transport의 다섯 SHA256이 현재 추적 파일과 각각 일치했다. CONNECT guard,
six-field lease와 unknown quarantine는 구현되어 있으며, isolated PostgreSQL
denial/quarantine/empty restore 결과는 아래 날짜와 입력의 보고로 보존한다.
실제 DEV TimescaleDB, n8n/HOME, S3 또는 complete recovery 수락으로 확대하지 않는다.

현재 frontmatter는 draft다. 아래 Review and Completion의 “In progress”는
기록된 실행 진행을 설명하며 합법적인 lifecycle transition이나 criterion 수락을
대신하지 않는다. 이번 조정은 status를 전이하지 않고 lifecycle 정합성 검토를
남긴다. Criterion 18/19의 decision owner는 기존 Task0012/0013이며, 후속
[Task0019](tsk-0019-n8n-native-notification.md)의 독립 W74 PASS도 두 owner의
수락이나 W65 전체 vertical 완료를 자동으로 만들지 않는다. 새 native 실행이나
전체 복구 수락은 수행하지 않았다.

W72 corrects the shared DEV function-only provision boundary before LOGIN.
A separate administrator-only cluster bootstrap affects PUBLIC CONNECT only on
postgres/template1; unknown consumers block its operational application. Existing
explicit grants require review; monitor receives its own explicit CONNECT.
W73 adds versioned quarantine for ambiguous or expired sends and checks the
server lease deadline with SMTP/ack/skew reserve before opening transport.
Unknown outcomes never enter automatic resend. An operator must reconcile actual
capture evidence before explicitly resolving a quarantined row.

The native baseline used unique labeled p04-pg containers, no network/mounts/ports,
read-only roots, 1 CPU/768 MiB each, at most two simultaneously, 512 MiB data
plus two 16 MiB tmpfs mounts, six-minute fixture and two-minute cleanup budgets.
All owned containers were removed and an independent label query was empty.
The PostgreSQL-only restore is separate from combined S3/n8n/HOME recovery.

### Current source and isolated verification

The cross-database guard RED failed on missing admission logic (exit 1). Its
shared-provisioner implementation and affected existing tests subsequently
passed 45 tests, exit 0. An early revised native run correctly denied login
but the test used a SQL-command ERROR/exit-3 matcher for a startup FATAL/exit-2
result; the assertion now requires actual connection exit 2, the exact database
permission-denial message and false effective CONNECT. It does not weaken the
permission boundary.

The SMTP lease RED rejected the new required server deadline with the old
five-field parser (one test, exit 1). The new six-field guard checks canonical
UTC milliseconds and more than 25 seconds remaining before transport creation
and again before send. SMTP timeout is 15 seconds, ack reserve 5 seconds and
maximum accepted DB/worker clock skew 5 seconds. This is bounded admission,
not continuous fencing or an exactly-once guarantee.

An initial SQL004 native trial failed with 42501 when the test called operator
reconciliation without the existing explicit SET ROLE owner step. The corrected
operator session is opsflow_migrator with SET ROLE opsflow_owner; no broader
runtime/schema grant was added. The changed native quarantine/restore and
admission methods then passed 2 tests in 41.826 seconds, exit 0. The former
verified unknown isolation, stale token rejection, expiry after simulated
capture/lost ack, restricted reconciliation, actual pg_dump/pg_restore into a
second empty owned container and no automatic claim after restore. The latter
verified PUBLIC/direct/inherited admission denial before LOGIN or target DB
creation, idempotent production bootstrap, preserved explicit third-party grant
and explicit monitor postgres-only access. All three owned containers had
cleanup PASS; an independent owner-label query returned no containers, exit 0.

The broader latest native run already passed actual denials for all four login
roles to postgres and template1, target database SELECT success, and the
existing version-2 roles/transactions/empty-restore case. Its one SQL004
operator-session failure is retained above and resolved only by the focused
correction. No native trial exercised real SMTP, n8n queue, HOME or S3.

Final affected source command:
`rtk python3 -m unittest tests.lib.ops.test_opsflow_manifest tests.lib.ops.test_opsflow_adapters tests.lib.ops.test_opsflow_provision_contract tests.validation.test_opsflow_airflow_contract tests.validation.test_opsflow_database_rehearsal.OpsflowDatabaseRehearsalBoundaryTests tests.lib.ops.test_n8n_outbox_workflow tests.validation.test_n8n_outbox_contract tests.validation.test_n8n_outbox_rehearsal tests.validation.test_opsflow_e2e_acceptance tests.validation.test_dev_pg_provision -q`
passed 125 tests in 8.612 seconds, exit 0. Locked node compile and all 27
no-network tests passed; version-worker coverage reported 97.38 percent lines,
95.12 percent branches and 88.24 percent functions. Scoped Ruff lint/format and
git diff --check passed. These are working-candidate receipts, not committed
head or hosted CI acceptance.

Independent review found that pre-existing version-2 retry rows were already
ambiguous, so SQL004 now quarantines all such rows during migration. A real
native regression seeds an immediately due v2 smtp_outcome_unknown retry before
004 and verifies unknown plus no automatic claim. It and the repeated v3
quarantine/expiry/reconciliation/empty-restore case passed 2 tests in 25.459
seconds, exit 0, with all three owned container cleanups PASS. This later SQL
receipt supersedes the prior SQL004 hash only; historical attempts are retained.

### Independent review corrections

Independent review found that the monitor still inherited non-postgres CONNECT
before its automatic LOGIN. A new focused test first failed on the missing
monitor guard (exit 1); the guard now runs before grant or LOGIN and the full
22-case provision module passed. The real monitor test demonstrated NOLOGIN
before cluster review, then successful postgres-only access after the same
production bootstrap.

Review also found that clearing a per-row reconciliation hash on the next claim
would erase the previous attempt's evidence. SQL004 now uses one restricted
notification_reconciliations table keyed by outbox ID and attempt. Resolution
records result/evidence/time atomically with the state transition; runtime
notifier writes are denied and history survives a later claim and independent
restore. This is an owner-controlled audit record, not an immutability promise
against its trusted administrator.

The monitor admission, legacy v2 retry migration and v3 unknown/expiry/operator/
event-history/empty-restore tests passed 3 cases in 42.376 seconds, exit 0.
Four owned containers had cleanup PASS and the independent label query was
empty. These are isolated PostgreSQL 18.6/plpgsql receipts, not the actual DEV
Timescale image, Airflow worker, S3, native n8n, SMTP delivery or HOME acceptance.
The final focused history test further required exact SQLSTATE 42501 for notifier
INSERT/UPDATE/DELETE and retained the first attempt SHA after manual no-send,
new claim and successful ack. It passed once in 17.466 seconds, exit 0; both
exact owned containers had cleanup PASS. The no-send Runbook now additionally requires quiescing every old executor and
in-flight SMTP attempt. Missing capture alone cannot prove no-send; unknown
worker termination or SMTP state leaves operator reconciliation BLOCKED.

The cached Airflow command
`rtk proxy env HYHOME_WORKFLOW_REHEARSAL=1 python3 -m unittest tests.validation.test_workflow_version_bundle.WorkflowCandidateRehearsalTests -v`
passed 2 cases in 30.817 seconds, exit 0, against reviewed immutable index
8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2 and checked
linux/amd64 manifest c9096805e76159e0b18d55a5e357b1958894c291ebf88e9af2a497de208f227e.
Serial disposable containers used 1 CPU/1 GiB, no network, read-only root,
no HOME/secret mounts, pull never and automatic removal. Core/provider imports
and pip check passed; cross-client denial mocked crypto/token exchange and is
not a live authentication result.

The canonical package reader passed all 36 packages after correcting only new
Task/Plan defects: initial status draft, one Work Unit table, unique new W71–73
and exact criterion/Work Unit evidence pairs. Earlier invalid metadata results
and their archive-profile cascade are failures on those earlier inputs; no
historical document or validator was modified to make them pass.

Frozen safety source SHA256 values:

- project.py: accdf1eae4d30b7b4ec1265607154af0dd936705a93418a9d055c06f3caf4fcf
- monitor.py: eddab916bcb694332510f048a209f8c6dab8214ebb235d8530f7243490176bd1
- cluster-connect.sql: ce60bc5343c85659fa40fe3e410bd2b04ddc4f0f0183e4eaac9302c8b48435d7
- SQL004: ad8176d875b75c15d0e7bfc21c1cb67cd5b31240a4901bccec5b8bb0d931bde9
- builder: e1d3d341963c3d1670bda8b694f47c709d1549e1e7608a3f0e89f9825327df44
- SMTP transport: 7b685f776d9d0475aa5cb164b9088218353820524a1d82a8b4b47c99433159f6

The preserved SQL001/002/003 hashes remain respectively
82a4762a8962832c7fdd05826df3b97cf02cc4f96c974a328e42e4493143b18f,
7ed4bfd5f160e93ad810e8d32ce2221a02f1629946e5e4297817385acbbb13ed and
830b62c6e8d175d5a4350bab27976121637df4aeca6688748865756be2d84d72.

### Coupled source commit and current base — 2026-10-16

The coordinator approved one coupled source delivery for W71 (stable n8n
artifact), W72 (DEV CONNECT admission) and W73 (notification safety), together
with their exact tests, binding metadata, Plan and both new Tasks. The stable
custom artifact includes the corrected six-field lease consumer, while its
SQL migration, notifier graph and interface tests must agree. Committing only
partial shared Plan/Task references or stale image-input bindings would create
an invalid intermediate candidate. This source unit does not combine or infer
the separate native n8n/HOME/complete-recovery acceptances.

The explicit approved staging manifest contained exactly 46 paths: 42 tracked
modifications and four new files. It excluded LAB runtime, private inputs,
node_modules and temporary fixtures. The first normal commit attempt exited 1
on four Markdown MD012 double-blank-line findings in Plan/GDE/POL/RUN0053;
JSON/YAML, Ruff, Dockerfile and secret hooks passed. Only those four blank lines
were corrected, explicitly re-staged, and the same normal commit succeeded,
exit 0, with no hook bypass: `34c0319c3e3c512e1d0de2a5a8113648c635ca5d`.

The checkout was clean. Fresh `rtk git fetch origin main` returned
`5a88c7937bf427021f2fd0441e04b1011ecd28a9`; the clean owned branch rebased
without conflict, exit 0. Its actual coupled source commit is now
`8306839bb377228f76881cadaeb1ebe0f14656b5`. W71, W72 and W73 all reference this
same actual source commit; no other worktree was reset, stashed or cleaned.
The post-rebase checkout was clean and no push, PR or merge occurred.

`shutil.which('graphify')` returned no executable, so graph refresh is SKIPPED;
no installation, forced generation or stale graph authority claim is made.
Affected final gates will run once against the final source after the separate
CI policy integration; pre-rebase tests are not relabeled as final-head or
hosted CI evidence. The separate blocked image-native/HOME/recovery lanes
remain visible.

### Owner decision 2026-10-29

On 2026-10-29 the owner decided that the frontmatter `draft` is stale: the Work
Log above already reports the source corrections and isolated verification. The status moves `draft`, `ready`, then
`in-progress`. No criterion is accepted here: criteria 18 and 19 keep their acceptance owners in TSK-0012 and TSK-0013, and HOME and complete recovery stay `NOT_RUN`.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0018 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0018 | ready | in-progress | #owner-decision-2026-10-29 |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Native CONNECT baseline | 18 | W72 | Cross-database runtime denial | e6807a7d; exact cached PG18.6 image; native class, 2 tests/23.880s, exit 1 | FAIL | Work Log | required | - |
| Isolated PostgreSQL restore baseline | 18 | W72 | Roles, schema, reader, outbox, replay and empty restore | Same native class positive method; cleanup PASS | PASS | Work Log | required | - |
| Provision guard RED | 18 | W72 | Reject non-target CONNECT before LOGIN | Focused new test; missing guard; exit 1 | FAIL | Work Log | required | - |
| Stale claim RED | 19 | W73 | Expired claim must not start SMTP | e6807a7d authored TS; no-network injected transport; 601s elapsed; sent once; exit 1 | FAIL | Work Log | required | - |
| Current CONNECT denial GREEN | 18 | W72 | Cross-database runtime denial | Revised native all-four-role postgres/template1 actual connection denials; target SELECT allowed | PASS | Current source and isolated verification | required | Native CONNECT baseline |
| Provision guard GREEN | 18 | W72 | Reject non-target CONNECT before LOGIN | 45 focused tests and native PUBLIC/direct/inherited admission; no target side effects | PASS | Current source and isolated verification | required | Provision guard RED |
| Stale claim GREEN | 19 | W73 | Expired claim must not start SMTP | Closed six-field guard; 27 no-network node tests and coverage PASS | PASS | Current source and isolated verification | required | Stale claim RED |
| Unknown quarantine native | 19 | W73 | Unknown/expired ack isolation, reconciliation and empty restore | Two changed native methods, 41.826s, exit 0; cleanup PASS | PASS | Current source and isolated verification | required | - |
| Source regression suite | 19 | W73 | Affected source/unit/fixture boundary tests | 125 tests, 8.612s, exit 0; actual node coverage separate | PASS | Current source and isolated verification | required | - |
| HOME and complete recovery | 19 | W73 | Real worker/S3/notifier/independent full restore | Exact live inputs, backups and consumer authority unavailable | NOT_RUN | Work Log | optional | - |

## Criterion Acceptance

Criterion 18 retains its durable decision in TSK-0012; criterion 19 retains its
durable decision in TSK-0013. This corrective Task creates no duplicate decision.

## Review and Completion

In progress. Record exact RED/GREEN, native denial/quarantine/restore, static
checks and independent review before delivery. Source rollback reverts only
this logical unit; deployed ACL/schema changes require their own reviewed
backup and recovery boundary. Unknown SMTP results remain quarantined across
restart/restore; no exactly-once or HOME acceptance claim is made.

## Related Documents

- [Plan](../plan.md)
- [P04 acceptance owner](tsk-0012-p04-airflow-manifest-pipeline.md)
- [P05 acceptance owner](tsk-0013-p05-n8n-outbox-notifier.md)
