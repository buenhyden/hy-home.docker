---
title: "Lakehouse Recovery Runbook"
version: "1.3.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
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

## Procedure

1. 점검한다.

   ```bash
   docker compose --profile lakehouse config --quiet
   docker compose --profile lakehouse logs --tail=100 seaweedfs-table-bucket seaweedfs-s3
   docker compose --profile lakehouse run --rm spark
   ```

   마지막 명령은 네임스페이스를 나열해 카탈로그 접근을 처음부터 끝까지
   증명한다. Trino의 경우:
   `docker compose --profile lakehouse logs --tail=100 trino`를 실행한 뒤
   `docker compose exec trino trino --execute "SHOW SCHEMAS FROM lakehouse"`를
   실행한다. Flink의 경우:
   `docker compose --profile lakehouse logs --tail=100 flink-jobmanager flink-taskmanager`를
   실행한 뒤 `docker compose exec flink-jobmanager /opt/flink/bin/flink list -a`를
   실행한다. 스위트의 경우:
   `docker compose --profile lakehouse run --rm great-expectations validate <suite>`를
   실행한다. `"success": false` 앞 줄에 실패한 expectation이 나온다(종료
   `1`). 종료 `2`는 아무것도 검사하지 못했다는 뜻이며 원인은 stderr에
   나온다.
2. 어느 wrapper에서든 `64` 종료는 `lakehouse` 시크릿이 없거나 비어 있다는
   뜻이다.
3. `table bucket … not found`는 table bucket이 없거나 다른 계정 소유라는
   뜻이다. `seaweedfs-table-bucket`을 재실행하면 버킷, 정책, 네임스페이스를
   멱등적으로 재생성한다(`seaweedfs-table-bucket`이 그 작업이며 수작업으로
   편집한 정책도 재설정한다).
4. `ForbiddenException`이나 `AccessDenied`는 `s3-identities.conf`의 identity
   줄이나 table bucket 정책이 누락되었다는 뜻이다. 둘 다 `seaweedfs-s3`를
   재생성하고 `seaweedfs-table-bucket`을 재실행하면 복원된다.
5. 잘못된 쓰기라면 스냅샷을 나열하고 롤백한다.

   ```sql
   SELECT snapshot_id, committed_at, operation FROM dev.t.snapshots;
   CALL lakehouse.system.rollback_to_snapshot('dev.t', <snapshot_id>);
   ```

   롤백은 스냅샷이 만료되기 전에만 동작한다. Trino에서는
   `SELECT snapshot_id, committed_at FROM lakehouse.dev."t$snapshots"`와
   `ALTER TABLE lakehouse.dev.t EXECUTE rollback_to_snapshot(<snapshot_id>)`를
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
`test`의 테이블은 재생 가능하며 따로 백업하지 않는다.

## Escalation

엔진에서 admin identity를 사용하거나, 카탈로그를 `object_net` 밖으로
노출하거나, 명시된 사유 없이 테이블의 스냅샷을 만료시키라는 요청이 있으면
중단한다.

## Traceability

- [Guide](../guides/0094-lakehouse.md) (`GDE-0094`)
- [Policy](../policies/0094-lakehouse.md) (`POL-0094`)
- [SeaweedFS runbook](0024-seaweedfs.md)

## Related Documents

- [Spark 패키지 README](../../../infra/04-data/lakehouse/spark/README.md)
- [Trino 패키지 README](../../../infra/04-data/lakehouse/trino/README.md)
- [Flink 패키지 README](../../../infra/04-data/lakehouse/flink/README.md)
- [Great Expectations 패키지 README](../../../infra/04-data/lakehouse/great-expectations/README.md)
- [Iceberg maintenance](https://iceberg.apache.org/docs/latest/maintenance/)
