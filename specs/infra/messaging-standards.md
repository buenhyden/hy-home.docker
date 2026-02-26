---
title: '[SPEC-MSG-01] Messaging Standards Technical Specification'
status: 'Draft'
version: 'v0.1.0'
owner: 'Messaging Engineer'
tags: ['spec', 'technical', 'messaging', 'kafka', 'kraft']
---

# [SPEC-MSG-01] Messaging Standards Technical Specification

## 1. Overview

This specification defines the standards for Kafka KRaft cluster management and topic lifecycle within Hy-Home.

## 2. Cluster Baseline (KRaft)

- **Quorum**: 3 Controllers (combined with Broker roles).
- **Network Protocol**: `PLAINTEXT` (Internal), `EXTERNAL` (Host map).
- **Metadata**: Unified KRaft protocol on port `9093`.

## 3. Topic Default Policies

| Policy | Value | Description |
| --- | --- | --- |
| `replication-factor` | 3 | Full redundancy across all nodes |
| `min.insync.replicas` | 2 | Minimum write safety gate |
| `cleanup.policy` | `delete` | Default retention strategy |
| `retention.ms` | 604800000 | 7-day default retention |

## 4. Partitioning Standards

- **Standard Tier**: 3 Partitions (Matching cluster size).
- **High Throughput Tier**: 6-12 Partitions (Application logs, telemetry).
- **Critical Control Tier**: 1 Partition (Sequential events).

## 5. Client Integration

- **Schema Registry**: Mandatory versioning for production topics.
- **Connectors**: Standardized JSON/Avro converters.
