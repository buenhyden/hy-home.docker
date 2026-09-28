---
title: "Management Database Health and Init Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0028"
parent_ids:
- "GDE-0028"
created: "2026-05-17"
---

# Management Database Health and Recovery Runbook

## When to Use

승인된 정적 진단, 백업 계획 또는 정확히 이 주제에 해당하는 격리 복구에 사용한다.
실 쓰기, 복원, cutover, 정리, credential 변경은 별도 승인된 task가 필요하다.

## Procedure

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

## Evidence

source revision/version, 범위, timestamp, manifest/checksum 요약, 명령과 종료
상태, 검증 결과, 관측된 recovery point/시간, 미검증 gap을 모두 기록한다.
secret, raw payload, private resolved path는 제외한다.

## Rollback or Recovery

cutover가 실패하면 consumer를 검증된 이전 HOME 엔진과 volume으로 되돌리고
격리된 restore는 client로부터 계속 차단해 둔다. cutover는 owner
승인, 최종 consistency capture, 애플리케이션 검증, 보존된 rollback window
이후에만 실행한다.

## Escalation

database 누락, dump 오류, 지원되지 않는 extension, ownership drift, AOF
truncation/repair prompt, checksum mismatch, 또는 모호한 queue semantics에서
중단한다. 이 문서에 설명한 recovery는 이번 문서 수정 task에서 실행하지 않았다.

## Traceability

- Artifact: `RUN-0028`; parent guide: `GDE-0028`.
- 날짜가 기록된 verification record가 실행 사실을 명시하지 않는 한 절차는 계획 상태다.

### References

- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
- [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)
- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Policy](../policies/0028-management-database.md)

## Related Documents

- [Domain catalog](../README.md)
