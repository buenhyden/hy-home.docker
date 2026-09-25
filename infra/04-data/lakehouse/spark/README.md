---
title: "Spark (Iceberg)"
version: "1.0.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-spark] -->
# Spark (Iceberg)

> On-demand OPTIONAL batch and table-maintenance job over Iceberg tables in the SeaweedFS REST catalog.

## Overview

Spark는 `lakehouse` profile로 선택되는 **OPTIONAL** one-shot 작업입니다.
SeaweedFS 내장 Iceberg REST catalog(`seaweedfs-s3:8181`)와 `lakehouse` table
bucket을 `lakehouse` S3 identity로 사용합니다. 기본 명령은 namespace 조회만
수행하며, 쓰기는 명시적 `docker compose run --rm spark ...`로만 실행합니다.

## Audience

이 README의 주요 독자:

- Data engineers
- Operators
- AI Agents

## Scope

### In Scope

- Spark local-mode job image with the pinned Iceberg runtime and AWS bundle.
- Catalog configuration generated at start and the scoped S3 identity.

### Out of Scope

- A Spark cluster (master/worker), Spark UI or history server.
- Interactive SQL serving ([Trino](../trino/README.md)) and streaming ([Flink](../flink/README.md)).

## Structure

```text
spark/
├── README.md          # This file
├── Dockerfile         # apache/spark plus checksum-pinned Iceberg jars
├── docker-compose.yml # One-shot job
└── hyhome-spark.sh    # Writes spark-defaults.conf to tmpfs, exports the secret
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | Apache Spark (Scala 2.13, Java 21; version in `Dockerfile`) | Local mode, 2 CPUs, 2 GiB |
| **Table format** | Apache Iceberg (version in `Dockerfile`) | `iceberg-spark-runtime-4.1_2.13`, `iceberg-aws-bundle` |
| **Catalog** | SeaweedFS Iceberg REST | SigV4, catalog name `lakehouse` (default) |
| **Storage** | SeaweedFS S3 | `lakehouse` table bucket, path-style |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `SEAWEEDFS_ICEBERG_PORT` | No | REST catalog port on `seaweedfs-s3` (default: 8181). |

The secret is `seaweedfs_s3_lakehouse_secret_key` (STRG-015); the access key ID
is `lakehouse`.

## Available Scripts

Starting a job requires runtime approval.

| Command | Description |
| :--- | :--- |
| `docker compose --profile lakehouse config --services` | Confirm the selected services. |
| `docker compose --profile lakehouse run --rm spark` | List namespaces (read only). |

## Validation

- `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Troubleshooting

- Exit `64`: the `lakehouse` secret is missing or empty.
- `table bucket … not found` or `ForbiddenException`: follow the lakehouse runbook.

## Related Documents

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/guides/0094-lakehouse.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/policies/0094-lakehouse.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`)
- [Documentation index](../../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Spark job leaf in `04-data/lakehouse`; services: `spark`; unconditional root include, profile-selected, in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/lakehouse/spark/docker-compose.yml` |
| Config files | `Dockerfile`, `docker-compose.yml`, `hyhome-spark.sh` |
| Config values | profiles: `lakehouse` |
| Compose linkage | unconditional root include, profile-selected, in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/lakehouse/spark/docker-compose.yml` |
| Networks | `object_net` |
| Volumes | `./hyhome-spark.sh:/opt/hyhome/hyhome-spark.sh:ro` |
| Ports | Not published |
| Labels | `hy-home.tier` |
| Secret refs | `seaweedfs_s3_lakehouse_secret_key` |
| Healthcheck | Not declared (one-shot job) |
| Operations | Guide (`docs/05.operations/guides/0094-lakehouse.md`), Policy (`docs/05.operations/policies/0094-lakehouse.md`), Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Run the default command to prove catalog access, then follow the runbook. |

## How to Work in This Area

1. Iceberg 버전을 올릴 때는 Spark·Trino·Flink의 jar를 함께 올리고 checksum을 다시 계산한다.
2. Renovate는 `FROM` 이미지만 갱신하며 Iceberg jar는 수동 소유이다.
3. 테이블 삭제·snapshot 만료는 대상 table과 사유를 기록한 뒤에만 실행한다.

Runtime image authority is [Dockerfile](Dockerfile) and [docker-compose.yml](docker-compose.yml);
the [derived Compose image projection](../../../tech-stack.versions.json) is drift evidence.
