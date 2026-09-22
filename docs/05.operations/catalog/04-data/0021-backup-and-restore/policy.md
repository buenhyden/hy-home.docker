---
title: "04-Data Backup Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "POL-0021"
parent_ids:
- "AD-0004"
created: "2026-06-04"
---

# 04-Data Backup Policy

## Overview

This policy binds current source configuration to data protection, security,
resource, lifecycle and independently verifiable operator controls.

### Purpose

This policy assigns a recoverability method to every retained HOME state owner. A
Compose volume is not a backup, replication on this single host is not host
availability, and a successful export is not restore evidence. All restores are
planned procedures until a dated rehearsal report says otherwise.

Paths beginning with `${DEFAULT_*}` are bind-backed named volumes whose resolved
host value remains private operator state.

## Policy Scope

This policy applies to the current source-backed package and its retained state.

### HOME state-owner matrix

| Owner and data class | Current state surface | Required backup method and destination | Encryption and retention | Planning target | Rehearsal and recovery owner |
| --- | --- | --- | --- | --- | --- |
| Management PostgreSQL: `postgres`, `n8n`, `keycloak`, `airflow`, `terrakube`, `sonarqube`, and `${SERVICE_POSTGRES_DB:-app_db}` | `mng-pg-data` → `${DEFAULT_MANAGEMENT_DIR}/pg`; roles and grants are cluster-wide | pgBackRest in the server image: full backup on Sunday, differential daily, continuous WAL archive (`archive_timeout`) to `${BACKUP_STATE_REPO_DIR}/pgbackrest` on the system SSD (budget, control 2); a globals-only export goes to Restic; never copy a live `PGDATA` tree | Repository `aes-256-cbc` with BKP-001; two full backups and their WAL retained; Restic 30 daily / 13 weekly / 12 monthly | RPO 5 min by WAL archive, RTO 4 h; planning target, unverified on HOME data | Synthetic full/diff/PITR rehearsal passes (`BackupRestoreRehearsalTests`, 2026-09-22); no HOME-data restore yet. Procedure: [RUN-0021](runbook.md); service recovery: [RUN-0028](../0028-management-database/runbook.md) |
| Management Valkey: OAuth2 Proxy sessions and Airflow/n8n broker/cache | `mng-valkey-data` → `${DEFAULT_MANAGEMENT_DIR}/valkey`; AOF enabled | Point-in-time RDB stream (`valkey-cli --rdb -`) into export staging, then a Restic snapshot; the live AOF directory is excluded; record whether queued work must be replayed or discarded | Restic encryption with BKP-002; 30 daily / 13 weekly / 12 monthly | RPO 24 h, RTO 4 h; queued-job semantics require incident approval | Synthetic RDB export and reload rehearsed 2026-09-22; no HOME-data restore. Recovery: [RUN-0028](../0028-management-database/runbook.md) |
| OpenBao secrets and Raft state | `openbao-data` → `${DEFAULT_SECURITY_DIR}/openbao/data` | Authenticated Raft snapshot to separate offline custody; seal/recovery material follows its security runbook | Barrier encryption does not replace encrypted backup custody; daily 30 days, monthly 1 year | RPO 24 h, RTO 4 h; planning target, unverified | No rehearsal. OpenBao security operations own recovery. `openbao-agent-data` and `openbao-agent-out` contain generated secret material and stay outside general archives. |
| OpenBao Agent generated auth/render state | `openbao-agent-data` → `${DEFAULT_SECURITY_DIR}/openbao/agent`; `openbao-agent-out` → `${DEFAULT_SECURITY_DIR}/openbao/out` | Do not generically back up rendered secret output. Recover by re-authenticating the agent and re-rendering from restored OpenBao; separately preserve non-secret template source | Output is secret-bearing and source-at-rest encryption is unverified; no general retention | Data RPO not applicable to derived output; recovery target 4 h, unverified | No rehearsal. Security operations own re-authentication, template verification and secure disposal of stale output. |
| MinIO S3: `loki-bucket`, `tempo-bucket`, `cdn-bucket`, `doc-intel-assets` | `minio-data` → `${DEFAULT_DATA_DIR}/minio/data-1`; optional LAB nodes use `${DEFAULT_DATA_DIR}/minio/data1` … `data4` | Object-aware mirror/replication to a separate target plus bucket inventory, policies, versioning and IAM configuration; no raw copy of active `/data` | No server-side encryption or KMS is declared; encrypted destination required; daily 30 days, weekly 90 days | RPO 24 h, RTO 8 h; planning target, unverified | No rehearsal. Recovery: [RUN-0023](../0023-minio/runbook.md) |
| Open WebUI application state | `open-webui` → `${DEFAULT_AI_MODEL_DIR}/open-webui` | `backup-sqlite-export` copies `webui.db` through the SQLite Online Backup API with an integrity check; uploads and other files go to Restic directly; the live database files and cache are excluded | Restic encryption with BKP-002; 30 daily / 13 weekly / 12 monthly | RPO 24 h, RTO 8 h; planning target, unverified | Synthetic WAL-database export rehearsed 2026-09-22; no HOME-data restore. The AI operations subject owns isolated validation. |
| SeaweedFS objects and filer metadata | `seaweedfs-{master,volume,filer}` → `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}` | Orchestrator pauses vacuum, exports filer metadata with `fs.meta.save`, Restic reads the volume and master trees, vacuum resumes on exit; the live leveldb2 filer store is not file-copied | Restic encryption with BKP-002; 30 daily / 13 weekly / 12 monthly; counts toward the 5 GiB state budget | RPO 24 h, RTO 8 h; planning target | Isolated rehearsal 2026-09-22: restore into empty stores returned identical objects; no HOME data yet. GDE/RUN-0024 own validation. |
| Gatus availability history | `gatus-data` → `${DEFAULT_OBSERVABILITY_DIR}/gatus`; SQLite at `/data/gatus.db` in WAL mode | `backup-sqlite-export` Online Backup API copy including uncheckpointed WAL pages, then Restic | Restic encryption with BKP-002; 30 daily / 13 weekly / 12 monthly | RPO 24 h, RTO 4 h; planning target, unverified | Synthetic WAL export rehearsed 2026-09-22; no HOME-data restore. The Gatus operations subject owns validation. |
| Grafana database, plugins and mutable state | `grafana-data` → `${DEFAULT_OBSERVABILITY_DIR}/grafana`; current Compose does not configure external PostgreSQL | `backup-sqlite-export` Online Backup API copy of `grafana.db`, then Restic; plugins are rebuildable from provisioning and the plugin list; provisioning files remain tracked source | Restic encryption with BKP-002; 30 daily / 13 weekly / 12 monthly | RPO 24 h, RTO 4 h; planning target, unverified | Synthetic export rehearsed 2026-09-22; no HOME-data restore. The Grafana operations subject owns validation. |
| Keycloak themes, providers and runtime configuration | `keycloak-themes` → `${DEFAULT_AUTH_DIR}/keycloak/themes`; `keycloak-providers` → `${DEFAULT_AUTH_DIR}/keycloak/providers`; `keycloak-config` → `${DEFAULT_AUTH_DIR}/keycloak/conf`; mounted read-only by the service | Versioned source/build artifact where available plus quiesced file snapshot and hash manifest; pair with the `keycloak` PostgreSQL database and separately custodied secrets | No at-rest encryption is declared; encrypt any backup; weekly 90 days and before upgrades | RPO 7 days, RTO 8 h; planning target, unverified | No rehearsal. Auth operations must validate provider/theme compatibility and realm login against restored database state. |
| Airflow schedules and metadata | `airflow-config`, `airflow-dags`, `airflow-logs`, `airflow-plugins`, PostgreSQL database `airflow`, and management Valkey | Coordinated PostgreSQL logical dump plus file snapshot after pausing schedulers/workers; retain DAGs/plugins/config; logs follow operational retention | Encrypted destination required; metadata/files daily 30 days, logs 14 days | RPO 24 h, RTO 8 h; planning target, unverified | No rehearsal. Airflow operations own application validation and Fernet/key custody. |
| n8n workflows, credentials and runners | `n8n-data`, `n8n-task-runner-data`, `n8n-task-runner-worker-data`, `infra/07-workflow/n8n/custom`, PostgreSQL database `n8n`, and management Valkey | Pause producers/workers; coordinated PostgreSQL dump plus file snapshot; preserve encryption key separately; decide queue replay before Valkey restore | Encrypted destination required; daily 30 days | RPO 24 h, RTO 8 h; planning target, unverified | No rehearsal. n8n operations own workflow, credential and runner validation. |
| ComfyUI user assets and workflows | `comfyui-custom-nodes`, `comfyui-input`, `comfyui-output`, `comfyui-user` | Quiesced file snapshot with custom-node source/revision inventory | Source-at-rest encryption is unverified; encrypted destination required; daily inputs/user, weekly outputs/custom nodes, 30/90 day retention | RPO 24 h, RTO 24 h; planning target, unverified | No rehearsal. `comfyui-models`, Hugging Face and Torch caches may be rebuilt only when model identifiers, licenses and hashes are recorded. |
| Ollama local model store | `ollama-data` → `${DEFAULT_AI_MODEL_DIR}/ollama` | Preserve custom Modelfiles and irreplaceable inputs; catalog downloaded models for verified re-pull | Source-at-rest encryption is unverified; custom inputs weekly 90 days | Rebuild target 24 h; downloaded blobs have no data-loss RPO when reproducibly sourced | No rehearsal. Rebuild exception requires source, version, license and hash evidence. |
| Qdrant vector collections | `qdrant-data` → `${DEFAULT_DATA_DIR}/qdrant/data` | Qdrant collection/full-storage snapshots copied to a separate target; never treat a live directory copy as a snapshot | Source-at-rest encryption is unverified; encrypted destination required; daily 30 days | RPO 24 h, RTO 8 h; planning target, unverified | No rehearsal. Qdrant operations own isolated snapshot restore. |
| Prometheus metrics | `prometheus-data` → `${DEFAULT_OBSERVABILITY_DIR}/prometheus` | Engine snapshot where supported, otherwise stopped filesystem snapshot; tracked scrape/rule configuration restores from source | Source-at-rest encryption is unverified; encrypted destination required; daily 7 days | RPO 24 h, RTO 8 h; planning target, unverified | No rehearsal. Prometheus operations own TSDB validation. |
| Loki logs | `loki-data` → `${DEFAULT_OBSERVABILITY_DIR}/loki` for WAL/cache/rules, plus MinIO `loki-bucket` | Coordinate Loki quiescence, local WAL/rule snapshot and MinIO object-aware backup; restore both sides to one recovery point | Source-at-rest encryption is unverified; encrypted destination required; daily 14 days | RPO 24 h, RTO 8 h; planning target, unverified | No rehearsal. Loki operations and [RUN-0023](../0023-minio/runbook.md) share validation. |
| Tempo traces (OPTIONAL service, retained HOME bucket state) | `tempo-data` → `${DEFAULT_OBSERVABILITY_DIR}/tempo` for WAL/cache, plus MinIO `tempo-bucket` | When traces are retained, coordinate Tempo quiescence, local WAL snapshot and MinIO object backup | Source-at-rest encryption is unverified; encrypted destination required; daily 7 days | RPO 24 h, RTO 8 h when selected; planning target, unverified | No rehearsal. Tempo operations and [RUN-0023](../0023-minio/runbook.md) share validation. |
| Alertmanager silences/state | `alertmanager-data` → `${DEFAULT_OBSERVABILITY_DIR}/alertmanager` | Stopped or application-consistent snapshot; tracked routing configuration restores from source | Source-at-rest encryption is unverified; encrypted destination required; daily 7 days | RPO 24 h, RTO 4 h; planning target, unverified | No rehearsal. Alertmanager operations own silence and route validation. |
| Alloy ingestion cursor/WAL | `alloy-data` → `${DEFAULT_OBSERVABILITY_DIR}/alloy` | Stopped snapshot when duplicate or missing ingestion is unacceptable; otherwise rebuild from tracked config with the loss window recorded | Source-at-rest encryption is unverified; encrypted destination required when retained; 7 days | RPO 24 h, RTO 4 h; planning target, unverified | No rehearsal. Rebuild is allowed only with an accepted telemetry gap. |

## Controls

1. The destination must be outside the source volume and on a different
   physical disk. `BACKUP_STATE_REPO_DIR` (system SSD) holds copies of
   data-disk state and `BACKUP_HOST_REPO_DIR` (data disk) holds copies of
   `secrets/` and `.env`; the orchestrator refuses a repository on the same
   filesystem as, or inside, its source. All copies are on one host, so
   **offsite recovery is not provided**.
2. The SSD repository has a size budget of `BACKUP_STATE_MAX_GIB` (5 GiB,
   owner 2026-09-22). Above it the run fails and Restic writes nothing;
   snapshots are never deleted automatically to meet the budget.
3. Backup keys BKP-001 and BKP-002 have an offline copy outside this host.
   Restic's host repository contains the keys but needs BKP-002 to open.
4. One scheduler owns backups: `hyhome-backup.timer` on the host. Airflow and
   other schedulers do not run backups. Snapshot deletion (`forget-prune`) is a
   separately approved manual procedure.
5. Use engine-supported export or snapshot methods. Raw copies of active
   PostgreSQL, SQLite, Valkey, MinIO, Qdrant, Loki or Tempo storage are not
   accepted backup artifacts. SeaweedFS volume trees are read live only
   because needles are append-only, vacuum is paused and filer metadata is
   exported first, and the restore of that set is rehearsed (GDE-0024);
   objects changed during the Restic read may be missing from it (POL-0024).
6. Capture a manifest containing service, engine/source version, timestamp,
   scope, object/file count where meaningful, byte size and cryptographic hash.
7. Do not place passwords, unseal material, database dumps, workflow credentials
   or secret-rendered agent output in Git or in the generic evidence tree.
8. Destructive recovery, cutover, cleanup, credential rotation or live service
   change requires a separately approved task. This policy does not authorize it.

### Restore acceptance

A rehearsal uses an isolated target, compatible engine version and disposable
credentials. It proves application-level reads and writes, records elapsed time
against the planning RTO, states the observed recovery point, and destroys or
secures the test copy afterward. Production replacement is a separate approved
cutover with rollback.

## Exceptions

HOME state owners; rebuildable exceptions require recorded source evidence. Exceptions do not authorize runtime mutation, plaintext secrets, raw active
storage copies or same-host availability claims.

## Verification

Verify root configuration and scoped static policy checks, then require an
isolated compatible restore with application-level acceptance before promotion or
cutover. Record unverified runtime properties explicitly.

## Review Cadence

Review after profile, image, volume, credential, consumer, retention or upstream
lifecycle change and at least annually while retained.

## Traceability

- Artifact: `POL-0021`; parent: `AD-0004`.
- Runtime authority remains the linked Compose/source files; exact pins stay there.

### Official references

- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
- [SQLite Online Backup API](https://sqlite.org/backup.html) and [backup-copy hazards](https://sqlite.org/howtocorrupt.html)
- [Valkey persistence](https://valkey.io/topics/persistence/)
- [MinIO community repository and maintenance status](https://github.com/minio/minio)
- [Qdrant snapshots](https://qdrant.tech/documentation/concepts/snapshots/)
- [Grafana backup guidance](https://grafana.com/docs/grafana/latest/administration/back-up-grafana/)
- [OpenBao Raft operator commands](https://openbao.org/docs/commands/operator/raft/)
- [pgBackRest user guide](https://pgbackrest.org/user-guide.html) and [command reference](https://pgbackrest.org/command.html)
- [Restic repository preparation](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html) and [snapshot removal](https://restic.readthedocs.io/en/stable/060_forget.html)

## Related Documents

- [Backup and Restore Guide](guide.md) and [Runbook](runbook.md)
- Runtime sources: [Restic Compose](../../../../../infra/09-tooling/restic/docker-compose.yml), [pgBackRest image](../../../../../infra/04-data/operational/mng-db/pg/backup/Dockerfile) and the [derived image projection](../../../../../infra/tech-stack.versions.json)
- [Data Architecture](../../../../02.architecture/descriptions/0004-data-architecture.md)
- [Data hardening policy](../0030-optimization-hardening/policy.md)
- [Storage exhaustion runbook](../0035-storage-exhaustion/runbook.md)
