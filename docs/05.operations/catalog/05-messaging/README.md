---
title: Operations — 05 Messaging
version: 1.0.0
type: operation/domain-readme
layer: operations
status: active
owner: "@buenhyden"
---

# Operations — 05 Messaging

> Messaging operations documents grouped by stable Kafka, hardening, and RabbitMQ subjects.

## Overview

This domain co-locates each existing guide, policy, and runbook under its
current four-digit subject directory without changing operational behavior.

## Audience

- Operators, SREs, messaging platform engineers, developers, and AI agents.

## Scope

- Existing messaging usage, approved controls, and recovery procedures.
- No broker startup, topic mutation, credential access, or new operational role.

## Structure

| Subject | Available documents |
| --- | --- |
| [Kafka](0036-kafka/guide.md) | [Guide](0036-kafka/guide.md), [Policy](0036-kafka/policy.md), [Runbook](0036-kafka/runbook.md) |
| [Optimization hardening](0037-optimization-hardening/guide.md) | [Guide](0037-optimization-hardening/guide.md), [Policy](0037-optimization-hardening/policy.md), [Runbook](0037-optimization-hardening/runbook.md) |
| [RabbitMQ](0038-rabbitmq/guide.md) | [Guide](0038-rabbitmq/guide.md), [Policy](0038-rabbitmq/policy.md), [Runbook](0038-rabbitmq/runbook.md) |

ksqlDB remains a data analytics subject; use the
[ksqlDB guide](../04-data/0018-ksqldb/guide.md).

## How to Work in This Area

Use guides for routine context, policies for control boundaries, and runbooks
for existing executable recovery procedures. Follow each document's safety,
evidence, rollback or recovery, and escalation boundaries.

## Related Documents

- [Operations index](../../README.md)
- [Messaging infrastructure](../../../../infra/05-messaging/README.md)
- [Guides index](../../README.md)
- [Policies index](../../README.md)
- [Runbooks index](../../README.md)
- [Incident records](../../incidents/README.md)
