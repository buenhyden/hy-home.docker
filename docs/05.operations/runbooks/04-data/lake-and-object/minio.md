---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/lake-and-object/minio.md -->

# MinIO Object Storage Health Runbook

> Scope: health checks, bucket bootstrap verification, evidence capture, and escalation for root-active MinIO.

---

## MinIO Object Storage Health Procedure

### Overview (KR)

이 런북은 root-active MinIO 단일 service와 `minio-create-buckets` job의 compose render, health, bucket bootstrap 상태를 확인할 때 사용한다. optional cluster node recovery, credential rotation, bucket deletion, volume restore는 이 런북의 검증된 복구 범위가 아니다.

### Purpose

`minio`와 `minio-create-buckets` 상태를 안전하게 확인하고, secret 노출 또는 destructive recovery가 필요한 경우 escalation하도록 한다.

### Canonical References

- **Spec**: [04-data spec](../../../../03.specs/04-data/spec.md)
- **Policy**: [MinIO policy](../../../policies/04-data/lake-and-object/minio.md)
- **Guide**: [MinIO guide](../../../guides/04-data/lake-and-object/minio.md)
- **Repo**: [MinIO infrastructure](../../../../../infra/04-data/lake-and-object/minio/README.md)

## When to Use

- `minio` is missing, unhealthy, or unavailable through the Traefik route.
- `minio-create-buckets` failed or bucket bootstrap needs verification.
- Object storage docs or compose references changed and need local verification evidence.
- Storage exhaustion is suspected and non-destructive evidence is needed before escalation.

## Procedure

### Checklist

- [ ] Confirm this is a health/status verification task, not bucket deletion, credential rotation, or volume restore.
- [ ] Confirm Docker Secret files exist without printing their values.
- [ ] Confirm `${DEFAULT_DATA_DIR}/minio/data-1` is the approved runtime data location.
- [ ] Confirm optional cluster compose is out of scope unless explicitly named in the task.

### Steps

1. Render the current root-active compose configuration.

   ```bash
   docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage config
   ```

2. Check service status.

   ```bash
   docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage ps minio minio-create-buckets
   ```

3. Inspect logs if a service is unhealthy. Do not copy secret values into evidence.

   ```bash
   docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage logs minio minio-create-buckets
   ```

4. Check liveness from inside the compose network boundary.

   ```bash
   docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage exec minio curl -f "http://localhost:${MINIO_PORT:-9000}/minio/health/live"
   ```

5. Re-run bucket bootstrap only when explicitly required and after confirming secrets are ready.

   ```bash
   docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage run --rm minio-create-buckets
   ```

### Verification Steps

- `docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage config`
- `docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage ps`
- Expected result: compose renders, `minio` is present, bootstrap job state is recorded, and no secret values are captured.

### Observability and Evidence Sources

- **Logs**: `docker compose -f infra/04-data/lake-and-object/minio/docker-compose.yml --profile storage logs ...`
- **Health**: MinIO `/minio/health/live` endpoint
- **Routes**: Traefik labels for `minio.${DEFAULT_URL}` and `minio-console.${DEFAULT_URL}`
- **Evidence to Capture**: command names, timestamps, service status summary, liveness result, bootstrap result if run, and skipped destructive actions

### Safe Rollback or Recovery Procedure

1. For documentation-only changes, revert the last documentation diff and rerun validation.
2. For bucket bootstrap failure, preserve logs and escalate; do not delete buckets or rotate credentials from this runbook.
3. For suspected secret exposure, stop copying output and escalate under `## Escalation`.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop using commands that reveal secret-bearing output when exposure risk appears.
- **Eval Re-run**: Re-run linked validation scripts after documentation remediation.

## Evidence

- Record the compose command executed, service status, liveness result, bootstrap outcome if applicable, and any destructive action that was intentionally skipped.
- Attach failed validation output or service symptoms to the related task or incident evidence without copying secret values.

## Rollback or Recovery

N/A - no verified destructive rollback or data recovery procedure is documented in this runbook. If bucket deletion, volume restore, optional cluster recovery, or credential rotation is required, stop and escalate with captured evidence.

## Escalation

Escalate to the owning operator when compose render fails, required secrets are missing, service health remains failed after documented checks, bucket bootstrap fails, secret exposure risk appears, or destructive object/credential/storage changes are required.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/lake-and-object/minio.md)
- [Operations policy](../../../policies/04-data/lake-and-object/minio.md)
- [Infrastructure service README](../../../../../infra/04-data/lake-and-object/minio/README.md)
