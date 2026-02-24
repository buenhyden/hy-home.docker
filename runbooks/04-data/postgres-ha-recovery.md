# Runbook: PostgreSQL HA & Patroni Recovery

> **Architecture**: [PostgreSQL HA Blueprint](../../docs/context/04-data/postgres-patroni-ha-guide.md)
> **Endpoint**: `pg-router:5000` (Write), `pg-router:5001` (Read)
> **Nodes**: `pg-0`, `pg-1`, `pg-2`

## 1. Issue: Split-Brain or No Leader Election

**Given**: `PatroniMissingLeader` alert triggered, or multiple nodes claim leadership.
**When**: Etcd quorum is lost or network partitions occur.
**Then**:

1. **Identify Topology**: `docker exec -it pg-0 patronictl -c /home/postgres/postgres0.yml topology`.
2. **Restart Etcd**: If Etcd is unhealthy:

   ```bash
   docker compose -f infra/04-data/postgresql-cluster/docker-compose.yml restart etcd-1 etcd-2 etcd-3
   ```

3. **Forced Failover**: If a primary is deadlocked:

   ```bash
   docker exec -it pg-1 patronictl -c /home/postgres/postgres1.yml failover --force
   ```

## 2. Issue: Replica Out of Sync

**Given**: Replica node is running but logs show divergence or lag.
**When**: Transaction logs (WAL) have been recycled before replica could fetch them.
**Then**: Wipe and re-initialize the specific node:

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres0.yml reinit pg-ha [stuck_node_name]
```

## 3. Destructive Re-initialization (Emergency Reset)

**Given**: The entire cluster state is corrupted beyond repair.
**When**: You need a clean slate (WARNING: DATA LOSS).
**Then**:

1. **Stop Stack**: `docker compose -f infra/04-data/postgresql-cluster/docker-compose.yml down`.
2. **Wipe Data**:

   ```bash
   sudo rm -rf ${DEFAULT_DATA_DIR}/pg/*
   sudo rm -rf ${DEFAULT_DATA_DIR}/etcd/*
   ```

3. **Restart**: `docker compose -f infra/04-data/postgresql-cluster/docker-compose.yml up -d`.

## 4. Verification Check

**Given**: Recover is complete.
**When**: Checking cluster health.
**Then**: `patronictl list` must show one "Leader" and two "Replicas" with `running` status and 0 lag.
