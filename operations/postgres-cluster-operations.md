# PostgreSQL Patroni Cluster Operations

This document defines the standard operating procedures for managing the `postgresql-cluster` stack in the `infra/04-data` directory.

## 1. Accessing the Database

Always route application traffic through the HAProxy container (`pg-router`).

- **Write Endpoint** (Primary Node): `pg-router:5000`
- **Read Endpoint** (Replica Nodes): `pg-router:5001`

Do not connect directly to `pg-0`, `pg-1`, or `pg-2` unless performing administrative maintenance.

## 2. Viewing Cluster State

Patroni orchestrates the cluster state via Etcd. You can query the cluster status by executing `patronictl` inside any of the PostgreSQL nodes.

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres0.yml topology
```

This will print a table showing the current Leader, Replicas, and their sync statuses.

## 3. Manual Failover (Switchover)

To manually trigger a leader switchover (e.g., for maintenance on the primary node):

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres0.yml switchover
```

Follow the interactive prompt to select the node you wish to demote and the node you wish to promote.

## 4. Backups and Snapshots

All PostgreSQL data resides on the host at `${DEFAULT_DATA_DIR}/pg`.
The most reliable way to take a snapshot block-level backup:

1. Ensure a replica `pg-1` or `pg-2` is fully synced.
2. Stop the specific replica container: `docker stop pg-1`
3. Back up the mapped volume directory: `tar -czvf pg1-backup.tar.gz ${DEFAULT_DATA_DIR}/pg/pg1-data`
4. Restart the replica: `docker start pg-1` (It will catch up via WAL logs automatically).

## 5. Reinitialization (Destroying Data)

If the cluster enters a completely unrecoverable state, or for testing:

```bash
docker compose -f infra/04-data/postgresql-cluster/docker-compose.yml down -v
sudo rm -rf ${DEFAULT_DATA_DIR}/pg/*
sudo rm -rf ${DEFAULT_DATA_DIR}/etcd/*
docker compose -f infra/04-data/postgresql-cluster/docker-compose.yml up -d
```

> [!CAUTION]
> This destroys ALL database data permanently.

## 6. HAProxy Stats

You can monitor HAProxy load distribution visually by navigating to the Traefik route: `https://pg-haproxy.local.dev` (assuming `DEFAULT_URL=local.dev`).
