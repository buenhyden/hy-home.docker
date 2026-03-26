# ksqlDB

> Streaming SQL engine for Apache Kafka.

## Overview

ksqlDB enables building real-time stream processing applications using familiar SQL syntax. It integrates directly with the Kafka cluster and Schema Registry to enable real-time analytics and data transformation.

## Audience

이 README의 주요 독자:

- Developers (Stream processing applications)
- Operators (Resource management and monitoring)
- Architects (System design and integration)
- AI Agents (Infrastructure discovery)

## Scope

### In Scope

- Real-time stream processing using SQL.
- Integration with Kafka brokers and Schema Registry.
- Data generation for testing and examples.
- Management of ksqlDB servers and CLI.

### Out of Scope

- Core Kafka cluster management (handled in `infra/05-messaging/kafka`).
- Schema Registry internal management.
- Long-term data persistence (handled by InfluxDB or PostgreSQL).

## Structure

```text
ksql/
├── docker-compose.yml       # Primary Deployment (ksqlDB Server & CLI)
└── README.md                # This file
```

## How to Work in This Area

1. Read the [ksqlDB System Guide](../../../docs/07.guides/04-data/analytics/ksqldb.md) for architecture and usage.
2. Follow the [Operations Policy](../../../docs/08.operations/04-data/analytics/ksqldb.md) for processing and resources.
3. In case of stream lag or connection issues, refer to the [Recovery Runbook](../../../docs/09.runbooks/04-data/analytics/ksqldb.md).
4. Ensure Kafka brokers and Schema Registry are healthy before starting ksqlDB.

## Related References

- **System Guide**: [docs/07.guides/04-data/analytics/ksqldb.md](../../../docs/07.guides/04-data/analytics/ksqldb.md)
- **Operations**: [docs/08.operations/04-data/analytics/ksqldb.md](../../../docs/08.operations/04-data/analytics/ksqldb.md)
- **Runbook**: [docs/09.runbooks/04-data/analytics/ksqldb.md](../../../docs/09.runbooks/04-data/analytics/ksqldb.md)
- **Kafka Status**: `infra/05-messaging/kafka/README.md`

---
Copyright (c) 2026. Licensed under the MIT License.
