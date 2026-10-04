---
title: "Quality Results and Isolated Load Testing Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0203"
parent_ids:
- "REQ-0027"
- "ADR-0045"
- "ADR-0046"
- "SPEC-0201"
- "SPEC-0202"
created: "2026-10-03"
---

# Quality Results and Isolated Load Testing Specification

## Overview

Implement Prompt 03's shared quality execution and result contract on the
2026-10-03 local main `5f99e0e51b41b912f128daafb4a3d41539b77560`.
SPEC-0202 supplied the single development PostgreSQL engine and delegated
`perf_db` ownership here. k6 is the default load generator; WireMock supplies
HTTP dependencies; Locust is an isolated learning option. No external business
application is created in this repository.

## Boundaries and Inputs

The user supplied Prompt 03 after requiring Prompt 02's local main integration.
The latter completed locally; remote main remained
`e2c841eb9ef5086d0fbd6cc2ccd43ea35d89e26d` when rechecked. This package
owns source and bounded synthetic checks only. HOME service start, stop,
restart, real traffic, data migration, credential rotation, remote push, PR,
merge, DNS and firewall changes require separate concrete approval. Do not
read actual secret values, private environment files or raw production logs.
Future learning applications 07/08 are planning-only inputs.

At the `5f99e0e5` baseline, root included k6 and Locust under `testing`,
WireMock under `api-mock`, and an existing k6 Prometheus remote-write dashboard.
The dev-pg provisioner created only the `platform_dev` fixture; `perf_db` did
not exist. Alloy received traces but had no OTLP metrics export path. Use the
current tool image declarations and recheck official licenses/options/digests
before any runtime acceptance. Source changes do not prove running state.
The official `grafana-cold-storage/xk6-output-timescaledb` repository was
archived read-only on 2026-06-05; it is not a required output dependency.

## Behavior Contract

1. Infra owns common runner, result format, finalization, importer and
   dashboards. A Project-Template-derived external project owns scenarios,
   fixtures, application thresholds and its API/E2E. Root Compose never
   includes that project's source path. The runner accepts one approved,
   read-only scenario directory and an independent per-run output directory.
2. A run manifest binds `run_id`, `attempt`, `project_id`, environment,
   generator and source revision, tool image, fixture hash, mock mode, exact
   target origin and allowed network, users/rate/duration and resource budget.
   Target and redirect policy reject public/admin endpoints, origin drift and
   credential leakage before traffic. Actual load requires target-owner approval.
3. k6 checks become failing process results only through declared thresholds.
   A 202 response is acceptance, not asynchronous completion. Explicit 429/503
   expectations, dropped iterations, generator saturation, collector loss and
   incomplete evidence are separate states. Do not authenticate to management
   Keycloak on every request or provide management DB credentials to runners.
4. Raw artifacts, summary, exit metadata and manifest are immutable per
   `(run_id, attempt)`. The finalizer separates execution state, test verdict,
   evidence completeness and ingestion state. Unknown and interrupted runs
   resolve to explicit incomplete/failed states, never automatic pass.
5. A shared `perf_db` on dev-pg stores normalized results and project IDs.
   SQL roles and grants enforce project-scoped reads/inserts and reserve verdict
   changes to a separate authority. Connection alone gives no cross-project
   access. The importer checks checksum and manifest identity: exact replay is
   idempotent; same identity with different bytes or metadata is an error.
   Concurrent or partial imports and database outages cannot silently pass.
6. Preserve count, unit and source distribution or mergeable histogram for
   aggregate latency. Never average p95/p99. Reject invalid time, units,
   NaN/Infinity, truncated JSON and zero-sample success. Do not export URL
   query, Authorization, cookies or PII into raw performance data. Raw files
   and reports have a separate restricted SeaweedFS owner and durable reference;
   no high-frequency synchronous sample insert into the target dev-pg.
7. WireMock function mode uses a bounded request journal and reset between
   runs. Load mode disables the journal and prefers stateless mappings. Both
   use tracked read-only mappings/files, version-verified CLI switches and
   cannot overlap on the same state. Its unauthenticated admin API remains
   unexposed to the public, with internal peer risk documented. Synthetic,
   de-identified XML/JSON fixtures must follow the actual approved external
   interface; the simple tracked ping JSON is not a government API contract.
   Toxiproxy is considered only for non-HTTP dependencies such as DB/Kafka
   when their failure modes require it. A WireMock-only measurement is labeled
   mock performance, not application performance.
8. Locust master/worker leaves the normal root graph for a separate LAB
   entrypoint/project/network/volume. Headless execution declares worker
   count/expect-workers, users, spawn rate, duration, exit policy and CSV
   outputs; CSV full history is not request-level raw data. A LAB run cannot
   share normal HOME state or start implicitly through root profiles.
9. Reuse the existing Prometheus remote write path for k6. Shared Alloy gains
   a bounded OTLP metrics to Prometheus remote-write path while preserving
   traces/logs/profiles; only stable project/environment/service labels are
   admitted. Grafana provisions project/run/attempt filters, incomplete
   markers, regression comparison and raw artifact references using a
   read-only data source. Prompt 03 is the serial owner of this Alloy change;
   Prompt 04 consumes the resulting contract.
10. No speculative speech server, duplicated collector, Grafana, object store
    or additional HTTP mock service is introduced. A future approved speech
    product supplies its own distinct browser, quality and privacy tests.

## Technical Approach

Reuse the existing dev-pg provisioner only for engine and role creation where
its contract fits. The quality-owned schema/migrations define `perf_db` tables,
row-level access, ingestion identity, final state and artifact references.
The source runner validates manifest and paths before launching k6, writes
per-attempt files by exclusive create, and finalizes after process exit. A
separate importer reads finalized artifacts and commits one transaction. Use
synthetic, isolated fixtures for database and HTTP acceptance; check Docker
context, project, ports, volumes, networks, capacity and exact cleanup first.
No HOME deployment or real load follows source acceptance.
Alloy's delta-to-cumulative processor is experimental in the current official
component reference and needs an explicit stability flag; source acceptance
records the bounded stream settings and defers HOME rollout until isolated
end-to-end evidence and operator review.

## Interfaces and Data

- Input: versioned run manifest, approved scenario directory, target allowlist,
  project-specific secret references and a fresh writable result directory.
- Output: immutable manifest, k6/Locust raw and summary files, exit metadata,
  checksum index, final verdict, import receipt and restricted object reference.
- Database: `perf_db` contains project-scoped run/attempt/result/artifact rows;
  project writer/reader and verdict authority are distinct. Management
  metadata and secrets stay in mng-pg/mng-valkey.
- Observability: existing k6 remote write uses run identity tags; Alloy OTLP
  metrics flow to existing Prometheus; Grafana consumes a read-only view.

## Failure Modes and Guardrails

Fail closed on unknown target, redirect escape, missing/changed scenario,
nonempty result directory, invalid manifest, absent thresholds, interrupted
runner, zero/truncated/invalid samples, upload mismatch, checksum collision,
wrong project grant, DB disconnect, concurrent import and collector drops.
No retry overwrites raw evidence. No retention deletion or public object
publication is inferred. A separate Task must approve HOME activation,
project credential issuance, live traffic and restoration.

## Acceptance Contract

1. k6 and Locust are compared by language, load model, protocol, CI fit,
   current configuration, maintenance and license from current official
   sources; k6 remains default and WireMock remains an HTTP mock.
2. A versioned run contract rejects unauthorized origin/redirect/path/resource
   inputs and yields isolated, immutable per-attempt artifacts.
3. k6 threshold/exit, asynchronous completion, expected errors and incomplete
   telemetry produce distinct recorded outcomes.
4. Finalization and import handle zero/truncated/NaN/partial/changed files,
   DB outage and concurrent exact replay or conflict without false pass.
5. `perf_db` provision/migration and project A/B, reader-write, writer-verdict
   denial tests prove actual SQL authority, including future rows.
6. Function and load WireMock modes render separately; journal/reset/admin
   behavior is tested in isolation, with no HOME or public exposure.
7. Locust LAB is absent from normal root including `--profile '*'`; its
   independent render, bounded headless output and client-specific OTel or
   request-event/timeout contract are validated.
8. Existing k6 remote write is retained; Alloy receive, batch/resource,
   temporality, Prometheus export/remote write and Grafana read-only result
   views are checked without duplicating stacks. Synthetic counters and
   histograms cover delta/cumulative, duplicate/drop/retry and restart.
9. Operations and external-project handoff state input/output/schema/secret/
   network/recovery contracts and distinguish source, static, isolated,
   HOME and data-migration evidence.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [ADR-0045](../../02.architecture/decisions/0045-data-storage-and-analytics-tier-boundary.md)
- [ADR-0046](../../02.architecture/decisions/0046-capability-tiers-and-quality-boundary.md)
- [SPEC-0201](../0201-home-infrastructure-diagnosis-and-work-design/spec.md)
- [SPEC-0202](../0202-development-data-and-lab-isolation/spec.md)

## Open Questions

The concrete external project `project_id`, target origin/network, traffic
budget, artifact bucket/prefix, real credentials and retention are not yet
approved. Their absence blocks live load and provisioning for that project,
not generic source implementation or synthetic tests.

## Operational Impact

Root/quality/LAB Compose, dev-pg quality provision, Alloy and Grafana source
would change. A later operational Task must measure capacity, select exact
services and rollback, and separately authorize HOME activation and traffic.
