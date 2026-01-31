# Messaging (05-messaging)

## Overview

Event streaming and messaging services. **Kafka** provides the core streaming platform for high-throughput event processing. **ksqlDB** is available for real-time stream SQL processing. **RabbitMQ** provides a robust AMQP-based message broker for reliable asynchronous communication.

## Services

| Service | Profile | Path | Notes |
| --- | --- | --- | --- |
| Kafka | (core) | `./kafka` | KRaft cluster + Schema Registry + Connect |
| ksqlDB | `ksql` | `./ksql` | Stream SQL engine (optional profile) |
| RabbitMQ | `rabbitmq` | `./rabbitmq` | AMQP 0-9-1 broker + Management UI |

## Run

```bash
# Core streaming (Kafka)
docker compose up -d kafka

# Stream SQL (optional)
docker compose --profile ksql up -d ksqldb-server

# Message Broker (optional)
docker compose --profile rabbitmq up -d rabbitmq
```

## Notes

- **ksqlDB** depends on Kafka and Schema Registry.
- **RabbitMQ** includes a management interface on port `15672`.

## File Map

| Path | Description |
| --- | --- |
| `kafka/` | Kafka cluster and Confluent stack. |
| `ksql/` | ksqlDB server/CLI and example datagen. |
| `rabbitmq/` | RabbitMQ service definition and documentation. |
| `README.md` | Category overview. |
