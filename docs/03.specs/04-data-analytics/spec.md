---
status: active
---
<!-- Target: docs/03.specs/04-data-analytics/spec.md -->

# Analytics Tier Technical Specification (Spec)

> This document defines the technical specification for the specialized analytics data engines within the `04-data/analytics` sub-tier.

---

## Overview

This document defines the technical design and interface contracts for the `04-data/analytics` tier engines: time-series storage (InfluxDB), stream processing (ksqlDB), log search (OpenSearch), and OLAP analytics (StarRocks). This specification translates PRD-2026-03-26-04-data-analytics requirements into technical details and describes integration with the infrastructure tier and data-processing rules. Because some analytics includes are currently commented out in the root `docker-compose.yml`, this specification describes the owned implementation and optional integration boundary.

## Strategic Boundaries & Non-goals

- **Owns**: Per-engine analytics configuration contracts, data retention policy boundaries, and cross-engine data-flow design.
- **Non-goals**: Query-detail design tied to individual business logic (owned by the application tier) and BI visualization layouts.

## Related Inputs

- **PRD**: [../../01.requirements/005-data-analytics.md](../../01.requirements/005-data-analytics.md)
- **ARD**: [../../02.architecture/requirements/0012-data-analytics-architecture.md](../../02.architecture/requirements/0012-data-analytics-architecture.md)
- **Related ADRs**: [../../02.architecture/decisions/0015-analytics-engine-selection.md](../../02.architecture/decisions/0015-analytics-engine-selection.md)

## Contracts

- **Infrastructure Contract**:
  - Analytics compose files are present under `infra/04-data/analytics/`, while root compose includes for InfluxDB, ksqlDB, and OpenSearch are currently optional/commented.
  - StarRocks warehouses compose is standalone and not included by the root compose.
  - Every engine must be attached to the `infra_net` bridge network.
  - Persistent data is mounted through bind-backed named volumes, and current compose device paths are service-specific under `${DEFAULT_DATA_DIR}` rather than a shared `analytics/` prefix.
- **Data / Interface Contract**:
  - InfluxDB: primary InfluxDB 3.x HTTP/Line Protocol + SQL query interface; legacy InfluxDB 2.x compose preserves Flux compatibility.
  - ksqlDB: SQL stream-processing interface based on Kafka topics.
  - OpenSearch: REST API on port `9200` and Lucene-based search interface.
  - StarRocks: MySQL Protocol-compatible interface on port `9030`.
- **Governance Contract**:
  - Data retention periods and cleanup criteria are managed in operations policy/runbook documents.
  - Retention is compose-enforced only when the linked service config declares it; otherwise it is an operational control requiring runtime evidence.

## Core Design

- **Component Boundary**:
  - InfluxDB: Metrics & Time-series data hub.
  - ksqlDB: Real-time stream processing & transformation.
  - OpenSearch: Logging & full-text search engine.
  - StarRocks: Unified OLAP engine for complex analytical queries.
- **Key Dependencies**:
  - `04-data/operational` and `04-data/relational`: source snapshot and transactional data sources.
  - `05-messaging/kafka`: ksqlDB upstream broker, Schema Registry, and Kafka Connect dependency.
- **Tech Stack**: Docker, InfluxDB 3.x Core primary with InfluxDB 2.x legacy compose, Confluent ksqlDB 8.x, OpenSearch 3.x, StarRocks 4.x.

## Data Modeling & Storage Strategy

- **Schema Strategy**:
  - InfluxDB: tag-based indexing and field-oriented storage.
  - OpenSearch: domain-specific index patterns (for example, `logs-*-*`).
  - StarRocks: star schema or flat table models are recommended for OLAP optimization.
- **Retention Plan**:
  - Time-series, log, stream state, and OLAP data retention targets must be recorded per service before production-like use.
  - Automatic deletion or cold-storage movement is not assumed unless the current service config declares it.

## Interfaces & Data Structures

### Analytics Engine Contract

| Engine | Interface | Primary Data Shape | Persistence Boundary |
| --- | --- | --- | --- |
| InfluxDB | HTTP / Line Protocol | time-series measurements, tags, fields | `influxdb-data`, `influxdb-plugins` |
| ksqlDB | Kafka topics + SQL streams | stream/table definitions | `ksqldb-data-volume`, Kafka state stores, topic retention |
| OpenSearch | HTTPS REST API | index documents and mappings | `opensearch-data`, `opensearch-dashboards-data` |
| StarRocks | MySQL-compatible protocol | OLAP tables and materialized views | `starrocks-fe-data`, `starrocks-be-data` |

## Verification

```bash
# InfluxDB 3.x primary health check
curl -i http://influxdb:8181/

# InfluxDB 2.x legacy compose health check, only when docker-compose.v2.yml is selected
curl -f http://influxdb:8086/health

# OpenSearch status requires HTTPS and the admin Docker Secret
read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
curl -fsSk -u "admin:${OPENSEARCH_ADMIN_PASSWORD}" https://opensearch:9200/_cluster/health
unset OPENSEARCH_ADMIN_PASSWORD

# StarRocks Connection test (via MySQL client)
mysql -h starrocks-fe -P 9030 -u root -e "SHOW FRONTENDS;"
```

## Success Criteria & Verification Plan

- **VAL-SPC-04-ANA-01**: All analytics engines can communicate with each other inside `infra_net`.
- **VAL-SPC-04-ANA-02**: Data integrity is preserved across container restarts after persistent volumes are mounted.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-05-22-data-analytics-execution-traceability.md](../../04.execution/plans/2026-05-22-data-analytics-execution-traceability.md)
- **Tasks**: [../../04.execution/tasks/2026-05-22-data-analytics-execution-traceability.md](../../04.execution/tasks/2026-05-22-data-analytics-execution-traceability.md)
- **Guide**: [../../05.operations/guides/04-data/analytics/README.md](../../05.operations/guides/04-data/analytics/README.md)
- **Policy**: [../../05.operations/policies/04-data/analytics/README.md](../../05.operations/policies/04-data/analytics/README.md)
- **Runbook**: [../../05.operations/runbooks/04-data/analytics/influxdb.md](../../05.operations/runbooks/04-data/analytics/influxdb.md)
