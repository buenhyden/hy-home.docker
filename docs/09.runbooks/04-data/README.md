# Data Emergency Runbook (04-data)

> Standard operating procedures for data-tier incidents.

## Severity 1: Data Loss or Corruption

### Postgres Cluster Split-Brain

**Symptoms**: Multiple nodes claiming leader status in Patroni.

**Resolution**:

1. Identify the node with the most recent timeline.
2. Stop all PostgreSQL nodes.
3. Clean up ETCD cluster state for the Postgres namespace.
4. Restart nodes one-by-one, starting with the designated leader.

### Storage Exhaustion

**Symptoms**: Containers stuck in `Exited (1)` or `I/O Error` in logs.

**Resolution**:

1. Check host disk usage with `df -h`.
2. Clean up old container logs or unused Docker volumes (`docker system prune`).
3. If persistent volumes are full, expand the underlying storage and resize the filesystem.

---

## Severity 2: Service Degradation

### High Latency in Search (OpenSearch)

**Symptoms**: Slow response times or search timeouts.

**Resolution**:

1. Verify JVM heap usage via OpenSearch Dashboards.
2. Check for long-running queries or excessive indexing pressure.
3. Scale the cluster by adding data nodes if resource consumption is consistently high.

---

## Navigation

- [Infrastructure Source](../../../infra/04-data/README.md)
- [Guides](../../../docs/07.guides/04-data/README.md)
- [Operational Policies](../../../docs/08.operations/04-data/README.md)
