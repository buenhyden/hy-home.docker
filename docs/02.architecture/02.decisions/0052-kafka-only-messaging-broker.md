---
title: "Kafka as the Only Messaging Broker"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "ADR-0052"
parent_ids:
- "AD-0005"
- "AD-0020"
created: "2026-11-06"
---

# ADR-0052: Kafka as the Only Messaging Broker

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-decision payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context

##### Problem and Drivers

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

###### Sources
<!-- core-payload-level:4 -->

Evidence is the current repository configuration and
`scripts/hardening/check-all-hardening.sh` (`check_05_messaging`). No runtime
state is claimed.

- [REQ-0006 Messaging](../../01.requirements/0006-messaging.md)
- [AD-0005 Messaging architecture](../01.descriptions/0005-messaging-architecture.md)
- [AD-0020 Messaging hardening](../01.descriptions/0020-messaging-optimization-hardening-architecture.md)
- [ADR-0038 Selective native OIDC](0038-selective-native-oidc-for-native-auth-apps.md)
- [POL-0107 LAB promotion](../../05.operations/02.policies/15.labs/0107-lab-promotion.md)

##### Decision Scope

This decision covers the messaging broker of HOME and the 05-messaging tier.
Redis Pub/Sub and cloud messaging services stay out of scope.

#### Options

##### Considered Options

- Keep the two-broker decision and restore RabbitMQ as an opt-in profile:
  rejected; it reintroduces a runtime no consumer uses.
- RabbitMQ only: rejected; it lacks Kafka's replay and partitioned retention
  for event and log streams.
- Kafka as the only broker, with task-queue needs met by the workflow
  packages' own Valkey: selected.

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Keep the two-broker decision and restore RabbitMQ as an opt-in profile | The ADR records no benefit for this option. | It reintroduces a runtime no consumer uses. | Rejected; it reintroduces a runtime no consumer uses. |
| RabbitMQ only | The ADR records no benefit for this option. | It lacks Kafka's replay and partitioned retention for event and log streams. | Rejected; it lacks Kafka's replay and partitioned retention for event and log streams. |
| Kafka as the only broker, with task-queue needs met by the workflow packages' own Valkey | One broker to operate and secure, the messaging documents describe one runtime, and the hardening gate already checks the only broker. | A future need for AMQP-style routing or per-message acknowledgement needs a new decision and runtime. | Selected; no current consumer needs AMQP routing, workflow queues use Valkey through the Airflow and n8n packages, and accepted decisions must describe the tree as it is. |

- Trade-off: a future need for AMQP-style routing or per-message
  acknowledgement needs a new decision and runtime.

#### Decision

##### Chosen Option

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

##### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval
record is linked. Effective from 2026-11-06.

###### Supersession
<!-- core-payload-level:4 -->

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

#### Consequences

##### Impacts

- Positive: one broker to operate and secure; the messaging documents describe
  one runtime.
- Positive: the hardening gate already checks the only broker.

##### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

Messaging requirement and description text that still names RabbitMQ is
reconciled by its owners.

###### Compliance
<!-- core-payload-level:4 -->

`check_05_messaging` in `scripts/hardening/check-all-hardening.sh` checks the
gateway chain and Kafbat native OIDC labels.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
