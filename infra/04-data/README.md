# Data (04-data)

## Overview

Persistent data stores for the stack: relational databases, caches, search, object storage, and vector databases. Most services are included from the repo root; a few are optional (profiles) or standalone.

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

## Run

```bash
# Core data services (example subset)
docker compose up -d mng-db postgresql-cluster minio qdrant

# Optional stacks
docker compose --profile redis-cluster up -d
docker compose --profile influxdb up -d
docker compose --profile couchdb up -d

# Standalone (not included at root)
cd infra/04-data/supabase
docker compose up -d
```

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
