---
title: "Management Database Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "GDE-0028"
parent_ids:
- "POL-0028"
implementation_services:
  infra/04-data/mng-db/docker-compose.yml:
  - 'mng-pg'
  - 'mng-pg-exporter'
  - 'mng-pg-init'
  - 'mng-valkey'
  - 'mng-valkey-exporter'
created: "2026-05-10"
---

# Management Database Usage Guide

## Usage

management database는 인증, 워크플로, 도구를 위한 5개 서비스로 구성된 HOME
의존성이다. `mng-pg`는 `n8n`, `keycloak`, `airflow`, `terrakube`, `sonarqube`,
`postgres`를 저장한다. 기존 `app_db`는 소유자 진술상 자료·앱 소비자가 없는
기술적 이관 대상으로 보존하며 새 업무 앱의 공용 DB로 사용하지 않는다. `mng-valkey`는
Airflow/n8n이 공유하는 broker/cache다. Grafana는 현재 Compose에서 management
PostgreSQL에 연결되지 않는다. 자체 `grafana-data`를 소유하고 기본 데이터베이스
구성을 그대로 사용한다.

### Current implementation

[`infra/04-data/mng-db/docker-compose.yml`](../../../infra/04-data/mng-db/docker-compose.yml)은
`mng-pg`, `mng-pg-init`, `mng-pg-exporter`, `mng-valkey`, `mng-valkey-exporter`를
정의한다. `mng`, `core`, `dev`, `local` profile은 엔진과 init을 함께 선택하고,
exporter는 `mng`와 `dev`에서 선택된다.

PostgreSQL은 `${DEFAULT_MANAGEMENT_DIR}/pg`의 `mng-pg-data`를 소유하고
`mng_postgres_password` secret을 사용한다. 기본 init job은 base 서비스별 데이터베이스
비밀번호 secret만 읽어 해당 role/database를 idempotent하게 생성한다. 선택적
기능은 자체 객체를 별도 feature job(`mlflow-db-provision`, `superset-db-provision`, `pact-broker-db-provision`)에서 provision한다. 이 job들은 입력을 검증하는
[runner](../../../infra/04-data/mng-db/pg/provision/run-feature-provision.sh)를
공유하지만 SQL과 grant는 각자의 패키지에 둔다. `mlops`, `data-science`,
`bi`, `contract-testing`도 의존성 closure를 위해 `mng-pg`와 `mng-pg-init`을
선택하지만, base job은 이들의 credential을 읽지 않으므로 `core`, `mng`, `dev`,
`local`은 이들 없이 기동한다.

선언된 command는 CDC를 위해 `wal_level=logical`, `max_replication_slots`,
`max_wal_senders`, `max_slot_wal_keep_size`를 설정한다. 실행 중인 인스턴스는
승인된 recreate 전까지 이전 설정을 유지한다. recreate하면 management database의
공유 DB 연결이 중단된다. Compose는 모든 consumer를 자동 재시작하지 않는다. logical WAL은 WAL 볼륨을 소폭 늘리고, slot은
등록된 CDC connector만 생성한다. Valkey는 `${DEFAULT_MANAGEMENT_DIR}/valkey`의
`mng-valkey-data`를 소유하고 AOF를 활성화하며 `mng_valkey_password`를 읽는다.
둘 다 `mng_data_net`을 사용한다. PostgreSQL host port(`POSTGRES_HOST_PORT`,
기본값 `25432`)는 `127.0.0.1`에만 게시하고, Valkey host port
(`VALKEY_MNG_HOST_PORT`, 기본값 `26379`)는 `HOST_LAN_BIND_IP`(기본값
`192.168.0.13`)에 게시해 k3d Argo CD 캐시가 도달한다. healthcheck와 리소스
제한은 공유 템플릿에서 온다.

### Identity-specific behavior

mng-pg18.6+pgBackRest2.58 은 physical/WAL backup 을, mng-valkey9.1.2 는 AOF state 와 backup orchestrator 의 RDB export 를 사용한다. mng-pg-init 는 base role/database DDL 이며 optional feature runner/SQL 은 해당 subject 가 소유한다(MLflow,Superset,Pact 등). PG 는 loopback, Valkey 는 HOST_LAN_BIND_IP 에 host port 를 게시한다. 두 exporter 는 각각 PG/Valkey 한 target 이며 health 는 업무 정합성을 확인하지 않는다. feature profile 에는 bi/contract-testing 도 포함한다. 앱 quiescence 와 조정된 logical dump 요구는 여전히 필수이며 현재 daily physical/RDB automation 이 앱별 동시 복구를 보장하지 않는다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `mng-pg` | 공유 PG database/roles + physical backup/WAL; custom entrypoint | PG 연결 수락; SQL 권한/업무 정합성 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/mng-db/docker-compose.yml) |
| `mng-pg-exporter` | 공유 PG metrics | 선언된 endpoint health; scrape/data 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/mng-db/docker-compose.yml) |
| `mng-pg-init` | base role/database provisioning job; feature DDL 제외 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/04-data/mng-db/docker-compose.yml) |
| `mng-valkey` | 공유 workflow/session AOF state; queue replay 별도 승인 | 인증 PING; cluster slot/queue 정합성 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/mng-db/docker-compose.yml) |
| `mng-valkey-exporter` | 공유 Valkey metrics | 선언된 endpoint health; scrape/data 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/mng-db/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### Images, configuration and resource controls

Compose 파일은 핀된 upstream PostgreSQL, Valkey, 두 exporter 이미지 계열의
권위 있는 정의다. 저장소 Renovate가 업데이트를 제안하면 버전 projection은
파생된다. PostgreSQL은 `POSTGRES_PASSWORD_FILE`, `POSTGRES_USER`,
`POSTGRES_DB`, `PGDATA`, `POSTGRES_HOSTNAME`, `POSTGRES_PORT`를 사용하며, init은
관리 서비스의 계정·DB 이름만 추가한다. root 포트 키가
host binding을 제어한다. `mng-pg`는 `template-stateful-db-med`를,
`mng-valkey`는 `template-stateful-low`를, init은 `template-job-low`를,
exporter는 `template-infra-readonly-low`를 extend하며, 엔진/exporter
healthcheck가 선언되어 있다. 현재 consumer는 `mng_data_net`으로 연결되며,
init은 PostgreSQL health 이후 role/database를 생성하고 exporter는 엔진을
관찰한다.

### Static preflight

```bash
docker compose --env-file .env.example --profile mng config --quiet
docker compose --env-file .env.example --profile mng config --services
```

저장소 루트에서 실행한다. leaf 파일만 단독으로 렌더링하거나 기동하지 않는다.
승인된 runtime task 없이 init을 재실행하거나, credential을 회전하거나, HOME
데이터베이스를 조회하거나, broker queue를 변경하지 않는다.

### Backup, recovery and upgrades

PostgreSQL은 global role과 모든 데이터베이스의 logical dump가 필요하다.
현재 자동 백업은 pgBackRest physical/WAL과globals export, Valkey RDB이며 이 logical/AOF 요구를 전부 구현하지 않는다. 완전한 앱 정합 복원은 별도 승인·검증이 필요하다. Valkey는 완전한 AOF set/manifest 하나와 RDB checkpoint 하나가 필요하며,
incident owner가 지연된 대기 작업을 재실행해도 안전한지 판단해야 한다.
[RUN-0028](../runbooks/0028-management-database.md)이 격리된 복구 순서와
애플리케이션 검증을 정의한다.

PostgreSQL major upgrade는 logical dump/restore 또는 별도로 승인된 다른
upstream 방법을 사용한다. minor 이미지 변경과 Valkey 변경도 release note,
backup, rollback이 필요하다. 새 major PostgreSQL 이미지를 기존 `PGDATA`에
연결하거나 실행 중인 데이터베이스 파일을 복사하지 않는다.

### Official references

- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
- [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)
- [PostgreSQL upgrading](https://www.postgresql.org/docs/current/upgrading.html)
- [PostgreSQL license](https://www.postgresql.org/about/licence/)
- [Valkey persistence](https://valkey.io/topics/persistence/)

## Common Checks

정확한 root profile, service, health/resource 제어, writable-state 소유권,
secret reference, exposure, 엔진별 복구 경계를 확인한다. static pass는 구성
증거일 뿐이며, runtime과 restore는 별개로 남는다.

## Traceability

- Artifact: `GDE-0028`; 거버넌스 정책: `POL-0028`.
- Runtime authority: `infra/04-data/mng-db/docker-compose.yml`.

## Related Documents

- [Operations policy](../policies/0028-management-database.md)
- [Health and recovery runbook](../runbooks/0028-management-database.md)
- [Backup policy](../policies/0021-backup-and-restore.md)
