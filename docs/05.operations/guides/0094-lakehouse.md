---
title: "Lakehouse Usage Guide"
version: "1.3.1"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0094"
parent_ids:
- "POL-0094"
implementation_services:
  infra/04-data/lake-and-object/seaweedfs/docker-compose.yml:
  - seaweedfs-table-bucket
  infra/04-data/lakehouse/flink/docker-compose.yml:
  - flink-jobmanager
  - flink-taskmanager
  infra/04-data/lakehouse/great-expectations/docker-compose.yml:
  - great-expectations
  infra/04-data/lakehouse/spark/docker-compose.yml:
  - spark
  infra/04-data/lakehouse/trino/docker-compose.yml:
  - trino
created: "2026-09-23"
---

# Lakehouse Usage Guide

## Usage

### Purpose and classification

레이크하우스는 OPTIONAL이며 `lakehouse`로 선택된다. 테이블은 SeaweedFS
`lakehouse` 테이블 버킷 안의 Apache Iceberg이며 SeaweedFS 내장 Iceberg
REST 카탈로그가 관리한다. Spark는 배치와 테이블 유지보수 엔진, Trino는
대화형 SQL 엔진, Flink는 스트리밍 엔진으로 모두 같은 카탈로그를
사용하고 Great Expectations는 Trino를 통해 테이블을 검사한다. Iceberg는
서비스가 아니라 테이블 포맷이다.

### Current implementation

- **Catalog.** `seaweedfs-s3`는 `object_net`에서만
  `http://seaweedfs-s3:${SEAWEEDFS_ICEBERG_PORT:-8181}`로 REST 카탈로그를
  제공하며 라우트는 없다. 요청은 S3 identity로 SigV4 서명된다. `lakehouse`
  테이블 버킷은 `dev`와 `test` 네임스페이스를 가지며,
  `seaweedfs-table-bucket`
  ([SeaweedFS Compose](../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml))이
  버킷, 정책, 네임스페이스를 생성한다.
- **Identity.** 모든 엔진은 `lakehouse` S3 identity(STRG-015)를 사용한다.
  이 identity의 S3 작업은 `lakehouse` 버킷에만 미치며, 테이블 버킷
  정책은 네임스페이스와 테이블 작업 권한만 부여하고 정책 변경이나 버킷
  삭제는 허용하지 않는다. 다른 버킷은 읽을 수 없다.
- **Spark.** [Spark Compose](../../../infra/04-data/lakehouse/spark/docker-compose.yml)는
  `apache/spark`에 고정된 Iceberg Spark 런타임과 AWS 번들을 더해 빌드한
  일회성 job을 정의한다. 래퍼는 `spark-defaults.conf`를 tmpfs에 작성해
  `lakehouse` 카탈로그를 기본 카탈로그로 설정하고 시크릿을 Spark
  프로세스에 내보내므로, `spark-sql`, `spark-submit`, `pyspark` 모두 같은
  카탈로그를 본다. Spark는 로컬 모드로 2 CPU, 2 GiB, 읽기 전용
  루트 파일시스템, UI 없이 실행된다.
- **Trino.** [Trino Compose](../../../infra/04-data/lakehouse/trino/docker-compose.yml)는
  `lakehouse` 카탈로그를 가진 단일 노드 코디네이터(`trinodb/trino`)를
  실행한다. 카탈로그 파일은 엔드포인트와 시크릿을 환경 변수
  (`${ENV:…}`)에서 읽으며 래퍼가 이 값을 Docker secret에서 채운다.
  SigV4는 S3 키를 명시적으로 설정해야 하고, SeaweedFS가 제공하지 않으므로
  view 엔드포인트는 꺼져 있다. HTTP API는 인증이 없으므로
  `127.0.0.1:${TRINO_HOST_PORT:-18090}`에만 게시되며 라우트는 없다.
  2 CPU, 2 GiB(80% 힙), 읽기 전용 루트, 데이터 디렉터리용 tmpfs로
  실행된다.
- **Flink.** [Flink Compose](../../../infra/04-data/lakehouse/flink/docker-compose.yml)는
  `flink`에 고정된 Iceberg Flink 런타임, AWS 번들, Kafka SQL 커넥터, Hadoop
  클라이언트를 더해 빌드한 세션 클러스터(`flink-jobmanager`,
  슬롯 2개를 가진 `flink-taskmanager`)를 실행한다. 래퍼는 각 JVM에
  시크릿을 내보내고 `CREATE CATALOG lakehouse` 구문을
  `/tmp/lakehouse.sql`에 작성하며, SQL 클라이언트가 이를 `-i`로 로드한다.
  Iceberg 싱크는 체크포인트에서만 커밋하므로 이 파일에서 60초 체크포인트
  간격도 설정한다. Job은 JobManager 컨테이너 안의 SQL 클라이언트에서
  제출하며 REST API를 통한 JAR 업로드는 꺼져 있다.
  파일 체크포인트는 두 컨테이너가 공유하는
  `${DEFAULT_DATA_DIR}/flink/checkpoints`에 저장된다. Kafka 소스와 싱크는
  `kafka_net`의 `kafka-1:19092`를 사용하며, Kafka는 자체 프로파일로
  선택된다. REST API와 UI는 인증이 없으므로
  `127.0.0.1:${FLINK_HOST_PORT:-18091}`에만 게시되며 라우트는 없다.
  JobManager는 1 CPU, 1.25 GiB(1 GiB Flink 프로세스), TaskManager는
  2 CPU, 2 GiB(1.5 GiB Flink 프로세스)를 가지며, 둘 다 UID 9999로 읽기
  전용 루트로 실행된다.
- **Great Expectations.** [GX Compose](../../../infra/04-data/lakehouse/great-expectations/docker-compose.yml)는
  Trino 다이얼렉트를 사용하는 GX Core의 일회성 job으로, `suites/`에서
  추적하는 각 suite를 일시적 컨텍스트에서 Trino로 테이블과 대조 검사한다.
  아무것도 쓰지 않으며 사용 이벤트는 꺼져 있다. 기본 명령은 suite
  목록을 표시하고, `validate`는 expectation 실패 시 `1`, 검사할 수 없을
  때 `2`로 종료한다.

### Commands and side effects

| Command | Effect |
| --- | --- |
| `docker compose --profile lakehouse up spark` | 네임스페이스 목록 표시; 아무것도 쓰지 않음 |
| `docker compose --profile lakehouse run --rm spark /opt/spark/bin/spark-sql -S -e "SHOW TABLES IN dev"` | 읽기 전용 |
| `… spark-sql -S -e "CREATE TABLE dev.t (…) USING iceberg"` / `INSERT` | 테이블 메타데이터와 데이터 파일을 씀 |
| `… -e "CALL lakehouse.system.rewrite_data_files(table => 'dev.t')"` | 데이터 파일을 압축; 스냅샷 추가 |
| `… -e "CALL lakehouse.system.expire_snapshots(table => 'dev.t', older_than => TIMESTAMP '…')"` | 참조되지 않는 파일 삭제; 그 시점 이전으로의 time travel은 사라짐 |
| `… -e "DROP TABLE dev.t PURGE"` | 테이블과 파일을 삭제 |
| `docker compose --profile lakehouse up -d trino` | SQL 엔진 시작; 아무것도 쓰지 않음 |
| `docker compose exec trino trino --execute "SHOW TABLES FROM lakehouse.dev"` | 읽기 전용 |
| `… --execute "CREATE TABLE lakehouse.dev.t (…)"` / `INSERT` / `UPDATE` | 테이블 메타데이터와 데이터 파일을 씀 |
| `… --execute "ALTER TABLE lakehouse.dev.t EXECUTE optimize"` | 데이터 파일을 압축; 스냅샷 추가 |
| `… --execute "DROP TABLE lakehouse.dev.t"` | 테이블과 파일을 삭제 |
| `docker compose --profile lakehouse up -d flink-jobmanager flink-taskmanager` | 세션 클러스터 시작; 아무것도 쓰지 않음 |
| `docker compose exec flink-jobmanager bash /opt/hyhome/hyhome-flink.sh /opt/flink/bin/sql-client.sh -i /tmp/lakehouse.sql` | `lakehouse` 카탈로그로 SQL 클라이언트 열기 |
| `INSERT INTO dev.t SELECT … FROM <kafka table>` (streaming) | 취소될 때까지 실행; 각 체크포인트에서 스냅샷 커밋 |
| `SET 'execution.runtime-mode' = 'batch'; INSERT INTO dev.t …` | 테이블 메타데이터와 데이터 파일을 한 번 씀 |
| `docker compose exec flink-jobmanager /opt/flink/bin/flink cancel <job_id>` | job 중지; 이전 체크포인트에서 커밋된 데이터는 유지 |
| `docker compose --profile lakehouse run --rm great-expectations validate [SUITE...]` | Trino를 통해 테이블을 읽음; expectation 실패 시 `1`로 종료 |

## Common Checks

- `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/check-operations-catalog.py`

## Runbook Handoff

카탈로그 오류, 접근 거부, job 실패, 테이블 복구는
[runbook](../runbooks/0094-lakehouse.md)을 사용한다.

## Traceability

- [Policy](../policies/0094-lakehouse.md) (`POL-0094`)
- [Runbook](../runbooks/0094-lakehouse.md) (`RUN-0094`)
- [SeaweedFS guide](0024-seaweedfs.md)

## Related Documents

- [Spark](../../../infra/04-data/lakehouse/spark/README.md) and [Trino](../../../infra/04-data/lakehouse/trino/README.md) package READMEs and [derived version projection](../../../infra/tech-stack.versions.json)
- [Iceberg Spark procedures](https://iceberg.apache.org/docs/latest/spark-procedures/)
- [Iceberg REST catalog configuration](https://iceberg.apache.org/docs/latest/spark-configuration/)
- [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)
- [Flink](../../../infra/04-data/lakehouse/flink/README.md) package README
- [Iceberg Flink connector](https://iceberg.apache.org/docs/latest/flink/)
- [Great Expectations](../../../infra/04-data/lakehouse/great-expectations/README.md) package README
- [GX Core SQL data sources](https://docs.greatexpectations.io/docs/core/connect_to_data/sql_data/)
