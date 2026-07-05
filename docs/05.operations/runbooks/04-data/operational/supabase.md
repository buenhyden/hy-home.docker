---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/operational/supabase.md -->

# Supabase Stack Health Runbook

> Scope: health checks, access verification, evidence capture, and escalation for the Supabase data profile stack.

---

## Supabase Stack Health Procedure

### Overview

이 런북은 Supabase stack이 기동되지 않거나 Kong/API 접근, Auth, REST, Realtime, Storage, DB, pooler 상태를 즉시 확인해야 할 때 사용한다. 파괴적 DB 복구, storage 삭제, credential rotation 실행 절차는 이 런북의 범위가 아니다.

### Purpose

Supabase data profile stack의 compose render, 서비스 상태, Kong 접근 경로, 주요 로그를 안전하게 확인하고, secret 노출이나 destructive recovery가 필요한 경우 빠르게 escalation하도록 한다.

### Canonical References

- **Spec**: [04-data spec](../../../../03.specs/004-data/spec.md)
- **Policy**: [Supabase policy](../../../policies/04-data/operational/supabase.md)
- **Guide**: [Supabase guide](../../../guides/04-data/operational/supabase.md)
- **Repo**: [Supabase infrastructure](../../../../../infra/04-data/operational/supabase/README.md)
- **Compose**: [Supabase compose](../../../../../infra/04-data/operational/supabase/docker-compose.yml)

## When to Use

- `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `db`, `analytics`, or `supavisor` is unhealthy or missing.
- Kong HTTP/HTTPS access does not respond on the compose-declared host port.
- JWT rotation, dashboard password reset, storage capacity, or DB restore is being considered and needs pre-change evidence.
- Linked Supabase operations docs or compose references were changed and need local verification evidence.

## Procedure

### Checklist

- [ ] Confirm this is a health/access verification task, not destructive restore or secret rotation.
- [ ] Confirm Docker Secret files exist for the compose secret refs without printing their values.
- [ ] Confirm `${DEFAULT_DATA_DIR}/supabase/...` runtime mounts exist on the approved host.
- [ ] Confirm any generated config inspection avoids copying embedded secret values.

### Steps

1. Render the current compose configuration.

   ```bash
   docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data config
   ```

2. Check service status.

   ```bash
   docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data ps studio kong auth rest realtime storage db analytics supavisor
   ```

3. Inspect relevant service logs. Do not copy secret values into evidence.

   ```bash
   docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data logs kong auth rest storage db analytics supavisor
   ```

4. Verify the public Kong access path declared by compose.

   ```bash
   curl -fsS "http://localhost:${SUPABASE_KONG_HTTP_HOST_PORT:-8000}/" >/dev/null
   ```

5. If dashboard access is being checked, use the approved Kong/stack route. Do not assume a direct Studio local host port; the current compose file does not publish Studio directly.

6. Capture a final status snapshot.

   ```bash
   docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data ps
   ```

### Verification Steps

- `docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data config`
- `docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data ps`
- Expected result: compose renders, services are present, Kong route status is recorded, and no secret values are captured.

### Observability and Evidence Sources

- **Logs**: `docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data logs ...`
- **Health**: compose `ps` status for the Supabase service set
- **Access**: Kong HTTP/HTTPS host-port checks using compose variables
- **Evidence to Capture**: command names, timestamps, service status summary, Kong route result, skipped destructive actions

### Safe Rollback or Recovery Procedure

1. For documentation-only changes, revert the last documentation diff and rerun validation.
2. For unhealthy services after the documented checks, preserve logs and escalate; do not delete database or storage volumes from this runbook.
3. For suspected secret exposure, stop copying output, preserve minimal context, and escalate under `## Escalation`.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop using commands that reveal secret-bearing output when exposure risk appears.
- **Eval Re-run**: Re-run linked validation scripts after documentation remediation.

## Evidence

- Record the compose command executed, service status, Kong route result, and any reason destructive recovery or credential rotation was skipped.
- Attach failed validation output or service symptoms to the related task or incident evidence without copying secret values.

## Rollback or Recovery

N/A — no verified destructive rollback or data recovery procedure is documented in this runbook. If database restore, storage recovery, JWT rotation, or credential reset is required, stop and escalate with captured evidence.

## Escalation

Escalate to the owning operator when compose render fails, required secrets or mounted configs are missing, services remain unhealthy after documented checks, Kong access remains unavailable, secret exposure risk appears, or destructive database/storage/credential changes are required.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/operational/supabase.md)
- [Operations policy](../../../policies/04-data/operational/supabase.md)
- [Infrastructure service README](../../../../../infra/04-data/operational/supabase/README.md)
