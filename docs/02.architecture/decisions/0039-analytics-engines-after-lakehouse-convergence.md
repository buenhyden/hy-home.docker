---
title: "Analytics Engines after Lakehouse Convergence"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0039"
parent_ids:
- "AD-0012"
supersedes:
- "ADR-0015"
created: "2026-09-24"
---

# ADR-0039: Analytics Engines after Lakehouse Convergence

## Context

ADR-0015 adopted InfluxDB (time series), ksqlDB (stream processing), OpenSearch
(log/search), and StarRocks (OLAP) as dedicated engines in `04-data/analytics`.
SPEC-0180 introduced a lakehouse that places Iceberg tables on SeaweedFS, and
its engines, Flink and Trino, take on the same roles as ksqlDB and StarRocks.
Keeping two engines for the same role doubles images, configuration, security
review, and operations documentation without gaining any feature.

The S01 ruling decided to remove ksqlDB after Flink live acceptance and
StarRocks after Trino live acceptance. Both acceptances passed on 2026-09-24.
Flink wrote a table with a streaming INSERT that went through batch INSERT and
checkpoint, Trino read the same rows, and the Great Expectations suite passed
through Trino. ksqlDB and StarRocks had never been deployed and had no host
data or volume.

## Decision

- **Time series**: Keep the single InfluxDB 3 Core deployment (same as
  ADR-0015).
- **Log/search**: Keep OpenSearch 3.x (same as ADR-0015).
- **Stream processing**: Flink handles SQL stream processing between Kafka
  topics and Iceberg tables. It is the `lakehouse` profile's JobManager and
  TaskManager, and checkpoints are kept in a host directory.
- **OLAP/SQL query**: Trino handles SQL queries against Iceberg tables on
  SeaweedFS. No separate warehouse with its own storage is kept.
- ksqlDB and StarRocks are not adopted. Adding an engine for the same role
  requires a decision that supersedes this ADR.

Tracked Compose files fix the runtime image tags, and
`infra/tech-stack.versions.json` holds the current image list.

## Consequences

- **Positive**:
  - Stream processing and OLAP share one table format (Iceberg) and one
    object store, so there is no copying or synchronization between engines.
  - Fewer engines means fewer images, less security review, and less
    operations documentation.
- **Trade-offs**:
  - Trino is a query engine with no storage layer, so its performance depends
    on Iceberg table design and SeaweedFS.
  - Flink SQL lacks serving features such as ksqlDB's pull query. A separate
    decision is needed if that becomes necessary.
  - Flink and Trino expose their unauthenticated APIs only on a loopback host
    port (POL-0094).

### Explicit Non-goals

- Moving InfluxDB or OpenSearch into the lakehouse.
- Storing core transactional data directly in an analytics engine.

## Options Considered

### Alternative 01: Keep ksqlDB and StarRocks alongside Flink and Trino

- **Good**: Does not change the existing decision.
- **Bad**: Operates two engines for the same role, and keeps maintaining
  documentation and validation for engines that were never deployed.

### Alternative 02: Handle stream and OLAP with Spark alone

- **Good**: Reduces to a single engine.
- **Bad**: Heavier than Trino for interactive SQL queries, and S12 Spark is
  kept for table maintenance and batch purposes.

## Traceability

The basis is the S01 ruling of SPEC-0180 Task 0008, the S12-S15 source
stages, the 2026-09-24 live acceptance record, and the current repository
configuration. Unrecorded runtime state is not claimed.

## Related Documents

- **Superseded ADR**: `ADR-0015` (`docs/98.archive/superseded/`에 보존)
- **Architecture Description**: [0012-data-analytics-architecture.md](../descriptions/0012-data-analytics-architecture.md)
- **Requirements**: [0005-data-analytics.md](../../01.requirements/0005-data-analytics.md)
- **Lakehouse policy**: [POL-0094](../../05.operations/policies/0094-lakehouse.md)
