---
title: "Development Data and LAB Source Integration Task"
version: "0.1.1"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0202-TSK-0001"
parent_ids:
- "SPEC-0202"
- "SPEC-0202-PLAN-0001"
created: "2026-10-02"
---

# Development Data and LAB Source Integration Task

## Objective

Implement and verify Prompt 02 authored source under SPEC-0202 without HOME
or real-data action. This Task is the serial owner of root/env/Registry,
new dev DB/Valkey, affected dbt/CDC source, backup/migration tooling and LAB
entrypoints. Independent reviewers are read-only. The owner deferred
SPEC-0201 W7.4 recovery; that deferral is not a test PASS.

## Inputs

- Owner's Prompt 02 implementation request and later instruction to allow
  its source work while deferring operational recovery.
- SPEC-0201 W7.1-W7.3 accepted scoped evidence; W7.4 NOT_RUN; W7.5 requires
  current implementation-time digest/platform/license/compatibility review.
- Main `e2c841eb9ef5086d0fbd6cc2ccd43ea35d89e26d`, current branch,
  official references and exact Task-owned file ledger below.

## Work Log

| Unit | State | Owned path and contract |
| --- | --- | --- |
| W1 | SOURCE_REVIEWED | SPEC/Plan/Task, docs/03.specs/README.md, docs/99.templates/registry.json; current official image and current source map. Root/env/projection are reserved for this Task only. |
| W2 | SOURCE_IMPLEMENTED / STATIC_PASS | New `infra/04-data/dev-db/docker-compose.yml`, root README, `pg/{Dockerfile,backup/,provision/,README.md}` and `tests/validation/test_dev_pg_provision.py`; new `infra/04-data/dev-db/valkey/{config/,scripts/,README.md}` and `tests/validation/test_dev_valkey_acl.py`. Existing mng-db init remains management-only. W2 workers own only their new engine trees/tests; root owns root/env/secrets. |
| W3 | SOURCE_IMPLEMENTED / STATIC_PASS | Existing infra/12-analytics/dbt/**, infra/05-messaging/kafka/**, tests/validation/test_mng_pg_init_sql.py and test_compose_baseline_gates.py; source transition with no live cutover. |
| W4 | SOURCE_IMPLEMENTED / RUNTIME_NOT_RUN | New `infra/04-data/influxdb/migration/validate_mapping.py`, `tests/validation/test_influx_mapping.py`, dev-pg backup files under `infra/04-data/dev-db/`, and updates to `docs/05.operations/policies/0021-backup-and-restore.md` and `docs/05.operations/runbooks/0021-backup-and-restore.md`. Owner reports InfluxDB empty on 2026-10-02; live count/writer inspection, export/import and restore remain NOT_RUN. |
| W5 | SOURCE_IMPLEMENTED / STATIC_PASS | Standalone `labs/postgresql-ha.yml`, `labs/valkey-cluster.yml`, `labs/kafka-cluster.yml`, `labs/cassandra.yml`, `labs/couchdb.yml`, `labs/mongodb.yml`, `labs/opensearch-cluster.yml`, matching `labs/*.md` package documents; split `infra/05-messaging/kafka/docker-compose.yml` and `infra/04-data/opensearch/docker-compose.yml`; isolate `infra/04-data/postgresql-cluster/docker-compose.yml`, `valkey-cluster/docker-compose.yml`, `cassandra/docker-compose.yml`, `couchdb/docker-compose.yml`, `mongodb/docker-compose.yml` and their package READMEs. Revise root `docker-compose.yml`, `scripts/lib/document_governance/operations_catalog.py`, `tests/lib/document_governance/test_operations_catalog.py`, `docs/05.operations/policies/0078-compose-profile-vocabulary.md`, `docs/05.operations/guides/0019-opensearch.md`, `docs/05.operations/policies/0019-opensearch.md`, `docs/05.operations/runbooks/0019-opensearch.md` and focused Compose tests. Normal and LAB entrypoints must be disjoint and each dependency closure complete. No `up`, stop or volume reuse. |
| W6 | SOURCE_IMPLEMENTED / STATIC_PASS | `.env.example`, `labs/.env.example`, `.gitignore`, `secrets/README.md`, `secrets/SENSITIVE_ENV_VARS.md.example`, `docker-compose.yml`, `infra/tech-stack.versions.json` through `scripts/operations/sync-tech-stack-versions.sh`, `tests/validation/test_compose_baseline_gates.py`, `infra/04-data/dev-db/README.md`, `infra/04-data/dev-db/pg/README.md`, `infra/04-data/dev-db/valkey/README.md` and this Task's 03/04/06 handoff section. Root is sole writer of shared files; engine workers own their READMEs. |

## Verification Evidence

The owner reported on 2026-10-02 that InfluxDB stores no data; no live row count, measurement list or writer traffic was inspected. This is an attested no-data path, not completed export/import or deletion approval. Source discovery (read-only) confirms mng-pg app_db bootstrap, dbt provision
and runtime, Debezium provision/connector and cluster LAB consume
`SERVICE_POSTGRES_*`; Schema Registry is named by the Avro connector. No
business app consumes `app_db` and the owner reports it contains no data.
Source still declares technical dbt/CDC objects; their live contents were not read. The only named source-only technical target is
`hyhome-platform`/`platform_dev`/`app` for dbt and CDC; no external project DB
is inferred. Official Docker Hub on 2026-10-02 lists TimescaleDB Community
`2.30.2-pg18` with linux/amd64 manifest digest
`sha256:cdf97a4b5be91038b5c1be0ad304c5d5746132992e54f7dd26ec467a6d005755`
and index digest
`sha256:e72689191e1c977892c53d6f2c344dbc4a9657a867dc8cc1899229f9d3672b2e`;
its layer metadata declares PostgreSQL 18.6 and
`PGDATA=/var/lib/postgresql/18/docker`. These are registry source facts, not
a pulled-image, extension-load, pgBackRest-package or restore result. The
Community variant includes TSL terms; the `-oss` image differs in license and
may lack features. Recheck the selected registry digest immediately before
source pin and any later build. The new custom dev image recipe is
`infra/04-data/dev-db/pg/Dockerfile`, with pgBackRest pinned to a version
compatible with PostgreSQL 18. On 2026-10-02 the [Timescale image layers](https://hub.docker.com/layers/timescale/timescaledb/2.30.2-pg18/images/sha256-cdf97a4b5be91038b5c1be0ad304c5d5746132992e54f7dd26ec467a6d005755)
identify Alpine 3.23.6, and [Alpine v3.23 community x86_64](https://pkgs.alpinelinux.org/package/v3.23/community/x86_64/pgbackrest)
provides `pgbackrest=2.57.0-r0`. [pgBackRest release notes](https://pgbackrest.org/release.html)
state PostgreSQL 18 support began in 2.55.0. The Alpine package also depends
on distro `postgresql`; the custom image must prove PATH/binary/library
selection before use. Actual package installation, extension load and restore
are isolated execution NOT_RUN. The source-only technical fixture is
`hyhome-platform`/`platform_dev`/`app`, with new CDC publication
`hyhome_platform_publication`, slot `hyhome_platform_slot` and topic prefix
`hyhome.platform`. Old connector, slot, publication and topic are retained;
registration, offsets and live switch are separate approval gates. W7.3
capacity is a point-in-time snapshot; the SPEC gives the proposed dev CPU,
RAM, SHM, connection, WAL, data and repository bounds and host floors. LAB
admission needs its own later measurement.

| Acceptance criterion | Plan work unit | Source/static result | Runtime or remaining boundary |
| --- | --- | --- | --- |
| 1 | W1 | Dated official image, license, PG/pgBackRest and host snapshots recorded | Image build, extension load and package ABI NOT_RUN |
| 2 | W2 | New dev-pg/dev-valkey root fragment and separate data/secret paths; no 07/08 DB | HOME start NOT_RUN |
| 3 | W2 | Explicit manifest, role/DB markers and two lock scopes have static tests | Cross-project read/write/DDL and live concurrency NOT_RUN |
| 4 | W2 | Valkey ACL synthetic tests; UTC/unit/precision/NULL/duplicate/late-event contract; no unapproved hypertable or retention | Live ACL, hypertable/chunk/CAGG and retention tests NOT_RUN pending an approved project schema |
| 5 | W3 | mng init, dbt and CDC source transition and Schema Registry connector references statically checked | Connector registration, snapshot and offset/LSN cutover NOT_RUN |
| 6 | W4 | Owner-attested Influx no-data route; strict mapping validator and synthetic tests | Live source count/writer inventory, export/import and reconciliation NOT_RUN |
| 7 | W4 | Separate inert dev pgBackRest source and key reference | Backup, WAL archive, PITR and isolated restore NOT_RUN |
| 8 | W5 | Seven separate LAB Compose entrypoints and normal root all-profile static render PASS | LAB start/stop, old containers and volume operations NOT_RUN |
| 9 | W6 | Focused tests, candidate image projection, operations catalog, metadata and links pass; exact diff reviewed | Image build and container integrations NOT_RUN |
| 10 | W6 | GDE/POL/RUN-0100 and SPEC-0202 handoff name project, perf_db, backup/restore owners | 03 perf_db implementation and 04/06 external provision remain separate Tasks |

### Handoff contract

| Consumer Task | Input from this Task | Owned next output and gate |
| --- | --- | --- |
| Prompt 03 quality/performance | `dev-pg` endpoint and explicit project manifest schema v1; separate `perf_db` is reserved | 03 owns `perf_db` provision, per-`project_id` writer/reader/result-verdict grants, re-ingest/idempotency tests and k6/WireMock result schema; no raw performance samples in mng-pg |
| Prompt 04 common integration/operations | `project_id`, `environment`, explicit DB/owner/migrator/runtime/reader names, Valkey ACL user/prefix/secret references, `infra_ref` and schema version | 04 owns approved project registration, network/endpoints by connection location, secret issuance, backup/restore execution and HOME cutover; no app migration source in root |
| Prompt 06 external project contract | Versioned manifest fields plus `platform_dev` fixture example and UTC/precision/late-event rules | 06 owns external Project-Template workspace migration, application E2E and ownership of object references, telemetry and rollback; 07/08 remain separate planning-only products |

No handoff authorizes runtime provisioning, issuance of a credential, or a
new 07/08 database. Names are explicit metadata, never derived by shell
concatenation.

### Source verification record (2026-10-03)

| Command / check | Exit | Evidence and limit |
| --- | ---: | --- |
| `python3 -m unittest -q tests.validation.test_secret_metadata_sync tests.validation.test_compose_baseline_gates tests.validation.test_dev_data_boundary tests.validation.test_dev_pg_provision tests.validation.test_dev_valkey_acl tests.validation.test_influx_mapping tests.validation.test_lab_credential_argv tests.validation.test_mng_pg_init_sql tests.validation.test_infra_tier_layout` | 0 | 169 tests OK, 23 opt-in/runtime skips |
| `bash scripts/validation/validate-docker-compose.sh` | 0 | 66 selections, 321 summed service selections, HOME 45; static render only |
| Seven `docker compose --env-file labs/.env.example -f labs/<name>.yml --profile '*' config --quiet` with synthetic LAB paths/ID | 0 each | PostgreSQL HA, Valkey, Cassandra, CouchDB, MongoDB, Kafka, OpenSearch after final key/path rename; parse/selection only |
| `docker compose --env-file .env.example --profile dev-data config --quiet`; same with `--profile '*'` | 0 each | Root static graph, LAB absent; all-profile render rechecked after identity/CIDR variable renames |
| `python3 scripts/validation/check-operations-catalog.py` with disposable candidate Git index | 0 | Profile and service inventory PASS |
| `bash scripts/operations/sync-tech-stack-versions.sh --check` with disposable candidate Git index | 0 | 91 Compose image repositories in sync |
| `python3 -m unittest tests.validation.test_tech_stack_version_contract.TechStackSynchronizationTests` and `TechStackVersionContractTests` | 0 each | 25 and 19 tests OK in separate index scopes |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref e2c841eb9ef5086d0fbd6cc2ccd43ea35d89e26d` with disposable candidate index | 0 | 66 selected, 0 violations on complete secrets/env inventory update |
| `python3 scripts/validation/check-document-links.py --mode all` | 0 | 0 failures, one pre-existing archive warning after final Task update |
| `bash scripts/operations/gen-secrets.sh --sync-metadata-prune-check` (earlier candidate snapshot) | 0 | 138/138 public/private registry rows at that snapshot; later root/LAB split and PG-020 metadata changed, so this is historical evidence only |
| `git diff --check` | 0 | Whitespace only; no runtime evidence |
| `python3 -m unittest -q tests.validation.test_secret_metadata_sync` | 0 | 39 synthetic metadata/secret-domain tests (the first 38 were included in the earlier 168-test run), including LAB env 0600/prune and per-entrypoint grants |
| Key-only public/private inventory | 0 | LAB 39/39, no missing/extra/duplicates, private mode 0600; root public 219 and main private 229 unique keys (ten retained compatibility/legacy names); no values printed |
| `bash scripts/operations/gen-secrets.sh --sync-metadata` and `--sync-metadata-check` | 0 / 0 | Candidate private registry/root/LAB projections aligned, final `files_changed=0`; values and secret files untouched |
| Main ignored registry metadata projection | 0 | 138 IDs and non-value cells equal to candidate public registry; every private value cell preserved, mode 0600 |
| `git check-ignore -v` for ignored root/LAB env, private registry and protected backups | 0 | All private paths ignored; no private values printed |
| Complete path-only `secrets/` and env domain audit | 0 | Registry 138 IDs = 105 file paths + 33 env-only IDs; current owner checkout 85 matching credential files, 20 declared-unissued dev/LAB paths, 17 certificate/snapshot/custody artifacts (14 bind certificates, one host-only CA key, snapshot, custody); root/LAB public and private key sets disjoint |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | 0 | Final rerun: document governance 629 tests, repository integrity 163 tests, 66 Compose selections; initial run found five unregistered new test modules, fixed in the existing Compose suite and its contract test |
| `python3 -m unittest -q tests.validation.test_dev_pg_provision tests.validation.test_lab_credential_argv` | 0 | 15 tests after the two commit-hook false-positive source-string adjustments |
| `graphify update .` | NOT_RUN | CLI unavailable; ignored graph projection not refreshed |

Private state handling: current ignored `labs/.env` and its candidate example now
have 39 unique LAB-prefixed keys. Thirteen internal-port knobs were removed
because the images or HAProxy config do not consume overrides; the retained
LAB host ports, paths, identity and network keys are explicit. The prior private
LAB file was backed up under an ignored 0700 custody directory. The main private
root `.env` now has 229 unique keys, including the 219 candidate public keys
and ten compatibility/legacy keys that current main still consumes. Two earlier empty R2
assignments were removed while their later nonempty assignments were preserved;
four candidate dev defaults were added. The root administrator UI CIDR input
was renamed to `ADMIN_UI_ALLOWED_CIDRS` in candidate source; OpenSearch admin
and Grafana native OIDC identity inputs became `OPENSEARCH_ADMIN_USERNAME` and
`GRAFANA_OIDC_CLIENT_ID`. Current main keeps all three old names with same-value
new aliases until source landing.
The ignored root backup is mode 0600.
No value was printed. The main ignored `SENSITIVE_ENV_VARS.md` has the same 138
IDs, paths, dates and purposes as the candidate public registry; every value
cell was preserved and a 0600 backup kept. Ten former LAB credential files
remain in ignored `secrets/.retired/2026-10-02/`; newly declared dev and LAB
secret files are unissued. Only their source paths were reclassified under
`secrets/db/dev-pg/`, `secrets/db/dev-valkey/`, `secrets/backup/dev-pg/` and
`secrets/labs/opensearch-cluster/`. Active HOME secret paths were not moved.
`PG-020` remains a named legacy `app_db` cutover hold. Current main has not
landed the candidate source; its old public registry has 126 IDs while the
private registry now matches the candidate public 138 IDs. Do not run the old
main `gen-secrets --sync-metadata*` before source landing; it can restore old
rows or metadata. These private metadata updates do not start HOME services or
approve credential issuance. Ignored backups remain for cutover
review.

## Review Evidence

Independent source, security and governance reviews found and corrected graph,
identity, LAB image/secret argv, idempotent init, profile, version projection,
active-doc and catalog drift. Static acceptance does not prove runtime
privilege denial, extension/ACL behavior, image compatibility or restore;
each remains NOT_RUN. Inherited mng-valkey/mng-pg-init credential argv and
mng-pg-exporter superuser access remain P2 source risks for a separately
approved management-service hardening change.
SPEC-0201 governance review accepted W7.4 deferral only for Prompt 02 source
entry; it did not approve HOME recovery or data migration.

## Commit Ledger

Source commit `b867eb7d466000ed8d49f6a8eb6410f1db646268` on local branch
`feat/spec-0201-home-infra-diagnosis` contains 154 changed paths, based on
`e2c841eb9ef5086d0fbd6cc2ccd43ea35d89e26d`. The ECC pre-commit secret
scanner passed after two synthetic/SQL-string false positives were rewritten;
no hook was bypassed. This ledger update is a separate local documentation
commit. No push, PR or merge occurred. HOME activation, real restore and data
migration remain separate approval gates.

## Rulings

Use current repository validation owners. No new app DB for planning-only 07/08,
no management TimescaleDB, no perf sample storage in mng-pg. An empty
`app_db` business dataset is not an authorization to delete its technical
objects. A source declaration is not deployed state.

## Deferred Items

Docker build/up/restore, source-current backup verification, HOME service
change, real `app_db` or Influx migration, retention deletion, secret issuance,
remote mutation and LAB start are deferred pending their own preflight and
approval. Record each as NOT_RUN, not PASS.
