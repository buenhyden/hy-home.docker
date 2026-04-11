---
name: infra-validate
description: >
  Pre/post Docker Compose validation pipeline. Use for compose edits, service add/remove,
  or network/volume/secret changes. Runs validate-docker-compose.sh, drift detection,
  SLO checks, and health verification in sequence.
---

# infra-validate

Compose validation pipeline. Executes pre-flight static validation → drift detection → post-flight health checks.
Shared orchestration skill for `infra-implementer` and `iac-reviewer`.

## Execution Order

```text
Pre-flight → Static validate → Apply → Post-flight → Health
```

### Phase 1 — Pre-flight (required before change)

```bash
bash scripts/validate-docker-compose.sh
```

On failure **HALT** — do not apply changes.

### Phase 2 — Static validate (compose syntax check)

```bash
docker compose config --quiet
```

- Must exit 0.
- Record warnings with file:line context.

### Phase 3 — Drift check (optional: live env only)

Run only when the live environment is reachable:

```bash
docker compose ps --format json 2>/dev/null | python3 -c "
import json, sys
services = json.load(sys.stdin)
for s in services:
    if s.get('State') != 'running':
        print(f'DRIFT: {s[\"Name\"]} state={s[\"State\"]}')
"
```

If drift is found, record it in `_workspace/drift_<date>.md`.

### Phase 4 — Apply (change execution)

- In-place edits only.
- Secrets: Docker Secrets / `secrets/` mounts only.
- Network: `infra_net` only.

### Phase 5 — Post-flight (required after change)

```bash
docker compose ps
```

Confirm all services are `running`. If any are unhealthy, inspect logs:

```bash
docker compose logs --tail=50 <service>
```

## SLO Checklist

- [ ] `LATENCY_SLO < 200ms` impact services have health-checks defined
- [ ] All stateful services have a restart policy
- [ ] `no-new-privileges: true` exists on every container
- [ ] Volume names follow `[Service]-[Data]-[Volume]`

## Secrets Guard

If the following pattern is detected in a changed file, **HALT**:

```bash
grep -nE '(password|secret|token|key)\s*[:=]\s*[A-Za-z0-9+/]{8,}' <file>
```

Escalate immediately to `security-auditor`. Do not commit.

## Error Handling

| Situation              | Action                                       |
| ---------------------- | -------------------------------------------- |
| Phase 1 failure        | HALT — fix cause, rerun                       |
| Phase 2 warning        | Record and proceed                            |
| Phase 5 unhealthy svc  | Roll back change → collect logs → escalate    |
| Secret pattern detected| HALT — invoke `security-auditor`              |

## References

- `docs/00.agent-governance/scopes/infra.md` §3 Implementation Flow
- `docs/00.agent-governance/rules/postflight-checklist.md` §1 Infrastructure Gate
- `.claude/agents/infra-implementer.md`
- `.claude/agents/iac-reviewer.md`
