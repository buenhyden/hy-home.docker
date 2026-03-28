# SeaweedFS Recovery Runbook

> Emergency procedures for SeaweedFS cluster restoration and troubleshooting.
> SeaweedFS 클러스터 복구 및 장애 해결을 위한 긴급 절차.

---

## Overview

### English

This runbook defines recovery procedures for Master, Volume, Filer, and S3 service failures within the SeaweedFS cluster. It provides step-by-step guidance to minimize data loss and restore services to a normal state quickly.

### Korean

이 문서는 SeaweedFS 클러스터 내 마스터, 볼륨, 필러 서비스 장애 발생 시의 복구 절차를 설명한다. 데이터 유실을 최소화하고 서비스를 신속하게 정상 상태로 되돌리기 위한 단계별 실행 지침을 제공한다.

## Runbook ID

`RB-DATA-LAKE-SWFS-001`

## Target Audience

- Site Reliability Engineers (SRE)
- Infrastructure Operators
- System Administrators

## When to Use

- **Master Outage**: Cluster management or volume allocation fails.
- **Volume Failure**: Data chunks are inaccessible or replication is broken.
- **Filer Corruption**: Metadata lookup or filesystem operations fail.
- **Mount Issues**: FUSE mount points become stale or unresponsive on the host.

## Diagnosis Steps

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

## Remediation Procedures

### 1. Master Server Recovery

If the master server's metadata is corrupted:

- Stop the master container.
- Restore or re-initialize the `seaweedfs-master-data` volume.
- Restart the master and verify that volume servers rejoin automatically.
- Run `weed master.reshard` if necessary to redistribute volume information.

### 2. Read-Only Mode Resolution

If volume servers switch to read-only due to space limits:

- Add new volume servers or free up space by deleting old data.
- Adjust `volumeSizeLimitMB` in master configuration if required.

### 3. FUSE Mount Restoration

If the host mount point is unresponsive:

- Restart the `seaweedfs-mount` container.
- If it fails, manually unmount the stale point on the host: `umount -l /mnt/seaweedfs`.
- Relaunch the mount container.

## Verification Steps

- [ ] `curl -s http://seaweedfs-master:9333/cluster/status | jq`: Verify all nodes are online.
- [ ] `weed filer.remote.sync`: Verify metadata synchronization if using remote storage.
- [ ] Write a test file to S3/Filer and read it back to confirm end-to-end functionality.

## Post-Mortem Tasks

- Perform Root Cause Analysis (RCA) on disk/network failures.
- Adjust monitoring thresholds and alerting rules based on findings.
- Update the documentation with any new troubleshooting patterns discovered.

## Related Documents

- **Technical Guide**: [seaweedfs.md](../../../07.guides/04-data/lake-and-object/seaweedfs.md)
- **Operations Policy**: [seaweedfs.md](../../../08.operations/04-data/lake-and-object/seaweedfs.md)
- **Infrastructure**: [seaweedfs/README.md](../../../../infra/04-data/lake-and-object/seaweedfs/README.md)
