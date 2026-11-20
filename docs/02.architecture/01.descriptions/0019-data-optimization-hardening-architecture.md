---
title: "Data Optimization and Hardening Architecture"
version: "2.0.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "AD-0019"
parent_ids:
- "REQ-0004"
created: "2026-03-28"
---

# Data Optimization and Hardening Architecture

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-description payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context and Boundaries

##### System Boundary

- `infra/04-data/**` owns the data service Compose topology and per-engine
  configuration.
- The Stage 03 capability Spec owns the implementation boundary, and the
  Stage 05 subject owns the operational procedure.
- Gateway routing, `03-security` secret supply, and `06-observability`
  telemetry collection are each provided by their own layer.
- Product business schema/query and cloud migration are outside this
  architecture.

###### Purpose and Readers
<!-- core-payload-level:4 -->

This document describes the relational, cache, object storage, search, and
graph/vector service structure of `infra/04-data/`. The
maintainer and operator manage the common Compose contract and the per-engine
lifecycle/recovery procedure separately.

###### Context
<!-- core-payload-level:4 -->

Gateway routing, `03-security` secret supply, and `06-observability` telemetry collection come from their own layers.

##### Constraints

Each engine combines the common optimization, secret, healthcheck, and network contract in Compose; credentials are injected through the Compose secret contract. Additional HA, lifecycle automation, and failover drills are not treated as implemented for every engine and need a separately approved current Requirement and ADR.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.

#### Structure

##### Building Blocks

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

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| SQL (PostgreSQL in `dev-db` and `mng-db`) | PostgreSQL in `dev-db` and `mng-db` | Services that connect to the data tier | The description links no contract for this interface. | Per-engine recovery is owned by the [Data hardening runbook](../../05.operations/03.runbooks/05.databases-and-storage/0030-data-optimization-hardening.md). |
| Redis/Valkey protocol | Valkey in `dev-db` and `mng-db` | Services that connect to the data tier | The description links no contract for this interface. | Per-engine recovery is owned by the [Data hardening runbook](../../05.operations/03.runbooks/05.databases-and-storage/0030-data-optimization-hardening.md). |
| S3-compatible object storage | SeaweedFS | Services that connect to the data tier | The description links no contract for this interface. | Per-engine recovery is owned by the [Data hardening runbook](../../05.operations/03.runbooks/05.databases-and-storage/0030-data-optimization-hardening.md). |
| Search protocol | OpenSearch | Services that connect to the data tier | The description links no contract for this interface. | Per-engine recovery is owned by the [Data hardening runbook](../../05.operations/03.runbooks/05.databases-and-storage/0030-data-optimization-hardening.md). |
| Vector protocol | Qdrant | Services that connect to the data tier | The description links no contract for this interface. | Per-engine recovery is owned by the [Data hardening runbook](../../05.operations/03.runbooks/05.databases-and-storage/0030-data-optimization-hardening.md). |
| Graph protocol | Neo4j | Services that connect to the data tier | The description links no contract for this interface. | Per-engine recovery is owned by the [Data hardening runbook](../../05.operations/03.runbooks/05.databases-and-storage/0030-data-optimization-hardening.md). |
| Compose secret credential supply | `03-security` layer | Data tier engines | Compose secret contract | The description records no failure handling for this interface. |
| Gateway routing | Gateway layer | The description names no consumer for this interface. | The description links no contract for this interface. | The description records no failure handling for this interface. |
| Telemetry collection | The description names no producer for this interface. | `06-observability` layer | The description links no contract for this interface. | The description records no failure handling for this interface. |

Services connect through SQL, Redis/Valkey, S3-compatible, search, vector, and graph protocols, with credentials injected through the Compose secret contract (see Runtime View).

#### Runtime Behavior

##### Normal Flow

###### Runtime View
<!-- core-payload-level:4 -->

Services connect explicitly through SQL, Redis/Valkey, S3-compatible, search,
vector, and graph protocols. Compose declares the state path of each service.
Management PostgreSQL and Valkey use `${DEFAULT_MANAGEMENT_DIR}`; development
PostgreSQL and Valkey use `${DEFAULT_DATA_DIR}`. The Compose secret contract
supplies credentials.

###### Deployment View
<!-- core-payload-level:4 -->

The current implementation combines `infra/common-optimizations.yml` with
each engine Compose file. The hardening and Compose validators check secret,
label, expose, and healthcheck consistency. Additional HA, lifecycle
automation, and failover drills are not treated as implemented for every
engine today, and are introduced only through a separately approved current
Requirement and ADR.

##### Failure and Recovery

Separate volume paths delimit service state. The [Data hardening runbook](../../05.operations/03.runbooks/05.databases-and-storage/0030-data-optimization-hardening.md)
owns per-engine recovery. Healthchecks and volume definitions do not establish
restorability.

#### Quality Scenarios

##### Scenarios

###### Quality Attributes
<!-- core-payload-level:4 -->

- **Security**: keeps credential injection consistent and reduces unnecessary
  exposure.
- **Reliability**: uses healthchecks and a per-engine recovery procedure.
- **Scalability**: an approved per-engine expansion must be introducible
  without breaking the common Compose boundary.
- **Operability**: the static gate, capability Spec, and Operations subject
  must describe the same topology and failure boundary.

##### Trade-offs

- The tier keeps one common Compose contract (optimization, secret, healthcheck
  and network) for every engine and accepts that additional HA, lifecycle
  automation and failover drills are not implemented for every engine; each
  needs a separately approved current Requirement and ADR (Constraints,
  Deployment View).
- Healthchecks and volume definitions give start ordering and state
  separation but do not establish restorability; per-engine recovery stays in
  the Data hardening runbook (Failure and Recovery).
- Scalability is bounded by the common Compose boundary: an approved
  per-engine expansion must fit it without breaking it (Quality Attributes).

#### Decisions and Adoption

##### Decisions

- [ADR-0062](../02.decisions/0062-home-lab-membership.md)

##### Adoption Boundaries

###### Requirement Mapping
<!-- core-payload-level:4 -->

- [REQ-0004](../../01.requirements/0004-data.md)

###### Currentness and Lineage
<!-- core-payload-level:4 -->

- [AD-0004 Data Tier (04-data) Architecture Description](0004-data-architecture.md)

The description reflects the current tree at its `updated` date and history lives in Git.

Operations documents:

- [Data hardening guide](../../05.operations/01.guides/05.databases-and-storage/0030-data-optimization-hardening.md)
- [Data hardening policy](../../05.operations/02.policies/05.databases-and-storage/0030-data-optimization-hardening.md)
- [Data hardening runbook](../../05.operations/03.runbooks/05.databases-and-storage/0030-data-optimization-hardening.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
