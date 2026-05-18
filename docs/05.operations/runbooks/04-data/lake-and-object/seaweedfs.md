---
status: active
---

# SeaweedFS Runbook

## SeaweedFS Recovery Procedure

> Emergency procedures for SeaweedFS cluster restoration and troubleshooting.
> SeaweedFS 클러스터 복구 및 장애 해결을 위한 긴급 절차.

---

### Overview

#### English

This runbook defines recovery procedures for Master, Volume, Filer, and S3 service failures within the SeaweedFS cluster. It provides step-by-step guidance to minimize data loss and restore services to a normal state quickly.

#### Korean

이 문서는 SeaweedFS 클러스터 내 마스터, 볼륨, 필러 서비스 장애 발생 시의 복구 절차를 설명한다. 데이터 유실을 최소화하고 서비스를 신속하게 정상 상태로 되돌리기 위한 단계별 실행 지침을 제공한다.

### Procedure ID

`RB-DATA-LAKE-SWFS-001`

### Target Audience

- Site Reliability Engineers (SRE)
- Infrastructure Operators
- System Administrators

### When to Use

- **Master Outage**: Cluster management or volume allocation fails.
- **Volume Failure**: Data chunks are inaccessible or replication is broken.
- **Filer Corruption**: Metadata lookup or filesystem operations fail.
- **Mount Issues**: FUSE mount points become stale or unresponsive on the host.

### Diagnosis Steps

1. **Check Cluster Status**:

   ```bash
   curl http://seaweedfs-master:9333/cluster/status
   ```

2. **Review Volume Logs**:

   ```bash
   docker logs seaweedfs-volume
   ```

3. **Check Filer Connectivity**:
   - Verify communication between `seaweedfs-filer` and Master/Volume servers.
4. **Verify Mount Point**:
   - Check if `/mnt/seaweedfs` is accessible: `ls /mnt/seaweedfs`.

### Remediation Procedures

#### 1. Master Server Recovery

If the master server's metadata is corrupted:

- Stop the master container.
- Restore or re-initialize the `seaweedfs-master-data` volume.
- Restart the master and verify that volume servers rejoin automatically.
- Run `weed master.reshard` if necessary to redistribute volume information.

#### 2. Read-Only Mode Resolution

If volume servers switch to read-only due to space limits:

- Add new volume servers or free up space by deleting old data.
- Adjust `volumeSizeLimitMB` in master configuration if required.

#### 3. FUSE Mount Restoration

If the host mount point is unresponsive:

- Restart the `seaweedfs-mount` container.
- If it fails, manually unmount the stale point on the host: `umount -l /mnt/seaweedfs`.
- Relaunch the mount container.

### Verification Steps

- [ ] `curl -s http://seaweedfs-master:9333/cluster/status | jq`: Verify all nodes are online.
- [ ] `weed filer.remote.sync`: Verify metadata synchronization if using remote storage.
- [ ] Write a test file to S3/Filer and read it back to confirm end-to-end functionality.

### Post-Mortem Tasks

- Perform Root Cause Analysis (RCA) on disk/network failures.
- Adjust monitoring thresholds and alerting rules based on findings.
- Update the documentation with any new troubleshooting patterns discovered.

### Overview (KR)

이 런북은 `docs/05.operations/04-data/lake-and-object/seaweedfs.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

### Canonical References

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/README.md](../../../README.md)

### Procedure or Checklist

#### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

#### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/lake-and-object/seaweedfs.md)
- [Operations policy](../../../policies/04-data/lake-and-object/seaweedfs.md)
- [Operations template](../../../../99.templates/operation.template.md)
