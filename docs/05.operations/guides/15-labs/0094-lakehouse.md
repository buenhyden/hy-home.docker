---
title: "Lakehouse Usage Guide"
version: "1.5.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "operations"
artifact_id: "GDE-0094"
parent_ids:
- "POL-0094"
implementation_services:
  labs/lakehouse/docker-compose.yml:
  - seaweedfs-table-bucket
  - flink-jobmanager
  - flink-taskmanager
  - great-expectations
  - spark
  - trino
created: "2026-09-23"
next_review_at: "2027-05-13"
---

# Lakehouse Usage Guide

## Purpose

### Outcome

레이크하우스는 root Compose에서 분리된 독립 LAB이며 `labs/lakehouse/docker-compose.yml`의 `lab-lakehouse`
profile로 선택된다(SPEC-0262). 테이블은 HOME SeaweedFS `lakehouse` 테이블 버킷 안의
Apache Iceberg이며 SeaweedFS 내장 Iceberg REST 카탈로그가 관리한다. Spark는 배치와 테이블
유지보수 엔진, Trino는 대화형 SQL 엔진, Flink는 스트리밍 엔진으로 모두 같은 카탈로그를
사용하고 Great Expectations는 Trino를 통해 테이블을 검사한다. Iceberg는 서비스가 아니라
테이블 포맷이다.

레이크하우스(Iceberg, Spark, Trino, Flink, Great Expectations)를 사용하는 데이터 엔지니어와 운영자를 위한 문서다. LAB 경계, 각 엔진의 역할과 명령의 부작용을 이해하고 안전하게 사용·점검하는 것이 목표다.

### Boundaries

#### Traceability

- [Policy](../../policies/15-labs/0094-lakehouse.md) (`POL-0094`)
- [Runbook](../../runbooks/15-labs/0094-lakehouse.md) (`RUN-0094`)
- [SeaweedFS guide](../05-databases-and-storage/0024-seaweedfs.md)
- SPEC-0262 Analytics labs migration: LAB 분리와 HOME endpoint 미결정 항목

#### Related Documents

- [Spark](../../../../labs/lakehouse/spark/README.md) and [Trino](../../../../labs/lakehouse/trino/README.md) package READMEs and [derived version projection](../../../../infra/tech-stack.versions.json)
- [Independent LAB source](../../../../labs/README.md)
- [Iceberg Spark procedures](https://iceberg.apache.org/docs/latest/spark-procedures/)
- [Iceberg REST catalog configuration](https://iceberg.apache.org/docs/latest/spark-configuration/)
- [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)
- [Flink](../../../../labs/lakehouse/flink/README.md) package README
- [Iceberg Flink connector](https://iceberg.apache.org/docs/latest/flink/)
- [Great Expectations](../../../../labs/lakehouse/great-expectations/README.md) package README
- [GX Core SQL data sources](https://docs.greatexpectations.io/docs/core/connect_to_data/sql_data/)

## Prerequisites

### Environment

#### Current implementation

- **Catalog.** HOME `seaweedfs-s3`가 REST 카탈로그를 제공하며 요청은 S3 identity로 SigV4
  서명된다. `lakehouse` 테이블 버킷은 `dev`와 `test` 네임스페이스를 가지며, LAB 작업
  `seaweedfs-table-bucket`([lakehouse LAB Compose](../../../../labs/lakehouse/docker-compose.yml))이 설정된
  S3 endpoint에 버킷, 정책, 네임스페이스를 생성한다.
- **Identity.** 모든 엔진은 `lakehouse` S3 identity(STRG-015)를 사용한다.
  이 identity의 S3 작업은 `lakehouse` 버킷에만 미치며, 테이블 버킷
  정책은 네임스페이스와 테이블 작업 권한만 부여하고 정책 변경이나 버킷
  삭제는 허용하지 않는다. 허용된 열 개 action에는 `DeleteNamespace`/`DeleteTable`도 있으므로 읽기 전용 identity가 아니다. 다른 버킷은 읽을 수 없다.
- **Spark.** `spark`는 `apache/spark`에 고정된 Iceberg Spark 런타임과 AWS 번들을 더해 빌드한
  일회성 job이다. 래퍼는 `spark-defaults.conf`를 tmpfs에 작성해
  `lakehouse` 카탈로그를 기본 카탈로그로 설정하고 시크릿을 Spark
  프로세스에 내보내므로, `spark-sql`, `spark-submit`, `pyspark` 모두 같은
  카탈로그를 본다. Spark는 로컬 모드로 2 CPU, 2 GiB, 읽기 전용
  루트 파일시스템, UI 없이 실행된다.
- **Trino.** `trino`는 `lakehouse` 카탈로그를 가진 단일 노드 코디네이터(`trinodb/trino`)다.
  카탈로그 파일은 엔드포인트와 시크릿을 환경 변수(`${ENV:…}`)에서 읽으며 래퍼가 이 값을
  Docker secret에서 채운다. SigV4는 S3 키를 명시적으로 설정해야 하고, SeaweedFS가 제공하지
  않으므로 view 엔드포인트는 꺼져 있다. HTTP API는 인증이 없으므로
  `127.0.0.1:${LAB_TRINO_HOST_PORT:-18090}`에만 게시되며 라우트는 없다.
  2 CPU, 2 GiB(80% 힙), 읽기 전용 루트, 데이터 디렉터리용 tmpfs로 실행된다.
- **Flink.** `flink`에 고정된 Iceberg Flink 런타임, AWS 번들, Kafka SQL 커넥터, Hadoop
  클라이언트를 더해 빌드한 세션 클러스터(`flink-jobmanager`, 슬롯 2개를 가진
  `flink-taskmanager`)다. 래퍼는 각 JVM에 시크릿을 내보내고 `CREATE CATALOG lakehouse` 구문을
  `/tmp/lakehouse.sql`에 작성하며, SQL 클라이언트가 이를 `-i`로 로드한다.
  Iceberg 싱크는 체크포인트에서만 커밋하므로 이 파일에서 60초 체크포인트
  간격도 설정한다. Job은 JobManager 컨테이너 안의 SQL 클라이언트에서
  제출하며 REST API를 통한 JAR 업로드는 꺼져 있다. 파일 체크포인트는 두 컨테이너가 공유하는
  LAB 체크포인트 디렉터리에 저장된다. REST API와 UI는 인증이 없으므로
  `127.0.0.1:${LAB_FLINK_HOST_PORT:-18091}`에만 게시되며 라우트는 없다.
  JobManager는 1 CPU, 1.25 GiB(1 GiB Flink 프로세스), TaskManager는
  2 CPU, 2 GiB(1.5 GiB Flink 프로세스)를 가지며, 둘 다 UID 9999로 읽기
  전용 루트로 실행된다.
- **Great Expectations.** `great-expectations`는 Trino 다이얼렉트를 사용하는 GX Core의
  일회성 job으로, `suites/`에서 추적하는 각 suite를 일시적 컨텍스트에서 같은 LAB의
  `trino:8080`으로 테이블과 대조 검사한다. 추적된 suite는 읽기 검사를 의도하며 사용 이벤트는
  꺼져 있다. Trino에 인증/권한 제한이 없으므로 suite의 raw SQL 권한을 읽기 전용으로 강제하지는 않는다. 기본 명령은 suite
  목록을 표시하고, `validate`는 expectation 실패 시 `1`, 검사할 수 없을
  때 `2`로 종료한다.

### Permissions

secret은 LAB 전용 `lab_lakehouse_<purpose>`이며 SeaweedFS admin·`lakehouse` key의 LAB 사본은 별도 승인 아래 준비한다. 실행은 활성 lease 안에서 승인된 S3·카탈로그 endpoint가 있을 때만 한다.

## Procedure

### Actions

#### Identity-specific behavior

`seaweedfs-table-bucket`은 admin 권한으로 policy를 매번 다시 쓰고, namespace/table delete 권한도 scoped identity에 부여한다. Flink JobManager와 TaskManager는 같은 build를 쓰지만 command, heap, slot, health가 다르다. JobManager는 `/overview`를 검사하고 TaskManager의 healthcheck는 JobManager `/taskmanagers` 응답에 등록 ID가 있는지 확인한다. 이 검사는 해당 job의 처리·checkpoint·복원 성공을 뜻하지 않으므로 그 결과는 따로 확인한다. Spark는 local one-shot이고 Trino는 인증 없는 single-node SQL이다. Great Expectations는 임시 context로 suite 목록을 표시하는 것이 기본이며 종료 코드 `0`은 통과, `1`은 expectation 실패, `2`는 검사 불가다. Trino username은 권한 제한이 아니다. build의 JAR 중 일부만 checksum으로 고정되며 Hadoop과 Iceberg 기준선 차이는 (미검증)이다. 재생 가능한 증거 없이 Flink checkpoint와 catalog/object를 삭제하지 않는다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `seaweedfs-table-bucket` | table bucket/policy/namespace provisioning job; policy 매번 재작성 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../../labs/lakehouse/docker-compose.yml) |
| `flink-jobmanager` | session/job coordination; shared checkpoint | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../../labs/lakehouse/docker-compose.yml) |
| `flink-taskmanager` | task execution/slots; shared checkpoint, JM 등록 확인 | JM `/taskmanagers` 등록 ID healthcheck; 해당 job·checkpoint·복원은 별도 확인 | [선택·의존·접속·입력·mount](../../../../labs/lakehouse/docker-compose.yml) |
| `great-expectations` | one-shot list/validate; ephemeral context, DB read 의도 | HTTP health 없음; 종료 코드와 읽기/검증 결과 확인 | [선택·의존·접속·입력·mount](../../../../labs/lakehouse/docker-compose.yml) |
| `spark` | one-shot local SQL; table mutation은 명시 command | HTTP health 없음; 종료 코드와 읽기/검증 결과 확인 | [선택·의존·접속·입력·mount](../../../../labs/lakehouse/docker-compose.yml) |
| `trino` | single-node SQL; username은 인증/권한 경계 아님 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../../labs/lakehouse/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 LAB Compose가 소유한다. [공통 template](../../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의 2026-10-01 source snapshot과 official version/build 검토는 W4 Task에 보존했다. 반복 OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

#### Commands and side effects

아래 명령은 저장소 루트에서 `docker compose --env-file labs/.env -f labs/lakehouse/docker-compose.yml --profile lab-lakehouse`
접두사(표에서 `LAB`)로 실행한다. 렌더링만 하는 `LAB config`는 안전하다. 무언가를 시작하는
명령은 `python3 scripts/operations/lab.py check|up|down lakehouse`의 목적·lease·충돌·예산
규칙을 따르는 활성 lease 안에서만 쓰며, 승인된 S3·카탈로그 endpoint가 없으면 실행하지 않는다.
`run --no-deps` 진단은 table-bucket provisioning과 Trino가 이미 준비된 경우에만 사용한다.
준비되지 않았으면 중단하고 [lakehouse runbook](../../runbooks/15-labs/0094-lakehouse.md#actions)을
따른다. `--no-deps`는 bucket/policy/namespace provisioning의 암묵 실행을 막으며 이를 대신하지 않는다.

| Command | Effect |
| --- | --- |
| `LAB config --quiet` | 렌더링만; 필수 endpoint가 비어 있으면 거부 |
| `LAB up spark` | 기본 SQL은 목록 조회; dependency table-bucket job은 bucket/policy/namespace를 변경할 수 있음 |
| `LAB run --rm --no-deps spark /opt/spark/bin/spark-sql -S -e "SHOW TABLES IN dev"` | 읽기 전용 |
| `… spark-sql -S -e "CREATE TABLE dev.t (…) USING iceberg"` / `INSERT` | 테이블 메타데이터와 데이터 파일을 씀 |
| `… -e "CALL lakehouse.system.rewrite_data_files(table => 'dev.t')"` | 데이터 파일을 압축; 스냅샷 추가 |
| `… -e "CALL lakehouse.system.expire_snapshots(table => 'dev.t', older_than => TIMESTAMP '…')"` | 참조되지 않는 파일 삭제; 그 시점 이전으로의 time travel은 사라짐 |
| `… -e "DROP TABLE dev.t PURGE"` | 테이블과 파일을 삭제 |
| `LAB up -d trino` | 엔진 시작과 dependency table-bucket provisioning 가능 |
| `LAB exec trino trino --execute "SHOW TABLES FROM lakehouse.dev"` | 읽기 전용 |
| `… --execute "CREATE TABLE lakehouse.dev.t (…)"` / `INSERT` / `UPDATE` | 테이블 메타데이터와 데이터 파일을 씀 |
| `… --execute "ALTER TABLE lakehouse.dev.t EXECUTE optimize"` | 데이터 파일을 압축; 스냅샷 추가 |
| `… --execute "DROP TABLE lakehouse.dev.t"` | 테이블과 파일을 삭제 |
| `LAB up -d flink-jobmanager flink-taskmanager` | session 시작과 dependency provisioning 가능; job 제출은 별도 |
| `LAB exec flink-jobmanager bash /opt/hyhome/hyhome-flink.sh /opt/flink/bin/sql-client.sh -i /tmp/lakehouse.sql` | `lakehouse` 카탈로그로 SQL 클라이언트 열기 |
| `INSERT INTO dev.t SELECT … FROM <kafka table>` (streaming) | 승인된 Kafka endpoint가 있을 때만; 취소될 때까지 실행하며 각 체크포인트에서 스냅샷 커밋 |
| `SET 'execution.runtime-mode' = 'batch'; INSERT INTO dev.t …` | 테이블 메타데이터와 데이터 파일을 한 번 씀 |
| `LAB exec flink-jobmanager /opt/flink/bin/flink cancel <job_id>` | job 중지; 이전 체크포인트에서 커밋된 데이터는 유지 |
| `LAB run --rm --no-deps great-expectations validate [SUITE...]` | Trino를 통해 테이블을 읽음; expectation 실패 시 `1`로 종료 |

### Exceptions

#### LAB boundary

- **Project.** `hy-home-lab-lakehouse` project의 `lab_lakehouse_net` 하나만 사용한다.
  root는 이 파일을 include하지 않고, 모든 서비스는 `hy-home.tier: lab`과
  `traefik.enable: 'false'` label을 가지며 gateway route가 없다. root `lakehouse` profile은
  이제 HOME SeaweedFS 서비스만 선택하고 분석 엔진은 선택하지 않는다.
- **HOME 의존성.** LAB은 HOME network에 합류하지 않는다(SPEC-0215 LAB 격리). SeaweedFS S3와
  Iceberg REST 카탈로그는 [`labs/.env.example`](../../../../labs/.env.example)의 필수 입력
  `LAB_LAKEHOUSE_S3_ENDPOINT`, `LAB_LAKEHOUSE_CATALOG_URI`로만 지정한다. 값이 비어 있으면
  렌더링이 거부된다. HOME은 기본적으로 이 서비스를 LAB network에 게시하지 않으므로 소유자가
  도달 가능한 endpoint를 승인하기 전까지 이 LAB은 렌더링 전용이다. 이 endpoint 결정은
  SPEC-0262 Task에 기록된 미결정 항목이며 별도 승인 대상이다.
- **Kafka.** Flink는 더 이상 HOME `kafka_net`에 합류하지 않는다. Kafka 소스·싱크에는 승인된
  도달 가능한 bootstrap endpoint가 필요하며 이것도 미결정 항목이다.
- **데이터 경로.** Flink 체크포인트는 `${LAB_DATA_DIR}/lakehouse/flink/checkpoints`에 있다
  (이전 `${DEFAULT_DATA_DIR}/flink/checkpoints`). 기존 데이터는 옮기지 않았으며 재배치는
  별도 승인 아래 수동으로 한다. secret은 LAB 전용이다. 이름은 `lab_lakehouse_<purpose>`이고
  파일은 `${LAB_SECRET_DIR:-../../secrets/labs}/lakehouse/` 아래에 있으며 원래 `/run/secrets/<name>`
  target에 mount되고 group은 `LAB_SECRETS_GID`다. 값은 복사되지 않았으므로 운영자가 SeaweedFS
  admin·`lakehouse` key의 LAB 사본을 별도 승인 아래 준비해야 한다(미결정 항목).

## Verification

### Expected Result

- `docker compose --env-file labs/.env -f labs/lakehouse/docker-compose.yml --profile lab-lakehouse config --quiet`
- `python3 -m unittest tests.validation.test_lab_isolation`
- `python3 scripts/validation/check-operations-catalog.py`

### Troubleshooting

#### Runbook Handoff

카탈로그 오류, 접근 거부, job 실패, 테이블 복구는
[runbook](../../runbooks/15-labs/0094-lakehouse.md)을 사용한다.
