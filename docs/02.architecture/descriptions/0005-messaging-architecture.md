---
title: "Messaging Architecture Description"
version: "1.4.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "AD-0005"
parent_ids:
- "REQ-0006"
created: "2026-03-26"
---

# Messaging Architecture Description

## Overview

`05-messaging` is the optional Kafka event-streaming boundary. The HOME
implementation has one Kafka KRaft broker, Schema Registry, Kafka Connect,
Kafka REST Proxy, Kafbat UI, Kafka Exporter, a topic-init job and a Debezium
database provisioning job. No second broker family is part of the
architecture.

## Scope

- **Owns:** Kafka topics, configuration and KRaft state, schema history,
  Connect runtime state, REST access, metrics export and Kafbat administration.
- **Consumes:** `01-gateway` TLS and routing, `02-auth` Keycloak identity,
  `04-data` `dev-pg` for CDC, and `06-observability` metrics and logs.
- **Does not own:** the Keycloak lifecycle, OAuth2 Proxy sessions, workflow
  orchestration, producer source-of-truth data, or external connector systems.

## Structure

### Architecture

All services are in `infra/05-messaging/kafka/docker-compose.yml` on
`kafka_net`:

- `kafka-1`, the single broker, and `kafka-exporter` (with `obs_net`).
- `schema-registry`, `kafka-connect` (also on `dev_data_net`) and
  `kafka-rest-proxy`, each routed through ForwardAuth.
- `kafbat-ui`, routed with `gateway-standard-chain@file` only.
- `kafka-init`, which declares replication factor 1, and
  `debezium-db-provision` for the CDC source.

The three-broker `lab-kafka-1/2/3` topology is a separate project in
`labs/kafka-cluster/docker-compose.yml`; its init job declares replication
factor 3.

## Runtime and Deployment

### Runtime View

```text
producer / consumer -> kafka-1
schema-registry -> kafka-1 _schemas topic
kafka-connect -> kafka-1 + dev-pg / approved external system
browser -> Traefik standard chain -> kafbat-ui -> Keycloak OIDC
```

Kafbat renders native `auth.type: OAUTH2` from its tracked template, reads its
client secret from Docker secrets, trusts the local CA and maps the Keycloak
`groups` claim to `/admins` and `/users` roles. OAuth2 Proxy is not in front of
Kafbat.

### Deployment View

`messaging` selects the full stack; `messaging-broker`, `messaging-schema`,
`messaging-connect`, `messaging-rest` and `messaging-admin` select narrower
sets, and `cdc` selects the broker, Schema Registry, Connect, exporter and the
Debezium provisioning job. Broker and Connect volumes are separate bind-backed
named volumes. Recovery must coordinate topic records and configs, consumer
offsets, KRaft metadata, Schema Registry subjects and IDs, connector
definitions and Connect internal state. The preferred path is producer replay
or approved replication into a fresh isolated cluster; raw log-directory copy
and live cluster-ID reuse are outside the architecture.

## Quality and Risks

### Quality Attributes

- **Reliability:** health checks, explicit broker and Connect volumes, and
  complete topic, offset, schema and connector recovery.
- **Security:** Kafbat uses native OIDC and RBAC; the other HTTP interfaces use
  ForwardAuth.
- **Operability:** exact root profiles and static rendering.
- **Observability:** JMX and Kafka Exporter metrics without record payloads or
  secrets.

### Risks

All broker, controller and host listeners are PLAINTEXT
(`KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`), so sensitive or untrusted traffic is
excluded until a TLS/SASL change. Replication factor 1 on one broker gives no
broker redundancy, and the LAB's three brokers on one host give no host
availability. Confluent edition-specific capabilities are not assumed.

### Evolution

Kafka stays OPTIONAL until a durable producer and consumer are named, with
workload, retention, capacity and recovery targets. Image, protocol, topology
or security changes need compatibility, license, isolated restore and rollback
evidence.

## Related Documents

- [REQ-0006 Messaging](../../01.requirements/0006-messaging.md)
- [ADR-0038 Selective Native OIDC](../decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- [Kafka guide](../../05.operations/guides/06-messaging-and-cdc/0036-kafka.md)
- [Kafka Compose](../../../infra/05-messaging/kafka/docker-compose.yml)
