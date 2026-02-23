# Database Clustering & HA Runbook

> **Components**: `postgresql-cluster` (Patroni), `valkey-cluster`

## PostgreSQL HA (Patroni) Troubleshooting

### Split Brain / No Leader

If `etcd` quorum is lost (e.g., 2 nodes down), the cluster becomes Read-Only.

- Check etcd health: `docker compose logs etcd-1`
- Ensure at least 2 etcd nodes are healthy.

### Node Flapping

If a PG node keeps restarting:

1. Check logs: `docker compose logs pg-0`
2. Look for "WalSender" or "Replication" errors.
3. Verify `etcd` connectivity from the PG container.

## Valkey Cluster Troubleshooting

### "Cluster Down"

- Check `valkey-cluster-init` logs.
- Verify node health checks (`valkey-cli ping`).

### "MOVED Error"

- Ensure your client is "Cluster Aware" and properly follows redirects.
- Do not use a standalone classic client for cluster operations.
