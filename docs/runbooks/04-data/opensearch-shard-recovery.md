# Service Runbook: OpenSearch Shard Recovery

_Target Directory: `runbooks/04-data/opensearch-shard-recovery.md`_
_Note: High-priority procedure for data tier availability and cluster health._

---

## 1. Service Overview & Ownership

- **Description**: Centralized logging and search backend.
- **Owner Team**: Data Reliability / SRE
- **Primary Contact**: #ops-search-cluster (Slack)

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| Docker Volumes | Storage | Permanent data loss | [Maintenance](../core/docker-resource-maintenance.md) |
| Loki Driver | Logging | Log ingestion stall | [Monitoring](../core/monitoring-runbook.md) |

## 3. Observability & Dashboards

- **Primary Dashboard**: [OpenSearch Health Dashboard](https://grafana.${DEFAULT_URL}/d/opensearch-health)
- **In-Browser UI**: `https://search-dashboards.${DEFAULT_URL}`

## 4. Operational Scenarios

### Scenario A: Cluster Health `red` (Unassigned Primary Shards)

- **Given**: `GET /_cluster/health` shows `red`.
- **When**: A node was restarted or disk usage stalled.
- **Then**:
  1. [ ] Check Cluster Health: `curl -u admin:$(cat /run/secrets/opensearch_admin_password) -k -X GET "https://localhost:9200/_cluster/health?pretty"`
  2. [ ] Identify shards: `curl -u admin:$(cat /run/secrets/opensearch_admin_password) -k -X GET "https://localhost:9200/_cat/shards?v&h=index,shard,prirep,state,unassigned.reason" | grep UNASSIGNED`
  3. [ ] Force reroute: `curl -u admin:$(cat /run/secrets/opensearch_admin_password) -k -X POST "https://localhost:9200/_cluster/reroute?retry_failed=true"`
- **Expected Outcome**: Health moves to `yellow` or `green`.

### Scenario B: Disk Watermark Hit

- **Given**: Cluster is `yellow`; nodes are read-only.
- **When**: Disk usage > 90% on data nodes.
- **Then**:
  1. [ ] Expand transient limits: (Commands below)

     ```bash
     curl -u admin:$(cat /run/secrets/opensearch_admin_password) -k -X PUT "https://localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'{"transient": {"cluster.routing.allocation.disk.watermark.high": "95%"}}'
     ```

- **Expected Outcome**: Indices become writable; logs resumes flow.

## 5. Safe Rollback Procedure

- [ ] Revert `cluster.routing.allocation.disk.watermark` to default (85%) after disk expansion.

## 6. Data Safety Notes (If Stateful)

- **Retention**: Controlled via ILM (Index Lifecycle Management) policies.
- **Snapshot**: Verify repository presence via `GET /_snapshot/_all`.

## 7. Escalation Path

1. **On-Call**: Data Engineer
2. **Emergency**: VP Platform (@handle)

## 8. Verification Steps (Post-Fix)

- [ ] `GET /_cluster/health` returns `status: green` or `status: yellow`.
- [ ] Log ingestion rate in Grafana shows recovery.
