---
name: incident-response
description: >
  Docker infrastructure incident response playbook. Use for service outages, SLO breaches,
  secret exposure, container crashes, and operational incidents. Follow timeline
  reconstruction, RCA, recovery planning, and MTTD/MTTR measurement.
---

# incident-response

Docker-specific incident response workflow. Reconstruct the timeline first, then perform
evidence-based RCA and recovery planning.

## Severity Classification

| SEV | Criteria | Response SLA | Postmortem |
| --- | --- | --- | --- |
| SEV1 | Full outage or secret exposure | Immediate | Within 24h |
| SEV2 | Core feature failure or SLO breach | 30 minutes | Within 72h |
| SEV3 | Partial degradation or warning breach | 4 hours | Optional |

## Phase 1 — Detect and Classify

```bash
docker compose ps
docker compose logs --tail=100 <service>
docker network inspect infra_net
```

Create an incident record immediately at `docs/10.incidents/INC-<YYYYMMDD>-<seq>.md`.

## Phase 2 — Timeline Reconstruction

Use the LGTM stack in this order:

1. Loki
2. Grafana
3. Tempo
4. Mimir or Prometheus

Timeline format:

```text
HH:MM:SS | Event | Source
```

## Phase 3 — Immediate Mitigation

```bash
docker compose restart <service>
docker compose ps <service>
docker compose logs --tail=20 <service>
```

If restart fails, follow the relevant runbook under `docs/09.runbooks/`.
If secret exposure is suspected, halt and escalate to `security-auditor`.

## Phase 4 — Root Cause Analysis

Use this structure:

```text
Symptom:
Root cause:
Contributing factors:
Detection delay:
```

- No speculation.
- Keep the analysis blameless and evidence-based.

## Phase 5 — Recovery and Verification

```bash
bash scripts/validate-docker-compose.sh
docker compose up -d <service>
docker compose ps
```

Confirm the service returns to the workspace SLO baseline.

## Phase 6 — Postmortem

For SEV1 and SEV2 incidents, create `docs/11.postmortems/PM-<INC-ID>.md`.
Include the incident link in `## Related Documents`.

## Error Handling

| Situation | Action |
| --- | --- |
| No runbook exists | Apply temporary mitigation and record the gap |
| Logs unavailable | Record a timeline gap and avoid speculation |
| Recurring incident | Escalate severity and continue RCA |

## Related Documents

- `docs/00.agent-governance/scopes/ops.md`
- `docs/00.agent-governance/rules/postflight-checklist.md`
- `docs/09.runbooks/`
- `docs/10.incidents/`
- `docs/11.postmortems/`
- `.claude/agents/incident-responder.md`
