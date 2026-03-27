# Valkey Cluster Recovery Runbook

> Emergency response and restoration procedures for Valkey Cluster failures.

## Overview

This runbook provides step-by-step instructions to recover the Valkey cluster from common failure scenarios.

## Initial Triage

1. **Check Dashboard**: Check Grafana/Homer for service alerts.
2. **Check Container Status**:
   ```bash
   docker compose ps
   ```
3. **Verify Cluster State**:
   ```bash
   docker exec valkey-node-0 valkey-cli -a $PASS cluster info
   ```

## Failure Scenarios

### 1. Single Node Failure (Primary)
When a primary node goes down, a replica should automatically take over.
- **Symptoms**: `cluster_state:fail` (temporarily), then `ok`. One primary missing.
- **Recovery**:
  1. Identify the failed container: `docker ps -a`.
  2. Restart the node: `docker compose start valkey-node-x`.
  3. Verify as replica: `valkey-cli cluster nodes` (The node returns as a replica).

### 2. Complete Quorum Loss (Multiple Primaries Down)
If more than half of the primaries fail simultaneously.
- **Symptoms**: `cluster_state:fail`. All clients blocked.
- **Recovery**:
  1. Restart all nodes: `docker compose up -d`.
  2. If nodes don't rejoin:
     ```bash
     ./scripts/valkey-cluster-init.sh
     ```
  3. Warning: Manual re-init might be destructive if `nodes.conf` is corrupted.

### 3. Slot Inconsistency
- **Symptoms**: Errors like `CLUSTERDOWN The cluster is down`.
- **Recovery**:
  1. Fix slots: `valkey-cli --cluster fix valkey-node-0:6379 -a $PASS`.
  2. Follow prompts to migrate or fix orphan slots.

### 4. Memory Exhaustion
- **Symptoms**: `OOM command not allowed`.
- **Recovery**:
  1. Connect manually: `valkey-cli -p 6379 -a $PASS`.
  2. Force flush (if temporary data): `FLUSHALL` (CAUTION: DESTRUCTIVE).
  3. Adjust `maxmemory` in `config/valkey.conf` and restart.

## Post-Mortem Actions

1. Check logs for the root cause: `docker compose logs --tail=100`.
2. Update operations policy if the threshold was incorrect.
3. Document incident in `docs/90.archive/incidents/`.

## Related Documents
- **Guide**: [Technical Guide](../../../07.guides/04-data/cache-and-kv/valkey-cluster.md)
- **Operations**: [Operations Policy](../../../08.operations/04-data/cache-and-kv/valkey-cluster.md)
