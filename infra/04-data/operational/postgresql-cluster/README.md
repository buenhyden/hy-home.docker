# PostgreSQL HA Cluster

> High-availability PostgreSQL cluster with Patroni, Etcd, and HAProxy.

## 1. Context & Objective

- **Engine**: PostgreSQL 16
- **Architecture**: Single-Leader HA (Patroni + Etcd + HAProxy)
- **Scale**: Multi-node production grade

The `postgresql-cluster` provides a robust, failover-capable relational database layer based on the Spilo image. It is designed for mission-critical transactional state within the `hy-home.docker` ecosystem.

### Key Components

- **Patroni**: Dynamic cluster management.
- **Etcd**: Distributed consensus and leader election.
- **HAProxy (pg-router)**: Intelligent TCP routing for read/write splitting.

## 2. Requirements & Constraints

- **Storage**: Minimum 10GB persistent storage per node.
- **Memory**: 1GB minimum allocated to PostgreSQL container.
- **Networking**: Isolated internal network for replication.
- **Networking**: Must be accessible via the `infra_net`.
- **Failover**: Master failover causes ~5s write downtime.
- **Quorum**: Etcd quorum loss will force the cluster into read-only mode.

## 3. Setup & Installation

### Deployment

```bash
# Start the cluster
docker compose up -d
```

### Verification

```bash
# Check Patroni cluster topology
docker exec pg-0 patronictl -c /home/postgres/postgres.yml list

# Test reachability (Master)
psql -h pg-router -p 15432 -U postgres -d postgres -c "SELECT pg_is_in_recovery();"
```

## 4. Usage & Integration

### Connection Endpoints

| Endpoint | Port | Mode | Description |
| :--- | :--- | :--- | :--- |
| `pg-router` | 15432 | **RW** | Master node access |
| `pg-router` | 15433 | **RO** | Replica node access |
| `pg-haproxy` | 8404 | **Stats** | HAProxy Dashboard |

### Integration Pointers

- Read the [Relational Databases Guide](../../../docs/07.guides/04-data/01.relational-dbs.md) for deep integration details.
- Use `pg-router` instead of direct `pg-0/1/2` hostnames for application traffic.

## 5. Maintenance & Safety

- **Backups**: Daily snapshots in `${DEFAULT_DATA_DIR}/backups/postgresql`.
- **Scaling**: Add new nodes to `docker-compose.yml` to increase read capacity.
- **Health**: Monitor Patroni via HAProxy dashboard.

### Operational Guardrails

1. Verify `primary` node status via `patronictl` before performing schema changes.
2. Monitor `etcd_server_has_leader` metrics to ensure cluster health.
3. WAL archiving must be verified against the [Data Persistence Policy](../../../docs/08.operations/04-data/README.md).

### Safety Warnings

- Modifying `haproxy.cfg` requires a `pg-router` service restart.
- Never manually delete data directories without stopping Patroni first.

---

Copyright (c) 2026. Licensed under the MIT License.
