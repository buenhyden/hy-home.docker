---
title: "Data Optimization and Hardening Architecture"
version: "1.1.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0019"
parent_ids:
- "REQ-0004"
created: "2026-03-28"
---
# Data Optimization and Hardening Architecture

## Context and Stakeholders

This document describes the relational, NoSQL, cache, object storage,
analytics, and graph/vector service structure of `infra/04-data/`. The
maintainer and operator manage the common Compose contract and the per-engine
lifecycle/recovery procedure separately.

## System Boundaries

- `infra/04-data/**` owns the data service Compose topology and per-engine
  configuration.
- The Stage 03 capability Spec owns the implementation boundary, and the
  Stage 05 subject owns the operational procedure.
- Gateway routing, Stage 03 security secret supply, and Stage 06 telemetry
  collection are each provided by their own layer.
- Product business schema/query and cloud migration are outside this
  architecture.

## Components

- Analytics: InfluxDB, OpenSearch
- Cache and KV: Valkey cluster
- Object storage: SeaweedFS
- NoSQL: Cassandra, CouchDB, MongoDB
- Operational platforms: management database, Supabase
- Relational: PostgreSQL cluster
- Specialized: Neo4j, Qdrant

Each component keeps its own configuration and volume, and combines the
common optimization, secret, healthcheck, and network contract in Compose.

## Data Flow

Services connect explicitly through SQL, Redis/Valkey, S3-compatible, search,
vector, and graph protocols. Persistent state keeps a per-service volume
boundary under `${DEFAULT_DATA_DIR}`, and credentials are injected through
the Compose secret contract.

## Deployment View

The current implementation combines `infra/common-optimizations.yml` with
each engine Compose file. The hardening and Compose validators check secret,
label, expose, and healthcheck consistency. Additional HA, lifecycle
automation, and failover drills are not treated as implemented for every
engine today, and are introduced only through a separately approved current
Requirement and ADR.

## Quality Attributes

- **Security**: keeps credential injection consistent and reduces unnecessary
  exposure.
- **Reliability**: uses healthchecks and a per-engine recovery procedure.
- **Scalability**: an approved per-engine expansion must be introducible
  without breaking the common Compose boundary.
- **Operability**: the static gate, capability Spec, and Operations subject
  must describe the same topology and failure boundary.

## Traceability

- [REQ-0004](../../01.requirements/0004-data.md)
- [ADR-0040](../decisions/0040-data-hardening-gate-and-staged-expansion.md) (supersedes ADR-0019)
- [SPEC-0004](0004-data-architecture.md)
- [Data hardening guide](../../05.operations/guides/0030-data-optimization-hardening.md)
- [Data hardening policy](../../05.operations/policies/0030-data-optimization-hardening.md)
- [Data hardening runbook](../../05.operations/runbooks/0030-data-optimization-hardening.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
