---
title: "Messaging Tier (05-messaging)"
version: "1.1.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2025-11-12"
---

# Messaging Tier (05-messaging)

> Event streaming, message brokering, and real-time data processing tier.

## Overview

The `05-messaging` tier provides the reactive backbone of the `hy-home.docker` ecosystem through Kafka event streaming. Streaming SQL is currently owned by `infra/04-data/analytics/ksql`, not by this tier.

## Audience

이 README의 주요 독자:

- Backend Developers (Event-driven patterns)
- Data Engineers (Kafka topics, schemas, and connectors)
- SREs (Broker reliability & scaling)
- AI Agents (Automated topic provisioning)

## Scope

### In Scope

- Apache Kafka Cluster (KRaft mode)
- Confluent Schema Registry & Kafka Connect
- Messaging UI & Management consoles

### Out of Scope

- Application-specific consumer logic
- External cloud messaging (AWS SQS/SNS)
- Long-term cold storage of events (handled by `04-data`)

## Structure

```text
05-messaging/
├── kafka/              # Kafka cluster, Connect, Registry, UI
└── README.md           # This file
```

## How to Work in This Area

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../.agents/governance/agentic.md)와 [documentation protocol](../../.agents/governance/documentation-protocol.md)을 따른다.

1. Read the Kafka Guide (`docs/05.operations/catalog/05-messaging/0036-kafka/guide.md`) for cluster ops.
2. Check the Operations Policy (`docs/05.operations/catalog/05-messaging/README.md`) for topic and secret controls.
3. Consult the Messaging Runbook (`docs/05.operations/catalog/05-messaging/README.md`) for recovery.

4. Always use the `Schema Registry` for any new topic schemas.
5. Use `replication-factor: 3` only when the `messaging-cluster` profile is selected; `messaging`/`dev` alone runs the single `kafka-1` broker.
6. Check consumer lag metrics before scaling producer throughput.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Streaming  | Confluent Kafka                | [declared runtime image](../tech-stack.versions.json) |
| Mode       | KRaft (Zookeeper-less)         | `messaging`/`dev` runs the single `kafka-1` broker; adding `messaging-cluster` brings up `kafka-2` and `kafka-3` |
| Schema     | Schema Registry                | [declared runtime image](../tech-stack.versions.json) |
| Connect    | Kafka Connect / REST Proxy     | Confluent CP [declared version](../tech-stack.versions.json)      |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `kafka-1` | Kafka/TCP | `messaging`, `dev` | 9092, 19092 |
| `kafka-2/3` | Kafka/TCP | `messaging-cluster` profile in the same compose file | 9094/9096, 19092 |
| `schema-registry`| HTTP | `messaging` | 8081 |
| `kafbat-ui` | HTTP | `messaging` | 8080 |

### Kafbat Authentication

Kafbat UI uses application-native OAuth2/OIDC with Keycloak.
Its Traefik route uses `gateway-standard-chain@file` only; OAuth2 Proxy ForwardAuth is not layered in front.

- client: `home-kafbat`
- roles field: `groups`
- `/admins` -> admin
- `/users` -> readonly

## Configuration

- **Data Path**: All broker data MUST be stored in `${DEFAULT_MESSAGE_BROKER_DIR}`.
- **Secrets**: Security tokens and passwords MUST use Docker secrets.
- **Networking**: High-throughput traffic is confined to the `infra_net`.

## Testing

```bash
# Verify root-included messaging compose
HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh

# Verify Kafka broker API from a running container
docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092

# Test RabbitMQ connectivity
docker exec rabbitmq rabbitmq-diagnostics check_running
```

## Change Impact

- Modifying Kafka partition counts is irreversible without data loss/re-balancing.
- Changing Schema Registry compatibility levels may break downstream consumers.
- RabbitMQ queue purging will permanently delete non-persistent messages.

## Related Documents

- [04-data](../04-data/README.md) - Storing and analyzing processed events.
- [ksqlDB analytics README](../04-data/analytics/ksql/README.md) - Streaming SQL implementation.
- [01-gateway](../01-gateway/README.md) - routing to Messaging UIs.
- Kafka guide (`docs/05.operations/catalog/05-messaging/0036-kafka/guide.md`)
- RabbitMQ guide (`docs/05.operations/catalog/05-messaging/0038-rabbitmq/guide.md`)
- [Documentation index](../../docs/README.md)

Runtime pins are owned by the Compose/Dockerfile declarations; the [curated version projection](../tech-stack.versions.json) provides drift verification.
