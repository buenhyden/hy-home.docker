# Messaging (05-messaging)

## Overview

Event streaming and messaging services. **Kafka** provides the core streaming platform. **ksqlDB** is available as an optional profile for stream processing. **RabbitMQ** is currently a placeholder.

## Services

| Service | Profile | Path | Notes |
| --- | --- | --- | --- |
| Kafka | (core) | `./kafka` | KRaft cluster + Schema Registry + Connect |
| ksqlDB | `ksql` | `./ksql` | Stream SQL engine (optional profile) |
| RabbitMQ | (placeholder) | `./rabbitmq` | No compose yet |

## Run

```bash
# Core streaming
docker compose up -d kafka

# Stream SQL (optional)
docker compose --profile ksql up -d ksqldb-server
```

## Notes

- ksqlDB depends on Kafka and Schema Registry.
- RabbitMQ is a reserved placeholder; no services are enabled yet.

## File Map

| Path | Description |
| --- | --- |
| `kafka/` | Kafka cluster and Confluent stack. |
| `ksql/` | ksqlDB server/CLI and example datagen. |
| `rabbitmq/` | Placeholder for future RabbitMQ. |
| `README.md` | Category overview. |
