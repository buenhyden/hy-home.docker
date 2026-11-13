---
title: "Spark (Iceberg)"
version: "1.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-spark] -->

# Spark (Iceberg)

> 승인된 Iceberg REST catalog의 table에 대한 lakehouse LAB의 on-demand 배치/table 유지보수 job입니다.

## Purpose

### Service Role

Spark는 독립 Compose project인 [lakehouse LAB](../docker-compose.yml)
(`lab-lakehouse` profile)의 one-shot 작업입니다. root Compose에 포함되지 않고
HOME network에 연결되지 않으며 Traefik route도 없습니다. catalog와 S3는 필수
LAB 입력 `LAB_LAKEHOUSE_CATALOG_URI`, `LAB_LAKEHOUSE_S3_ENDPOINT`로 지정하고
`lakehouse` S3 identity를 사용합니다. HOME은 SeaweedFS를 LAB network에 게시하지
않으므로 owner가 도달 가능한 endpoint를 승인하기 전(미결정)까지는 render 검증만
합니다. 기본 명령은 namespace 조회만 수행하며 쓰기는 명시적 `run --rm spark ...`로만
실행합니다.

#### Audience

이 README의 주요 독자:

- Data engineers
- Operators

#### In Scope

- 고정된 Iceberg runtime과 AWS bundle을 갖춘 Spark local-mode job 이미지.
- 시작 시 생성되는 catalog 설정과 범위 S3 identity.

#### Out of Scope

- Spark cluster(master/worker), Spark UI, history 서버.
- 대화형 SQL 서비스([Trino](../trino/README.md))와 스트리밍([Flink](../flink/README.md)).

#### Structure

```text
spark/
├── README.md          # 이 파일
├── Dockerfile         # apache/spark와 checksum-pinned Iceberg jar
└── hyhome-spark.sh    # spark-defaults.conf를 tmpfs에 쓰고 secret을 export함
```

서비스 정의는 [labs/lakehouse/docker-compose.yml](../docker-compose.yml)이 소유합니다.

### Supported Environment

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | Apache Spark(Scala 2.13, Java 21; 버전은 `Dockerfile`) | Local mode, 2 CPU, 2 GiB |
| **Table format** | Apache Iceberg(버전은 `Dockerfile`) | `iceberg-spark-runtime-4.1_2.13`, `iceberg-aws-bundle` |
| **Catalog** | Iceberg REST(`LAB_LAKEHOUSE_CATALOG_URI`) | SigV4, catalog 이름 `lakehouse`(기본값) |
| **Storage** | S3(`LAB_LAKEHOUSE_S3_ENDPOINT`) | `lakehouse` table bucket, path-style |

## Interfaces

### Inputs and Outputs

입력은 `LAB_LAKEHOUSE_CATALOG_URI`, `LAB_LAKEHOUSE_S3_ENDPOINT` 환경 변수가 가리키는 승인된 Iceberg REST catalog와 S3 endpoint이며 출력은 `spark-sql` 질의 결과이다. 환경 변수는 아래 표와 같다.

#### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `LAB_LAKEHOUSE_CATALOG_URI` | Yes | 승인된 Iceberg REST catalog endpoint. 비어 있으면 render가 거부됩니다. |
| `LAB_LAKEHOUSE_S3_ENDPOINT` | Yes | 승인된 S3 endpoint. 비어 있으면 render가 거부됩니다. |
| `LAB_SECRETS_GID` | No | LAB secret 파일을 읽는 group(기본값: 1000). |

Secret은 `${LAB_SECRET_DIR}/lakehouse/s3_lakehouse_secret_key.txt`의 LAB 전용
`lab_lakehouse_s3_lakehouse_secret_key`이며 원래 이름
`/run/secrets/seaweedfs_s3_lakehouse_secret_key`로 마운트됩니다. access key ID는
`lakehouse`입니다. HOME 값을 복사하려면 별도 승인이 필요합니다.

### Security Boundary

`lab_lakehouse_net`만 사용하고 호스트 포트를 게시하지 않으며 HOME network에 연결되지 않는다. secret은 `lab_lakehouse_s3_lakehouse_secret_key`(-> `seaweedfs_s3_lakehouse_secret_key`)만 사용하고 값은 문서에 쓰지 않는다.

## Development

### Local Workflow

아래 `LAB`은 저장소 루트에서
`docker compose --env-file labs/.env -f labs/lakehouse/docker-compose.yml --profile lab-lakehouse`입니다.
`config`는 render만 합니다. 컨테이너를 시작하는 명령은
`python3 scripts/operations/lab.py check|up|down lakehouse`의 lease 규칙
([LAB 안내](../../README.md#local-workflow))을 따릅니다.

| Command | Description |
| :--- | :--- |
| `LAB config --services` | 선택된 서비스 확인(render-only). |
| `LAB run --rm spark` | namespace 목록(읽기 전용, table-bucket job이 먼저 실행됨). |
| `LAB run --rm --no-deps spark /opt/spark/bin/spark-sql -S -e "SHOW TABLES IN dev"` | provisioning이 끝난 뒤 읽기 전용 조회. |

#### Usage

1. Iceberg 버전을 올릴 때는 Spark·Trino·Flink의 jar를 함께 올리고 checksum을 다시 계산한다.
2. Renovate는 `FROM` 이미지만 갱신하며 Iceberg jar는 수동 소유이다.
3. 테이블 삭제·snapshot 만료는 대상 table과 사유를 기록한 뒤에만 실행한다.

런타임 이미지 권한은 [Dockerfile](Dockerfile)과 [labs/lakehouse/docker-compose.yml](../docker-compose.yml)이 소유하며
[derived Compose 이미지 투영](../../../infra/tech-stack.versions.json)은 drift 증거입니다.

### Checks

- `docker compose --env-file labs/.env -f labs/lakehouse/docker-compose.yml --profile lab-lakehouse config --quiet`
- `python3 -m unittest tests.validation.test_lab_isolation`

## Operations

### Runbook Links

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/guides/15-labs/0094-lakehouse.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/policies/15-labs/0094-lakehouse.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/runbooks/15-labs/0094-lakehouse.md`)
- [LAB 탐색](../../README.md)
- [문서 인덱스](../../../docs/README.md)

### Observability and Recovery

- Exit `64`: `lakehouse` secret이 없거나 비어 있습니다.
- `table bucket … not found` 또는 `ForbiddenException`: lakehouse runbook을 따르십시오.

#### Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | lakehouse LAB의 Spark job leaf; services: `spark` |
| Config files | `Dockerfile`, `hyhome-spark.sh` |
| Config values | profiles: `lab-lakehouse` |
| Compose linkage | 독립 Compose project `hy-home-lab-lakehouse`([labs/lakehouse/docker-compose.yml](../docker-compose.yml)); root include 없음 |
| Networks | `lab_lakehouse_net`(`hy-home-lab-lakehouse`); HOME network 없음 |
| Volumes | `./lakehouse/spark/hyhome-spark.sh:/opt/hyhome/hyhome-spark.sh:ro` |
| Ports | 게시되지 않음 |
| Labels | `hy-home.tier: lab`, `traefik.enable: 'false'` |
| Secret refs | `lab_lakehouse_s3_lakehouse_secret_key` -> `seaweedfs_s3_lakehouse_secret_key` |
| Healthcheck | 선언되지 않음(one-shot job) |
| Operations | Guide (`docs/05.operations/guides/15-labs/0094-lakehouse.md`), Policy (`docs/05.operations/policies/15-labs/0094-lakehouse.md`), Runbook (`docs/05.operations/runbooks/15-labs/0094-lakehouse.md`) |
| Validation | `config --quiet` render, `tests.validation.test_lab_isolation` |
| Troubleshooting | 활성 lease 안에서 기본 명령으로 catalog 접근을 확인한 뒤 runbook을 따름 |
