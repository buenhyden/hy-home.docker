---
title: "P04 Airflow Independent Manifest Pipeline Task"
version: "0.1.24"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0012"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P04 Airflow Independent Manifest Pipeline Task

## Overview

### Objective

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

### 현재 후속 증거 인계 — 2026-10-22

현재 소스에는 manifest/adapters/TLS, manual paused DAG와 versioned SQL이
구현되어 있다. 아래 2026-10-13–14 CONNECT FAIL은 당시 입력의 결과로 보존한다.
후속 [Task0018](tsk-0018-workflow-lease-and-connect-safety.md)은 별도 isolated
PostgreSQL에서 CONNECT denial과 quarantine/empty restore 성공을 보고한다.
[Task0020](tsk-0020-airflow-native-publication.md)은 generation-1 실제 Celery
publication, controlled retry와 replay PASS를 보고하지만 generation-2는
UNVERIFIED이고 recovery는 NOT_RUN/BLOCKED이다.

이 후속 결과는 각 frozen 입력과 isolated 대상의 supporting evidence다. 실제
TimescaleDB, HOME, TLS/권한/consumer 및 전체 복구 수락이나 P05와 같은 data를
통한 W65 vertical PASS로 확대하지 않는다. Criterion 18은 pending을 유지하며,
과거 Evidence/실패와 source-only delivery 기록은 그대로 보존한다. 이번 공개
소스 대조는 native 실행이나 새 수락을 수행하지 않았다.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0012 | draft | ready | #worker-start-and-ownership |
| SPEC-0204-TSK-0012 | ready | in-progress | #worker-start-and-ownership |

### Worker Start and Ownership

The user dispatched W34-W37 on 2026-10-11 in the issued dedicated worktree.
Actual HEAD and local main were `4e26a5a8022a7307c7461af60337442912955df1`,
with a clean index/tree; remote main remained
`6da5e3bf380d5002e0e28181136fde8c016e49ce`. The issuance's earlier local
`74feff942` is preserved above as assessment history, not the worker start SHA.
The user subsequently confirmed that SEC01's final workload image and P03's
endpoint/worker identity contracts are unconfirmed. Native DAG import and W38
publication, private delivery, migration and recovery remain NOT_RUN. P01/P06
are not global source-start prerequisites.

Exclusive writer split inside this P04 worktree: the manifest worker owns
`workflow_lib/manifest.py`, its initializer and `test_opsflow_manifest.py`;
the adapter worker owns `workflow_lib/adapters.py` and its unit tests; the
single SQL worker owns both versioned SQL files and the provision-contract
tests. The controller owns this Task, DAG/overlay, validation tests, all new
folder READMEs, synthetic fixtures and ignored integration proposals. Other
sessions' files are read-only. None of these assignments grants native or
private execution; request/token/time ceilings and provider enforcement are
UNKNOWN. Independent reviewers do not edit the implementation.

The existing generic DEV provisioner grants runtime direct DML/default table
privileges and reader access to all tables. P04 cannot execute that default
against this function-only workload. Its narrow execution-only extension,
additional notifier role and ACL recovery remain proposals to the current
owner; no second production grant generator is introduced. Shared Plan output
from the execution-plan procedure remains a proposed hunk because the current
user reserves the Plan to the coordinator.

| Criterion/work | Exclusive files | Witnessed check or next gate |
| --- | --- | --- |
| 18/W35 parser | `workflow_lib/manifest.py`, manifest unit module | Strict bounds/JSON/source/date/path/immutability and object-before-DB RED/GREEN |
| 18/W35 adapters | `workflow_lib/adapters.py`, adapter unit module | Protected inode/parent/type/owner/JSON, explicit connections and redacted dependency failures |
| 18/W36 publication | `sql/001_opsflow.sql`, `sql/002_checks.sql`, provision-contract unit | Version/shape/ACL preflight, executable direct SQL guards; native execution NOT_RUN |
| 18/W37 DAG/overlay | `dags/source_manifest_ingest.py`, `compose.workflow.override.yml`, Airflow contract module | Synthetic SDK parse-no-I/O and worker-only merge; exact-image import NOT_RUN |
| 18/W38 | Future exact DEV/isolated target receipt | Fixed relevant image/endpoint/identity, grants, object policy, backup and empty restore review |

| Item | Classification | Current effect |
| --- | --- | --- |
| Existing Airflow metadata, DEV/MNG infrastructure and provisioner | NO_CHANGE | Existing source reused; no current operational action |
| New canonical parser, adapters, SQL and manual DAG source | IMPLEMENT | Dedicated P04 source and synthetic tests only |
| Exact-image import, identity/endpoint/role/S3 behavior and empty restoration | VERIFY_RUNTIME | NOT_RUN while contracts are unconfirmed |
| Shared QA/Registry/provisioner/S3 policy integration | BLOCKED_FACTS | Exact proposals await the named owner's integration |
| Wiki implementation, learning apps, LAB runtime, private material deletion | OUT_OF_SCOPE | No new work or deletion in this lane |

At the issuance HEAD, before creating the DAG or overlay,
`python3 -m unittest tests.validation.test_opsflow_airflow_contract -v`
exited 1 with three missing-implementation errors. After the minimal source,
the command exited 0 with three PASS. Extended task/private-output cases then
passed five tests, exit 0. This uses a synthetic SDK and proves no native
Airflow/Celery execution. Public API basis is the official
[Task SDK reference](https://airflow.apache.org/docs/task-sdk/stable/api.html);
the version-specific public-interface page was unavailable. Exact compatible
SDK acceptance belongs to the future fixed-image import.

### Intermediate Source Gates

On a later read, local main advanced to
`f7543e0697e2473cbbbeb254792e7a1d5b4b8423` while origin/main and an actual
`git ls-remote origin refs/heads/main` returned this Task's issuance
`4e26a5a8022a7307c7461af60337442912955df1`. This worker kept its original
HEAD and edits; no merge/rebase or reset was performed during concurrent writing.
The earlier remote 6da5e3bf3 observation remains historical.

The latest formatted DAG/overlay SDK-double tests passed five, exit0. Scoped
Ruff initially exited1 for timezone alias/import ordering; scoped fixes and
formatting were applied, followed by a fresh five-test PASS. The current
existing-source baseline command with system Python passed35, exit0, 10.389s;
this is a fresh run at worker HEAD4e26a5a with only P04 new files, distinct from
the issuance's earlier35PASS and the separate reference42PASS.

Independent IaC review approved the W37 source/static contract against frozen
file hashes, and rendered the public synthetic root+override model. Its native
image, selected P03 inputs and recovery verdict remain blocked/NOT_RUN.
The registered infrastructure static helper exited2: 11PASS, zeroFAIL,
fourBLOCKED for an existing external absolute path and dependent Compose
checks, twoNOT_RUN for runtime/secrets. Its tracked-index snapshot did not
yet include new unstaged P04 paths; this result is not P04 model acceptance.
No guard was weakened and no daemon operation ran.

The explicit seven-document changed metadata check at HEAD4e26a5a exited1
with five findings for only `workflow_lib/README.md`: Registry's lowercase
hyphen-only subpath matcher does not register that required Python package
folder. The proposed exact additional_path in the existing package-readme
profile is held in ignored `registry-readme.patch`; the shared Registry stays
untouched. Actual metadata acceptance awaits coordinator integration. Patch
applicability for that hunk and the README/QA-registration hunks passed, exit0.

Historical W37 source state at worker HEAD4e26a5a, before the current TLS unit:
Independent security review found that a CA pathname alone did not protect
against changed/symlinked trust roots at driver open. The adapter's revised
source fails before driver import/client/connect for HTTPS or verify-full
with `tls_delivery_not_ready`; closed TLS field schemas describe a future
delivery contract, not supported execution. Synthetic regressions witnessed
the missing guard (RED), then the fixed denial (GREEN). Internal protected-file
connections still require W38 endpoint/network authorization. TLS delivery,
actual identity readability, native role/policy and recovery remain NOT_RUN.

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

### Source Validation Receipt

The Python source unit was committed locally as
`944cf2ec1af877d39f9f5e788bc84e13a9b08189` after independent code and security
approval. This is not remote delivery. No push, PR, deployment, migration,
credential read/generation/rotation, data deletion or recovery has run.
Relevant current source SHA256 values are:

| Input | SHA256 |
| --- | --- |
| `workflow_lib/manifest.py` | ef19e0093b990c6b8400b29f234877e9d6f346a38440f3a181c37aa5cd744b60 |
| `workflow_lib/adapters.py` | 2bba454121d52d04716d55d9adb8986374b9324a7f6259ba83b6ad15de707af3 |
| `test_opsflow_manifest.py` | 73ca024a75fe2f9b5b48c5907c60d2df2b77f5df7f6f74e1d51636e1d5502087 |
| `test_opsflow_adapters.py` | f3b0dc8a310038bb9653eaa76e88dac0af264758414fcb72ba6e04a958f07766 |
| `dags/source_manifest_ingest.py` | d3e7a67ef8af1b438c79626de24f850834b83fb49475d3fe5cf6a205ea55844e |
| `test_opsflow_airflow_contract.py` | 8668255471a029c0c3d66cf796ce9c77d99ca792ece907e9e898f875f23dc354 |
| `compose.workflow.override.yml` | c024c16e0ccecd4ae30df3792063b4d416dce76335925af4b484883dc4ed6a15 |

Commands ran from the exclusive worktree. At the issuance HEAD plus the
listed source files, `python3 -m unittest tests.lib.ops.test_opsflow_manifest
tests.lib.ops.test_opsflow_adapters tests.validation.test_opsflow_airflow_contract
-q` passed43, exit0, 0.900s. A later fresh DAG-only run at944cf2ec1 passed5,
exit0, 0.011s. Only the SDK and external drivers are doubles; the adapter tests
import the real parser. Public fixture parsing with the real parser returned
`synthetic_fixture_valid=True`, exit0, at944cf2ec1. No private input was used.

Branch coverage used `/tmp/hy-home-p09-qa/bin/python -m coverage run --branch
--data-file=/tmp/p04-root-source.coverage
--source=infra/07-workflow/airflow/workloads/manifest-pipeline/workflow_lib,infra/07-workflow/airflow/workloads/manifest-pipeline/dags
-m unittest` with those three modules, followed by coverage JSON/report.
The run passed43, exit0: parser157/157 lines and66/66 branches, adapter293/297
lines and102/104 branches, DAG17/17 lines with no branches. This measured
source before the final test-only constant refactor; production hashes match.
The final combined-head receipt must rerun it, not reuse these percentages as
evidence for changed implementation.

Scoped Ruff check/format and `git diff --check` passed, exit0. Registered
`bash scripts/validation/run-ci-precommit.sh --mode local-staged` passed,
exit0, first for the Python unit and then the DAG/overlay/docs/fixtures index.
Nonapplicable language hooks reported SKIP; they are not native tests.
The first Python commit attempt exited1 because the ECC secret scanner
matched two public synthetic `password=` literals. Their identical values
were moved to named synthetic constants; assertions and production behavior
were retained. No hook, credential or policy was changed or bypassed.
The revised43-test run, staged gate and normal commit succeeded.

Independent code review ran the original frozen three modules separately:
43PASS, exit0, 0.317s, then reviewed the test-only constant refactor. Security
review approved the production hashes and post-refactor adapter test hash;
its own execution was blocked by the sandbox launch failure, so it relies on
the separately identified controller receipt. These verdicts exclude SQL,
native dependencies and overall Task completion.

Independent IaC review rendered the actual root plus this override with
Docker Compose5.6.0, `.env.example`, workflow/workflow-airflow profiles,
an intentionally nonresolvable synthetic immutable image reference and absent
synthetic code/secret directory paths. Raw model JSON streamed directly to an
allowlist projection; no private env file or daemon action was used. Exit0
confirmed seven identical images, build reset, pull never, five code mounts,
worker-only secret/DEV/object additions and preserved base commands, user,
dependencies, MNG/Airflow networks and mounts. Root SHA256 was
`d04187b004e6e41f73e5b61befee2505ad2f8ec78e83e3f200a6032fe354b5f6`,
Airflow leaf `9358f1c648314d147f0f3b532b240e378e1c80bbd68dd003a40babd68f268997`,
public env `2464faf7798e52d07a8eb49a4d9e3330d78723174f462b27722365ee182aba15`.
This model PASS does not bind the still-unconfirmed P03 selected model.

All-document links passed1193 documents/11582 links, exit0, with one existing
historical-capture warning and no failures. Actual Registry metadata failed
for only the required `workflow_lib/README.md` path. Seven-document validation
against the ignored exact-path Registry candidate passed, exit0, zero findings.
Actual shared Registry acceptance and registered changed QA remain pending;
the candidate PASS does not replace them. The existing static helper receipt
above remains BLOCKED, not a successful whole-stack Compose check.

After tracking the overlay, the fresh seven-document metadata runs at
`b2a46bc88` both exited1: actual Registry158 findings, ignored Registry
candidate153. The Task's extra hash table inside Evidence made registered
evidence noncontiguous and caused package/archive/lifecycle inference fallout;
the receipt was moved into Work Log. Those unrelated archive files were not
edited. A separate current source incompatibility remains: authored runtime
image discovery rejects `${OPSFLOW_AIRFLOW_IMAGE:?}` as an ambiguous image,
despite successful Compose parsing/render of the required selected input.
The exact diagnostic `_runtime_compose_entry` call exited1 with that public
source error. Earlier candidate metadata PASS preceded tracking this overlay
and is not acceptance of the current source. Shared validator adaptation or a
reviewed resolved-image projection is now another coordinator prerequisite;
do not insert an old image default, bypass the guard or claim latest-image
acceptance to clear it.

### Exclusive File and Shared Interface Ledger

Intermediate source receipt at `b2a46bc88` plus the earlier SQL inputs below:
the same coverage command with data file `/tmp/p04-root-source-final.coverage`
also included `tests.lib.ops.test_opsflow_provision_contract`. It passed50,
exit0, 2.972s. JSON output `/tmp/p04-root-source-final-coverage.json` confirmed
parser157/157 lines,66/66 branches; adapter293/297 lines,102/104 branches;
DAG17/17 lines, no branches. Parser protocol ellipses use the tool's default
exclusion; no custom exclusion or coverage suppression was added. SQL source
guards added seven tests but are neither SQL branch coverage nor PostgreSQL proof.

| Frozen SQL input | SHA256 |
| --- | --- |
| `sql/001_opsflow.sql` | 5dff64c03d5494db6ef73daec445b5edc0aa5262abe89d691c8aaefc22acbb30 |
| `sql/002_checks.sql` | 2b82f35bfef98b93da06a96a09480ced41b6974547d275b365e994f244322ffe |
| `test_opsflow_provision_contract.py` | 704e444732fdd3cccbe62258abcb4e9226556ff23d0f73652330066950ab4747 |

SQL initial source tests failed3 with missing files, exit1, then passed3.
Two privilege/fingerprint regressions later failed, exit1, before their fixes.
Final independent review found relation-ambiguous constraint signatures and
uncaptured existing/custom types; each new regression first failed1, exit1,
then the corrected seven-test suite passed, exit0, 0.002s. Both fingerprints
now bind constraints to relation/domain/name and include type metadata;
preflight rejects preexisting `ops_flow` types. Ruff initially rejected import
ordering, exit1; explicit scoped fix/format and final check/format passed.
Security re-review approved these exact SQL hashes for a local source commit;
PostgreSQL behavior and the complete standalone catalog inventory remain
NOT_RUN. A privileged owner/audit/provisioner stays a controlled trust boundary.

`claim_notification()` now returns six fields including `lease_until`.
The SQL README holds the single P05 draft signature/state/retry contract;
P05 must review version1 and the recorded001 hash before consuming it. No P05
file was written, and native P05 acceptance is NOT_RUN. UTC partition, original
JSON duplicate keys/repo/ref/size and content authenticity belong to the
parser/raw-object boundary, not the six SQL publication arguments.

The exact `runtime-required-image.patch` proposal keeps concrete/default pin
checks, rejects partial/optional substitutions and preserves authored source
link requirements. Only an entire `${NAME:?}` image is classified as an
unresolved required input, never as an accepted image pin. Its isolated source
copy regression ran6 PASS, exit0, while explicitly asserting the actual
validator remains RED. Shared heading.py base blob is
`8627bae903f8d71e246a36af404e090c1320300c`. The proposal is not applied to the
shared validator and requires existing-suite registration and final combined
head checks by its owner. `git apply --check` passed for all five hunks; the
first hand-written runtime hunk had a line-count error, exit128, corrected
before the isolated test. Actual metadata acceptance remains pending.

All source additions are below `infra/07-workflow/airflow/workloads/`:
family README; workload README and override; DAG plus its README; library
initializer/parser/adapters plus README; SQL001/002 plus README; fixture README,
manifest and the two connection examples. Dedicated added tests are
`tests/lib/ops/test_opsflow_manifest.py`, `test_opsflow_adapters.py`,
`test_opsflow_provision_contract.py` and
`tests/validation/test_opsflow_airflow_contract.py`. The only modified existing
tracked file is this Task. No tracked/private file is deleted.

Shared conflict candidates remain read-only: root/leaf Compose and environment,
Airflow version/dependencies, existing DEV provisioner, Seaweed identity/policy
renderer, Registry, workflow/QA registration, shared backup, Spec/Plan and the
parent Airflow README. Five exact hunks and base blob IDs are in ignored
`.agent-work/integration-proposal/`; this is an integration artifact, not a
second progress authority. The Registry hunk adds only one exact README path.
The generic existing provisioner and action-only S3 renderer cannot yet realize
the function-only/prefix-only contracts; their current owners must implement
and review the narrow extensions before W38.

SEC01 final platform/digest/core/Python/SDK/provider and installed boto3/psycopg
receipt are UNKNOWN. P03 selected inputs, effective UID/GID, endpoint/TLS and
network acceptance are UNKNOWN. P02 protected references, function-only
provisioning, isolated audit identity, S3 identity policy enforcement, pool1,
backup artifact, empty restore target and resource cleanup budget are pending.
No private host target has been selected. Token/time/shared-budget ceilings
and provider-enforced limits remain UNKNOWN. Knowledge is valid only for the
recorded source hashes; changed shared/image contracts invalidate affected
checks and require a fresh receipt.

SQL source review also found a deterministic retry-budget assertion defect;
it was corrected in the source before freeze. The native check script's row
ROLLBACK does not undo PostgreSQL identity sequence advancement. Execute it
only on a separately approved disposable isolated DB, with a separately
reviewed superuser audit session for role switching; runtime roles keep zero
memberships. It is neither a pristine empty-target restoration nor an
operational recovery receipt. Actual role switching and sequence effects are
NOT_RUN here, not inferred from source guards.

W37 native DAG import and all W38 ISOLATED/HOME/MIGRATION/RECOVERY are NOT_RUN.
ROTATION is not required; no rotation occurred. SOURCE/UNIT/STATIC local
evidence does not promote any of those categories to PASS. DELIVERY records
local logical commits only; remote head CI/PR/merge await coordinated prefix
reconciliation and final integration. Rollback currently reverts only owned
source hunks. It does not reverse schema/state; future native rollback pauses
this DAG, preserves accepted receipts and restores only the reviewed isolated
or DEV workload target without MNG reset, volume deletion or global restart.

### Latest Source Handoff

The user's latest reply leaves SEC01 and P03 execution contracts unconfirmed.
Continue source and synthetic work; actual image import, private delivery,
native DEV publication and restoration remain NOT_RUN. There is no selected
private host, credential path, DB or restore target. Earlier reviews and test
receipts above apply only to their explicitly recorded inputs.

The final SQL candidate supersedes the preceding seven-test generation:

| Latest SQL input | SHA256 |
| --- | --- |
| `sql/001_opsflow.sql` | 57a744cf33581bafd73f610b9c18c83d64c9457486a02e02398df56b444ee584 |
| `sql/002_checks.sql` | 0a00944569aa05b7a0eec6a555cc3357197b26257ee76a1779c7e258eb9a0b73 |
| `test_opsflow_provision_contract.py` | bb95d0cf1ab0f10cbc4a45f4cbb63f472c7660f277451823efdce67001e32423 |

Independent review additionally found public types outside the empty-target
guard and missing sequence configuration in the fingerprint. Two separated
regressions first failed2/9, exit1; after correction all9 passed, exit0.
Both SQL scripts now reject public types and fingerprint sequence type/start/
increment/bounds/cache/cycle. Runtime sequence position remains excluded.
Security re-review approved these exact001/002 hashes without remaining
Critical/High/Medium findings. Source checks do not execute PostgreSQL or prove
global catalog inventory, cross-DB grants, concurrent leases or restoration.
Independent SQL fix-range re-review approved the same001/002 and test hashes,
ran9/9 source tests, exit0, 0.003s, and verified hashes remained stable.

At input HEAD `b2a46bc886bdad787c077994d0eca41d1a32dcd9` plus the three latest
SQL inputs, the fresh combined command below passed52, exit0, 2.723s:

```sh
/tmp/hy-home-p09-qa/bin/python -m coverage run --branch \
  --data-file=/tmp/p04-root-source-final.coverage \
  --source=infra/07-workflow/airflow/workloads/manifest-pipeline/workflow_lib,infra/07-workflow/airflow/workloads/manifest-pipeline/dags \
  -m unittest tests.lib.ops.test_opsflow_manifest \
  tests.lib.ops.test_opsflow_adapters \
  tests.lib.ops.test_opsflow_provision_contract \
  tests.validation.test_opsflow_airflow_contract -q
/tmp/hy-home-p09-qa/bin/python -m coverage json \
  --data-file=/tmp/p04-root-source-final.coverage \
  -o /tmp/p04-root-source-final-coverage.json
```

JSON generation exited0. Parser branch coverage is66/66 (100%); adapter102/104
(98.08%); DAG17/17 lines with no branches. Default protocol ellipsis exclusion
is unchanged. Nine SQL source guards are not SQL execution coverage.
The exact four-file SQL index passed the registered local-staged gate, exit0,
and `git diff --cached --check`, exit0. The fresh all-document link check passed
1199 documents/11609 links, exit0, zero failures and one existing historical
capture warning. Nonapplicable staged hooks reported SKIP.

After moving the receipt outside Evidence, the actual seven-document metadata
check still failed11, exit1: six runtime-image discovery findings and five
unregistered README/profile findings. Task/lifecycle/archive inference fallout
is resolved without editing historical documents. The ignored proposal process
with the exact Registry path addition and required-image adaptation passed7
selected documents with zero violations, exit0. This is PROPOSAL_ONLY; actual
shared validation remains FAIL until coordinated integration and fresh checks.

While other sessions advanced shared refs, `git ls-remote origin refs/heads/main`
returned `da2c84ce5b92a2a594002050c9b3e70fa795451e`, exit0. A subsequent local
observation saw main and origin/main at `4a14baa1aaeec72c7a7e9f95f62c293a788d7ff0`.
These are separate observations, not a claim of a stable synchronized head.
This worktree did not fetch, merge, rebase, push or write main; its test inputs
remain the recorded P04 head and file hashes. Reconcile the current owning-Spec
prefix and proposal base blobs before any coordinated final integration or PR.

Exact additions, relative to issuance SHA
`4e26a5a8022a7307c7461af60337442912955df1`, are:

```text
infra/07-workflow/airflow/workloads/README.md
infra/07-workflow/airflow/workloads/manifest-pipeline/README.md
infra/07-workflow/airflow/workloads/manifest-pipeline/compose.workflow.override.yml
infra/07-workflow/airflow/workloads/manifest-pipeline/dags/README.md
infra/07-workflow/airflow/workloads/manifest-pipeline/dags/source_manifest_ingest.py
infra/07-workflow/airflow/workloads/manifest-pipeline/workflow_lib/README.md
infra/07-workflow/airflow/workloads/manifest-pipeline/workflow_lib/__init__.py
infra/07-workflow/airflow/workloads/manifest-pipeline/workflow_lib/manifest.py
infra/07-workflow/airflow/workloads/manifest-pipeline/workflow_lib/adapters.py
infra/07-workflow/airflow/workloads/manifest-pipeline/sql/README.md
infra/07-workflow/airflow/workloads/manifest-pipeline/sql/001_opsflow.sql
infra/07-workflow/airflow/workloads/manifest-pipeline/sql/002_checks.sql
infra/07-workflow/airflow/workloads/manifest-pipeline/fixtures/README.md
infra/07-workflow/airflow/workloads/manifest-pipeline/fixtures/2026-10-10.json
infra/07-workflow/airflow/workloads/manifest-pipeline/fixtures/pg-connection.example.json
infra/07-workflow/airflow/workloads/manifest-pipeline/fixtures/s3-connection.example.json
tests/lib/ops/test_opsflow_manifest.py
tests/lib/ops/test_opsflow_adapters.py
tests/lib/ops/test_opsflow_provision_contract.py
tests/validation/test_opsflow_airflow_contract.py
```

The only existing file modified is this Task. Ignored proposal files are local
handoff artifacts, excluded from the tracked source inventory. No deletion,
Dockerfile, workload dependency pin or second provisioner was introduced.

Next source verification is the same52-test command against the reconciled
combined head, followed by registered changed QA, metadata, links and reviews.
W37 needs the fixed SEC01 platform/digest/installed-package receipt and actual
SDK import; the current double cannot supply it. W38 still requires a reviewed
native harness and exact disposable/DEV identity, migration, S3 prefix policy,
backup and empty-restoration contract. Protected service-file references must
be bound by the operator before the following templates become executable:

```sh
psql --dbname='service=opsflow-p04-migrator' -X -v ON_ERROR_STOP=1 \
  -v migration_sha256=57a744cf33581bafd73f610b9c18c83d64c9457486a02e02398df56b444ee584 \
  -c 'SET ROLE opsflow_owner' \
  -f infra/07-workflow/airflow/workloads/manifest-pipeline/sql/001_opsflow.sql
psql --dbname='service=opsflow-p04-isolated-audit' -X -v ON_ERROR_STOP=1 \
  -v migration_sha256=57a744cf33581bafd73f610b9c18c83d64c9457486a02e02398df56b444ee584 \
  -f infra/07-workflow/airflow/workloads/manifest-pipeline/sql/002_checks.sql
```

Both templates are NOT_RUN and refer to proposed service names, not existing
credentials or accepted operational targets. Run002 only on the reviewed
disposable isolated database. It does not test backup/empty restore, cross-DB
isolation or real S3 publication. TLS CA delivery is fail-closed in the source;
its accepted implementation requires the P03 protected-delivery contract.

### Local Commit and Delivery Ledger

| Logical unit | Local commit |
| --- | --- |
| Strict parser and protected adapters | 944cf2ec1af877d39f9f5e788bc84e13a9b08189 |
| Paused DAG, overlay, navigation and synthetic fixtures | b2a46bc886bdad787c077994d0eca41d1a32dcd9 |
| Guarded publication and leased outbox SQL | 79dde32059dbf6eae8dacd9f5f2a04aee29f31a5 |

All three normal Conventional Commits succeeded, exit0, without hook bypass.
This Task's final documentation commit is identified by Git history rather
than embedding a circular self-hash. The ignored integration folder contains
a template-based `p04-pr-draft.md`; it is local preparation, not an open PR.
The branch-specific GitHub PR query returned an empty list, exit0. No P04 push,
PR, merge or remote CI result exists. Source rollback is limited to these
owned commits; no private/runtime state requires reversal because none changed.

### Coordinator source integration — 2026-10-11

Actual base is remote `8bef97d915495d4adb8dddd1801724db8065783e`.
Merge `24bdda3d99d292d773ee122f890af793016e8d25` preserves all four worker
commits through `5864c0501`; no source file was dropped or overwritten.
Common metadata/Registry repair is `085d9bf79`; P01 consumer registration is
`329754101`. P04 common registration is
`59a091705a7e72cc3584b71c4ae013870b76fac5`, preserving P02/P03 routes.
The coordinator reran52 source tests (exit0); default metadata selected7
owned documents, violations0. Three common README inputs selected1 governed
README, violations0. Historical11 metadata failures remain above.
Seven affected registered leaves have segmented success, not full aggregate
exit0: baseline596/71 opt-in skips, CI-contract, workflow39, control-plane,
workflow validator, manifest and repository-integrity407. First baseline
failed two checkout0775 modes; exact0755 correction changed no file bytes.
First workflow38 failed the old selector list; strict42-module expectation
and explicit workload-routing regression passed39 without relaxing skips.
Source/common/test independent reviews and staged checks passed. Exact argv,
input hashes, logs and failures are retained in the coordinator's ignored
`.agent-work/p04-combined-acceptance.json`; coverage was not rerun.
Local source integration does not closeW38/criterion18. PR/remote CI, native
image import, DEV publication, HOME, migration and empty restore remain NOT_RUN.

### Optional overlay source classification repair — 2026-10-11

The current integration input is main
`4c83f14b11a77e13e582eb85d0bf256685472a95`. The twenty worker source files
listed above and all four logical worker commits through `5864c0501` remain
preserved after coordinator merge `24bdda3d99d292d773ee122f890af793016e8d25`
and subsequent common registration. The earlier pasted Task version0.1.0 is
a stale handoff snapshot; the coordinated Task was already version0.1.1.
This continuation preserves its identity, created date, lifecycle and recorded
worker/coordinator history rather than replacing it with that snapshot.

At the main input, the coordinator's official operations catalog check failed
with exit code1 and 22 findings in 16.593 seconds: one include drift, seven missing
profile declarations, seven Guide bindings and seven inventory membership
entries for `compose.workflow.override.yml`. The receipt and public output are
`.agent-work/p07-baseline-operations-catalog.json` and `.log` in the isolated
P07 admission worktree. This SOURCE/STATIC failure concerns classification of
existing Airflow service overrides; it is not seven new services and is not
a native deployment failure. Historical segmented gate successes above stay
bound to their earlier inputs and do not replace this later FAIL.

The coordinator is repairing the shared classification under POL-0078 using
an explicit `x-hyhome-overlay` marker: integer version 1, safe tracked regular
non-overlay base already included by root, nonempty services limited to that
base, no root include of the overlay, no independent top-level declarations
and no service profile override. Root plus overlay explicitly selected with
ordered `-f` inputs inherits base profiles and uses existing Guide/inventory
rows. Malformed markers fail closed; filenames grant no exemption.

The valid typed-overlay regression first failed against the unchanged main
helper, exit1, with `compose-include-drift` and
`compose-service-profile-missing`. The actual RED command was:

```sh
env PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.lib.document_governance.test_operations_catalog.ComposeProfileVocabularyTests.test_typed_overlay_is_not_a_root_include_or_profile_authority -v
```

The QA executor subsequently reported final focused profile/inventory tests
59 PASS, exit0, 5.893 seconds, and the full operations catalog test module
102 PASS, exit0, 321.691 seconds under branch coverage. The module's combined
line/branch coverage with branch measurement enabled was 88%: 1204 statements,
132 missed statements, 522 branches and 68 partial branches. Branch-only
coverage was 444/522, or 85.06%. Newly added helper lines820–963 had no missed
lines. The full102 run used the final classifier but earlier test hash
`72022f451617c6eebd5ac60bdbf2f03d87d3188a0e033cbc1944705b665deec1`.
Only null/empty-base table inputs were added afterward; no production source
changed. Final focused59 used the final test hash below. The combined coverage
binds that unchanged classifier across full102 and final59. Final candidate
hashes were independently rechecked by the documentation writer:

| Final classification input | SHA256 |
| --- | --- |
| `scripts/lib/document_governance/operations_catalog.py` | 864a8304cf5b3d9e17d7a7d56065e426a8d46c4378ae94742f89a611a191605e |
| `tests/lib/document_governance/test_operations_catalog.py` | b426f723612bd9ed89a339752da775cd351723426682355229342121af2f79dd |
| `compose.workflow.override.yml` | 8314933a0d088b4c2610002ee6330eb2d50373698cd16bad0654957f3203a35f |

The full module ran first, then the final focused command appended coverage
for additional refusal cases; the coverage export is
`.agent-work/p04-overlay-coverage.json`. RED is retained in
`.agent-work/p04-overlay-red.json`. Exact QA GREEN commands were:

```sh
env PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python -m coverage run \
  --branch --data-file=/tmp/p04-overlay-catalog.coverage \
  --source=scripts.lib.document_governance.operations_catalog \
  -m unittest tests.lib.document_governance.test_operations_catalog -q
env PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python -m coverage run \
  --append --branch --data-file=/tmp/p04-overlay-catalog.coverage \
  --source=scripts.lib.document_governance.operations_catalog -m unittest \
  tests.lib.document_governance.test_operations_catalog.ComposeProfileVocabularyTests \
  tests.lib.document_governance.test_operations_catalog.ServiceInventoryTests -q
```

QA reported official catalog PASS, exit0, 16.690 seconds, on the final
classifier/overlay input; only additional test cases changed afterward.
The actual argv was the command below. That QA invocation captured tool
output, not a stdout log file; the coordinator's older
`.agent-work/p04-overlay-catalog.log` is not a final-input receipt.

```sh
env PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python scripts/validation/check-operations-catalog.py
```

The earlier candidate classifier `963f14e3acc95f0179ef22b6b70a8413303bdbdfed3bd66f7ae2450e3b3598f7`
also had a coordinator catalog PASS, with duration not measured. That is
superseded candidate evidence, distinct from both the unchanged-main 22 FAIL
and the final classifier result. Earlier focused59/3.043-second evidence is
likewise historical; the final focused result is59/5.893 seconds.

The coordinator reran the four P04 dedicated modules, 52 PASS, exit0, 0.344
seconds, using the exact command below. Public argv/result and source
preservation facts are in `.agent-work/p04-overlay-integration-receipt.json`;
the public output is `.agent-work/p04-overlay-opsflow-tests.log`.

```sh
/tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.lib.ops.test_opsflow_manifest tests.lib.ops.test_opsflow_adapters \
  tests.lib.ops.test_opsflow_provision_contract \
  tests.validation.test_opsflow_airflow_contract -q
```

QA reported scoped Ruff and diff-check PASS. Current-head document, staged
checks and independent review/delivery receipts remain pending. This is a
SOURCE/UNIT/STATIC candidate, not fresh full-pipeline acceptance, exact-image
import, dependency, DB/S3 grant or native readiness. No private file, DEV
resource, HOME deployment, migration, rotation or recovery action occurred.

The subsequent registered staged gate failed, exit1, because Ruff-format
found formatting differences in the classifier and its tests after refactoring.
The coordinator applied only the registered Ruff formatter to those two files.
`.agent-work/p04-final-format-preservation.json` proves AST equality against
the preceding classifier/test inputs; the overlay and runtime model did not
change. The formatted source hashes are:

| Formatted classification input | SHA256 |
| --- | --- |
| `scripts/lib/document_governance/operations_catalog.py` | 0dbccf87d4775774db3689fdeae600f7a978fff1079a6c9f5cba665d66a7fc2d |
| `tests/lib/document_governance/test_operations_catalog.py` | b92337f5f5968cac6b7d724b57529ded1b007c5679f324294194127c670a4852 |

The coordinator then reran the exact focused command below on these formatted
inputs: 59 PASS, exit0, 3.298 seconds. Public output is
`.agent-work/p04-final-formatted-focused.log`. The exact catalog command below
also passed, exit0, with output in `.agent-work/p04-final-formatted-catalog.log`;
its duration was not measured separately.

```sh
env PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.lib.document_governance.test_operations_catalog.ComposeProfileVocabularyTests \
  tests.lib.document_governance.test_operations_catalog.ServiceInventoryTests -q
env PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python scripts/validation/check-operations-catalog.py
```

The full102 run and coverage above remain historical receipts for the
pre-format classifier; neither was rerun after formatting. The prior
three-document metadata check passed, exit0, selected3/violations0, with this
Task at SHA256 `401569033ff545870ceec99a2de79cd70d074ecde110aa0e7c06c59c7cfd9c1b`.
POL-0078 and the workload README remain unchanged. The coordinator's link
check also passed, exit0, 1205 documents/11659 links, zero failures and one
existing warning, in `.agent-work/p04-final-links.log`; that result predates
this factual amendment. Task-only metadata and the next staged/delivery result
must bind the amended document. No full aggregate or native PASS is claimed.

Current coordination uses logical local-main integration without dev, PR or
remote push. A later separately adopted remote lane still requires exact
owning-Spec/current-head checks and independent review. W38 and criterion18
remain open; only the relevant accepted image and exact resource/recovery
contract can enable the native batch and P05's subsequent notification proof.

### Required-image-input projection repair — 2026-10-11

The first overlay classification unit was committed as
`f1a7726c4a77220d7dddc5f0b027b7fedcfe879d`. The subsequent registered local
changed gate failed, exit1, when `sync-tech-stack-versions.sh --check` rejected
the typed overlay's `${OPSFLOW_AIRFLOW_IMAGE:?}` image declaration. The public
failure is retained in `.agent-work/p04-registered-local-changed.log`. Earlier
classification, formatting and test receipts remain bound to their inputs;
this later aggregate FAIL was not replaced by a component PASS.

The second source unit reuses the central overlay classifier and derives
`required_image_inputs` in the existing version registry. It records required
variables without reading environment/private values, resolving an image or
treating an unresolved declaration as a pin. Every concrete image pin stays
in the existing registry; no parallel inventory or image authority is added.

QA witnessed RED for the valid `${REQUIRED_IMAGE:?}` typed-overlay fixture,
exit1, before the script change. The old script reported invalid Compose
declaration for the synthetic `infra/example/compose.workflow.override.yml`.
The exact RED command was:

```sh
env PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.validation.test_tech_stack_version_contract.TechStackSynchronizationTests.test_typed_overlay_projects_required_image_input_without_resolving_it -v
```

QA then reported six focused refusal/projection tests PASS, exit0, 14.880
seconds, followed by all 33 TechStackSynchronizationTests PASS, exit0, 34.712
seconds. The latter's public output is `/tmp/p04-tech-stack-required-input-unit.log`.
The final class command was:

```sh
env PYTHONDONTWRITEBYTECODE=1 /tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.validation.test_tech_stack_version_contract.TechStackSynchronizationTests -v
```

The frozen script SHA256 is
`d2c0014be61f0b46dbf2154294c042de36958817fb2f64d436ae0308cdbfae46`;
the test SHA256 is
`50779bf5356088e62b73de2dd13fb1aaa2e08d3526de9b3db8009ba410b6641c`.
QA reported scoped Ruff check/format, `bash -n` and diff-check exit0. New
coverage for this inline shell/Python projection is NOT_MEASURED; the earlier
classification module coverage does not measure this source unit.

With QA tools on PATH and `PYTHONDONTWRITEBYTECODE=1`, the coordinator executed
`bash scripts/operations/sync-tech-stack-versions.sh --write`, exit0. The
public `.agent-work/p04-required-input-projection.json` records registry change
from `9ca1dfbf0b257ad5a136d0cbc31fccae72d8f65558ec744ad76eb3251c579b04`
to `8b95290672195e0bc61796adeb4fc33eb87ad73cc0a65d2921bcd82d3e5dea67`.
JSON equality proved all 88 concrete entries and every other pre-existing field
unchanged. Exactly one overlay source record names `OPSFLOW_AIRFLOW_IMAGE`;
its status is unresolved-not-pin. The subsequent `--check` passed, exit0,
reporting 91 repositories/72 external/19 local-custom/one required input in
`.agent-work/p04-required-input-check.log`. These are observed projection
counts, not a fixed service census or accepted runtime image.

The coordinator's script manifest check passed, exit0, and the command below
passed 63 tests, exit0, 39.055 seconds. Public outputs are
`.agent-work/p04-required-input-manifest.log` and
`.agent-work/p04-required-input-regressions.log`.

```sh
/tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.validation.test_tech_stack_version_contract \
  tests.validation.test_validator_entrypoints -q
```

Independent review of the four-file source unit accepted it without Critical
or Important findings. Final combined registered changed/staged checks and
local-main merge remain pending. The latest direct user local-main lane
overrides the older PR expectation for this integration receipt only; remote
push, a new P04 PR and hosted CI remain NOT_RUN. Source projection does not
accept SEC01's image, installed dependencies or grants. Criterion18/W38,
native image import, DEV execution, HOME, migration, rotation and recovery
remain open or NOT_RUN under their exact resource/image/restore contracts.

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

Earlier combined P04/P05 synthetic checks passed196 in19.313s, exit0; P06/P07
checks separately passed62 in16.592s, exit0. P04 safe-path repair preserved the
candidate767 actual gate failure: RED2/exit1, GREEN4/5.438s/exit0 and broader64/
38.558s/exit0, without weakening PYTHONSAFEPATH. These are separate input-bound
receipts, not native image/SQL acceptance. No new coverage measurement is claimed.

Completed prefix receipts include metadata148 tests/555.270s, document-governance
666/734.010s, active metadata509/0 findings and candidate metadata24/0. The first
suffix included supply263/88.823s and all67 declared Compose selections (329
total), plus364/84/18 contract tests; its596-test baseline failed only the two
checkout modes before their correction. Final suffix passed workflow39/7.349s,
control59/26.571s, precommit wrapper, workflow5/7/8 declarations, Storybook,
release18/0.023s and final repository494/127.874s. Native criterion18/W38,
ISOLATED/HOME/MIGRATION/ROTATION/RECOVERY and remote delivery remain open or
NOT_RUN as previously recorded; segmented source checks do not close this Task.

### Function-only Provision Source Completion — 2026-10-12

Baseline `241a470d246191751a7a5655a86d5ec4f679a0ff` now has a closed
schema-v2 source contract for the five fixed Opsflow identities. The existing
schema-v1 platform manifest and its generated SQL remain byte-identical; the
generated v1 SQL SHA256 is
`6c5a395271102d1db425900562bbcb9651df0f36cf409ff8f3d1ca303acc3b6f`.
The tracked `opsflow.json` contains no credential name or value. Its null
binding is valid only for structural validation and cannot generate SQL or
reach secret reads. P02 catalog binding therefore remains an explicit input,
not an invented catalog identifier.

The v2 SQL creates only `opsflow_owner`, `opsflow_migrator`,
`opsflow_ingest`, `opsflow_notifier` and `opsflow_reader`. It grants database
CONNECT, runtime schema USAGE and the non-inheriting migrator-to-owner
membership needed by the reviewed migration. It grants no table, sequence or
default object access. Existing role/member drift is checked before role
creation. Existing DB, public objects and owner, schema and default ACL drift
are checked before LOGIN/password, connection-limit or owner-membership
changes. An existing unmarked database is rejected pending a separately
reviewed recovery input; an empty shape alone is not accepted as creation
provenance. Public `pg_class`, `pg_proc` and `pg_type` objects are part of that
fail-closed check.

The initial test-first input produced four expected errors: schema v2 was not
supported and `opsflow.json` did not exist. The first completed candidate
passed 28 focused tests, then independent code and security reviews both found
the same two Important ordering/recovery defects. Two focused correction tests
reproduced one failure and one error before the fix. The corrected input passes
29 focused tests, with branch coverage 81% for `project.py`. Ruff lint and
format checks plus `git diff --check` pass. Actual CLI validation exits 0 with
`project manifest structurally valid; credential bindings pending`; ordinary
execution of that unbound fixture exits 64 before any secret read or SQL. The
security and code-quality re-reviews approve the correction with no remaining
Critical or Important finding.

Frozen pre-document hashes are `55138bf6d3bf6aa9eed3e047d3f8a9af5814cdf46cf16eaedceab146f6f02512`
for `project.py`, `df4a32efe1c0acf14f822781b910825da05eec63b510911c67ae049fd00a1754`
for `opsflow.json`, `19bd902277bc0b07c6cf0ff4d30bce2c7a891acc0eb56bce1d96e277fe878d11`
for the provision validation test and
`432783cacc22c7cda0be677859ce8d45d33209c2305bca8f7bfed28aaf0a7368`
for the SQL/provision bridge test. PostgreSQL, Docker, credentials, DEV/HOME,
migration, rotation, backup and recovery were not accessed or changed.
Criterion 18/W38 and the Task remain in-progress pending the bound credential
contract, native function-only privilege proof, approved image and empty
restore target.

The first ordinary commit attempt exited 1 because the ECC hook treated the
public psql variable name in the `ALTER ROLE ... PASSWORD` template as a
generic credential assignment. No value was present and no bypass was used.
Splitting the SQL keyword from the psql placeholder with normal Python string
concatenation preserves the generated v1 bytes and v2 quoting while allowing
the same hook to inspect the staged source without that false positive.

### Native acceptance reassessment — 2026-10-13

This reassessment binds the Task to dedicated-worktree HEAD
`603a7637f77df1b5d63c971453853388a39c7df6`. `git fetch origin main` exited 0;
the observed remote/main and worktree baseline resolved to that SHA. The
worktree was clean at assessment, and the branch-specific GitHub open-PR query
was empty. These observations do not replace prior historical receipts or
prove remote delivery.

The source comparison is limited to the P04 workload, its DEV provision
contract, and its four registered test modules. Relative to
`23e37362b72e98028a4675f282819c0346ae59dc`, that selected source diff is
empty. The repository-wide comparison contains 393 changed paths outside this
Task's ownership; they were not inspected, modified, reset, stashed, or
attributed to P04.

| Assessment item | Classification | Receipt and next boundary |
| --- | --- | --- |
| Existing Airflow manifest DAG, workflow library, SQL and provision source | NO_CHANGE | Selected P04 source diff is empty; preserve the existing implementation. |
| Existing source/unit/static tests | SOURCE_APPLIED | The four P04 modules passed 53 tests, exit 0, in 0.354 seconds. Existing DEV/provision/registration coverage passed 43 tests, exit 0, in 11.624 seconds. These results do not prove a native worker, S3, PostgreSQL, or restore lane. |
| Same-date publication conflict | CONFIRMED_GAP | Current source permits distinct `p_time` values for the same source and UTC business date to publish. A versioned migration must correct this while preserving schema v1 and P05's six-argument function signature. |
| P03 worker identity, DEV PostgreSQL/S3 target and protected service files | CONSUMER_DEPENDENT | The requested target identifiers and protected path references are not bound. Do not read values or invent a credential, bucket, role, network, or cleanup target. |
| SEC01 Airflow 3.3.2 image/provider constraints | RUNTIME_UNVERIFIED | Cached candidate `sha256:8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2` is linux/amd64 with Python 3.13.15 and has a SEC01 bounded isolated-bundle receipt. Signature, SBOM, scan, advisory applicability, and HOME approval remain NOT_RUN. HOME runs 3.3.1; do not change the root image or scanner without an actual current-image security warning. |
| HOME, migration, rotation and empty restore | RUNTIME_UNVERIFIED | No selected HOME target, role grant boundary, object prefix policy, backup input, or empty restore target exists. Rotation remains NOT_APPLICABLE because no credential change is authorized. |
| Isolated PostgreSQL and Airflow-import preparation | PLANNED | The user selected isolated native validation plus HOME rollout preparation, not rollout. PostgreSQL uses cached linux/amd64 image `sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873`, unique `p04-native-<UUID>` ownership, `--network none`, tmpfs `/var/lib/postgresql`, no host ports, mounts, shared volumes, or credentials. A separate owned restore container must use `pg_dump`/`pg_restore`, not schema reconstruction. The future Airflow import uses `--network none`, read-only source code and no opsflow secret mounts. Neither candidate image is approved for HOME deployment. |
| Cross-database `PUBLIC CONNECT` review finding | CONFIRMED_GAP | The SQL review found a cross-database `PUBLIC CONNECT` gap. Native role testing must expose and retain that failure; no grant revocation or assertion change may manufacture a PASS. |

W34 assessment is complete only as the source/reuse classification above. W36
must add the smallest compatible versioned migration for the date-conflict
defect and its RED/GREEN regression. W38 then requires the selected disposable
PostgreSQL trial covering migration, role denial, idempotency, concurrency, and
an empty `pg_dump`/`pg_restore` restore; W39 requires current-head
source/security review, registered changed/staged gates, and the owning-Spec
delivery path. Neither planned work nor a passing source test is a native
acceptance result.

The initial document-check probes used obsolete names
`check-doc-metadata.py` and `check-doc-links.py`, each exiting 2 because those
entrypoints do not exist. The correct registered commands are
`python3 scripts/validation/check-document-metadata.py` and
`python3 scripts/validation/check-document-links.py`. The corrected metadata
command passed for the earlier 55-line amendment at `603a7637`, selecting one
document with zero violations. A later run against this 98-line amendment was
interrupted during repository-wide lifecycle traversal (exit 130), so it is
not a PASS and must be rerun after source integration. Link validation also
remains pending against the final input. The final validation sequence includes
`git diff --check`,
`python3 scripts/validation/run-ci-gate.py --profile changed --local-only`,
and `bash scripts/validation/run-ci-precommit.sh --mode local-staged`, each on
the reconciled owning-Spec head. No result is recorded before it is run.

HOME execution remains NOT_RUN while the operator selects exact target facts:
Docker context/Compose project, approved Airflow image digest, P03 worker
UID:GID, protected PG/S3 path references, opsflow DEV bucket identity, and an
empty restore target. Those facts must exclude values, private `.env` files,
raw logs, and personal data. Source rollback is a logical revert of the owning
P04 migration/source commit; it does not reverse a later database migration,
object write, credential change, or restore action.

#### HOME rollout preparation receipt

The selected preparation target is Docker's default context with Compose project
`hy-home-infra` and root configuration at the repository's absolute main path.
Six Airflow roles currently run 3.3.1 on image ID
`sha256:0388863fe9964d7f2d0d8bacc26dcae0ad5888eadd275c10086a7683bfe46c56`.
The worker, API server, and processor report UID:GID `1000:0` with supplementary
group `1000`; `/run/opsflow` is not mounted. Existing DAG and log volumes are
`hy-home-infra_airflow-dags` and `hy-home-infra_airflow-logs`.

The observed DEV PostgreSQL container is
`db7edba6ddbf5624c707f4805babc95e59a89ed1eaf810a1f4a33493e23f3ba3` on
`dev_data_net`, using 18.6-ts2.30.2-pgbackrest2.57-r2, volume
`hy-home-infra_dev-pg-data`, and the path-only pgBackRest bind
`/home/hyunyoun/backups/dev-pgbackrest`. SeaweedFS HOME remains 4.47 on the
edge and `object/seaweed_internal` networks. These are read-only preparation
facts, not a claim that a P04 bucket, object policy, mount, backup, restore, or
role is ready.

Before any HOME execution, render the proposed seven-Airflow-role target with
the local candidate image ID, public `.env.example`, this worktree's source
directory, and an intentionally absent proposed secret path; record the render
only if its failure behavior is safe. Then obtain the accepted image/digest,
MNG metadata backup/migration decision, exact opsflow empty-restore target, S3
policy, and protected-file path contract. No Home service is changed by this
preparation, and the local image ID is not a repository digest or SEC01 image
acceptance.

The public render has completed, exit 0: all seven Airflow roles resolve to the
same local candidate image ID with `build: none` and `pull: never`; it uses the
public `.env.example`, no daemon action, and a worker-only unresolved private
path. The model preserves the Airflow, DEV, MNG, and object network structure.
This render proves no mount readability, secret delivery, image provenance, or
HOME readiness.

The only approved native resource envelope is the isolated PostgreSQL trial:
768 MiB memory, one CPU, 128 PIDs, a 512 MiB tmpfs, six minutes of execution,
and a separately reserved cleanup interval. The resulting assertion may prove
only `ISOLATED_PG_EMPTY_RESTORE`; full P04 PostgreSQL plus S3 empty-restore,
HOME recovery readiness, and authentication remain NOT_RUN. Synthetic roles
and dump material stay in memory; record only their SHA metadata and the
generated owned-container ID and attempt labels after execution.

`p04_native_qa` owns the bounded implementation/test execution and
`p04_runtime_review` owns its independent runtime/IaC review. The trusted human
authority is the full request and its selected isolated-validation plus
HOME-preparation scope. Neither role may invent credentials, claim a production
recovery result, or convert an unsigned/SBOM-unscanned/advisory-unreviewed
Airflow candidate into a HOME-approved image.

#### P05 schema-v2 source handoff

The reviewed source handoff remains `SOURCE_REVIEW_ONLY`, observed on main
`603a7637`. Earlier hashes in this Task remain historical receipts. The current
approved sources are `001_opsflow.sql`
`a9fecb083d60947a245e437fbbc97a3a5ac82a58d8d1842aff60ddefcfbca79f`,
`002_checks.sql`
`49126bd221ae768120d8b2f94627ba938f8e28da3cf24b2e555966e292ee04d8`, and
`003_business_date.sql`
`6c7f6fd032e9a0e73a104bc2376f9825f4e1bc28f7618652ebcc44b30abf8301`.
Schema v2 preserves the six-argument publication function and the six-field
claim result; ack/retry retains its five-attempt, 600-second contract. P05
runtime remains UNBOUND.

The final public P05 reference JSON begins `abca285` and has synchronized the
16-pass consumer contract while preserving provisional/native NOT_RUN state.
The P05 writer exclusively owns `outbox-contract.json` and its tests; P04 did
not copy SQL or edit that worktree. The approved hunk updates the `002` and
`003` hashes while preserving the NULL provisional binding. On new main
`5bf0e947`, the reviewed P05 binding still names historical `001`
`57a744cf...`; reconciling it with the approved final hashes requires explicit
permission outside this public hunk. That was BLOCKED at the recorded
checkpoint; the user subsequently granted the minimal reconciliation permission.
P05 still owns its QA edits and runtime remains unbound. No native PostgreSQL,
S3, or P05 notifier result follows from this source handoff.

A parent probe of the nonexistent
`tests.validation.test_n8n_outbox_e2e` module exited 1 with a loader error and
is NOT_RUN. The registered replacement
`tests.validation.test_n8n_outbox_contract` plus
`tests.validation.test_n8n_outbox_rehearsal` passed 13 tests, exit 0, in 1.693
seconds on base `603a7637`. This receipt is distinct from the earlier verified
16-pass consumer-contract commands and does not bind a P05 runtime target.

#### Fresh bounded-native and integration receipts

The user explicitly approved the P04 branch's public source-reference JSON
hunk. P05's foreign dirty diff was preserved. The JSON receipt begins
`49b26df`; it records the consumer contract and E2E 16 PASS result (parent,
1.437 seconds), while the worker reported 25 combined SQL/P05 PASS. These are
public source/consumer-contract checks and do not bind a P05 runtime target.

The initial native-module CI registration proposed an additional optional
runtime-skip class. Auto-review rejected that weakening. The safe final CI
change qualifies only BoundaryTests at
`f5e0783`; the existing skip list is byte-identical. The gate plan, five
workflows, seven jobs, and eight actions passed. The four P04 source modules
also passed 58 tests in 0.337 seconds. Independent IaC and security review
approved the exact harness, SQL/P05 handoff, and CI boundary at source hash
`ab11ed3`; neither review witnessed a native workload run.

The first positive PostgreSQL attempt used container ID
`7003bf37a21201f457e72a3310dfeb1ff10171395e06aea53e14df7a246b5418` with
the selected PostgreSQL 18.6 image. Provisioning failed before migration,
restore, or dump (exit 1). The harness cleanup then failed. An independent
manual identity check removed only that owned container and confirmed its
absence; no data artifact was created. The cleanup parser/status SQLSTATE fix
is at harness hash `cfe01484` and awaits one bounded retry plus review.

The failure traced to the root provisioner's quoted psql `:'create_schema'`
form in its `DO` block. It is a source defect, not a runtime privilege result.
The SQL worker exclusively owns the narrow `project.py` and DEV-PG test repair
after a worktree collision check found no dirty source. The repair needs a
source regression and verification before PostgreSQL is retried.

The isolated Airflow import passed with container ID
`7ef0608c7a65eb5ddcdd8295199a0bb62782e7dfe93c77413e23e517633a3143`; cleanup
left no orphan. It observed Core 3.3.2, Python 3.13.15, Keycloak provider
0.11.0, common-compat 1.20.0, Celery 3.24.1, boto3/psycopg2 imports, a passing
`pip check`, and UID:GID 50000:0. The target remained manual/paused with pool
one, retry two, and one task. The workload library was not imported and no task
executed.

The public SDK framework-warmup is separate from strict target checks. The
strict file/socket/subprocess gate passed after one narrowed retry; it does not
claim zero interpreter I/O. Earlier two zero-stdin transport failures and the
strict SDK-lazy-croniter/devnull-instrumentation failure remain preserved.
There is still no HOME worker S3 GET. The infrastructure helper result is 11
PASS, four BLOCKED for an external absolute path, and two NOT_RUN (exit 2).
Worker README metadata passed and the prior link corpus result was 1,272
documents/11,441 links with one historical warning; both predate this Task
amendment. Final long gates remain pending and criterion 18 is not closed.

#### PostgreSQL corrective progression

Project source `6cd65c97` corrected the quoted `DO`-block psql interpolation;
the associated DEV-PG test source begins `37381`. Positive attempt `20f40`
reached provision GREEN, then migration `001` failed at `42725`; cleanup
passed. Cross-database attempt `1dc241` showed `opsflow_ingest` could execute
`SELECT 1` in PostgreSQL, a genuine denial failure that remains FAIL. Diagnostic
`385df` reproduced `42725`; the public pure-catalog probe confirmed the
`text || internalchar` ambiguity.

The exact catalog-pair diagnostic driver was
`df21e0e46d38fb115d6db82881ae46b4ab3647225e241ee78acf7df5d288147b`, exit 0:
the untyped case produced `42725`, the typed case passed, and kind `r` cleanup
passed with the label query empty. The driver intentionally neither emitted nor
persisted an attempt container ID, so no such ID is recorded after cleanup.

The narrow correction adds eight explicit `::text` casts across four
fingerprints. Independent source and security review approved it. The current
`001`, `002`, and `003` hashes are those recorded in the P05 handoff above.
An earlier unaccepted DRAFT `001` changed catalog serialization only; it did
not change DDL, function, or grant behavior. Its historical hash and receipts
are preserved without silent repair. At this checkpoint, the positive post-cast
PostgreSQL attempt was pending; the completed source PASS and empty-restore
FAIL are recorded below. HOME, S3, and whole PostgreSQL-plus-S3 empty restore
remain NOT_RUN.

The final combined source/security P05 hunk review, beginning `abca285`,
approved ten source-consumer and 16 security-consumer checks. Current branch
coverage ran 79 tests, exit 0: `project.py` 81 percent, adapters 99 percent,
manifest 100 percent, and the selected directories 92 percent. The unchanged
monitor contributes 42 percent coverage and is not part of the corrected
source. The command used
`PATH=/tmp/hyhome-p04-qa-tools/bin:$PATH COVERAGE_FILE=/tmp/p04-final-source.coverage python3 -m coverage run --branch --source=infra/07-workflow/airflow/workloads/manifest-pipeline/workflow_lib,infra/04-data/dev-db/pg/provision -m unittest tests.lib.ops.test_opsflow_manifest tests.lib.ops.test_opsflow_adapters tests.lib.ops.test_opsflow_provision_contract tests.validation.test_opsflow_airflow_contract tests.validation.test_dev_pg_provision`.

The registered local changed aggregate exited 124 by timeout after document
metadata passed 148 checks in 521.410 seconds. Earlier hook checks passed 15,
lifecycle checks passed 15 in 136 seconds, and public links passed for 1,272
documents/11,441 links. Source changed during the aggregate run, so those
partial receipts are not a final atomic-head result. No gate code was changed
or bypassed; a hosted candidate must test the committed head.

#### Isolated PostgreSQL empty-restore result

Native source execution reached `001`, `002`, `003`, the business-date v1 RED
and v2 GREEN cases, idempotent/concurrent/backfill behavior, reader view,
outbox acknowledgement, wrong-role DML denial, and role/custom-data dumps.
The source attempt was `6e0b403af39825798681bd83`, container ID
`9f6cc1fc0521be67540d0f62b0b3ed2115880eecba3aab8548003253dbfc9c74`; the
restore attempt was `af5f5b1ba93b4aebd0dc5753`, container ID
`56aae931b150555850fef614c577620b46a1d05e0cfa190df67c426a2962f06a`.
Both used PostgreSQL 18.6 with plpgsql and had cleanup PASS with each exact
container absent afterward.

The role dump restore failed before `pg_restore` at psql `42501`. Accordingly,
`ISOLATED_PG_EMPTY_RESTORE` is FAIL, not NOT_RUN. The harness returned exit 1
despite four boundary PASS results; its exact branch coverage is 84 percent at
source hash `3aee`. No dump contains a password: the public synthetic role dump
is 1,795 bytes with SHA256
`01f629767e013035d395189d1fc6b5d9cbdf55fd5bb81b55ca5de00d46fa42e1`, and the
data dump is 27,206 bytes with SHA256
`7339e9e64ffaa625c6218554f9eeb643f75270bd30be0e17992fd7ed9a625a47`.

Full HOME PostgreSQL-plus-S3 recovery remains NOT_RUN. The current Task and
README metadata run selected two documents with zero violations before this
amendment; it is not metadata acceptance for this newer Task revision.

#### Corrected source handoff freeze for C1

The latest fetched origin/main observation begins `5bf0`; P05 PR 435 is merged.
This freeze prepares the concrete P04 C1 source commit only. It records isolated
PostgreSQL source success and the empty-restore FAIL above; it makes no native
full-P04, HOME, S3, or recovery PASS claim.

The P04-owned schema-v2 SQL handoff has one unchanged six-argument publication
interface and these final hashes: `001_opsflow.sql`
`a9fecb083d60947a245e437fbbc97a3a5ac82a58d8d1842aff60ddefcfbca79f`,
`002_checks.sql`
`49126bd221ae768120d8b2f94627ba938f8e28da3cf24b2e555966e292ee04d8`, and
`003_business_date.sql`
`6c7f6fd032e9a0e73a104bc2376f9825f4e1bc28f7618652ebcc44b30abf8301`.
The corrected source handoff has independent source and security approval.
The user granted the subsequent minimal binding-reconciliation permission.
P05 may reference C1 only through its own reviewed QA integration; the existing
historical P05 consumer heading and string remain preserved until then.

#### HOME preparation matrix — proposed, no execution authority

This matrix makes the selected HOME-preparation lane reviewable. Values marked
`<REQUIRED>` are not observed facts and cannot be inferred from source. The
candidate Airflow image remains isolation-only pending SEC01 and HOME approval.

| Boundary | Proposed owner and identity | Required evidence before action | Prohibited result |
| --- | --- | --- | --- |
| Compose and Airflow | Docker default context; project `hy-home-infra`; seven existing Airflow roles; observed HOME UID:GID `1000:0` is proposal only | Render with `<REQUIRED: OPSFLOW_CODE_DIR>`, candidate `<REQUIRED: OPSFLOW_AIRFLOW_IMAGE>`, and intentionally absent `<REQUIRED: OPSFLOW_SECRET_DIR>`; effective runtime UID:GID/groups remain REQUIRED | Starting or replacing any HOME role from this receipt |
| Ingest and S3 | `airflow-worker` only; canonical source names `opsflow-dev`, `manifest-input/`, and `manifest-validated/`; endpoint, identity, and existence remain REQUIRED | P03/operator identity, prefix-only HEAD/GET/validated-PUT/readback, SHA/size/version inventory, and retained orphan reuse decision | API server, scheduler, DAG processor, triggerer, Flower, n8n main/runners, reader, or notifier S3 access |
| PostgreSQL | Canonical database `opsflow_dev`; migrator is operator-only; ingest invokes approved functions; reader is operator-audit-only; P05 worker is notifier-only | Role provenance, approved grants/HBA, migration checksum, extensions and lock result | Owner/admin grants, direct ingest DML, or MNG access |
| Secret delivery | `<REQUIRED: OPSFLOW_SECRET_DIR>` supplied by P03/operator; inside container `/run/opsflow`; existing adapter-defined filenames only | Directory 0700 and files 0600, effective owner/groups, read-only regular non-symlink checks, and `airflow-worker`-only mount/readability proof | Secret value, filename invention, argv/log/CI/backups exposure, or P05 notifier-secret access outside its worker |
| Backup and restore | Operator and independent reviewer; separate empty PG and S3 targets | `<REQUIRED: PG backup set/WAL/checksum/extensions/role provenance>` plus raw/validated S3 SHA/size/version/readback inventory | Schema reconstruction, destructive orphan repair, in-place restore, or a HOME recovery claim |

The public-safe proposed commands below are templates, not authorization to
execute. They use no private environment file or credential value.

```sh
# Render only; <ROOT_MAIN> is the selected repository main path. The candidate
# image is isolation-only and <REQUIRED: OPSFLOW_SECRET_DIR> must stay absent.
OPSFLOW_CODE_DIR='<REQUIRED: public workload source>' \
OPSFLOW_AIRFLOW_IMAGE='sha256:8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2' \
OPSFLOW_SECRET_DIR='<REQUIRED: intentionally absent public placeholder>' \
docker --context default compose --project-name hy-home-infra --profile workflow \
  --env-file <ROOT_MAIN>/.env.example -f <ROOT_MAIN>/docker-compose.yml \
  -f <ROOT_MAIN>/infra/07-workflow/airflow/workloads/manifest-pipeline/compose.workflow.override.yml config

# Metadata/parse observation only, not worker, authentication, paused, or manual-state proof.
OPSFLOW_CODE_DIR='<REQUIRED: public workload source>' \
OPSFLOW_AIRFLOW_IMAGE='sha256:8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2' \
OPSFLOW_SECRET_DIR='<REQUIRED: intentionally absent public placeholder>' \
docker --context default compose --project-name hy-home-infra --profile workflow \
  --env-file <ROOT_MAIN>/.env.example -f <ROOT_MAIN>/docker-compose.yml \
  -f <ROOT_MAIN>/infra/07-workflow/airflow/workloads/manifest-pipeline/compose.workflow.override.yml \
  exec airflow-apiserver airflow dags list
OPSFLOW_CODE_DIR='<REQUIRED: public workload source>' \
OPSFLOW_AIRFLOW_IMAGE='sha256:8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2' \
OPSFLOW_SECRET_DIR='<REQUIRED: intentionally absent public placeholder>' \
docker --context default compose --project-name hy-home-infra --profile workflow \
  --env-file <ROOT_MAIN>/.env.example -f <ROOT_MAIN>/docker-compose.yml \
  -f <ROOT_MAIN>/infra/07-workflow/airflow/workloads/manifest-pipeline/compose.workflow.override.yml \
  exec airflow-apiserver \
  airflow dags details source_manifest_ingest

# Execute only after the migration receipt binds every <REQUIRED> input. The
# migrator connection and SET ROLE happen in the same psql session.
psql --dbname='<REQUIRED: migrator service>' -X -v ON_ERROR_STOP=1 \
  -v migration_sha256=82a4762a8962832c7fdd05826df3b97cf02cc4f96c974a328e42e4493143b18f \
  -c 'SET ROLE opsflow_owner' \
  -f infra/07-workflow/airflow/workloads/manifest-pipeline/sql/001_opsflow.sql
psql --dbname='<REQUIRED: migrator service>' -X -v ON_ERROR_STOP=1 \
  -v migration_sha256=830b62c6e8d175d5a4350bab27976121637df4aeca6688748865756be2d84d72 \
  -c 'SET ROLE opsflow_owner' \
  -f infra/07-workflow/airflow/workloads/manifest-pipeline/sql/003_business_date.sql

# Verify bounded reader/outbox counts only; 002 checksum verification remains an
# owner-controlled operator action, never an ingest runtime grant.
psql --dbname='<REQUIRED: reader service>' -X -v ON_ERROR_STOP=1 \
  -c 'SELECT count(*) FROM ops_flow.published_documents; SELECT count(*) FROM ops_flow.delivery_status;'
```

The verified public DAG-state query is NOT_RUN until it is bound to the selected
3.3.2 image and operator contract; the two commands above establish only
metadata presence/parse observation. Restore order is paired PG roles/WAL and
S3 raw/validated artifacts, then separate empty PG and S3 targets, then reader/
outbox/idempotency and S3 SHA/version validation, followed by separately
approved rebind/cutover. Use the existing [Airflow guide](../../../05.operations/guides/08-workflows-and-automation/0050-airflow.md) and [RUN-0021](../../../05.operations/runbooks/10-platform-and-backup/0021-backup-and-restore.md) rather than inventing a helper.

The following RUN-0021-derived restore references are gated templates, not
commands to run from this Task. The exact DEV source label, continuous WAL
range, executor, repository mount, paired filer/volume snapshot, and owned
empty targets are all REQUIRED. The prior `42501` empty-PG restore failure is a
historical checkpoint; the final isolated restore passed. Paired HOME PG-plus-S3
inputs and authorization still block HOME recovery acceptance, and no LAB
restore is in scope.

```sh
# RUN-0021 step 5 semantics: restore dev stanza into an owned empty PG target.
<REQUIRED: approved dev-pg restore executor> pgbackrest --stanza=dev \
  --set=<REQUIRED: approved backup label> --type=time \
  --target=<REQUIRED: approved recovery time> --target-action=promote \
  --archive-mode=off restore

# RUN-0021 step 6 semantics: restore the paired SeaweedFS Restic state set to
# an owned empty S3 target, then inventory filer metadata and volume tree.
restic restore <REQUIRED: reviewed paired state snapshot> \
  --target <REQUIRED: owned empty SeaweedFS target>
```

#### P05 binding recipe — proposed under explicit user approval

P05's owner verifies the C1 corrected-source-handoff-freeze-for-C1 hashes,
updates only its approved binding/test inputs, runs its owned QA, and records
the resulting commit. This Task does not make those edits or claim notifier
execution. Rollback pauses only the selected DAG, restores only the reviewed
target database to a separate target, validates it, and rebinds only after
approval; accepted outbox receipts are retained. It never changes MNG, deletes
shared volumes, runs `down -v`, or destructively repairs S3 orphans.

#### C2 P05 binding checkpoint

After explicit user approval, P05 committed the narrow reconciliation as
`fc3289738ee7bca59c22102e52e0b97bae66e001`. Its public JSON, contract-test,
and caller-test receipts begin `579b66ed`, `7498c409`, and `6d1a57e`,
respectively. Independent source/security review and registered local-staged
checks passed; the P05 contract plus E2E result passed 16 tests and the combined
rehearsal passed 19. C1 `c809153705d583998209330db932cbbe9bbe918f` remains
immutable, with the reviewed `a9fe` binding and
`corrected-source-handoff-freeze-for-c1` receipt. P05 native execution remains
NOT_RUN.

The roles-only bootstrap probe used source attempt
`5d43c03faf134cfc7ff6753a`, container
`1cefbe87dcfef41084727d5b1d45284769a2d49b44a5aa23cf54a32fa70cd04a`, restore
attempt `be93bffa42b5ea9875867a61`, and container
`b4735a97b679b7b04bccd97bfc0fc07c001ea84c645e770b574ea54a8e16425b`.
Cleanup passed and both containers are absent. Its single bootstrap call failed
closed for unknown phase (exit 1), so there is no roles-preservation PASS and
no database restore. PostgreSQL 18's formatter lookup indicates `SET TRUE` is
an omitted default; the driver's required `SET TRUE` may therefore reject valid
grammar. A QA RED/fix candidate is pending strict catalog checks and is not
accepted. No raw dump is recorded.

#### Restore-stable source handoff

This is the sole current official P05 handoff. The restore-stable schema-v2
sources are `001_opsflow.sql`
`82a4762a8962832c7fdd05826df3b97cf02cc4f96c974a328e42e4493143b18f`,
`002_checks.sql`
`7ed4bfd5f160e93ad810e8d32ce2221a02f1629946e5e4297817385acbbb13ed`, and
`003_business_date.sql`
`830b62c6e8d175d5a4350bab27976121637df4aeca6688748865756be2d84d72`.
They preserve one public interface and schema v2; independent source/security
review approved the narrow ACL-normalization correction without a DDL,
function, grant, or API change. C1/C2 references above are historical, not the
current binding. The immutable C3 source commit is pending; a later C4 binding
must use this handoff rather than rewriting that history.

The actual isolated harness is
`e46a8819069bc9c4a05b45d214706192a6db083ff41e8be996bdedd39120db8c`, approved
by source, security, and IaC review. One positive method passed, exit 0, in
16.466 seconds, alongside seven boundary PASS results and 87-percent branch
coverage (425 statements, 42 missed; 94 branches, 26 partial). PostgreSQL 18.6
with plpgsql used UID:GID 70:70. Source attempt
`3e71efe4ccb58806cd818087` used container
`2cfbd1ca3e22e9c880a804bcbf22641c5041adeff7a1c0010c7b25e8d5179ca3`; restore
attempt `4dfc2afbfb275657a3f654a7` used container
`efe4202fdb1d6bef21cb239517aa1579a71ec7f332027293d68887077965fe5d`. Cleanup
passed and both exact IDs are absent.

Roles and custom data restored, `RESTORED_SCHEMA_PREFLIGHT`, reader/outbox/
replay/pointer, UTC-date concurrency/backfill, and the reader grant/revoke
denial path all passed. Each of the reader-SELECT grant and owner-ALL revoke
checks used psql exit 3 with the sole `P0001` schema-drift rollback; the reader
then received `42501` denial and the baseline passed. The roles dump is 1,795
synthetic, password-free in-memory bytes with SHA256
`8898edfd5276d59a3fd15e31a751d64917fd02be279de6f73aef9f09ae37a757`; the data
dump is 27,205 bytes with SHA256
`0b2139f2f98c7ce366f95a551c319d7d4c8f633f8b07709559dfbde228da6c1c`.

The `8783` diagnostic proved only five NULL/default ACL representations changed
(four tables and one sequence) while effective ACLs remained equal. The new
normalizer covers tables `r`, partitioned tables `p`, views `v`, materialized
views `m`, foreign tables `f`, and sequences `S`, plus NULL defaults and sorted
grantor/grantee/PUBLIC/privilege/grantable JSON. Explicit `{}` ACLs preserve
their semantic `[]`; only non-grantable relation kinds retain raw metadata. It
does not retroactively repair or accept earlier receipts. The historical
`42501`, `645/P0001`, and `0797` failures remain preserved.

`ISOLATED_PG_EMPTY_RESTORE` is now PASS. Cross-database CONNECT remains FAIL;
full HOME PostgreSQL plus S3 recovery, HOME worker S3 GET, and authentication/
TLS proof remain NOT_RUN. PR 437 is an actual draft at head `fc328`; its source
candidate quality run `38337706234` passed, as did CodeQL and GitGuardian.
Final-head CI, independent delivery review, merge, criterion 18 HOME evidence,
and the Task remain in-progress.

Metadata validation at C1 `c809153705d583998209330db932cbbe9bbe918f` passed,
exit 0, selecting the then-current Task and SQL README with zero violations.
Its inputs were Task v0.1.12 SHA256
`edd74041a86372527ff5c84c6e2ccd993ed2edf46eb4763f1c992ca3f37885e5` and
SQL README SHA256 `cd2f33`; it predates this amendment and is not a PASS for
this amendment. The prior final local-staged check also passed before C1; neither
receipt replaces the required check on the final integrated head.

### Current TLS source correction — 2026-10-14

The current user request authorizes safe source fixes, tests and owning-Spec
PR delivery from `ALL_PROMPTS.md` input SHA256
`3a8c715ee7d6719535f44ba2d6174fdc2609861915417bb27b2f9d586dd0bdde`.
This unit uses base `262dc2dde6eea27195f7d8909e9453f5ccc97f66` and
`codex/p04-tls-ca-delivery`. The worker owns adapters, the new package-local
`tls.py`, the DAG and the two existing test modules. The controller owns the
workload/library READMEs and this result receipt. SQL, Compose and P05 binding
remain byte-for-byte unchanged. The existing workload-prefix selector covers
the helper; no shared manifest or workflow is changed.

The earlier `tls_delivery_not_ready` guard was an intentional historical
source limitation, not the current behavior. Current source validates protected
CA input and pins the verified bytes in a sealed memfd. When TLS is selected,
PG requires verify-full and rejects ambient connection variables. S3 admits only the fixed future
`https://seaweedfs-s3:443` origin/contract, disables proxies and redirects, and
closes its client/CA snapshot on both normal and exceptional DAG exits.

Initial new regression tests ran 35 cases with 7 failures and 10 errors before
implementation. The initial size-driven test refactor then broke the existing
E2E `ConnectionDouble` consumer (77 cases, 5 errors); restoring that public
fixture API corrected it. Neither failure is rewritten as success. Final
independent QA and security checks ran the expanded registered suite: 77 PASS,
zero skips, exit 0. Ruff check, format check and diff check passed. Worker
coverage.py 7.16.2 branch measurement reports total 94%, adapters 94%, TLS 85%
and DAG 100%; an independent coverage rerun was sandbox-blocked, so those
percentages are worker-observed rather than independently reproduced.

The first reviewed code manifest was
`3e84f0d935d76841f9ce0abfa5ae36638d985836211b8334483161eb85c6088a`.
Independent IaC review then found that libpq may prefer GSS encryption over
TLS despite verify-full. A new driver-argument assertion failed with KeyError
`gssencmode` (one case, exit 1). Explicit `gssencmode=disable` plus poisoned
`PGGSSENCMODE` coverage passed the two targeted cases and the expanded 77-case
suite. Independent QA, code, security and IaC affected-slice reviews approved
the corrected source. The final five-file checksum manifest is `b196ed66fd08ba32d20798f556fe9bd6ebc84d3d5c685af2c56b37a6e5a497d8`.
The manifest hashes UTF-8 rows sorted by repository-relative path, each
`path`, one ASCII space, file SHA256 and LF, including the final LF. The five
paths are the adapters, TLS helper, DAG, adapter tests and Airflow contract
tests named in this unit. This closes the source transport finding only; the
[libpq connection contract](https://www.postgresql.org/docs/18/libpq-connect.html)
and exact-image compatibility still require their named native evidence.
Actual SeaweedFS TLS listener/certificate/SAN, wrong-CA/expired-certificate
handshakes, frozen driver/image behavior, real Celery worker identity and
protected-file readability, DB/S3 publication, auth/restart and recovery remain
NOT_RUN. The existing internal plaintext :8333 lane is preserved. Historical
cross-database CONNECT denial FAIL is a separate privilege gap and is not
resolved by this source unit. Criterion 18 remains pending.

### Current TLS logical commit receipt — 2026-10-14

The reviewed eight-file source/document unit was committed as
`667dcd9328ca6aa2923ad14a012967931877931b`,
`fix(airflow): Enable verified TLS for manifest adapters`, with normal hooks.
Immediately before the commit, explicit staging contained only its five
source/test files, two workload/library READMEs and this Task. The registered
Python Commitizen 4.15.1 check with `.cz.toml` and the 75-character limit passed;
`rtk bash scripts/validation/run-ci-precommit.sh --mode local-staged` then
passed all applicable style/secret hooks without edits, exit 0. No index change
occurred between that PASS and the commit. Push/PR/merge had not run at this
receipt; current source-only delivery does not close criterion 18.

The prior selected document metadata command used
`rtk python3 scripts/validation/check-document-metadata.py --mode check-changed
--base-ref HEAD` with explicit `--changed-path` arguments for the workload
README, library README and this Task: selected 3, violations 0, exit 0. The
canonical registry/spec-package reader loaded 32 packages, exit 0.
`rtk python3 scripts/validation/check-document-links.py --mode traceability`
checked 1,295 documents/11,534 links with zero failures or warnings, exit 0.
These structural checks preceded the final wording-only clarification and
this result-only addition; they are preserved against their actual inputs,
not relabeled as a check of this new Task hash. Independent final code/security
review approved the last wording clarification before the staged gate.
Task-only metadata/links/review must cover this new receipt before commit;
unchanged source tests are not repeated merely to record their result.

### Follow-ups from the TSK-0013 W42 review 2026-10-30

TSK-0013 froze 001, 003 and 004 as the P05 interface after an independent
security review that approved them with notes. The notes belong to this Task.
Medium:

- `002_checks.sql` accepts only versions 1 and 2, so it needs a post-004
  version.
- The checks need executable denial cases: ingest and reader cannot run
  `unknown_notification` or `retry_not_sent_notification`, and cannot read
  `notification_reconciliations`.

Low, for the next migration:

- use `SET search_path = pg_catalog, pg_temp`;
- give 001-style migrations their own lock and statement timeouts and the
  migration advisory lock;
- add SKIP LOCKED to the claim's expiry sweep;
- map a same-day publication's `23505` to a named contract error;
- drop or fix the migrator `EXECUTE` grant on reconcile, which has no effect;
- add connection limits and per-database role settings to the fingerprint.

None of these changes the frozen interface. A migration that does change it
needs a new TSK-0013 binding.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Git and owner baseline | 1, 18 | W34 | status/worktree/fetch/open PR inspection | Local74feff942; remote6da5e3bf3 | PASS | Assessment above; no remote write or P04 runtime | - |
| Existing source reuse | 1, 8, 18 | W34 | Focused existing DEV/workflow/registration unittest | Clean74feff942 | PASS | 35 tests, 9.529s, exit0; command below | - |
| Supplied reference audit | 18 | W34 | Extracted public reference UNIT only | Prompt c50695e5a46c; isolated Python3.12.3 | PASS | 42 tests, 0.19s, exit0; ignored receipt only | - |
| New manifest implementation | 18 | W35 | RED/GREEN parser and protected adapters | b2a46bc88 plus latest SQL inputs in Work Log | PASS | Final52 unit/synthetic/source tests, exit0; native excluded | - |
| New SQL contract | 18 | W36 | Source guards for migration and outbox | Latest SQL hashes in Work Log | PASS | Source checks only; native PostgreSQL evidence is the W38 restore row | - |
| New DAG contract | 18 | W37 | Synthetic SDK import and public overlay model | Frozen DAG/overlay hashes in Work Log | PASS | Five synthetic tests and independent Compose render, exit0 | - |
| Typed optional overlay candidate | 18 | W37 | RED/GREEN profile/inventory boundaries, coverage and official catalog | Main 4c83f14b plus final classifier/test/overlay hashes in Work Log | PASS | 59 focused and 102 full-module tests; catalog exit0; SOURCE/UNIT/STATIC only, review/delivery pending | - |
| Required image projection candidate | 18 | W37 | RED/GREEN required-input projection and concrete-pin preservation | f1a7726 plus frozen script/test/registry hashes in Work Log | PASS | 33 class tests, root63 regressions, generator/check and manifest exit0; unresolved image, combined delivery pending | - |
| Isolated empty PostgreSQL restore | 18 | W38 | `ISOLATED_PG_EMPTY_RESTORE` | Restore-stable isolated PostgreSQL harness | PASS | Roles/custom data, preflight, reader/outbox/replay/pointer, and UTC-date cases passed; cleanup confirmed | - |
| Cross-database CONNECT denial | 18 | W38 | Cross-database role boundary | Isolated PostgreSQL role probe | FAIL | `opsflow_ingest` could execute `SELECT 1`; the denial boundary remains open | - |
| HOME/S3 recovery | 18 | W38 | HOME, S3, worker GET, full recovery | No bound HOME/S3 target or authorization/TLS proof | NOT_RUN | HOME/S3, worker S3 GET, and full recovery remain unexecuted | - |
| Rotation | 18 | W38 | Credential rotation | No rotation required | NOT_APPLICABLE | No rotation authorized by issuance | - |
| Delivery | 8, 18 | W39 | Latest-head CI/review/PR/merge | Draft PR 437 at published head `fc328`; revised head pending | NOT_RUN | Candidate checks passed, but final revised-head CI, independent review, and merge remain pending | - |
| Segmented source checks | 8 | W39 | Registered local nodes0–32 across preserved runs; final continuation26–32 exit0 | c7d56a383 then5b1a92db; unchanged registered contract | PASS | Segmented Local Source Validation; original aggregate124 and suffix1/1 preserved; final docs/delivery pending | - |
| Current TLS source RED | 18 | W35 | New adapter/Airflow source regressions; 35 cases, 7 failures and 10 errors; exit 1 | Base 262dc2dde with newly written synthetic regressions; exact RED patch hash not recorded | FAIL | Current TLS source correction | - |
| Shared fixture compatibility regression | 18 | W35 | Expanded P04/E2E source suite; 77 cases, 5 errors from missing ConnectionDouble; exit 1 | Initial split test freeze; adapter-test SHA 582e9e65ecdd5e5d755d863d7780872ef435623046c27aa14a77be7339139b7f | FAIL | Current TLS source correction | - |
| Current TLS source and fixture GREEN | 18 | W35 | python3 -m unittest tests.lib.ops.test_opsflow_manifest tests.lib.ops.test_opsflow_adapters tests.lib.ops.test_opsflow_provision_contract tests.validation.test_opsflow_airflow_contract tests.validation.test_opsflow_e2e_acceptance -v; 77 PASS, skip 0; exit 0 | Five-file manifest 3e84f0d935d76841f9ce0abfa5ae36638d985836211b8334483161eb85c6088a | PASS | Current TLS source correction | Current TLS source RED, Shared fixture compatibility regression |
| Current TLS source style and security review | 18 | W35 | Scoped Ruff check/format, diff check and independent security source review; PASS | Same five-file checksum manifest | PASS | Current TLS source correction | - |
| GSS transport assertion RED | 18 | W35 | PostgresAdapter.test_verify_full_driver_reads_sealed_ca_and_closes_it_after_connect; 1 case, KeyError gssencmode; exit 1 | Pre-GSS manifest 3e84f0d935d76841f9ce0abfa5ae36638d985836211b8334483161eb85c6088a | FAIL | Current TLS source correction | - |
| GSS transport correction GREEN | 18 | W35 | Explicit gssencmode=disable; argument and poisoned PGGSSENCMODE tests; targeted 2 PASS, expanded 77 PASS, skip 0; exit 0 | Final five-file manifest b196ed66fd08ba32d20798f556fe9bd6ebc84d3d5c685af2c56b37a6e5a497d8 | PASS | Current TLS source correction | GSS transport assertion RED |
| Final TLS source QA and independent review | 18 | W35 | QA expanded 77-case suite; Ruff/check/format/diff; independent code, security and IaC affected-slice approval | Final five-file manifest b196ed66fd08ba32d20798f556fe9bd6ebc84d3d5c685af2c56b37a6e5a497d8 | PASS | Current TLS source correction | - |
| Current TLS logical commit | 18 | W39 | Explicit reviewed eight-file staging; registered Commitizen 4.15.1 and local-staged hooks PASS without edits, normal commit exit 0 | Commit 667dcd9328ca6aa2923ad14a012967931877931b; final source manifest b196ed66fd08ba32d20798f556fe9bd6ebc84d3d5c685af2c56b37a6e5a497d8 | PASS | Current TLS logical commit receipt — 2026-10-14 | - |

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
`python3 scripts/validation/run-ci-gate.py --profile changed` and
`scripts/validation/run-ci-precommit.sh --mode local-staged`; proposal-only
registration is not a PASS. Run document metadata/links and git diff --check.
Keep SOURCE / UNIT / STATIC / ISOLATED / HOME / MIGRATION / ROTATION /
RECOVERY / DELIVERY separate; unit results do not satisfy native acceptance.

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 18 | pending | - | - |

## Review and Completion

Issuance was draft; the current worker transition is in-progress as recorded
above. The user's latest reply again leaves SEC01/P03 contracts unconfirmed.
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
- [Airflow guide](../../../05.operations/guides/08-workflows-and-automation/0050-airflow.md)
- [Airflow source](../../../../infra/07-workflow/airflow/README.md)
- [DEV database source](../../../../infra/04-data/dev-db/README.md)
- [SeaweedFS source](../../../../infra/04-data/seaweedfs/README.md)
