---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/lake-and-object/seaweedfs.md -->

# SeaweedFS Stack Health Runbook

> Scope: health checks, route verification, mount evidence capture, and escalation for SeaweedFS.

---

## SeaweedFS Stack Health Procedure

### Overview (KR)

이 런북은 SeaweedFS data-profile stack의 compose render, master/volume/filer/S3 health, mount service 상태를 확인할 때 사용한다. master metadata restore, volume deletion, forced unmount, reshard operations are not verified recovery steps in this runbook.

### Purpose

SeaweedFS 서비스 상태를 안전하게 확인하고, elevated mount behavior나 destructive recovery가 필요한 경우 escalation하도록 한다.

### Canonical References

- **Spec**: [04-data spec](../../../../03.specs/04-data/spec.md)
- **Policy**: [SeaweedFS policy](../../../policies/04-data/lake-and-object/seaweedfs.md)
- **Guide**: [SeaweedFS guide](../../../guides/04-data/lake-and-object/seaweedfs.md)
- **Repo**: [SeaweedFS infrastructure](../../../../../infra/04-data/lake-and-object/seaweedfs/README.md)

## When to Use

- `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, or `seaweedfs-s3` is missing or unhealthy.
- `seaweedfs-mount` appears stale or host mount behavior needs evidence.
- SeaweedFS route access through Traefik needs verification evidence.
- SeaweedFS docs or compose references changed and need local verification evidence.

## Procedure

### Checklist

- [ ] Confirm this is a health/status verification task, not metadata restore, forced unmount, volume deletion, or reshard work.
- [ ] Confirm host-impacting `seaweedfs-mount` behavior is in scope before restarting it.
- [ ] Confirm runtime volumes `seaweedfs-master-data` and `seaweedfs-volume-data` are preserved.
- [ ] Confirm no private data, credentials, or file contents will be copied into evidence.

### Steps

1. Render the current compose configuration.

   ```bash
   docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data config
   ```

2. Check service status.

   ```bash
   docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data ps seaweedfs-master seaweedfs-volume seaweedfs-filer seaweedfs-s3 seaweedfs-mount
   ```

3. Inspect relevant logs if a service is unhealthy.

   ```bash
   docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data logs seaweedfs-master seaweedfs-volume seaweedfs-filer seaweedfs-s3 seaweedfs-mount
   ```

4. Check master status from the service boundary.

   ```bash
   docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data exec seaweedfs-master wget -qO- "http://localhost:${SEAWEEDFS_MASTER_HTTP_PORT:-9333}/cluster/status"
   ```

5. Restart `seaweedfs-mount` only when mount evidence points to a stale mount and host-impacting scope is approved.

   ```bash
   docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data restart seaweedfs-mount
   ```

### Verification Steps

- `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data config`
- `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data ps`
- Expected result: compose renders, all expected services are present, health status and master status evidence are recorded, and destructive recovery is skipped.

### Observability and Evidence Sources

- **Logs**: `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data logs ...`
- **Health**: compose health checks for master, volume, filer, and S3
- **Routes**: Traefik labels for `seaweedfs.${DEFAULT_URL}`, `cdn.${DEFAULT_URL}`, and `s3.${DEFAULT_URL}`
- **Evidence to Capture**: command names, timestamps, service status summary, master status summary, mount restart result if approved, and skipped destructive actions

### Safe Rollback or Recovery Procedure

1. For documentation-only changes, revert the last documentation diff and rerun validation.
2. For stale mount behavior, restart only `seaweedfs-mount` after approval and preserve logs.
3. For suspected metadata or volume corruption, stop changes, preserve evidence, and escalate; do not restore, delete, reshard, or force unmount from this runbook.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop using commands that expose private file contents or credentials when exposure risk appears.
- **Eval Re-run**: Re-run linked validation scripts after documentation remediation.

## Evidence

- Record the compose command executed, service status, master status summary, mount restart result if applicable, and any destructive action that was intentionally skipped.
- Attach failed validation output or service symptoms to the related task or incident evidence without copying private file contents or credentials.

## Rollback or Recovery

N/A - no verified destructive rollback or data recovery procedure is documented in this runbook. If metadata restore, volume restore, forced unmount, reshard, or credential/security configuration changes are required, stop and escalate with captured evidence.

## Escalation

Escalate to the owning operator when compose render fails, services remain unhealthy after documented checks, master status cannot be verified, mount behavior remains stale after approved restart, private data exposure risk appears, or destructive metadata/storage changes are required.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/lake-and-object/seaweedfs.md)
- [Operations policy](../../../policies/04-data/lake-and-object/seaweedfs.md)
- [Infrastructure service README](../../../../../infra/04-data/lake-and-object/seaweedfs/README.md)
