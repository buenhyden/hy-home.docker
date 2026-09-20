---
title: "Supabase Stack Health Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0029"
parent_ids:
- "GDE-0029"
created: "2026-05-17"
---

# Supabase Stack Health Runbook

> Scope: health checks, access verification, evidence capture, and escalation for the Supabase data profile stack.

---

## Overview

이 런북은 health triage와 별도 승인 후 수행할 coherent Supabase backup의 격리 복원 rehearsal 계약을 제공한다. 아래 database/storage/config 복원은 이번 문서 변경에서 실행하지 않았다.

### Purpose

Supabase data profile stack의 compose render, 서비스 상태, Kong 접근 경로, 주요 로그를 안전하게 확인하고, secret 노출이나 destructive recovery가 필요한 경우 빠르게 escalation하도록 한다.

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
   docker compose --profile supabase config --quiet
   ```

2. Check service status.

   ```bash
   docker compose --profile supabase ps studio kong auth rest realtime storage db analytics supavisor
   ```

3. Inspect relevant service logs. Do not copy secret values into evidence.

   ```bash
   docker compose --profile supabase logs kong auth rest storage db analytics supavisor
   ```

4. Verify the public Kong access path declared by compose.

   ```bash
   curl -fsS "http://localhost:${SUPABASE_KONG_HTTP_HOST_PORT:-8000}/" >/dev/null
   ```

5. If dashboard access is being checked, use the approved Kong/stack route. Do not assume a direct Studio local host port; the current compose file does not publish Studio directly.

6. Capture a final status snapshot.

   ```bash
   docker compose --profile supabase ps
   ```

### Verification Steps

- `docker compose --profile supabase config --quiet`
- `docker compose --profile supabase ps`
- Expected result: compose renders, services are present, Kong route status is recorded, and no secret values are captured.

### Observability and Evidence Sources

- **Logs**: `docker compose --profile supabase logs ...`
- **Health**: compose `ps` status for the Supabase service set
- **Access**: Kong HTTP/HTTPS host-port checks using compose variables
- **Evidence to Capture**: command names, timestamps, service status summary, Kong route result, skipped destructive actions

### Safe Rollback or Recovery Procedure

1. For documentation-only changes, revert the last documentation diff and rerun validation.
2. For unhealthy services after the documented checks, preserve logs and escalate; do not delete database or storage volumes from this runbook.
3. For suspected secret exposure, stop copying output, preserve minimal context, and escalate under `## Escalation`.

### Planned Isolated Restore Rehearsal

1. 사전 승인 후 Compose image declarations, PostgreSQL version/extensions, roles and databases, Storage buckets/object counts, mounted config/functions, Auth providers, JWT issuer expectations와 free capacity를 inventory한다. secret values는 manifest에 넣지 않는다.
2. PostgreSQL globals/roles, schema and data를 protected logical artifacts로 export하고 checksum한다. Storage metadata tables와 `${DEFAULT_DATA_DIR}/supabase/storage` object files는 같은 recovery point로 보존한다. Kong, functions, pooler, DB init and analytics/vector config는 별도 configuration artifact로 보존한다.
3. JWT, anon/service-role keys, SMTP/provider credentials, database passwords, vault and crypto keys는 backup data와 분리된 approved secret store에서 동일 identifier/version으로 참조한다.
4. production network, ports and volumes를 공유하지 않는 compatible empty stack을 별도 test credentials로 준비한다. roles/globals, schema, data 순서로 PostgreSQL을 복원하고 Storage objects와 metadata를 함께 배치한 후 mounted configuration을 적용한다.
5. Kong API, Auth signup/login policy, REST read, Realtime subscription, Storage object read, Function invocation, Studio metadata, analytics ingestion과 Supavisor connection을 synthetic data로 확인한다. object-count/metadata mismatch나 missing key가 있으면 승격하지 않는다.
6. 실패 시 isolated stack과 전용 volumes를 폐기한다. production cutover, DNS/route switch, secret rotation은 별도 승인 절차이며 source stack은 변경하지 않는다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop using commands that reveal secret-bearing output when exposure risk appears.
- **Eval Re-run**: Re-run linked validation scripts after documentation remediation.

## Evidence

- Record the compose command executed, service status, Kong route result, and any reason destructive recovery or credential rotation was skipped.
- Attach failed validation output or service symptoms to the related task or incident evidence without copying secret values.

## Rollback or Recovery

데이터 복구는 위 planned isolated rehearsal로만 검증한다. 이 변경에서는 backup/restore, storage mutation, JWT rotation이나 credential reset을 실행하지 않았다.

## Escalation

Escalate to the owning operator when compose render fails, required secrets or mounted configs are missing, services remain unhealthy after documented checks, Kong access remains unavailable, secret exposure risk appears, or destructive database/storage/credential changes are required.

## Traceability

- Declared parent: [Supabase Usage Guide](guide.md) (`GDE-0029`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0029`), [Policy](policy.md) (`POL-0029`)

## Related Documents

- [Compose implementation: infra/04-data/operational/supabase/docker-compose.yml](../../../../../infra/04-data/operational/supabase/docker-compose.yml)

- [Supabase self-hosted restore guidance](https://supabase.com/docs/guides/self-hosting/restore-from-platform)
- [Supabase self-hosted update guidance](https://supabase.com/docs/guides/self-hosting/updating)
- [Supabase source and licenses](https://github.com/supabase/supabase)

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
- [Infrastructure service README](../../../../../infra/04-data/operational/supabase/README.md)
