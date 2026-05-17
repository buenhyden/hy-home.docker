---
status: active
---

# MinIO Object Storage Runbook

## MinIO Object Storage Recovery Procedure

> MinIO Service Recovery & Emergency Restoration
> MinIO 서비스 복구 및 긴급 복원 절차.

---

### Overview

#### English

This runbook defines implementation procedures for responding to failure situations in MinIO Object Storage. It provides step-by-step processes for operators to take immediate action in cases of storage exhaustion, loss of administrator credentials, and cluster node failures.

#### Korean

이 런북은 MinIO 오브젝트 스토리지의 장애 상황에 대응하기 위한 실행 절차를 정의한다. 디스크 공간 부족, 관리자 자격 증명 분실, 그리고 클러스터 노드 장애 발생 시 운영자가 즉각적으로 수행할 수 있는 단계별 프로세스를 제공한다.

### Procedure ID

`RB-DATA-LAKE-MINIO-001`

### Target Audience

- Site Reliability Engineers (SRE)
- Infrastructure Operators
- Data Engineers

### When to Use

- **Storage Exhaustion**: API write failures due to lack of disk space.
- **Credential Loss**: Root user password lost or compromised.
- **Node Failure**: One or more nodes in the cluster are offline or unresponsive.
- **Service Outage**: Total service unavailability through S3 API or Console.

### Diagnosis Steps

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

### Remediation Procedures

#### 1. Storage Exhaustion (디스크 공간 부족)

- Identify and delete unnecessary logs or non-critical data.
- Check and clear `tempo-bucket` or `loki-bucket` retention if applicable.
- For permanent resolution, increase the volume size in `docker-compose.yml` and redeploy.

#### 2. Root Credential Reset (비밀번호 초기화)

- Verify the credentials defined in `infra/04-data/lake-and-object/minio/.env` or secrets.
- If lost, update the secret files and restart the service:

  ```bash
  docker compose restart minio
  ```

- Update the `mc` (MinIO Client) configuration to match new credentials.

#### 3. Node Failure (클러스터 노드 장애)

- Identify the failed node: `docker compose ps`.
- Check logs for the specific node: `docker compose logs [node-name]`.
- Attempt restart: `docker compose start [node-name]`.
- Verify quorum and node status: `mc admin info myminio`.

### Verification Steps

- [ ] `mc admin info myminio`: Confirm cluster health and quorum status.
- [ ] `mc ls myminio`: Verify bucket and object browsing is functional.
- [ ] `curl -f http://localhost:9000/minio/health/live`: Confirm Liveness probe returns 200 OK.

### Post-Mortem Tasks

- Document the Root Cause Analysis (RCA).
- Review and update monitoring thresholds in Grafana/Prometheus.
- Record the Recovery Time Objective (RTO) achieved.

### Overview (KR)

이 런북은 `docs/05.operations/04-data/lake-and-object/minio.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

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

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/lake-and-object/minio.md)
- [Operations policy](../../../policies/04-data/lake-and-object/minio.md)
- [Operations template](../../../../99.templates/operation.template.md)
