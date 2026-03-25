# Messaging Tier (05-messaging)

> Event streaming, message brokering, and real-time data processing tier.

## Overview

The `05-messaging` tier provides the reactive backbone of the `hy-home.docker` ecosystem. It supports high-throughput event streaming via Kafka and lightweight task queuing via RabbitMQ. Integrated streaming SQL (ksqlDB) enables real-time analytics and transformations as data flows through the platform.

## Audience

이 README의 주요 독자:

- Backend Developers (Event-driven patterns)
- Data Engineers (Stream processing)
- SREs (Broker reliability & scaling)
- AI Agents (Automated topic provisioning)

## Scope

### In Scope

- Apache Kafka Cluster (KRaft mode)
- Confluent Schema Registry & Kafka Connect
- ksqlDB Streaming SQL Engine
- RabbitMQ AMQP Broker
- Messaging UI & Management consoles

### Out of Scope

- Application-specific consumer logic
- External cloud messaging (AWS SQS/SNS)
- Long-term cold storage of events (handled by `04-data`)

## Structure

```text
05-messaging/
├── kafka/              # Kafka cluster, Connect, Registry, UI
├── ksql/               # ksqlDB server configuration
├── rabbitmq/           # RabbitMQ broker configuration
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Kafka KRaft Guide](../../docs/07.guides/05-messaging/01.kafka-kraft.md) for cluster ops.
2. Follow the [RabbitMQ Operations Guide](../../docs/07.guides/05-messaging/02.rabbitmq-ops.md) for queues.
3. Check the [Operations Policy](../../docs/08.operations/05-messaging/README.md) for retention.
4. Consult the [Messaging Runbook](../../docs/09.runbooks/05-messaging/README.md) for recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Streaming  | Apache Kafka                   | v8.1.1 (Confluent Spilo)  |
| Mode       | KRaft (Zookeeper-less)         | 3-node HA                 |
| Schema     | Schema Registry                | Avro/JSON support         |
| AMQP       | RabbitMQ                       | Management-enabled        |
| Analytics  | ksqlDB                         | Streaming SQL             |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `kafka-1/2/3` | Kafka/TCP | `messaging` | 9092, 19092 |
| `schema-registry`| HTTP | `messaging` | 8081 |
| `rabbitmq` | AMQP/HTTP | `rabbitmq` | 5672, 15672 (UI) |
| `kafbat-ui` | HTTP | `messaging` | 8080 |

## Configuration

- **Data Path**: All broker data MUST be stored in `${DEFAULT_MESSAGE_BROKER_DIR}`.
- **Secrets**: Security tokens and passwords MUST use Docker secrets.
- **Networking**: High-throughput traffic is confined to the `infra_net`.

## Testing

```bash
# Verify Kafka cluster health via Kafbat UI
docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092

# Test RabbitMQ connectivity
docker exec rabbitmq rabbitmq-diagnostics check_running
```

## Change Impact

- Modifying Kafka partition counts is irreversible without data loss/re-balancing.
- Changing Schema Registry compatibility levels may break downstream consumers.
- RabbitMQ queue purging will permanently delete non-persistent messages.

## Related References

- [04-data](../04-data/README.md) - Storing processed events.
- [01-gateway](../01-gateway/README.md) - routing to Messaging UIs.

## AI Agent Guidance

1. Always use the `Schema Registry` for any new topic schemas.
2. Ensure `replication-factor: 3` for all production-grade topics.
3. Check consumer lag metrics before scaling producer throughput.
4. RabbitMQ queues should use TTLs and DLXs as per the messaging policy.
