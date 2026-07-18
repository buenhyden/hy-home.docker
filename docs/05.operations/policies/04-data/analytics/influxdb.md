---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/analytics/influxdb.md -->

# InfluxDB Operations Policy

## Overview

이 문서는 `infra/04-data/analytics/influxdb`의 InfluxDB 운영 정책을 정의한다. Current implementation은 InfluxDB 3 Core 단일 compose와 database/endpoint source contract만 정의하며 token provisioning은 runtime-unverified 상태다.

## Policy Scope

- **Systems**: `influxdb` service, `docker-compose.yml`
- **Persistence**: `influxdb-data`, `influxdb-plugins`
- **Secrets**: root Compose declarations and metadata are not leaf server wiring; the InfluxDB leaf mounts neither declared secret and provisions no server token
- **Environments**: repo-local, development, homelab, and production-like rehearsals

## Controls

- **Required**: operations use `docker-compose.yml`, `INFLUXDB_DB_NAME`, port `8181`, and `/api/v3/write_lp` for line-protocol writes.
- **Required**: token creation/provisioning and authenticated write acceptance require separate runtime approval; this source-only change does not select or enable an offline admin token file.
- **Required**: retention or cleanup changes require database-scoped evidence and separate runtime approval.
- **Allowed**: source-only Compose and documentation validation without service startup.
- **Disallowed**: presenting static source checks as runtime acceptance, authorization, or data-migration evidence; source-only validation cannot prove authorization.

## Exceptions

Long retention or manual data cleanup requires owner approval and evidence showing the database, volume, and token boundary used.

## Verification

- `test -f infra/04-data/analytics/influxdb/docker-compose.yml`
- Confirm `INFLUXDB_DB_NAME`, port `8181`, and `/api/v3/write_lp` agree across source and active docs without claiming token provisioning.
- `bash scripts/validation/check-doc-implementation-alignment.sh`
- `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- On compose image/tag change
- On secret mount or volume path change
- On retention or migration requirement change

## Related Documents

- [Operations policies index](../../../README.md)
- [Usage guide](../../../guides/04-data/analytics/influxdb.md)
- [Recovery runbook](../../../runbooks/04-data/analytics/influxdb.md)
- [Infra README](../../../../../infra/04-data/analytics/influxdb/README.md)
