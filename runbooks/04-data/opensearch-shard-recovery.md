# Runbook: OpenSearch Shard Recovery

## Given

- OpenSearch cluster status is `red` or `yellow`.
- Some indices show `UNASSIGNED` shards.

## When

- A node was restarted or disk usage hit the floor-watermark.

## Then

### 1. Check Cluster Health

```bash
curl -u admin:$(cat /run/secrets/opensearch_admin_password) -k -X GET "https://localhost:9200/_cluster/health?pretty"
```

### 2. Identify Unassigned Shards

```bash
curl -u admin:$(cat /run/secrets/opensearch_admin_password) -k -X GET "https://localhost:9200/_cat/shards?v&h=index,shard,prirep,state,unassigned.reason" | grep UNASSIGNED
```

### 3. Trigger Manual Allocation (If needed)

```bash
curl -u admin:$(cat /run/secrets/opensearch_admin_password) -k -X POST "https://localhost:9200/_cluster/reroute?retry_failed=true"
```

### 4. Adjust Watermarks (If disk issue)

```bash
curl -u admin:$(cat /run/secrets/opensearch_admin_password) -k -X PUT "https://localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "transient": {
    "cluster.routing.allocation.disk.watermark.low": "85%",
    "cluster.routing.allocation.disk.watermark.high": "90%",
    "cluster.info.update.interval": "1m"
  }
}'
```
