# Kafka Messaging

A distributed event streaming platform for high-throughput, low-latency data pipelines.

## Services

| Service     | Image                             | Role            | Resources       | Port       |
| :---------- | :-------------------------------- | :-------------- | :-------------- | :--------- |
| `kafka`     | `bitnami/kafka:3.9.0`             | Message Broker  | 1 CPU / 2GB RAM | 9092, 9094 |
| `zookeeper` | `bitnami/zookeeper:3.9.1`         | Consensus       | 0.5 CPU / 512MB | 2181       |
| `kafka-ui`  | `provectuslabs/kafka-ui:latest`   | Monitoring UI   | 0.2 CPU / 256MB | 8080 (Int) |

## Networking

| Endpoint                    | Port | Purpose                |
| :-------------------------- | :--- | :--------------------- |
| `kafka-ui.${DEFAULT_URL}`   | 8080 | Dashboard Web UI       |
| `kafka:9092`                | 9092 | Internal PLAINTEXT     |
| `kafka:9094`                | 9094 | External/Host SASL/SSL |

## Persistence

- **Kafka Data**: `/bitnami/kafka` (mounted to `kafka-data` volume).
- **Zookeeper Data**: `/bitnami/zookeeper` (mounted to `zookeeper-data` volume).

## Configuration

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
