---
title: "Messaging Architecture Description"
version: "1.3.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "architecture"
artifact_id: "AD-0005"
parent_ids:
- "REQ-0006"
created: "2026-03-26"
---

# Messaging Architecture Description

## Context and Stakeholders

`05-messaging` is the optional Kafka event-streaming boundary. The current
implementation contains Kafka KRaft brokers, Schema Registry, Kafka Connect,
Kafka REST Proxy, Kafbat UI, Kafka Exporter and a topic-init job. No second broker family is part of the current architecture.

## System Boundaries

- **Owns:** Kafka topic/configuration and KRaft state, schema history, Connect
  runtime state, REST access, metrics export and Kafbat administration.
- **Consumes:** `01-gateway` TLS/routing, `02-auth` Keycloak identity and
  `06-observability` metrics/logs.
- **Does not own:** Keycloak lifecycle, OAuth2 Proxy sessions, workflow
  orchestration, producer source-of-truth data, or external connector systems.

## Quality Attributes

- **Reliability:** health checks, explicit persistent broker/Connect volumes and
  complete topic/offset/schema/connector recovery. Three brokers on one host do
  not provide host availability.
- **Security:** services remain on `infra_net`; Kafbat uses native OIDC/RBAC.
  Current broker/controller/host listeners are PLAINTEXT, a known boundary that
  excludes sensitive or untrusted traffic until a planned TLS/SASL change.
- **Operability:** exact root profiles and static rendering; named workload,
  retention, capacity and recovery targets before activation.
- **Observability:** JMX/Kafka exporter metrics without record payload or secret
  disclosure.

## Components

- `kafka-1` participates in `messaging`, role-specific selectors and
  `messaging-cluster`.
- `kafka-2` and `kafka-3` participate only in `messaging-cluster`.
- Schema Registry, Connect, REST, Kafbat, exporter and init have the current
  selectors documented in [GDE-0036](../../05.operations/catalog/05-messaging/0036-kafka/guide.md).
- The init job declares replication factor 3 for its two bootstrap topics, so a
  valid initialization requires the three-broker topology.

## Data Flow

Kafbat renders native `auth.type: OAUTH2` configuration from its tracked template,
reads its client secret from Docker secret custody, trusts the local CA and maps
Keycloak `groups` to `/admins` and `/users` RBAC roles. Traefik provides TLS and
`gateway-standard-chain@file`. OAuth2 Proxy ForwardAuth is not placed in front of
this native-OIDC application.

```text
producer / consumer -> Kafka broker
Schema Registry -> Kafka _schemas topic
Kafka Connect -> Kafka + approved external system
browser -> Traefik standard chain -> Kafbat -> Keycloak OIDC
```

## Deployment View

Broker and Connect volumes are separate bind-backed named volumes. Recovery must
coordinate topic records/configs, consumer offsets, KRaft metadata, Schema
Registry subjects/versions/IDs, connector definitions and Connect internal state.
The preferred path is producer replay or approved cross-cluster replication into
a fresh isolated cluster. Piecemeal raw log-directory copy and live cluster-ID
reuse are outside the architecture.

## Risks

Kafka remains OPTIONAL until a durable producer/consumer is named. Current
PLAINTEXT listeners and same-host replication limit the suitable workload. Image,
protocol, topology or security changes require compatibility, license, isolated
restore and rollback evidence. Confluent edition-specific capabilities are not
assumed from the selected images.

## Traceability

- **Requirement:** [REQ-0006 Messaging](../../01.requirements/0006-messaging.md)
- **Decision:** [ADR-0038 Selective Native OIDC](../decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- **Operations:** [Kafka Guide](../../05.operations/catalog/05-messaging/0036-kafka/guide.md)
- **Runtime source:** [Kafka Compose](../../../infra/05-messaging/kafka/docker-compose.yml)
