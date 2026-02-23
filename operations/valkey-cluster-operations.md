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

The cluster leverages `read_only: false` data writes mounted via defined volumes. However, to execute upgrades safely:

1. Verify replica redundancy.
2. Upgrade replica node images first in `docker-compose.yml`, restarting them individually:

   ```bash
   docker compose -f infra/04-data/valkey-cluster/docker-compose.yml up -d valkey-node-3 valkey-node-4 valkey-node-5
   ```

3. Upgrade master node images afterwards, invoking automatic failover during downtime.

> [!CAUTION]
> If multiple master tiers are restarted simultaneously, cluster quorum drops, causing immediate read/write denial until nodes rejoin. Only restart the entire cluster during verified maintenance windows.
