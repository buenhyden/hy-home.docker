---
title: "Flink (Iceberg)"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-04"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-flink] -->
# Flink (Iceberg)

> 승인된 Iceberg REST catalog의 table에 스트리밍/배치 SQL을 쓰는 lakehouse LAB의 on-demand Flink session cluster입니다.

## Overview

Flink는 독립 Compose project인 [lakehouse LAB](../../lakehouse.yml)
(`lab-lakehouse` profile)의 stream processing engine입니다. JobManager 하나와
TaskManager 하나(slot 2개)로 된 session cluster이며 catalog `lakehouse`는 Spark·Trino와
같은 `LAB_LAKEHOUSE_CATALOG_URI` catalog와 `lakehouse` S3 identity를 사용합니다.
HOME network에 연결되지 않으므로 HOME Kafka는 이 network에 없습니다. Kafka
source/sink는 승인된 Kafka endpoint가 있을 때만 씁니다. REST API와 UI에 인증이
없으므로 `127.0.0.1`에만 게시하고 Traefik route는 없습니다. REST API로 JAR를 올릴
수도 없습니다. HOME은 SeaweedFS를 LAB network에 게시하지 않으므로 owner가 endpoint를
승인하기 전(미결정)까지는 render 검증만 합니다.

## Audience

이 README의 주요 독자:

- Data engineers
- Operators

## Scope

### In Scope

- Iceberg, AWS, Kafka, Hadoop client jar를 포함한 session cluster(JobManager, TaskManager).
- `lakehouse` catalog statement, 범위 S3 identity, file checkpoint.

### Out of Scope

- 고가용성, TLS, 인증, Traefik route.
- Application mode와 REST API를 통한 JAR 제출.
- 배치 유지보수([Spark](../spark/README.md))와 대화형 SQL([Trino](../trino/README.md)).

## Structure

```text
flink/
├── README.md           # 이 파일
├── Dockerfile          # flink base와 checksum-pinned jar
└── hyhome-flink.sh     # secret을 export하고 /tmp/lakehouse.sql을 작성한 뒤 명령을 실행함
```

서비스 정의(`flink-jobmanager`, `flink-taskmanager`)는 [labs/lakehouse.yml](../../lakehouse.yml)이 소유합니다.

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | Apache Flink(`Dockerfile`의 base image) | JobManager 1 CPU / 1.25 GiB, TaskManager 2 CPU / 2 GiB, slot 2개 |
| **Table format** | Iceberg Flink runtime | Spark와 동일한 Iceberg 버전; SigV4 REST catalog, S3FileIO |
| **Streaming source** | Kafka SQL connector | 승인된 Kafka endpoint 필요; HOME Kafka는 LAB network에 없음 |
| **State** | File checkpoint | `${LAB_DATA_DIR}/lakehouse/flink/checkpoints`, 두 컨테이너가 공유 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `LAB_FLINK_HOST_PORT` | No | REST API/UI용 loopback 호스트 포트(기본값: 18091). |
| `LAB_LAKEHOUSE_CATALOG_URI` | Yes | 승인된 Iceberg REST catalog endpoint. |
| `LAB_LAKEHOUSE_S3_ENDPOINT` | Yes | 승인된 S3 endpoint. |
| `LAB_DATA_DIR` | Yes | 격리된 LAB data root; checkpoint 디렉터리의 상위 경로. |

Secret은 `${LAB_SECRET_DIR}/lakehouse/s3_lakehouse_secret_key.txt`의 LAB 전용
`lab_lakehouse_s3_lakehouse_secret_key`이며
`/run/secrets/seaweedfs_s3_lakehouse_secret_key`로 마운트됩니다. access key ID는
`lakehouse`입니다. HOME 값을 복사하려면 별도 승인이 필요합니다. Flink 설정은
Compose의 `-D` 인자로 지정하며 이미지 설정 파일은 수정하지 않습니다.

## Available Scripts

아래 `LAB`은 저장소 루트에서
`docker compose --env-file labs/.env -f labs/lakehouse.yml --profile lab-lakehouse`입니다.
`config`는 render만 합니다. 컨테이너를 시작하는 명령은
`python3 scripts/operations/lab.py check|up|down lakehouse`의 lease 규칙
([LAB 안내](../../README.md#usage))을 따릅니다. 먼저 checkpoint 디렉터리를
생성하십시오: `install -d -m 2770 -g "${LAB_SECRETS_GID:-1000}" "$LAB_DATA_DIR/lakehouse/flink/checkpoints"`.

| Command | Description |
| :--- | :--- |
| `LAB up -d flink-jobmanager flink-taskmanager` | session cluster 시작; dependency table-bucket provisioning 가능. |
| `LAB exec flink-jobmanager bash /opt/hyhome/hyhome-flink.sh /opt/flink/bin/sql-client.sh -i /tmp/lakehouse.sql` | `lakehouse` catalog에 대한 SQL client. |
| `LAB exec flink-jobmanager /opt/flink/bin/flink list -a` | job 목록. |
| `LAB exec flink-jobmanager /opt/flink/bin/flink cancel <job_id>` | job 중지. |

## Validation

- `docker compose --env-file labs/.env -f labs/lakehouse.yml --profile lab-lakehouse config --quiet`
- `python3 -m unittest tests.validation.test_lab_isolation`

## Troubleshooting

- Exit `64`: `lakehouse` secret이 없거나 비어 있습니다.
- `ClassNotFoundException: org.apache.hadoop.conf.Configuration`: 이미지에 Hadoop client jar가 없습니다.
- SQL client에서 `lakehouse` catalog가 없거나 S3 `403`이 발생: wrapper 없이 시작되었습니다. 위와 같이 `hyhome-flink.sh`로 실행하십시오.
- 스트리밍 `INSERT`가 커밋되지 않음: checkpointing이 꺼져 있습니다. wrapper는 60초 간격을 설정하며 세션 `SET`으로 이를 끄면 안 됩니다.
- Checkpoint `AccessDeniedException`: 호스트 checkpoint 디렉터리가 group-writable이 아닙니다. lakehouse runbook을 따르십시오.

## Related Documents

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/guides/15-labs/0094-lakehouse.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/policies/15-labs/0094-lakehouse.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/runbooks/15-labs/0094-lakehouse.md`)
- [LAB 탐색](../../README.md)
- [문서 인덱스](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | lakehouse LAB의 Flink leaf; services: `flink-jobmanager`, `flink-taskmanager` |
| Config files | `Dockerfile`, `hyhome-flink.sh` |
| Config values | profiles: `lab-lakehouse` |
| Compose linkage | 독립 Compose project `hy-home-lab-lakehouse`([labs/lakehouse.yml](../../lakehouse.yml)); root include 없음 |
| Networks | `lab_lakehouse_net`(`hy-home-lab-lakehouse`); HOME network 없음 |
| Volumes | `./lakehouse/flink/hyhome-flink.sh:/opt/hyhome/hyhome-flink.sh:ro`, `flink-checkpoints:/opt/flink/checkpoints`(`${LAB_DATA_DIR}/lakehouse/flink/checkpoints`) |
| Ports | `127.0.0.1:${LAB_FLINK_HOST_PORT:-18091}:8081`(JobManager) |
| Labels | `hy-home.tier: lab`, `traefik.enable: 'false'` |
| Secret refs | `lab_lakehouse_s3_lakehouse_secret_key` -> `seaweedfs_s3_lakehouse_secret_key` |
| Healthcheck | JobManager는 `/overview`, TaskManager는 JobManager의 `/taskmanagers` 응답에 등록 ID가 있는지 검사함. 후자는 특정 작업 성공·checkpoint·복원 증거가 아님 |
| Operations | Guide (`docs/05.operations/guides/15-labs/0094-lakehouse.md`), Policy (`docs/05.operations/policies/15-labs/0094-lakehouse.md`), Runbook (`docs/05.operations/runbooks/15-labs/0094-lakehouse.md`) |
| Validation | `config --quiet` render, `tests.validation.test_lab_isolation` |
| Troubleshooting | 활성 lease 안에서 `flink list -a`를 실행한 뒤 runbook을 따름 |

## Usage

1. Flink와 Spark Dockerfile의 Iceberg 버전을 함께 올리십시오. Flink runtime jar 이름에는 Flink minor 버전이 들어갑니다.
2. Renovate는 `FROM` 이미지만 갱신하며 jar는 새 checksum으로 수동 갱신합니다. Flink minor 버전이 오르면 대응하는 `iceberg-flink-runtime-<minor>`와 Kafka connector jar도 필요합니다.
3. 스트리밍 `INSERT`는 취소될 때까지 실행되며 각 checkpoint(wrapper 기본값 60초)마다 커밋됩니다. job ID와 대상 table을 기록하십시오.

런타임 이미지 권한은 [labs/lakehouse.yml](../../lakehouse.yml)이 소유하며
[derived Compose 이미지 투영](../../../infra/tech-stack.versions.json)은 drift 증거입니다.
