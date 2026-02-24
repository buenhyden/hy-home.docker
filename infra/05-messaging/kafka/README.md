# Kafka Messaging

A distributed event streaming platform for high-throughput, low-latency data pipelines.

## Services

| Service | Image | Role | IP |
| :--- | :--- | :--- | :--- |
| `kafka-1,2,3` | `cp-kafka:8.1.1` | KRaft Brokers | `172.19.0.20..22`|
| `schema-reg` | `cp-schema-reg:8.1.1` | Avro Registry | `172.19.0.23` |
| `connect` | `cp-kafka-connect:8.1.1` | Connectors | `172.19.0.24` |
| `kafbat-ui` | `kafbat/kafka-ui:main` | Management Web | `172.19.0.26` |

## Networking

- **Broker Internal**: Port `19092` (PLAINTEXT).
- **Broker External**: Port `9092` (Host-mapped).
- **Web UI**: `kafbat-ui.${DEFAULT_URL}` via Traefik.
- **Metrics**: Exporters on port `9404` (JMX) and `9308` (Kafka Exporter).

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
| `docker-compose.yml` | Kafka + Zookeeper + UI stack definition.    |
| `README.md`          | Messaging overview and producer/consumer docs. |
