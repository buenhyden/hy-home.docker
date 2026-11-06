---
title: "Analytics Services Requirements"
version: "1.5.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "requirements"
artifact_id: "REQ-0005"
created: "2026-03-26"
---
# Analytics Services Requirements

## Overview

### Problem and Goals

The platform needs time-series history, full-text log search, SQL stream
processing into shared tables, and interactive SQL over those tables. Time-series
history is owned by the DEV TimescaleDB engine (ADR-0047) and log search by
OpenSearch in the data tier. Stream processing and SQL analysis over Iceberg
tables (ADR-0039) are optional capabilities that run only in the standalone
lakehouse LAB (SPEC-0262); the root platform includes no stream-processing or SQL analytics engine.
ksqlDB and StarRocks were removed in SPEC-0180 after the Flink and Trino live
acceptance on 2026-09-24.

## Scope

### Constraints

- **In Scope**: The time-series, log search, stream processing and SQL
  analysis needs above, the boundary that keeps the analytics engines separate
  from core transactional data, and the InfluxDB retirement.
- **Owned elsewhere**: POL-0094 owns the Iceberg catalog, table bucket and
  object storage operations. SPEC-0262 owns the LAB entrypoints.
- **Out of Scope**: Dashboard design for individual visualization tools.
- **Non-goals**: Transactional SQL processing, which the core PostgreSQL owns,
  and promoting a LAB, which is an owner decision.
- **Agent boundary**: An agent may query analytics schemas, analyze log
  patterns and suggest query optimizations. It must not delete source data or
  change a running analytics engine's configuration without approval.

### Assumptions

Source data is supplied reliably through the core data tier or the messaging
tier. A LAB reaches a HOME service only through an approved endpoint input.

### Risks

- Large data inflow can exhaust analytics storage or compute.
- The LAB engines depend on the Iceberg catalog in object storage and on Kafka
  for stream input; neither is reachable unless its endpoint is supplied.

## Requirements

### Functional Requirements

- **REQ-0005-FR-0001**: Provide a dedicated write and query interface for time-series data.
- **REQ-0005-FR-0003**: Provide full-text search over collected logs.
- **REQ-0005-FR-0005**: Write events to an Iceberg table via SQL-based stream processing, resuming from the last checkpoint after a failure.
- **REQ-0005-FR-0006**: Provide interactive SQL queries against Iceberg tables.

FR numbers 0002 (ksqlDB stream processing) and 0004 (StarRocks OLAP) were
retired with those engines and are not reused; 0005 and 0006 restate the same
needs without naming an engine.

### Stakeholders and User Needs

- **Data scientist**: derives trends with SQL queries against shared tables.
- **SRE**: searches logs within seconds and watches system metrics.
- **Home automation user**: queries a year of sensor history with sub-second
  latency from a dashboard.
- **Data engineer**: processes Kafka events with SQL into a table and queries
  that table with SQL.

### Non-functional Requirements

No separately numbered non-functional requirement is defined.

### Interface Requirements

No separately numbered solution-independent interface requirement is defined.

## Acceptance Criteria

- **REQ-0005-FR-0001**: InfluxDB is retired (ADR-0047, SPEC-0213) and nothing
  current deploys it. Time-series history uses DEV TimescaleDB tables; a
  hypertable is created only for a named consumer.
- **REQ-0005-FR-0003**: OpenSearch is documented as the single node the data
  tier declares, starts only when its optional profile is selected, and keeps
  its secrets, data and health check boundary. A three-node topology exists
  only as a LAB. Latency figures are claimed only with separate benchmark
  evidence.
- **REQ-0005-FR-0005**: Flink writes to an Iceberg table by batch and by
  checkpointed streaming INSERT, and resumes from its checkpoint. This passed
  live acceptance on 2026-09-24 (SPEC-0180) before the move to the lakehouse
  LAB; the LAB form has static rendering evidence only.
- **REQ-0005-FR-0006**: Trino reads the table Flink wrote, and the data quality
  suite passes through Trino. This passed live acceptance on 2026-09-24 before
  the move to the lakehouse LAB. Interactive latency is claimed only with
  separate benchmark evidence.

## Related Documents

### Traceability

- **Architecture Description**: [0012-data-analytics-architecture.md](../02.architecture/descriptions/0012-data-analytics-architecture.md)
- **ADR**: [ADR-0058 HOME Tiers versus LABs](../02.architecture/decisions/0058-home-tiers-versus-labs.md) (supersedes ADR-0015), [0047-dev-timescale-influx-retirement-and-load-tools.md](../02.architecture/decisions/0047-dev-timescale-influx-retirement-and-load-tools.md)
- **Spec**: [SPEC-0262 analytics LAB migration](../03.specs/0262-analytics-labs-migration/spec.md); SPEC-0180 (lakehouse adoption and the removal of ksqlDB and StarRocks) is retired and its body is in version history.
- **Guide**: [Operations guides](../05.operations/guides/README.md)
- **Retired domain Spec SPEC-0005** (data-analytics): replaced by the data-analytics guides, policies and runbooks in the operations catalog under `docs/05.operations/`.
