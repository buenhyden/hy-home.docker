---
title: "Messaging Tier (05-messaging) Requirements"
version: "1.3.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "requirements"
artifact_id: "REQ-0006"
created: "2026-03-26"
---
# Messaging Tier (05-messaging) Requirements

## Overview

### Problem and Goals

Direct calls between components do not scale and risk data loss and reduced
availability. The messaging tier (`05-messaging`) of `hy-home.docker` lowers
that coupling with event streaming on Apache Kafka: a broker, schema
management, a connector boundary, an HTTP access path and metrics. Streaming
SQL processing on top of Kafka is an optional capability of the lakehouse LAB
(SPEC-0262), not of this tier.

## Scope

### Constraints

- **In Scope**: A single Kafka broker in KRaft mode with replication factor 1,
  schema management, the connector boundary, the HTTP access path, the
  management UI, and broker and consumer metrics.
- **Owned elsewhere**: The three-broker training topology is the
  `kafka-cluster` LAB.
- **Out of Scope**: Producer and consumer logic inside individual services,
  and external cloud messaging services.
- **Non-goals**: Permanent data storage, which the data tier owns.
- **Agent boundary**: An agent may review topic declarations and query schema
  registration and consumer group status. It must not reset the cluster or
  change a retention period without approval.

### Assumptions

Messaging services communicate on a dedicated internal network and keep their
data on dedicated persistent storage.

### Risks

- Recovery after a broker failure is not automatic with a single broker and
  replication factor 1.
- A schema change can break backward compatibility for consumers.
- Management access depends on the `02-auth` tier. The lakehouse LAB joins no
  messaging network and reaches Kafka only through an approved endpoint.

## Requirements

### Functional Requirements

- **REQ-0006-FR-0001**: Provide an Apache Kafka event streaming broker in KRaft mode, with multi-broker training kept in a separate LAB.
- **REQ-0006-FR-0003**: Provide schema management for Avro and JSON events and a connector boundary for moving data between Kafka and external systems.
- **REQ-0006-FR-0004**: Provide a web-based management UI for the Kafka cluster.
- **REQ-0006-FR-0005**: Provide an HTTP access path and a metrics collection boundary for the broker and its consumers.

FR number 0002 (AMQP 0-9-1 task queue on RabbitMQ) is retired because no
RabbitMQ broker is implemented, and is not reused.

### Stakeholders and User Needs

- **Backend developers**: implement asynchronous patterns and event sourcing,
  for example by collecting system logs and events for analysis and archival.
- **Data engineers**: use topics, schema management and connectors as the
  pipeline input boundary and validate event formats.
- **SREs**: manage broker availability, retention and recovery.
- **Agents**: detect events and drive automated responses.

### Non-functional Requirements

No separately numbered non-functional requirement is defined.

### Interface Requirements

No separately numbered solution-independent interface requirement is defined.

## Acceptance Criteria

- **REQ-0006-FR-0001**: The root model declares exactly one KRaft broker with
  replication factor 1 and renders without error when the messaging profile is
  selected; the three-broker topology renders only as its own LAB project.
- **REQ-0006-FR-0003**: Schema management and the connector service render
  with their secrets and health checks when their profiles are selected.
- **REQ-0006-FR-0004**: The management UI requires a login through the
  platform's OIDC identity provider.
- **REQ-0006-FR-0005**: The HTTP access path and the exporter render, and the
  broker and consumer metrics are declared as observability scrape targets.
  Live scrape success is claimed only with runtime evidence.

## Related Documents

### Traceability

- **Architecture Description**: [Messaging architecture](../02.architecture/descriptions/0005-messaging-architecture.md)
- **ADR**: [Kafka vs RabbitMQ selection decision](../02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md) (historical; RabbitMQ is not implemented)
- **Retired domain Spec SPEC-0006** (messaging): replaced by the messaging guides, policies and runbooks in the operations catalog under `docs/05.operations/`.
- **Retired requirement REQ-0017** (messaging optimization hardening): retired under SPEC-0169 because every clause named an implementation artifact (a middleware chain, run account, secret mount, compose declaration, or CI gate) rather than a solution-independent need. Its implementation contract lives in the messaging operations catalog policy under `docs/05.operations/`, and its documentation traceability clause moved to REQ-0026-FR-0011.
