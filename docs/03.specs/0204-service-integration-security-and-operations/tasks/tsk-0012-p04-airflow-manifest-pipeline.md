---
title: "P04 Airflow Independent Manifest Pipeline Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0012"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P04 Airflow Independent Manifest Pipeline Task

## Objective

Own criterion18/W34-W39: implement the independent synthetic manifest
validation/publication batch using the existing DEV PostgreSQL, object storage
and Airflow worker. Freeze the SQL/outbox interface for P05 notification.
This batch is not a Wiki engine, crawler, search system or learning application.
Initial issuance defines ownership and prerequisites; it implements no workload
and changes no database, bucket, credential or runtime.

## Inputs and Authorization

The user's complete P04 prompt and current coordination request authorize
assessment, Task issuance and the independent worker instructions below.
Prompt SHA256 is
`c50695e5a46c2654a95b0286f4183a2f64d9830c3a905cc9d6256282a1e2c11d`;
its historical baseline is `860ac1c3633eac9ad416fb1abd8a61a6e617ebd8`.
Actual clean local main is `74feff9429d302233d2475b31beed3dbf2ac07c9`;
fetch confirms remote main `6da5e3bf380d5002e0e28181136fde8c016e49ce`.
The one local-only commit issues P03. GitHub returned no open PRs and successful
quality checks at remote 6da5e3bf3. These are baseline delivery observations,
not P04 execution or whole SEC01 latest/security/HOME acceptance.

Read bootstrap/provider and SPEC-0204/0212 before source changes. Reuse
completed registration, DEV/MNG, Influx retirement, RedisInsight/exporter,
k6/OTLP, common controls and Stage05 source. Preserve OpenBao PR409/410 TLS,
wrapping/readiness/audit/snapshot implementation. Historical TSK-0001 labels
and completed TSK-0002/0003 are not a new P04 allocation. TSK-0005 remains its
SMTP/history owner. This Task issues no new Spec or P05 Task/criterion ID.

The newer full P04 prompt requests an owning-Spec PR after implementation,
latest-head CI and independent review. Older SEC01/SMTP01/CLN01 keep local-main
delivery without PRs. Dev is unused. Reconcile the local preparation prefix
with fresh remote main before the P04-only PR; do not publish main implicitly.
User authorization is not requested again for already-authorized source work.
Each actual shared/private operation still binds exact target, effects,
consumer, validation and recovery in this Task before execution.

### Independent Worker and Exclusive Files

One writer uses `codex/p04-airflow-manifest-pipeline` in
`/home/hyunyoun/data/hy-home.docker/.worktrees/p04-airflow-manifest-pipeline`,
from this Task's issuance commit after reviewed local-main integration. Record
HEAD, clean status, input file hashes and current remote before implementing.
Creating this worktree does not dispatch an implementation chat. Other writers
are active: preserve their files and never reset, stash, clean or force-push.

After a reuse check, the exclusive new paths are:

- This Task and its evidence/commit ledger.
- `infra/07-workflow/airflow/workloads/README.md`, then the single canonical
  subtree `infra/07-workflow/airflow/workloads/manifest-pipeline/`.
- Within that subtree: Korean `README.md`; `dags/source_manifest_ingest.py`;
  `workflow_lib/__init__.py`, `manifest.py`, `adapters.py`; versioned SQL under
  `sql/` including `001_opsflow.sql` and executable `002_checks.sql`; public
  synthetic `fixtures/`; and optional reviewed `requirements-test.txt`.
- The same subtree's Airflow-only `compose.workflow.override.yml` and optional
  `Dockerfile.airflow`, only if the frozen SEC01 image lacks required packages.
  A workload image extends that exact compatible image; it does not replace
  the core/provider pins or install packages at container startup.
- `tests/lib/ops/test_opsflow_manifest.py`, `test_opsflow_adapters.py` and
  `test_opsflow_provision_contract.py` for narrow contracts, not another
  production provisioner; `tests/validation/test_opsflow_airflow_contract.py`,
  `test_opsflow_database_rehearsal.py` and `test_opsflow_airflow_rehearsal.py`.

Every new folder, including `workloads`, `dags`, `workflow_lib`, `sql` and
`fixtures`, receives Korean README navigation. Add no duplicate source/test
tree from the supplied `reference/` files. Existing parent README changes are
proposals. The P04 workload is the only canonical SQL owner; P05 consumes the
frozen version/hash there and never copies or directly rewrites it.

Existing `infra/04-data/dev-db/pg/provision/project.py` and its tests retain
their current owner/coordinator. Propose a versioned narrow execution-only
extension or adapter that reuses guards and recovery; copying the supplied
standalone provisioner would create a second grant authority. No edit to those
existing files occurs before an exact writer lease and reviewed grant plan.
SEC01 owns Airflow core/Python/providers/constraints and exact-image security.
P03 owns new endpoint contracts; P02 catalog/schema/tools; P01 OpenBao helpers,
subject0085 and its README; SMTP canonical COMM-002/COMM-003 and its executor;
CLN01 consumer/deletion assessment. P04 takes none of those files.

Root/leaf Compose, environment, gateway, Alloy, shared backup, S3 identities/
policies, catalogs/support metadata, service inventory, Registry, shared
validators, manifest/workflow registration, Spec/Plan and existing Stage05/
README indexes remain proposals to their named owner or coordinator. Submit
base blob IDs, exact hunks, tests, consumer effects and rollback in ignored
`.agent-work/integration-proposal/README.md`. Same-file changes are integrated
once after both sides are reviewed. The new override has no n8n changes.

### Parallel Work and Operational Prerequisites

Proceed with W34-W37 public source, RED/GREEN unit/static tests, draft SQL and
outbox contract, and integration proposals. Full SEC01 and P03 completion are
not global start prerequisites. Classify current rows as NO_CHANGE, IMPLEMENT,
VERIFY_RUNTIME, DELETE, BLOCKED_FACTS or OUT_OF_SCOPE; existing recovery and
positive consumers stay retained. P04 deletes no legacy/private material.

Before native execution, bind the relevant SEC01 Airflow image tag and immutable
digest/ID, core/Python/providers/constraints and installed package receipts.
All seven declared Airflow roles must use one compatible image. Reuse the
current constrained build; the supplied reference re-pins core from an unknown
base and cannot be copied unchanged. Required boto3/psycopg/provider versions
follow the frozen image, not conflicting reference test pins. No runtime pip.

P03 supplies selected root-plus-override inputs, explicit public environment,
profiles, dev-pg/object endpoints, TLS/CA, timeout and actual worker identity.
P02 reviews value-free secret references and classification. Before mounts,
verify effective UID/GID, parent ownership, modes, group access and negative
readability. Source default UID50000 differs from observed worker UID1000;
do not assume either is final or use broad chown. Only worker mounts ingest
PG/S3 files; never administrative, reader or P05 notifier credentials. Reject
symlink/parent escape, unsafe owner/link/mode, duplicate JSON keys, unknown
fields, missing values and sensitive errors. No password in argv, environment
exports, XCom, logs, raw render, workflow exports or Git.

Protected worker-only file delivery may support bounded DEV verification before
P01/P06 OpenBao migration. Final Agent delivery awaits their contracts; it does
not block all native tests. Credential operations require a named exact host,
path/identity, effects and recovery; issuance reads or generates no values.
Define worker-only dev_data_net/object_net additions without changing existing
airflow_net/mng_data_net dependencies or metadata. n8n worker/network/manual
offload verification belongs to P05/coordinator. Do not broaden every node.

W38 first uses isolated synthetic resources, then only the selected operational
DEV batch. Record Docker context/project, exact DB/roles/object identity,
budget, migration and backup artifact, owned empty restore target, operational
writer, independent review, identity-bound cleanup and rollback before action.
Relevant image/security and shared resource readiness gate this lane, not an
unrelated global image gate. Do not reuse MNG, production app data or an
occupied restore target. No full-stack up/down, volume prune, shared PGDATA
initialization, broad role revoke, credential rotation or LAB runtime change.

### Canonical SQL, S3 and P05 Interface

Use database `opsflow_dev`, schema `ops_flow`, NOLOGIN owner `opsflow_owner`,
LOGIN `opsflow_ingest`, `opsflow_notifier`, `opsflow_reader`; distinguish a
separately controlled migration capability. Runtime identities receive no
owner/superuser/direct table-write grants. Reader sees only approved views,
ingest only publication, notifier only claim/ack/retry. Existing wider roles,
memberships, ownership or incompatible schema fail closed; do not silently
rotate/reassign/revoke to force success. Default PUBLIC CONNECT and other
database permissions need actual cross-DB negative proof without breaking
other consumers. Reuse safe provision input and lifecycle checks.

Version migrations with checksum, existing ownership/shape/ACL checks and
rollback/restore compatibility. IF NOT EXISTS alone proves neither convergence
nor safe migration. Revoke PUBLIC access, fix SECURITY DEFINER search_path,
qualify objects and parameterize values. Validate invariants through direct
SQL calls as well as Python: types, closed fields, paths including uppercase
secret segments/control characters, source/date/size/hash syntax and duplicate
rows. `002_checks.sql` comments must become executable tests with assertions.

Freeze with independent SQL/security review and P05 consumer review: DB/schema/
roles and migration version/hash; publication signature/results; views;
outbox states and claim/ack/retry signatures; lease UUID/expiry and stale-token
denial; at-least-once semantics; five attempts, ten-minute lease and bounded
retry; SMTP acceptance versus uncertain/actual delivery. P05 must use a stable
run-derived Message-ID and record duplicate uncertainty. Reference defaults
remain draft until that review; no P05 native test runs concurrently with
P04 schema/provisioning. P04 publish/outbox native proof precedes P05 notify.

Same raw bytes/source yield the same run ID. Verify input size at most1MiB,
rows at most5000, the four approved repo/ref pairs, UTC capture day, paths and
strict JSON before publishing. Hash format is not actual Git/content proof;
fixtures are synthetic. Upload original and validated artifacts to bucket
`opsflow-dev`, restricted `manifest-input/` and `manifest-validated/` prefixes;
read back and verify bytes/SHA before one PostgreSQL transaction publishes
runs/docs/current-pointer/outbox. Dedicated S3 policy must prove actual prefix,
cross-bucket, list and Delete denial; broad bucket Write is insufficient proof.
Store no admin identity. Endpoint/region/path-style/CA/timeouts are explicit.

Replay creates no duplicate run or outbox. Concurrent duplicate input is safe;
different manifests with equal source/captured_at are rejected throughout
history, not only against the latest pointer. Backfill never regresses the
current pointer or creates a fresh notification for historical publication.
Define run.status as its recorded publication outcome with current-pointer
authority for latest selection, or explicitly version a different coherent
model. A later publication must not silently reinterpret historical results.
PG and S3 are not atomic: failed DB publication leaves an unpublished reusable
artifact; retry verifies existing bytes before reuse. Orphan disposition uses
published ledger facts and an independently scoped policy. Restore reconciles
objects, pointer and outbox without re-notifying accepted events silently.

Use public airflow.sdk, DAG `source_manifest_ingest`, pool `manifest_ingest`
with one slot, max_active_runs1, explicit timeout/retries, paused and schedule
None initially. DAG parse has zero workload-file/DB/S3 I/O and no Airflow ORM.
One task performs I/O; XCom contains only bounded run/status/count metadata.
Prove actual Celery worker execution with sanitized metadata, never raw logs.

## Work Log

### Assessment Observations and Next Units

Local main and coordinator were clean at74feff942. P01 was clean at6da5e3bf3;
P02 had eight catalog/schema/tool/test/Task changes; P03 was clean at74feff942.
SEC and SMTP retained foreign worktree changes. These are local observations,
not remote implementation or worker self-reported completion. Preserve them.
Remote quality run38102984241 succeeded; no open PRs. No P04 production paths,
opsflow DB/role/bucket or workload execution were verified by this assessment.

Safe container metadata found six running/healthy Airflow roles on3.3.1-keycloak
and identical image ID
`sha256:0388863fe9964d7f2d0d8bacc26dcae0ad5888eadd275c10086a7683bfe46c56`,
USER1000:0. Source selects3.3.2/Python3.13. airflow-init was absent: the scoped
inspect exited1 despite returning the other nine containers. Actual dev-pg
reported18.6-ts2.30.2-pgbackrest2.57-r2, Seaweed S3 reported4.47 versus source4.48,
and n8n worker2.41.6-local. Health proves neither policies nor batch readiness.
OpenBao source2.7.1 versus observed2.6.2 remains P01/SEC ownership.

1. W34: baseline/consumer/reuse map, RED tests and exact file ledger. Compare
   all supplied reference files; use only adapted single canonical source.
2. W35: parser/adapters/idempotency and privacy RED/GREEN, then refactor with
   meaningful coverage at least80percent. Include immutable input behavior,
   rejected duplicate fields/rows, bounds/date/source/traversal, no import I/O,
   protected-file failures and S3 timeout/wrong-key/readback corruption.
3. W36: versioned migration/provisioning proposal, direct SQL invariants,
   restricted roles and draft outbox; independently review and freeze P05 hash.
4. W37: exact-image DAG import and Airflow-only overlay model. Coordinator
   integrates common hunks and QA registration at a reviewed commit SHA.
5. W38: native migration, worker S3-to-DEV publication, reader/outbox checks,
   replay/concurrency/backfill, DB unreachable/failure after object, scoped S3
   denials and role/cross-DB denials. Test separate empty restoration and
   retry reconciliation; record resource cleanup and compatible rollback.
6. W39: freeze logical source/test/docs commits and common proposal hashes;
   rerun affected registered changed/staged checks, independent code/security/
   SQL/IaC/docs review and latest-head CI before the owning-Spec PR merge.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Git and owner baseline | 1, 18 | W34 | status/worktree/fetch/open PR inspection | Local74feff942; remote6da5e3bf3 | PASS | Assessment above; no remote write or P04 runtime | pending |
| Existing source reuse | 1, 8, 18 | W34 | Focused existing DEV/workflow/registration unittest | Clean74feff942 | PASS | 35 tests, 9.529s, exit0; command below | pending |
| Supplied reference audit | 18 | W34 | Extracted public reference UNIT only | Prompt c50695e5a46c; isolated Python3.12.3 | PASS | 42 tests, 0.19s, exit0; ignored receipt only | pending |
| New manifest implementation | 18 | W35 | RED/GREEN parser and adapters | Issuance commit pending | NOT_RUN | Worker implementation pending | pending |
| New SQL contract | 18 | W36 | Versioned migration and outbox | Issuance commit pending | NOT_RUN | Worker implementation pending | pending |
| New DAG contract | 18 | W37 | Zero-I/O import and compatible overlay | Issuance commit pending | NOT_RUN | Worker implementation pending | pending |
| Native batch and recovery | 18 | W38 | ISOLATED/HOME/MIGRATION/RECOVERY | No selected ready execution contract | NOT_RUN | No DB/role/bucket creation or deployment | pending |
| Rotation | 18 | W38 | Credential rotation | No rotation required | NOT_APPLICABLE | No rotation authorized by issuance | not-required |
| Delivery | 8, 18 | W39 | Latest-head CI/review/PR/merge | No P04 PR | NOT_RUN | Issuance is local documentation only | pending |

Existing-source command, exit0:

```sh
/tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.validation.test_dev_pg_provision \
  tests.validation.test_dev_data_boundary \
  tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests \
  tests.validation.test_project_registration -q
```

Reference audit extracted17 public files only under ignored
`.agent-work/p04-reference-audit/reference/`. Shared QA Python lacked pytest
(exit1); system venv creation lacked ensurepip (exit1). A separate uv-created
`/tmp/hy-home-p04-reference-qa.970sdfx3` Python3.12.3 environment installed only
pytest9.0.2, then PYTHONPATH selected that reference directory with automatic
pytest plugins disabled. Its `python -m pytest <reference>/tests -q` passed42.
No shared tool environment was modified. Airflow/boto3/psycopg native execution,
full reference dependency installation, image build, SQL migration and Docker
rehearsal were not performed. Passing references are not a deployable workload.

Issuance validation initially found one Evidence row containing multiple Work
Unit IDs; that column requires a single issued unit. The metadata check exited1
and package-inference fallout reported unchanged archive documents. Split only
the new row into W35/W36/W37; no archive or validator was changed. Two staged
style attempts exited2 on a duplicate Plan blank line; the gate restores edits
on failure, so the coordinator explicitly corrected that line and the next
staged run passed. The first link invocation omitted required mode (exit2);
`--mode all` passed1192 documents/11571 links, zero failures and one pre-existing
historical-capture warning (exit0). Record the final metadata/review receipts
against the corrected files before committing.

Worker commands must bind actual HEAD/blobs and explicit public input paths.
After implementation, run the named opsflow unit and validation modules,
affected existing modules above, DAG import in the reviewed image, SQL checks
through the four intended role boundaries, and opt-in native rehearsal with
recorded exact target/cleanup. Record RED failure, GREEN exit, meaningful
coverage, skipped classes, failure corrections and each resource receipt.
Coordinator registers gates in existing manifest/workflow before final
`scripts/qa.py changed` and
`scripts/validation/run-ci-precommit.sh --mode local-staged`; proposal-only
registration is not a PASS. Run document metadata/links and git diff --check.
Keep SOURCE / UNIT / STATIC / ISOLATED / HOME / MIGRATION / ROTATION /
RECOVERY / DELIVERY separate; unit results do not satisfy native acceptance.

## Review and Completion

Issuance is draft. The worker records in-progress when implementation starts.
Criterion18 requires the real native batch, restricted identities, failure and
empty-restore proof; source-only PR delivery does not complete this Task.
The broader existing P04/P05 workflow criterion remains pending until P05
notification acceptance as well. Do not infer its completion from P04 outbox.

Commit by W34/W35 validation, W36 SQL/provisioning contract, W37 DAG/overlay,
then W38 evidence and W39 docs/gates; keep coupled migrations together. Review
shared proposals before the coordinator's integration commit, then retest the
final combined head. Preserve owning-Spec P04 commits in one PR with current
required CI and independent reviews; changed head invalidates affected reviews
and checks. Record PR URL, head/merge SHA and actual delivery separately. Do not
delete dirty or undelivered branches/worktrees; preserve ignored evidence first.

Rollback pauses only this DAG and selected workload, keeps accepted outbox
receipts, and uses reviewed compatible migration/empty-restore procedures.
Source revert does not reverse runtime/schema state. No MNG reset, shared
volume deletion or whole-stack restart is a rollback.

Hand P05 the exact SQL version/hash/function/view/lease/retry/state contract,
publication fixture, role/reference names and native acceptance receipts.
Hand P02 secret classifications/references, P03 endpoints/UID/networks and
denial evidence, SEC01 workload package/image findings, P01/P06 future isolated
renderer contract, P07 measured resource facts, P08 final paths and P10 replay/
failure/recovery tests. Each names final source SHA, schema version, proposal
base blobs, actual versus NOT_RUN evidence and next exact command/inputs.
Wiki preparation remains P09; no app, raw source collection, production OIDC,
search/embedding/model, Wiki schedule, blog-data write, external workspace,
learning-app planning or LAB runtime action is included.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Current reconciliation](../../0212-request-baseline-and-reconciliation/spec.md)
- [SEC01 image and security owner](tsk-0009-sec01-stable-security-integration.md)
- [P01 OpenBao continuation](tsk-0006-openbao-trust-bootstrap-and-recovery.md)
- [P02 catalog](tsk-0010-p02-secret-catalog-and-views.md)
- [P03 integration contracts](tsk-0011-p03-service-integration-contracts.md)
- [Airflow guide](../../../05.operations/guides/0050-airflow.md)
- [Airflow source](../../../../infra/07-workflow/airflow/README.md)
- [DEV database source](../../../../infra/04-data/dev-db/README.md)
- [SeaweedFS source](../../../../infra/04-data/seaweedfs/README.md)
