<!-- [ID:04-data:root] -->
# Data Tier (04-data)

> Central repository for databases, object storage, and persistence engines.

## 1. Context (SSoT)

This tier provides a polyglot persistence layer for the `hy-home.docker` ecosystem. It manages all stateful data ranging from transactional SQL to high-velocity time-series and semantic vector data.

- **SSoT Documentation**: [docs/07.guides/04-data/README.md](../../docs/07.guides/04-data/README.md)
- **Governance**: [docs/08.operations/04-data/README.md](../../docs/08.operations/04-data/README.md)
- **Status**: Production-Ready / HA Enabled

## 2. Structure

```text
04-data/
├── mng-db/               # Shared Management DB (Postgres/Valkey)
├── postgresql-cluster/   # HA Patroni-based PostgreSQL
├── valkey-cluster/       # 6-node Distributed Cache Cluster
├── minio/                # S3-Compatible Object Storage
├── qdrant/               # Vector Database (RAG Support)
├── opensearch/           # Search & Analytics Engine
├── seaweedfs/            # Distributed Object Storage
├── supabase/             # Integrated Full-Stack Persistence
├── mongodb/              # NoSQL Document (Replica Set)
├── cassandra/            # NoSQL Wide-Column Cluster
├── influxdb/             # Time-Series Engine (TSDB)
├── couchdb/              # NoSQL Document Cluster
└── neo4j/                # Graph Database
```

## 3. Service Matrix

| Service | Category | Profile | Role |
| :--- | :--- | :--- | :--- |
| **mng-db** | SQL/Cache | `mng-data` | Shared core database and cache |
| **postgresql-cluster** | HA SQL | `data` | Patroni-based HA PostgreSQL cluster |
| **valkey-cluster** | HA Cache | `data` | Distributed 6-node Valkey cluster |
| **minio** | Object Storage | `storage` | Primary S3 object storage |
| **opensearch** | Search | `data` | Search engine and analytics dashboard |
| **qdrant** | Vector DB | `ai` | Semantic vector storage for RAG |
| **seaweedfs** | Dist FS | `data` | Distributed filesystem and filer |
| **supabase** | Full Stack | `data` | Managed-like Supabase experience |
| **mongodb** | Document | `data` | NoSQL document storage (Replica Set) |
| **cassandra** | Wide-Column | `data` | Distributed NoSQL cluster |
| **influxdb** | TSDB | `data` | High-performance metrics storage |
| **couchdb** | Document | `data` | Multi-master synced NoSQL cluster |
| **neo4j** | Graph | `data` | Relationship-intensive data store |

## 4. Tech Stack

- **SQL**: PostgreSQL 17 (Spilo), Supabase
- **NoSQL**: MongoDB 8.0, Cassandra 5.0, CouchDB 3.5
- **Caching**: Valkey 8.0 (Redis-compatible)
- **Vector**: Qdrant v1.12
- **Storage**: MinIO, SeaweedFS
- **Graph**: Neo4j 5.26
- **TSDB**: InfluxDB 3.8

## 5. Governance & Persistence

- **Data Path**: All services MUST store data in `${DEFAULT_DATA_DIR}` or `${DEFAULT_MANAGEMENT_DIR}`.
- **Secrets**: Passwords MUST be managed via Docker secrets.
- **HA**: Core services (Postgres, Valkey, MongoDB, CouchDB) use clustering/replication by default.

---

Copyright (c) 2026. Licensed under the MIT License.
