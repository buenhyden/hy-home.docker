---
status: active
---

# Loki Operational Policy Runbook

## Loki Recovery Procedure

> Critical recovery procedures for Loki logging service.

### 1. Service Health Check

Verify if Loki is healthy and ready to receive logs:

```bash
## Check readiness
wget -qO- http://loki:3100/ready

## Check service status (docker compose)
docker compose ps loki
```

### 2. Common Scenarios

#### Scenario A: "No logs found" in Grafana

**Symptoms**: Explore shows empty results despite containers running.

1. **Verify Alloy Status**: Check `https://alloy.${DEFAULT_URL}`. Ensure `loki.write` components are healthy.
2. **Check Loki Ingestion**: Look for `entry out of order` or `rate limit exceeded` errors in Loki logs:

   ```bash
   docker compose logs --tail=100 loki
   ```

3. **Verify Labels**: Ensure the LogQL query labels match exactly what Alloy is sending.

#### Scenario B: MinIO Connection Failure

**Symptoms**: Loki logs show `S3 storage: connection refused` or `access denied`.

1. **Check MinIO Status**: `docker compose ps minio`.
2. **Verify Credentials**: Ensure `MINIO_APP_USERNAME` and `minio_app_user_password` secret match the `loki-config.yaml` S3 settings.
3. **Bucket Existence**: Verify `loki-bucket` exists in MinIO UI.

#### Scenario C: Loki Ingester OOM (Out Of Memory)

**Symptoms**: `infra-loki` container restarts frequently with exit code 137.

1. **Temporary Fix**: Increase memory limit in `infra/06-observability/docker-compose.yml` if traffic has surged.

```bash
docker compose -f infra/06-observability/docker-compose.yml restart loki
```

#### 2. Check S3/MinIO Connectivity

1. **Root Cause**: Check for a specific service emitting massive log volume (log spikes).
2. **Mitigation**: Use `limits_config` in `loki-config.yaml` to throttle high-volume streams.

### 3. Emergency Maintenance

#### Force Compaction

If storage is full and retention cleanup is pending:

```bash
## Compactor runs automatically, but check for errors:
docker compose -f infra/06-observability/docker-compose.yml logs -f loki | grep "compactor"
```

#### Flush Chunks

If Loki needs to be shut down gracefully while ensuring all logs are committed to S3:

- Loki handles this automatically on `SIGTERM`. Ensure `stop_grace_period` is sufficient (min 30s).

---

- [Loki System Usage](../../guides/06-observability/loki.md)
 | [Operational Policy](../../policies/06-observability/loki.md)

---

### Overview (KR)

이 런북은 `docs/05.operations/06-observability/loki.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

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

### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

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

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/loki.md)
- [Operations policy](../../policies/06-observability/loki.md)
- [Operations template](../../../99.templates/operation.template.md)
