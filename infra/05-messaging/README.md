# Messaging (05-messaging)

This category manages message brokers, event streaming, and real-time data processing.

## Services

| Service  | Profile | Path        | Purpose                                |
| -------- | ------- | ----------- | -------------------------------------- |
| Kafka    | (core)  | `./kafka`   | Distributed event streaming platform   |
| ksqlDB   | `ksql`  | `./ksql`    | Streaming SQL engine for Kafka         |
| RabbitMQ | (n/a)   | `./rabbitmq`| Optional AMQP broker (Placeholder)      |

## Dependencies

- **Zookeeper**: Kafka uses the internal Zookeeper (or KRaft mode if enabled).
- **Dashboard**: Kafka UI is available at `kafka-ui.${DEFAULT_URL}`.

## File Map

| Path         | Description                            |
| ------------ | -------------------------------------- |
| `kafka/`     | Kafka, Zookeeper, and UI stack.        |
| `ksql/`      | ksqlDB server and CLI.                 |
| `rabbitmq/`  | Placeholder for RabbitMQ configuration.|
| `README.md`  | Category overview.                     |
