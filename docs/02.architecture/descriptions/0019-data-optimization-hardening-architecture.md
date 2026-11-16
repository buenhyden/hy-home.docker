---
title: "Data Optimization and Hardening Architecture"
version: "1.2.5"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-16"
layer: "architecture"
artifact_id: "AD-0019"
parent_ids:
- "REQ-0004"
created: "2026-03-28"
---

# Data Optimization and Hardening Architecture

## Overview

### Purpose and Readers

This document describes the relational, cache, object storage, search, and
graph/vector service structure of `infra/04-data/`. The
maintainer and operator manage the common Compose contract and the per-engine
lifecycle/recovery procedure separately.

### System Boundary

- `infra/04-data/**` owns the data service Compose topology and per-engine
  configuration.
- The Stage 03 capability Spec owns the implementation boundary, and the
  Stage 05 subject owns the operational procedure.
- Gateway routing, `03-security` secret supply, and `06-observability`
  telemetry collection are each provided by their own layer.
- Product business schema/query and cloud migration are outside this
  architecture.

## Context and Constraints

### Context

Gateway routing, `03-security` secret supply, and `06-observability` telemetry collection come from their own layers.

### Constraints

Each engine combines the common optimization, secret, healthcheck, and network contract in Compose; credentials are injected through the Compose secret contract. Additional HA, lifecycle automation, and failover drills are not treated as implemented for every engine and need a separately approved current Requirement and ADR.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.

## Current Structure

### Building Blocks

- Development databases: `dev-db` (PostgreSQL and Valkey with provisioners
  and exporters)
- Management database: `mng-db`
- Search: OpenSearch
- Object storage: SeaweedFS
- Specialized: Neo4j, Qdrant
- Administration: RedisInsight
- Operational platforms: management database

The Valkey cluster, Cassandra, CouchDB, MongoDB, PostgreSQL HA and OpenSearch
cluster packages are standalone LABs under `labs/`, outside this tier; none is
promoted.

Each component keeps its own configuration and volume, and combines the
common optimization, secret, healthcheck, and network contract in Compose.

### Runtime and Deployment

#### Runtime View

Services connect explicitly through SQL, Redis/Valkey, S3-compatible, search,
vector, and graph protocols. Compose declares the state path of each service.
Management PostgreSQL and Valkey use `${DEFAULT_MANAGEMENT_DIR}`; development
PostgreSQL and Valkey use `${DEFAULT_DATA_DIR}`. The Compose secret contract
supplies credentials.

#### Deployment View

The current implementation combines `infra/common-optimizations.yml` with
each engine Compose file. The hardening and Compose validators check secret,
label, expose, and healthcheck consistency. Additional HA, lifecycle
automation, and failover drills are not treated as implemented for every
engine today, and are introduced only through a separately approved current
Requirement and ADR.

## Interfaces

### Contracts

Services connect through SQL, Redis/Valkey, S3-compatible, search, vector, and graph protocols, with credentials injected through the Compose secret contract (see Runtime View).

### Failure Boundaries

Separate volume paths delimit service state. The [Data hardening runbook](../../05.operations/runbooks/05-databases-and-storage/0030-data-optimization-hardening.md)
owns per-engine recovery. Healthchecks and volume definitions do not establish
restorability.

## Decisions

### Decision Links

- [ADR-0062](../decisions/0062-home-lab-membership.md)

### Quality and Risks

#### Quality Attributes

- **Security**: keeps credential injection consistent and reduces unnecessary
  exposure.
- **Reliability**: uses healthchecks and a per-engine recovery procedure.
- **Scalability**: an approved per-engine expansion must be introducible
  without breaking the common Compose boundary.
- **Operability**: the static gate, capability Spec, and Operations subject
  must describe the same topology and failure boundary.

## Traceability

### Requirement Mapping

- [REQ-0004](../../01.requirements/0004-data.md)

### Currentness and Lineage

- [AD-0004 Data Tier (04-data) Architecture Description](0004-data-architecture.md)

The description reflects the current tree at its `updated` date and history lives in Git.

Operations documents:

- [Data hardening guide](../../05.operations/guides/05-databases-and-storage/0030-data-optimization-hardening.md)
- [Data hardening policy](../../05.operations/policies/05-databases-and-storage/0030-data-optimization-hardening.md)
- [Data hardening runbook](../../05.operations/runbooks/05-databases-and-storage/0030-data-optimization-hardening.md)
