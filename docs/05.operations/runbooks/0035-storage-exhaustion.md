---
title: "04-Data Storage Exhaustion Runbook"
version: "1.0.3"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0035"
parent_ids: []
created: "2026-06-04"
---

# Storage Exhaustion Runbook

## When to Use

승인된 정적 진단, 백업 계획 또는 정확히 이 주제에 해당하는 격리 복구에 사용한다.
실 쓰기, 복원, cutover, 정리, credential 변경은 별도 승인된 task가 필요하다.

### Scope and safety

이 runbook은 데이터를 삭제하지 않고 low-space 상황을 triage한다.
`docker system prune`, volume 제거, database compaction, retention 축소,
log truncation, 또는 알 수 없는 경로의 정리를 승인하지 않는다. 복구와 삭제는
영향받은 owner, 검증된 백업, 별도 승인된 조치가 필요하다.

## Procedure

1. 경보가 발생한 filesystem, mount, 영향받은 서비스를 식별한다. root로
   렌더링한 Compose에서 정확한 bind-backed volume을 확인하되 private path
   값은 공개하지 않는다. 일반적인 Docker volume root를 스캔하거나 수정하는
   방식으로 대체하지 않는다.
2. 식별한 mount에 대해 읽기 전용 filesystem 용량/inode evidence를 기록한다.
   증가 원인이 어느 owner에 속하는지 가린다: database, object store, queue,
   model/cache, observability retention, 또는 container runtime.
3. 승인된 runtime observation을 통해 서비스 health와 쓰기 오류를 확인한다.
   서비스 owner가 손상 위험을 선언하면 추가 writer를 중단한다.
4. 서비스의 백업/복구 policy를 찾아 최신 artifact, destination, checksum,
   격리된 restore 상태를 확인한다. 같은 full filesystem 위의 volume 복사는
   보호가 아니다.
5. 검토된 remediation을 선택한다: filesystem 확장, 엔진이 지원하는 migration을
   통한 데이터 이동, 이미 승인된 retention policy 적용, 또는 재생성 가능성이
   입증된 artifact만 제거한다. 회수되는 바이트와 rollback을 추정한다.

## Evidence

source revision/version, 범위, timestamp, manifest/checksum 요약, 명령과 종료
상태, 검증 결과, 관측된 recovery point/시간, 미검증 gap을 모두 기록한다.
secret, raw payload, private resolved path는 제외한다.

## Rollback or Recovery

rollback은 client를 확장된 용량 또는 승인된 rollback 이후 이전의 변경되지
않은 상태로 되돌린다. cutover는 owner 승인, 최종 consistency capture,
애플리케이션 검증, 보존된 rollback window 이후에만 실행한다.

## Escalation

- Management PostgreSQL/Valkey: [RUN-0028](0028-management-database.md)
- Valkey Cluster: [RUN-0022](0022-valkey-cluster.md)
- SeaweedFS: [RUN-0024](0024-seaweedfs.md)
- 모든 HOME state owner와 예외: [POL-0021](../policies/0021-backup-and-restore.md)

filesystem 명령으로 PostgreSQL WAL/data, Valkey AOF/RDB, SeaweedFS volume
파일, Kafka log, SQLite WAL/journal 파일, OpenBao Raft data, Qdrant snapshot,
observability WAL을 삭제하지 않는다.

## Verification Record

### Validation and closeout

승인된 remediation 이후 filesystem 여유 공간, 서비스 health, 애플리케이션
읽기/쓰기, 백업 연속성을 입증한다. 변경 전후 용량, 무엇을 변경했는지, 승인,
rollback 상태, 수정된 alert 임계값을 기록한다. 데이터 무결성이 미검증 상태로
남아 있으면 여유 공간 evidence만으로 종료하지 않는다.

## Traceability

- Artifact: `RUN-0035`; parent guide: `GDE-0035`.
- 날짜가 기록된 verification record가 실행 사실을 명시하지 않는 한 절차는 계획 상태다.

## Related Documents

- [Data backup policy](../policies/0021-backup-and-restore.md)
- [Data hardening policy](../policies/0030-data-optimization-hardening.md)
