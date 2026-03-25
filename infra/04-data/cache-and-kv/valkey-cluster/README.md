# Valkey Distributed Cluster

> High-performance, 6-node distributed cache cluster (Redis-compatible).

## Overview

A distributed Valkey cluster providing high-throughput, low-latency caching and state storage. It consists of 6 nodes (3 primaries + 3 replicas) with automatic partitioning across hash slots.

## Audience

- SREs (Cluster balancing)
- AI Agents (Cache monitoring)

## Scope

- 6-node Valkey Cluster
- Automatic cluster initialization
- Redis-compatible protocol support

## Structure

```text
valkey-cluster/
├── config/             # Valkey configuration (valkey.conf)
├── scripts/            # Startup and init scripts
└── docker-compose.yml  # Cluster orchestration
```

## How to Work in This Area

1. Read the [Valkey Cluster Guide](../../../docs/07.guides/04-data/02.valkey-cluster.md) for maintenance.
2. Check `scripts/valkey-cluster-init.sh` for partitioning logic.
3. Use the [Data Runbook](../../../docs/09.runbooks/04-data/README.md) for node recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Engine     | Valkey 9.0                     | Alpine-based              |
| Protocol   | Redis                          | Fully compatible          |
| Topology   | 3 Master / 3 Replica           | Automatic Failover        |

## Configuration

| Variable | Description | Initial Port |
| :--- | :--- | :--- |
| `VALKEY0_PORT` | Node 0 Port | 6379 |
| `VALKEY1_PORT` | Node 1 Port | 6380 |
| `...` | ... | ... |

## Testing

```bash
# Check cluster state
docker exec valkey-node-0 valkey-cli -p 6379 cluster info

# List cluster nodes and slots
docker exec valkey-node-0 valkey-cli -p 6379 cluster nodes
```

## Change Impact

- Adding/removing nodes requires manual `rebalance` operations.
- Key evictions may occur if memory limits are exceeded without proper tuning.

## Related References

- [02-auth](../../02-auth/README.md) - Used for session caching.
- [docs/08.operations/04-data](../../../docs/08.operations/04-data/README.md) - Memory limit policies.

## AI Agent Guidance

1. Use `redis-py` or similar clients with cluster support enabled.
2. Large `KEYS *` operations are strictly forbidden; use `SCAN`.
3. Monitor `cluster_slots_assigned` to ensure 16384 slots are covered.
