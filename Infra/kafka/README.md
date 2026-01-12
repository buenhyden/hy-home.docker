# Apache Kafka (KRaft Mode)

## Overview

A 3-node Kafka cluster running in KRaft mode (no Zookeeper), along with Schema Registry, Kafka Connect, REST Proxy, and Kafka UI.

## Services

- **kafka-1, kafka-2, kafka-3**: Kafka Brokers acting as both Controller and Broker.
  - Ports:
    - `9093`: Controller
    - `19092`: Internal PLAINTEXT
    - External Port: `${KAFKA_CONTROLLER_PORT}`
- **schema-registry**: Confluent Schema Registry.
  - URL: `https://schema-registry.${DEFAULT_URL}`
- **kafka-connect**: Distributed Kafka Connect.
  - URL: `https://kafka-connect.${DEFAULT_URL}`
- **kafka-rest-proxy**: Kafka REST Proxy.
  - URL: `https://kafka-rest.${DEFAULT_URL}`
- **kafka-ui**: Web UI for managing Kafka clusters.
  - URL: `https://kafka-ui.${DEFAULT_URL}`
- **kafka-exporter**: Prometheus exporter for Kafka metrics.

## Configuration

### Environment Variables

- `KAFKA_PROCESS_ROLES`: `broker,controller`
- `KAFKA_CONTROLLER_QUORUM_VOTERS`: Defines the voting members for KRaft.
- `CLUSTER_ID`: Unique Cluster ID.
- `KAFKA_ADVERTISED_LISTENERS`: Critical for client connectivity.
- `SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS`: Connection to Kafka cluster.

### Volumes

- `kafka-1-data`: `/var/lib/kafka/data`
- `kafka-2-data`: `/var/lib/kafka/data`
- `kafka-3-data`: `/var/lib/kafka/data`
- `kafka-connect-data`: `/var/lib/kafka-connect`

## Networks

- `infra_net`
  - Fixed IPs assigned for stable inter-node communication (`172.19.0.20-27`).

## Traefik Routing

- **Schema Registry**: `schema-registry.${DEFAULT_URL}`
- **Kafka Connect**: `kafka-connect.${DEFAULT_URL}`
- **REST Proxy**: `kafka-rest.${DEFAULT_URL}`
- **Kafka UI**: `kafka-ui.${DEFAULT_URL}`
