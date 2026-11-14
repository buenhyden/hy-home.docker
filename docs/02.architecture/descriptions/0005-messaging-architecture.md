---
title: "Messaging Architecture Description"
version: "1.5.2"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "architecture"
artifact_id: "AD-0005"
parent_ids:
- "REQ-0006"
created: "2026-03-26"
---

# Messaging Architecture Description

## Overview

### Purpose and Readers

`05-messaging` is the optional Kafka event-streaming boundary. The HOME
implementation has one Kafka KRaft broker, Kafbat UI, Kafka Exporter and a
topic-init job. Schema Registry and Kafka Connect (Debezium CDC) moved to the LAB
`labs/kafka-cluster` by the ADR-0062 amendment of 2026-11-10. No second broker
family is part of the architecture.

### System Boundary

- **Owns:** Kafka topics, configuration and KRaft state, metrics export and
  Kafbat administration.
- **Consumes:** `01-gateway` TLS and routing, `02-auth` Keycloak identity,
  and `06-observability` metrics and logs.
- **Does not own:** the Keycloak lifecycle, OAuth2 Proxy sessions, workflow
  orchestration, producer source-of-truth data, or external connector systems.

## Context and Constraints

### Context

Producers and consumers reach `kafka-1`; browsers reach `kafbat-ui` through Traefik with Keycloak OIDC. The tier consumes `01-gateway` TLS and routing, `02-auth` identity, and `06-observability` metrics and logs.

### Constraints

Kafka stays OPTIONAL; see Evolution under Currentness and Lineage. All listeners are PLAINTEXT, so sensitive or untrusted traffic is excluded until a TLS/SASL change, and Confluent edition-specific capabilities are not assumed.

## Current Structure

### Building Blocks

All services are in `infra/05-messaging/kafka/docker-compose.yml` on
`kafka_net`:

- `kafka-1`, the single broker, and `kafka-exporter` (with `obs_net`).
- `kafbat-ui`, routed with `gateway-standard-chain@file` only; it configures
  neither a schema registry nor a Connect cluster.
- `kafka-init`, which declares replication factor 1.

The three-broker `lab-kafka-1/2/3` topology is a separate project in
`labs/kafka-cluster/docker-compose.yml`; its init job declares replication
factor 3, and it also runs `lab-schema-registry` and `lab-kafka-connect`.

### Runtime and Deployment

#### Runtime View

```text
producer / consumer -> kafka-1
browser -> Traefik standard chain -> kafbat-ui -> Keycloak OIDC
```

Kafbat renders native `auth.type: OAUTH2` from its tracked template, reads its
client secret from Docker secrets, trusts the local CA and maps the Keycloak
`groups` claim to `/admins` and `/users` roles. OAuth2 Proxy is not in front of
Kafbat.

#### Deployment View

`messaging` selects the full stack; `messaging-broker` and `messaging-admin`
select narrower sets. The broker volume is a separate bind-backed named volume.
Recovery must coordinate topic records and configs, consumer offsets and KRaft
metadata (plus Schema Registry subjects and Connect state when the LAB uses
them). The preferred path is producer replay
or approved replication into a fresh isolated cluster; raw log-directory copy
and live cluster-ID reuse are outside the architecture.

## Interfaces

### Contracts

Services run on `kafka_net` in `infra/05-messaging/kafka/docker-compose.yml`. Kafbat uses native `auth.type: OAUTH2` and maps the Keycloak `groups` claim to `/admins` and `/users`; other HTTP interfaces use ForwardAuth. JMX and Kafka Exporter metrics carry no record payloads or secrets.

### Failure Boundaries

Replication factor 1 on one broker gives no broker redundancy (see Risks below). Recovery coordinates topic records and configs, consumer offsets and KRaft metadata, preferably by producer replay or approved replication into a fresh isolated cluster.

## Decisions

### Decision Links

- [ADR-0038 Selective Native OIDC](../decisions/0038-selective-native-oidc-for-native-auth-apps.md)

### Quality and Risks

#### Quality Attributes

- **Reliability:** health checks, explicit broker and Connect volumes, and
  complete topic, offset, schema and connector recovery.
- **Security:** Kafbat uses native OIDC and RBAC; the other HTTP interfaces use
  ForwardAuth.
- **Operability:** exact root profiles and static rendering.
- **Observability:** JMX and Kafka Exporter metrics without record payloads or
  secrets.

#### Risks

All broker, controller and host listeners are PLAINTEXT
(`KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`), so sensitive or untrusted traffic is
excluded until a TLS/SASL change. Replication factor 1 on one broker gives no
broker redundancy, and the LAB's three brokers on one host give no host
availability. Confluent edition-specific capabilities are not assumed.

## Traceability

### Requirement Mapping

- [REQ-0006 Messaging](../../01.requirements/0006-messaging.md)

### Currentness and Lineage

- [Kafka guide](../../05.operations/guides/06-messaging-and-cdc/0036-kafka.md)
- [Kafka Compose](../../../infra/05-messaging/kafka/docker-compose.yml)

#### Evolution

Kafka stays OPTIONAL until a durable producer and consumer are named, with
workload, retention, capacity and recovery targets. Image, protocol, topology
or security changes need compatibility, license, isolated restore and rollback
evidence.
