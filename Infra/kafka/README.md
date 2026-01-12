# Kafka Cluster (KRaft)

## Overview

A 3-node Kafka cluster running in KRaft mode (ZooKeeper-less), accompanied by Schema Registry, Kafka Connect, REST Proxy, and Kafka UI.

## Service Details

### Brokers

- **Nodes**: `kafka-1`, `kafka-2`, `kafka-3` (`confluentinc/cp-kafka:8.1.1`)
- **Mode**: Broker + Controller (Combined)
- **Data Persistence**: `kafka-1-data`, `kafka-2-data`, `kafka-3-data`

### Components

- **Schema Registry**: `schema-registry` (Port `${SCHEMA_REGISTRY_PORT}`)
- **Kafka Connect**: `kafka-connect` (Port `${KAFKA_CONNECT_PORT}`)
- **REST Proxy**: `kafka-rest-proxy` (Port `${KAFKA_REST_PROXY_PORT}`)
- **Kafka UI**: `kafka-ui` (Provectus)
- **Kafka Exporter**: `kafka-exporter` (For Prometheus metrics)

## Environment Variables

- `CLUSTER_ID`: Unique Kafka Cluster ID.
- `KAFKA_NODE_ID`: 1, 2, or 3.
- `KAFKA_CONTROLLER_QUORUM_VOTERS`: `1@kafka-1:9093,2@kafka-2:9093,3@kafka-3:9093`
- `KAFKA_ADVERTISED_LISTENERS`: Configured for both internal (Docker network) and external (Host) access.

## Traefik Configuration

| Service | Host Rule | Entrypoint | TLS | Middleware |
| :--- | :--- | :--- | :--- | :--- |
| **Schema Registry** | `schema-registry.${DEFAULT_URL}` | `websecure` | True | - |
| **Kafka Connect** | `kafka-connect.${DEFAULT_URL}` | `websecure` | True | - |
| **REST Proxy** | `kafka-rest.${DEFAULT_URL}` | `websecure` | True | - |
| **Kafka UI** | `kafka-ui.${DEFAULT_URL}` | `websecure` | True | `sso-auth` |
