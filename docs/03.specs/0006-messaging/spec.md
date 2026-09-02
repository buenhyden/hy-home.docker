---
title: Messaging Capability Specification
type: sdlc/spec
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0006
parent_ids:
  - AD-0020
created: 2026-07-05
updated: 2026-09-01
---
# Messaging Capability Specification

## Overview

This specification defines the current Kafka and RabbitMQ infrastructure
contract under infra/05-messaging/.

## Boundaries and Inputs

- Input architecture: AD-0020 and messaging decisions.
- In scope: Kafka, Kafbat UI, supporting Kafka services, RabbitMQ, gateway
  middleware, images, networks, health, and persistent state.
- Out of scope: application producer/consumer business logic and undeployed
  multi-region or multi-AZ topology.

## Behavior Contract

- Tracked images use approved pinned versions rather than floating tags.
- Externally routed management paths use the current gateway middleware and
  authentication boundary.
- Root messaging profiles render the declared development topology; the full
  Kafka topology remains a service-local variant with explicit context.
- Network, volume, secret, and health declarations remain deterministic.

## Technical Approach

Kafka and RabbitMQ keep separate service directories and Compose variants.
Traefik terminates external TLS while infra_net carries internal protocols.
Topic retention, DLQ/reprocessing, quorum queues, and recovery procedures are
owned by their Stage 05 subjects when implemented.

## Interfaces and Data

Kafka protocols, Schema Registry, Kafka Connect, REST, management UI, and
RabbitMQ protocols are exposed only through their tracked service and gateway
contracts. Persistent broker state and credentials stay within their declared
volumes and secrets.

## Failure Modes and Guardrails

Floating images, missing middleware, invalid relative mounts, unhealthy
dependencies, or a service-local render without required network/secret context
must not be reported as a valid root configuration.

## Acceptance Contract

- Messaging and messaging-development profiles render in the root context.
- scripts/hardening/check-all-hardening.sh 05-messaging passes.
- Template security and document traceability checks pass.
- Operations procedures match the current single/full topology distinction.

## Traceability

- [REQ-0017](../../01.requirements/0017-messaging-optimization-hardening.md)
- [AD-0020](../../02.architecture/descriptions/0020-messaging-optimization-hardening-architecture.md)
- [Messaging Operations catalog](../../05.operations/catalog/05-messaging/README.md)
