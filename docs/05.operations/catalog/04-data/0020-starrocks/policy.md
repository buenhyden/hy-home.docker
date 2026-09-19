---
title: "StarRocks Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0020"
parent_ids:
- "AD-0012"
created: "2026-05-17"
---

# StarRocks Operations Policy

## Overview

이 문서는 `infra/04-data/analytics/starrocks`의 StarRocks 운영 정책을 정의한다. current implementation은 `starrocks-fe`와 `starrocks-be` 단일 pair를 `starrocks` profile로 제공한다.

## Policy Scope

- **Systems**: `starrocks-fe`, `starrocks-be`
- **Persistence**: `starrocks-fe-data`, `starrocks-be-data`
- **Interfaces**: FE MySQL-compatible port `9030`, FE HTTP port `8030`, BE HTTP port `8040`
- **Environments**: repo-local, development, homelab, and production-like rehearsals

## Controls

- **Activation and exposure**: validate with `docker compose --profile starrocks config --quiet`. The three wildcard host publications are development-only until network and authentication controls are approved.
- **Authentication**: do not retain passwordless administrative access for a promoted workload. Create named least-privilege query/load and backup roles without placing passwords in Compose or docs.
- **Retention and recovery**: define table/partition retention per consumer. A valid recovery point is a completed remote-repository snapshot plus FE/BE metadata evidence, destination integrity, and restore rehearsal; copying live FE/BE directories is not the documented backup method.
- **Resources**: the pair can consume up to 4 CPUs/4 GiB in aggregate. Promotion requires measured query/load concurrency, disk growth, compaction, and restore duration.
- **Upgrade**: back up first, check the supported version path, and validate FE/BE compatibility in an isolated pair. Never downgrade rewritten metadata or data in place.
- **Removal**: require consumer confirmation, completed export/snapshot retention, repository credential disposition, and explicit approval before deleting either bind-backed volume.
- **Required**: BE registration must preserve the compose command that adds `starrocks-be:9050` to FE before starting BE.
- **Required**: FE and BE health evidence must use `SHOW FRONTENDS` and `SHOW BACKENDS` through `starrocks-fe:9030`.
- **Required**: data load retry procedures must record label, database, table, and final load state.
- **Allowed**: schema and load examples for development when they do not imply benchmark completion.
- **Disallowed**: documenting undeclared Prometheus exporters, undeclared Docker Secrets, or multi-node HA topology as current implementation.

## Exceptions

Manual FE metadata changes, backend add/drop operations, or destructive data cleanup require owner approval and captured pre-change state.

## Verification

- `test -f infra/04-data/analytics/starrocks/docker-compose.yml`
- `mysql -u root -h starrocks-fe -P 9030 -e "SHOW FRONTENDS;"`
- `mysql -u root -h starrocks-fe -P 9030 -e "SHOW BACKENDS;"`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Review Cadence

- On StarRocks image, FE/BE volume, port, or BE registration command change
- Monthly when load or schema examples are used as operating procedures

## Traceability

- Declared parent: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](guide.md) (`GDE-0020`), [Runbook](runbook.md) (`RUN-0020`)

## Related Documents

- [StarRocks backup and restore statements](https://docs.starrocks.io/docs/sql-reference/sql-statements/backup_restore/)
- [Compose implementation](../../../../../infra/04-data/analytics/starrocks/docker-compose.yml)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations policies index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/analytics/starrocks/README.md)
