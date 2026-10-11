---
title: "P04 Airflow Independent Manifest Pipeline Task"
version: "0.1.4"
type: "sdlc/task"
status: "in-progress"
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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Git and owner baseline | 1, 18 | W34 | status/worktree/fetch/open PR inspection | Local74feff942; remote6da5e3bf3 | PASS | Assessment above; no remote write or P04 runtime | pending |
| Existing source reuse | 1, 8, 18 | W34 | Focused existing DEV/workflow/registration unittest | Clean74feff942 | PASS | 35 tests, 9.529s, exit0; command below | pending |
| Supplied reference audit | 18 | W34 | Extracted public reference UNIT only | Prompt c50695e5a46c; isolated Python3.12.3 | PASS | 42 tests, 0.19s, exit0; ignored receipt only | pending |
| New manifest implementation | 18 | W35 | RED/GREEN parser and protected adapters | b2a46bc88 plus latest SQL inputs in Work Log | PASS | Final52 unit/synthetic/source tests, exit0; native excluded | pending |
| New SQL contract | 18 | W36 | Source guards for migration and outbox | Latest SQL hashes in Work Log | PASS | Nine source tests, exit0; PostgreSQL native NOT_RUN | pending |
| New DAG contract | 18 | W37 | Synthetic SDK import and public overlay model | Frozen DAG/overlay hashes in Work Log | PASS | Five synthetic tests and independent Compose render, exit0 | pending |
| Typed optional overlay candidate | 18 | W37 | RED/GREEN profile/inventory boundaries, coverage and official catalog | Main 4c83f14b plus final classifier/test/overlay hashes in Work Log | PASS | 59 focused and 102 full-module tests; catalog exit0; SOURCE/UNIT/STATIC only, review/delivery pending | pending |
| Required image projection candidate | 18 | W37 | RED/GREEN required-input projection and concrete-pin preservation | f1a7726 plus frozen script/test/registry hashes in Work Log | PASS | 33 class tests, root63 regressions, generator/check and manifest exit0; unresolved image, combined delivery pending | pending |
| Native batch and recovery | 18 | W38 | ISOLATED/HOME/MIGRATION/RECOVERY | No selected ready execution contract | NOT_RUN | No DB/role/bucket creation or deployment | pending |
| Rotation | 18 | W38 | Credential rotation | No rotation required | NOT_APPLICABLE | No rotation authorized by issuance | not-required |
| Delivery | 8, 18 | W39 | Latest-head CI/review/PR/merge | Local source commits; no P04 PR | NOT_RUN | Local checks do not satisfy remote CI/merge | pending |
| Segmented source checks | 8 | W39 | Registered local nodes0–32 across preserved runs; final continuation26–32 exit0 | c7d56a383 then5b1a92db; unchanged registered contract | PASS | Segmented Local Source Validation; original aggregate124 and suffix1/1 preserved; final docs/delivery pending | pending |

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
- [Airflow guide](../../../05.operations/guides/0050-airflow.md)
- [Airflow source](../../../../infra/07-workflow/airflow/README.md)
- [DEV database source](../../../../infra/04-data/dev-db/README.md)
- [SeaweedFS source](../../../../infra/04-data/seaweedfs/README.md)
