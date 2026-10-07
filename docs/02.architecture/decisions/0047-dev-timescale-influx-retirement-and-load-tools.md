---
title: "DEV Timescale, InfluxDB Retirement and Load Tools"
version: "0.2.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "architecture"
artifact_id: "ADR-0047"
parent_ids:
- "AD-0004"
- "AD-0031"
created: "2026-10-07"
---

# ADR-0047: DEV Timescale, InfluxDB Retirement and Load Tools

## Context

The 2026-10-07 user request asks for one time-series and test-result store,
removal of every active InfluxDB surface, a single default load tool, and
HA/replica services kept out of normal startup. At `main` `23b0e6959`,
`dev-pg` already runs a TimescaleDB build, `mng-pg` holds management metadata,
k6 has a run/result contract, Locust and every HA/cluster service already
live in standalone `labs/*.yml` files, and `infra/04-data/influxdb` is still
root-included with its own profile and Traefik route. ADR-0045 lists InfluxDB
in the Data tier and REQ-0005-FR-0001 still requires it. SPEC-0212 records the
baseline and inventory.

### Decision Drivers

Reuse running engines and contracts. Keep one owner per data role. Do not
duplicate raw results across stores. Keep normal startup free of lab topology.
Removal must be complete in source while data disposal stays a separate,
verified operation.

## Decision

1. DEV TimescaleDB is the store for project time-series history and for
   `perf_db` results. Run, attempt, verdict and checksum records stay ordinary
   relational tables; only measured point/histogram tables become hypertables.
2. MNG PostgreSQL stays plain PostgreSQL for service metadata. It receives no
   TimescaleDB extension and no test raw data.
3. InfluxDB is retired from every active surface: service, root include,
   profile, route, env keys, version projection, consumers, active operations
   documents and their tests. Historical records and the migration receipt
   stay. Source removal and data purge are reported separately.
4. k6 is the default load tool. Locust stays a standalone LAB for Python or
   protocol comparisons. WireMock simulates dependencies and is not a load
   generator. Live load metrics flow through the existing Alloy to Prometheus;
   final results are imported into `perf_db` after the run.
5. HA, replica and multi-broker topologies stay in standalone LAB files with
   their own project, network, data root, secrets and ports. They are never
   root-included; a profile is a selector, not an isolation boundary.

## Alternatives

### Options Considered

- Keep InfluxDB as an optional service: rejected; the request retires it and
  it would remain a second time-series owner.
- QuestDB, ClickHouse or VictoriaMetrics: deferred to LAB comparison when a
  measured bottleneck appears; none has a current consumer.
- TimescaleDB on MNG: rejected; no MNG consumer needs it.
- Locust as default: rejected for now; k6 already owns the result contract.
  The choice is reopened if Python protocol needs dominate.
- Root profiles for HA services: rejected; explicit service targeting
  activates a profiled service, so a profile cannot keep lab services out.

## Consequences

ADR-0045's Data tier list loses InfluxDB once the retirement change lands;
its storage/processing boundary is otherwise unchanged. REQ-0005,
AD-0004/AD-0012, POL-0078 and the InfluxDB guide, policy and runbook change
in that same follow-on package. A DEV-only engine shares CPU and I/O between
projects; a separate quality instance is considered only after measured
interference, never by moving load to MNG.

### Compliance

The retirement package proves an empty active reference set outside history,
a root model without `influxdb`, and passing replacement regressions. The
LAB package proves no LAB key or network in the root `--profile '*'` model
and a standalone render for each LAB file.

### Follow-up

Accepted on 2026-10-07 with SPEC-0213, which implements decisions 1-3 and
retires InfluxDB. Decisions 4 and 5 describe the current source (k6 default,
Locust and HA topologies in standalone LAB files); the live load metric path
is completed by the follow-on quality package. Real data export, purge and HOME container removal
need a confirmed target and recovery path; until then they stay `NOT_RUN`.

## Related Documents

- [AD-0004](../descriptions/0004-data-architecture.md)
- [AD-0031](../descriptions/0031-home-development-host.md)
- [ADR-0045](0045-data-storage-and-analytics-tier-boundary.md)
- [SPEC-0212](../../03.specs/0212-request-baseline-and-reconciliation/spec.md)
