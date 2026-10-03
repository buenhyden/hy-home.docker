---
title: "Development Data and LAB Isolation Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0202"
parent_ids:
- "REQ-0027"
- "AD-0004"
- "AD-0031"
- "SPEC-0201"
created: "2026-10-02"
---

# Development Data and LAB Isolation Specification

## Overview

This package contracts Prompt 02 source integration after the accepted
SPEC-0201 diagnosis. It introduces a single TimescaleDB Community development
PostgreSQL and a single development Valkey, separates future project data
from management metadata, and makes stateful LAB entrypoints independent of
the normal root Compose model. The owner deferred SPEC-0201 W7.4 current
management-backup verification/restore on 2026-10-02. That deferral permits
source work here; it does not prove any new backup or authorize runtime change.

## Boundaries and Inputs

The inspected main and initial working baseline is
`e2c841eb9ef5086d0fbd6cc2ccd43ea35d89e26d` (2026-10-02). Recheck it
before editing and preserve other workers' changes. Read AGENTS/bootstrap,
provider, approval, quality, documentation and Git policy, plus SPEC-0201 and
this package's current Task. The user authorized Prompt 02 source work and
explicitly deferred later recovery work. No HOME deployment, stop/restart,
real data export/import/delete, credential issuance/rotation, remote push/PR,
DNS/firewall change, or retention policy activation follows from that approval.

Current management PostgreSQL contains no business-app data per owner
attestation and catalog corroboration; its heartbeat row and dbt view are
technical data. DBeaver reaches management PostgreSQL over SSH; its selected
database and observed `app_db` transaction origins are unknown. Do not remove
an existing database, slot, publication, view, role, or volume as a side effect
of source cleanup. Prompts 07 and 08 remain planning-only, with no DB, schema,
account, GPU, network or application provisioning here. External business app
source belongs to Project-Template-derived workspaces, never this repository.

**Subsequent scoped authorization (2026-10-03).**

After the source commits, the owner requested issuance of the 20 newly declared
dev/LAB secret files, isolated execution checks, and integration into the local
`main` branch before Prompt 03. The owner selected **no HOME service start or
restart**. SPEC-0202-TSK-0002 owns this later execution, its exact preflight,
results, recovery and local merge evidence. This authorization does not cover
existing credential rotation, HOME deployment, real data movement or deletion,
remote push/PR/merge, or the deferred SPEC-0201 W7.4 management restore.

## Behavior Contract

1. `mng-pg` and `mng-valkey` retain management metadata, sessions and queues;
   their existing PGDATA, backup chain and consuming tools remain accounted for.
   Future business projects use one `dev-pg` and `dev-valkey`, with explicit
   `project_id` and a named per-project database. `app_db` is a legacy
   technical-source transition item, never a general shared business DB.
2. `dev-pg` uses a pinned TimescaleDB Community PostgreSQL image built with a
   compatible pgBackRest binary. The implementation records the selected
   linux/amd64 manifest digest, PG major, Timescale/TSL and backup tool
   versions, actual PGDATA/UID/GID contract, and fresh compatibility limits.
   Build, extension load and restore are separate evidence, not inferred from
   the image tag. A fresh data volume, isolated network, bounded resources,
   readiness and backup/restore source contract are required.
3. Provisioning accepts approved explicit project metadata, not a database
   name assembled from untrusted shell text. Each project receives a NOLOGIN
   owner, migrator, runtime and reader with least privilege. Runtime owns no
   DB or schema and cannot do DDL; reader cannot write. PUBLIC grants,
   `search_path`, default privileges, sequences, future objects and cross
   project access are tested. First empty-PGDATA initialization and repeatable
   migration/provisioning are separate, fail-closed paths.
4. Time precision, UTC/unit, NULL, duplicate and late-arrival rules are
   documented. Only approved historical series become hypertables; uniqueness
   includes partition dimensions. No raw retention deletion or compression
   policy activates without data-owner approval. Capacity, WAL, autovacuum,
   connection and statement budgets are explicit assumptions until measured.
5. `dev-valkey` uses per-project ACL users and key prefixes, an explicit TTL,
   persistence and maxmemory policy. DB numbers do not provide isolation.
   Conflicting queue `noeviction` and cache LRU requirements trigger a
   separately sized instance decision, not silent shared eviction.
6. Current source consumers are transitioned as one contract: mng init's
   `SERVICE_POSTGRES_*` business responsibility, dbt provision/runtime,
   Debezium source/provision/publication/slot/topic/offset/heartbeat, and host
   IDE endpoint guidance. Avro users retain Schema Registry. Management
   metadata for Superset, MLflow, Pact and other tools remains on mng-pg.
   Connector registration or old LSN reuse is not automatic. A source-only
   internal fixture `project_id=hyhome-platform`, database `platform_dev`,
   schema `app` is the explicit dbt/CDC target; it is provisioned only when
   those profiles are selected, is not an external app DB, and does not
   authorize live cutover. Its owner/migrator/runtime/reader roles are
   `platform_owner`, `platform_migrator`, `platform_runtime`, and
   `platform_reader`. No other project ID is inferred.
7. The owner reported on 2026-10-02 that InfluxDB stores no data. The
   no-data route records that attestation; runtime row-count and writer
   checks remain NOT_RUN. If a dataset appears before cutover, a declared
   measurement/tag/field/type, unit, timestamp precision, retention, query
   and writer inventory is required. The strict mapping validator accepts
   only that explicit input. Export/transform/import/reconciliation adapters
   then depend on the actual source format. Writer/reader cutover, actual
   movement and source-volume deletion stay separately approved and NOT_RUN.
8. Dev-pg has a separate proposed pgBackRest stanza `dev`, repository
   `${BACKUP_STATE_REPO_DIR}/dev-pgbackrest`, and secret reference
   `dev_pgbackrest_cipher_pass`, with backup selection, WAL archive, Restic
   handoff and restore order documented. Its fresh data mount is
   `${DEFAULT_DATA_DIR}/dev-pg`; management and HA PGDATA/repositories are
   excluded. The proposed key custodian is `@buenhyden`, with a distinct
   read-only Docker secret bind after issuance. Backup schedule, retention,
   capacity and RPO/RTO are proposals, not active settings: weekly full,
   daily differential and continuous WAL; two full backup chains; initial
   10 GiB data plus 2 GiB repository reservation; RPO 5 minutes and RTO 4
   hours. Recalculate from measured write rate before activation. Recovery
   selects an immutable backup set, verifies the archive chain, restores to a
   new isolated volume with the matching image/key, checks roles/extensions/
   migration revision and application read/write acceptance, and preserves
   both source and scratch until owner review. Implementer, independent
   reviewer and `@buenhyden` approval are distinct. Key issuance, retention
   activation and separate-volume restore remain later gates. A logical dump
   is not PITR evidence; HOME backup changes and actual recovery are deferred.
9. PostgreSQL HA, Valkey cluster, Kafka multi-broker and NoSQL replica LAB
   dependency closures leave the normal root include graph. Each LAB has a
   separate entrypoint/project/network/volume/credential boundary; normal
   `--profile '*'` render contains no LAB. The existing operations catalog
   rule requiring every tracked infra Compose file in root must be revised
   with focused tests and profile policy to distinguish normal from LAB.
   The normal root and each `labs/<topology>.yml` entrypoint are separate
   Compose projects; each service is reachable from exactly one entrypoint,
   with its dependency closure satisfied there. Split mixed Kafka and OpenSearch
   source declarations so LAB services cannot be reached from normal root.
   LAB definitions are preserved for learning with no shared production
   state and no automatic start/stop.
10. `.env.example`, secret names, profiles, image/version projection,
    Renovate owner, focused validation and runbooks match authored Compose.
    Shared root/env/Registry files have one serial writer. No heavy global
    check is added to commit, push or end-of-task hooks.

## Technical Approach

Write and review this package before implementation. Implement dev engines and
explicit provision inputs first, then source consumers, backup/migration tools,
and LAB graph. Root/env/version edits are serialized by this Task. Prefer
existing Compose/resource/validation patterns. Use static, path-aware checks
for source changes; isolated containers require a fresh Docker/project/port/
network/volume/resource/cleanup preflight and separate approval. Never run all
profiles up. Hold all HOME and real-data operations.

The provisional source budget is dev-pg 2 CPU/2 GiB RAM/256 MiB shared
memory, 100 connections, 2 GiB WAL ceiling and 10 GiB initial data; dev-valkey
0.5 CPU/256 MiB RAM with an explicit memory ceiling. Provision jobs are
short-lived and LAB is not concurrent with the normal budget. The W7.3 host
snapshot showed 12 CPUs, about 13.55 GiB available RAM, 32.72 GiB free on
the system/backup filesystem and 2572.89 GiB free on the data filesystem.
Those are point-in-time facts, not admission evidence. Retain at least 25 GiB
system/backup and 8 GiB data free; remeasure host and existing containers
before any start. If limits or floor fail, runtime is blocked.

The internal fixture uses a *new* CDC identity: publication
`hyhome_platform_publication`, slot `hyhome_platform_slot` and topic prefix
`hyhome.platform`. Connector registration, snapshot mode, old offset/LSN
retirement and downstream topic migration need a separate cutover plan. Old
`app_db` technical objects stay intact until that plan is approved.

## Interfaces and Data

- Input: approved `project_id`, environment, explicit database and role names,
  secret *references*, quota, infra/template/project refs, endpoint locations,
  allowed networks, schema version and approval state from the later 06
  integration contract. A metadata record alone cannot issue a secret or
  deploy an app.
- Output: dev-pg database/roles and dev-valkey ACL/prefix declarations;
  connection metadata for external project migration/runtime/reader; backup
  stanza and restore instructions; CDC/dbt source configuration; LAB entrypoint
  and source-only migration procedure.
- No project is provisioned on behalf of the unapproved 07/08 applications.
  `perf_db` project authority is handed to Prompt 03, not populated here.

## Failure Modes and Guardrails

A missing digest, incompatible PGDATA/extension/pgBackRest package, shared
secret/volume, privilege leak, unbounded WAL, stale CDC offset, ambiguous
Influx precision, or LAB inclusion in root fails source acceptance. An absent
runtime test stays `NOT_RUN`; no catalog query or grep is called a restore.
Keep live `app_db` and Influx sources intact until separately approved
cutover/rollback. If an old consumer cannot be retargeted safely, retain its
source mapping with a blocked handoff rather than claim migration complete.

## Acceptance Contract

1. Baseline, current authored declarations, official digest/platform,
   Timescale license and PG/pgBackRest compatibility are dated and bounded.
2. Static Compose/root/env defines one normal dev-pg and dev-valkey without
   altering mng state; no 07/08 resource is created.
3. Static tests cover explicit project provision, first/repeated/partial
   failure and concurrency logic. Actual cross-project, read/write/DDL
   privilege denial remains isolated execution `NOT_RUN` until approved.
4. Timestamp/hypertable/index/retention and Valkey ACL/TTL/eviction contracts
   have source fixtures and bounded assumptions; extension load and live ACL
   behavior remain isolated execution `NOT_RUN`.
5. dbt, CDC, mng init, Schema Registry and management metadata transition as
   one validated source contract; live connector or data cutover is NOT_RUN.
6. The owner-reported Influx no-data route is recorded without claiming a
   live count. Mapping validation rejects unknown precision/type when a real
   mapping is supplied. Actual export, transform/import and reconciliation
   remain deferred unless source data and writers are discovered.
7. Dev backup/restore source and key reference are documented; actual PITR,
   offsite, HOME operation and real restore remain NOT_RUN by owner deferral.
8. Normal and LAB Compose graphs are statically independent, including
   service, dependency, port, network, volume, name and secret references.
9. Path-aware focused tests, generated version projection check, metadata,
   links and exact changed diff pass; unavailable runtime gates say NOT_RUN.
10. A handoff to 03 (perf_db) and 04/06 (project provision, connection,
    recovery) names owners, schemas, versions and remaining approvals.

## Traceability

- [SPEC-0201](../0201-home-infrastructure-diagnosis-and-work-design/spec.md)
- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [AD-0004](../../02.architecture/descriptions/0004-data-architecture.md)
- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)
- [POL-0021](../../05.operations/policies/0021-backup-and-restore.md)
- [RUN-0021](../../05.operations/runbooks/0021-backup-and-restore.md)

## Open Questions

Live confirmation of the owner-reported empty Influx source and any writers; live dev engine
budget; external project IDs/database names; HOME cutover timing; new dev
backup key custody/retention/RPO/RTO and owner-approved recovery rehearsal. These block only their dependent runtime or project
provision actions, not the source package's static design.

## Operational Impact

Source changes are inert until deployed. A future root include change does not
stop currently running LAB containers or clear their restart policy. Existing
HOME data, secrets, volumes, backup repository and services remain untouched.
