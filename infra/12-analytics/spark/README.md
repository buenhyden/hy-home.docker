---
title: "Spark (Iceberg)"
version: "1.0.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-spark] -->
# Spark (Iceberg)

> SeaweedFS REST catalog의 Iceberg table에 대한 on-demand OPTIONAL 배치/table 유지보수 job입니다.

## Overview

Spark는 `lakehouse` profile로 선택되는 **OPTIONAL** one-shot 작업입니다.
SeaweedFS 내장 Iceberg REST catalog(`seaweedfs-s3:8181`)와 `lakehouse` table
bucket을 `lakehouse` S3 identity로 사용합니다. 기본 명령은 namespace 조회만
수행하며 쓰기는 명시적 `docker compose run --rm spark ...`로만 실행합니다.

## Audience

이 README의 주요 독자:

- Data engineers
- Operators
- AI Agents

## Scope

### In Scope

- 고정된 Iceberg runtime과 AWS bundle을 갖춘 Spark local-mode job 이미지.
- 시작 시 생성되는 catalog 설정과 범위 S3 identity.

### Out of Scope

- Spark cluster(master/worker), Spark UI, history 서버.
- 대화형 SQL 서비스([Trino](../trino/README.md))와 스트리밍([Flink](../flink/README.md)).

## Structure

```text
spark/
├── README.md          # 이 파일
├── Dockerfile         # apache/spark와 checksum-pinned Iceberg jar
├── docker-compose.yml # one-shot job
└── hyhome-spark.sh    # spark-defaults.conf를 tmpfs에 쓰고 secret을 export함
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | Apache Spark(Scala 2.13, Java 21; 버전은 `Dockerfile`) | Local mode, 2 CPU, 2 GiB |
| **Table format** | Apache Iceberg(버전은 `Dockerfile`) | `iceberg-spark-runtime-4.1_2.13`, `iceberg-aws-bundle` |
| **Catalog** | SeaweedFS Iceberg REST | SigV4, catalog 이름 `lakehouse`(기본값) |
| **Storage** | SeaweedFS S3 | `lakehouse` table bucket, path-style |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `SEAWEEDFS_ICEBERG_PORT` | No | `seaweedfs-s3`의 REST catalog 포트(기본값: 8181). |

Secret은 `seaweedfs_s3_lakehouse_secret_key`(STRG-015)이며 access key ID는
`lakehouse`입니다.

## Available Scripts

job 시작에는 runtime 승인이 필요합니다.

| Command | Description |
| :--- | :--- |
| `docker compose --profile lakehouse config --services` | 선택된 서비스 확인. |
| `docker compose --profile lakehouse run --rm spark` | namespace 목록(읽기 전용). |

## Validation

- `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Troubleshooting

- Exit `64`: `lakehouse` secret이 없거나 비어 있습니다.
- `table bucket … not found` 또는 `ForbiddenException`: lakehouse runbook을 따르십시오.

## Related Documents

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/guides/0094-lakehouse.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/policies/0094-lakehouse.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`)
- [문서 인덱스](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `12-analytics`의 Spark job leaf; services: `spark`; [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/12-analytics/spark/docker-compose.yml` |
| Config files | `Dockerfile`, `docker-compose.yml`, `hyhome-spark.sh` |
| Config values | profiles: `lakehouse` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/12-analytics/spark/docker-compose.yml` |
| Networks | `object_net` |
| Volumes | `./hyhome-spark.sh:/opt/hyhome/hyhome-spark.sh:ro` |
| Ports | 게시되지 않음 |
| Labels | `hy-home.tier` |
| Secret refs | `seaweedfs_s3_lakehouse_secret_key` |
| Healthcheck | 선언되지 않음(one-shot job) |
| Operations | Guide (`docs/05.operations/guides/0094-lakehouse.md`), Policy (`docs/05.operations/policies/0094-lakehouse.md`), Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | catalog 접근을 증명하기 위해 기본 명령을 실행한 뒤 runbook을 따름 |

## Usage

1. Iceberg 버전을 올릴 때는 Spark·Trino·Flink의 jar를 함께 올리고 checksum을 다시 계산한다.
2. Renovate는 `FROM` 이미지만 갱신하며 Iceberg jar는 수동 소유이다.
3. 테이블 삭제·snapshot 만료는 대상 table과 사유를 기록한 뒤에만 실행한다.

런타임 이미지 권한은 [Dockerfile](Dockerfile)과 [docker-compose.yml](docker-compose.yml)이 소유하며
[derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift 증거입니다.
