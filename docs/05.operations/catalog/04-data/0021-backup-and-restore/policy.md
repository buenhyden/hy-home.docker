---
title: "04-Data Backup Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
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

## Purpose

This policy assigns a recoverability method to every retained HOME state owner. A
Compose volume is not a backup, replication on this single host is not host
availability, and a successful export is not restore evidence. All restores are
planned procedures until a dated rehearsal report says otherwise.

Paths beginning with `${DEFAULT_*}` are bind-backed named volumes whose resolved
host value remains private operator state.

## Policy Scope

This policy applies to the current source-backed package and its retained state.

## HOME state-owner matrix

| Owner and data class | Current state surface | Required backup method and destination | Encryption and retention | Planning target | Rehearsal and recovery owner |
| --- | --- | --- | --- | --- | --- |
| Management PostgreSQL: `postgres`, `n8n`, `keycloak`, `airflow`, `terrakube`, `sonarqube`, and `${SERVICE_POSTGRES_DB:-app_db}` | `mng-pg-data` → `${DEFAULT_MANAGEMENT_DIR}/pg`; roles and grants are cluster-wide | Logical dump of globals plus every database to a separate backup device; never copy a live `PGDATA` tree | Source-at-rest encryption is unverified; encrypted destination and access-controlled custody required; daily 30 days, weekly 90 days | RPO 24 h, RTO 4 h; planning target, unverified | No HOME-data rehearsal. The synthetic major-upgrade rehearsal in [RUN-0032](../0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md) is not HOME backup proof. Recovery: [RUN-0028](../0028-management-database/runbook.md) |
| Management Valkey: OAuth2 Proxy sessions and Airflow/n8n broker/cache | `mng-valkey-data` → `${DEFAULT_MANAGEMENT_DIR}/valkey`; AOF enabled | Preserve the complete AOF set and manifest plus an RDB checkpoint at one quiesced point; separately record whether queued work must be replayed or discarded | Source-at-rest encryption is unverified; encrypted destination required; daily 7 days | RPO 24 h, RTO 4 h; queued-job semantics require incident approval | No rehearsal. Recovery: [RUN-0028](../0028-management-database/runbook.md) |
| OpenBao secrets and Raft state | `openbao-data` → `${DEFAULT_SECURITY_DIR}/openbao/data` | Authenticated Raft snapshot to separate offline custody; seal/recovery material follows its security runbook | Barrier encryption does not replace encrypted backup custody; daily 30 days, monthly 1 year | RPO 24 h, RTO 4 h; planning target, unverified | No rehearsal. OpenBao security operations own recovery. `openbao-agent-data` and `openbao-agent-out` contain generated secret material and stay outside general archives. |
| OpenBao Agent generated auth/render state | `openbao-agent-data` → `${DEFAULT_SECURITY_DIR}/openbao/agent`; `openbao-agent-out` → `${DEFAULT_SECURITY_DIR}/openbao/out` | Do not generically back up rendered secret output. Recover by re-authenticating the agent and re-rendering from restored OpenBao; separately preserve non-secret template source | Output is secret-bearing and source-at-rest encryption is unverified; no general retention | Data RPO not applicable to derived output; recovery target 4 h, unverified | No rehearsal. Security operations own re-authentication, template verification and secure disposal of stale output. |
| MinIO S3: `loki-bucket`, `tempo-bucket`, `cdn-bucket`, `doc-intel-assets` | `minio-data` → `${DEFAULT_DATA_DIR}/minio/data-1`; optional LAB nodes use `${DEFAULT_DATA_DIR}/minio/data1` … `data4` | Object-aware mirror/replication to a separate target plus bucket inventory, policies, versioning and IAM configuration; no raw copy of active `/data` | No server-side encryption or KMS is declared; encrypted destination required; daily 30 days, weekly 90 days | RPO 24 h, RTO 8 h; planning target, unverified | No rehearsal. Recovery: [RUN-0023](../0023-minio/runbook.md) |
| Open WebUI application state | `open-webui` → `${DEFAULT_AI_MODEL_DIR}/open-webui` | Application export when available, otherwise SQLite Online Backup API or a fully stopped copy of the whole application data directory | Source-at-rest encryption is unverified; encrypted destination required; daily 30 days | RPO 24 h, RTO 8 h; planning target, unverified | No rehearsal. The AI operations subject owns isolated validation. |
| Gatus availability history | `gatus-data` → `${DEFAULT_OBSERVABILITY_DIR}/gatus`; SQLite at `/data/gatus.db` | SQLite Online Backup API or stopped copy including database, WAL and journal files | Source-at-rest encryption is unverified; encrypted destination required; daily 14 days | RPO 24 h, RTO 4 h; planning target, unverified | No rehearsal. The Gatus operations subject owns validation. |
| Grafana database, plugins and mutable state | `grafana-data` → `${DEFAULT_OBSERVABILITY_DIR}/grafana`; current Compose does not configure external PostgreSQL | Follow Grafana backup guidance; quiesce and preserve the SQLite database, plugins and mutable data together; provisioning files remain tracked source | Source-at-rest encryption is unverified; encrypted destination required; daily 30 days | RPO 24 h, RTO 4 h; planning target, unverified | No rehearsal. The Grafana operations subject owns validation. |
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

1. The destination must be outside the source volume and outside the physical
   failure domain where practicable. Record owner, media, access boundary and
   encryption-key custody without committing private paths or credentials.
2. Use engine-supported export or snapshot methods. Raw copies of active
   PostgreSQL, SQLite, Valkey, MinIO, Qdrant, Loki or Tempo storage are not
   accepted backup artifacts.
3. Capture a manifest containing service, engine/source version, timestamp,
   scope, object/file count where meaningful, byte size and cryptographic hash.
4. Do not place passwords, unseal material, database dumps, workflow credentials
   or secret-rendered agent output in Git or in the generic evidence tree.
5. Destructive recovery, cutover, cleanup, credential rotation or live service
   change requires a separately approved task. This policy does not authorize it.

## Restore acceptance

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

## Official references

- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
- [SQLite Online Backup API](https://sqlite.org/backup.html) and [backup-copy hazards](https://sqlite.org/howtocorrupt.html)
- [Valkey persistence](https://valkey.io/topics/persistence/)
- [MinIO community repository and maintenance status](https://github.com/minio/minio)
- [Qdrant snapshots](https://qdrant.tech/documentation/concepts/snapshots/)
- [Grafana backup guidance](https://grafana.com/docs/grafana/latest/administration/back-up-grafana/)
- [OpenBao Raft operator commands](https://openbao.org/docs/commands/operator/raft/)

## Related Documents

- [Data Architecture](../../../../02.architecture/descriptions/0004-data-architecture.md)
- [Data hardening policy](../0030-optimization-hardening/policy.md)
- [Storage exhaustion runbook](../0035-storage-exhaustion/runbook.md)
