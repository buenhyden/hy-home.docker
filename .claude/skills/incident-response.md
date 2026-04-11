---
name: incident-response
description: >
  Docker infrastructure incident response playbook. Use for service outages, SLO breaches,
  secret exposure, container crashes, and all infra incidents.
  Follow timeline reconstruction → RCA → recovery plan, and measure MTTD/MTTR.
---

# incident-response

Docker-specific incident response playbook. Timeline first → evidence-based RCA → MTTD/MTTR tracking.
Orchestration skill for the `incident-responder` agent.

## Severity Classification

| SEV  | Criteria                               | Response SLA | Postmortem |
| ---- | -------------------------------------- | ------------ | ---------- |
| SEV1 | Full outage / secret exposure          | Immediate    | within 24h |
| SEV2 | Core feature failure / SLO breach      | 30 minutes   | within 72h |
| SEV3 | Partial degradation / warning breach   | 4 hours      | Optional   |

## Phase 1 — Detect and Classify

```bash
# Check overall service status
docker compose ps

# Collect logs from unhealthy containers
docker compose logs --tail=100 <service> 2>&1 | tee _workspace/incident_logs_$(date +%Y%m%d_%H%M).txt

# Inspect network connectivity
docker network inspect infra_net
```

Create incident record immediately: `docs/10.incidents/INC-<YYYYMMDD>-<seq>.md`

## Phase 2 — Timeline Reconstruction

LGTM stack lookup order:

1. **Loki** — collect 30 minutes of logs before incident
2. **Grafana** — snapshot dashboards for the time window
3. **Tempo** — collect error trace IDs
4. **Mimir/Prometheus** — identify metric anomalies

Timeline format:

```text
HH:MM:SS | Event | Source (log/metric/trace)
```

## Phase 3 — Immediate Mitigation (SEV1/SEV2)

```bash
# Attempt service restart
docker compose restart <service>

# Re-check status
docker compose ps <service>
docker compose logs --tail=20 <service>
```

If restart fails → consult runbook: `docs/09.runbooks/<service>.md`

If secret exposure is suspected:

- **HALT** and escalate to `security-auditor`
- Consider stopping the service until secrets are isolated

## Phase 4 — Root Cause Analysis (RCA)

RCA structure:

```text
Symptom: [observed behavior]
Root cause: [why it happened — 5-why]
Contributing factors: [compound causes]
Detection delay: [why it was detected late]
```

- No speculation — evidence only.
- Blameless: focus on system/process failures.

## Phase 5 — Recovery and Verification

```bash
bash scripts/validate-docker-compose.sh
docker compose up -d <service>
docker compose ps
```

Confirm SLO recovery: wait for `LATENCY_SLO < 200ms` to stabilize.

## Phase 6 — Postmortem (SEV1: 24h / SEV2: 72h)

Create: `docs/11.postmortems/PM-<INC-ID>.md`

Required sections:

- Timeline (Phase 2)
- RCA (Phase 4)
- Preventive actions (owner + due date)
- `## Related Documents` (include incident link)

## Error Handling

| Situation        | Action                                      |
| ---------------- | ------------------------------------------- |
| No runbook       | Apply temporary mitigation; request runbook |
| Logs unavailable | Record timeline gap; no speculation         |
| Recurrence       | Escalate to higher SEV; resume RCA          |

## References

- `docs/00.agent-governance/scopes/ops.md`
- `docs/00.agent-governance/rules/postflight-checklist.md` §1 §3
- `docs/09.runbooks/`
- `docs/10.incidents/`
- `docs/11.postmortems/`
- `.claude/agents/incident-responder.md`
