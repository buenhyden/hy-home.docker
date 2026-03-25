# Kafka Event Streaming Cluster

> High-performance, 3-node Kafka cluster in KRaft mode.

## Overview

The platform's primary event streaming backbone. This cluster utilizes the Zookeeper-less KRaft architecture for improved scalability and simpler management. It includes a full ecosystem of Schema Registry, Connectors, and a Management UI.

## Audience

- Data Engineers (Pipelines)
- Backend Developers (Event-sourcing)
- AI Agents (Real-time monitoring)

## Scope

### In Scope

- 3-node Kafka Broker Cluster (KRaft)
- Confluent Schema Registry
- Kafka Connect Service
- Kafbat UI (Management Dashboard)
- JMX/Prometheus Monitoring

### Out of Scope

- Custom Kafka Connector development
- Consumer application logic
- Producer-side schema definition

## Structure

```text
kafka/
├── jmx-exporter/       # JMX to Prometheus metrics config
├── kafbat-ui/          # UI configuration
└── docker-compose.yml  # Kafka ecosystem orchestration
```

## How to Work in This Area

1. Read the [Kafka KRaft Guide](../../../docs/07.guides/05-messaging/01.kafka-kraft.md) for bootstrapping.
2. Check `docker-compose.yml` for broker ID and port mappings.
3. Use the [Messaging Runbook](../../../docs/09.runbooks/05-messaging/README.md) for broker recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Engine     | Confluent CP-Kafka             | v8.1.1                    |
| Mode       | KRaft                          | Integrated Metadata log   |
| UI         | Kafbat (Kafka UI)              | Web-based management      |

## Configuration

| Variable | Node 1 | Node 2 | Node 3 |
| :--- | :--- | :--- | :--- |
| `EXTERNAL_PORT` | 9092 | 9094 | 9096 |
| `NODE_ID` | 1 | 2 | 3 |

## Testing

```bash
# List internal topics
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list

# Verify schema registry connectivity
curl -s http://schema-registry.localhost/subjects
```

## Change Impact

- Reducing the replication factor of a topic will decrease durability.
- KRaft controller node restarts may cause a brief leadership election delay.

## AI Agent Guidance

1. Use `kafbat-ui` for visual debugging of message offsets and partitions.
2. New topics MUST be created via `kafka-init` service in `docker-compose.yml` for standardization.
3. Always monitor `UnderReplicatedPartitions` during broker maintenance.
