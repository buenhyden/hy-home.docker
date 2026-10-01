---
title: "Infrastructure Tier Layout and Documentation Consistency"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0197"
parent_ids:
- "REQ-0005"
- "REQ-0027"
- "AD-0004"
- "AD-0012"
created: "2026-10-01"
---

# Infrastructure Tier Layout and Documentation Consistency

## Overview

Flatten twelve storage and data-platform packages under `infra/04-data`,
create `infra/12-analytics` for five processing, query, quality and BI packages,
and move PostgreSQL-based dbt there from `infra/09-tooling`. Retain the other
tier boundaries and correct the documented inventory drift.

The user approved this design and requested the written specification on
2026-10-01. The user subsequently approved the written specification and requested the
implementation plan on 2026-10-01. Frontmatter remains draft for initial
registration; implementation still requires written-plan review and execution
method selection.

## Boundaries and Inputs

Reuse REQ-0027's discovery and consistency requirements, REQ-0005's optional
analytics boundary, and AD-0004, AD-0012 and AD-0031 as current architecture
inputs. The approved scope covers structure, classification, configuration
references and documentation, including dbt's change of tier ownership.

Preserve service behavior, activation, images, credentials, resource limits and
persistent data. Do not deploy, restart, consolidate or retire services, move
host data, or split the root Compose project. SPEC-0182 and other concurrent
packages retain their scope. Frozen archives and dated research snapshots
are not rewritten to make their historical paths look current.

On 2026-10-01, tracked source contained 49 included Compose fragments and 153
service declarations. Data owned 17 fragments/72 declarations; its five
Analytics candidates owned eight declarations. These are dated source counts,
not running-container counts or constants to add to operational READMEs.

## Behavior Contract

### Package placement

All paths below are relative to `infra/`. Move each package as a unit with its
Compose file, README, build sources, scripts and configuration. Helper
containers and provisioning jobs stay with their package.

| Existing package | Destination |
| --- | --- |
| `04-data/operational/mng-db` | `04-data/mng-db` |
| `04-data/operational/supabase` | `04-data/supabase` |
| `04-data/relational/postgresql-cluster` | `04-data/postgresql-cluster` |
| `04-data/cache-and-kv/valkey-cluster` | `04-data/valkey-cluster` |
| `04-data/nosql/cassandra` | `04-data/cassandra` |
| `04-data/nosql/couchdb` | `04-data/couchdb` |
| `04-data/nosql/mongodb` | `04-data/mongodb` |
| `04-data/lake-and-object/seaweedfs` | `04-data/seaweedfs` |
| `04-data/analytics/influxdb` | `04-data/influxdb` |
| `04-data/analytics/opensearch` | `04-data/opensearch` |
| `04-data/specialized/neo4j` | `04-data/neo4j` |
| `04-data/specialized/qdrant` | `04-data/qdrant` |
| `04-data/lakehouse/flink` | `12-analytics/flink` |
| `04-data/lakehouse/spark` | `12-analytics/spark` |
| `04-data/lakehouse/trino` | `12-analytics/trino` |
| `04-data/lakehouse/great-expectations` | `12-analytics/great-expectations` |
| `04-data/analytics/superset` | `12-analytics/superset` |
| `09-tooling/dbt` | `12-analytics/dbt` |

### Responsibilities

Data owns storage and data-platform packages. SeaweedFS remains shared storage
for observability, AI and analytics consumers; Supabase remains intact.
Analytics owns processing, transformation, SQL queries, quality and BI.
Flink checkpoints and Superset metadata remain persistent state even though
the packages move. dbt keeps its PostgreSQL adapter; no new pipeline or Trino
adapter is introduced.

Messaging transports events; Workflow schedules and coordinates jobs;
Observability handles operational telemetry; Tooling retains other development
and operations tools. Tier numbers do not define startup order, isolation or
independent deployment. Tier READMEs provide navigation and role/classification
summaries; package READMEs and existing operations owners retain exact selectors
and dependency details. Do not add a competing service registry.

## Technical Approach

### Alternatives and decision

The eight current Data categories mix operational role, database model and
workload. Flattening all seventeen packages removes nesting but still mixes
BI/processing with storage. The approved split adds one capability tier and
keeps both tiers flat. Further database-type, BI-only or single-platform tiers
have no demonstrated need in this change.

Root `docker-compose.yml` remains the entry point and
`infra/common-optimizations.yml` remains the shared template. Update includes,
relative `extends.file`, build contexts, repository-owned bind sources and
cross-package provisioning references together. Preserve package contents
except for reviewed path and classification adjustments.

Set `hy-home.tier` to `analytics` for the six Analytics packages and retain
Data labels for the twelve retained packages. Trace label consumers so
monitoring/discovery does not silently lose services. Other labels and all
profile memberships remain unchanged.

Update active consumers: hardening tier dispatch/checks, `.github/labeler.yml`,
existing image projection, operations Guide implementation bindings,
source-path tests, README links and architecture descriptions. In particular,
update the tier table and directory tree in `infra/README.md` and the Data
and Tooling entries. Use registered generators for derived files. Transfer
useful content from the seven existing Data category READMEs to the surviving
tier/package READMEs, then remove those obsolete directory indexes. They are
`infra/` navigation files, not active-stage records requiring Stage 98 bodies;
Git history retains their previous contents. Existing stage documents still
follow their own retention rules. Do not leave compatibility symlinks or
duplicate current package copies.

Align AD-0004 with HOME storage versus LAB clusters and remove unsupported
tier-wide HA/latency guarantees. AD-0012 describes the current Data analytics
sub-tier, not an existing physical tier 12. Record the new boundary in an
architecture decision and align descriptions and REQ-0005 path references
without changing requirement identifiers or engine responsibilities.
ADR-0039's separation of InfluxDB/OpenSearch from lakehouse processing remains.

Correct the existing cross-tier drift: replace the stale HOME count in
`infra/README.md` with a source query, reconcile Observability service/profile
summaries, include `restic-offsite` in Tooling's backup map, and describe flat
package layout plus Observability's tier-level Compose exception. The old
lakehouse category disappears, so no README is added at its old path.

### Research basis

Official sources were consulted on 2026-10-01. They establish tool semantics;
the placement recommendation is a repository-specific inference.

- [Docker include](https://docs.docker.com/reference/compose-file/include/):
  included models resolve paths from their own project directories.
- [Docker extends](https://docs.docker.com/compose/how-tos/multiple-compose-files/extends/):
  shared configuration and relative paths require explicit checking.
- [Docker config](https://docs.docker.com/reference/cli/docker/compose/config/):
  resolved-model comparison.
- [Flink](https://flink.apache.org/what-is-flink/flink-architecture/) and
  [Trino](https://trino.io/docs/current/overview.html): processing and query
  engines have roles distinct from their external storage.
- [GX](https://docs.greatexpectations.io/docs/core/introduction/),
  [Superset](https://superset.apache.org/) and
  [dbt](https://docs.getdbt.com/docs/introduction): quality, BI and transformation.

## Interfaces and Data

Allowed resolved-model differences are the eighteen mapped source relocations
and Analytics tier labels. Compare corresponding repository bind/build/config
paths through that explicit map and verify destination contents. Do not
normalize arbitrary differences. Persistent host paths, named-volume names
and options, project/service/container names, ports, networks, dependencies,
commands, healthchecks, profiles, secret references and resource limits must
otherwise remain equal.

Render with `.env.example` for public reproducibility. Do not read or emit
private environment or secret values. Public-model equality does not prove
private overrides or running containers use the new paths.

## Failure Modes and Guardrails

- A moved mount can resolve to the wrong existing file. Check resolution and
  mapped source contents, not just syntax.
- Tier dispatch and label filters can omit Analytics. Retain all existing
  checks for moved services and verify both Data and Analytics selection.
- Broad replacements can corrupt history. Update active consumers selectively
  and preserve archived bytes and dated observations.
- Moving mounted source directories affects later container recreation.
  Inventory these mounts before implementation and report any need for a
  separately approved operational step; do not claim live acceptance.
- Stop on unapproved model differences and correct the migration. Do not
  weaken checks or expand into service redesign to obtain PASS.

## Acceptance Contract

1. All eighteen packages have the exact destinations above: twelve Data and
   six Analytics. No service is added, removed or duplicated. Obsolete paths
   have no active executable/navigation consumers; historical provenance is
   distinguished from current references.
2. Root include and shared template resolution succeed. Public resolved-model
   comparisons preserve execution/storage identities and settings except
   mapped source paths and Analytics labels. Compare the full declared model,
   HOME selection and affected profile selections.
3. Existing hardening, operations catalog, image projection, tier-label
   consumers and source-path tests recognize the layout without dropping
   previous checks. New nontrivial checker logic has failing-before and
   passing-after regression evidence and at least 80% changed-line coverage.
4. Tier/package READMEs, operations bindings, current requirement paths and
   architecture descriptions agree with the new boundary. HOME count,
   Observability selector and backup inventory defects are corrected;
   the seven obsolete category indexes are removed after content transfer,
   while governed stage records follow existing retention policy.
5. Scoped Compose/catalog checks, affected hardening/tests, document
   metadata/link/lifecycle checks and the registered changed CI profile pass.
   Author-independent read-only review finds no unresolved material omissions
   or unsupported completion claims.
6. The eventual Task records baseline, allowed comparison exceptions,
   commands/results and acceptance-to-durable-document mapping. It separates
   source verification from unperformed runtime reconciliation. No private
   values, host-data moves, restarts or unrelated SPEC-0182 changes occur.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md):
  FR-0001, FR-0003, FR-0004, FR-0005; NFR-0001, NFR-0003, NFR-0004.
- [REQ-0005](../../01.requirements/0005-data-analytics.md): preserve
  FR-0001, FR-0003, FR-0005, FR-0006 and opt-in activation.
- [AD-0004](../../02.architecture/descriptions/0004-data-architecture.md),
  [AD-0012](../../02.architecture/descriptions/0012-data-analytics-architecture.md),
  [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md):
  current architecture inputs and boundary alignment targets.
- [ADR-0039](../../02.architecture/decisions/0039-analytics-engines-after-lakehouse-convergence.md):
  retained engine responsibilities.
- [POL-0078](../../05.operations/policies/0078-compose-profile-vocabulary.md):
  unchanged activation vocabulary.

## Open Questions

No unresolved design choice remains for this specification. Written-spec
approval was received on 2026-10-01. The [implementation plan](plan.md) records
checks and ordering and awaits user review and execution-method selection.
It does not authorize runtime changes.

## Operational Impact

This is a repository migration, not deployment. The root Compose project,
opt-in selectors and persistent data remain intact. Running containers are not
recreated by the implementation task. Repository rollback restores moved
files and references together; it is not data restoration. Later runtime
reconciliation must account for moved source mounts and labels under its own
scoped authorization.
