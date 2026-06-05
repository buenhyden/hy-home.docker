---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/analytics/influxdb.md -->

# InfluxDB Operations Policy

## Overview

이 문서는 `infra/04-data/analytics/influxdb`의 InfluxDB 운영 정책을 정의한다. current implementation은 InfluxDB 3.x Core primary compose와 InfluxDB 2.x legacy compose를 분리하고, API token/password는 Docker Secrets로 주입한다.

## Policy Scope

- **Systems**: `influxdb` primary service, `docker-compose.yml`, `docker-compose.v2.yml`
- **Persistence**: `influxdb-data`, `influxdb-plugins`
- **Secrets**: `influxdb_password`, `influxdb_api_token`
- **Environments**: repo-local, development, homelab, and production-like rehearsals

## Controls

- **Required**: primary operations must use `docker-compose.yml` unless a legacy InfluxDB 2.x Flux compatibility requirement is explicitly recorded.
- **Required**: token and password values must be supplied through Docker Secrets and must not be written into docs, shell history, or command output.
- **Required**: retention or cleanup changes require evidence of the selected InfluxDB variant because v3 and v2 management commands differ.
- **Allowed**: legacy v2 compose may be used for compatibility testing or migration evidence.
- **Disallowed**: treating v2 bucket commands as verified v3 primary operations without runtime evidence.

## Exceptions

Legacy v2 usage, long retention, or manual data cleanup requires owner approval and evidence showing which compose file, volume, and token boundary were used.

## Verification

- `test -f infra/04-data/analytics/influxdb/docker-compose.yml`
- `test -f infra/04-data/analytics/influxdb/docker-compose.v2.yml`
- `bash scripts/validation/check-doc-implementation-alignment.sh`
- `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- On compose image/tag change
- On secret mount or volume path change
- On retention, migration, or legacy-v2 usage change

## Related Documents

- [Operations policies index](../../../README.md)
- [Usage guide](../../../guides/04-data/analytics/influxdb.md)
- [Recovery runbook](../../../runbooks/04-data/analytics/influxdb.md)
- [Infra README](../../../../../infra/04-data/analytics/influxdb/README.md)
