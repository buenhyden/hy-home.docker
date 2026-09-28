---
title: "Messaging Tier (05-messaging) Product Requirements"
version: "1.0.3"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "requirements"
artifact_id: "REQ-0006"
parent_ids: []
created: "2026-03-26"
---
# Messaging Tier (05-messaging) Product Requirements

## Problem and Goals

This document defines the product requirements for the messaging tier (`05-messaging`) of the `hy-home.docker` architecture. It supports asynchronous communication across the system through high-performance event streaming (Kafka) and a lightweight task queue (RabbitMQ). Streaming SQL processing (Flink) is currently owned by the `04-data/lakehouse` implementation and its operations documentation.

### Problem Statement

In the current complex microservice and infrastructure environment, direct communication between components does not scale well and can cause data loss risk and reduced system availability. A layered messaging solution is needed to handle diverse traffic characteristics (high throughput vs. simple queuing).

## Stakeholders and User Needs

Provide a robust, dedicated messaging infrastructure that lowers coupling between system components and enables real-time event processing and reliable message delivery.

### Personas

- **Backend Developers**: Use the messaging infrastructure to implement asynchronous patterns and event sourcing.
- **Data Engineers**: Use Kafka topics, Schema Registry, and Kafka Connect as the data pipeline input boundary.
- **SREs**: Manage cluster availability, retention policy, and recovery procedures.
- **AI Agents**: Used for real-time event detection and automated response handling.

### Key Use Cases

- **STORY-01**: Collect system logs and events into Kafka for real-time analysis and archival.
- **STORY-02**: Place long-running tasks in a RabbitMQ queue for processing by asynchronous workers.
- **STORY-03**: Use Schema Registry and Kafka Connect to validate the event format and connector boundary.

## Functional Requirements

- **REQ-0006-FR-0001**: Provide Apache Kafka (KRaft mode). A single file, `infra/05-messaging/kafka/docker-compose.yml`, holds both topologies. The root `docker-compose.yml` includes it unconditionally; the `messaging`/`dev` profiles select the single `kafka-1` broker, and the `messaging-cluster` profile selects `kafka-2` and `kafka-3`. A 3-broker configuration requires selecting `messaging` and `messaging-cluster` together.
- **REQ-0006-FR-0002**: Support the standard AMQP 0-9-1 protocol via RabbitMQ.
- **REQ-0006-FR-0003**: Provide Schema Registry for Avro/JSON schema management.
- **REQ-0006-FR-0004**: Provide web-based management UIs (Kafbat, RabbitMQ Management).
- **REQ-0006-FR-0005**: Provide an operations API and metrics collection boundary through Kafka REST Proxy and Kafka Exporter.

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0006-FR-0001**: `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh` passes with 0 failures on the root-included messaging configuration.
- **REQ-0006-FR-0002**: `bash scripts/hardening/check-all-hardening.sh 05-messaging` blocks regressions in image pinning, router middleware, SSO, and path baselines.

## Constraints

- **In Scope**:
  - Kafka Cluster (KRaft)
  - Schema Registry & Kafka Connect
  - RabbitMQ Broker
  - Kafka REST Proxy
  - Kafka Exporter and the broker JMX exporter agent
- **Out of Scope**:
  - Consumer/producer application logic inside individual services.
  - External cloud messaging services (AWS SQS, and so on).
- **Non-goals**:
  - Permanently storing data at the messaging tier (the responsibility of the Data tier).

### AI Agent Requirements

- **Allowed Actions**: Review topic declarations against `kafka-init`, query schema registration status, query consumer group status.
- **Disallowed Actions**: Full cluster reset, arbitrary changes to the message retention period.

## Risks

- **Risks**: Possible delayed partition rebalancing after a Kafka node failure. Risk of backward-compatibility violations on schema changes.
- **Dependencies**: Depends on the `02-auth` tier for authentication and authorization management. The Flink consumer/processing boundary depends on `04-data/lakehouse/flink`.
- **Assumptions**: All nodes communicate within `kafka_net` and store data on dedicated volumes.

## Traceability

- **Architecture Description**: [Messaging architecture descriptions](../02.architecture/descriptions/0005-messaging-architecture.md)
- **Spec**: [Messaging technical specification](../02.architecture/descriptions/0005-messaging-architecture.md)
- **Plan**: Messaging standardization plan
- **ADR**: [Kafka vs RabbitMQ selection decision](../02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md)
