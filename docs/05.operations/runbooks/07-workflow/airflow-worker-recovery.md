---
status: active
---
<!-- Target: docs/05.operations/runbooks/07-workflow/airflow-worker-recovery.md -->

# Airflow Worker Recovery Operations

## Procedure

### Airflow Worker Recovery Procedure

> Scope: Airflow / Workflow Tier

---

#### Overview (KR)

이 런북은 응답하지 않거나 'stuck' 상태인 Airflow Worker를 복구하는 절차를 정의합니다. Celery 브로커 상태 확인 및 워커 재시작 단계를 제공합니다.

#### Purpose

To resolve issues where Airflow tasks remain in `queued` or `running` state indefinitely due to worker failure or broker congestion.

## When to Use

- Tasks are stuck in `queued` for > 15 minutes.
- `airflow-worker` container is healthy but not picking up tasks.
- `flower` UI shows workers as "Offline".

### Procedure or Checklist

#### Procedure

1. **Check Disk Space**: Ensure the log volume is not full.

   ```bash
   df -h /opt/airflow/logs
   ```

2. **Inspect Broker**: Check if Valkey is reachable and has pending messages.

   ```bash
   docker exec airflow-valkey valkey-cli info keyspace
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

- [ ] Check Airflow UI "Celery" tab for active worker heartbeats.
- [ ] Trigger a test DAG and verify task completion.

#### Related Operational Documents

- **Policy**: [DAG Deployment Policy](../../policies/07-workflow/dag-deployment.md)
- **Usage**: [Airflow System Usage](../../guides/07-workflow/airflow.md)

---

#### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

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
- [Operations template](../../../99.templates/operation.template.md)
