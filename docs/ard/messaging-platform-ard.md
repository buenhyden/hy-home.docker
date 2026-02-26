---
title: '[ARD-MSG-01] Messaging Platform Architecture'
status: 'Draft'
version: 'v0.1.0'
owner: 'Messaging Architect'
tags: ['ard', 'architecture', 'messaging', 'kafka', 'kraft']
---

# [ARD-MSG-01] Messaging Platform Architecture

## 1. Overview

This platform utilizes Apache Kafka in KRaft mode (Kafka Raft Metadata mode) to eliminate ZooKeeper dependencies. It provides a distributed, durable, and high-throughput messaging backbone.

## 2. Cluster Topology

- **Quorum**: 3-node cluster with combined Broker and Controller roles.
- **Protocol**: KRaft mode for unified metadata management.
- **Client Access**: Multi-listener setup (Internal, Controller, External).

## 3. High Availability Strategy

- **Replication**: Default `replication-factor: 3` for all production-grade topics.
- **Min ISR**: `min.insync.replicas: 2` to ensure write durability.
- **Partitioning**: Dynamic partitioning based on throughput requirements (Default: 3-6).

## 4. Ecosystem Components

- **Schema Registry**: Confluent Schema Registry for Avro/Protobuf versioning.
- **Kafka Connect**: Distributed workers for source/sink integration.
- **REST Proxy**: HTTP interface for non-native Kafka clients.
- **UI**: Kafbat (formerly Kafka UI) for administrative visibility.

## 5. Security Standards

- **Isolation**: Network isolation via `infra_net`.
- **RBAC**: Consumer group and client authentication strategies (TBD).
