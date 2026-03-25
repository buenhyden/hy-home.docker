# Kafka Messaging (kafka)

> Distributed event streaming platform powered by Confluent CP 8.1.1.

## Overview

High-throughput, low-latency event streaming cluster running in **KRaft mode** (ZooKeeper-less). This stack includes the core cluster, schema validation, connector framework, and management UIs.

## Service Matrix

| Service | Image | Port | Role |
| :--- | :--- | :--- | :--- |
| **Kafka 1-3** | `cp-kafka:8.1.1` | 9092, 19092 | KRaft Broker/Controllers |
| **Schema Registry** | `cp-schema-registry:8.1.1` | 8081 | Avro/JSON/Protobuf validation |
| **Kafka Connect** | `cp-kafka-connect:8.1.1` | 8083 | Connector framework |
| **Kafbat UI** | `kafka-ui:main` | 8080 | Web Management UI |

## Connectivity Map

- **Internal**: Brokers listen on `19092` (intra-cluster).
- **External**: host-mapped ports `9092`, `9094`, `9096` for development.
- **Web UIs**:
  - [Kafbat UI](https://kafbat-ui.${DEFAULT_URL}) (SSO protected)
  - [Schema Registry](https://schema-registry.${DEFAULT_URL})
  - [Kafka Connect](https://kafka-connect.${DEFAULT_URL})

## Setup & Persistence

### 1. Persistence

- **Brokers**: `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/kafka[1-3]-data`
- **Connect**: `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/kafka-connect`

### 2. Initialization

The `kafka-init` service automatically creates the following topics:

- `infra-events`: System-level event stream (3 partitions, factor 3).
- `application-logs`: Centralized logging stream (6 partitions, factor 3).

---

## Operations

### Monitoring

- **Exporter**: Kafka Exporter at port `9308` for Prometheus.
- **JMX**: JMX Prometheus agent at port `9404` on each broker.

### Security

- **SSO**: `kafbat-ui` uses Keycloak via Traefik middleware (`sso-auth@file`).
- **OAuth2**: Check `kafbat-ui/dynamic_config.yaml` for client secrets.

## Navigation
- [Messaging Tier Overview](../README.md)
- [Kafka Guide](../../../docs/07.guides/05-messaging/01.kafka-kraft.md)
- [Operational Policy](../../../docs/08.operations/05-messaging/README.md)
