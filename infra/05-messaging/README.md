# Messaging Tier (05-messaging)

> Event streaming, message brokering, and real-time data processing tier.

## Overview

The `05-messaging` tier provides the reactive backbone of the `hy-home.docker` ecosystem. It supports high-throughput event streaming via Kafka and lightweight task queuing via RabbitMQ. Streaming SQL is currently owned by `infra/04-data/analytics/ksql`, not by this tier.

## Audience

이 README의 주요 독자:

- Backend Developers (Event-driven patterns)
- Data Engineers (Kafka topics, schemas, and connectors)
- SREs (Broker reliability & scaling)
- AI Agents (Automated topic provisioning)

## Scope

### In Scope

- Apache Kafka Cluster (KRaft mode)
- Confluent Schema Registry & Kafka Connect
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
├── rabbitmq/           # RabbitMQ broker configuration
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Kafka Guide](../../docs/05.operations/guides/05-messaging/kafka.md) for cluster ops.
2. Follow the [RabbitMQ Guide](../../docs/05.operations/guides/05-messaging/rabbitmq.md) for queues.
3. Check the [Operations Policy](../../docs/05.operations/policies/05-messaging/README.md) for topic, secret, and queue controls.
4. Consult the [Messaging Runbook](../../docs/05.operations/runbooks/05-messaging/README.md) for recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Streaming  | Confluent Kafka                | `confluentinc/cp-kafka:8.2.1` |
| Mode       | KRaft (Zookeeper-less)         | root dev single broker; service-local full 3 broker compose |
| Schema     | Schema Registry                | `confluentinc/cp-schema-registry:8.2.1` |
| Connect    | Kafka Connect / REST Proxy     | Confluent CP `8.2.1`      |
| AMQP       | RabbitMQ                       | `rabbitmq:4.3.1-management-alpine` |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `kafka-1` | Kafka/TCP | `messaging`, `dev` | 9092, 19092 |
| `kafka-2/3` | Kafka/TCP | `messaging` in service-local full compose only | 9094/9096, 19092 |
| `schema-registry`| HTTP | `messaging` | 8081 |
| `rabbitmq` | AMQP/HTTP | `messaging`, `messaging-option` | 5672, 15672 (UI) |
| `kafbat-ui` | HTTP | `messaging` | 8080 |

## Configuration

- **Data Path**: All broker data MUST be stored in `${DEFAULT_MESSAGE_BROKER_DIR}`.
- **Secrets**: Security tokens and passwords MUST use Docker secrets.
- **Networking**: High-throughput traffic is confined to the `infra_net`.

## Testing

```bash
# Verify root-included messaging compose
HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh

# Verify Kafka broker API from a running container
docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092

# Test RabbitMQ connectivity
docker exec rabbitmq rabbitmq-diagnostics check_running
```

## Change Impact

- Modifying Kafka partition counts is irreversible without data loss/re-balancing.
- Changing Schema Registry compatibility levels may break downstream consumers.
- RabbitMQ queue purging will permanently delete non-persistent messages.

## Related Documents

- [04-data](../04-data/README.md) - Storing and analyzing processed events.
- [ksqlDB analytics README](../04-data/analytics/ksql/README.md) - Streaming SQL implementation.
- [01-gateway](../01-gateway/README.md) - routing to Messaging UIs.
- [Kafka guide](../../docs/05.operations/guides/05-messaging/kafka.md)
- [RabbitMQ guide](../../docs/05.operations/guides/05-messaging/rabbitmq.md)

## AI Agent Guidance

1. Always use the `Schema Registry` for any new topic schemas.
2. Use `replication-factor: 3` only in the full 3 broker Kafka compose; root dev single broker topics are development-only.
3. Check consumer lag metrics before scaling producer throughput.
4. RabbitMQ queues should use TTLs and DLXs as per the messaging policy.
