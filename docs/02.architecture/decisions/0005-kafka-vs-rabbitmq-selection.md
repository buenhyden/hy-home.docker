---
title: "Polyglot Messaging Strategy (Kafka & RabbitMQ Selection)"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0005"
parent_ids:
- "AD-0005"
created: "2026-03-26"
---
# ADR-0005: Polyglot Messaging Strategy (Kafka & RabbitMQ Selection)

## Context

This document is the decision record for the polyglot messaging strategy that adopts both Apache Kafka and RabbitMQ on the `hy-home.docker` platform. It is a choice made to satisfy the different needs of streaming data and asynchronous task queues.

A modern microservices architecture has two types of messaging patterns interacting together:

1. **High-throughput event streaming**: large-volume data transfer such as log collection, real-time analytics, and data replication.
2. **Asynchronous task queue**: one-off message delivery such as work distribution, push notifications, and delayed execution.

Trying to satisfy both needs with a single solution (Kafka or RabbitMQ) leads to high operational complexity and low efficiency, so an approach that maximizes each tool's strengths is needed.

## Decision

- Select **Apache Kafka** as the **Primary Event Backbone**.
  - For large-scale log collection and durable event stream retention.
  - For data-centric work that needs strong ordering guarantees and replay capability.
- Select **RabbitMQ** as the **Lightweight Task Queue**.
  - For pure asynchronous jobs and low-latency message delivery.
  - For cases that need complex routing rules (Exchange) based on the AMQP standard.
- Adopt **Kafka KRaft Mode** to remove the Zookeeper dependency and simplify cluster management.

## Consequences

- **Positive**:
  - Secures system performance and flexibility by using the optimal tool per use case.
  - Adopting Kafka KRaft mode saves infrastructure resources and simplifies deployment.
- **Trade-offs**:
  - Cost of operating both solutions (image size, memory usage).
  - Developers need to understand the guidelines for which tool to use.

### Explicit Non-goals

- Does not replace Redis Pub/Sub (excludes Zustand/in-memory state uses).
- A Cloud Native Messaging (SQS/SNS) integration strategy is out of scope for this ADR.

## Options Considered

### [Only Apache Kafka]

- Good: convenience of operating a single stack.
- Bad: offset management and partition assignment logic can be overkill for simple task queuing.

### [Only RabbitMQ]

- Good: excellent routing flexibility and simplicity.
- Bad: lacks horizontal scalability and replay capability for large-volume data such as log streaming.

## Traceability

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked in `Related Documents`, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

## Decision Drivers

The decision context above records the applicable drivers and evidence.

## Related Documents

- **PRD**: [../../01.requirements/0006-messaging.md](../../01.requirements/0006-messaging.md)
- **Architecture Description**: [../descriptions/0005-messaging-architecture.md](../descriptions/0005-messaging-architecture.md)
- **Spec**: [../../03.specs/006-messaging/spec.md](../descriptions/0005-messaging-architecture.md)
