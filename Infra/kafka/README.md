# Kafka Cluster (KRaft Mode)

## Overview

A robust 3-node **Kafka Cluster** running in **KRaft mode** (ZooKeeper-less), integrated with the full Confluent Platform ecosystem:

- **Brokers**: 3 Nodes (Controller + Broker roles combined)
- **Schema Management**: Schema Registry
- **Integration**: Kafka Connect (Distributed)
- **Interface**: REST Proxy & Kafka UI (Provectus)
- **Observability**: Kafka Exporter (Prometheus)

## Services

- **Kafka Brokers** (`kafka-1`, `kafka-2`, `kafka-3`)
  - **Image**: `confluentinc/cp-kafka:8.1.1`
  - **Role**: KRaft Controller + Broker
- **Schema Registry** (`schema-registry`)
  - **Image**: `confluentinc/cp-schema-registry:8.1.1`
  - **Role**: Avro/Protobuf/JSON Schema management
- **Kafka Connect** (`kafka-connect`)
  - **Image**: `confluentinc/cp-kafka-connect:8.1.1`
  - **Role**: Distributed Connect Worker
- **REST Proxy** (`kafka-rest-proxy`)
  - **Image**: `confluentinc/cp-kafka-rest:8.1.1`
  - **Role**: HTTP Interface for Kafka
- **Kafka UI** (`kafka-ui`)
  - **Image**: `provectuslabs/kafka-ui:v0.7.2`
  - **Role**: Web Management Interface
- **Kafka Exporter** (`kafka-exporter`)
  - **Image**: `danielqsj/kafka-exporter:v1.9.0`
  - **Role**: Prometheus Metrics Exporter

## Networking

All components are assigned **Static IPs** within the `infra_net` network to ensure stable internal communication.

| Service | Role | Static IPv4 | Internal Port | Host Port |
| :--- | :--- | :--- | :--- | :--- |
| `kafka-1` | Broker/Controller | `172.19.0.20` | 19092, 9093 | `${KAFKA_CONTROLLER_1_HOST_PORT}` |
| `kafka-2` | Broker/Controller | `172.19.0.21` | 19092, 9093 | `${KAFKA_CONTROLLER_2_HOST_PORT}` |
| `kafka-3` | Broker/Controller | `172.19.0.22` | 19092, 9093 | `${KAFKA_CONTROLLER_3_HOST_PORT}` |
| `schema-registry` | Schema Registry | `172.19.0.23` | 8081 | `${SCHEMA_REGISTRY_PORT}` |
| `kafka-connect` | Connect Worker | `172.19.0.24` | 8083 | - |
| `kafka-rest-proxy` | HTTP Proxy | `172.19.0.25` | 8082 | - |
| `kafka-ui` | Web Management UI | `172.19.0.26` | 8080 | `${KAFKA_UI_PORT}` |
| `kafka-exporter` | Metrics Exporter | `172.19.0.27` | 9308 | - |

## Persistence

Data is persisted in named volumes mapped to `/var/lib/kafka/data`:

- `kafka-1-data`
- `kafka-2-data`
- `kafka-3-data`
- `kafka-connect-data` (for Connect specific data)

## Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `CLUSTER_ID` | KRaft Cluster ID | `${KAFKA_CLUSTER_ID}` |
| `KAFKA_NODE_ID` | Unique Node identifier | `1`, `2`, `3` |
| `KAFKA_PROCESS_ROLES` | Server Role | `broker,controller` |
| `KAFKA_CONTROLLER_QUORUM_VOTERS`| KRaft Quorum Configuration | `1@kafka-1...` |
| `KAFKA_LISTENERS` | Listener URIs | `PLAINTEXT,CONTROLLER,EXTERNAL` |
| `KAFKA_ADVERTISED_LISTENERS` | Advertised URIs | `kafka-x,localhost` |
| `KAFKA_AUTO_CREATE_TOPICS_ENABLE`| Enable auto topic creation | `true` |
| `CONNECT_GROUP_ID` | Connect Cluster Group ID | `kafka-connect-cluster` |
| `CONNECT_BOOTSTRAP_SERVERS` | Kafka Bootstrap Servers | `kafka-1:19092...` |

## Traefik Integration

Services are exposed via Traefik with TLS enabled.

| Service | Domain | Entrypoint | Auth |
| :--- | :--- | :--- | :--- |
| **Kafka UI** | `kafka-ui.${DEFAULT_URL}` | `websecure` | **SSO Enabled** |
| **Schema Registry** | `schema-registry.${DEFAULT_URL}` | `websecure` | - |
| **Kafka Connect** | `kafka-connect.${DEFAULT_URL}` | `websecure` | - |
| **REST Proxy** | `kafka-rest.${DEFAULT_URL}` | `websecure` | - |

## Usage

### Start Cluster

```bash
docker-compose up -d
```

*Note: The cluster may take a minute to elect a controller and become healthy.*

### Health Check

Run the internal health check command on any broker:

```bash
docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092
```

### Accessing Kafka UI

- **URL**: `https://kafka-ui.<your-domain>`
- **Login**: Protected by SSO (if configured in middlewares).
