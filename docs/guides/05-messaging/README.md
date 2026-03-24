---
layer: infra
---

# Messaging Tier Guides (05-messaging)

Event streaming and message brokers (Kafka, RabbitMQ, ksqlDB).

- [Procedural & Lifecycle Guide](./PROCEDURAL.md): Common messaging operations.
- [System & Service Context](./kafka-context.md): Event streaming architecture.
- [Service Specifics](./kafka-kraft-guide.md): Deep dives into Kafka and RabbitMQ.

## Service Deep Dives

- [Kafka KRaft Mode](./kafka-kraft-guide.md)
- [RabbitMQ Guide](./rabbitmq-guide.md)
- [ksqlDB Context](./ksqldb-context.md)

For technical configuration details (Docker Compose, Config files), see [infra/05-messaging/](../../infra/05-messaging/README.md).
