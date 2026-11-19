---
title: "Data Tier (04-data) Architecture Description"
version: "1.4.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0004"
parent_ids:
- "REQ-0004"
created: "2026-03-26"
---

# Data Tier (04-data) Architecture Description

## Context and Boundaries

### System Boundary

Data owns its database and object-store configuration and state contracts. It
does not own every persistent file: analytics checkpoints, application
metadata and package-local stores stay with their consumers. Secrets, ingress
and backup orchestration keep their owners.
No package is split only to make the folder taxonomy uniform.

#### Purpose and Readers

Data provides storage and data-platform packages for HOME applications and
explicitly selected development workloads. Operators need to tell shared HOME
state apart from OPTIONAL packages and LAB topologies. Root packages are
direct children of `infra/04-data`; LAB topologies are standalone entrypoints
under `labs/`. Analytics processing follows ADR-0062 and, since SPEC-0262,
runs as LAB entrypoints.

#### Context

Auth, Workflow, Tooling, Observability (Grafana), AI consumers, the analytics LABs and development workloads consume Data packages as described under Runtime View. Secrets, ingress and backup orchestration stay with their owners.

### Constraints

Data owns its database and object-store configuration and state contracts only, with no package split merely to make the folder taxonomy uniform. Declared secret, network, port and persistent path boundaries are kept; a folder or a Compose profile adds no isolation, and POL-0078 owns the profile vocabulary.

## Structure

### Building Blocks

| Packages | Responsibility | Classification |
| --- | --- | --- |
| mng-db | service metadata PostgreSQL/Valkey, management provisioning and exporters | HOME |
| dev-db | single TimescaleDB Community PostgreSQL and Valkey, project-scoped DB/roles and ACLs | DEV |
| seaweedfs | shared S3 storage and Iceberg REST catalog | HOME |
| qdrant | vector persistence for AI consumers | HOME |
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

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `mng-db` identities | `mng-db` (`mng-pg`, `mng-valkey`) | Auth, Workflow, Tooling and Observability (Grafana); MLflow and Pact Broker for their own databases | The description links no contract for this interface. | `mng-pg` loss affects Auth, Workflow, Tooling and Grafana together; recovery follows each engine's supported backup and restore process and POL-0021. |
| Qdrant vector persistence | `qdrant` | AI consumers configured for it | The description links no contract for this interface. | Recovery follows each engine's supported backup and restore process and POL-0021. |
| SeaweedFS S3 storage | `seaweedfs` | Observability, AI and the analytics LABs, each with its own storage identity | The description links no contract for this interface. | Recovery follows each engine's supported backup and restore process and POL-0021. |
| SeaweedFS Iceberg REST catalog | `seaweedfs` | `labs/lakehouse` Flink, Spark and Trino entrypoints | Iceberg REST catalog | The description records no failure handling for this interface. |
| Development PostgreSQL business fixture | `dev-db` | `labs/dbt` | The description links no contract for this interface. | The description records no failure handling for this interface. |

Consumers use declared `mng-db` identities, Qdrant, SeaweedFS storage identities and the SeaweedFS Iceberg catalog. Infra provisions only approved explicit databases, roles and Valkey ACLs.

## Runtime Behavior

### Normal Flow

#### Runtime View

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

#### Deployment View

The root Compose includes every `infra/04-data` package; profiles select them:
`mng-db` by `mng`, `core`, `dev` and `local` (`mng-pg` also by `mlops`,
`data-science`, `contract-testing` and `bi`); `dev-db` by `dev-data`,
`analytics-engineering` and `quality-results`; `seaweedfs` by
`seaweedfs`, `storage`, the observability storage profiles, `mlops`,
`data-science` and `lakehouse`; `qdrant` by `ai`, `ai-llm` and `qdrant`;
`neo4j` by `graph`; `opensearch` by `opensearch`; `redisinsight` by `admin`
and `admin-data`. LAB entrypoints are separate projects, excluded even from
root `--profile '*'`, with their own network, state and credential contracts.
POL-0078 owns the profile vocabulary.

The root still declares Neo4j and single-node OpenSearch as optional packages.
ADR-0062 records the planned Neo4j LAB move and single-node OpenSearch
retirement. The existing OpenSearch cluster LAB is a separate project.

### Failure and Recovery

`mng-pg` backs most HOME metadata and its loss affects Auth, Workflow, Tooling and Grafana together (see Risks below). Recovery follows each engine's supported backup and restore process and POL-0021; same-host replicas do not give host HA.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- HOME `mng-pg` and `mng-valkey` are shared single-instance dependencies,
  separate from the LAB clusters. Same-host replicas do not give host HA.
- Performance and failover need measured workload and recovery evidence; this
  description makes no tier-wide latency or availability guarantee.
- Declared secret, network, port and persistent path boundaries are kept. A
  folder or a Compose profile adds no isolation.
- Recovery follows each engine's supported backup and restore process and
  POL-0021; a volume declaration or a Git rollback is not a verified backup.

#### Risks

`mng-pg` backs most HOME metadata; its loss affects Auth, Workflow, Tooling and
Grafana together.

### Trade-offs

- HOME `mng-pg` and `mng-valkey` are shared single-instance dependencies,
  separate from the LAB clusters; the accepted cost is that `mng-pg` loss
  affects Auth, Workflow, Tooling and Grafana together, and same-host replicas
  do not give host HA (Quality Attributes, Risks).
- The description makes no tier-wide latency or availability guarantee;
  performance and failover need measured workload and recovery evidence
  (Quality Attributes).
- No package is split only to make the folder taxonomy uniform, and a folder
  or a Compose profile adds no isolation (Constraints).

## Decisions and Adoption

### Decisions

- [ADR-0062 HOME Membership and Planned LABs](../02.decisions/0062-home-lab-membership.md)

### Adoption Boundaries

#### Requirement Mapping

- [REQ-0004 Data requirements](../../01.requirements/0004-data.md)
- [REQ-0027 HOME development host](../../01.requirements/0027-home-development-host.md)

#### Currentness and Lineage

- SPEC-0265 (retired; version history) captured the Hermes report source under ADR-0060.
- [Data packages](../../../infra/04-data/README.md)
- [LAB entrypoints](../../../labs/README.md)
- [Analytics architecture](0012-data-analytics-architecture.md)
- [Backup policy](../../05.operations/02.policies/10.platform-and-backup/0021-backup-and-restore.md)
- [Profile vocabulary](../../05.operations/02.policies/01.common/0078-compose-profile-vocabulary.md)
- [Development database policy](../../05.operations/02.policies/05.databases-and-storage/0100-development-database.md)

#### Evolution

Promoting a LAB topology into `infra/04-data` is an owner decision under the
LAB promotion contract.
