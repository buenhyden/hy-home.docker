# Messaging Stack Runbook

> **Components**: `kafka`

## Kafka Troubleshooting

### "Inconsistent Cluster ID"

If you see errors about `CLUSTER_ID` mismatch in logs:

1. Stop the cluster: `docker compose down`
2. Remove volumes: `docker volume rm infra_kafka-1-data infra_kafka-2-data infra_kafka-3-data`
3. Restart: `docker compose up -d`

**\*Note**: This deletes all data! Ensure `KAFKA_CLUSTER_ID` in `.env` remains constant.\*

### Broker Not Joining

Check `KAFKA_CONTROLLER_QUORUM_VOTERS`. All nodes must list the exact same voters string.

### Connect Worker OOM

Kafka Connect is memory intensive. If it crashes, increase the memory limit in `docker-compose.yml` (currently `1.5G`).

### Grafana Kafka Dashboard Shows No Data

**Symptom**: Grafana dashboards show empty panels even though Kafka is running.

**Cause**: Prometheus scrape job name does not match Grafana's `job="kafka"` filter.

**Fix**:

1. Ensure Prometheus uses `job_name: "kafka"` for the Kafka JMX scrape targets.
2. Reload Prometheus configuration.
3. Refresh Grafana dashboards.
