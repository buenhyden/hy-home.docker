---
title: "Trino (Iceberg)"
version: "1.0.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-trino] -->
# Trino (Iceberg)

> SeaweedFS REST catalog의 Iceberg table에 대한 on-demand OPTIONAL 단일 노드 SQL 엔진입니다.

## Overview

Trino는 `lakehouse` profile로 선택되는 **OPTIONAL** SQL engine입니다.
coordinator 한 개가 작업도 실행하며 catalog `lakehouse`는 Spark와 같은
SeaweedFS Iceberg REST catalog(`seaweedfs-s3:8181`)와 `lakehouse` S3 identity를
사용합니다. HTTP API에 인증이 없으므로 `127.0.0.1`에만 게시하고 route는 없습니다.

## Audience

이 README의 주요 독자:

- Data engineers
- Operators
- AI Agents

## Scope

### In Scope

- `lakehouse` Iceberg catalog을 갖춘 단일 노드 Trino.
- 환경 변수 기반 catalog 파일과 범위 S3 identity.

### Out of Scope

- Worker, TLS, 인증, Traefik route.
- 배치 유지보수([Spark](../spark/README.md))와 스트리밍([Flink](../flink/README.md)).

## Structure

```text
trino/
├── README.md                   # 이 파일
├── docker-compose.yml          # 단일 노드 서비스
├── hyhome-trino.sh             # secret을 export한 뒤 Trino를 시작함
└── catalog/
    └── lakehouse.properties    # Iceberg REST catalog(SigV4)와 native S3
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | Trino(버전은 `docker-compose.yml`) | 단일 노드, 2 CPU, 2 GiB, heap 80% |
| **Catalog** | SeaweedFS Iceberg REST | SigV4(`signing-name=s3`), view endpoint 꺼짐 |
| **Storage** | SeaweedFS S3 | Native S3 파일 시스템, path-style |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `TRINO_HOST_PORT` | No | HTTP API용 loopback 호스트 포트(기본값: 18090). |
| `SEAWEEDFS_ICEBERG_PORT` | No | `seaweedfs-s3`의 REST catalog 포트(기본값: 8181). |

Secret은 `seaweedfs_s3_lakehouse_secret_key`(STRG-015)이며 access key ID는
`lakehouse`입니다. catalog 파일은 둘 다 `${ENV:…}`를 통해 읽습니다.

## Available Scripts

서비스 시작에는 runtime 승인이 필요합니다.

| Command | Description |
| :--- | :--- |
| `docker compose --profile lakehouse up -d trino` | 엔진 시작(아무것도 쓰지 않음). |
| `docker compose exec trino trino --execute "SHOW SCHEMAS FROM lakehouse"` | catalog 접근 증명. |

## Validation

- `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests`

## Troubleshooting

- Exit `64`: `lakehouse` secret이 없거나 비어 있습니다.
- `Failed to list views`: `iceberg.rest-catalog.view-endpoints-enabled=false`가 누락되었습니다.
- `ForbiddenException`: lakehouse runbook을 따르십시오.

## Related Documents

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/guides/0094-lakehouse.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/policies/0094-lakehouse.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`)
- [문서 인덱스](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `12-analytics`의 Trino leaf; services: `trino`; [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/12-analytics/trino/docker-compose.yml` |
| Config files | `docker-compose.yml`, `hyhome-trino.sh`, `catalog/lakehouse.properties` |
| Config values | profiles: `lakehouse` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/12-analytics/trino/docker-compose.yml` |
| Networks | `object_net` |
| Volumes | `./hyhome-trino.sh:/opt/hyhome/hyhome-trino.sh:ro`, `./catalog/lakehouse.properties:/etc/trino/catalog/lakehouse.properties:ro` |
| Ports | `127.0.0.1:${TRINO_HOST_PORT:-18090}:8080` |
| Labels | `hy-home.tier` |
| Secret refs | `seaweedfs_s3_lakehouse_secret_key` |
| Healthcheck | `/usr/lib/trino/bin/health-check` |
| Operations | Guide (`docs/05.operations/guides/0094-lakehouse.md`), Policy (`docs/05.operations/policies/0094-lakehouse.md`), Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `SHOW SCHEMAS FROM lakehouse`를 실행한 뒤 runbook을 따름 |

## Usage

1. Trino는 자체 Iceberg 라이브러리를 포함합니다. 둘 중 하나를 업그레이드한 뒤에는 Spark가 쓴 table을 읽는지 확인하십시오.
2. Renovate가 이미지 tag를 갱신합니다.
3. Table 삭제와 snapshot 만료는 named table과 기록된 사유가 있을 때만 실행합니다.

런타임 이미지 권한은 [docker-compose.yml](docker-compose.yml)이 소유하며
[derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift 증거입니다.
