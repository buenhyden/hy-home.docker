# Kafka KRaft Streaming Guide

> **Component**: `kafka`
> **Architecture**: Zookeeper-less KRaft Quorum
> **Nodes**: 3 Broker-Controllers

## 1. Streaming Infrastructure

We utilize a modern KRaft (Kafka Raft) architecture where nodes manage their own metadata without an external Zookeeper.

- **Internal Broker Port**: `9092` (Inside `infra_net`)
- **Controller Quorum Port**: `9093`
- **Metadata Log Path**: `/var/lib/kafka/data/__cluster_metadata-0`

## 2. Standard Maintenance

### Topic Lifecycle

```bash
# Create a topic with 3 replicas for safety
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --create --topic events.logs --partitions 6 --replication-factor 3
```

## 3. Schema Management & Registry

Producers should utilize the integrated Schema Registry for Avro/JSON serialization:

- **Registry Port**: `8081`

## 4. Administrative Visualizer

Manage topics, consumer groups, and connectors via the Kafbat UI:

- **URL**: `https://kafka-ui.${DEFAULT_URL}`
