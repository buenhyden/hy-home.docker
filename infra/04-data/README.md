# Data (04-data)

This category manages databases, object storage, and persistence search engines.

## Services

| Service            | Profile         | Path                   | Notes                                     |
| ------------------ | --------------- | ---------------------- | ----------------------------------------- |
| mng-db             | (core)          | `./mng-db`             | Shared PostgreSQL + Valkey + RedisInsight |
| postgresql-cluster | (core)          | `./postgresql-cluster` | Patroni-based HA PostgreSQL               |
| valkey-cluster     | (core)          | `./valkey-cluster`     | 6-node Valkey cluster                     |
| minio              | (core)          | `./minio`              | S3-compatible object storage              |
| opensearch         | (core)          | `./opensearch`         | Search + Dashboards + exporter            |
| qdrant             | (core)          | `./qdrant`             | Vector database (RAG)                     |
| redis-cluster      | `redis-cluster` | `./redis-cluster`      | Optional Redis cluster                    |
| influxdb           | `influxdb`      | `./influxdb`           | Optional time-series DB                   |
| couchdb            | `couchdb`       | `./couchdb`            | Optional CouchDB cluster                  |
| supabase           | (standalone)    | `./supabase`           | Self-hosted Supabase stack                |

## Notes

- Secrets and shared settings are managed at the repo root (`.env`, `secrets/`).
- Many services assume the shared Docker network `infra_net`.

## File Map

| Path                  | Description                                |
| --------------------- | ------------------------------------------ |
| `mng-db/`             | Shared PostgreSQL + Valkey + RedisInsight. |
| `postgresql-cluster/` | Patroni HA PostgreSQL.                     |
| `valkey-cluster/`     | Valkey cluster.                            |
| `redis-cluster/`      | Optional Redis cluster.                    |
| `minio/`              | S3-compatible storage.                     |
| `opensearch/`         | OpenSearch + Dashboards.                   |
| `qdrant/`             | Vector DB.                                 |
| `influxdb/`           | InfluxDB v2.                               |
| `couchdb/`            | CouchDB cluster.                           |
| `supabase/`           | Standalone Supabase stack.                 |
| `README.md`           | Category overview.                         |

> **Note**: This component's local documentation has been migrated to the global repository standards to enforce Spec-Driven Development boundaries.

Please refer to the following global documentation directories for information regarding this service:

- **Architecture & Topology**: [docs/architecture](../../docs/architecture)
- **Configuration & Setup Guides**: [docs/guides](../../docs/guides)
- **Routine Operations**: [operations/](../../operations)
- **Troubleshooting & Recovery**: [runbooks/](../../runbooks)
