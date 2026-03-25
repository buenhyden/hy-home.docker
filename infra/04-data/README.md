# Data Tier (04-data)

> Central repository for databases, object storage, and persistence engines.

## Overview

The `04-data` tier provides a polyglot persistence layer for the `hy-home.docker` ecosystem. It manages all stateful data ranging from transactional SQL to high-velocity time-series and semantic vector data. It is engineered for high availability (HA) and durability, ensuring that platform state is preserved across restarts and failures.

## Audience

이 README의 주요 독자:

- DBAs & SREs (Database reliability)
- Application Developers (Persistence selection)
- AI Agents (Automated backup & migration)

## Scope

### In Scope

- Transactional Databases (Postgres, MongoDB, etc.)
- Caching Engines (Valkey Cluster)
- Object Storage (MinIO, SeaweedFS)
- Vector & Graph Databases (Qdrant, Neo4j)

### Out of Scope

- Application-level schema migrations (handled by apps)
- Secret generation (handled by `03-security`)
- External cloud DBs (RDS, Atlas)

## Structure

```text
04-data/
├── mng-db/               # Shared Management DB (Postgres/Valkey)
├── postgresql-cluster/   # HA Patroni-based PostgreSQL
├── valkey-cluster/       # 6-node Distributed Cache Cluster
├── minio/                # S3-Compatible Object Storage
├── qdrant/               # Vector Database (RAG Support)
└── ...                   # Other polyglot engines
```

## How to Work in This Area

1. Read the [PostgreSQL HA Guide](../../docs/07.guides/04-data/01.postgresql-ha.md) for cluster setup.
2. Follow the [Valkey Cluster Guide](../../docs/07.guides/04-data/02.valkey-cluster.md) for cache management.
3. Check [Operations Policy](../../docs/08.operations/04-data/README.md) for backup standards.
4. Consult the [Data Runbook](../../docs/09.runbooks/04-data/README.md) for recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| SQL        | PostgreSQL 17 (Spilo)          | HA with Patroni/Etcd      |
| Cache      | Valkey 8.0                     | 6-node Distributed Clstr  |
| Vector     | Qdrant v1.12                   | AI/RAG Support            |
| Search     | OpenSearch                     | Analytics & Dashboard     |
| Object     | MinIO / SeaweedFS              | S3-Compatible             |

## Service Matrix (Core)

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `pg-router` | PostgreSQL | `data` | 15432 (RW) / 15433 (RO) |
| `valkey-cluster` | Redis | `data` | 6379-6384 |
| `minio` | S3/HTTP | `storage` | 9000 (API) / 9001 (Console) |

## Configuration

- **Data Path**: All services MUST store data in `${DEFAULT_DATA_DIR}`.
- **Secrets**: Passwords MUST be managed via Docker secrets.
- **Networking**: All data services are isolated within `infra_net`.

## Testing

```bash
# Verify PostgreSQL HA status
docker exec pg-0 patronictl -c /home/postgres/postgres.yml list

# Verify Valkey cluster
docker exec valkey-node-0 valkey-cli -p 6379 cluster nodes
```

## Change Impact

- Restarting `pg-router` will cause temporary connection drops.
- Changing `DEFAULT_DATA_DIR` requires manual migration of existing volumes.
- Policy changes (WAL levels, max connections) require full cluster re-validation.

## Related References

- [03-security](../03-security/README.md) - Secret management for DBs.
- [01-gateway](../01-gateway) - routing to DB UIs (Adminer, MinIO Console).

## AI Agent Guidance

1. Never perform `DROP` operations in production without manual gate verification.
2. Use the `pg-router` entrypoint for all database connections to ensure failover support.
3. Check `available_slots` before adding new nodes to the Valkey cluster.
4. Always verify snapshot integrity before initiating a restore runbook.
