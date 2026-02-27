# Messaging (05-messaging)

This category manages message brokers, event streaming, and real-time data processing.

## Services

| Service  | Profile | Path        | Purpose                                |
| -------- | ------- | ----------- | -------------------------------------- |
| Kafka    | `messaging`  | `./kafka`   | Distributed event streaming platform   |
| ksqlDB   | `ksql`  | `./ksql`    | Streaming SQL engine for Kafka         |
| RabbitMQ | (n/a)   | `./rabbitmq`| Optional AMQP broker (Placeholder)      |

## Dependencies

- **KRaft**: Kafka runs in KRaft mode (no ZooKeeper in the root-included stack).
- **Dashboard**: Kafka UI is available at `kafbat-ui.${DEFAULT_URL}` (Traefik + SSO middleware).

## File Map

| Path         | Description                            |
| ------------ | -------------------------------------- |
| `kafka/`     | Kafka (KRaft) + Schema Registry + UI stack. |
| `ksql/`      | ksqlDB server and CLI.                 |
| `rabbitmq/`  | Placeholder for RabbitMQ configuration.|
| `README.md`  | Category overview.                     |
