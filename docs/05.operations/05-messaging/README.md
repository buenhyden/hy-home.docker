# Operations — 05 Messaging

> Messaging operations documents grouped by stable Kafka, hardening, and RabbitMQ subjects.

## Overview

This domain co-locates each existing guide, policy, and runbook under its frozen
`ops-0036` through `ops-0038` identity without changing operational behavior.

## Audience

- Operators, SREs, messaging platform engineers, developers, and AI agents.

## Scope

- Existing messaging usage, approved controls, and recovery procedures.
- No broker startup, topic mutation, credential access, or new operational role.

## Structure

| Subject | Available documents |
| --- | --- |
| [Kafka](./ops-0036-kafka/guide.md) | [Guide](./ops-0036-kafka/guide.md), [Policy](./ops-0036-kafka/policy.md), [Runbook](./ops-0036-kafka/runbook.md) |
| [Optimization hardening](./ops-0037-optimization-hardening/guide.md) | [Guide](./ops-0037-optimization-hardening/guide.md), [Policy](./ops-0037-optimization-hardening/policy.md), [Runbook](./ops-0037-optimization-hardening/runbook.md) |
| [RabbitMQ](./ops-0038-rabbitmq/guide.md) | [Guide](./ops-0038-rabbitmq/guide.md), [Policy](./ops-0038-rabbitmq/policy.md), [Runbook](./ops-0038-rabbitmq/runbook.md) |

ksqlDB remains a data analytics subject; use the
[ksqlDB guide](../04-data/ops-0018-analytics-ksqldb/guide.md).

## How to Work in This Area

Use guides for routine context, policies for control boundaries, and runbooks
for existing executable recovery procedures. Follow each document's safety,
evidence, rollback or recovery, and escalation boundaries.

## Related Documents

- [Operations index](../README.md)
- [Messaging infrastructure](../../../infra/05-messaging/README.md)
- [Guides index](../guides/README.md)
- [Policies index](../policies/README.md)
- [Runbooks index](../runbooks/README.md)
- [Incident records](../incidents/README.md)
