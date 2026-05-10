# SeaweedFS Operations Policy

> Governance and operational standards for SeaweedFS distributed storage.
> SeaweedFS 분산 스토리지 거버넌스 및 운영 표준.

---

## Overview

### English

This document defines the operational policies and guidelines to ensure the stability of SeaweedFS. It covers data integrity protection, performance monitoring, backup, and security governance, providing core operational standards for SeaweedFS in the `hy-home.docker` data layer.

### Korean

이 문서는 SeaweedFS의 안정성을 보장하기 위한 운영 정책과 가이드라인을 정의한다. 데이터 무결성 보호, 성능 모니터링, 백업 및 보안 거버넌스를 아우르며, `hy-home.docker` 데이터 레이어의 핵심 운영 기준을 제시한다.

## Policy ID

`OP-DATA-LAKE-SWFS-001`

## Scope

- Management of Master, Volume, Filer, S3, and Mount services.
- Data lifecycle management for the Data Lake assets.
- Governance of `/mnt/seaweedfs` mount points and FUSE interactions.

## Controls & Standards

- **Metadata Integrity**: Filer metadata persistence must be ensured through regular backups (LevelDB/PostgreSQL).
- **Volume Replication**: Minimum replication level of `001` (2 copies in the same DC) is mandatory for production data.
- **Concurrency Control**: Monitor `GOMAXPROCS` and memory usage of the Filer during heavy I/O to prevent bottlenecks.
- **Network Security**: S3 port exposure is restricted to the internal `infra_net`. Remote access requires `security.toml` JWT authentication.

## Monitoring & Alerting

- **Master Status**: Track cluster health via `http://seaweedfs-master:9333/cluster/status`. Alert if free space falls below 20%.
- **Latency**: Alert if individual volume server response time exceeds 500ms.
- **Mount Health**: Monitor FUSE mount container CPU/Memory. Restart container if the mount point becomes stale.

## Backup & Lifecycle

- **Volume Export**: Use `weed export` for periodic archival of volume data to cold storage.
- **Filer Snapshot**: Daily snapshots of the Filer database and metadata volume (`seaweedfs-master-data`).
- **TTL Policies**: Use SeaweedFS TTL features to manage the expiration of log files and temporary artifacts.

## Compliance Requirements

- **Access Audit**: Retain Filer and S3 access logs for at least 90 days.
- **Encryption**: Use SSL/TLS for all S3 interface traffic in staging and production.

## Related Documents

- **Technical Usage**: [seaweedfs.md](./seaweedfs.md)
- **Recovery Procedure**: [seaweedfs.md](./seaweedfs.md)
- **Infrastructure**: [seaweedfs/README.md](../../../../../infra/04-data/lake-and-object/seaweedfs/README.md)

---

## Overview (KR)

이 문서는 `docs/05.operations/04-data/lake-and-object/seaweedfs.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/04-data/lake-and-object/seaweedfs.md` during the 2026-05-10 operations taxonomy consolidation.

### SeaweedFS Storage Usage

> High-performance distributed storage with S3 and FUSE interfaces.

---

#### Overview (KR)

이 문서는 SeaweedFS 분산 스케일아웃 스토리지에 대한 기술 가이드를 제공한다. SeaweedFS는 메타데이터와 실제 데이터를 분리하여 관리함으로써 수십억 개의 파일에 대한 저지연 접근을 보장한다. `hy-home.docker` 환경에서의 연결 방법, 인터페이스 활용법 및 성능 최적화 방안을 설명한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- DevOps Engineer
- Data Engineer

#### Purpose

사용자가 SeaweedFS의 다양한 인터페이스(S3, Filer API, FUSE)를 목적에 맞게 선택하고 연동할 수 있도록 돕는다.

#### Prerequisites

- `infra/04-data/lake-and-object/seaweedfs` 서비스가 실행 중이어야 함.
- S3 SDK 또는 WebDAV/Filer API 호출을 위한 `curl`, `mc` 툴 필요.

#### Step-by-step Instructions

##### 1. S3 API 활용 (Using S3 API)

MinIO와 동일한 S3 호환 API를 제공한다.

- **Endpoint**: `https://s3.${DEFAULT_URL}`
- **Bucket 생성**: `mc mb myseaweed/bucket-name`

##### 2. Filer API (CDN) 활용 (Using Filer API)

파일시스템 수준의 정적 자원 서빙에 최적화되어 있다.

- **Endpoint**: `https://cdn.${DEFAULT_URL}`
- **파일 업로드 예시**:

  ```bash
  curl -F file=@picture.jpg http://seaweedfs-filer:8888/path/to/save/
  ```

##### 3. FUSE 호스트 마운트 (FUSE Host Mount)

컨테이너 외부 호스트 환경에서 SeaweedFS를 로컬 디렉토리처럼 사용할 수 있다.

- **Mount Point**: `/mnt/seaweedfs`
- **사용 사례**: 대용량 로그 분석, 미디어 파일 직접 편집 등.

##### 4. 클러스터 모니터링 (Cluster Monitoring)

Master UI를 통해 볼륨 서버 상태와 복제 상태를 확인한다.

- **Dashboard**: `https://seaweedfs.${DEFAULT_URL}`

#### Common Pitfalls

- **Volume Size Limit**: 볼륨 파일 하나가 가득 차면 자동으로 새로운 볼륨이 할당되지만, 마스터 서버에서 이를 확인하지 못할 경우 쓰기 장애가 발생할 수 있다.
- **Filer Persistence**: Filer의 메타데이터는 Cassandra, MySQL, Redis 등 외부 DB에 저장할 수 있다. 기본 설정은 Filer 내장 LevelDB를 사용하므로 데이터 유실에 주의해야 한다.

#### Related Documents

- **Spec**: [Data Persistence Spec](../../../../03.specs/04-data/spec.md)
- **Operation**: [SeaweedFS Operations Policy](./seaweedfs.md)
- **Procedure**: [SeaweedFS Recovery Procedure](./seaweedfs.md)

## Procedure

> Migrated from `docs/05.operations/04-data/lake-and-object/seaweedfs.md` during the 2026-05-10 operations taxonomy consolidation.

### SeaweedFS Recovery Procedure

> Emergency procedures for SeaweedFS cluster restoration and troubleshooting.
> SeaweedFS 클러스터 복구 및 장애 해결을 위한 긴급 절차.

---

#### Overview

##### English

This runbook defines recovery procedures for Master, Volume, Filer, and S3 service failures within the SeaweedFS cluster. It provides step-by-step guidance to minimize data loss and restore services to a normal state quickly.

##### Korean

이 문서는 SeaweedFS 클러스터 내 마스터, 볼륨, 필러 서비스 장애 발생 시의 복구 절차를 설명한다. 데이터 유실을 최소화하고 서비스를 신속하게 정상 상태로 되돌리기 위한 단계별 실행 지침을 제공한다.

#### Procedure ID

`RB-DATA-LAKE-SWFS-001`

#### Target Audience

- Site Reliability Engineers (SRE)
- Infrastructure Operators
- System Administrators

#### When to Use

- **Master Outage**: Cluster management or volume allocation fails.
- **Volume Failure**: Data chunks are inaccessible or replication is broken.
- **Filer Corruption**: Metadata lookup or filesystem operations fail.
- **Mount Issues**: FUSE mount points become stale or unresponsive on the host.

#### Diagnosis Steps

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

#### Remediation Procedures

##### 1. Master Server Recovery

If the master server's metadata is corrupted:

- Stop the master container.
- Restore or re-initialize the `seaweedfs-master-data` volume.
- Restart the master and verify that volume servers rejoin automatically.
- Run `weed master.reshard` if necessary to redistribute volume information.

##### 2. Read-Only Mode Resolution

If volume servers switch to read-only due to space limits:

- Add new volume servers or free up space by deleting old data.
- Adjust `volumeSizeLimitMB` in master configuration if required.

##### 3. FUSE Mount Restoration

If the host mount point is unresponsive:

- Restart the `seaweedfs-mount` container.
- If it fails, manually unmount the stale point on the host: `umount -l /mnt/seaweedfs`.
- Relaunch the mount container.

#### Verification Steps

- [ ] `curl -s http://seaweedfs-master:9333/cluster/status | jq`: Verify all nodes are online.
- [ ] `weed filer.remote.sync`: Verify metadata synchronization if using remote storage.
- [ ] Write a test file to S3/Filer and read it back to confirm end-to-end functionality.

#### Post-Mortem Tasks

- Perform Root Cause Analysis (RCA) on disk/network failures.
- Adjust monitoring thresholds and alerting rules based on findings.
- Update the documentation with any new troubleshooting patterns discovered.

#### Related Documents

- **Technical Usage**: [seaweedfs.md](./seaweedfs.md)
- **Operations Policy**: [seaweedfs.md](./seaweedfs.md)
- **Infrastructure**: [seaweedfs/README.md](../../../../../infra/04-data/lake-and-object/seaweedfs/README.md)

---

#### Overview (KR)

이 런북은 `docs/05.operations/04-data/lake-and-object/seaweedfs.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

#### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

#### Canonical References

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/README.md](../../../README.md)

#### Procedure or Checklist

##### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

##### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/incidents/README.md](../../../incidents/README.md)
