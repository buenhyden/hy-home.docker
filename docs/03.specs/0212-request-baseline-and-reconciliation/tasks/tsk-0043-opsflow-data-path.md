---
title: "Opsflow Data Path Task"
version: "0.1.8"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0043"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-02"
---

# Opsflow Data Path Task

## Overview

This draft Task records the approved P04 local implementation and its exact
evidence. A draft label does not imply missing source or cancel earlier acceptance.

### Objective

Repair the existing Opsflow Airflow path: safe connection URI construction,
bounded invalid-input quarantine, explicit data_version, least-privilege fixture
access and metadata-preserving independent isolated restore. Preserve the
existing CDC, analytics and optional Iceberg contracts. A new experiment waits
for actual inputs rather than a fabricated dataset or application.

## Inputs and Authorization

The direct user approval of the P04 plan on 2026-11-02 authorizes bounded local
source/configuration/documentation changes, synthetic and owned isolated tests,
independent review and a normal local logical commit. The observed clean start
is HEAD `6853286dbd73851a6419f7fb5457c53720ba6d98`, branch
`codex/p03-model-runner-tool-contracts`. This identity is an observation, not a
future constant. Service counts and earlier ledger snapshots are not targets.
The local integration branch was subsequently created as
`codex/p04-opsflow-data-path` at the same parent; this does not change the
recorded initial branch observation or authorize remote integration.

No operating HOME service, host setting, actual credential, external checkout,
remote integration or image/model download is changed. Operating restore,
credential issuance/rotation and P12 final acceptance have separate owners and
authorization. Shared MNG Valkey remains the default; dedicated opt-ins remain
available. DEV PostgreSQL's internal 5432 is distinct from its host publication.

Governing inputs are REQ-0027, AD-0031, this package's approved Spec/Plan, the
provided P04 crosscheck/corrections/ownership material, and current tracked
source. Historical SPEC-0204-TSK-0012 and its supporting Worker/restore records
retain their original actor, generation, criterion and environment scope.

## Work Log

### Baseline and issued writer leases

The documentation writer recorded public pre-edit SHA-256 values at
`_workspace/repo-support/analysis/p04/doc-baseline.json` before this amendment.
No private input body, credential or credential-derived hash was read. Each
source writer records its own exact path fingerprints before editing and
hands them to this Task. Changed shared input pauses only its dependent slice.

| Scope | Single writer | Reviewer | Boundary |
| --- | --- | --- | --- |
| DAG, manifest/adapter and new SQL migration | `/root/p04_pipeline` | independent code/security/SQL review | Existing Opsflow path only; issued SQL migrations and P05 outbox signature preserved |
| Airflow Compose and Dockerfile | `/root/p04_infra` | independent IaC/security review | Small read-only helper installation and supported _CMD wiring; pins/listeners/topology remain owned by current contracts |
| Unit/integration/CLI and owned native fixture | `/root/p04_uri` for URI tests; `/root/p04_pipeline` for pipeline tests; `/root/p04_native` for owned native fixture | independent code/security review | Synthetic credentials and exact owned isolated resources; no HOME operation |
| Spec, Plan, this Task, DATA-0096 and selected living docs | `/root/p04_docs` | independent document review | P04 amendment only; completed Task bodies preserved |
| Script manifest and CI selectors | `/root/p03_docs_impl` reused as the P04 CI integrator | independent CI review | Register existing scoped tests without broadening runtime or environment authority |

The documentation pre-edit values are Spec
`745a0fc75e24cbfbcd134a65e736c3f86b505f6f4d347bcb80d481767e07d767`,
Plan `077d5987c6dc0e265a5ee079927bd670b586745fa4105c2d1895dd10577f7a67`,
DATA README `f8cb82887f3e6dcea2dd922f484ad8709a077ed43dcd8b4f2134dcc508a273f3`
and data payload
`e71b6ca961740e6cd6045202801f6dea88f4e32aa076fb961c2311082d4da895`.
The new Task did not exist at the start. Only the documentation writer
integrates these shared-file segments. The separate CI projection writer
`/root/p03_docs_impl` retains only the canonical m0021 generated inventory block;
the catalog correction changes seven Airflow Env cells and no historical prose.

### Exact source lease packets

- `/root/p04_uri` alone writes new `infra/07-workflow/airflow/connection_uri.py`
  and `tests/validation/test_airflow_connection_uri.py`. Its only existing P02
  edit is `ManagementDataPortContractTests.test_airflow_uses_declared_management_postgres_and_valkey_ports`
  in `tests/validation/test_p02_service_contracts.py` (pre-edit file
  `b15238120e8e40b1eb49a9f603a1f540c56933e8d32621a030f8398b4a523dec`).
- `/root/p04_infra` alone integrates Airflow `Dockerfile` (pre-edit
  `afc44a2c14f8937193eabecf00f1433bbf0bbac349b6172335ada81a758319f1`)
  and `docker-compose.yml` (pre-edit
  `b3ddab42b06ae41a332b6b683ffb2846f9a40110903feb6d44727a162e05ecb9`).
- `/root/p04_pipeline` alone integrates `manifest.py` (pre-edit
  `ef19e0093b990c6b8400b29f234877e9d6f346a38440f3a181c37aa5cd744b60`),
  `adapters.py` (pre-edit
  `9cf420222aa3d90e1db8507130afa04242e3a9a469283871e3ca19c678a4cbf5`),
  optional new `quarantine.py`, new SQL `005_data_version.sql` and
  `006_checks.sql`, and its manifest/adapter/quarantine/contract tests. Issued
  SQL 001–004 remain byte-for-byte unchanged; the new checks support version 4.
- `/root/p04_native` owns the Airflow rehearsal and its Airflow-specific helper,
  new focused data/metadata tests, and the bounded `_generated_secrets` evidence
  extension for paired synthetic administrator credentials. No general fixture
  guard is weakened. Exact pre-edit values are required before its write.
  The supervisor subsequently assigns `/root/p04_infra` a QA-only lease for
  new `tests/validation/test_opsflow_airflow_native_scenario.py` (ABSENT before
  this unit). After two execution-capacity interruptions, the supervisor transfers only this
  test-file lease to `/root/p04_uri`, preserving the earlier writer's existing
  467-line test file (takeover SHA-256
  `8fee4aec372126483ec93bf7fe7a5982ce3852a8d9d7acd9baff41f88b6ac1ef`).
  Neither author edits reviewed production code; `/root/p04_pipeline`
  independently reviews the tests. Synthetic control-flow coverage does not
  resolve a failed real native rehearsal.
  Its pre-edit Airflow rehearsal SHA-256 is
  `3311383f4ad3a11c6f32be4f18992ebd7a03d0a86355a78d2b6f5598e427691f`,
  Airflow-specific fixture `43f1ae528442669c2fbe53234117d016f8f28104c9c44876ab7d2957a0f68688`,
  guards `87968dcb0cab174db4f822b3879e4369ca167b00ed298229ef8d644cecb51d36`
  and evidence `bc9cf5e4b53f1e44d302944825bc19665969ec7eae1c59dceb237d769fa47571`.
- The documentation writer owns the workload, SQL, library and DAG READMEs;
  the Airflow runbook; the Flink README; and the lakehouse guide's observed
  TaskManager healthcheck wording. Each additional existing path is fingerprinted
  locally before its first edit. DATA-0096 is regenerated only after source freeze.

Acceptance owner, source writer, reviewer, data owner and operational accepter
are separate. The local source acceptance owner is SPEC-0212 TSK-0043; actual
business data owner and operating accepter remain UNASSIGNED until identified
through their trusted channel. P labels and past names confer no account rights.

### Current dispositions and evidence axes

| P04 item | Criterion | Work Unit | Initial disposition | Current action and residual |
| --- | --- | --- | --- | --- |
| P04.01 | 66 | W71 | REUSE_ACCEPTED | Preserve existing DEV/MNG provisioning boundaries; run affected source regressions. Historical acceptance is reused only for its evidenced scope. |
| P04.02 | 67 | W72 | IMPLEMENT_GAP | Repair URI encoding, quarantine, data_version and independent isolated recovery. Current Worker and restore results await actual receipts. |
| P04.03 | 68 | W73 | SOURCE_READY | Existing platform_dev CDC/Avro source and historical rehearsal are retained. Opsflow adoption is deferred until a consumer and exact provisioning/offset/recovery contract exist. |
| P04.04 | 69 | W74 | SOURCE_READY | Reuse Opsflow quality blocking; expand negative publication evidence. Optional engine connectivity/smoke is not business output acceptance. |
| P04.05 | 70 | W75 | BLOCKED | User chose deferral until actual dataset/version, time field, target, baseline and owner exist. No private notebook inspection or invented experiment. |
| P04.06 | 71 | W76 | REUSE_ACCEPTED | Retain accepted optional Iceberg platform; this workload's adoption is deferred. Current version equivalence and independent recovery remain separate. |

Source, static checks, isolated tests, recorded historical operator acceptance,
this execution's direct operation, credential rotation, independent restore,
hosted CI and final acceptance are independent fields. Current operation,
real credential actions, HOME independent restore, remote CI and P12 acceptance
are NOT_RUN. A fixture restore will be recorded as isolated restore only.

### Preserved consumer and acceptance scopes

The current CDC connector names `dev-pg:5432/platform_dev`, `app` plus
`debezium_heartbeat`, publication `hyhome_platform_publication`, connector-owned
slot `hyhome_platform_slot`, topic prefix `hyhome.platform`, initial snapshot
and Avro converters through Schema Registry. Its provisioner separates the
administrator from the restricted replication login, refuses a foreign
publication scope and writes only its heartbeat table. It does not enroll
Timescale internal chunks. This is not Opsflow's `opsflow_dev/ops_flow` owner
contract. SPEC-0204-TSK-0005 W15 records an isolated 260-second snapshot,
Avro/schema-v2, restart/offset and heartbeat-LSN PASS at commit `619c984cb`;
that historical synthetic consumer does not prove a current business consumer
or current live offset recovery. No connector is registered or repointed here.
P07 retains current per-slot/WAL/consumer-lag observation; P12 retains vertical
acceptance once a business consumer is selected.

ADR-0039 remains accepted. SPEC-0180-TSK-0008 records the owner-approved
2026-09-24 lakehouse acceptance: table bucket/namespaces, Spark listing,
Flink batch plus checkpointed stream, Trino 23-row readback and GX three-check
PASS. Current source pins are a later observation, not proof that this historical
runtime validates them. Shared lakehouse identity can write/delete; Trino/GX
username is not an authentication or read-only boundary. No retention, orphan
cleanup or snapshot expiry is run. Catalog, objects and Flink checkpoints must
be recovered together for the selected capability; snapshot rollback alone is
not an independent backup restore.

Optional dbt connectivity/create-view smoke and the GX lakehouse rehearsal
suite remain separate from Opsflow publication. Flink's tracked rehearsal
uses datagen and is not the Kafka/Debezium business stream. Jupyter work is a
host-managed mount; its private body was not inspected, so public source absence
is not evidence that private experiments do not exist. Actual experiment input,
SDK identity and artifact recovery contracts remain prerequisites if P04.05 is
resumed. P02/P03/P06 retain the machine-authentication handoff for MLflow;
browser SSO and allowed-Host validation do not establish SDK authorization.

### Implementation and recovery contract

The URI helper reads bounded private files, uses one-time password-component
encoding and outputs the URI only to Airflow's supported _CMD consumer. Errors
and test receipts contain neither password nor complete URI. The reader accepts
single-line UTF-8 with an optional single terminal LF, preserves surrounding
spaces and literal percent, and rejects embedded newlines/NUL/bad encoding;
broker control characters also follow its existing ACL reader restriction.
MNG PG/broker nondefault listeners are exercised without relaxing DEV ownership.

Invalid bounded manifests retain their original bytes, digest and fixed reason
under a deterministic manifest-quarantine key. No SQL/outbox publication follows
rejection; failure to quarantine fails closed. Unreadable/oversized input is not
copied or called preserved. raw_sha256 becomes data_version in bounded DAG
results and an approved reader view using a new migration, while run_id and P05
outbox remain unchanged.

The existing native Worker fixture uses the actual URI helper, restricted Worker
S3 identity and a separate setup/recovery administrator. Other bucket/prefix and
delete denials must be observed on the actual cached server; unsupported policy
semantics remain unaccepted. Restore covers DB roles/extensions/schema/current
publication/outbox plus S3 body, size, Content-Type, user metadata and tags in a
separate owned target. Fresh server ETag/version identifiers need not equal the
original. Same-input replay must preserve business output without duplicate
publication or a new outbox notification. This P04 fixture has no actual n8n or
SMTP delivery service: outbox/claim/ack state is not proof of real delivery or
absence of a repeated SMTP effect. Actual notification remains P05/P12 NOT_RUN.
Existing custody/barrier procedures are reused.

### Public connection extraction limit

The read-only inventory comparison found zero extracted Airflow _CMD rows both
before and after this P04 change: the existing parser never recognized these
three command-derived URIs. There is no P04 row loss, but metadata/result/broker
connections remain an explicit semantic extraction blind spot. The manually
reviewed source/port/helper contracts in this Task do not become stored product
registration. P01 receives a bounded public-only extraction handoff: recognize
only the known helper commands, public port and host/secret-reference selectors;
never execute the helper or read private values. No parser change is included
in this P04 implementation.

### Image and native environment observations

The existing local `hy-home/airflow:3.3.2-keycloak` image is cached as
`sha256:b7c57ce073b480a512240aa5e364be80d3acffdf88384b60ddee7a1958f37dfc`.
The exact pinned upstream base image is absent from the image store. No pull
or new Dockerfile build occurred. A broad cache-size query was cancelled with
exit 130 without output, so builder-cache availability is UNVERIFIED. Existing
cached-image execution with injected reviewed helper/source is isolated behavior
evidence only and does not accept a newly built image artifact. The new-image
build and supply-chain acceptance remain P08/SEC01 residuals.

### Existing file-size maintenance boundary

The existing Airflow-specific fixture was already 822 lines at the baseline
and is now 846; new data/scenario/test files stay below 800. The bounded P04
extension does not justify an unrelated fixture rewrite during runtime
verification. A later maintenance unit may split the existing helper under its
own exact writer/review lease. This source-maintenance note is neither a
security finding nor a runtime acceptance result.

### Verification and stop conditions

RED precedes GREEN for each behavior change. New executable code must reach
80% coverage. Use focused unit/integration/CLI tests, registered local QA,
synthetic Compose render and independent code/security/SQL/IaC/document review.
Metadata/link/Registry gates sharing caches execute sequentially. The final
source is followed by graphify update, current DATA comparison and diff review.

Preflight trusted UID/GID/temp paths, existing tools, exact cached image identity
and resources before one owned cluster at a time. No pull or protection-guard
weakening is allowed to make a test pass. Keep existing time limits; preserve
the exact failed phase and bounded receipts on interruption. Unrelated n8n
receipt drift remains P05/P08-owned rather than a P04 success or blocker to
unrelated local implementation. Roll back only this logical source delta;
real data recovery requires its separate approved contract.

### D04 phase diagnosis and native reruns

A direct user request on 2026-11-04 re-ran this contract as D04 on clean `main`
`fb790c539b267f8acb85f5897a110db22ae347fa`, branch
`fix/opsflow-storage-admin-cpu`. The Opsflow/Airflow source suites ran 248
tests: OK, eight declared skips. The cached Airflow 3.3.2 image
`sha256:8c139ddd…` and SeaweedFS 4.48 `sha256:4e61d15f…` were present; nothing
was pulled or built. Running `dev-pg` and `mng-pg` have no replication slot,
and both declare `max_slot_wal_keep_size=2048MB`.

Phase timing of the narrow storage rehearsal reproduced the earlier ERROR at
189.5 seconds: probe 57 s, storage readiness 38 s, then each S3 call about 27 s.
In-container timing showed 23 s importing boto3 and creating the client, and
0.2 s of S3 work. The cause was the 0.05 CPU `storage-admin` cap, not the
policy or the server. With the fixture default 0.25 CPU the same call took
about 5 s and the narrow rehearsal passed in 125.5 s: the old principal policy
allowed delete (204), and the corrected policy matrix passed. Owned residue was
zero.

The first full Worker rerun then passed the corrected S3 matrix and stopped at
`quarantine metadata changed`. Instrumentation showed matching bytes, reason
and data version, but ContentType `application/json`. A minimal pinned-image
probe confirmed that SeaweedFS 4.48 stores `application/json` for any `*.json`
key whatever the request sends, while a `.bin` key keeps the requested type.
The production SeaweedFS uses the same digest, so every quarantine write failed
its own verification there and surfaced only as a generic contract rejection.
`put_quarantine` now stores and verifies `application/json`, matching the key;
a regression with an extension-typing store failed before the fix.

The second full rerun passed the S3 matrix, invalid-input quarantine, Celery
publication with retry (try 2) and replay, then ended ERROR at 812.8 s: the
existing 780 s work deadline expired while the recovery phase created its
second-generation `storage-admin`. One owned created container remained; its
attempt and owner labels were verified before removal, and owned containers
and networks are now zero. The fixture's retained attempt directory is kept as
failure evidence. The time limit was not raised, so independent restore
remains NOT_RUN for this Task.

Official pages re-read on 2026-11-04: Airflow DAGs and connections (3.3.2,
`quote_plus` for reserved characters), PostgreSQL logical decoding (unused
slots retain WAL and must be dropped), Confluent Schema Registry (8.4,
Community License) and dbt data tests.

### Full rehearsal optimization and independent recovery

A follow-up direct user request on 2026-11-04 asked to optimize the full Worker
rehearsal and resolve the recovery phase. A measurement-only run with the work
deadline extended to 1,500 s (repository source unchanged) passed in 1,059.7 s,
including recovery, so the earlier FAIL was time budget, not behavior. Phase
totals were dominated by recover 425.8 s, `initialize_airflow` 310.8 s, waits
236.7 s and DAG triggers 134.0 s: each `airflow` CLI call imports Airflow under
the fixture's 0.25-0.65 CPU caps, while production allows 2 CPUs per role. The
api, scheduler, processor and worker caps are now 1 CPU each (memory and pid
limits unchanged), raising the pinned aggregate from 2,250 to 4,800 milli-CPU.
The next measurement passed in 719.5 s with work ending at 683.7 s, inside the
unchanged 780 s work deadline; no time limit was raised.

The registered tests then ran unmodified with their original deadlines:
`AirflowNativeRehearsal` and `AirflowStoragePermissionRehearsal` ran 2 tests
OK in 889.3 s. Recovery restored metadata and DEV databases into empty physical
PostgreSQL 18.6 servers and objects into an empty SeaweedFS, read back body,
size, ContentType, user metadata and tags, and replayed the Worker run (PASS).
Owned containers, networks and attempt directories were zero afterwards. The
failed attempt directory of the 812.8 s run was moved into local custody with
its inode, owner and mode preserved before the reruns.

### Operating installation handoff to D12

The adapter fix is not yet operating: the production `airflow-scheduler`
`/opt/airflow/dags` (bind-backed by `${DEFAULT_WORKFLOW_DIR}/airflow/dags`) is
empty, so the Opsflow workload has never been installed in HOME. D12 owns the
first installation under an approved window, in this order, each step with its
own check: (1) back up `opsflow_dev`, the Airflow metadata database and the
`opsflow-dev` bucket listing; (2) apply SQL 001-008 to `opsflow_dev` as the
migrator role and verify `008_checks.sql`; (3) create the bucket and apply the
worker bucket policy, then run the permission canaries; (4) install `dags/` and
`workflow_lib/` at the reviewed commit into the DAG directory without editing
the image; (5) create the pool, keep the DAG paused, run one synthetic business
date, and confirm raw, validated, published and outbox rows plus quarantine of
an invalid input with `application/json`; (6) unpause only after that. Rollback
removes the installed files, keeps the backups, and drops nothing that existed
before. This Task performs none of these steps.

### T03 Kafka and CDC re-review

The same 2026-11-04 request asked to re-review and optimize the Kafka,
Debezium and Schema Registry path. Read-only HOME observation: the stack
(`kafka-1`, `kafka-connect`, `schema-registry`, `kafka-rest-proxy`, `kafbat-ui`,
`kafka-exporter`) has run since 2026-11-02 using about 1.36 GiB; Connect has
zero registered connectors; there are zero consumer groups; the declared
`application-logs` and `infra-events` topics hold no messages; DEV
`platform_dev`, the connector's source database, does not exist in HOME.
Leftovers of an earlier, unregistered connector remain: two `hyhome.app`
heartbeat topics (10,267 messages) and four Schema Registry subjects, while the
current prefix is `hyhome.platform`. Broker CLI tools inside `kafka-1` fail
unless `KAFKA_JMX_OPTS` and `KAFKA_OPTS` are unset first, exactly as the
healthcheck already does. Stopping the idle stack or deleting the leftovers is
an operating change awaiting the owner; this Task performs neither.

The source connector is single-broker correct (replication factor 1,
`topic.creation.default.*`, publication auto-create disabled, `pgoutput`,
heartbeat). Its two `schema.history.internal.kafka.*` keys were removed: they
apply to MySQL-family connectors, and the Debezium 3.7 PostgreSQL property
reference lists none. Static Compose and DEV-boundary suites pass. The
isolated `CdcStreamRehearsalTests` ran twice and both ended ERROR in setup
(433.1 s and 407.1 s): under host load 13-18 on 12 CPUs, the TimescaleDB
image's post-init `pg_ctl stop` timed out before PostgreSQL became ready, so
no connector was registered and the runs say nothing about the connector
change. The declared Debezium 3.6.3 image trails 3.7 and is a D09 image
candidate.

### T03 owner-approved stop and leftover removal

After a re-review, the owner answered "정지와 삭제를 둘 다 실행" on
2026-11-04. The re-review found that `messaging` is not in the POL-0078 HOME
selection, so the stack had been started on demand and stopping it restores the
HOME default without a profile or policy change; Kafka has no `absent(up)`
rule and `KafkaBrokerDown` needs the exporter metric, so no false alert follows.
Immediately before acting, Connect still had zero connectors and the broker
zero consumer groups. The four `hyhome.app` heartbeat subjects were soft- then
hard-deleted (each returned version `[1]`; subjects now `[]`), and the topics
`__debezium-heartbeat.hyhome.app` and `hyhome.app.debezium_heartbeat.heartbeat`
were deleted; `application-logs`, `infra-events` and the internal topics remain.
`docker compose --profile messaging stop` then stopped `kafbat-ui`,
`kafka-rest-proxy`, `kafka-connect`, `schema-registry`, `kafka-exporter` and
`kafka-1` (exit 143); `kafka-init` was not running. The four Kafka and Connect
volumes are unchanged, so a later start resumes the same state. Prometheus
shows no Kafka alert; its five firing alerts (backup staleness, OpenBao scrape
and agent authentication, missing gatus and pyroscope targets) predate this
action and belong to their owners.

### T03 CDC rehearsal setup failure diagnosis

A follow-up owner request on 2026-11-05 ("실패 검토후 진행") reviewed the CDC
rehearsal failure. A third run at host load about 5 failed the same way, so
the earlier host-load explanation was wrong. Standalone, the TimescaleDB image
stops its temporary init server in about 9 s, of which the shutdown checkpoint
takes 3.9 s; disabling telemetry made no difference. The fixture started
PostgreSQL together with Kafka, Schema Registry and Connect, and under their
start-up I/O that stop overran `pg_ctl`'s 60 s wait ("server does not shut
down"), so the container exited. The fixture now starts PostgreSQL first and
waits for the final server on TCP, which the temporary socket-only server never
answers, before starting the JVM services; no time limit changed. The rerun
passed both tests in 345.1 s: stream decode, schema evolution and resume, and
heartbeat writes advancing the slot, with the connector that no longer carries
schema-history keys. Owned residue was zero.

### T03 D09 Debezium 3.7.0.Final source pin

The owner decided on 2026-11-06 ("D09 Debezium 3.7 — 정적 변경만 PR") to raise the
declared Debezium image as a static change only. The `kafka-connect` build now
takes the PostgreSQL connector plugin from `quay.io/debezium/connect:3.7.0.Final`
(was `3.6.3.Final`) and the local image tag is
`hy-home/kafka-connect:8.3.2-debezium-3.7.0` (was `...-3.6.3`); the Confluent
base `cp-kafka-connect:8.3.2` is unchanged. A read-only quay.io tag lookup on
2026-11-06 shows `3.7.0.Final` as the only stable 3.7 tag (index digest
`sha256:9716a72bce5313186d7528cf5ea00f3e2d1a0a71ba84156d38417d0262cf3599`); the
Dockerfile pins by tag, as before, so no digest is added. The 3.7 release
summary of 2026-09-29 lists breaking changes only for the Oracle, JDBC sink and
Cassandra connectors, none for PostgreSQL, so `postgres-connector.json` is
unchanged. The tech-stack projection, the Compose tag, the Dockerfile and the
security-updates ledger and build-input records follow the pin; the observed
running 3.6.3 image and the dated lookups stay as history. Image build, plugin
loading, snapshot/offset/restart/recovery on the existing slot, scan and HOME
recreation are NOT_RUN: the messaging stack is stopped and this Task starts
nothing.

### T03 messaging restart review (2026-11-09)

The owner asked on 2026-11-09 to review and optimize `kafka-broker`,
`kafka-exporter`, `kafka-connect` and `schema-registry`, then run them.
cAdvisor kept no named series for the stack from before the 2026-11-04 stop,
so the changes rest on static review and direct measurement:

- **Broker healthcheck.** `kafka-broker-api-versions` starts a JVM each run;
  two throwaway runs of the pinned image took 2.4 and 2.7 CPU-seconds, about
  0.16 CPU at the 15 s interval. The interval is now 60 s with a 5 s
  `start_interval`, so dependants do not wait longer at start.
- **JMX remote.** The unauthenticated RMI port 9101 (host `127.0.0.1:19101`)
  had no consumer in the repository; the jmx_exporter agent on 9404 serves
  the metrics. The JMX options, variables and port are removed.
- **Connect heap.** The image defaults to `-Xms256M -Xmx2G`, equal to the 2g
  limit, which leaves no room off-heap. It is now `-Xms256M -Xmx1G`.
- **Connect image.** Only `...-debezium-3.6.3` exists locally; the declared
  3.7.0 image must be built before Connect can start.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Issued P04 baseline and documentation leases | 66 | W71 | `git status --short`; `git rev-parse HEAD`; public file SHA-256 and governing source readback | Clean HEAD 6853286dbd73851a6419f7fb5457c53720ba6d98 | PASS | Inputs and Authorization; Baseline and issued writer leases; local doc-baseline.json at 2026-11-02T07:46:20Z | required | - |
| URI behavior RED | 67 | W72 | P04 URI behavior regression | Missing helper baseline | FAIL | Three expected missing-helper failures before implementation; writer receipt uri-receipt.json | optional | - |
| URI behavior GREEN | 67 | W72 | P04 URI behavior regression | Helper 62b61910cb386d1ffbe817832c8216e3d40f8ee534c801889b125e63855744e7; tests fccbff797b6893e421f5583037f56335c5c050c02e2916050260d6f67b8b65ed | PASS | Writer 24 tests in 0.142s, line coverage 154/155 (99.355%); semantic P02 port-contract case 1 PASS in 4.565s; Ruff/format/diff PASS. Line coverage is not branch coverage. | required | URI behavior RED |
| Initial URI independent source/security review | 67 | W72 | Independent URI code/security review | Same exact helper/test GREEN packet | PASS | Reviewer /root/p04_infra: APPROVED, no findings; independent synthetic host suite 24 PASS in 0.085s. Later closed-pipe process review supersedes this initial approval for current acceptance. Actual mount readability, provider behavior and new image remain separate. | optional | - |
| URI closed-pipe review correction required | 67 | W72 | Independent URI code/security review | Prior helper 62b61910cb386d1ffbe817832c8216e3d40f8ee534c801889b125e63855744e7 | FAIL | Fresh-process closed-stdout probe exposes CPython shutdown reflush: process exit120 and extra BrokenPipeError stderr after main returns1. Synthetic only, no value leak; actual-process regression, fix and exact re-review required before current approval. | required | - |
| URI closed-pipe corrective re-review | 67 | W72 | Independent URI code/security review | Final helper 27a7501cfeb112ba92f2d6a1e66ab69c9f87a32299e5ffe80cea2afe4010f309; tests 523497ffe459bcf54aee9de84686296e38b304d0eaacdc92dfc332e849d6b656 | PASS | Fresh-process exit120 RED resolved to exit1 with exactly the fixed error. Writer 25 PASS in 0.113s; final trace 25 PASS in 0.170s, 159/167 lines (95.210%). Independent /root/p04_infra APPROVED: 25 PASS in 0.100s. Final P02 semantic port case 1 PASS in 4.206s. URI receipt retains the initial packet separately. | required | URI closed-pipe review correction required |
| Pipeline behavior RED | 67 | W72 | P04 pipeline behavior regression | Prior parser/adapter without quarantine or data_version | FAIL | Manifest selected cases failed on missing quarantine/data_version; four adapter cases errored on missing method. Expected RED, not acceptance. | optional | - |
| Pipeline behavior GREEN | 67 | W72 | P04 pipeline behavior regression | Writer-frozen source and pipeline-coverage.json receipt | PASS | /root/p04_pipeline: final host 80 PASS in 13.519s; stdlib trace full manifest 213/216 (98.61%), adapters 484/507 (95.46%); new lines 32/33 (96.97%) and 31/31 (100%). Line coverage only; no SQL runtime claim. Initial eight namespace UID errors resolved on actual host without weakening guards. | required | Pipeline behavior RED |
| Airflow source render and IaC review | 67 | W72 | Public synthetic Compose render and independent IaC review | Compose 621bcf244286dc784c0004ef2b51a3af8fca93b1b483f28fe1340cd54df3fc9b; Dockerfile 3cf83481bbfb8ea5a2e0f1f016075b69cd429b08655cb10acf5b4c53ef61bff5 | PASS | /root/p04_infra: listener suite 5 PASS in 4.420s; /root/p04_uri independent review APPROVED, seven roles across shared/dedicated synthetic models with 21 command links each. No build, actual mount or HOME operation. | required | - |
| Pipeline independent code/security/SQL source review | 67 | W72 | Independent pipeline source review | manifest df479fb44437052bcb55a6b90703f8d803c242a93801501e1105a8bb408d71d1; adapters 60ef4a0841bb1cc13918902b1b302abcbcf17bcdadf7b0a62dacc021fb2e05ff; SQL005 85eb63d22f2967ac84996f561a14ca3433e429eaf55a597d294478e21dfe00c2; SQL006 38eb6b22e99e573c40cd1fa920af7a3cc5945d0ce0a53e9d2872983834c0ef76 | PASS | /root/p04_infra APPROVED, no findings; independent host 63 PASS in 0.709s; prior001–004 byte-identical, appended view preserves grants and notification functions. Actual SQL/restore runtime separate. | required | - |
| Living document source review | 69 | W74 | Independent living-document review | Exact seven-file living-doc-reviewed-v1.json packet | PASS | /root/p04_uri APPROVED; all seven original fingerprints match source. Quarantine/version/v4/read-only checks, historical scopes and Flink registration-probe limits corroborated. The two later wording changes explicitly limit P05 NOT_RUN to this P04/version4 scope; narrow re-review APPROVED against living-doc-current.json with the other five files unchanged. | required | - |
| Native source prelaunch correction required | 67 | W72 | Native source review | Prelaunch native packet, no actual attempt consumed | FAIL | Review requires safe administrator failure capture and fixes for snapshot argv E2BIG with accepted 2x64KiB input and aggregate artifact bounds. Native launch is held; correction and exact re-review pending. | required | - |
| Native source corrective re-review | 67 | W72 | Native source review | Data helper 115061d5208de5dc2e7a5b0e0df093a69af3482b9e86109f2735d6dbea5eaf74; scenario a1f34a0abf3de442451e9171b1bbd60905afecc8024944db5c9840a2bc9c17dd; guards 7aa09b4d6aaad2c19fe36a19163b2548d1c0994d817dc0db2d3bcf4cae759392; fixture a1876d4983ec08e38dd4e16394db4d28db4a686079201333e02f61189b56ca29; evidence 0320961a085dd1c48c00d859e2aad7c1953b0833440faa0d22cbac2e95b9b826 | PASS | /root/p04_pipeline independently APPROVED code/security source; 51 total, 50 PASS and one native skip in 0.743s. Data tests fab0fd4bb8f467e12f8b5433bf64d979b3f8c90e94688814495d411bc2d51f84, rehearsal 89c5ce39d7561fd8efcfaa4afb2f804afc5185c71df6e72b7296c83d86f6fe53, evidence tests eefcbed606b22392732eb3545ee19e19cd2a2cc40e2a8fdf445d8e27f71a6dd1. Administrator failure is redacted while preserving rc7; restore uses static argv plus bounded stdin. Fixture limits: at most 16 objects, 1MiB each and 2MiB serialized aggregate; this does not prove restore of a maximum-size input/validated pair. Actual native outcome separate. | required | Native source prelaunch correction required |
| Recovery snapshot preflight RED | 67 | W72 | Recovery snapshot preflight | Stateful synthetic scenario test with malformed object snapshot | FAIL | The meaningful control-flow test exposed generation1 teardown before complete snapshot validation. No real resources were changed by this test. Source author must validate the entire bounded recovery input before teardown/start of generation2; fix, GREEN and independent re-review remain separate from the full native S3 failure. | required | - |
| Recovery snapshot preflight GREEN | 67 | W72 | Recovery snapshot preflight | Corrective source data helper 2d7688c6e0560672827e26faf4e50639493bccb1075f91eaeadeba0f81720e9d; scenario b4aada9cdc9b1c0a041b273f9488e63ae76a68f4a1326cd77e2953db4b4f8791 before style-only finalization | PASS | Whole bounded snapshot validation now precedes generation1 teardown and generation2 start. /root/p04_pipeline corrective source review APPROVED: 53 PASS, two native skips in 0.784s. This closes the synthetic preflight ordering defect only, not actual Worker/restore acceptance. Final style fingerprints are recorded with the final packet. | required | Recovery snapshot preflight RED |
| First native bounded foundation observations | 67 | W72 | Owned native phase receipts | First full attempt only; frozen cached image and reviewed SQL005 source | PASS | Actual probe reported core3.3.2/provider3.24.1/UID50000. The SQL005 apply control path completed after the witnessed version3 data_version rejection; Airflow DB migration, pool/DAG registration and unpause completed. SQL006 was NOT_RUN because it follows publication. These phase observations do not establish a Worker business result, current end-to-end publication or recovery. | optional | - |
| First owned native Worker and restore rehearsal | 67 | W72 | Owned native Worker and restore rehearsal | First P04 owned cached-image attempt after corrected source review | FAIL | Actual duration 582.770s; SeaweedFS static-identity principal was 000000000000 while the fixture deny policy named 111111111111. Stopped at S3 permission before publication, input quarantine and recovery; those phases remain NOT_RUN. Final cleanup reported FAIL with the original evidence retained while independently confirmed owned containers/networks were zero. Preserve both facts. The exact same-filesystem custody rename at 2026-11-02T08:35:37Z preserved identity bindings and modes; native-custody-event.json (0600) records it. A 0.001-second retained-path preflight denial started no resources and did not consume the narrow probe budget. One bounded three-role cached-S3 probe is separate and cannot resolve this full Worker/restore FAIL. | required | - |
| Narrow owned S3 permission retry | 67 | W72 | Owned S3 permission diagnostic | The one authorized cached-S3 retry after principal/source correction; three owned roles | FAIL | ERROR after 190.468s: 180-second work deadline reached during administrator permission canaries, before old/new action matrices. No corrected-policy runtime PASS, Worker publication, input quarantine or independent restore follows. The 0.001s admission denial is preserved separately; no third runtime is performed. Value-free receipt: native-storage-retry-resumed.log. | required | - |
| D04 narrow S3 permission rerun | 67 | W72 | Owned S3 permission diagnostic | storage-admin 0.25 CPU, cached images | PASS | 125.5 s; old principal delete 204, corrected matrix PASS; residue 0 | required | Narrow owned S3 permission retry |
| D04 full Worker rerun | 67 | W72 | Owned native Worker and restore rehearsal | Both D04 fixes, unchanged 780 s deadline | FAIL | S3 matrix, quarantine, Celery publication retry/replay PASS; recovery stopped at the 780 s deadline (812.8 s); owned residue removed to 0; restore NOT_RUN | required | - |
| Optimized full Worker and restore rehearsal | 67 | W72 | Owned native Worker and restore rehearsal | Airflow roles 1 CPU, unchanged 780 s/900 s deadlines, registered test unmodified | PASS | 2 tests OK in 889.3 s with the narrow S3 test; recovery PASS (empty PG18.6 metadata/DEV, empty SeaweedFS, metadata/tags read back, Worker replay); measured 719.5 s, work ended 683.7 s; residue 0 | required | First owned native Worker and restore rehearsal |
| Narrow retry cleanup postcondition | 67 | W72 | Owned S3 retry cleanup | Exact retry probe, three roles and two networks | PASS | Confirmed absent; retained lists zero and attempt directory null. This is cleanup only, not data recovery or closure of the first full native FAIL. | optional | - |
| P04 local implementation and review | 67 | W72 | Approved source, RED/GREEN, coverage and independent review | Final owner packets and DATA-0096 file fingerprints | PASS | URI, pipeline, IaC, native source and corrective scenario QA are independently reviewed. Native data 13 unit PASS, 289/300 lines (96.33%); scenario QA 11 PASS, 528/538 lines (98.1413%), independent 11 PASS in 0.115s. Python controller line coverage is not branch coverage or proof that embedded container programs/DB/IAM/queue executed. Full native and narrow timeout remain separate failed evidence. | required | - |
| CDC current-consumer reconciliation | 68 | W73 | Tracked connector/provisioner, ADR and historical receipt readback | Existing platform_dev path; no live query or registration | PASS | Preserved consumer and acceptance scopes; current CDC is SOURCE_READY and Opsflow adoption is deferred, not a new runtime PASS | required | - |
| T03 HOME stream observation | 68 | W73 | Read-only HOME Connect, topic, consumer-group and subject queries | Running HOME stack, 2026-11-04 | PASS | 0 connectors, 0 consumer groups, declared topics 0 messages, ~1.36 GiB; leftover `hyhome.app` topics/subjects recorded; no state changed | required | - |
| T03 isolated CDC stream rehearsal | 68 | W73 | `CdcStreamRehearsalTests` with HYHOME_CDC_REHEARSAL=1 | Connector without schema-history keys; host load 13-18 | FAIL | Two setup ERRORs (433.1 s, 407.1 s): TimescaleDB post-init stop timed out before readiness; no connector registered; owned residue 0 | required | - |
| T03 isolated CDC stream rehearsal rerun | 68 | W73 | `CdcStreamRehearsalTests` with HYHOME_CDC_REHEARSAL=1 | PostgreSQL started and ready before the JVM services; connector without schema-history keys | PASS | 2 tests OK in 345.1 s: decode/evolve/resume and heartbeat slot advance; residue 0 | required | T03 isolated CDC stream rehearsal |
| T03 owner-approved stop and cleanup | 68 | W73 | HOME leftover deletion and messaging stop | Owner approval 2026-11-04; 0 connectors, 0 groups rechecked | PASS | 4 subjects hard-deleted, 2 topics deleted, 6 services stopped (exit 143), volumes unchanged, no Kafka alert | required | - |
| Quality publication regressions | 69 | W74 | Invalid/partial/no-publication unit and adapter tests | Current reviewed manifest/adapter packet and synthetic inputs | PASS | Included in the actual 80-case focused suite: failed schema/partition and failed quarantine never reach DB/outbox; source driver boundaries are synthetic. Actual native publication/quarantine remain NOT_RUN. | required | - |
| Experiment input decision | 70 | W75 | Direct user scope choice and missing-input record | No approved dataset/version/time field/target/baseline/owner | PASS | User selected experiment-input deferral during P04 planning; no claim about private experiment absence | required | - |
| Iceberg current-workload reconciliation | 71 | W76 | Current optional source, ADR-0039 and preserved owner acceptance readback | Existing optional platform; no runtime change | PASS | Preserved consumer and acceptance scopes; DATA-0096 research records Iceberg 1.11.0 maintenance separately from latest 1.12.0 | required | - |
| Combined direct local QA | 67 | W72 | Final combined Docker-free regressions | Final pipeline, URI, native data and scenario QA packets | PASS | /root/p03_docs_impl:129 PASS in0.910s (80+25+13+11). This does not resolve full-native FAIL582.770s or narrow ERROR190.468s. | required | - |
| Current public inventory and comparison | 66 | W71 | Existing inventory scan/validate/compare | P04 source freeze with explicit new public paths; no global render; current branch codex/p04-opsflow-data-path | PASS | First current scan counted41401 accessible entries,2294 text review denominator,7 explicit complete and54 partial reviews; discovery render0/17, operation0/112 and restore0/112. Earlier203 expanded render combinations remain dated history, not this unexpanded discovery denominator. Metadata validation PASS; comparison to preserved prior P03 observation:9 added,25 changed,0 removed and25 invalidated reviews; no connection-row delta. It is not a clean-start full-body or operational acceptance. Final Task evidence is followed by a safe metadata refresh. | required | - |
| Local document metadata and links | 66 | W71 | Registered changed metadata and alignment links | Contiguous Task Evidence table and frozen local document packet | PASS | CI writer ran changed metadata and links alignment sequentially; both exited0 before the catalog-only projection correction. No hosted CI or operating result. | required | - |
| Operations catalog drift | 66 | W71 | Registered local operations catalog | P04 helper environment migration; prior canonical projection | FAIL | Seven Airflow Env cells were stale. Other research prose and service cells were unaffected. This required the existing single CI projection writer, not manual source duplication. | required | - |
| Operations catalog projection correction | 66 | W71 | Registered local operations catalog | Canonical m0021 prehash0a870fd75457a2249e8b14058b0b5b090d09f456aa8599e2d380a64818a528a7; final9952a7485243ac9e41b4efd3e9d456d7dcf7e0081e83aaa3c03c3c387d3a1f70 | PASS | /root/p03_docs_impl regenerated exactly seven Env cells through the canonical renderer; markers/prose/other cells unchanged. Catalog and diff check PASS; /root/p04_uri independent narrow review APPROVED. DATA updates only affected source/ownership/partial-review metadata. | required | Operations catalog drift |
| Initial local staged wrapper | 67 | W72 | Registered local staged validation | Initial staged P04 packet before formatting/fixture annotations | FAIL | Normal wrapper reported markdownlint MD012 at workload README line104. Two synthetic test literals also triggered the installed secret scanner. This failure is retained until the actual normal wrapper retry succeeds; scoped corrections alone do not resolve it. | required | - |
| Synthetic fixture scanner finding | 67 | W72 | Scoped synthetic fixture leak scan | Prior URI/P02 test literals in protected disposable fixtures; no deployed credential | FAIL | Two synthetic-only fixture lines triggered scanner detection; no actual secret exposure or credential rotation is inferred. | required | - |
| Synthetic fixture annotation verification | 67 | W72 | Scoped synthetic fixture leak scan | URI test dcc5345a4f19975c2d62ed83790202d5bb763c44f1178bf902939264ddb798d2; P02 test 76783c0e6a1bf3079d63237182a8be2fc3f9c8d6d08637f0d27b3a269b349e5d | PASS | Only two supported inline allow comments explain synthetic fixtures; installed gitleaks8.30.0 scans and Ruff PASS. Independent /root/p04_pipeline APPROVED AST(index)==AST(worktree); no global allowlist, obfuscation or behavior change. Earlier129-case execution is reused on identical executable AST, not recorded as a new run. README MD012 was corrected by removing one blank line only. Full staged wrapper remains separately pending. | required | Synthetic fixture scanner finding |
| Final independent document review | 66 | W71 | Independent current document and curated-data review | Exact13-path final-doc-source-packet at2026-11-02T09:00:08Z | PASS | /root/p04_uri APPROVED: contiguous typed Evidence, same-scope Resolutions, truthful unresolved native FAIL/ERROR, actual whole-body reader attribution and exact writer/handoff hashes. Generated inventory review covers P04 curation plus CLI consistency, not semantic review of every row. Later whitespace/comments/evidence-only changes reuse unaffected proof. | required | - |
| Normal local staged wrapper retry | 67 | W72 | Registered local staged validation | Exact35 staged public paths after one README blank-line correction and two AST-identical synthetic fixture comments | PASS | Actual normal local-staged hooks all PASS, including markdownlint, gitleaks, Ruff and Dockerfile checks; no hook skip or broad scan bypass. Cached diff check PASS. This closes only the earlier staged-wrapper failure, not native execution or hosted CI. | required | Initial local staged wrapper |
| Registry-backed document integration | 66 | W71 | Registered metadata, links, catalog and corpus lifecycle | Current registry/build profiles and corrected local document/projection packet | PASS | Actual changed metadata, alignment links and operations catalog exit0; corpus lifecycle loaded Stage99 Registry/build profiles and passed. Independent narrow13-path document/curation re-review APPROVED after formatting/comment metadata refresh. Historical unexecuted operating/remote axes remain separate. | required | - |
| D09 Debezium 3.7.0.Final source pin | 68 | W73 | Read-only quay.io tag lookup, 3.7 release-summary breaking-change readback and edit of Dockerfile.connect, kafka Compose tag, tech-stack projection and security-updates ledger/build-input records | Owner decision 2026-11-06 (static change only); `quay.io/debezium/connect:3.6.3.Final` to `3.7.0.Final`; `hy-home/kafka-connect:8.3.2-debezium-3.6.3` to `8.3.2-debezium-3.7.0` | PASS | Index digest sha256:9716a72bce5313186d7528cf5ea00f3e2d1a0a71ba84156d38417d0262cf3599; no PostgreSQL breaking change listed, connector JSON unchanged. Compose config, supply-chain policy, operations catalog, hardening, Compose baseline/DEV-boundary/wiring/tech-stack suites and the update-ledger gates pass. Build, plugin loading, snapshot/offset/recovery, scan and HOME recreation NOT_RUN; the CDC stream rehearsal was not re-run (it starts containers) and the earlier PASS covers 3.6.3 only. | required | - |
| Messaging restart review | 68 | W73 | Throwaway healthcheck JVM timing; repo search for JMX consumers; image heap default read | `cp-kafka:8.3.2`, Connect 3.6.3 image | PASS | 2.4-2.7 CPU-s per check; no JMX 9101 consumer; default `-Xmx2G` equals the limit. | required | - |
| Graphify AST freshness | 66 | W71 | graphify update . | Final executable source; AST-only, no API cost | PASS | Actual command exited0; no graph files changed. Parser limits remain:18 SQL and9 HCL inputs lack tree-sitter dependencies, and5 files yielded no symbols. This is bounded AST refresh, not whole-source semantic coverage or SQL/runtime validation. No parser dependency was installed to manufacture success. | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 66 | accepted | Issued P04 baseline and documentation leases, Current public inventory and comparison, Local document metadata and links, Operations catalog projection correction, Final independent document review, Registry-backed document integration, Graphify AST freshness | REUSE_ACCEPTED for bounded existing ownership with current affected source regressions; operating roles and restore remain independently unaccepted. Owner @buenhyden accepted on 2026-11-06. | SPEC-0212 TSK-0043 |
| 67 | pending | P04 local implementation and review, D04 narrow S3 permission rerun, Optimized full Worker and restore rehearsal | SOURCE_READY: S3 matrix, input quarantine, Celery publication retry/replay and independent recovery pass in the isolated native rehearsal within the unchanged deadline; HOME installation is NOT_RUN and handed to D12. | SPEC-0212 TSK-0043 |
| 68 | accepted | CDC current-consumer reconciliation, T03 HOME stream observation, T03 isolated CDC stream rehearsal rerun, T03 owner-approved stop and cleanup | SOURCE_READY; HOME stack measured idle with no consumer; the isolated CDC stream rehearsal passes on the Debezium 3.6.3 image (the 3.7.0.Final build, plugin loading and rehearsal are NOT_RUN); the idle stack is stopped and leftovers removed with owner approval. Owner @buenhyden accepted on 2026-11-06. | SPEC-0212 TSK-0043 |
| 69 | pending | Quality publication regressions | SOURCE_READY: current unit/adapter quality blocking is evidenced; actual Worker publication remains residual. | SPEC-0212 TSK-0043 |
| 70 | pending | Experiment input decision | BLOCKED on actual inputs by user choice; no experiment is invented. | SPEC-0212 TSK-0043 |
| 71 | pending | Iceberg current-workload reconciliation | REUSE_ACCEPTED only for the evidenced optional platform; workload adoption is deferred. | SPEC-0212 TSK-0043 |

## Review and Completion

All authorized source changes and independent code/security/SQL/IaC/QA reviews
are complete. Current P04.02 is TEST_RESIDUAL, not full feature acceptance:
the full native failure and narrow timeout remain visible, and the corrected
permission matrices, actual Worker business result and independent restore are
unaccepted. No third runtime follows the bounded retry rule. A future owner
first measures initialization phases under unchanged safety/resource boundaries;
50m-CPU/Python cold-start cost is a hypothesis, not a measured root cause or
performance improvement. There is no invented operating-permission blocker.

Independent document review, registered local gates, bounded graphify AST
freshness and exact inventory/diff comparison are evidenced above. The final
changes after those receipts are evidence-only Task/data fingerprints; the
controller re-stages them, checks the exact staged diff and uses the normal
staged wrapper/commit hooks again. No commit SHA is invented or embedded as a
self-reference; the controller records the actual post-commit receipt locally.
Remote CI/integration, HOME operation, credential rotation, HOME restore and
P12 acceptance remain NOT_RUN. The final inventory
keeps global render observations separate from the two actual synthetic
Airflow render cases and preserves earlier dated receipts as history.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Workspace inventory](../../../90.references/data/0096-workspace-inventory/README.md)
- [Historical P04 Task](../../0204-service-integration-security-and-operations/tasks/tsk-0012-p04-airflow-manifest-pipeline.md)
- [Current P02 listener contracts](tsk-0041-service-connection-contracts.md)
- [Current P03 model/Runner contracts](tsk-0042-models-runners-wiki.md)
