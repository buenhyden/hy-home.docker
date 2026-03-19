---
layer: infra
---
# Kafka KRaft Streaming Guide

**Overview (KR):** ZooKeeper 없이 KRaft 모드로 동작하는 Kafka 클러스터 구축 및 관리 가이드입니다.

> **Component**: `kafka`
> **Architecture**: Zookeeper-less KRaft Quorum
> **Nodes**: 3 Broker-Controllers
> **Profile**: `messaging`

## 1. Streaming Infrastructure

The stack utilizes KRaft mode (ZooKeeper-less) for simplified metadata management across 3 nodes. Each node acts simultaneously as a **Broker** and a **Controller**, forming a self-contained quorum.

### Technical Specifications

| Service | Internal DNS | Internal Port | Role |
| --- | --- | --- | --- |
| `kafka-1` | `kafka-1` | `19092` | Broker + Controller |
| `kafka-2` | `kafka-2` | `19092` | Broker + Controller |
| `kafka-3` | `kafka-3` | `19092` | Broker + Controller |
| `schema-registry` | `schema-registry` | `8081` | Confluent Schema Registry |
| `kafka-connect` | `kafka-connect` | `8083` | Distributed Connect Worker |
| `kafka-rest-proxy` | `kafka-rest-proxy` | `8082` | REST Proxy (optional) |
| `kafka-exporter` | `kafka-exporter` | `9308` | Prometheus metrics exporter |
| `kafbat-ui` | `kafbat-ui` | `8080` | Web Management UI |
| `kafka-init` | `kafka-init` | — | One-shot topic bootstrap job |

### Provisioning Verification

Check KRaft leader election results:

```bash
docker compose exec kafka-1 kafka-metadata-quorum --bootstrap-server localhost:19092 describe --status
```

Or scan logs for leader election:

```bash
docker compose logs kafka-1 | grep -i "leader election"
```

## 2. Component Layout

The Kafka ecosystem includes:

- **Schema Registry**: Port `8081`. Validates and enforces data schemas (Avro/JSON/Protobuf). Exposed externally at `https://schema-registry.${DEFAULT_URL}`.
- **Kafka Connect**: Distributed data pipeline workers (port `8083`). Exposed at `https://kafka-connect.${DEFAULT_URL}`.
- **Kafka REST Proxy**: HTTP interface for producing/consuming messages (port `8082`). Exposed at `https://kafka-rest.${DEFAULT_URL}`.
- **Kafka Exporter**: Prometheus metrics endpoint (port `9308`). Scraped internally by the observability stack.
- **Kafbat UI**: Graphical management at `https://kafbat-ui.${DEFAULT_URL}` (SSO-protected via Keycloak + Traefik middleware).
- **kafka-init**: One-shot job that creates bootstrap topics (`infra-events`, `application-logs`) on first startup.

## 3. Initial Interaction

Upon `docker compose up -d`, wait ~45s for leader election.

1. Navigate to the UI (`https://kafbat-ui.${DEFAULT_URL}`) and verify the cluster status.
2. Confirm the existence of internal topics (`_schemas`, `__consumer_offsets`, `infra-events`, `application-logs`).
3. Confirm Schema Registry is reachable at `https://schema-registry.${DEFAULT_URL}/subjects`.

## 4. Standard Maintenance

### Topic Lifecycle

```bash
# Create a topic with 3 replicas for safety
docker compose exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --create --topic events.logs --partitions 6 --replication-factor 3

# List all topics
docker compose exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list

# Describe a topic
docker compose exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --describe --topic events.logs

# Delete a topic
docker compose exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --delete --topic events.logs
```

### Consumer Group Management

```bash
# List all consumer groups
docker compose exec kafka-1 kafka-consumer-groups --bootstrap-server localhost:19092 --list

# Describe a group's lag
docker compose exec kafka-1 kafka-consumer-groups --bootstrap-server localhost:19092 \
  --describe --group my-consumer-group
```

## 5. Schema Management

Producers point to `http://schema-registry:8081`. It handles transparent serialization and backward compatibility checks.

```bash
# List registered subjects
curl -s http://localhost:8081/subjects

# Get schema for a subject
curl -s http://localhost:8081/subjects/events.logs-value/versions/latest
```

## 6. Kafka Connect

Manage connectors via the REST API (or the Kafbat UI).

```bash
# List installed connector plugins
curl -s https://kafka-connect.${DEFAULT_URL}/connector-plugins | jq .

# Deploy a connector
curl -X POST -H "Content-Type: application/json" \
  --data @my-connector.json \
  https://kafka-connect.${DEFAULT_URL}/connectors

# Get connector status
curl -s https://kafka-connect.${DEFAULT_URL}/connectors/my-connector/status
```

## 7. Maintenance & Integration References

| Action | Reference |
| --- | --- |
| **Broker Recovery** | Refer to infra troubleshooting runbooks (docs/runbooks/) |
| **Java/Node/Python Clients** | See project onboarding examples |
| **Security** | SSO via Keycloak/Traefik. OAuth2 config in `kafbat-ui/dynamic_config.yaml` |
