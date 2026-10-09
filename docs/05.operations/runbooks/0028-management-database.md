---
title: "Management Database Health and Init Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "operations"
artifact_id: "RUN-0028"
parent_ids:
- "GDE-0028"
created: "2026-05-17"
---

# Management Database Health and Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

승인된 정적 진단, 백업 계획 또는 정확히 이 주제에 해당하는 격리 복구에 사용한다.
실 쓰기, 복원, cutover, 정리, credential 변경은 별도 승인된 task가 필요하다.

### Execution and stop boundary

대상: `mng-pg`, `mng-pg-exporter`, `mng-pg-init`, `mng-valkey`, `mng-valkey-exporter`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

### Procedure

저장소 루트에서 실행한다.

```bash
docker compose --env-file .env.example --profile mng config --quiet
docker compose --env-file .env.example --profile mng config --services
```

두 엔진, init, exporter, 분리된 persistent volume, secret 참조, health check,
`mng_data_net`을 확인한다. 환경 변수 치환으로 private value가 노출될 수 있는
완전히 렌더링된 configuration은 출력하지 않는다.

### Planned PostgreSQL backup

1. consumer를 고려한 시간대를 확보하고 role과 `postgres`, `n8n`,
   `keycloak`, `airflow`, `terrakube`, `sonarqube`, 그리고 설정된 애플리케이션
   database를 조사한다. 이 목록이 전부라고 가정하지 말고 추가 항목을 찾는다.
2. 호환되는 PostgreSQL client를 사용해 cluster globals와 각 database를 복원
   가능한 logical format으로 dump한다. 실행 중인 `PGDATA`를 raw로 복사하지 않는다.
3. source/server 및 client 버전, database 이름, 크기, dump 크기, 종료 상태,
   해시를 기록한다. 산출물은 별도의 암호화된 destination에 저장하고 비밀번호는
   인자나 evidence에 남기지 않는다.

### Planned PostgreSQL isolated restore

1. 애플리케이션 경로가 없는 지원되는 호환 버전의 빈 격리 target을 준비한다.
   최소 권한 restore operator를 사용한다.
2. `pg_restore`는 source superuser가 선택한 문장을 실행할 수 있으므로 dump
   source를 신뢰할 수 있는지 검사한다. globals/role을 먼저 복원한 뒤 의존성
   순서에 맞춰 각 database를 생성하고 복원한다.
3. role과 grant, schema object, extension 가용성, table/row 개수, 선택한
   애플리케이션 읽기를 검증한다. Keycloak, Airflow, n8n, Terrakube, SonarQube의
   disposable 확인은 해당 owner가 승인한 경우에만 연결한다.
4. recovery point와 소요 시간을 기록한다. 별도 cutover에서 writer를 일시
   중지하고 최종 dump를 뜬 뒤 consumer를 전환하며, rollback을 위해 이전
   volume을 보존한다.

### Planned Valkey backup and restore

1. workflow producer/worker를 일시 중지하거나 drain하고, 대기 중인 job을
   재생할지 폐기할지 문서화한다.
2. RDB checkpoint를 생성/확인하고 AOF rewrite를 가로지르지 않은 상태로 전체
   AOF 디렉터리와 manifest를 복사한다. 해시와 persistence 설정을 기록한다.
3. 전체 세트를 비어 있는 격리된 호환 Valkey target에 복원한다. 정상 로드,
   key/type/TTL 개수, disposable 읽기/쓰기/삭제 테스트를 확인한다.
4. workflow owner의 승인 없이는 복원된 stale queue 상태를 active worker에
   연결하지 않는다.

### 관측 경보와 monitor 계정

`mng-pg-exporter`와 `mng-valkey-exporter`는 관리자 비밀 대신 `mng_pg_monitor`
role과 `mngmonitor` ACL 사용자로 접속한다. 경보는 `db_scope="mng"`로 구분한다.

| 경보 | 뜻 | 먼저 볼 것 |
| --- | --- | --- |
| `MngDatastoreExporterDown` | Prometheus가 exporter를 수집하지 못함(`up=0`) | exporter 컨테이너 상태와 재시작 반복, `obs_net` 연결 |
| `PostgresDown` | exporter는 응답하지만 `mng-pg` 접속 실패(`pg_up=0`) | `mng-pg` health, monitor 비밀번호 불일치, 연결 한도 3 |
| `ValkeyDown` | exporter는 응답하지만 `mng-valkey` 접속 실패(`redis_up=0`) | `mng-valkey` health, `mngmonitor` 비밀번호 불일치 |
| `PostgresqlExporterError` | 마지막 수집에 오류가 있음 | `pg_scrape_collector_success`가 0인 collector와 role 권한 |

monitor 비밀번호 회전은 다음 순서다. 비밀 값은 출력하지 않는다.

1. `secrets/db/mng-pg/monitor_password.txt`를 base64 문자(16자 이상)의 새 값으로
   바꾼다. 다른 문자가 섞이면 provision job이 접속 전에 거부한다.
2. `mng-pg-monitor-provision`을 다시 실행해 exit 0을 확인하고 `mng-pg-exporter`를
   재생성한다.
3. Valkey는 `secrets/db/mng-valkey/monitor_password.txt`를 바꾸고 `mng-valkey`를
   재생성한 뒤(ACL은 시작할 때 렌더링된다; 공유 소비자가 잠시 다시 연결된다)
   `mng-valkey-exporter`를 재생성한다.
4. `pg_up{db_scope="mng"}`와 `redis_up{db_scope="mng"}`가 1로 돌아오는지 확인한다.

## Verification

### Evidence

source revision/version, 범위, timestamp, manifest/checksum 요약, 명령과 종료
상태, 검증 결과, 관측된 recovery point/시간, 미검증 gap을 모두 기록한다.
secret, raw payload, private resolved path는 제외한다.

## Rollback and Escalation

### Rollback or Recovery

cutover가 실패하면 consumer를 검증된 이전 HOME 엔진과 volume으로 되돌리고
격리된 restore는 client로부터 계속 차단해 둔다. cutover는 owner
승인, 최종 consistency capture, 애플리케이션 검증, 보존된 rollback window
이후에만 실행한다.

### Escalation

database 누락, dump 오류, 지원되지 않는 extension, ownership drift, AOF
truncation/repair prompt, checksum mismatch, 또는 모호한 queue semantics에서
중단한다. 이 문서에 설명한 recovery는 이번 문서 수정 task에서 실행하지 않았다.

### Traceability

- Artifact: `RUN-0028`; parent guide: `GDE-0028`.
- 날짜가 기록된 verification record가 실행 사실을 명시하지 않는 한 절차는 계획 상태다.

### References

- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
- [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)
- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Policy](../policies/0028-management-database.md)

## Related Documents

- [Domain catalog](../README.md)
