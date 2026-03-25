# PostgreSQL HA Cluster

> High-availability PostgreSQL cluster with Patroni, Etcd, and HAProxy.

## Overview

A robust, failover-capable PostgreSQL cluster based on the Spilo image. It uses Patroni for cluster management, Etcd for distributed consensus, and HAProxy (pg-router) for intelligent routing between the Master and Replica nodes.

## Audience

- DBAs (Performance & Tuning)
- SREs (Failover & Clustering)
- AI Agents (Monitoring & Optimization)

## Scope

### In Scope

- 3-node PostgreSQL Cluster (Patroni)
- 3-node Etcd Cluster (Consensus)
- HAProxy Router (Load Balancing)
- Metrics Exporters (Prometheus)

### Out of Scope

- Application-specific DB schemas
- External DB migrations
- Long-term WAL archiving (outside this tier's local scope)

## Structure

```text
postgresql-cluster/
├── config/             # HAProxy configuration
├── init-scripts/       # Initial SQL bootstrap
├── scripts/            # Spilo entrypoint wrappers
└── docker-compose.yml  # Cluster orchestration
```

## How to Work in This Area

1. Read the [PostgreSQL HA Guide](../../../docs/07.guides/04-data/01.postgresql-ha.md) for bootstrapping.
2. Check `docker-compose.yml` for node environment variables.
3. Use the [Data Runbook](../../../docs/09.runbooks/04-data/README.md) for master recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Engine     | PostgreSQL 17                  | Spilo 4.0 p3              |
| HA Agent   | Patroni                        | Python-based cluster mgr  |
| Consensus  | Etcd v3.6                      | Distributed key-value     |
| Proxy      | HAProxy v3.3                   | TCP Routing Layer         |

## Configuration

### Connection Endpoints

| Endpoint | Port | Mode | Description |
| :--- | :--- | :--- | :--- |
| `pg-router` | 15432 | **RW** | Master node access |
| `pg-router` | 15433 | **RO** | Replica node access |
| `pg-haproxy` | 8404 | **Stats** | HAProxy Dashboard |

## Testing

```bash
# Check Patroni cluster topology
docker exec pg-0 patronictl -c /home/postgres/postgres.yml list

# Test reachability (Master)
psql -h pg-router -p 15432 -U postgres -d postgres -c "SELECT pg_is_in_recovery();"
```

## Change Impact

- Master failover will cause ~5s write downtime.
- Modifying `haproxy.cfg` requires a `pg-router` restart.
- Etcd quorum loss will make the entire cluster read-only.

## Related References

- [03-security](../../03-security/README.md) - Vault integration for DB secrets.
- [docs/08.operations/04-data](../../../docs/08.operations/04-data/README.md) - Data persistence policy.

## AI Agent Guidance

1. Always use `pg-router` instead of direct `pg-0/1/2` hostnames for app traffic.
2. Verify `primary` node status via `patronictl` before performing schema changes.
3. Monitor `etcd_server_has_leader` metrics to ensure cluster health.
