---
title: "Lakehouse LAB"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-11-05"
---

# Lakehouse LAB

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Service

##### Purpose

이 폴더는 root Compose에서 분리된 lakehouse LAB의 진입점과 엔진별 build·설정
source를 보관한다. Spark·Trino·Flink·Great Expectations가 HOME SeaweedFS의
Iceberg REST 카탈로그를 같이 쓰며, LAB은 HOME network에 연결하지 않고
`LAB_LAKEHOUSE_*` endpoint 입력으로만 대상을 지정한다(SPEC-0262).

###### Audience
<!-- core-payload-level:4 -->

- 데이터 엔지니어: 엔진별 source와 LAB 진입점을 찾는다.
- 운영자: LAB 경계, 자원, 승격 계획을 확인한다.
- Agent: 엔진 README와 운영 문서로 가는 경로를 추적한다.

###### In Scope
<!-- core-payload-level:4 -->

- `hy-home-lab-lakehouse` project의 Compose 진입점과 승격 manifest
- 엔진별 build source, wrapper, 카탈로그 설정, GX suite

###### Out of Scope
<!-- core-payload-level:4 -->

- HOME SeaweedFS·카탈로그 기동과 그 데이터
- 실제 실행, 데이터 적재·삭제, secret 값

###### Structure
<!-- core-payload-level:4 -->

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

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `LAB_LAKEHOUSE_S3_ENDPOINT` | HOME SeaweedFS(승인된 S3 endpoint) | lakehouse LAB 엔진 | LAB은 HOME network에 연결하지 않고 이 endpoint 입력으로만 대상을 지정한다. | 복구는 RUN-0094 lakehouse 런북을 따른다. |
| `LAB_LAKEHOUSE_CATALOG_URI` | HOME SeaweedFS의 Iceberg REST 카탈로그 | Spark, Trino, Flink, Great Expectations | 승인된 Iceberg REST 카탈로그 endpoint를 입력으로 받는다. | 복구는 RUN-0094 lakehouse 런북을 따른다. |
| loopback `LAB_TRINO_HOST_PORT` | `trino` | 이 README는 소비자를 기록하지 않는다. | 대화형 SQL용 loopback 호스트 노출이다. | 이 README는 실패 처리를 기록하지 않는다. |
| loopback `LAB_FLINK_HOST_PORT` | `flink-jobmanager` | 이 README는 소비자를 기록하지 않는다. | 스트리밍용 loopback 호스트 노출이다. | 이 README는 실패 처리를 기록하지 않는다. |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

| Variable | Required | Description |
| --- | ---: | --- |
| `LAB_DATA_DIR` | Yes | 격리된 LAB 상태 root |
| `LAB_LAKEHOUSE_S3_ENDPOINT` | Yes | 승인된 SeaweedFS S3 endpoint |
| `LAB_LAKEHOUSE_CATALOG_URI` | Yes | 승인된 Iceberg REST 카탈로그 endpoint |

###### Security Boundary
<!-- core-payload-level:4 -->

LAB은 HOME network에 연결되지 않으며 secret은 `LAB_SECRET_DIR` 아래 `lakehouse/s3_admin_secret_key.txt`(Compose secret `lab_lakehouse_s3_admin_secret_key`), `lakehouse/s3_lakehouse_secret_key.txt`(Compose secret `lab_lakehouse_s3_lakehouse_secret_key`) 파일로만 참조하고 값은 문서에 쓰지 않는다. 호스트 노출은 loopback `LAB_TRINO_HOST_PORT`, `LAB_FLINK_HOST_PORT`뿐이다.

#### Usage

##### Prerequisites

| Category | Source of truth | Boundary |
| --- | --- | --- |
| Compose | [docker-compose.yml](docker-compose.yml) | 독립 LAB project `hy-home-lab-lakehouse`, profile `lab-lakehouse` |
| Spark | [spark/README.md](spark/README.md) | 배치·테이블 유지보수 |
| Trino | [trino/README.md](trino/README.md) | 대화형 SQL, host port `LAB_TRINO_HOST_PORT` |
| Flink | [flink/README.md](flink/README.md) | 스트리밍, host port `LAB_FLINK_HOST_PORT` |
| Great Expectations | [great-expectations/README.md](great-expectations/README.md) | Trino 경유 품질 검사 |

##### Selected Start

기동은 `python3 scripts/operations/lab.py up lakehouse --purpose "<목적>" --lease <기간>`으로만
한다. 엔진별 명령과 부작용은 각 엔진 README와 운영 문서를 따른다.

#### Checks

##### Readiness

```bash
LAB_DATA_DIR=/tmp/hyhome-lakehouse-static \
LAB_LAKEHOUSE_S3_ENDPOINT=http://lab-endpoint.invalid:8333 \
LAB_LAKEHOUSE_CATALOG_URI=http://lab-endpoint.invalid:8181 \
docker compose --env-file labs/.env.example -f labs/lakehouse/docker-compose.yml \
  --profile lab-lakehouse config --quiet
```

정적 render는 컨테이너를 만들지 않으며 실행·카탈로그 연결의 증거가 아니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [LAB 탐색](../README.md)
- [운영 문서 색인](../../docs/05.operations/README.md) — `GDE-0094`, `POL-0094`, `RUN-0094`
- [15-labs runbooks](../../docs/05.operations/03.runbooks/15.labs/README.md): RUN-0094 lakehouse, RUN-0107 lab-promotion

###### Observability and Recovery
<!-- core-payload-level:4 -->

| Field | Evidence |
| --- | --- |
| Entry point | [docker-compose.yml](docker-compose.yml) |
| Project | `hy-home-lab-lakehouse` |
| Services | `seaweedfs-table-bucket`, `spark`, `trino`, `great-expectations`, `flink-jobmanager`, `flink-taskmanager` |
| Secret refs | `LAB_SECRET_DIR` 아래 `lakehouse/s3_admin_secret_key.txt`(Compose secret `lab_lakehouse_s3_admin_secret_key`), `lakehouse/s3_lakehouse_secret_key.txt`(Compose secret `lab_lakehouse_s3_lakehouse_secret_key`) |
| Host exposure | loopback `LAB_TRINO_HOST_PORT`, `LAB_FLINK_HOST_PORT` |
| Promotion | [promotion.yaml](promotion.yaml); 대상 미정(`undecided`) |

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
