# MinIO Object Storage Operations Policy

> S3-compatible object storage operations and governance.
> S3 호환 오브젝트 스토리지 운영 및 거버넌스 정책.

---

## Overview

### English

This document defines the operational policies for MinIO Object Storage. It regulates backup strategies for data persistence, security control standards, system availability maintenance, and performance monitoring methods within the `hy-home.docker` environment.

### Korean

이 문서는 MinIO 오브젝트 스토리지의 운영 정책을 정의한다. `hy-home.docker` 환경 내에서 데이터 지속성 보장을 위한 백업 전략, 보안 통제 기준, 시스템 가용성 유지 및 성능 모니터링 방법을 규정한다.

## Policy ID

`OP-DATA-LAKE-MINIO-001`

## Scope

- MinIO Cluster and Single Node data volume protection.
- Global and application-level Access Control (IAM).
- Storage quota management and monitoring thresholds.
- Manual and automated bucket lifecycle management.

## Controls & Standards

- **Secret Management**: Must use `MINIO_ROOT_USER_FILE` and `MINIO_ROOT_PASSWORD_FILE`. Direct use of plaintext credentials in environment variables is prohibited in production.
- **Monitoring**: Prometheus endpoint must be enabled and integrated with the global monitoring system (Grafana/Prometheus).
- **Data Protection**: Critical data buckets must have periodic backups enabled using `mc mirror` or server-side replication.
- **Access Control**: Follow the Principle of Least Privilege (PoLP). Application-specific service accounts must be used instead of root credentials.

## Monitoring & Alerting

- **Health Check**: Monitor `/_minio/health/live` and `/_minio/health/ready` endpoints.
- **Metrics**: Track `minio_disk_storage_used_bytes` and `minio_disk_storage_free_bytes`. Alert if free space is less than 15%.
- **Uptime**: Alert if the MinIO service is unresponsive for more than 5 minutes.

## Backup & Lifecycle

- **Volume Backup**: Nightly backups of the `/data` volume using filesystem snapshots or `mc mirror` to an offsite location.
- **Version Control**: Enable Object Locking and Versioning for critical production buckets to prevent accidental deletion.
- **Retention**: Define lifecycle rules for temporary buckets (e.g., auto-delete after 24 hours for `tmp-` prefix).

## Compliance Requirements

- **Audit Logs**: Access logs must be retained for at least 90 days for compliance auditing.
- **Encryption**: Enable Server-Side Encryption (SSE) for sensitive data buckets.
- **Public Access**: Public access remains disabled by default. Exceptions for CDN/Public assets require explicit approval.

## Related Documents

- **Technical Usage**: [minio.md](./minio.md)
- **Recovery Procedure**: [minio.md](./minio.md)
- **Infrastructure**: [minio/README.md](../../../../../infra/04-data/lake-and-object/minio/README.md)

---

## Overview (KR)

이 문서는 `docs/05.operations/04-data/lake-and-object/minio.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

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

> Migrated from `docs/05.operations/04-data/lake-and-object/minio.md` during the 2026-05-10 operations taxonomy consolidation.

### MinIO Object Storage Usage

> S3-compatible high-performance object storage server.

---

#### Overview (KR)

이 문서는 MinIO 오브젝트 스토리지에 대한 기술 가이드를 제공한다. `hy-home.docker` 환경에서 MinIO를 연결하고 사용하는 방법, 버킷 관리 절차 및 아키텍처적 통합 방안을 설명한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator

#### Purpose

이 가이드는 사용자가 MinIO 서비스를 이해하고, 애플리케이션 또는 다른 인프라 서비스와 통합하며, 기본적인 관리 작업을 수행할 수 있도록 돕는다.

#### Prerequisites

- `infra/04-data/lake-and-object/minio` 서비스가 실행 중이어야 함.
- S3 SDK (AWS SDK 등) 또는 MinIO Client (`mc`)가 설치되어야 함.

#### Step-by-step Instructions

##### 1. 연결 정보 확인 (Connection Info)

- **Internal API**: `http://minio:9000`
- **Internal Console**: `http://minio:9001`
- **External API**: `https://minio.${DEFAULT_URL}`
- **External Console**: `https://minio-console.${DEFAULT_URL}`

##### 2. 버킷 초기화 및 자동화 (Bucket Initialization)

MinIO 배포 시 `minio-create-buckets` 작업이 자동으로 실행되어 다음 버킷을 생성한다.

- `tempo-bucket`: Tempo 분산 추적 데이터 저장
- `loki-bucket`: Loki 로그 데이터 저장
- `cdn-bucket`: 공개 에셋 저장소 (Public/Anonymous Read 활성화)
- `doc-intel-assets`: 문서 지능화 작업을 위한 자산 저장소

##### 3. MinIO Client (mc) 사용 (Using mc)

원격 관리를 위해 `mc`를 설정한다.

```bash
### 별칭 설정
read -r MINIO_ACCESS_KEY
read -rsp "MinIO secret key: " MINIO_SECRET_KEY; echo
mc alias set myminio https://minio.${DEFAULT_URL} "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"
unset MINIO_SECRET_KEY

### 버킷 리스트 확인
mc ls myminio

### 데이터 복사 예시
mc cp local-file.txt myminio/cdn-bucket/
```

민감값을 명령어에 직접 적거나 문서에 남기지 않는다. 가능한 경우 승인된 secret 주입 절차를 사용한다.

##### 4. 애플리케이션 연동 (App Integration)

애플리케이션에서 AWS SDK 등을 사용하여 연결할 때는 `path-style` 접근 방식을 활성화해야 한다.

```javascript
const s3 = new AWS.S3({
  endpoint: 'http://minio:9000',
  s3ForcePathStyle: true, // 필수 설정
  signatureVersion: 'v4'
});
```

#### Common Pitfalls

- **Path-Style Access**: MinIO는 기본적으로 가상 호스트 기반 접근이 아닌 경로 기반 접근을 사용하므로 클라이언트 설정에서 반드시 활성화해야 한다.
- **Root Credentials**: `MINIO_ROOT_USER`와 `MINIO_ROOT_PASSWORD`는 서비스 배포용 비밀번호이므로, 애플리케이션 연동 시에는 별도의 IAM 사용자나 App Credentials를 사용하는 것을 권장한다.

#### Related Documents

- **Spec**: [Data Persistence Spec](../../../../03.specs/04-data/spec.md)
- **Operation**: [MinIO Operations Policy](./minio.md)
- **Procedure**: [MinIO Recovery Procedure](./minio.md)

## Procedure

> Migrated from `docs/05.operations/04-data/lake-and-object/minio.md` during the 2026-05-10 operations taxonomy consolidation.

### MinIO Object Storage Recovery Procedure

> MinIO Service Recovery & Emergency Restoration
> MinIO 서비스 복구 및 긴급 복원 절차.

---

#### Overview

##### English

This runbook defines implementation procedures for responding to failure situations in MinIO Object Storage. It provides step-by-step processes for operators to take immediate action in cases of storage exhaustion, loss of administrator credentials, and cluster node failures.

##### Korean

이 런북은 MinIO 오브젝트 스토리지의 장애 상황에 대응하기 위한 실행 절차를 정의한다. 디스크 공간 부족, 관리자 자격 증명 분실, 그리고 클러스터 노드 장애 발생 시 운영자가 즉각적으로 수행할 수 있는 단계별 프로세스를 제공한다.

#### Procedure ID

`RB-DATA-LAKE-MINIO-001`

#### Target Audience

- Site Reliability Engineers (SRE)
- Infrastructure Operators
- Data Engineers

#### When to Use

- **Storage Exhaustion**: API write failures due to lack of disk space.
- **Credential Loss**: Root user password lost or compromised.
- **Node Failure**: One or more nodes in the cluster are offline or unresponsive.
- **Service Outage**: Total service unavailability through S3 API or Console.

#### Diagnosis Steps

1. **Check Physical Storage**:

   ```bash
   df -h
   ```

2. **Analyze Bucket Usage**:

   ```bash
   mc du myminio
   ```

3. **Verify Cluster Health**:

   ```bash
   mc admin info myminio
   ```

4. **Check Service Logs**:

   ```bash
   docker compose logs --tail=100 minio
   ```

#### Remediation Procedures

##### 1. Storage Exhaustion (디스크 공간 부족)

- Identify and delete unnecessary logs or non-critical data.
- Check and clear `tempo-bucket` or `loki-bucket` retention if applicable.
- For permanent resolution, increase the volume size in `docker-compose.yml` and redeploy.

##### 2. Root Credential Reset (비밀번호 초기화)

- Verify the credentials defined in `infra/04-data/lake-and-object/minio/.env` or secrets.
- If lost, update the secret files and restart the service:

  ```bash
  docker compose restart minio
  ```

- Update the `mc` (MinIO Client) configuration to match new credentials.

##### 3. Node Failure (클러스터 노드 장애)

- Identify the failed node: `docker compose ps`.
- Check logs for the specific node: `docker compose logs [node-name]`.
- Attempt restart: `docker compose start [node-name]`.
- Verify quorum and node status: `mc admin info myminio`.

#### Verification Steps

- [ ] `mc admin info myminio`: Confirm cluster health and quorum status.
- [ ] `mc ls myminio`: Verify bucket and object browsing is functional.
- [ ] `curl -f http://localhost:9000/minio/health/live`: Confirm Liveness probe returns 200 OK.

#### Post-Mortem Tasks

- Document the Root Cause Analysis (RCA).
- Review and update monitoring thresholds in Grafana/Prometheus.
- Record the Recovery Time Objective (RTO) achieved.

#### Related Documents

- **Technical Usage**: [minio.md](./minio.md)
- **Operations Policy**: [minio.md](./minio.md)
- **Infrastructure**: [minio/README.md](../../../../../infra/04-data/lake-and-object/minio/README.md)

---

#### Overview (KR)

이 런북은 `docs/05.operations/04-data/lake-and-object/minio.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

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
