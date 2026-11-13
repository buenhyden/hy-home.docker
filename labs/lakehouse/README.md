---
title: "Lakehouse LAB"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2026-11-05"
---

# Lakehouse LAB

## Purpose

### Service Role

이 폴더는 root Compose에서 분리된 lakehouse LAB의 진입점과 엔진별 build·설정
source를 보관한다. Spark·Trino·Flink·Great Expectations가 HOME SeaweedFS의
Iceberg REST 카탈로그를 같이 쓰며, LAB은 HOME network에 연결하지 않고
`LAB_LAKEHOUSE_*` endpoint 입력으로만 대상을 지정한다(SPEC-0262).

#### Audience

- 데이터 엔지니어: 엔진별 source와 LAB 진입점을 찾는다.
- 운영자: LAB 경계, 자원, 승격 계획을 확인한다.
- Agent: 엔진 README와 운영 문서로 가는 경로를 추적한다.

#### In Scope

- `hy-home-lab-lakehouse` project의 Compose 진입점과 승격 manifest
- 엔진별 build source, wrapper, 카탈로그 설정, GX suite

#### Out of Scope

- HOME SeaweedFS·카탈로그 기동과 그 데이터
- 실제 실행, 데이터 적재·삭제, secret 값

#### Structure

```text
labs/lakehouse/
├── docker-compose.yml         # 독립 LAB entrypoint
├── promotion.yaml             # SPEC-0263 승격 manifest
├── README.md                  # 서비스 README
├── seaweedfs-table-bucket.sh  # 테이블 버킷 준비 job
├── flink/                     # Flink build·wrapper
├── great-expectations/        # GX build·suite
├── spark/                     # Spark build·wrapper
└── trino/                     # Trino wrapper·카탈로그
```

### Supported Environment

| Category | Source of truth | Boundary |
| --- | --- | --- |
| Compose | [docker-compose.yml](docker-compose.yml) | 독립 LAB project `hy-home-lab-lakehouse`, profile `lab-lakehouse` |
| Spark | [spark/README.md](spark/README.md) | 배치·테이블 유지보수 |
| Trino | [trino/README.md](trino/README.md) | 대화형 SQL, host port `LAB_TRINO_HOST_PORT` |
| Flink | [flink/README.md](flink/README.md) | 스트리밍, host port `LAB_FLINK_HOST_PORT` |
| Great Expectations | [great-expectations/README.md](great-expectations/README.md) | Trino 경유 품질 검사 |

## Interfaces

### Inputs and Outputs

| Variable | Required | Description |
| --- | ---: | --- |
| `LAB_DATA_DIR` | Yes | 격리된 LAB 상태 root |
| `LAB_LAKEHOUSE_S3_ENDPOINT` | Yes | 승인된 SeaweedFS S3 endpoint |
| `LAB_LAKEHOUSE_CATALOG_URI` | Yes | 승인된 Iceberg REST 카탈로그 endpoint |

### Security Boundary

LAB은 HOME network에 연결되지 않으며 secret은 `LAB_SECRET_DIR` 아래 `lakehouse/s3_admin_secret_key.txt`, `lakehouse/s3_lakehouse_secret_key.txt` 파일로만 참조하고 값은 문서에 쓰지 않는다. 호스트 노출은 loopback `LAB_TRINO_HOST_PORT`, `LAB_FLINK_HOST_PORT`뿐이다.

## Development

### Local Workflow

기동은 `python3 scripts/operations/lab.py up lakehouse --purpose "<목적>" --lease <기간>`으로만
한다. 엔진별 명령과 부작용은 각 엔진 README와 운영 문서를 따른다.

### Checks

```bash
LAB_DATA_DIR=/tmp/hyhome-lakehouse-static \
LAB_LAKEHOUSE_S3_ENDPOINT=http://lab-endpoint.invalid:8333 \
LAB_LAKEHOUSE_CATALOG_URI=http://lab-endpoint.invalid:8181 \
docker compose --env-file labs/.env.example -f labs/lakehouse/docker-compose.yml \
  --profile lab-lakehouse config --quiet
```

정적 render는 컨테이너를 만들지 않으며 실행·카탈로그 연결의 증거가 아니다.

## Operations

### Runbook Links

- [LAB 탐색](../README.md)
- [운영 문서 색인](../../docs/05.operations/README.md) — `GDE-0094`, `POL-0094`, `RUN-0094`

### Observability and Recovery

| Field | Evidence |
| --- | --- |
| Entry point | [docker-compose.yml](docker-compose.yml) |
| Project | `hy-home-lab-lakehouse` |
| Services | `seaweedfs-table-bucket`, `spark`, `trino`, `great-expectations`, `flink-jobmanager`, `flink-taskmanager` |
| Secret refs | `LAB_SECRET_DIR` 아래 `lakehouse/s3_admin_secret_key.txt`, `lakehouse/s3_lakehouse_secret_key.txt` |
| Host exposure | loopback `LAB_TRINO_HOST_PORT`, `LAB_FLINK_HOST_PORT` |
| Promotion | [promotion.yaml](promotion.yaml); 대상 미정(`undecided`) |
