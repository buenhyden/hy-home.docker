# Kafka Cluster (KRaft Mode)

## Overview

A robust 3-node **Kafka Cluster** running in **KRaft mode** (ZooKeeper-less), integrated with the full Confluent Platform ecosystem:

- **Brokers**: 3 Nodes (Controller + Broker roles combined)
- **Schema Management**: Schema Registry
- **Integration**: Kafka Connect (Distributed)
- **Interface**: REST Proxy & Kafka UI (Provectus)
- **Observability**: Kafka Exporter (Prometheus)

## Use Cases

- Event Streaming Platform
- Log Aggregation
- Metrics Collection
- Stream Processing

## Architecture & Networking

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

## Volume Persistence

Data is persisted in named volumes mapped to `/var/lib/kafka/data`:

- `kafka-1-data`
- `kafka-2-data`
- `kafka-3-data`
- `kafka-connect-data` (for Connect specific data)

## Environment Variables (Highlights)

### Brokers (KRaft)

- `KAFKA_PROCESS_ROLES`: `broker,controller` (Combined mode)
- `KAFKA_CONTROLLER_QUORUM_VOTERS`: Defines the KRaft quorum (`1@kafka-1...`).
- `KAFKA_ADVERTISED_LISTENERS`:
  - **Internal**: `PLAINTEXT://kafka-X:19092`
  - **External**: `EXTERNAL://localhost:<HostPort>`

### Kafka Connect

- `CONNECT_GROUP_ID`: `kafka-connect-cluster`
- `CONNECT_BOOTSTRAP_SERVERS`: `kafka-1:19092,kafka-2:19092,kafka-3:19092`
- `CONNECT_KEY/VALUE_CONVERTER`: `JsonConverter` (Schema-less by default)
- `CONNECT_PLUGIN_PATH`: `/usr/share/java,/usr/share/confluent-hub-components`

## Traefik Configuration

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
