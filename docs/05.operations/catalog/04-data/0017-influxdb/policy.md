---
title: "InfluxDB Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0017"
parent_ids:
- "AD-0012"
created: "2026-05-17"
---

# InfluxDB Operations Policy

## Overview

이 문서는 `infra/04-data/analytics/influxdb`의 InfluxDB 운영 정책을 정의한다. Current implementation은 InfluxDB 3 Core 단일 compose와 database/endpoint source contract만 정의하며 token provisioning은 runtime-unverified 상태다.

## Policy Scope

- **Systems**: `influxdb` service, `docker-compose.yml`
- **Persistence**: `influxdb-data`, `influxdb-plugins`
- **Secrets**: root Compose declarations and metadata are not leaf server wiring; the InfluxDB leaf mounts neither declared secret and provisions no server token
- **Environments**: repo-local, development, homelab, and production-like rehearsals

## Controls

- **Activation**: use root-project selection `docker compose --profile influxdb config --quiet`; starting or restarting `influxdb` is a separately approved runtime action.
- **Network and authorization**: keep the service on `edge_net` behind the declared TLS router and gateway middleware. A `401` proves an authentication challenge, not successful authorization. Provisioning or rotating a token is outside this document.
- **Retention and backup**: define database retention before enabling a consumer. A recovery point must preserve the documented local-object-store order: snapshots, database Parquet files, WAL, catalog log, then catalog checkpoint. Store it outside the live data path and record whether encryption at rest is configured; none is proven here.
- **Resources**: retain the inherited 1 CPU/512 MiB ceiling until measured ingest, compaction, query latency, disk growth, and restore duration justify a reviewed change.
- **Upgrade and migration**: review release notes and rehearse the candidate image against a copied recovery point. Do not substitute InfluxDB 2 backup/restore commands or Enterprise-only commands for this Core deployment.
- **Removal**: removal requires a confirmed lack of consumers, an owner decision for both bind-backed volumes, an export or retained recovery point, and separate approval for deletion.
- **Required**: operations use `docker-compose.yml`, operator-selected database name, port `8181`, and `/api/v3/write_lp` for line-protocol writes.
- **Required**: token creation/provisioning and authenticated write acceptance require separate runtime approval; this source-only change does not select or enable an offline admin token file.
- **Required**: retention or cleanup changes require database-scoped evidence and separate runtime approval.
- **Allowed**: source-only Compose and documentation validation without service startup.
- **Disallowed**: presenting static source checks as runtime acceptance, authorization, or data-migration evidence; source-only validation cannot prove authorization.

## Exceptions

Long retention or manual data cleanup requires owner approval and evidence showing the database, volume, and token boundary used.

## Verification

- `test -f infra/04-data/analytics/influxdb/docker-compose.yml`
- Confirm operator-selected database name, port `8181`, and `/api/v3/write_lp` agree across source and active docs without claiming token provisioning.
- `python3 scripts/validation/check-document-links.py --mode all`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Review Cadence

- On compose image/tag change
- On secret mount or volume path change
- On retention or migration requirement change

## Traceability

- Declared parent: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](guide.md) (`GDE-0017`), [Runbook](runbook.md) (`RUN-0017`)

## Related Documents

- [InfluxDB 3 Core backup and restore](https://docs.influxdata.com/influxdb3/core/admin/backup-restore/)
- [Compose implementation](../../../../../infra/04-data/analytics/influxdb/docker-compose.yml)

- [Operations policies index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/analytics/influxdb/README.md)
