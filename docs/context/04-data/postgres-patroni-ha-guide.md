# PostgreSQL Patroni High-Availability Guide

> **Component**: `pg-cluster`
> **Nodes**: 3 (Leader + 2 Replicas)
> **Orchestrator**: Patroni + Etcd
> **Image**: Spilo (Zalando)

## 1. High-Level Topology

The cluster uses Patroni to handle automatic failover. Etcd serves as the Distributed Configuration Store (DCS) for leader election.

- **Nodes**: `pg-0`, `pg-1`, `pg-2`
- **Etcd Quorum**: `etcd-1`, `etcd-2`, `etcd-3`
- **Internal API**: `8008` (Patroni Health/Status)
- **Database Port**: `5432`

## 2. Bootstrapping & Initialization

The cluster is initialized using a temporary `pg-cluster-init` container which injects `init_users_dbs.sql` upon the first successful startup.

### Provisioning Verification

Check logs for successful SQL execution:

```bash
docker compose logs pg-cluster-init
```

> [!NOTE]
> Database migrations should be executed against the HAProxy Writer endpoint (`pg-router:5000`).

## 3. Technical Specifications

### Network Bindings (Internal)

| Service | Internal DNS | Ports | Notes |
| --- | --- | --- | --- |
| `etcd-1..3` | `etcd-1`, `etcd-2`, `etcd-3` | `2379`, `2380` | DCS quorum for Patroni |
| `pg-0..2` | `pg-0`, `pg-1`, `pg-2` | `5432` | Postgres nodes (Spilo/Patroni) |
| `pg-router`| `pg-router` | `5000`, `5001`, `8404` | HAProxy write/read + stats |

### Storage Layout

- **PG Data**: `${DEFAULT_DATA_DIR}/pg/pg[0-2]-data` → `/home/postgres/pgdata`
- **Etcd Data**: `${DEFAULT_DATA_DIR}/etcd/etcd[1-3]-data` → `/etcd-data`

## 3. Reading Cluster Health

To check the current cluster leader and replication lag:

```bash
docker compose exec pg-0 patronictl -c /home/postgres/postgres0.yml list
```

## 4. Database Routing

Traffic is balanced via HAProxy (pg-router) to ensure apps always hit the correct node role:

- **Write (Primary)**: `pg-router:5000`
- **Read (Replica)**: `pg-router:5001`

## 5. Maintenance Operations

### Switchover (Graceful Failover)

Use this command to demote the current leader and promote a replica without downtime:

```bash
docker compose exec pg-0 patronictl -c /home/postgres/postgres0.yml switchover
```

### Data Re-initialization

If a node becomes unsynchronized, use `patronictl reinit` to wipe and re-clone from the master.
