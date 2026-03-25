# Valkey Distributed Cluster

> High-performance, 6-node distributed cache cluster (Redis-compatible).

## 1. Context & Objective

The `valkey-cluster` provides a high-throughput, low-latency caching and state storage layer for the `hy-home.docker` ecosystem. It is engineered for automatic partitioning and high availability.

### Topology

- **Structure**: 6 nodes total (3 Primaries + 3 Replicas).
- **Partitioning**: Automated hash slot distribution (16384 slots).

## 2. Requirements & Constraints

- **Compatibility**: Fully compatible with the Redis protocol.
- **Failover**: Supports automatic master-to-replica promotion.
- **Scaling**: Adding or removing nodes requires manual `rebalance` operations.
- **Resources**: Key evictions may occur if memory limits are exceeded.

## 3. Setup & Installation

### Deployment

```bash
# Start the cluster nodes
docker compose up -d
```

### Verification

```bash
# Check cluster state
docker exec valkey-node-0 valkey-cli -p 6379 cluster info

# List cluster nodes and slots
docker exec valkey-node-0 valkey-cli -p 6379 cluster nodes
```

## 4. Usage & Integration

### Configuration
Endpoints are exposed on ports `6379` through `6384`.

### Integration Pointers

- Use `redis-py` or similar clients with cluster support enabled.
- Large `KEYS *` operations are strictly forbidden; use `SCAN`.
- Consult the [Cache & KV Stores Guide](../../../docs/07.guides/04-data/02.cache-kv-dbs.md) for maintenance procedures.

## 5. Maintenance & Safety

### Operational Guardrails

1. Monitor `cluster_slots_assigned` to ensure all 16384 slots are covered.
2. Memory limit policies are defined in [Operations Policy](../../../docs/08.operations/04-data/README.md).
3. Use the [Data Runbook](../../../docs/09.runbooks/04-data/README.md) for node recovery flows.

### Safety Warnings

- Never manually edit `nodes.conf`; this is managed by the engine.
- Ensure all 6 nodes can communicate with each other over the cluster bus port (Port + 10000).

---

Copyright (c) 2026. Licensed under the MIT License.
