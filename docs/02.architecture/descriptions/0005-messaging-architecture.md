---
title: "Messaging Architecture Description"
version: "1.6.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0005"
parent_ids:
- "REQ-0006"
created: "2026-03-26"
---

# Messaging Architecture Description

## Context and Boundaries

### System Boundary

- **Owns:** Kafka topics, configuration and KRaft state, metrics export and
  Kafbat administration.
- **Consumes:** `01-gateway` TLS and routing, `02-auth` Keycloak identity,
  and `06-observability` metrics and logs.
- **Does not own:** the Keycloak lifecycle, OAuth2 Proxy sessions, workflow
  orchestration, producer source-of-truth data, or external connector systems.

#### Purpose and Readers

`05-messaging` is the optional Kafka event-streaming boundary. The HOME
implementation has one Kafka KRaft broker, Kafbat UI, Kafka Exporter and a
topic-init job. Schema Registry and Kafka Connect (Debezium CDC) moved to the LAB
`labs/kafka-cluster` by the ADR-0062 amendment of 2026-11-10. Kafka is the sole
broker family. ADR-0062 removed the HOME broker REST proxy.

#### Context

Producers and consumers reach `kafka-1`; browsers reach `kafbat-ui` through Traefik with Keycloak OIDC. The tier consumes `01-gateway` TLS and routing, `02-auth` identity, and `06-observability` metrics and logs.

### Constraints

Kafka stays OPTIONAL; see Evolution under Currentness and Lineage. All listeners are PLAINTEXT, so sensitive or untrusted traffic is excluded until a TLS/SASL change, and Confluent edition-specific capabilities are not assumed.

## Structure

### Building Blocks

The HOME services are in `infra/05-messaging/kafka/docker-compose.yml` on
`kafka_net`:

- `kafka-1`, the single broker, and `kafka-exporter` (with `obs_net`).
- `kafbat-ui`, routed with `gateway-standard-chain@file` only; it configures
  neither a schema registry nor a Connect cluster.
- `kafka-init`, which declares replication factor 1.

The three-broker `lab-kafka-1/2/3` topology is a separate project in
`labs/kafka-cluster/docker-compose.yml`; its init job declares replication
factor 3. `lab-schema-registry` and `lab-kafka-connect` use the LAB brokers on
`lab_kafka_net`. Connect has no configured source connector or source database
credential in the tracked Compose. A connector requires separately approved
inputs and operation.

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Kafka broker `kafka-1` on `kafka_net` | `kafka-1` | Producers and consumers | PLAINTEXT listeners (`KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`); [Kafka Compose](../../../infra/05-messaging/kafka/docker-compose.yml) | Replication factor 1 gives no broker redundancy; recovery prefers producer replay or approved replication into a fresh isolated cluster. |
| Kafbat UI management route | `kafbat-ui` | Browsers through Traefik `gateway-standard-chain@file` | Native `auth.type: OAUTH2` with Keycloak `groups` mapped to `/admins` and `/users`; [ADR-0038 Selective Native OIDC](../decisions/0038-selective-native-oidc-for-native-auth-apps.md) | The description records no failure handling for this interface. |
| JMX and Kafka Exporter metrics | `kafka-1` and `kafka-exporter` | `06-observability` | Metrics without record payloads or secrets | The description records no failure handling for this interface; scrape is confirmed separately. |
| LAB Schema Registry and Kafka Connect HTTP | `lab-schema-registry` and `lab-kafka-connect` | Clients inside `lab_kafka_net` | [Kafka LAB Compose](../../../labs/kafka-cluster/docker-compose.yml) | LAB recovery accounts for schema subjects and the Connect configuration, offset and status topics in its brokers. |

HOME services use `kafka_net`. Kafbat exposes management through native OIDC
and role mapping. JMX and Kafka Exporter expose metrics without record payloads
or secrets. Schema Registry and Connect expose LAB-internal HTTP interfaces
without a HOME gateway route.

## Runtime Behavior

### Normal Flow

#### Runtime View

```text
producer / consumer -> kafka-1
browser -> Traefik standard chain -> kafbat-ui -> Keycloak OIDC
```

Kafbat renders native `auth.type: OAUTH2` from its tracked template, reads the
configured client secret file, trusts the local CA and maps the Keycloak
`groups` claim to `/admins` and `/users` roles. This is the HOME HTTP management
route. LAB Schema Registry and Connect listen inside the LAB network.

#### Deployment View

`messaging` selects the full HOME messaging stack. `messaging-broker` and
`messaging-admin` select narrower sets. The standalone LAB uses `lab-kafka`.
The HOME broker volume is a separate bind-backed named volume.
Recovery must coordinate topic records and configs, consumer offsets and KRaft
metadata (plus Schema Registry subjects and Connect state when the LAB uses
them). The preferred path is producer replay
or approved replication into a fresh isolated cluster; raw log-directory copy
and live cluster-ID reuse are outside the architecture.

### Failure and Recovery

Replication factor 1 on one broker gives no broker redundancy (see Risks below). Recovery coordinates topic records and configs, consumer offsets and KRaft metadata, preferably by producer replay or approved replication into a fresh isolated cluster.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- **Reliability:** health checks and explicit broker volumes. LAB recovery
  accounts for schema subjects and the Connect configuration, offset and
  status topics in its brokers.
- **Security:** Kafbat uses native OIDC and RBAC. Schema Registry and Connect
  stay inside the LAB network.
- **Operability:** run static rendering for the selected HOME or LAB profile.
  Confirm actual authentication, connector execution and scrape separately.
- **Observability:** JMX and Kafka Exporter metrics without record payloads or
  secrets.

#### Risks

All broker, controller and host listeners are PLAINTEXT
(`KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`), so sensitive or untrusted traffic is
excluded until a TLS/SASL change. Replication factor 1 on one broker gives no
broker redundancy, and the LAB's three brokers on one host give no host
availability. Confluent edition-specific capabilities are not assumed.

### Trade-offs

- All broker, controller and host listeners are PLAINTEXT, so sensitive or
  untrusted traffic is excluded until a TLS/SASL change (Risks, Constraints).
- HOME runs one broker with replication factor 1, which gives no broker
  redundancy; the LAB's three brokers on one host give no host availability
  (Risks).
- Confluent edition-specific capabilities are not assumed (Risks).
- Raw log-directory copy and live cluster-ID reuse are outside the
  architecture; recovery prefers producer replay or approved replication into
  a fresh isolated cluster (Deployment View).

## Decisions and Adoption

### Decisions

- [ADR-0038 Selective Native OIDC](../decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- [ADR-0062 HOME Membership and Planned LABs](../decisions/0062-home-lab-membership.md)

### Adoption Boundaries

#### Requirement Mapping

- [REQ-0006 Messaging](../../01.requirements/0006-messaging.md)

#### Currentness and Lineage

- [Kafka guide](../../05.operations/guides/06-messaging-and-cdc/0036-kafka.md)
- [Kafka Compose](../../../infra/05-messaging/kafka/docker-compose.yml)
- [Kafka LAB Compose](../../../labs/kafka-cluster/docker-compose.yml)

#### Evolution

Kafka stays OPTIONAL until a durable producer and consumer are named, with
workload, retention, capacity and recovery targets. Image, protocol, topology
or security changes need compatibility, license, isolated restore and rollback
evidence.
