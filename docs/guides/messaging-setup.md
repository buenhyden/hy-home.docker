# Messaging Stack Setup Guide

> Configuration patterns and initial setup instructions for the local Apache Kafka (KRaft) and Schema Registry stack.

## 1. Introduction

The messaging component (`infra/05-messaging/kafka/docker-compose.yml`) leverages a 3-node Apache Kafka cluster utilizing the modern KRaft (Kafka Raft) consensus protocol, completely abandoning legacy Zookeeper dependencies.

## 2. Component Layout

The deployment consists of several tightly integrated services:

- **Kafka Brokers (nodes 1-3)**: Act as both data brokers and controller quorums.
- **Schema Registry**: Enforces and validates data schemas (Avro, Protobuf, JSON Schema) over port `8081`.
- **Kafka Connect**: Distributed workers for sourcing and sinking external data streams without custom code.
- **Kafka REST Proxy**: Translates REST API calls directly to native Kafka binary protocol for non-Java external consumers.
- **kafbat-ui**: A comprehensive, web-based graphical interface for exploring topic data, consumer groups, and cluster metrics.

## 3. KRaft Network Binding

Understanding the listener configuration is paramount for routing internal vs external traffic:

- `INTERNAL://0.0.0.0:19092`: Port used locally explicitly for broker-to-broker and container-to-container traffic inside `infra_net`.
- `CONTROLLER://0.0.0.0:9093`: The dedicated KRaft voting protocol port.
- `EXTERNAL://0.0.0.0:9092` (mapped distinctively per container): Reaches out to the host, broadcasting specific `localhost:909x` endpoints for WSL developers consuming from IDE environments.

## 4. Initial Interaction

Upon executing `docker compose up -d`, wait roughly 45 seconds for the controller quorum to elect a leader.

1. Validate the UI by navigating to Traefik's reverse proxy: `https://kafbat-ui.${DEFAULT_URL}`.
2. Confirm the cluster named `local-cluster` displays `Healthy`.
3. Select "Topics" to verify the auto-created internal storage layers like `_schemas` and `__consumer_offsets`.

## 5. Schema Registry Basics

Instead of passing complex schema configurations manually, Kafka Connect and producer containers point to internal DNS `http://schema-registry:8081`.

If you are developing a local Typescript or Python application utilizing Kafka, specify the Schema URL directly. It handles validation on write and transparent deserialization on read, ensuring backward compatibility policies are respected avoiding pipeline crashes.
