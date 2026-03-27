# MinIO Object Storage Recovery Runbook

> MinIO Service Recovery & Emergency Restoration
> MinIO 서비스 복구 및 긴급 복원 절차.

---

## Overview

### English
This runbook defines implementation procedures for responding to failure situations in MinIO Object Storage. It provides step-by-step processes for operators to take immediate action in cases of storage exhaustion, loss of administrator credentials, and cluster node failures.

### Korean
이 런북은 MinIO 오브젝트 스토리지의 장애 상황에 대응하기 위한 실행 절차를 정의한다. 디스크 공간 부족, 관리자 자격 증명 분실, 그리고 클러스터 노드 장애 발생 시 운영자가 즉각적으로 수행할 수 있는 단계별 프로세스를 제공한다.

## Runbook ID

`RB-DATA-LAKE-MINIO-001`

## Target Audience

- Site Reliability Engineers (SRE)
- Infrastructure Operators
- Data Engineers

## When to Use

- **Storage Exhaustion**: API write failures due to lack of disk space.
- **Credential Loss**: Root user password lost or compromised.
- **Node Failure**: One or more nodes in the cluster are offline or unresponsive.
- **Service Outage**: Total service unavailability through S3 API or Console.

## Diagnosis Steps

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

## Remediation Procedures

### 1. Storage Exhaustion (디스크 공간 부족)
- Identify and delete unnecessary logs or non-critical data.
- Check and clear `tempo-bucket` or `loki-bucket` retention if applicable.
- For permanent resolution, increase the volume size in `docker-compose.yml` and redeploy.

### 2. Root Credential Reset (비밀번호 초기화)
- Verify the credentials defined in `infra/04-data/lake-and-object/minio/.env` or secrets.
- If lost, update the secret files and restart the service:
  ```bash
  docker compose restart minio
  ```
- Update the `mc` (MinIO Client) configuration to match new credentials.

### 3. Node Failure (클러스터 노드 장애)
- Identify the failed node: `docker compose ps`.
- Check logs for the specific node: `docker compose logs [node-name]`.
- Attempt restart: `docker compose start [node-name]`.
- Verify quorum and node status: `mc admin info myminio`.

## Verification Steps

- [ ] `mc admin info myminio`: Confirm cluster health and quorum status.
- [ ] `mc ls myminio`: Verify bucket and object browsing is functional.
- [ ] `curl -f http://localhost:9000/minio/health/live`: Confirm Liveness probe returns 200 OK.

## Post-Mortem Tasks

- Document the Root Cause Analysis (RCA).
- Review and update monitoring thresholds in Grafana/Prometheus.
- Record the Recovery Time Objective (RTO) achieved.

## Related Documents

- **Technical Guide**: [minio.md](../../../07.guides/04-data/lake-and-object/minio.md)
- **Operations Policy**: [minio.md](../../../08.operations/04-data/lake-and-object/minio.md)
- **Infrastructure**: [minio/README.md](../../../../infra/04-data/lake-and-object/minio/README.md)
