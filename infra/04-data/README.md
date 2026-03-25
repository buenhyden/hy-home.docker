# Data Tier (04-data)

> Central repository for databases, object storage, and persistence engines.

## 1. Context & Objective

The `04-data` tier provides a polyglot persistence layer for the `hy-home.docker` ecosystem. It manages all stateful data ranging from transactional SQL to high-velocity time-series and semantic vector data. It is engineered for high availability (HA) and durability, ensuring that platform state is preserved across restarts and failures.

### Target Personas

- **Storage Engineers**: Database performance and reliability.
- **Application Developers**: Selecting the right persistence engine.
- **AI Agents**: Automated backup, migration, and state management.

## 2. Requirements & Constraints

### Infrastructure Requirements

- **Data Path**: All services MUST store data in `${DEFAULT_DATA_DIR}`.
- **Secrets**: Passwords MUST be managed via Docker secrets.
- **Networking**: All data services are isolated within `infra_net`.

### Constraints

- Never perform `DROP` operations in production without manual gate verification.
- Policy changes (WAL levels, max connections) require full cluster re-validation.

## 3. Setup & Installation

### Core Stack Deployment

Deployment is handled via individual `docker-compose.yml` files in subdirectories.

| Category | Technology | Notes |
| :--- | :--- | :--- |
| SQL | PostgreSQL 17 (Spilo) | HA with Patroni/Etcd |
| NoSQL | MongoDB, CouchDB, Cassandra | Polyglot persistence |
| Cache | Valkey 8.0 | 6-node Distributed Clstr |
| Vector | Qdrant v1.12 | AI/RAG Support |
| Graph | Neo4j | Relationship data |
| Search | OpenSearch | Analytics & Dashboard |
| Object | MinIO / SeaweedFS | S3-Compatible |

### Verification

```bash
# Verify PostgreSQL HA status
docker exec pg-0 patronictl -c /home/postgres/postgres.yml list

# Verify Valkey cluster
docker exec valkey-node-0 valkey-cli -p 6379 cluster nodes
```

## 4. Usage & Integration

### Service Matrix (Core)

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `pg-router` | PostgreSQL | `data` | 15432 (RW) / 15433 (RO) |
| `valkey-cluster` | Redis | `data` | 6379-6384 |
| `minio` | S3/HTTP | `storage` | 9000 (API) / 9001 (Console) |
| `qdrant` | HTTP/gRPC | `ai` | 6333 / 6334 |
| `opensearch` | HTTP | `analytics` | 9200 |

### Integration Guidelines

1. Read the [Relational Databases Guide](../../docs/07.guides/04-data/01.relational-dbs.md) for cluster setup.
2. Follow the [Cache & KV Stores Guide](../../docs/07.guides/04-data/02.cache-kv-dbs.md) for cache management.

## 5. Maintenance & Safety

### Health & Monitoring

- Check [Operations Policy](../../docs/08.operations/04-data/README.md) for backup standards.
- Consult the [Data Runbook](../../docs/09.runbooks/04-data/README.md) for recovery.

### Safety Protocols

1. Use the `pg-router` entrypoint for all database connections to ensure failover support.
2. Check `available_slots` before adding new nodes to the Valkey cluster.
3. Always verify snapshot integrity before initiating a restore runbook.

---

Copyright (c) 2026. Licensed under the MIT License.
