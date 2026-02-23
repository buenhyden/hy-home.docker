# Runbook: Kafka Broker/Controller Offline

> Recovery strategies when KRaft nodes fail, crash loops occur, or the topic cluster becomes degraded.

## Context

The infrastructure runs a 3-node combined Broker+Controller KRaft architecture. The election quorum demands a strict majority (`N/2 + 1`). If 2 nodes permanently fail or partition, the cluster loses quorum and immediately denies all state changes (including producer writes and topic creations) falling into a read-only or totally isolated state.

## Symptoms

- Applications report `TimeoutException: Failed to update metadata after 60000 ms.`
- Kafbat UI shows a cluster status of `Offline` or displays missing brokers.
- Container logs (`docker logs kafka-1`) explicitly state `Rejecting request since controller is not active`.

## Resolution Steps

### Method 1: Isolating the Unhealthy Node

1. Identify which broker process is crash looping or hanging:

```bash
docker ps | grep kafka
docker logs kafka-2 --tail 50
```

1. Look for `java.io.IOException: Map failed` (storage full) or `Out of Memory` errors.

2. Attempt a graceful restart of strictly the failing node:

```bash
docker compose -f infra/05-messaging/kafka/docker-compose.yml restart kafka-2
```

1. Monitor the logs to verify it syncs with the Active Controller and `CatchingUp` states resolve back to `InSync`.

### Method 2: Handling Storage / Quorum Corruption

If a node's physical log directory (`kafka-2-data`) becomes corrupted locally:

1. Stop the failing container.

```bash
docker compose -f infra/05-messaging/kafka/docker-compose.yml stop kafka-2
```

1. Destroy the physical mapped volume backing it (e.g., `docker volume rm infra_kafka-2-data`).
2. Re-start the container.

```bash
docker compose -f infra/05-messaging/kafka/docker-compose.yml up -d kafka-2
```

1. **KRaft Recovery:** The fresh container will format a completely blank meta log directory. Assuming the other 2 nodes hold quorum and the replication factor defaults to `3`, the blank node will rapidly begin pulling replication streams from the existing leaders until synchronization reaches 100%.

> [!WARNING]
> Do not execute `Method 2` on multiple nodes simultaneously, or you risk entirely losing the cluster metadata quorum and experiencing total data loss.
