---
title: "Data Storage and Analytics Tier Boundary"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "architecture"
artifact_id: "ADR-0045"
parent_ids:
- "AD-0012"
created: "2026-10-01"
---

# ADR-0045: Data Storage and Analytics Tier Boundary

## Context

Data's former eight categories mixed operational role, data model and
processing workload. Flink/Spark/Trino/GX/Superset lived beside storage while
dbt transformation was in Tooling. The user approved SPEC-0197 and its native
execution plan on 2026-10-01. Initial registration uses the proposed state;
this records the approved design without inventing a prior Git transition.

## Decision Drivers

Make package discovery predictable; keep storage and processing ownership
explicit; preserve runtime identities, profiles and persistent data; reuse
root Compose and existing operations/verification contracts.

## Options Considered

- Keep eight categories: smallest move but retains mixed classification axes.
- Flatten all seventeen Data packages: removes nesting, keeps BI/processing
  mixed with storage, and leaves dbt elsewhere.
- Flatten twelve Data packages and establish Analytics with the five processing
  packages plus dbt: one additional tier with a clear capability boundary.

## Decision

Adopt the third option. Data keeps mng-db, Supabase, PostgreSQL/Valkey clusters,
Cassandra, CouchDB, MongoDB, SeaweedFS, InfluxDB, OpenSearch, Neo4j and Qdrant.
Analytics owns Flink, Spark, Trino, Great Expectations, Superset and dbt.
Each package is a direct tier child and retains its helper/provisioning jobs.
SeaweedFS stays shared across consumers; dbt stays on PostgreSQL.

Messaging transports, Workflow orchestrates and Observability monitors.
Tier numbering is a namespace, not startup order or an isolation guarantee.
Keep the root project, service names, opt-in selectors and storage identities.
Only source relocations and Analytics tier labels change in rendered models.

## Consequences

A single role-oriented index replaces overlapping category indexes. Current
path consumers and hardening dispatch must move atomically with packages.
Source mounts need explicit consideration before future runtime recreation.
No new runtime, service registry, profile or independent project is introduced.
ADR-0039's engine selection and storage/processing separation remain valid.

## Traceability

- [AD-0004](../descriptions/0004-data-architecture.md)
- [AD-0012](../descriptions/0012-data-analytics-architecture.md)
- [REQ-0005](../../01.requirements/0005-data-analytics.md)
- [SPEC-0197](../../03.specs/0197-infra-tier-layout/spec.md)

## Compliance

Use the Spec's exact move map and model-difference allowlist. Registered
Compose, hardening, catalog and document gates and independent review provide
source acceptance. Task evidence records actual results and limitations.

## Follow-up

Runtime reconciliation requires a separately scoped operation. Do not treat
source validation as live rollout, HA, authentication or recovery evidence.
