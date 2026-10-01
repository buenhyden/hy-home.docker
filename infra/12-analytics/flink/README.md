---
title: "Flink (Iceberg)"
version: "1.0.2"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-09-23"
---

<!-- [ID:04-data:lakehouse-flink] -->
# Flink (Iceberg)

> SeaweedFS REST catalog의 Iceberg table에 스트리밍/배치 SQL을 쓰는 on-demand OPTIONAL Flink session cluster입니다.

## Overview

Flink는 `lakehouse` profile로 선택되는 **OPTIONAL** stream processing engine입니다.
JobManager 하나와 TaskManager 하나(slot 2개)로 된 session cluster입니다. catalog
`lakehouse`는 Spark·Trino와 같은 SeaweedFS Iceberg REST catalog와 `lakehouse`
S3 identity를 사용합니다. Kafka source와 sink는 `kafka_net`의 `kafka-1:19092`를
씁니다. REST API와 UI에 인증이 없으므로 `127.0.0.1`에만 게시하고 route는 없습니다.
REST API로 JAR를 올릴 수도 없습니다.

## Audience

이 README의 주요 독자:

- Data engineers
- Operators
- AI Agents

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
├── docker-compose.yml  # flink-jobmanager, flink-taskmanager
└── hyhome-flink.sh     # secret을 export하고 /tmp/lakehouse.sql을 작성한 뒤 명령을 실행함
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Engine** | Apache Flink(`Dockerfile`의 base image) | JobManager 1 CPU / 1.25 GiB, TaskManager 2 CPU / 2 GiB, slot 2개 |
| **Table format** | Iceberg Flink runtime | Spark와 동일한 Iceberg 버전; SigV4 REST catalog, S3FileIO |
| **Streaming source** | Kafka SQL connector | `kafka_net`의 `kafka-1:19092` |
| **State** | File checkpoint | `${DEFAULT_DATA_DIR}/flink/checkpoints`, 두 컨테이너가 공유 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `FLINK_HOST_PORT` | No | REST API/UI용 loopback 호스트 포트(기본값: 18091). |
| `SEAWEEDFS_ICEBERG_PORT` | No | `seaweedfs-s3`의 REST catalog 포트(기본값: 8181). |
| `DEFAULT_DATA_DIR` | Yes | checkpoint 디렉터리의 상위 경로. |

Secret은 `seaweedfs_s3_lakehouse_secret_key`(STRG-015)이며 access key ID는
`lakehouse`입니다. Flink 설정은 `docker-compose.yml`의 `-D` 인자로 지정하며
이미지 설정 파일은 수정하지 않습니다.

## Available Scripts

서비스 시작에는 runtime 승인이 필요합니다. 먼저 checkpoint 디렉터리를
생성하십시오: `install -d -m 2770 -g "${SECRETS_GID:-1000}" "$DEFAULT_DATA_DIR/flink/checkpoints"`.

| Command | Description |
| :--- | :--- |
| `docker compose --profile lakehouse up -d flink-jobmanager flink-taskmanager` | session cluster 시작(아무것도 쓰지 않음). |
| `docker compose exec flink-jobmanager bash /opt/hyhome/hyhome-flink.sh /opt/flink/bin/sql-client.sh -i /tmp/lakehouse.sql` | `lakehouse` catalog에 대한 SQL client. |
| `docker compose exec flink-jobmanager /opt/flink/bin/flink list -a` | job 목록. |
| `docker compose exec flink-jobmanager /opt/flink/bin/flink cancel <job_id>` | job 중지. |

## Validation

- `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests.test_3_flink_writes_the_lakehouse_catalog`

## Troubleshooting

- Exit `64`: `lakehouse` secret이 없거나 비어 있습니다.
- `ClassNotFoundException: org.apache.hadoop.conf.Configuration`: 이미지에 Hadoop client jar가 없습니다.
- SQL client에서 `lakehouse` catalog가 없거나 S3 `403`이 발생: wrapper 없이 시작되었습니다. 위와 같이 `hyhome-flink.sh`로 실행하십시오.
- 스트리밍 `INSERT`가 커밋되지 않음: checkpointing이 꺼져 있습니다. wrapper는 60초 간격을 설정하며 세션 `SET`으로 이를 끄면 안 됩니다.
- Checkpoint `AccessDeniedException`: 호스트 checkpoint 디렉터리가 group-writable이 아닙니다. lakehouse runbook을 따르십시오.

## Related Documents

- **Guide**: Lakehouse Usage Guide (`docs/05.operations/guides/0094-lakehouse.md`)
- **Policy**: Lakehouse Operations Policy (`docs/05.operations/policies/0094-lakehouse.md`)
- **Runbook**: Lakehouse Recovery Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`)
- [문서 인덱스](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `12-analytics`의 Flink leaf; services: `flink-jobmanager`, `flink-taskmanager`; [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/12-analytics/flink/docker-compose.yml` |
| Config files | `Dockerfile`, `docker-compose.yml`, `hyhome-flink.sh` |
| Config values | profiles: `lakehouse` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/12-analytics/flink/docker-compose.yml` |
| Networks | `object_net`, `kafka_net` |
| Volumes | `./hyhome-flink.sh:/opt/hyhome/hyhome-flink.sh:ro`, `flink-checkpoints:/opt/flink/checkpoints` |
| Ports | `127.0.0.1:${FLINK_HOST_PORT:-18091}:8081`(JobManager) |
| Labels | `hy-home.tier` |
| Secret refs | `seaweedfs_s3_lakehouse_secret_key` |
| Healthcheck | JobManager `curl -fsS http://localhost:8081/overview`; TaskManager는 없음(정상 JobManager를 기다림) |
| Operations | Guide (`docs/05.operations/guides/0094-lakehouse.md`), Policy (`docs/05.operations/policies/0094-lakehouse.md`), Runbook (`docs/05.operations/runbooks/0094-lakehouse.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `flink list -a`를 실행한 뒤 runbook을 따름 |

## How to Work in This Area

1. Flink와 Spark Dockerfile의 Iceberg 버전을 함께 올리십시오. Flink runtime jar 이름에는 Flink minor 버전이 들어갑니다.
2. Renovate는 `FROM` 이미지만 갱신하며 jar는 새 checksum으로 수동 갱신합니다. Flink minor 버전이 오르면 대응하는 `iceberg-flink-runtime-<minor>`와 Kafka connector jar도 필요합니다.
3. 스트리밍 `INSERT`는 취소될 때까지 실행되며 각 checkpoint(wrapper 기본값 60초)마다 커밋됩니다. job ID와 대상 table을 기록하십시오.

런타임 이미지 권한은 [docker-compose.yml](docker-compose.yml)이 소유하며
[derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift 증거입니다.
