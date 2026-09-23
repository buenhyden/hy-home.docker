---
title: "Trino (Iceberg)"
version: "1.0.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-trino] -->
# Trino (Iceberg)

> On-demand OPTIONAL single-node SQL engine over Iceberg tables in the SeaweedFS REST catalog.

## Overview

Trino는 `lakehouse` profile로 선택되는 **OPTIONAL** SQL engine입니다.
coordinator 한 개가 작업도 실행하며, catalog `lakehouse`는 Spark와 같은
SeaweedFS Iceberg REST catalog(`seaweedfs-s3:8181`)와 `lakehouse` S3 identity를
사용합니다. HTTP API에 인증이 없으므로 `127.0.0.1`에만 게시하고 route는 없습니다.

## Audience

이 README의 주요 독자:

- Data engineers
- Operators
- AI Agents

## Scope

### In Scope

- Single-node Trino with the `lakehouse` Iceberg catalog.
- Environment-driven catalog file and the scoped S3 identity.

### Out of Scope

- Workers, TLS, authentication and a Traefik route.
- Batch maintenance ([Spark](../spark/README.md)) and streaming (Flink, S14).

## Structure

```text
trino/
├── README.md                   # This file
├── docker-compose.yml          # Single-node service
├── hyhome-trino.sh             # Exports the secret, then starts Trino
└── catalog/
    └── lakehouse.properties    # Iceberg REST catalog (SigV4) and native S3
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | Trino (version in `docker-compose.yml`) | Single node, 2 CPUs, 2 GiB, heap 80% |
| **Catalog** | SeaweedFS Iceberg REST | SigV4 (`signing-name=s3`), view endpoints off |
| **Storage** | SeaweedFS S3 | Native S3 file system, path-style |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `TRINO_HOST_PORT` | No | Loopback host port for the HTTP API (default: 18090). |
| `SEAWEEDFS_ICEBERG_PORT` | No | REST catalog port on `seaweedfs-s3` (default: 8181). |

The secret is `seaweedfs_s3_lakehouse_secret_key` (STRG-015); the access key ID
is `lakehouse`. The catalog file reads both through `${ENV:…}`.

## Available Scripts

Starting the service requires runtime approval.

| Command | Description |
| :--- | :--- |
| `docker compose --profile lakehouse up -d trino` | Start the engine (writes nothing). |
| `docker compose exec trino trino --execute "SHOW SCHEMAS FROM lakehouse"` | Prove catalog access. |

## Validation

- `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests`

## Troubleshooting

- Exit `64`: the `lakehouse` secret is missing or empty.
- `Failed to list views`: `iceberg.rest-catalog.view-endpoints-enabled=false` is missing.
- `ForbiddenException`: follow the lakehouse runbook.

## Related Documents

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/catalog/04-data/0094-lakehouse/guide.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/catalog/04-data/0094-lakehouse/policy.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/catalog/04-data/0094-lakehouse/runbook.md`)
- [Documentation index](../../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Trino leaf in `04-data/lakehouse`; services: `trino`; unconditional root include, profile-selected, in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/lakehouse/trino/docker-compose.yml` |
| Config files | `docker-compose.yml`, `hyhome-trino.sh`, `catalog/lakehouse.properties` |
| Config values | profiles: `lakehouse` |
| Compose linkage | unconditional root include, profile-selected, in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/lakehouse/trino/docker-compose.yml` |
| Networks | `object_net` |
| Volumes | `./hyhome-trino.sh:/opt/hyhome/hyhome-trino.sh:ro`, `./catalog/lakehouse.properties:/etc/trino/catalog/lakehouse.properties:ro` |
| Ports | `127.0.0.1:${TRINO_HOST_PORT:-18090}:8080` |
| Labels | `hy-home.tier` |
| Secret refs | `seaweedfs_s3_lakehouse_secret_key` |
| Healthcheck | `/usr/lib/trino/bin/health-check` |
| Operations | Guide (`docs/05.operations/catalog/04-data/0094-lakehouse/guide.md`), Policy (`docs/05.operations/catalog/04-data/0094-lakehouse/policy.md`), Runbook (`docs/05.operations/catalog/04-data/0094-lakehouse/runbook.md`) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Run `SHOW SCHEMAS FROM lakehouse`, then follow the runbook. |

## How to Work in This Area

1. Trino ships its own Iceberg library; check it reads the tables Spark writes after an upgrade of either.
2. Renovate updates the image tag.
3. Table deletion and snapshot expiry run only with a named table and a recorded reason.

Runtime image authority is [docker-compose.yml](docker-compose.yml);
the [derived Compose image projection](../../../tech-stack.versions.json) is drift evidence.
