---
layer: infra
---

# Messaging Tier: System & Service Context

The `05-messaging` tier provides the backbone for asynchronous communication, event streaming, and task distribution within the `hy-home.docker` cluster.

## 1. Role in Ecosystem

The messaging tier balances two specialized brokers to handle different communication patterns:

- **Kafka (Primary)**: The event streaming backbone. Used for high-throughput, durable log aggregation, and cross-service domain events.
- **RabbitMQ (Secondary)**: The task queue broker. Used for complex routing, per-message acknowledgments, and short-lived transient messages (e.g., job queues).

| Feature | Kafka (Confluent) | RabbitMQ |
| :--- | :--- | :--- |
| **Pattern** | Publish/Subscribe (Log) | Message Queuing (AMQP) |
| **Logic** | Consumer-side offset tracking | Broker-side message routing |
| **Retention** | Long-term (Configurable) | Until consumed (or TTL) |
| **Scaling** | High (Partition-based) | Moderate (Queue-based) |

## 2. Shared Infrastructure

Both brokers share the following infrastructure constants:

- **Network**: `infra_net` internal bridge.
- **Security**: OAuth2 SSO via `02-auth` for management UIs (Kafbat, RabbitMQ Mgmt).
- **Storage**: Persistent volumes mapped to `${DEFAULT_MESSAGE_BROKER_DIR}`.

## 3. Architecture Overview

### Kafka Cluster (KRaft)

The Kafka stack runs in a 3-broker KRaft quorum (ZooKeeper-less), providing high availability and metadata consensus without external dependencies. It includes Schema Registry, Connect, and REST Proxy.

### RabbitMQ (Single-Node)

RabbitMQ is currently deployed as a single-node broker (with clustering support available) for AMQP 0-9-1 compliant services.

## 4. Traffic Flow

1. **Internal**: Services connect via `PLAINTEXT://kafka:19092` or `amqp://rabbitmq:5672`.
2. **External**: Management UIs are exposed via Traefik on subdomains (e.g., `kafbat-ui.hy-home.dev`, `rabbitmq.hy-home.dev`).
3. **Monitoring**: Both brokers export metrics to the `06-observability` stack via specialized exporters.
