# Valkey Cluster Operations Policy

> Global Operations and Maintenance Standards for Valkey Cluster

## Overview

This policy defines the operational standards for the distributed Valkey cluster, focusing on monitoring, data integrity, and security.

## Monitoring Standards

### Key Metrics (SLIs)

| Metric | Threshold | Action |
| :--- | :--- | :--- |
| `cluster_state` | `ok` | Critical Alert if `fail` |
| `connected_clients` | > 5000 | Investigate connection leaks |
| `used_memory_rss` | > 85% limit | Scale up or evict items |
| `evicted_keys` | > 100/sec | Increase memory |

### Health Checks

- **Automated**: Traefik and Docker Compose healthchecks (`valkey-cli ping`).
- **Manual Check**: `valkey-cli -p 6379 cluster info`.

## Data Governance

### Persistence Policy
- **AOF**: `appendfsync everysec` enabled for durability.
- **RDB**: Snapshots every 900s (if 1 change) to ensure point-in-time recovery.

### Memory Management
- **Maxmemory Policy**: `allkeys-lru` (Least Recently Used) is the default evacuation strategy.
- **Eviction**: Monitor `evicted_keys` to ensure capacity planning.

## Security Controls

### Access Control
- **Authentication**: Mandatory password protection via Docker Secrets.
- **Network**: Only accessible within `infra_net`. Management access via SSH/Internal VPN only.

### Encryption
- **At Rest**: Volume encryption at host level (if required).
- **In Transit**: internal cluster bus communication is non-encrypted by default (trusted network). External TLS can be layered via Traefik.

## Maintenance Procedures

### Updating Configuration
1. Modify `infra/04-data/cache-and-kv/valkey-cluster/config/valkey.conf`.
2. Perform rolling restart: `docker compose restart valkey-node-0`, etc.
3. Verify cluster state after each node restart.

### Scaling
- **Vertical**: Update `common-optimizations.yml` resources.
- **Horizontal**: Requires manual slot rebalancing (use `valkey-cli --cluster reshard`).

## Related Documents
- **Guide**: [Technical Guide](../../../07.guides/04-data/cache-and-kv/valkey-cluster.md)
- **Runbook**: [Emergency Recovery](../../../09.runbooks/04-data/cache-and-kv/valkey-cluster.md)
