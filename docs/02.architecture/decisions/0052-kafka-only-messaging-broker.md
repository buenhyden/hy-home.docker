---
title: "Kafka as the Only Messaging Broker"
version: "0.2.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "ADR-0052"
parent_ids:
- "AD-0005"
- "AD-0020"
created: "2026-11-06"
---

# ADR-0052: Kafka as the Only Messaging Broker

## Context

### Problem and Drivers

The platform once planned two brokers: Kafka for event streams and RabbitMQ
for task queues, with RabbitMQ kept behind an opt-in `messaging-option`
profile. The current tree has no RabbitMQ runtime. `infra/05-messaging/`
holds only `kafka/`, no Compose file defines a RabbitMQ service, and the root
Compose includes only `infra/05-messaging/kafka/docker-compose.yml`. Kafka
runs in KRaft mode (`KAFKA_PROCESS_ROLES: 'broker,controller'`). A
multi-broker Kafka cluster exists only as the `labs/kafka-cluster` LAB.

- One broker is one image set, one security review and one set of operations
  documents.
- No current consumer needs AMQP routing; workflow queues use Valkey through
  the Airflow and n8n packages.
- Accepted decisions must describe the tree as it is.

### Decision Scope

This decision covers the messaging broker of HOME and the 05-messaging tier.
Redis Pub/Sub and cloud messaging services stay out of scope.

## Decision

### Chosen Option

1. Apache Kafka in KRaft mode, without ZooKeeper, is the only messaging broker
   in HOME. It carries event streams that need ordering, retention and replay.
2. RabbitMQ is not part of the platform. Adding a task-queue broker needs a new
   ADR.
3. A multi-broker Kafka topology stays in the `labs/kafka-cluster` LAB until
   the owner promotes it under the LAB promotion policy (POL-0107).
4. The messaging management UI (Kafbat UI) sits behind
   `gateway-standard-chain@file`, with native OIDC as decided in
   [ADR-0038](0038-selective-native-oidc-for-native-auth-apps.md); its image
   tags are pinned, never floating.
5. `scripts/hardening/check-all-hardening.sh 05-messaging` and the CI
   `infrastructure-hardening` job guard these items. Catalog expansion (DLQ,
   reprocessing, HA) proceeds in phases through policy, guide and runbook
   approval.

### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval
record is linked. Effective from 2026-11-06.

## Alternatives

### Considered Options

- Keep the two-broker decision and restore RabbitMQ as an opt-in profile:
  rejected; it reintroduces a runtime no consumer uses.
- RabbitMQ only: rejected; it lacks Kafka's replay and partitioned retention
  for event and log streams.
- Kafka as the only broker, with task-queue needs met by the workflow
  packages' own Valkey: selected.

### Trade-offs

- Trade-off: a future need for AMQP-style routing or per-message
  acknowledgement needs a new decision and runtime.

## Consequences

### Impacts

- Positive: one broker to operate and secure; the messaging documents describe
  one runtime.
- Positive: the hardening gate already checks the only broker.

### Follow-up

Messaging requirement and description text that still names RabbitMQ is
reconciled by its owners.

#### Compliance

`check_05_messaging` in `scripts/hardening/check-all-hardening.sh` checks the
gateway chain and Kafbat native OIDC labels.

## Traceability

### Sources

Evidence is the current repository configuration and
`scripts/hardening/check-all-hardening.sh` (`check_05_messaging`). No runtime
state is claimed.

- [REQ-0006 Messaging](../../01.requirements/0006-messaging.md)
- [AD-0005 Messaging architecture](../descriptions/0005-messaging-architecture.md)
- [AD-0020 Messaging hardening](../descriptions/0020-messaging-optimization-hardening-architecture.md)
- [ADR-0038 Selective native OIDC](0038-selective-native-oidc-for-native-auth-apps.md)
- [POL-0107 LAB promotion](../../05.operations/policies/15-labs/0107-lab-promotion.md)

### Supersession

This record replaces two accepted ADRs, deleted in the same change (ADR-0051);
both are historical and non-authoritative:

- ADR-0005 selected Kafka as the primary event backbone and RabbitMQ as the
  lightweight task queue, adopted KRaft mode, and rejected a Kafka-only and a
  RabbitMQ-only stack. Its Kafka and KRaft decisions carry forward here; its
  RabbitMQ selection is withdrawn.
- ADR-0020 ordered the 05-messaging hardening (the gateway chain on the
  management router, pinned `kafka-ui` image tags, dev Compose path
  consistency, a messaging hardening check and CI job) and kept RabbitMQ on
  the opt-in `messaging-option` profile, with catalog expansion in phases. Its
  hardening and phased-expansion decisions carry forward; the RabbitMQ item is
  withdrawn.
