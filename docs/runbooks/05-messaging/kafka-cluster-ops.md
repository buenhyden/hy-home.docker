# Runbook: Kafka Cluster & KRaft Recovery

> **Component**: `kafka`
> **Quorum**: KRaft Controller Nodes (nodes 1-3)
> **Endpoint**: `kafka-1:9092` (Internal)

## 1. Issue: Inconsistent Cluster ID

**Given**: Kafka containers restart with "Inconsistent cluster ID" in logs.
**When**: The `meta.properties` file in volumes is corrupted or mismatched after a reset.
**Then**:

1. **Stop Cluster**: `docker compose -f infra/05-messaging/kafka/docker-compose.yml down`
2. **Wipe Volumes**: `docker volume rm infra_kafka-1-data infra_kafka-2-data infra_kafka-3-data` (Caution: Data loss).
3. **Reset**: Ensure `KAFKA_CLUSTER_ID` in your environment matches the initialized ID and restart.

## 2. Issue: Cluster Quorum Lost (Leader Election Failure)

**Given**: Producers fail with "Leader not available".
**When**: KRaft quorum cannot elect a leader due to node outages.
**Then**:

1. **Verify Voters**: Check `KAFKA_CONTROLLER_QUORUM_VOTERS` on all nodes. They must match exactly.
2. **Log Audit**: `docker compose -f infra/05-messaging/kafka/docker-compose.yml logs -f kafka-1`.

## 3. Issue: Schema Registry 401/403 Errors

**Given**: Connectors or Producers fail to register schemas.
**When**: Registry credentials or auth middleware integration is broken.
**Then**:

1. **Check Connectivity**: `curl -u $USER:$PASS http://schema-registry:8081/subjects`.
2. **Restart Registry**: `docker compose restart schema-registry`.

## 4. Manual Topic Maintenance

```bash
# Force delete internal metadata topic if corrupted (Dangerous)
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --delete --topic [topic_name]
```
