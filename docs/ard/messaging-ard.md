---
title: '[ARD-MSG-01] Messaging & Eventing Architecture'
status: 'Approved'
owner: 'Infrastructure Architect'
prd_reference: '../prd/messaging-prd.md'
adr_references: ['../adr/adr-0006-event-streaming-protocol.md']
tags: ['ard', 'messaging', 'infra', 'kafka', 'rabbitmq']
---

# Architecture Reference Document (ARD)

> **Status**: Approved
> **Owner**: Infrastructure Architect
> **PRD Reference**: [[REQ-PRD-MSG-01] Messaging & Eventing PRD](../prd/messaging-prd.md)
> **ADR References**: [ADR-0006](../adr/adr-0006-event-streaming-protocol.md)

---

## 1. Executive Summary

Blueprint for the decoupled communication backbone of the Hy-Home ecosystem. This architecture provides high-availability event streaming via Kafka and lightweight task queuing via RabbitMQ to ensure system resilience and asynchronous scalability.

## 2. Business Goals

- Enable reliable asynchronous integration between microservices.
- Ensure zero-data-loss for critical infrastructure events.
- Standardize message formats across heterogeneous service tiers.

## 3. System Overview & Context

```mermaid
C4Context
    title Messaging System Context
    Container(apps, "App Services", "Producers/Consumers")
    System(msg_bus, "Messaging Tier", "Kafka/RabbitMQ")
    System(persistence, "Data Tier", "Sink Connectors")

    Rel(apps, msg_bus, "Pub/Sub Events")
    Rel(msg_bus, persistence, "Streams to Sinks")
```

## 4. Component Architecture & Tech Stack Decisions

### 4.1 Component Architecture

- **Stream Processor**: Kafka cluster operating in KRaft mode for unified metadata management.
- **Task Broker**: RabbitMQ for low-latency point-to-point task distribution.
- **Contract Guard**: Schema Registry enforcing Avro/Protobuf metadata consistency.

### 4.2 Technology Stack

- **Streaming**: Apache Kafka 3.x
- **Queuing**: RabbitMQ 3.x (Management Plugin enabled)
- **Connectors**: Kafka Connect (S3, Postgres sinks)

## 5. Data Architecture

- **Replication Strategy**: `min.insync.replicas=2` for critical topics to guarantee persistence.
- **Retention Policy**: Tiered retention (7 days for events, infinite for logs/audit).

## 6. Security & Compliance

- **Access Control**: Topic-level ACLs for all producers and consumers.
- **Data in Transit**: Mandatory TLS for all messaging endpoints.

## 7. Infrastructure & Deployment

- **Profile**: Managed under the `messaging` Docker Compose profile.
- **High Availability**: 3-node Kafka cluster with spread across internal sub-nets.

## 8. Non-Functional Requirements (NFRs)

- **Durability**: `min.insync.replicas=2` enforced via Sidecars (see [[REQ-SPEC-AUTO-01] Infrastructure Automation Spec](../../specs/infra/automation/spec.md)).
- **Latency**: End-to-end messaging latency SHALL remain < 100ms (p95).

## 9. Architectural Principles, Constraints & Trade-offs

- **What NOT to do**: Use RabbitMQ for long-term event retention.
- **Chosen Path**: KRaft over Zookeeper to reduce operational complexity and initialization time.
