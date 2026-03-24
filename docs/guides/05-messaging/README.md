---
layer: infra
---

# Messaging Tier Guides (05-messaging)

Event streaming and message brokers (Kafka, RabbitMQ, ksqlDB).

## Navigation Map

| View | Command | Focus |
| :--- | :--- | :--- |
| **Architecture** | `[LOAD:CONTEXT]` | Traffic flow and component roles |
| **Installation** | `[LOAD:SETUP]` | Initial bootstrap and verification |
| **Operations** | `[LOAD:USAGE]` | Daily tasks and connection strings |
| **Maintenance** | `[LOAD:PROCEDURAL]` | Lifecycle and recovery |

## Categorized Service Index

### Core Messaging

- **[CONTEXT.md](./CONTEXT.md)**: Unified context for Kafka and RabbitMQ.
- **[SETUP.md](./SETUP.md)**: Installation and bootstrapping guides.
- **[USAGE.md](./USAGE.md)**: Common operations and troubleshooting.
- **[PROCEDURAL.md](./PROCEDURAL.md)**: Scaling and lifecycle procedures.

### Service Deep Dives

- **[Kafka KRaft Mode](./kafka-kraft-guide.md)**: Detailed KRaft internals.
- **[RabbitMQ Guide](./rabbitmq-guide.md)**: Advanced AMQP routing and clustering.
- **[ksqlDB Context](./ksqldb-context.md)**: Stream processing with ksqlDB.

For technical configuration details (Docker Compose, Config files), see [infra/05-messaging/](../../infra/05-messaging/README.md).
