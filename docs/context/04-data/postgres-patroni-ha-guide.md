# PostgreSQL Patroni High-Availability Guide

> **Component**: `pg-cluster`
> **Nodes**: 3 (Leader + 2 Replicas)
> **Orchestrator**: Patroni + Etcd

## 1. High-Level Topology

The cluster uses Patroni to handle automatic failover. Etcd serves as the Distributed Configuration Store (DCS).

- **Internal API**: `8008` (Patroni Health/Status)
- **Database Port**: `5432`

## 2. Reading Cluster Health

To check the current cluster leader and replication lag:

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres0.yml list
```

## 3. Database Routing

Traffic is balanced via HAProxy (pg-router) to ensure apps always hit the correct node role:

- **Write (Primary)**: `pg-router:5000`
- **Read (Replica)**: `pg-router:5001`

## 4. Maintenance Operations

### Switchover (Graceful Failover)

Use this command to demote the current leader and promote a replica without downtime:

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres0.yml switchover
```

### Data Re-initialization

If a node becomes unsynchronized, use `patronictl reinit` to wipe and re-clone from the master.
