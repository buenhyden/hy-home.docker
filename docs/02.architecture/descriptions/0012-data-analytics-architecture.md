---
title: "Analytics Tier Architecture Description"
version: "1.1.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "architecture"
artifact_id: "AD-0012"
parent_ids:
- "REQ-0005"
created: "2026-03-26"
---

# Analytics Tier Architecture Description

## Context and Stakeholders

`infra/12-analytics` groups stream/batch processing, SQL queries, transformation,
data quality and BI for data engineers and analysts. The former description
covered only `04-data/analytics` storage engines; ADR-0045 makes the storage
versus processing boundary explicit. InfluxDB and OpenSearch remain in Data.

## System Boundaries

Analytics owns seven complete execution packages: Flink, Spark, Trino, Great Expectations, Superset, dbt and JupyterLab. Great Expectations validates data; software verification belongs to `11-quality`. Data owns the shared object/database stores;
Messaging transports events; Workflow schedules jobs; Observability handles
operational telemetry. This directory boundary provides neither physical
failure isolation nor a separate Compose project.

## Quality Attributes

Retain optional profiles and current network/secret boundaries. Preserve
Flink checkpoints and Superset metadata; processing packages are not assumed
stateless. Loopback-only Trino/Flink interfaces remain loopback-only. No
performance, HA, authenticated runtime or backup success is inferred from
static source validation. Runtime version pins remain in Compose/Dockerfiles.

## Components

| Package | Interface and dependency | Activation |
| --- | --- | --- |
| Flink | stream/batch SQL and Iceberg catalog; Kafka input selected separately | lakehouse |
| Spark | batch and Iceberg table maintenance | lakehouse |
| Trino | SQL over the SeaweedFS Iceberg catalog | lakehouse |
| Great Expectations | quality checks through Trino | lakehouse |
| Superset | BI, Keycloak OIDC and mng-pg metadata; configured Trino datasource | bi |
| dbt | PostgreSQL transformations using feature-owned grants/schema | analytics-engineering |
| JupyterLab | interactive data analysis, token-protected kernels and optional MLflow SDK access | data-science |

## Data Flow

Flink writes and Spark maintains Iceberg tables on SeaweedFS; Trino reads them.
Great Expectations validates through Trino and Superset presents configured
data sources. dbt uses PostgreSQL, not an implied Trino adapter. Shared
storage identity, schema ownership and provisioning stay unchanged. Running
a query engine does not automatically ingest a Kafka topic or run a dbt model.

## Deployment View

Root Compose includes all seven package files; existing profile memberships
control selection. No new analytics profile or HOME activation is added.
`hy-home.tier: analytics` describes the packages. Source paths move while
persistent host paths, volume identities and services remain unchanged.
Running-container reconciliation is a separate operational action.

## Traceability

- [REQ-0005](../../01.requirements/0005-data-analytics.md)
- [ADR-0039](../decisions/0039-analytics-engines-after-lakehouse-convergence.md)
- [ADR-0045](../decisions/0045-data-storage-and-analytics-tier-boundary.md)
- [SPEC-0197](../../98.archive/completed/03.specs/0197-infra-tier-layout/spec.md)

## Related Documents

- [Analytics packages](../../../infra/12-analytics/README.md)
- [Data architecture](0004-data-architecture.md)
- [Lakehouse guide](../../05.operations/guides/0094-lakehouse.md)
- [Superset guide](../../05.operations/guides/0097-superset.md)
- [dbt guide](../../05.operations/guides/0090-dbt.md)
