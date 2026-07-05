---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/cache-and-kv/valkey-cluster.md -->

# Valkey Cluster Health Runbook

> Scope: health checks, cluster status checks, evidence capture, and escalation for the Valkey cluster.

---

## Valkey Cluster Health Procedure

### Overview

이 런북은 Valkey cluster의 compose render, 6개 노드 상태, init job, exporter 상태, cluster info를 즉시 확인해야 할 때 사용한다. 데이터 볼륨 삭제, 강제 cluster recreation, RDB/AOF restore는 이 런북의 검증된 복구 범위가 아니다.

### Purpose

`valkey-node-0..5`, `valkey-cluster-init`, `valkey-cluster-exporter`의 상태를 안전하게 확인하고, secret 노출 또는 destructive recovery가 필요한 경우 escalation하도록 한다.

### Canonical References

- **Spec**: [04-data spec](../../../../03.specs/004-data/spec.md)
- **Policy**: [Valkey Cluster policy](../../../policies/04-data/cache-and-kv/valkey-cluster.md)
- **Guide**: [Valkey Cluster guide](../../../guides/04-data/cache-and-kv/valkey-cluster.md)
- **Repo**: [Valkey Cluster infrastructure](../../../../../infra/04-data/cache-and-kv/valkey-cluster/README.md)

## When to Use

- One or more `valkey-node-*` services are missing or unhealthy.
- `valkey-cluster-init` failed or skipped cluster creation unexpectedly.
- Cluster status, slot assignment, or exporter health needs verification.
- Linked Valkey operations docs or compose references were changed and need local verification evidence.

## Procedure

### Checklist

- [ ] Confirm this is a health/status verification task, not volume deletion, forced recreation, or backup restore.
- [ ] Confirm Docker Secret file `service_valkey_password` exists without printing its value.
- [ ] Confirm `${DEFAULT_DATA_DIR}/valkey/data-0` through `data-5` are the approved runtime data locations.
- [ ] Confirm any evidence capture avoids copying secret values or full credential-bearing command output.

### Steps

1. Render the current compose configuration.

   ```bash
   docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data config
   ```

2. Check service status.

   ```bash
   docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data ps valkey-node-0 valkey-node-1 valkey-node-2 valkey-node-3 valkey-node-4 valkey-node-5 valkey-cluster-exporter
   ```

3. Inspect relevant logs if a service is unhealthy. Do not copy secret values into evidence.

   ```bash
   docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data logs valkey-node-0 valkey-node-1 valkey-node-2 valkey-node-3 valkey-node-4 valkey-node-5 valkey-cluster-init valkey-cluster-exporter
   ```

4. Check cluster state from inside the node boundary without printing the secret.

   ```bash
   docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data exec valkey-node-0 sh -c 'VALKEY_PASSWORD=$(cat /run/secrets/service_valkey_password | tr -d "\n"); valkey-cli -a "$VALKEY_PASSWORD" -p "${PORT:-6379}" cluster info | grep "^cluster_state:"'
   ```

5. Re-run the init job only when cluster creation or idempotent init verification is explicitly required.

   ```bash
   docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data run --rm valkey-cluster-init
   ```

### Verification Steps

- `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data config`
- `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data ps`
- Expected result: compose renders, six node services and exporter are present, and cluster state evidence is recorded without exposing the secret.

### Observability and Evidence Sources

- **Logs**: `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data logs ...`
- **Health**: compose `ps` status for six nodes and exporter
- **Cluster status**: `cluster info` and `cluster nodes` summaries captured from inside a node container
- **Evidence to Capture**: command names, timestamps, service status summary, cluster-state summary, init-job outcome if run, and skipped destructive actions

### Safe Rollback or Recovery Procedure

1. For documentation-only changes, revert the last documentation diff and rerun validation.
2. For an init-job failure, preserve logs and current data-volume state, then escalate; do not delete volumes or force recreate the cluster from this runbook.
3. For suspected secret exposure, stop copying output and escalate under `## Escalation`.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop using commands that reveal secret-bearing output when exposure risk appears.
- **Eval Re-run**: Re-run linked validation scripts after documentation remediation.

## Evidence

- Record the compose command executed, service status, cluster-state summary, init-job result if applicable, and any destructive action that was intentionally skipped.
- Attach failed validation output or service symptoms to the related task or incident evidence without copying secret values.

## Rollback or Recovery

N/A - no verified destructive rollback or data recovery procedure is documented in this runbook. If volume restore, forced cluster recreation, or credential rotation is required, stop and escalate with captured evidence.

## Escalation

Escalate to the owning operator when compose render fails, required secrets are missing, services remain unhealthy after documented checks, cluster state cannot be verified, secret exposure risk appears, or destructive data recovery is required.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/cache-and-kv/valkey-cluster.md)
- [Operations policy](../../../policies/04-data/cache-and-kv/valkey-cluster.md)
- [Infrastructure service README](../../../../../infra/04-data/cache-and-kv/valkey-cluster/README.md)
