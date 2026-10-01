---
title: "Data Tier (04-data) Architecture Description"
version: "1.0.6"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "architecture"
artifact_id: "AD-0004"
parent_ids:
- "REQ-0004"
created: "2026-03-26"
---

# Data Tier (04-data) Architecture Description

## Context and Stakeholders

Data provides storage and data-platform packages for HOME applications and
explicitly selected development workloads. Operators need to distinguish
shared HOME state from OPTIONAL platforms and LAB topologies. Package names
are direct children of `infra/04-data`; Analytics processing lives in
`infra/12-analytics` under ADR-0045.

## System Boundaries

Data owns its database/object-store configuration and state contracts. It does
not own every persistent file in the platform: analytics checkpoints,
application metadata and package-local stores remain with their consumers.
Secrets, ingress and backup orchestration retain their existing owners.
Supabase is an intact optional data platform, including its bundled interfaces.
No package is split solely to make a folder taxonomy more uniform.

## Quality Attributes

- HOME mng-pg and mng-valkey are shared single-instance dependencies, separate
  from LAB PostgreSQL/Valkey clusters. Same-host replicas do not provide host HA.
- Performance and failover require measured workload/recovery evidence; this
  description makes no tier-wide latency or availability guarantee.
- Preserve declared secret, network, port and persistent path boundaries.
  A folder or Compose profile does not add isolation.
- Recovery follows each engine's supported backup/restore process and POL-0021;
  a volume declaration or a Git rollback is not a verified data backup.

## Components

| Packages | Responsibility | Classification |
| --- | --- | --- |
| mng-db | shared PostgreSQL/Valkey, provisioning and exporters | HOME |
| seaweedfs | shared S3 storage and Iceberg REST catalog | HOME |
| qdrant | vector persistence for AI consumers | HOME |
| supabase | separate application data platform | OPTIONAL |
| influxdb, neo4j | time-series and graph persistence | OPTIONAL |
| opensearch | search/index storage and optional cluster topology | OPTIONAL / LAB |
| postgresql-cluster, valkey-cluster | independent cluster rehearsals | LAB |
| cassandra, couchdb, mongodb | selected nonrelational engines | LAB |
| redisinsight | local connection/settings metadata and Redis/Valkey administration | OPTIONAL |

The PostgreSQL cluster retains Patroni, etcd, pg-router and exporters. Those
components do not describe HOME's mng-pg topology. SurrealDB stays with its
sole consumer Open Notebook in `08-ai`. RedisInsight owns only its administration metadata; target engine backups remain owned by the corresponding Data service. Restic stays in Tooling as cross-platform orchestration.

## Data Flow

Auth, Workflow, Tooling and Analytics use declared mng-db identities. AI uses
Qdrant. Observability, AI and Analytics share SeaweedFS with their own storage
identities. Flink/Spark/Trino consume its Iceberg catalog; dbt transforms
PostgreSQL data. Existing Compose dependencies and profiles define actual
activation; this description does not assert an automatic ingestion pipeline.

## Deployment View

The root Compose includes package files. Exact profiles and networks remain
in source and POL-0078. The structural move preserves service names, images,
ports, secrets, persistent volume identities and host paths. It does not
restart containers or reconcile existing source mounts.

## Traceability

- [REQ-0004](../../01.requirements/0004-data.md)
- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [ADR-0045](../decisions/0045-data-storage-and-analytics-tier-boundary.md)
- [SPEC-0197](../../03.specs/0197-infra-tier-layout/spec.md)

## Related Documents

- [Data packages](../../../infra/04-data/README.md)
- [Analytics architecture](0012-data-analytics-architecture.md)
- [Backup policy](../../05.operations/policies/0021-backup-and-restore.md)
- [Profile vocabulary](../../05.operations/policies/0078-compose-profile-vocabulary.md)
