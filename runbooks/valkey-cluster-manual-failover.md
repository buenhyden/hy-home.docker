# Runbook: Valkey Cluster Manual Failover & Upgrades

> **Component**: `valkey-cluster`
> **Profile**: `compose-file` (Standard)
> **Severity**: MEDIUM (Service Interruption)

## 1. Description

This runbook defines how to perform a graceful failover and rolling upgrade of a 6-node Valkey cluster to ensure high availability during maintenance.

## 2. Steps

### 2.1. Verify Cluster Health

Before starting, ensure the cluster is in a healthy state.

```bash
docker exec -it valkey-node-0 sh -c 'valkey-cli -a $(cat /run/secrets/valkey_password) -p ${VALKEY0_PORT} cluster info'
```

### 2.2. Rolling Upgrade (Replica First)

1. Update the image tag in `infra/04-data/valkey-cluster/docker-compose.yml`.
2. Restart the **Replica** nodes first:

   ```bash
   docker compose -f infra/04-data/valkey-cluster/docker-compose.yml up -d valkey-node-3 valkey-node-4 valkey-node-5
   ```

3. Wait for them to sync with their masters.

### 2.3. Master Failover

Restarting a Master node will trigger an automatic failover to its corresponding healthy replica.

1. Restart Master nodes one-by-one:

   ```bash
   docker compose -f infra/04-data/valkey-cluster/docker-compose.yml restart valkey-node-0
   # Wait 30s
   docker compose -f infra/04-data/valkey-cluster/docker-compose.yml restart valkey-node-1
   # Wait 30s
   docker compose -f infra/04-data/valkey-cluster/docker-compose.yml restart valkey-node-2
   ```

## 3. Troubleshooting

If cluster quorum drops (`cluster_state:fail`), ensure at least 3 master nodes (original or promoted replicas) are reachable. Re-run `valkey-cluster-init` if nodes lose track of the cluster mesh.
