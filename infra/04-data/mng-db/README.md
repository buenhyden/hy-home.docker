---
title: "Management Database (mng-db)"
version: "1.1.5"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
created: "2025-12-03"
---

# Management database

## Overview

이 패키지는 저장소의 HOME 관리 PostgreSQL과 Valkey를 정의합니다.

## Audience

공유 관리 상태의 operator와 maintainer를 대상으로 합니다.

## Scope

[`docker-compose.yml`](docker-compose.yml)이 HOME `mng-pg`, `mng-pg-init`,
`mng-pg-exporter`, `mng-valkey`, `mng-valkey-exporter`를 정의합니다. `mng`,
`core`, `dev`, `local` profile이 두 엔진/init을 선택하고, exporter는 `mng`와
`dev`를 사용합니다. `mlops`, `data-science`, `analytics-engineering`, `cdc`도
의존성 closure만을 위해 `mng-pg`와 `mng-pg-init`을 선택합니다. 선언된 `mng-pg`
명령은 CDC와 pgBackRest로의 연속 WAL 아카이빙을 위해 logical WAL
(`wal_level=logical`과 slot, sender, retention cap)을 활성화합니다. 실행 중인
인스턴스는 승인된 재생성 전까지 이전 설정을 유지합니다.

`mng-pg`는 일반 PostgreSQL 이미지에 고정된 Alpine pgBackRest 패키지를 더한
`pg/backup/Dockerfile`로 빌드되므로, `archive_command`는 서버 내부에서
`postgres` 사용자(UID/GID 70)로 실행됩니다. `pg/backup/pgbackrest.conf`는
`/var/lib/pgbackrest`의 암호화된 repository를 사용하는 stanza `mng`를
정의하며 다른 물리 디스크의 `${BACKUP_STATE_REPO_DIR}/pgbackrest`에
바인딩됩니다(`create_host_path: false`). `pg/backup/entrypoint.sh`는 공식
entrypoint가 시작되기 전에 `pgbackrest_cipher_pass` secret을
`/tmp/pgbackrest/conf.d` 아래 0600 include 파일에 씁니다. 이 passphrase는
환경 변수나 추적된 설정에 절대 들어가지 않습니다. 비어 있거나 공백만 있는
secret은 컨테이너를 exit 64로 중지시킵니다.

## Structure

`mng-pg-data`는 `${DEFAULT_MANAGEMENT_DIR}/pg`에 매핑됩니다. init job은
n8n, Keycloak, Airflow, Terrakube, SonarQube와 설정된 애플리케이션 database를
위한 현재 role/database를 생성합니다. `mng-valkey-data`는
`${DEFAULT_MANAGEMENT_DIR}/valkey`에 매핑되며 workflow broker/cache 상태를
위해 AOF가 활성화되어 있습니다. Grafana는 현재 Compose에서 관리 PostgreSQL에
연결되어 있지 않습니다.

PostgreSQL은 `mng_postgres_password`와 `pgbackrest_cipher_pass`를 읽습니다.
init은 서비스 database password secret을 읽습니다. Valkey는 시작할 때
`valkey/scripts/render-acl.sh`로 `/run/valkey` tmpfs에 ACL을 만듭니다. `default`
사용자는 `mng_valkey_password`를 그대로 쓰므로 OAuth2 Proxy·n8n·Airflow와
LAN 포트의 외부 클라이언트는 이전과 같이 인증하고(Gatus는 인증 없는 TCP 검사), RedisInsight 조회용
`mnginspector`는 `mng_valkey_inspector_password`로 읽기만 합니다. 지표 수집용
`mngmonitor`는 `mng_valkey_monitor_password`로 `PING`·`INFO`와 로그 길이만 읽습니다.
두 exporter는 관리자 비밀을 받지 않습니다. `mng-pg-monitor-provision`이 만드는
`mng_pg_monitor` role(통계·설정·WAL 디렉터리 조회만, 읽기 전용, 연결 3개)로
`mng-pg-exporter`가 접속하고, `mng-valkey-exporter`는 `mngmonitor`로 접속합니다.
provision job은 실행할 때마다 비밀번호를 비밀 파일에 맞추므로, 회전은 비밀 파일을
바꾸고 job을 다시 실행한 뒤 exporter를 재생성하는 순서입니다. 두 엔진 모두
`mng_data_net`을 사용합니다.
PostgreSQL은 루트 `POSTGRES_HOST_PORT` 키로 `127.0.0.1`에만 호스트 포트를
게시하고, Valkey는 루트 `VALKEY_MNG_HOST_PORT` 키로
`HOST_LAN_BIND_IP`(기본값 `192.168.0.13`)에 게시합니다. exporter는
내부용입니다. PostgreSQL은
`pg_isready`를, Valkey는 인증된 `PING`을, exporter는 HTTP 헬스 체크를
사용하며 init은 완료 여부로 게이트됩니다. `pg/init-scripts/init_users_dbs.sql`은
기본 role/database 초기화를 소유하며 optional-capability secret은 절대 읽지
않습니다. `pg/provision/run-feature-provision.sh`는 feature 소유 job
(`mlflow-db-provision`, `dbt-db-provision`, `debezium-db-provision`)의 공유
입력 처리기입니다. 연결 전에 식별자와 secret 파일을 검증하고 secret은
argv가 아니라 psql 환경(`\getenv`)으로 전달합니다. 각 feature는 자신의 SQL과
grant를 자신의 패키지에 둡니다. 그 외 엔진 설정은 Compose에 남아 있습니다.

## Usage

```bash
docker compose --env-file .env.example --profile mng config --quiet
docker compose --env-file .env.example --profile mng config --services
```

저장소 루트에서 실행하십시오. leaf 전용 Compose 명령은 사용하지 마십시오.
PostgreSQL 복구는 pgBackRest(물리 백업, WAL archive, point-in-time
restore)를 사용합니다. Valkey 복구는 RDB export를 사용합니다. 둘 다 호스트
백업 job에서 실행되며 먼저 격리된 target에만 복원합니다. queue 상태를
재생하기 전에는 workflow owner 승인을 받으십시오. synthetic rehearsal은
`HYHOME_BACKUP_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.BackupRestoreRehearsalTests`입니다.

## Related Documents

[문서 진입점](../../../docs/README.md)을 사용해 Stage 05 subject
`docs/05.operations/guides/0028-management-database.md`, synthetic rehearsal
RUN-0032, 백업 subject `docs/05.operations/guides/0021-backup-and-restore.md`
(POL/GDE/RUN-0021)을 찾으십시오. 공식 소스:
[PostgreSQL backup](https://www.postgresql.org/docs/current/backup.html),
[upgrade](https://www.postgresql.org/docs/current/upgrading.html),
[Valkey persistence](https://valkey.io/topics/persistence/),
[pgBackRest user guide](https://pgbackrest.org/user-guide.html).
