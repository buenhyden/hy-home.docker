---
title: "Data Tier (04-data)"
version: "1.2.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2025-11-12"
---

# 04 Data

## Overview

This tier contains persistent engines and stateful platform dependencies. The root
Compose project includes the leaf files and owns shared networks, secrets and
`extends`; operate from the repository root rather than treating a leaf as a
standalone project.

## Audience

This package map is for operators and maintainers of the repository data tier.

## Scope

It covers the data packages selected by the root Compose project and their
documented operating boundaries.

## Structure

### Package map and disposition

| Component | Root profile(s) | Classification | Relationship and service operations |
| --- | --- | --- | --- |
| [`operational/mng-db`](operational/mng-db/README.md) | `mng`, `core`, `dev`, `local` | HOME | Shared PostgreSQL/Valkey for auth, workflow and tooling; never share its directories with alternatives |
| [`cache-and-kv/valkey-cluster`](cache-and-kv/valkey-cluster/README.md) | `valkey-cluster` | LAB | Six nodes on one host; distinct from management Valkey and not host HA |
| [`lake-and-object/seaweedfs`](lake-and-object/seaweedfs/README.md) | `storage`, `obs`, `logs`, `tracing`, `nginx`, `mlops`, `data-science`, `lakehouse`, `seaweedfs`, `storage-seaweedfs` | HOME | S3 store that replaced MinIO (S07) and serves the Iceberg REST catalog (S12); persistent set, identities, JWT and gRPC mTLS; only S3 is routed |
| [`lakehouse/flink`](lakehouse/flink/README.md) | `lakehouse` | OPTIONAL | Flink session cluster for streaming and batch SQL into the SeaweedFS Iceberg catalog; Kafka on `kafka_net`; loopback REST only |
| [`lakehouse/great-expectations`](lakehouse/great-expectations/README.md) | `lakehouse` | OPTIONAL | One-shot GX Core job checking Iceberg tables through Trino against tracked suites |
| [`lakehouse/trino`](lakehouse/trino/README.md) | `lakehouse` | OPTIONAL | Single-node Trino SQL engine on the SeaweedFS Iceberg catalog; loopback HTTP only |
| [`lakehouse/spark`](lakehouse/spark/README.md) | `lakehouse` | OPTIONAL | One-shot Spark batch and Iceberg maintenance job on the SeaweedFS catalog; tables in the `lakehouse` table bucket |
| [`operational/supabase`](operational/supabase/README.md) | `supabase` | OPTIONAL | Separate application platform; no management-database merge |
| [`relational/postgresql-cluster`](relational/postgresql-cluster/README.md) | `postgres-ha` | LAB | Same-host Patroni/etcd/router topology; no `mng-pg` volume reuse |
| [`analytics/influxdb`](analytics/influxdb/README.md) | `influxdb` | OPTIONAL | Separate time-series engine; no inferred Prometheus replacement |
| [`analytics/ksql`](analytics/ksql/README.md) | `ksql` | OPTIONAL | Kafka-dependent stream processing; requires named Kafka workload |
| [`analytics/opensearch`](analytics/opensearch/README.md) | `opensearch`, `opensearch-cluster` | OPTIONAL/LAB | Single-node search versus same-host cluster exercise |
| [`analytics/starrocks`](analytics/starrocks/README.md) | `starrocks` | OPTIONAL | Named analytical workload only |
| [`nosql/cassandra`](nosql/cassandra/README.md), [`couchdb`](nosql/couchdb/README.md), [`mongodb`](nosql/mongodb/README.md) | `cassandra`, `couchdb`, `mongodb` | LAB | Separate same-host datastore laboratories; no cross-engine volume or migration assumption |
| [`specialized/qdrant`](specialized/qdrant/README.md) | `ai`, `ai-llm`, `qdrant` | HOME | Vector store for HOME AI; snapshot/isolated restore required |
| [`specialized/neo4j`](specialized/neo4j/README.md) | `graph` | OPTIONAL | Graph workload only; distinct from Qdrant |
| SurrealDB (moved) | `surrealdb`, `notebook` | OPTIONAL | Co-located with its only consumer in [`11-laboratory/open-notebook`](../11-laboratory/open-notebook/surrealdb/README.md) since owner commit `3870f08ff`; data path unchanged |

## How to Work in This Area

### Operating contract

- Use the exact profile from the matrix through the root project; for example,
  `docker compose --env-file .env.example --profile mng config --quiet`.
- Do not print rendered secrets or private resolved host paths into evidence.
- A named volume backed by a host directory is persistent state, not a backup.
  Same-host replicas do not protect against host loss.
- Every selected engine needs a named consumer, capacity/retention boundary,
  engine-supported backup, separate encrypted destination and isolated restore.
- Image, topology, credential, volume, migration and cleanup changes require the
  owning Stage 05 guide/policy/runbook and an approved task.

## Related Documents

Use the [documentation entry point](../../docs/README.md) to locate the Stage 05
Data catalog (`docs/05.operations/catalog/04-data/`), especially POL-0021 for the
HOME state-owner matrix and RUN-0035 for storage exhaustion.
