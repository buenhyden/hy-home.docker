---
title: "Trino (Iceberg)"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-05"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-trino] -->
# Trino (Iceberg)

> 승인된 Iceberg REST catalog의 table에 대한 lakehouse LAB의 on-demand 단일 노드 SQL 엔진입니다.

## Overview

Trino는 독립 Compose project인 [lakehouse LAB](../docker-compose.yml)
(`lab-lakehouse` profile)의 SQL engine입니다. coordinator 한 개가 작업도 실행하며
catalog `lakehouse`는 Spark와 같은 `LAB_LAKEHOUSE_CATALOG_URI` catalog와 `lakehouse`
S3 identity를 사용합니다. HOME network에 연결되지 않고, HTTP API에 인증이 없으므로
`127.0.0.1`에만 게시하며 Traefik route는 없습니다. HOME은 SeaweedFS를 LAB network에
게시하지 않으므로 owner가 endpoint를 승인하기 전(미결정)까지는 render 검증만 합니다.

## Audience

이 README의 주요 독자:

- Data engineers
- Operators

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
├── hyhome-trino.sh             # secret을 export한 뒤 Trino를 시작함
└── catalog/
    └── lakehouse.properties    # Iceberg REST catalog(SigV4)와 native S3
```

서비스 정의는 [labs/lakehouse/docker-compose.yml](../docker-compose.yml)이 소유합니다.

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | Trino(버전은 `labs/lakehouse/docker-compose.yml`) | 단일 노드, 2 CPU, 2 GiB, heap 80% |
| **Catalog** | Iceberg REST(`LAB_LAKEHOUSE_CATALOG_URI`) | SigV4(`signing-name=s3`), view endpoint 꺼짐 |
| **Storage** | S3(`LAB_LAKEHOUSE_S3_ENDPOINT`) | Native S3 파일 시스템, path-style |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `LAB_TRINO_HOST_PORT` | No | HTTP API용 loopback 호스트 포트(기본값: 18090). |
| `LAB_LAKEHOUSE_CATALOG_URI` | Yes | 승인된 Iceberg REST catalog endpoint. |
| `LAB_LAKEHOUSE_S3_ENDPOINT` | Yes | 승인된 S3 endpoint. |

Secret은 `${LAB_SECRET_DIR}/lakehouse/s3_lakehouse_secret_key.txt`의 LAB 전용
`lab_lakehouse_s3_lakehouse_secret_key`이며
`/run/secrets/seaweedfs_s3_lakehouse_secret_key`로 마운트됩니다. access key ID는
`lakehouse`입니다. catalog 파일은 둘 다 `${ENV:…}`를 통해 읽습니다. HOME 값을
복사하려면 별도 승인이 필요합니다.

## Available Scripts

아래 `LAB`은 저장소 루트에서
`docker compose --env-file labs/.env -f labs/lakehouse/docker-compose.yml --profile lab-lakehouse`입니다.
`config`는 render만 합니다. 컨테이너를 시작하는 명령은
`python3 scripts/operations/lab.py check|up|down lakehouse`의 lease 규칙
([LAB 안내](../../README.md#usage))을 따릅니다.

| Command | Description |
| :--- | :--- |
| `LAB up -d trino` | 엔진 시작; dependency table-bucket provisioning 가능. |
| `LAB exec trino trino --execute "SHOW SCHEMAS FROM lakehouse"` | catalog 접근 증명. |

2026-10-26에는 장부의 공식 후보 이미지와 공식 launcher 명령으로 소스를
준비했습니다. 기존 secret wrapper, catalog, 환경 변수 참조와 S3 속성 alias를
유지하며 read-only template·loopback·identity 경계도 바꾸지 않습니다.
새 이미지 실행, SQL/JSON 의미, Iceberg/SigV4 질의, 인증과 상태 복구는
`NOT_RUN`입니다. 소스 복구는 이전 pin과 명령을 함께 되돌리는 변경이며,
운영 데이터 복구나 실제 질의 호환성까지 검증한 것으로 해석하지 않습니다.

## Validation

- `docker compose --env-file labs/.env -f labs/lakehouse/docker-compose.yml --profile lab-lakehouse config --quiet`
- `python3 -m unittest tests.validation.test_lab_isolation`

## Troubleshooting

- Exit `64`: `lakehouse` secret이 없거나 비어 있습니다.
- `Failed to list views`: `iceberg.rest-catalog.view-endpoints-enabled=false`가 누락되었습니다.
- `ForbiddenException`: lakehouse runbook을 따르십시오.

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | lakehouse LAB의 Trino leaf; services: `trino` |
| Config files | `hyhome-trino.sh`, `catalog/lakehouse.properties` |
| Config values | profiles: `lab-lakehouse` |
| Compose linkage | 독립 Compose project `hy-home-lab-lakehouse`([labs/lakehouse/docker-compose.yml](../docker-compose.yml)); root include 없음 |
| Networks | `lab_lakehouse_net`(`hy-home-lab-lakehouse`); HOME network 없음 |
| Volumes | `./lakehouse/trino/hyhome-trino.sh:/opt/hyhome/hyhome-trino.sh:ro`, `./lakehouse/trino/catalog/lakehouse.properties:/etc/trino/catalog/lakehouse.properties:ro` |
| Ports | `127.0.0.1:${LAB_TRINO_HOST_PORT:-18090}:8080` |
| Labels | `hy-home.tier: lab`, `traefik.enable: 'false'` |
| Secret refs | `lab_lakehouse_s3_lakehouse_secret_key` -> `seaweedfs_s3_lakehouse_secret_key` |
| Healthcheck | `/usr/lib/trino/bin/health-check` |
| Operations | Guide (`docs/05.operations/guides/15-labs/0094-lakehouse.md`), Policy (`docs/05.operations/policies/15-labs/0094-lakehouse.md`), Runbook (`docs/05.operations/runbooks/15-labs/0094-lakehouse.md`) |
| Validation | `config --quiet` render, `tests.validation.test_lab_isolation` |
| Troubleshooting | 활성 lease 안에서 `SHOW SCHEMAS FROM lakehouse`를 실행한 뒤 runbook을 따름 |

## Usage

1. Trino는 자체 Iceberg 라이브러리를 포함합니다. 둘 중 하나를 업그레이드한 뒤에는 Spark가 쓴 table을 읽는지 확인하십시오.
2. Renovate가 이미지 tag를 갱신합니다.
3. Table 삭제와 snapshot 만료는 named table과 기록된 사유가 있을 때만 실행합니다.

런타임 이미지 권한은 [labs/lakehouse/docker-compose.yml](../docker-compose.yml)이 소유하며
[derived Compose 이미지 투영](../../../infra/tech-stack.versions.json)은 drift 증거입니다.

## Related Documents

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/guides/15-labs/0094-lakehouse.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/policies/15-labs/0094-lakehouse.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/runbooks/15-labs/0094-lakehouse.md`)
- [LAB 탐색](../../README.md)
- [문서 인덱스](../../../docs/README.md)

---
