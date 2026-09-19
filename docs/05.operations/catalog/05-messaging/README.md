---
title: "Operations — 05 Messaging"
version: "1.0.0"
type: "operation/domain-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
---

# Operations — 05 Messaging

## Overview

The current messaging implementation is Kafka-family only; no second broker family is present in the root Compose project.

## Structure

| Subject | Disposition | Operator contract |
| --- | --- | --- |
| [Kafka](0036-kafka/guide.md) | OPTIONAL; three-broker topology remains same-host | Nine current services, exact profile families, KRaft/data recovery, Schema Registry, Connect, REST, exporter, init and Kafbat native OIDC |
| [Messaging hardening](0037-optimization-hardening/guide.md) | Static control baseline | Root rendering, plaintext broker boundary, secret/OIDC checks, resource controls and recovery evidence |

## Scope

The canonical source is `infra/05-messaging/kafka/docker-compose.yml`, included by
the root project.

## How to Work in This Area

Stage 05 documents do not authorize service activation, topic
changes, credential rotation, data restore or image upgrades.

## Related Documents

- [Kafka policy](0036-kafka/policy.md)
- [Kafka runbook](0036-kafka/runbook.md)
- [Hardening policy](0037-optimization-hardening/policy.md)
- [Hardening runbook](0037-optimization-hardening/runbook.md)
- [Messaging architecture](../../../02.architecture/descriptions/0005-messaging-architecture.md)
