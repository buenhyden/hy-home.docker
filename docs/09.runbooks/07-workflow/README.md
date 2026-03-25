# 07-workflow Runbooks

> Emergency recovery procedures and operational checklists for the workflow tier.

## Overview (KR)

이 폴더는 워크플로우 티어의 장애 대응 및 긴급 복구 절차를 관리합니다. Airflow 스케줄러 먹통 현상이나 n8n 큐 적체 상황 시 즉각적으로 수행해야 할 단계를 제공합니다.

## Runbook Index

### Airflow
- [Airflow Worker Recovery](./airflow-worker-recovery.md) — Steps to recover stuck or unresponsive workers.
- [Valkey Broker Cleanup](./valkey-cleanup.md) — Flushing stale tasks from the Celery broker.

### n8n
- [n8n Queue Reset](./n8n-queue-reset.md) — Clearing the Bull queue in case of runaway executions.

## Escalation

If recovery steps fail, escalate to the Infrastructure team via the `#ops-urgent` Slack channel.
