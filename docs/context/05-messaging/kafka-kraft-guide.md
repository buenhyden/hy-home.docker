# Kafka KRaft Streaming Guide

> **Component**: `kafka`
> **Architecture**: Zookeeper-less KRaft Quorum
> **Nodes**: 3 Broker-Controllers

## 1. Streaming Infrastructure

The stack utilizes KRaft mode (ZooKeeper-less) for simplified metadata management across 3 nodes.

### Technical Specifications

| Service | IPv4 | Internal Port | Role |
| --- | --- | --- | --- |
| `kafka-1` | `172.19.0.20` | `19092` | Broker + Controller |
| `kafka-2` | `172.19.0.21` | `19092` | Broker + Controller |
| `kafka-3` | `172.19.0.22` | `19092` | Broker + Controller |
| `schema-registry`| `172.19.0.23` | `8081` | Confluent SR |
| `ksql-server` | `172.19.0.24` | `8088` | [Hardened: Standard] |

### Provisioning Verification

Check KRaft leader election results:

```bash
docker logs kafka-1 | grep "Leader election"
```

## 2. Component Layout

The Kafka ecosystem includes:

- **Schema Registry**: Port `8081`. Validates data schemas (Avro/JSON).
- **Kafka Connect**: Distributed data workers.
- **Kafbat UI**: Graphical management at `https://kafka-ui.${DEFAULT_URL}`.

## 3. Maintenance & Integration

| Action | Reference | Link |
| --- | --- | --- |
| **Recovery** | Broker Offline | [Runbook](../../../runbooks/05-messaging/kafka-broker-offline.md) |
| **Ops**      | Cluster Ops   | [Runbook](../../../runbooks/05-messaging/kafka-cluster-ops.md) |
| **Connect**  | Java/Node/Py  | [Onboarding](../../../examples/README.md#pubsub) |

## 3. Initial Interaction

Upon `docker compose up -d`, wait ~45s for leader election.

1. Navigate to the UI and verify the `local-cluster` status.
2. Confirm the existence of internal topics (`_schemas`, `__consumer_offsets`).

## 4. Standard Maintenance

### Topic Lifecycle

```bash
# Create a topic with 3 replicas for safety
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --create --topic events.logs --partitions 6 --replication-factor 3
```

## 5. Schema Management

Producers point to `http://schema-registry:8081`. It handles transparent serialization and backward compatibility checks.
