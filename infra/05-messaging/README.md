# Messaging (05-messaging)

> Event streaming, message brokering, and real-time data processing tier.

## Overview

The Messaging tier provides the reactive backbone of `hy-home.docker`. It supports both high-throughput event streaming (Kafka) and lightweight task queuing (RabbitMQ), with integrated streaming SQL (ksqlDB) for real-time analytics.

## Service Matrix

| Service | Profile | Port | Purpose |
| :--- | :--- | :--- | :--- |
| **Kafka** | `messaging` | 9092, 19092 | Distributed event streaming (KRaft) |
| **KSqlDB** | `messaging-option` | 8088 | Streaming SQL engine |
| **RabbitMQ** | `rabbitmq` | 5672, 15672 | Lightweight AMQP task queues |

## Navigation Map

### Infrastructure Source

- [Kafka](./kafka/README.md): KRaft cluster + Schema Registry + Connect
- [ksqlDB](./ksql/README.md): Streaming SQL server and CLI
- [RabbitMQ](./rabbitmq/README.md): AMQP broker

### Documentation

- [Messaging Guide](../../docs/07.guides/05-messaging/README.md)
- [Operational Policy](../../docs/08.operations/05-messaging/README.md)
- [Recovery Runbook](../../docs/09.runbooks/05-messaging/README.md)

## Component Taxonomy

### 1. Event Streaming (Kafka)

- **Engine**: 3-node KRaft cluster (no Zookeeper).
- **Tooling**: Schema Registry (Avro/JSON), REST Proxy, Kafbat UI.
- **Persistence**: `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/`.

### 2. Streaming Analytics (ksqlDB)

- **Engine**: ksqlDB Server integrated with Kafka + Schema Registry.
- **Persistence**: `${DEFAULT_DATA_DIR}/ksql`.

### 3. Task Queuing (RabbitMQ)

- **Engine**: RabbitMQ Management (Alpine).
- **Persistence**: `${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq`.

---

## Technical Standards

- **Internal Port**: 19092 (Kafka Internal), 5672 (RabbitMQ).
- **External Port**: 9092/9094/9096 (Kafka), 15672 (RabbitMQ UI).
- **Governance**: All brokers must use dedicated storage volumes under `${DEFAULT_MESSAGE_BROKER_DIR}`.
