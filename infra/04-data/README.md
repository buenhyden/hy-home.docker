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
| influxdb           | `influxdb`      | `./influxdb`           | Optional time-series DB                   |
| couchdb            | `couchdb`       | `./couchdb`            | Optional CouchDB cluster                  |
| mongodb            | (standalone)    | `./mongodb`            | MongoDB replica set (Primary+Secondary+Arbiter) |
| cassandra          | (standalone)    | `./cassandra`          | Apache Cassandra single-node + exporter   |
| neo4j              | (standalone)    | `./neo4j`              | Neo4j graph database                      |
| seaweedfs          | (standalone)    | `./seaweedfs`          | SeaweedFS distributed object storage      |
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
| `minio/`              | S3-compatible storage.                     |
| `opensearch/`         | OpenSearch + Dashboards.                   |
| `qdrant/`             | Vector DB.                                 |
| `influxdb/`           | InfluxDB v2.                               |
| `couchdb/`            | CouchDB cluster.                           |
| `mongodb/`            | MongoDB replica set.                       |
| `cassandra/`          | Apache Cassandra.                          |
| `neo4j/`              | Neo4j graph database.                      |
| `seaweedfs/`          | SeaweedFS distributed object storage.      |
| `supabase/`           | Standalone Supabase stack.                 |
| `README.md`           | Category overview.                         |

## Documentation References

- **Architecture Principles**: [ARCHITECTURE.md](../../ARCHITECTURE.md)
- **Data Technical Blueprints**: [docs/guides/04-data](../../docs/guides/04-data)
- **Platform Guides**: [docs/guides/README.md](../../docs/guides/README.md)
- **Runbooks (Executable)**: [runbooks/README.md](../../runbooks/README.md)
- **Operations History**: [operations/README.md](../../operations/README.md)
