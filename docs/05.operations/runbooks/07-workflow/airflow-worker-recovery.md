---
status: active
---
<!-- Target: docs/05.operations/runbooks/07-workflow/airflow-worker-recovery.md -->

# Airflow Worker Recovery Operations

## Overview (KR)

이 런북은 응답하지 않거나 `queued` 상태가 장기화된 Airflow worker를 복구하는 절차를 정의합니다. 현재 구현은 `airflow-worker`, `airflow-apiserver`, root-included dev `mng-valkey`, service-local `airflow-valkey` 경계를 기준으로 합니다.

## Procedure

### Checklist

- [ ] 현재 실행 환경이 root-included dev compose인지 service-local compose인지 식별한다.
- [ ] `airflow-worker`, `airflow-scheduler`, `airflow-apiserver` 상태와 최근 로그를 캡처한다.

### Airflow Worker Recovery Procedure

> Scope: Airflow / Workflow Tier

---

#### Purpose

To resolve issues where Airflow tasks remain in `queued` or `running` state indefinitely due to worker failure or broker congestion.

### Steps

1. `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`로 static validation을 확인한다.
2. `docker compose logs --tail=100 airflow-worker airflow-scheduler airflow-apiserver` 결과를 캡처한다.
3. Broker 상태를 확인한다.
   - root-included dev compose: `docker compose exec mng-valkey sh -lc 'valkey-cli -a "$(cat /run/secrets/mng_valkey_password)" ping'`
   - service-local compose: `docker compose exec airflow-valkey sh -lc 'valkey-cli -a "$(cat /run/secrets/airflow_valkey_password)" ping'`
4. worker만 재시작한다: `docker compose restart airflow-worker`
5. 검증 실패, secret exposure 위험, 파괴적 변경 필요 시 즉시 중단하고 `## Escalation`으로 이동한다.

### Verification Steps

- [ ] `docker compose exec airflow-apiserver airflow dags list`가 성공한다.
- [ ] Flower UI 또는 worker 로그에서 worker heartbeat가 회복된다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 runbook 범위를 벗어난 별도 승인 절차로 분리한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## When to Use

- Tasks are stuck in `queued` for > 15 minutes.
- `airflow-worker` container is healthy but not picking up tasks.
- `flower` UI shows workers as "Offline".

### Procedure or Checklist

#### Procedure

1. **Check Disk Space**: Ensure the Airflow log volume is not full.

   ```bash
   docker compose exec airflow-worker df -h /opt/airflow/logs
   ```

2. **Inspect Broker**: Check if Valkey is reachable and has pending messages.

   ```bash
   docker compose exec airflow-apiserver airflow celery inspect ping
   ```

3. **Restart Workers**: Force a restart of the worker nodes.

   ```bash
   docker compose restart airflow-worker
   ```

4. **Verify Log Streaming**: Check the logs of the restarted worker.

   ```bash
   docker compose logs -f airflow-worker
   ```

#### Verification Steps

- [ ] Check Flower for active worker heartbeats.
- [ ] Trigger a test DAG and verify task completion.

#### Related Operational Documents

- **Policy**: [DAG Deployment Policy](../../policies/07-workflow/dag-deployment.md)
- **Usage**: [Airflow System Usage](../../guides/07-workflow/airflow.md)

---

#### Canonical References

- [Operations index](../../README.md)
- [Airflow usage guide](../../guides/07-workflow/airflow.md)
- [Airflow operations policy](../../policies/07-workflow/airflow.md)

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

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Airflow usage guide](../../guides/07-workflow/airflow.md)
- [Airflow operations policy](../../policies/07-workflow/airflow.md)
