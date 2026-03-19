# Kafka Messaging

A distributed event streaming platform for high-throughput, low-latency data pipelines. Runs in KRaft mode (ZooKeeper-less) with a 3-node broker-controller quorum.

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `kafka-1..3` | `confluentinc/cp-kafka:8.1.1` | KRaft broker/controllers (combined role) |
| `schema-registry` | `confluentinc/cp-schema-registry:8.1.1` | Schema Registry (Avro/JSON/Protobuf) |
| `kafka-connect` | `confluentinc/cp-kafka-connect:8.1.1` | Connect worker (connector framework) |
| `kafka-rest-proxy` | `confluentinc/cp-kafka-rest:8.1.1` | HTTP REST interface for Kafka |
| `kafka-exporter` | `danielqsj/kafka-exporter:v1.9.0` | Prometheus metrics exporter |
| `kafka-init` | `confluentinc/cp-kafka:8.1.1` | One-shot topic bootstrap job |
| `kafbat-ui` | `ghcr.io/kafbat/kafka-ui:main` | Web UI (SSO via Traefik middleware) |

## Networking

- **Internal (infra_net)**: Brokers listen on `${KAFKA_INTERNAL_PORT:-19092}` via service DNS (`kafka-1`, `kafka-2`, `kafka-3`).
- **Controller (internal)**: Brokers communicate via `${KAFKA_CONTROLLER_PORT:-9093}` (not exposed externally).
- **External (host-mapped)**: Each broker maps an external port for local development:
  - `kafka-1`: `${KAFKA_EXTERNAL_1_HOST_PORT:-9092}`
  - `kafka-2`: `${KAFKA_EXTERNAL_2_HOST_PORT:-9094}`
  - `kafka-3`: `${KAFKA_EXTERNAL_3_HOST_PORT:-9096}`
- **Schema Registry / Connect / REST Proxy**: Exposed via Traefik hostnames:
  - `https://schema-registry.${DEFAULT_URL}`
  - `https://kafka-connect.${DEFAULT_URL}`
  - `https://kafka-rest.${DEFAULT_URL}`
- **Kafka UI**: `https://kafbat-ui.${DEFAULT_URL}` (SSO via `sso-auth@file`).
- **Kafka Exporter**: Port `9308` (internal only, scraped by Prometheus).

## Persistence

| Volume | Mount Path | Host Path |
| --- | --- | --- |
| `kafka-1-data` | `/var/lib/kafka/data` | `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/kafka1-data` |
| `kafka-2-data` | `/var/lib/kafka/data` | `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/kafka2-data` |
| `kafka-3-data` | `/var/lib/kafka/data` | `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/kafka3-data` |
| `kafka-connect-data` | `/var/lib/kafka-connect` | `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/kafka-connect` |

## Configuration

- **Clustering**: KRaft mode (No Zookeeper). `KAFKA_PROCESS_ROLES: broker,controller`.
- **JMX**: JMX exporter agent enabled on port `9404` per broker, with the JAR in `./jmx-exporter/`.
- **Security**: SSO enabled for `kafbat-ui` via Keycloak OAuth2 middleware.

### Key Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `KAFKA_CLUSTER_ID` | Unique cluster ID (must be pre-generated) | `${KAFKA_CLUSTER_ID}` |
| `DEFAULT_URL` | Host domain for Traefik routing | `${DEFAULT_URL}` |
| `KAFKA_INTERNAL_PORT` | Broker-to-broker + client internal port | `19092` |
| `KAFKA_EXTERNAL_PORT` | External-facing listener port per broker | `9092` |
| `KAFKA_CONTROLLER_PORT` | KRaft controller quorum port | `9093` |
| `SCHEMA_REGISTRY_PORT` | Schema Registry listen port | `8081` |
| `KAFKA_CONNECT_PORT` | Kafka Connect REST port | `8083` |
| `KAFKA_REST_PROXY_PORT` | REST Proxy listen port | `8082` |
| `KAFKA_UI_PORT` | Kafbat UI listen port | `8080` |
| `KAFKA_EXPORTER_PORT` | Prometheus exporter port | `9308` |

## File Map

| Path | Description |
| --- | --- |
| `docker-compose.yml` | **Primary**: Kafka (KRaft) + Schema Registry + Connect + REST Proxy + UI + Exporter |
| `docker-compose.dev.yml` | Single-node Kafka dev stack (kafka-dev, schema-registry-dev, connect-dev, kafbat-ui-dev) |
| `docker-compose-kafka.yml` | **Legacy**: Older Kafka 7.x config. Do not use for new deployments. |
| `jmx-exporter/` | JMX Prometheus Java agent JAR and `kafka-config.yaml` |
| `kafbat-ui/` | `dynamic_config.yaml` — Kafbat UI OAuth2 / RBAC config |
| `README.md` | This file |

> **⚠️ Kafbat UI OAuth2**: `kafbat-ui/dynamic_config.yaml` contains a `<replace_me>` placeholder for `clientSecret`. This must be replaced with the actual Keycloak client secret before deploying.

## Documentation References

| Topic | Guide |
| --- | --- |
| Architecture & Components | [kafka-kraft-guide.md](../../../docs/guides/05-messaging/kafka-kraft-guide.md) |
| Routine Operations | [kafka-operations.md](../../../docs/guides/05-messaging/kafka-operations.md) |
| System Context | [kafka-context.md](../../../docs/guides/05-messaging/kafka-context.md) |
