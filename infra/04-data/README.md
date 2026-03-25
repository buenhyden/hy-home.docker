<!-- [ID:04-data:root] -->
# Data Tier (04-data)

> Central repository for databases, object storage, and persistence engines.

## Overview (KR)

이 계층은 시스템의 모든 영속성 데이터를 관리합니다. 관계형 데이터베이스(PostgreSQL), NoSQL(MongoDB, Cassandra), 벡터 데이터베이스(Qdrant), 시계열 데이터베이스(InfluxDB) 및 객체 스토리지(MinIO)를 포함하는 다중 모드 데이터 인프라를 제공합니다.

## Overview

The `04-data` tier provides a polyglot persistence layer for the `hy-home.docker` ecosystem. It is designed for high availability (HA), scalability, and specialized data workloads (e.g., RAG, Time-series, Graph). All services are integrated into the `infra_net` and utilize standardized secret management and persistence volumes.

## Documentation Navigation Map

| Type | Link | Description |
| :--- | :--- | :--- |
| **Guide** | [Data Setup & Management](../../docs/07.guides/04-data/README.md) | Deployment, scaling, and integration guides. |
| **Operations** | [Data Policies](../../docs/08.operations/04-data/README.md) | Backup, replication, and data residency standards. |
| **Runbook** | [Data Emergency Recovery](../../docs/09.runbooks/04-data/README.md) | Recovery from corruption, split-brain, or storage exhaustion. |

## Service Matrix

| Service | Category | Profile | Path | Role |
| :--- | :--- | :--- | :--- | :--- |
| **mng-db** | Core SQL/Cache | (core) | [`./mng-db`](./mng-db) | Shared Postgres + Valkey |
| **postgresql-cluster** | HA SQL | (core) | [`./postgresql-cluster`](./postgresql-cluster) | Patroni-based HA PostgreSQL |
| **valkey-cluster** | HA Cache | (core) | [`./valkey-cluster`](./valkey-cluster) | 6-node distributed Valkey cluster |
| **minio** | Object Storage | (core) | [`./minio`](./minio) | S3-compatible object storage |
| **opensearch** | Search / Analytics | (core) | [`./opensearch`](./opensearch) | Search engine + Dashboards |
| **qdrant** | Vector DB | (core) | [`./qdrant`](./qdrant) | Vector search engine (RAG) |
| **seaweedfs** | Distributed FS | (standalone) | [`./seaweedfs`](./seaweedfs) | Distributed object storage |
| **supabase** | Full Stack | (standalone) | [`./supabase`](./supabase) | Self-hosted Supabase stack |
| **mongodb** | NoSQL Document | (standalone) | [`./mongodb`](./mongodb) | MongoDB replica set |
| **cassandra** | NoSQL Columnar | (standalone) | [`./cassandra`](./cassandra) | Apache Cassandra single-node |
| **influxdb** | Time-series | `influxdb` | [`./influxdb`](./influxdb) | Time-series database |
| **couchdb** | NoSQL Sync | `couchdb` | [`./couchdb`](./couchdb) | CouchDB cluster |
| **neo4j** | Graph DB | (standalone) | [`./neo4j`](./neo4j) | Graph database |

## Structure

```text
04-data/
├── mng-db/               # Shared Management DB (Postgres/Valkey)
├── postgresql-cluster/   # High Availability PG (Patroni)
├── valkey-cluster/       # Distributed Cache Cluster
├── minio/                # S3 Object Storage
├── qdrant/               # Vector Database
├── opensearch/           # Search & Analytics
├── supabase/             # Supabase Integrated Stack
└── ...                   # Specialized Databases
```

## Governance

- **Persistence**: All data MUST reside in `${DEFAULT_DATA_DIR}` or `${DEFAULT_MANAGEMENT_DIR}`.
- **Secrets**: Passwords MUST be managed via Docker secrets or injected from Vault JIT.
- **Networking**: Services MUST connect via the `infra_net` internal bridge.

---

Copyright (c) 2026. Licensed under the MIT License.
