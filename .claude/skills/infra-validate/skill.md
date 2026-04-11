---
name: infra-validate
description: >
  Pre/post Docker Compose validation pipeline. Use for compose edits, service add/remove,
  or network, volume, and secret changes. Runs validate-docker-compose.sh, drift detection,
  SLO checks, and health verification in sequence.
---

# infra-validate

Compose validation pipeline. Execute pre-flight static validation, optional drift checks,
and post-flight health verification around infrastructure changes.

## Execution Order

```text
Pre-flight → Static validate → Drift check → Apply → Post-flight
```

### Phase 1 — Pre-flight

```bash
bash scripts/validate-docker-compose.sh
```

On failure, halt. Do not apply infra changes until the baseline is clean.

### Phase 2 — Static Validate

```bash
docker compose config --quiet
```

- Must exit `0`.
- Record warnings with file and command context.

### Phase 3 — Drift Check

Run only when the live environment is reachable:

```bash
docker compose ps --format json 2>/dev/null | python3 -c "
import json, sys
services = json.load(sys.stdin)
for service in services:
    if service.get('State') != 'running':
        print(f'DRIFT: {service[\"Name\"]} state={service[\"State\"]}')
"
```

Record drift in `_workspace/drift_<date>.md`.

### Phase 4 — Apply

- In-place edits only.
- Secrets via Docker Secrets and mounted secret files only.
- Keep inter-service traffic on `infra_net`.

### Phase 5 — Post-flight

```bash
docker compose ps
```

If any service is unhealthy, inspect logs before closing the task:

```bash
docker compose logs --tail=50 <service>
```

## SLO Checklist

- [ ] Gateway-impacting services have health checks.
- [ ] Stateful services define a restart policy.
- [ ] Every container uses `no-new-privileges: true`.
- [ ] Volume names follow `[Service]-[Data]-[Volume]`.

## Secrets Guard

If a changed file matches the pattern below, halt and escalate to `security-auditor`:

```bash
grep -nE '(password|secret|token|key)\s*[:=]\s*[A-Za-z0-9+/]{8,}' <file>
```

## Error Handling

| Situation | Action |
| --- | --- |
| Pre-flight failure | Halt, fix the baseline, rerun validation |
| Static validation warning | Record it, continue only if safe |
| Unhealthy post-flight service | Revert or repair, collect logs, escalate if unresolved |
| Secret pattern detected | Halt and request security review |

## Related Documents

- `docs/00.agent-governance/scopes/infra.md`
- `docs/00.agent-governance/rules/postflight-checklist.md`
- `.claude/agents/infra-implementer.md`
- `.claude/agents/iac-reviewer.md`
- `.claude/skills/infra-cross-validate/skill.md`
