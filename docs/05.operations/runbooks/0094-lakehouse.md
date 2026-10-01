---
title: "Lakehouse Recovery Runbook"
version: "1.3.3"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0094"
parent_ids:
- "GDE-0094"
created: "2026-09-23"
---

# Lakehouse Recovery Runbook

## When to Use

Spark 작업, Trino, Flink 작업 또는 Great Expectations 스위트가 실패하거나,
카탈로그가 오류를 반환하거나, 접근이 거부되거나, 잘못된 쓰기 이후 테이블
롤백이 필요할 때 사용한다.


### Execution and stop boundary

대상: `seaweedfs-table-bucket`, `flink-jobmanager`, `flink-taskmanager`, `great-expectations`, `spark`, `trino`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

1. 저장소 루트에서 승인된 대상만 점검한다. `--no-deps` 예시는 SeaweedFS/table-bucket와 Trino가 이미 준비된 경우만 해당한다. 준비되지 않았으면 멈추며 진단을 위해 provisioning을 암묵 실행하지 않는다.

   ```bash
   docker compose --profile lakehouse config --quiet
   docker compose --profile lakehouse logs --tail=100 seaweedfs-table-bucket seaweedfs-s3
   docker compose --profile lakehouse run --rm --no-deps spark
   ```

   마지막 명령은 네임스페이스를 나열해 카탈로그 접근을 처음부터 끝까지
   증명한다. Trino의 경우:
   `docker compose --profile lakehouse logs --tail=100 trino`를 실행한 뒤
   `docker compose exec trino trino --execute "SHOW SCHEMAS FROM lakehouse"`를
   실행한다. Flink의 경우:
   `docker compose --profile lakehouse logs --tail=100 flink-jobmanager flink-taskmanager`를
   실행한 뒤 `docker compose exec flink-jobmanager /opt/flink/bin/flink list -a`를
   실행한다. 스위트의 경우:
   `docker compose --profile lakehouse run --rm --no-deps great-expectations validate <suite>`를
   실행한다. `"success": false` 앞 줄에 실패한 expectation이 나온다(종료
   `1`). 종료 `2`는 아무것도 검사하지 못했다는 뜻이며 원인은 stderr에
   나온다.
2. Spark/Flink/Trino의 명시적 secret 검증 실패는64일 수 있지만 shell 환경/파일 오류는 다른 종료 코드다. GX는 secret을 읽지 않고 검사 불가2를 사용한다. 종료 코드와 실제 오류 종류를 함께 확인한다.
3. `table bucket … not found`는 table bucket이 없거나 다른 계정 소유라는
   뜻이다. 원인을 확인하고 owner가 provisioning mutation을 승인한 경우에만 `seaweedfs-table-bucket`을 재실행한다(`seaweedfs-table-bucket`이 그 작업이며 수작업으로
   편집한 정책도 재설정한다).
4. `ForbiddenException`/`AccessDenied`는 잘못된 credential, 정책, 시간/SigV4, 대상 bucket 등 여러 원인이 있다. source·mount 참조와 sanitized 오류를 비교하고 즉시 재생성하지 않는다. 수정 승인 뒤 key/config 소비자를 제한 재생성하고 signed allow/deny를 검증한다. table-bucket 재실행은 정책을 덮어쓰며 data restore가 아니다.
5. 잘못된 쓰기라면 writer를 승인 범위에서 quiesce하고 snapshot 목록·보존 기간을 확인한다. 정확한 table/snapshot과 영향 승인 후에만 아래 Iceberg rollback을 수행한다.

   ```sql
   SELECT snapshot_id, committed_at, operation FROM dev.t.snapshots;
   CALL lakehouse.system.rollback_to_snapshot('dev.t', <snapshot_id>);
   ```

   롤백은 스냅샷이 만료되기 전에만 동작한다. Trino에서는
   `SELECT snapshot_id, committed_at FROM lakehouse.dev."t$snapshots"`와
   `ALTER TABLE lakehouse.dev.t EXECUTE rollback_to_snapshot(snapshot_id => <snapshot_id>)`를
   사용한다.
6. Trino의 `Failed to list views`는 카탈로그 파일에
   `iceberg.rest-catalog.view-endpoints-enabled=false`가 누락되었다는
   뜻이다.
7. Flink 체크포인트가 `/opt/flink/checkpoints`에서 `AccessDeniedException`으로
   실패하면 컨테이너가 호스트 디렉터리에 쓸 수 없다는 뜻이다. 운영자
   권한으로
   `install -d -m 2770 -g "${SECRETS_GID:-1000}" "$DEFAULT_DATA_DIR/flink/checkpoints"`를
   실행해 생성한다. 컨테이너는 `SECRETS_GID` 그룹을 통해 쓴다. `RESTARTING`
   상태에 멈춘 작업은 `flink cancel <job_id>`로 취소한다. 이전 체크포인트에서
   커밋된 행은 테이블에 남는다.

## Evidence

네임스페이스, 테이블 이름, 스냅샷 ID, 행 개수, 종료 코드, 소스 커밋을
기록한다. 데이터 값이나 시크릿은 절대 기록하지 않는다.

## Rollback or Recovery

테이블 메타데이터와 데이터는 SeaweedFS 객체로, SeaweedFS 복구 세트에서
다룬다(RUN-0024). filer 메타데이터를 잃으면 카탈로그를 잃는다. `dev`와
`test`라는 이름만으로 재생 가능하다고 가정하지 않는다. 원본·revision·재생 절차가 검증된 disposable table만 owner가 backup 제외를 승인한다. 그 외 catalog/object/checkpoint는 보존한다.

## Escalation

엔진에서 admin identity를 사용하거나, 카탈로그를 `object_net` 밖으로
노출하거나, 명시된 사유 없이 테이블의 스냅샷을 만료시키라는 요청이 있으면
중단하고 @buenhyden에게 target·영향·검증되지 않은 항목을 전달한다.

## Traceability

- [Guide](../guides/0094-lakehouse.md) (`GDE-0094`)
- [Policy](../policies/0094-lakehouse.md) (`POL-0094`)
- [SeaweedFS runbook](0024-seaweedfs.md)

## Related Documents

- [Spark 패키지 README](../../../infra/12-analytics/spark/README.md)
- [Trino 패키지 README](../../../infra/12-analytics/trino/README.md)
- [Flink 패키지 README](../../../infra/12-analytics/flink/README.md)
- [Great Expectations 패키지 README](../../../infra/12-analytics/great-expectations/README.md)
- [Iceberg maintenance](https://iceberg.apache.org/docs/latest/maintenance/)
