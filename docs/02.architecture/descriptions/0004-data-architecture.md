---
title: "Data Tier (04-data) Architecture Description"
version: "1.2.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "AD-0004"
parent_ids:
- "REQ-0004"
created: "2026-03-26"
---

# Data Tier (04-data) Architecture Description

## Overview

Data provides storage and data-platform packages for HOME applications and
explicitly selected development workloads. Operators need to tell shared HOME
state apart from OPTIONAL packages and LAB topologies. Root packages are
direct children of `infra/04-data`; LAB topologies are standalone entrypoints
under `labs/`. Analytics processing follows ADR-0058 and, since SPEC-0262,
runs as LAB entrypoints.

## Scope

Data owns its database and object-store configuration and state contracts. It
does not own every persistent file: analytics checkpoints, application
metadata and package-local stores stay with their consumers. Secrets, ingress
and backup orchestration keep their owners.
Supabase is an intact optional data platform, including its bundled interfaces.
No package is split only to make the folder taxonomy uniform.

## Structure

### Architecture

| Packages | Responsibility | Classification |
| --- | --- | --- |
| mng-db | service metadata PostgreSQL/Valkey, management provisioning and exporters | HOME |
| dev-db | single TimescaleDB Community PostgreSQL and Valkey, project-scoped DB/roles and ACLs | DEV |
| seaweedfs | shared S3 storage and Iceberg REST catalog | HOME |
| qdrant | vector persistence for AI consumers | HOME |
| supabase | separate application data platform | OPTIONAL |
| neo4j | optional single-node graph persistence | OPTIONAL |
| opensearch | optional single-node search/index storage and dashboards | OPTIONAL |
| redisinsight | local connection/settings metadata and Redis/Valkey administration | OPTIONAL |
| `labs/postgresql-ha`, `labs/valkey-cluster`, `labs/opensearch-cluster` | independent cluster rehearsals | LAB |
| `labs/cassandra`, `labs/couchdb`, `labs/mongodb` | selected nonrelational engines | LAB |

The PostgreSQL HA LAB keeps Patroni, etcd, the router and exporters; they do
not describe HOME's `mng-pg`. SurrealDB stays with its only consumer, Open
Notebook, in `08-ai`. RedisInsight owns only its administration metadata;
target engine backups stay with the engine's Data package. Restic stays in
`09-platform-ops` as cross-platform orchestration. InfluxDB is retired
(ADR-0047); DEV TimescaleDB owns time-series history.

## Runtime and Deployment

### Runtime View

Auth, Workflow, Tooling and Observability (Grafana) use declared `mng-db`
identities; MLflow and Pact Broker provision their own `mng-pg` databases. AI
consumers that are configured for it use Qdrant. Observability, AI and the
analytics LABs share SeaweedFS with their own storage identities. The
`labs/lakehouse` Flink, Spark and Trino entrypoints consume the SeaweedFS
Iceberg catalog, and `labs/dbt` transforms the development PostgreSQL
business fixture. Project migration source stays in external repositories;
infra provisions only approved explicit databases, roles and Valkey ACLs.
`perf_db` keeps test results with project-scoped access, not raw business data
in management databases. No automatic ingestion pipeline exists.

### Deployment View

The root Compose includes every `infra/04-data` package; profiles select them:
`mng-db` by `mng`, `core`, `dev` and `local` (`mng-pg` also by `mlops`,
`data-science`, `contract-testing` and `bi`); `dev-db` by `dev-data`,
`analytics-engineering`, `cdc` and `quality-results`; `seaweedfs` by
`seaweedfs`, `storage`, the observability storage profiles, `nginx`, `mlops`,
`data-science` and `lakehouse`; `qdrant` by `ai`, `ai-llm` and `qdrant`;
`neo4j` by `graph`; `opensearch` by `opensearch`; `redisinsight` by `admin`
and `admin-data`. LAB entrypoints are separate projects, excluded even from
root `--profile '*'`, with their own network, state and credential contracts.
POL-0078 owns the profile vocabulary.

## Quality and Risks

### Quality Attributes

- HOME `mng-pg` and `mng-valkey` are shared single-instance dependencies,
  separate from the LAB clusters. Same-host replicas do not give host HA.
- Performance and failover need measured workload and recovery evidence; this
  description makes no tier-wide latency or availability guarantee.
- Declared secret, network, port and persistent path boundaries are kept. A
  folder or a Compose profile adds no isolation.
- Recovery follows each engine's supported backup and restore process and
  POL-0021; a volume declaration or a Git rollback is not a verified backup.

### Risks

`mng-pg` backs most HOME metadata; its loss affects Auth, Workflow, Tooling and
Grafana together.

### Evolution

Promoting a LAB topology into `infra/04-data` is an owner decision under the
LAB promotion contract.

## Related Documents

- [REQ-0004 Data requirements](../../01.requirements/0004-data.md)
- [REQ-0027 HOME development host](../../01.requirements/0027-home-development-host.md)
- [ADR-0058 HOME tiers versus LABs](../decisions/0058-home-tiers-versus-labs.md)
- [Data packages](../../../infra/04-data/README.md)
- [LAB entrypoints](../../../labs/README.md)
- [Analytics architecture](0012-data-analytics-architecture.md)
- [Backup policy](../../05.operations/policies/10-platform-and-backup/0021-backup-and-restore.md)
- [Profile vocabulary](../../05.operations/policies/01-common/0078-compose-profile-vocabulary.md)
- [Development database policy](../../05.operations/policies/05-databases-and-storage/0100-development-database.md)
