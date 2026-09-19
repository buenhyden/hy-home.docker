---
title: "Messaging Architecture Description"
version: "1.2.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-18"
layer: "architecture"
artifact_id: "AD-0005"
parent_ids:
- "REQ-0006"
created: "2026-03-26"
---

# Messaging Architecture Description

## Context and Stakeholders

이 문서는 메시징 계층(`05-messaging`)의 참조 아키텍처와 품질 속성을 정의한다.
Kafka KRaft 기반 broker, Schema Registry, Kafka Connect, Kafka REST Proxy,
Kafbat UI, Kafka Exporter와 RabbitMQ를 다룬다.

## System Boundaries

- **Owns**:
  - Kafka/RabbitMQ messaging runtime
  - schema/connector management surface
  - Kafbat UI Kafka administration surface
- **Consumes**:
  - `01-gateway` routing/TLS
  - `02-auth` Keycloak identity
  - `06-observability` metrics/logging
- **Does Not Own**:
  - Keycloak identity lifecycle
  - OAuth2 Proxy session lifecycle
  - application workflow orchestration

## Quality Attributes

- **Reliability**: KRaft metadata quorum과 broker health.
- **Scalability**: broker/partition 수평 확장.
- **Observability**: Kafka JMX exporter, Kafka Exporter, RabbitMQ metrics.
- **Operability**: Kafbat UI 및 RabbitMQ Management 제공.
  Kafbat UI는 Keycloak application-native OIDC를 사용하고 RabbitMQ 관리 UI는
  승인된 gateway ForwardAuth 정책을 따른다.

## Components

### Kafka

- `kafka-1`: `messaging`/`dev` profile 기본 broker
- `kafka-2`, `kafka-3`: `messaging-cluster` profile 추가 broker
- `schema-registry`
- `kafka-connect`
- `kafka-rest-proxy`
- `kafka-exporter`
- `kafka-init`

### Kafbat UI

Kafbat UI는 `home-kafbat` Keycloak client를 사용하는 Native OAuth2/OIDC
관리 UI다.

Traefik은 TLS와 `gateway-standard-chain@file`만 제공하며 OAuth2 Proxy
ForwardAuth를 Kafbat UI 앞에 중복 적용하지 않는다.

Kafbat RBAC는 Keycloak `groups` claim을 사용한다.

- `/admins` -> admin
- `/users` -> readonly

RBAC `clusters` 값은 runtime `KAFKA_CLUSTERS_0_NAME`과 일치해야 한다.

### RabbitMQ

RabbitMQ Management UI는 현재 승인된 ForwardAuth 경계를 따른다.

## Data Flow

- producer/consumer -> Kafka broker
- Schema Registry -> Kafka `_schemas`
- Kafka Connect -> Kafka + external systems
- Browser -> Traefik -> Kafbat UI -> Keycloak OIDC
- Browser -> Traefik -> OAuth2 Proxy -> RabbitMQ Management (ForwardAuth pattern)

Kafbat의 local TLS trust는 JDK default `cacerts` 복사본에 mkcert root를 추가하는
방식으로 유지한다. public root CA trust를 제거하지 않는다.

## Deployment View

`infra/05-messaging/kafka/docker-compose.yml`은 profile 기반으로 broker 수를 선택한다.

Kafbat:

- image: [Kafbat declaration](../../../infra/05-messaging/kafka/docker-compose.yml)
- route: `gateway-standard-chain@file`
- client ID: `home-kafbat`
- issuer: `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`

## Traceability

- **PRD**: [REQ-0006 Messaging](../../01.requirements/0006-messaging.md)
- **ADR**: [Kafka vs RabbitMQ](../decisions/0005-kafka-vs-rabbitmq-selection.md)
- **ADR**: [ADR-0038 Selective Native OIDC](../decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- **Spec**: [Current Spec Package index](../../03.specs/README.md)
- **Operations**: [Kafka Guide](../../05.operations/catalog/05-messaging/0036-kafka/guide.md)
- **Auth Integration**: [Application Authentication Integration Guide](../../05.operations/catalog/02-auth/0079-application-auth-integration/guide.md)

## Risks

A multi-broker topology on the same host does not isolate host power or storage
failure. Native OIDC readiness also requires provisioned application roles;
a healthy container alone does not prove authorization.

## Evolution

Keep messaging optional until a durable event consumer is identified. Validate
partition data, client compatibility and recovery before topology or image changes.
Runtime image declarations remain in Compose and the [version projection](../../../infra/tech-stack.versions.json).
