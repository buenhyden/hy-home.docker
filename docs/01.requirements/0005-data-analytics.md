---
title: "Analytics Tier (04-data/analytics) Product Requirements"
version: "1.1.1"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "requirements"
artifact_id: "REQ-0005"
parent_ids: []
created: "2026-03-26"
---
# Analytics Tier (04-data/analytics) Product Requirements

> This document defines the product requirements for the specialized analytics data engines within the `04-data/analytics` sub-tier.

## Problem and Goals

This document defines the platform's analytics requirements. Time-series and log search are handled by dedicated engines in `04-data/analytics` (InfluxDB, OpenSearch), while stream processing and SQL/OLAP analysis are handled by engines in `04-data/lakehouse` (Flink, Trino) on top of Iceberg tables (ADR-0039).

### Problem Statement

The current implementation holds InfluxDB and OpenSearch compose under `infra/04-data/analytics`, and Flink and Trino compose under `infra/04-data/lakehouse`. This PRD defines the requirement that these engines remain an optional tier separate from core transactional data: even though the root compose unconditionally includes the files, they do not belong to the `core` profile and do not start without a separate profile selection. ksqlDB and StarRocks, which previously handled stream processing and OLAP, were removed in SPEC-0180 S19 after the Flink and Trino live acceptance (2026-09-24).

## Stakeholders and User Needs

Build a high-performance analytics hub that collects, processes, and analyzes all structured/unstructured data generated on the platform in real time, providing users with immediate, in-depth visualization and insight.

### Personas

- **Data Scientist**: Needs to derive trends through SQL/OLAP queries against Iceberg tables.
- **SRE/DevOps**: Needs real-time log search and system metric monitoring.
- **Home Automation User**: Wants to see real-time charts and sensor data changes without delay.

### Key Use Cases

- **STORY-01**: A user wants to query the trend of smart home sensor data over the past year through a dashboard with sub-second latency (InfluxDB).
- **STORY-02**: An operator wants to perform fast, second-level keyword search over collected microservice logs (OpenSearch).
- **STORY-03**: A data engineer wants to process Kafka events with SQL, accumulate them into a table, and query the same table with SQL (Flink, Trino).

## Functional Requirements

- **REQ-0005-FR-0001**: Provide a dedicated write and query interface for time-series data (TSDB).
- **REQ-0005-FR-0003**: Integrate full-text search and log collection pipelines.
- **REQ-0005-FR-0005**: Write events to an Iceberg table via SQL-based stream processing, resuming from the last checkpoint after a failure.
- **REQ-0005-FR-0006**: Provide interactive SQL/OLAP queries against Iceberg tables.

FR numbers 0002 (ksqlDB stream processing) and 0004 (StarRocks OLAP) were retired along with the engine removal and are not reused. The same needs are redefined in an engine-neutral way by 0005 and 0006.

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0005-FR-0001**: The InfluxDB 3 Core single compose, database name, port `8181`, `/api/v3/write_lp` endpoint/schema, and current healthcheck must match between the documentation and the static source. Token provisioning and authenticated write acceptance are not considered verified until a separate runtime approval.
- **REQ-0005-FR-0003**: The OpenSearch documentation must describe, without exaggeration, the single primary stack the current compose proves, the cluster topology selected by the profile, and the secret/volume/healthcheck boundary. Live performance figures (P95, indexing latency) are recorded as success evidence only when separate runtime benchmark evidence exists.
- **REQ-0005-FR-0005**: Flink must write to the Iceberg table via batch INSERT and checkpointed streaming INSERT, with checkpoints recorded to the host directory. This passed live acceptance on 2026-09-24 (SPEC-0180 Task 0008).
- **REQ-0005-FR-0006**: Trino must read the same table that Flink wrote, and the Great Expectations suite must pass through Trino. This passed live acceptance on 2026-09-24. Interactive performance figures are recorded only when separate benchmark evidence exists.

## Constraints

- **In Scope**: Analytics requirements, interfaces, and optional-compose execution boundary definitions for InfluxDB, OpenSearch, Flink, and Trino.
- **Owned elsewhere**: SPEC-0180 and POL-0094 own the Iceberg catalog, table bucket, and SeaweedFS storage operations.
- **Out of Scope**: Detailed dashboard design for individual data visualization tools (Grafana).
- **Non-goals**: Real-time transactional SQL data processing (owned by core PostgreSQL).

### AI Agent Requirements

- **Allowed Actions**: Query analytics schemas, analyze log patterns, suggest SQL query optimizations.
- **Disallowed Actions**: Delete source data, make unauthorized configuration changes to a running analytics cluster.

## Risks

- **Dependency**: All analytics engines depend on declared networks, compose profiles, bind-backed named volumes, and Docker Secrets; the lakehouse engines also depend on the Iceberg catalog in SeaweedFS and Kafka (stream input).
- **Risk**: Risk of resource shortage on analytics nodes (storage/compute) during large-scale data inflow.
- **Assumption**: Source data is reliably supplied through the core data tier or the messaging tier.

## Traceability

- **Architecture Description**: [0012-data-analytics-architecture.md](../02.architecture/descriptions/0012-data-analytics-architecture.md)
- **ADR**: [0039-analytics-engines-after-lakehouse-convergence.md](../02.architecture/decisions/0039-analytics-engines-after-lakehouse-convergence.md) (supersedes ADR-0015)
- **Spec**: [SPEC-0180](../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md) (lakehouse 도입과 ksqlDB·StarRocks 제거)
- **Guide**: [README.md](../05.operations/guides/README.md)
