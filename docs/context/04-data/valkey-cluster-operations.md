# Valkey Cluster Operations Blueprint

> Standard operating procedures for the 6-node Valkey (Redis-compatible) cluster.

## 1. Description

This document establishes operational patterns for managing the Valkey memory-store cluster (`infra/04-data/valkey-cluster/docker-compose.yml`), comprised of 3 master nodes and 3 replica nodes.

## 2. Infrastructure Topology

- **Nodes**: `valkey-node-[0-5]` bridging ports `6379-6384` to their corresponding internal ports.
- **Cluster Initialization**: Handled automatically on initial deployment by a one-shot `valkey-cluster-init` container, running `valkey-cli --cluster create ... --cluster-replicas 1`.
- **Exporters**: Monitored collectively by stateless `valkey-exporter` feeding into Prometheus.
- **UI Management**: Connected to a `mng-valkey-insight` container (RedisInsight) mapped under the separate Mng-DB stack.

## 3. Core Administrative Actions

### Checking Cluster Health

You can query cluster health via any participating node, relying on `valkey_password` secret mounts:

```bash
docker exec -it valkey-node-0 sh -c 'valkey-cli -a $(cat /run/secrets/valkey_password) -p ${VALKEY0_PORT} cluster info'
```

You should expect `cluster_state:ok` and `cluster_known_nodes:6`.

### Hard Reloads & Upgrades

For manual failover and rolling upgrade procedures, refer to the dedicated playbook: `runbooks/04-data/valkey-cluster-manual-failover.md`.
