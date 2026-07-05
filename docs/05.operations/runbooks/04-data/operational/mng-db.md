---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/operational/mng-db.md -->

# Management Database Health and Init Runbook

> Scope: health checks, init-job rerun, evidence capture, and escalation for `mng-db`.

---

## Management Database Health and Init Procedure

### Overview

이 런북은 `mng-db`의 compose render, 서비스 상태, PostgreSQL readiness, Valkey readiness, `mng-pg-init` 재실행을 즉시 점검해야 할 때 사용한다. 파괴적 데이터 복구나 HA failover 절차는 이 런북의 범위가 아니다.

### Purpose

관리용 PostgreSQL/Valkey가 unhealthy 상태이거나 신규 관리 서비스 DB/role 동기화가 필요한 상황에서, 안전한 확인 절차와 증거 수집 기준을 제공한다.

### Canonical References

- **Spec**: [04-data spec](../../../../03.specs/004-data/spec.md)
- **Policy**: [Management Database policy](../../../policies/04-data/operational/mng-db.md)
- **Guide**: [Management Database guide](../../../guides/04-data/operational/mng-db.md)
- **Repo**: [mng-db infrastructure](../../../../../infra/04-data/operational/mng-db/README.md)

## When to Use

- `mng-pg`, `mng-valkey`, or exporter services are missing or unhealthy.
- A new management service database/role must be synchronized through `mng-pg-init`.
- Linked operations docs or compose references were changed and need local verification evidence.
- Secret exposure risk or destructive data recovery is not required.

## Procedure

### Checklist

- [ ] Confirm the task or incident scope and record the reason for running this procedure.
- [ ] Confirm Docker Secret files exist for the compose secret refs without printing their values.
- [ ] Confirm `DEFAULT_MANAGEMENT_DIR` points to the approved runtime data location.
- [ ] Confirm the operation is not a destructive restore, volume deletion, or credential disclosure task.

### Steps

1. Render the current compose configuration.

   ```bash
   docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng config
   ```

2. Check service status.

   ```bash
   docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng ps mng-pg mng-valkey mng-pg-exporter mng-valkey-exporter
   ```

3. Inspect relevant logs if a service is unhealthy. Do not copy secret values into evidence.

   ```bash
   docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng logs mng-pg mng-valkey mng-pg-init
   ```

4. Re-run the initialization job only when database/role synchronization is required.

   ```bash
   docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng run --rm mng-pg-init
   ```

5. Capture a final status snapshot.

   ```bash
   docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng ps
   ```

### Verification Steps

- `docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng config`
- `docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng ps`
- Expected result: compose renders, `mng-pg` and `mng-valkey` are present, and the init job completes when explicitly run.

### Observability and Evidence Sources

- **Logs**: `docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng logs ...`
- **Health**: compose `ps` status for `mng-pg`, `mng-valkey`, and exporters
- **Config**: compose render output without secret values
- **Evidence to Capture**: command names, timestamps, service status summary, failure symptoms, and whether `mng-pg-init` was run

### Safe Rollback or Recovery Procedure

1. For documentation-only changes, revert the last documentation diff and rerun the validation commands.
2. For an init-job failure, stop further changes, preserve logs, and escalate; do not delete volumes or restore databases from this runbook.
3. For suspected credential exposure, stop reading secret-bearing output and escalate under `## Escalation`.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop using commands that reveal secret-bearing output when exposure risk appears.
- **Eval Re-run**: Re-run the linked validation scripts after documentation remediation.

## Evidence

- Record the compose command executed, final service status, init-job result if applicable, and any skipped destructive action.
- Attach failed validation output or service symptoms to the related task or incident evidence without copying secret values.

## Rollback or Recovery

N/A — no verified destructive rollback or data recovery procedure is documented in this runbook. If volume restore, credential rotation, or database repair is required, stop and escalate with the captured evidence.

## Escalation

Escalate to the owning operator when compose render fails, required secrets are missing, services remain unhealthy after the documented checks, secret exposure risk appears, or destructive data recovery is required.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/operational/mng-db.md)
- [Operations policy](../../../policies/04-data/operational/mng-db.md)
- [Infrastructure service README](../../../../../infra/04-data/operational/mng-db/README.md)
