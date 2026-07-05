---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/storage/storage-exhaustion.md -->

# 04-Data Storage Exhaustion Runbook

## 04-Data Storage Exhaustion Procedure

> Scope: emergency response when `04-data` persistent volumes or the host data root approach full capacity.

### Overview

이 런북은 데이터 볼륨이 포화되어 write failure, service crash, healthcheck failure가 발생할 때 사용하는 실행 절차다. 용량 확인, 증거 확보, 승인된 정리, 장기 복구 계획으로 절차를 분리한다.

### Purpose

- 데이터 서비스 중단을 최소화하면서 storage pressure의 원인을 식별한다.
- destructive cleanup 전에 evidence와 승인 경계를 명확히 한다.
- 백업/보존 정책과 충돌하지 않는 복구 경로를 선택한다.

### Canonical References

- **Spec**: [04-data spec](../../../../03.specs/004-data/spec.md)
- **Policy**: [04-data backup policy](../../../policies/04-data/backup/backup-policy.md)
- **Guide**: [04-data guides index](../../../guides/04-data/README.md)

## When to Use

- 데이터 서비스가 `No space left on device` 오류로 중단되거나 write operation이 실패할 때
- monitoring signal이 `NodeDiskSpaceFilled` 또는 equivalent disk exhaustion 상태를 보고할 때
- Docker volume, `${DEFAULT_DATA_DIR}`, object storage path, or service data directory가 capacity threshold를 초과할 때

## Procedure

### Checklist

- [ ] 영향 서비스, host, volume, timestamp를 기록한다.
- [ ] backup policy와 retention requirement를 확인한다.
- [ ] cleanup이나 truncation이 필요하면 owner approval을 확보한다.
- [ ] secret 값이 command output이나 evidence에 포함되지 않도록 확인한다.

### Steps

1. 현재 용량 상태를 확인한다.

   ```bash
   docker system df -v
   df -h
   ```

2. 데이터 루트에서 큰 경로를 식별한다.

   ```bash
   du -ah "${DEFAULT_DATA_DIR:-/var/lib/docker/volumes}" | sort -rn | head -n 20
   ```

3. 서비스별 영향 범위를 분류한다.
   - PostgreSQL/Supabase: write failure, WAL or table bloat, vacuum requirement
   - Valkey: persistent cache growth or reconstructable cache data
   - MinIO/SeaweedFS: object lifecycle or garbage collection requirement
   - OpenSearch/Qdrant/Neo4j/MongoDB/Cassandra/CouchDB: index, segment, snapshot, or compaction pressure
4. 승인된 정리만 수행한다.
   - unused Docker object cleanup은 backup/retention 영향 검토 후 실행한다.
   - service-specific truncation, flush, garbage collection, compaction은 해당 service runbook or owner approval이 있을 때만 실행한다.
5. 장기 복구 계획을 기록한다.
   - physical disk expansion
   - retention or lifecycle adjustment
   - backup window and restore drill update

### Verification Steps

- [ ] `df -h`에서 affected filesystem capacity가 threshold 아래로 내려갔는지 확인한다.
- [ ] affected service healthcheck가 정상으로 돌아왔는지 확인한다.
- [ ] backup or retention policy violation이 없는지 확인한다.
- [ ] evidence에 cleanup approval, command class, and final state가 기록되었는지 확인한다.

### Observability and Evidence Sources

- **Logs**: affected service logs, Docker event output, host journal summary
- **Metrics**: disk usage, service health status, write error rate, backup job status
- **Evidence**: before/after capacity output, approval note, affected volume list, final verification result

### Safe Rollback or Recovery Procedure

- N/A - no verified rollback procedure can recreate deleted data after destructive cleanup.
- If cleanup would delete data, stop and escalate unless backup evidence and owner approval are both present.
- If capacity cannot be recovered safely, prioritize disk expansion or service scale-out over data deletion.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: stop file inspection if command output risks exposing secrets.
- **Eval Re-run**: run repository validation only after documentation changes; live runtime validation requires approved services.

## Evidence

- Capture affected service, host, volume, command class, before/after capacity, approval status, and final service health.
- Do not record secret values, token values, credentials, private keys, or raw sensitive logs.

## Rollback or Recovery

N/A - no verified rollback procedure can restore data removed by emergency cleanup. Use verified backups, disk expansion, or service-specific recovery procedures when available, then record the selected path in incident evidence.

## Escalation

Escalate to the owning operator before destructive cleanup, when backup evidence is missing, when affected services remain unhealthy after capacity relief, or when the root cause involves unknown data growth. Include captured evidence, attempted steps, current capacity, and the proposed recovery option.

## Related Documents

- [Operations index](../../../README.md)
- [04-data runbooks index](../README.md)
- [04-data backup policy](../../../policies/04-data/backup/backup-policy.md)
- [Incident records](../../../incidents/README.md)
