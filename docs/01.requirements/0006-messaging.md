---
title: "Messaging Tier (05-messaging) Requirements"
version: "1.4.1"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-19"
layer: "requirements"
artifact_id: "REQ-0006"
created: "2026-03-26"
---

# Messaging Tier (05-messaging) Requirements

## Overview

### Problem and Outcome

Direct calls between components do not scale and risk data loss and reduced
availability. The messaging tier (`05-messaging`) of `hy-home.docker` lowers
that coupling with event streaming on Apache Kafka. The HOME placement provides
the broker, authenticated web administration and metrics. The separate Kafka
LAB owns schema management and the connector boundary. Streaming SQL on Kafka
belongs to the optional lakehouse LAB (SPEC-0262).

### Stakeholders

- **Backend developers**: implement asynchronous patterns and event sourcing,
  for example by collecting system logs and events for analysis and archival.
- **Data engineers**: use topics, schema management and connectors as the
  pipeline input boundary and validate event formats.
- **SREs**: manage broker availability, retention and recovery.
- **Agents**: detect events and drive automated responses.

The owner, @buenhyden, writes, reviews and accepts this package.

## Scope

### In Scope

- HOME: a single Kafka broker in KRaft mode with replication factor 1,
  topic initialization, authenticated HTTP management and broker and consumer
  metrics.
- Kafka LAB: the separate three-broker topology, schema management and the
  connector boundary.

### Constraints and Exclusions

- **Approved placement**: The `kafka-cluster` LAB hosts the training topology,
  Schema Registry and Kafka Connect. The broker REST proxy was removed from
  HOME under [ADR-0062](../02.architecture/02.decisions/0062-home-lab-membership.md).
- **Out of Scope**: Producer and consumer logic inside individual services,
  and external cloud messaging services.
- **Non-goals**: Permanent data storage, which the data tier owns.
- **Agent boundary**: An agent may review topic declarations and query schema
  registration and consumer group status. It must not reset the cluster or
  change a retention period without approval.

**Assumptions.**

Messaging services communicate on a dedicated internal network and keep their
data on dedicated persistent storage.

**Risks.**

- Recovery after a broker failure is not automatic with a single broker and
  replication factor 1.
- A schema change can break backward compatibility for consumers.
- Management access depends on the `02-auth` tier. The lakehouse LAB joins no
  messaging network and reaches Kafka only through an approved endpoint.

## Requirements

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| REQ-0006-FR-0001 | Provide an Apache Kafka event streaming broker in KRaft mode, with multi-broker training kept in a separate LAB. | Direct calls between components do not scale and risk data loss and reduced availability; event streaming on Kafka lowers that coupling. | The root model declares exactly one KRaft broker with replication factor 1 and renders without error with the messaging profile; the three-broker topology renders only as its own LAB project. | must |
| REQ-0006-FR-0003 | Provide schema management for Avro and JSON events and a connector boundary for moving data between Kafka and external systems. | Data engineers use schema management and connectors as the pipeline input boundary and validate event formats. | The isolated Kafka LAB renders schema management and the connector service with health checks and its own broker dependencies; a source connector requires separate approved inputs and execution evidence. | must |
| REQ-0006-FR-0004 | Provide a web-based management UI for the Kafka cluster. | The HOME placement provides authenticated web administration; SREs manage broker availability, retention and recovery. | The management UI requires a login through the platform's OIDC identity provider. | must |
| REQ-0006-FR-0005 | Provide an HTTP access path and a metrics collection boundary for the broker and its consumers. | The HOME placement provides authenticated HTTP management and broker and consumer metrics. | The HOME HTTP management route and exporter render, and observability declares broker and consumer metrics scrape targets; live access and scrape success require separate runtime evidence. | must |

### Functional Requirements

- **REQ-0006-FR-0001**: Provide an Apache Kafka event streaming broker in KRaft mode, with multi-broker training kept in a separate LAB.
- **REQ-0006-FR-0003**: Provide schema management for Avro and JSON events and a connector boundary for moving data between Kafka and external systems.
- **REQ-0006-FR-0004**: Provide a web-based management UI for the Kafka cluster.
- **REQ-0006-FR-0005**: Provide an HTTP access path and a metrics collection boundary for the broker and its consumers.

FR number 0002 (AMQP 0-9-1 task queue on RabbitMQ) is retired because no
RabbitMQ broker is implemented, and is not reused.

### Quality Requirements

This package declares no quality requirement and records no reason why none applies.

## Traceability

### Sources

This package records the owner's requirements for the messaging tier; no upstream
document governs it.

### Verification Links

#### Acceptance Conditions

- **REQ-0006-FR-0001**: The root model declares exactly one KRaft broker with
  replication factor 1 and renders without error when the messaging profile is
  selected; the three-broker topology renders only as its own LAB project.
- **REQ-0006-FR-0003**: The isolated Kafka LAB renders schema management and
  the connector service with health checks and its own broker dependencies.
  A source connector requires separate approved inputs and execution evidence.
- **REQ-0006-FR-0004**: The management UI requires a login through the
  platform's OIDC identity provider.
- **REQ-0006-FR-0005**: The HOME HTTP management route and exporter render,
  and observability declares broker and consumer metrics scrape targets.
  Live access and scrape success require separate runtime evidence.

#### Verification Method

Review the selected HOME and LAB Compose configurations separately for the
broker, schema, UI and metrics declarations. Record live authentication,
connector execution and scrape observations separately in the implementing
Task. The owner named in the frontmatter, @buenhyden, judges each condition
from the applicable evidence and accepts the requirement once every condition
is met.

#### Downstream Links

- **Architecture Description**: [Messaging architecture](../02.architecture/01.descriptions/0005-messaging-architecture.md)
- **ADR**: [ADR-0052 Kafka as the Only Messaging Broker](../02.architecture/02.decisions/0052-kafka-only-messaging-broker.md) (historical; RabbitMQ is not implemented)
- **Retired domain Spec SPEC-0006** (messaging): replaced by the messaging guides, policies and runbooks in the operations catalog under `docs/05.operations/`.
- **Retired requirement REQ-0017** (messaging optimization hardening): retired under SPEC-0169 because every clause named an implementation artifact (a middleware chain, run account, secret mount, compose declaration, or CI gate) rather than a solution-independent need. Its implementation contract lives in the messaging operations catalog policy under `docs/05.operations/`, and its documentation traceability clause moved to REQ-0026-FR-0011.
