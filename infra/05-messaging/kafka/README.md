# Kafka Messaging

A distributed event streaming platform for high-throughput, low-latency data pipelines.

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `kafka-1..3` | `confluentinc/cp-kafka:8.1.1` | KRaft brokers/controllers |
| `schema-registry` | `confluentinc/cp-schema-registry:8.1.1` | Schema Registry |
| `kafka-connect` | `confluentinc/cp-kafka-connect:8.1.1` | Connect worker (optional) |
| `kafka-rest-proxy` | `confluentinc/cp-kafka-rest:8.1.1` | REST Proxy (optional) |
| `kafka-exporter` | `danielqsj/kafka-exporter` | Prometheus exporter |
| `kafka-init` | `confluentinc/cp-kafka:8.1.1` | One-shot topic bootstrap |
| `kafbat-ui` | `ghcr.io/kafbat/kafka-ui:main` | Web UI (SSO via Traefik middleware) |

## Networking

- **Internal (infra_net)**: Brokers listen on `${KAFKA_INTERNAL_PORT:-19092}` via service DNS (`kafka-1`, `kafka-2`, `kafka-3`).
- **External (host-mapped)**: Each broker maps `${KAFKA_EXTERNAL_PORT:-9092}` to a host port (`${KAFKA_EXTERNAL_1_HOST_PORT:-9092}`, `${KAFKA_EXTERNAL_2_HOST_PORT:-9094}`, `${KAFKA_EXTERNAL_3_HOST_PORT:-9096}`).
- **Schema Registry / Connect / REST Proxy**: Exposed via Traefik hostnames (e.g., `schema-registry.${DEFAULT_URL}`).
- **Kafka UI**: `https://kafbat-ui.${DEFAULT_URL}` (SSO via `sso-auth@file`).

## Persistence

- **Volumes**: `kafka-1-data`, `kafka-2-data`, `kafka-3-data`.
- **Mount Path**: `/var/lib/kafka/data`.

## Configuration

- **Clustering**: KRaft mode (No Zookeeper).
- **Security**: SSO enabled for `kafbat-ui` via Keycloak middleware.

### Key Variables

| Variable          | Description          | Value                  |
| :---------------- | :------------------- | :--------------------- |
| `KAFKA_CLUSTER_ID`| Unique Cluster ID    | `${KAFKA_CLUSTER_ID}`  |
| `DEFAULT_URL`     | Host domain          | `${DEFAULT_URL}`       |

## File Map

| Path                 | Description                                 |
| -------------------- | ------------------------------------------- |
| `docker-compose.yml` | Kafka (KRaft) + Schema Registry + UI stack definition. |
| `README.md`          | Messaging overview and producer/consumer docs. |
