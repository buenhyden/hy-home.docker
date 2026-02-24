# Kafka KRaft Streaming Guide

> **Component**: `kafka`
> **Architecture**: Zookeeper-less KRaft Quorum
> **Nodes**: 3 Broker-Controllers

## 1. Streaming Infrastructure

We utilize a modern KRaft (Kafka Raft) architecture where nodes manage their own metadata without an external Zookeeper.

- **Internal Broker Port**: `19092` (Inside `infra_net`)
- **Controller Quorum Port**: `9093`
- **External Port (WSL)**: `9092`
- **Metadata Log Path**: `/var/lib/kafka/data/__cluster_metadata-0`

## 2. Component Layout

The Kafka ecosystem includes:

- **Schema Registry**: Port `8081`. Validates data schemas (Avro/JSON).
- **Kafka Connect**: Distributed data workers.
- **Kafbat UI**: Graphical management at `https://kafka-ui.${DEFAULT_URL}`.

## 3. Initial Interaction

Upon `docker compose up -d`, wait ~45s for leader election.

1. Navigate to the UI and verify the `local-cluster` status.
2. Confirm the existence of internal topics (`_schemas`, `__consumer_offsets`).

## 4. Standard Maintenance

### Topic Lifecycle

```bash
# Create a topic with 3 replicas for safety
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --create --topic events.logs --partitions 6 --replication-factor 3
```

## 5. Schema Management

Producers point to `http://schema-registry:8081`. It handles transparent serialization and backward compatibility checks.
