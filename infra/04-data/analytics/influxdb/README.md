# InfluxDB (TSDB)

> High-performance time series database for metrics and analytics.

## Overview

The `influxdb` service provides the time-series persistence layer for `hy-home.docker`. It is designed for storing granular performance metrics and observability data, supporting high-ingest rates and analytical queries via Flux/SQL. This implementation supports both InfluxDB 3.x (Core) and 2.x (Legacy) via conditional configurations.

## Audience

이 README의 주요 독자:

- Developers (Metrics integration)
- Operators (Resource management)
- AI Agents (Infrastructure discovery)

## Scope

### In Scope

- Time-series data persistence for observability.
- Metrics ingestion via Telegraf, k6, and Locust.
- Dashboarding data source for Grafana.
- Management of InfluxDB buckets and retention policies.

### Out of Scope

- Long-term log storage (handled by Loki).
- Object storage (handled by MinIO).
- Real-time stream processing (handled by ksqlDB).

## Structure

```text
influxdb/
├── docker-compose.yml       # Primary Deployment (InfluxDB 3.x)
├── docker-compose.v2.yml    # Legacy Deployment (InfluxDB 2.x)
└── README.md                # This file
```

## How to Work in This Area

1. Read the [InfluxDB System Guide](../../../docs/07.guides/04-data/analytics/influxdb.md) for architecture details.
2. Follow the [Operations Policy](../../../docs/08.operations/04-data/analytics/influxdb.md) for data retention and security.
3. In case of ingestion failures, refer to the [Recovery Runbook](../../../docs/09.runbooks/04-data/analytics/influxdb.md).
4. All API tokens must be defined in `secrets/influxdb_api_token`.

## Related References

- **System Guide**: [docs/07.guides/04-data/analytics/influxdb.md](../../../docs/07.guides/04-data/analytics/influxdb.md)
- **Operations**: [docs/08.operations/04-data/analytics/influxdb.md](../../../docs/08.operations/04-data/analytics/influxdb.md)
- **Runbook**: [docs/09.runbooks/04-data/analytics/influxdb.md](../../../docs/09.runbooks/04-data/analytics/influxdb.md)
- **Monitoring**: `https://grafana.${DEFAULT_URL}`

---
Copyright (c) 2026. Licensed under the MIT License.
