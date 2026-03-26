# Airflow Worker Recovery Runbook

: Airflow / Workflow Tier

---

## Overview (KR)

이 런북은 응답하지 않거나 'stuck' 상태인 Airflow Worker를 복구하는 절차를 정의합니다. Celery 브로커 상태 확인 및 워커 재시작 단계를 제공합니다.

## Purpose

To resolve issues where Airflow tasks remain in `queued` or `running` state indefinitely due to worker failure or broker congestion.

## When to Use

- Tasks are stuck in `queued` for > 15 minutes.
- `airflow-worker` container is healthy but not picking up tasks.
- `flower` UI shows workers as "Offline".

## Procedure or Checklist

### Procedure

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

## Verification Steps

- [ ] Check Airflow UI "Celery" tab for active worker heartbeats.
- [ ] Trigger a test DAG and verify task completion.

## Related Operational Documents

- **Operation**: [Resource Allocation Policy](../../08.operations/07-workflow/02.resource-allocation.md)
- **Guide**: [Airflow CLI Guide](../../07.guides/07-workflow/airflow-cli.md)
