# Messaging (05-messaging)

This category manages message brokers, event streaming, and real-time data processing.

## Services

| Service | Profile | Path | Purpose |
| --- | --- | --- | --- |
| Kafka (KRaft Cluster) | `messaging` | `./kafka` | Distributed event streaming platform (3-node KRaft) |
| Schema Registry | `messaging` | `./kafka` | Confluent schema validation (Avro/JSON/Protobuf) |
| Kafka Connect | `messaging` | `./kafka` | Distributed connector framework |
| Kafka REST Proxy | `messaging` | `./kafka` | HTTP interface for Kafka |
| Kafka Exporter | `messaging` | `./kafka` | Prometheus metrics exporter |
| Kafbat UI | `messaging` | `./kafka` | Web management UI (SSO-protected) |
| ksqlDB Server | `messaging-option` | `./ksql` | Streaming SQL engine for Kafka |
| ksqlDB CLI | `ksql` | `./ksql` | Interactive CLI for ksqlDB |
| ksql-datagen | `ksql` | `./ksql` | Sample data generator for ksqlDB |
| RabbitMQ | `rabbitmq` | `./rabbitmq` | AMQP broker for task queues |

## Dependencies

- **KRaft**: Kafka runs in KRaft mode (no ZooKeeper). Each broker is also a controller.
- **Dashboard**: Kafka UI is available at `https://kafbat-ui.${DEFAULT_URL}` (Traefik + SSO middleware).
- **SSO**: `kafbat-ui` and other UIs require Keycloak (from `02-auth`) for authentication.

## Profile Notes

| Profile | Services Activated |
| --- | --- |
| `messaging` | kafka-1, kafka-2, kafka-3, schema-registry, kafka-connect, kafka-rest-proxy, kafka-exporter, kafbat-ui, kafka-init |
| `messaging-option` | ksqldb-server (requires `messaging` to already be running) |
| `ksql` | ksqldb-cli, ksql-datagen |
| `rabbitmq` | rabbitmq |

## File Map

| Path | Description |
| --- | --- |
| `kafka/` | Kafka (KRaft) + Schema Registry + Connect + REST Proxy + UI stack |
| `ksql/` | ksqlDB server and CLI |
| `rabbitmq/` | RabbitMQ AMQP broker (optional tier) |
| `README.md` | Category overview (this file) |
