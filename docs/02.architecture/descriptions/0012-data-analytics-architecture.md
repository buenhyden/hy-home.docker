---
title: "Analytics Tier Architecture Description"
version: "1.3.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "AD-0012"
parent_ids:
- "REQ-0005"
created: "2026-03-26"
---

# Analytics Tier Architecture Description

## Overview

### Context and Stakeholders

The analytics tier groups stream/batch processing, SQL queries, transformation,
data quality and BI for data engineers and analysts. Since SPEC-0262 its packages
are standalone LAB entrypoints (`labs/lakehouse/docker-compose.yml`, `labs/dbt/docker-compose.yml`,
`labs/superset/docker-compose.yml`, `labs/jupyterlab/docker-compose.yml`) that join no HOME network and reach
HOME stores only through approved LAB endpoint inputs; `infra/12-analytics` holds
no root package. The former description
covered only `04-data/analytics` storage engines; ADR-0062 makes the storage
versus processing boundary explicit. OpenSearch remains in Data; InfluxDB is retired (ADR-0047).

## Scope

### System Boundaries

The analytics capability covers seven execution packages, delivered as four LAB entrypoints: Flink, Spark, Trino and Great Expectations (`lakehouse`), Superset, dbt and JupyterLab. No LAB is promoted; promotion is an owner decision recorded in each `labs/<name>/promotion.yaml`. Great Expectations validates data; software verification belongs to `11-quality`. Data owns the shared object/database stores;
Messaging transports events; Workflow schedules jobs; Observability handles
operational telemetry. Each LAB is its own Compose project (`hy-home-lab-<name>`), which isolates its project and network names but not host failure.

### Traceability

- [REQ-0005](../../01.requirements/0005-data-analytics.md)
- [ADR-0062](../decisions/0062-home-lab-membership.md)
- SPEC-0197

## Structure

### Architecture

| Package | Interface and dependency | Activation |
| --- | --- | --- |
| Flink | stream/batch SQL and Iceberg catalog; Kafka input selected separately | `lab-lakehouse` (LAB) |
| Spark | batch and Iceberg table maintenance | `lab-lakehouse` (LAB) |
| Trino | SQL over the SeaweedFS Iceberg catalog | `lab-lakehouse` (LAB) |
| Great Expectations | quality checks through Trino | `lab-lakehouse` (LAB) |
| Superset | BI, Keycloak OIDC and mng-pg metadata; configured Trino datasource | `lab-superset` (LAB) |
| dbt | PostgreSQL transformations using feature-owned grants/schema | `lab-dbt` (LAB) |
| JupyterLab | interactive data analysis, token-protected kernels and optional MLflow SDK access | `jupyterlab` (LAB) |

## Runtime and Deployment

### Runtime View

Flink writes and Spark maintains Iceberg tables on SeaweedFS; Trino reads them.
Great Expectations validates through Trino and Superset presents configured
data sources. dbt uses PostgreSQL, not an implied Trino adapter. Shared
storage identity, schema ownership and provisioning stay unchanged. Running
a query engine does not automatically ingest a Kafka topic or run a dbt model.

### Deployment View

Root Compose includes none of these packages. Each LAB entrypoint is started
on its own and selected by its LAB profile; none has a HOME activation. Service
identities are unchanged by the move. Running-container reconciliation is a
separate operational action.

## Quality and Risks

### Quality Attributes

Retain optional profiles and current network/secret boundaries. Preserve
Flink checkpoints and Superset metadata; processing packages are not assumed
stateless. Loopback-only Trino/Flink interfaces remain loopback-only. No
performance, HA, authenticated runtime or backup success is inferred from
static source validation. Runtime version pins remain in Compose/Dockerfiles.

## Related Documents

- [Analytics packages](../../../infra/12-analytics/README.md) and [LAB sources](../../../labs/README.md)
- [Data architecture](0004-data-architecture.md)
- [Lakehouse guide](../../05.operations/guides/15-labs/0094-lakehouse.md)
- [Superset guide](../../05.operations/guides/15-labs/0097-superset.md)
- [dbt guide](../../05.operations/guides/15-labs/0090-dbt.md)
