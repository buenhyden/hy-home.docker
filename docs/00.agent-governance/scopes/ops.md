---
layer: ops
title: 'Operations & SRE Scope'
---

# Operations & SRE Scope

**Monitoring, alerting, incident response, and environment reliability standards.**

## 1. Context & Objective

- **Goal**: Minimize MTTR (Mean Time To Recovery) and maximize system availability.
- **Stack**: **LGTM** (Loki, Grafana, Tempo, Mimir/Prometheus) stack.
- **Criteria**: Mandatory alignment with `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Observability**:
  - **Metrics**: Standardized Prometheus exporters for all infra services.
  - **Logging**: JSON-structured logs with correlated Trace IDs.
  - **Tracing**: End-to-end distributed tracing via Tempo.
- **Reliability**: Automated health checks and restart policies for all production containers.

## 3. Implementation Flow

1. **Monitor**: Configure dashboards in `infra/06-observability/grafana/`.
2. **Alert**: Define SLI/SLO and alert rules in Prometheus/AlertManager.
3. **Recover**: Create and maintain operations procedures in `docs/05.operations/`.

## 4. Operational Procedures

- **Incident Response**: Follow the `docs/05.operations/incidents/` protocol for live tracking.
- **Post-mortems**: Mandatory retrospective in `docs/05.operations/incidents/` for any SEV1/SEV2 incident.

## 5. Maintenance & Safety

- **Backups**: Verified daily off-site backups for `04-data` volumes.
- **Drills**: Periodically perform disaster recovery drills (Chaos Engineering).

## 6. File Ownership SSOT

| Path Pattern              | Owner Agent          | Read-Only For                |
| ------------------------- | -------------------- | ---------------------------- |
| `docs/05.operations/`       | `incident-responder` | all other agents             |
| `docs/05.operations/incidents/`      | `incident-responder` | `security-auditor` (read), `doc-writer` (template fill) |
| `infra/06-observability/` | `incident-responder` | read-only for others         |

## 7. Subagent Bridge

```text
# incident-responder agent preamble
@import docs/00.agent-governance/scopes/ops.md
# Postmortem pattern — timeline → RCA → remediation
# MTTR target · LGTM stack · SEV1/SEV2 mandatory postmortem
```

Spawn via the active runtime's delegated-agent facility. Do not embed ops policy inline in agent files.

## Related Documents

- [Agent governance hub](../README.md)
- [Bootstrap rule](../rules/bootstrap.md)
- [Persona protocol](../rules/persona.md)
- [Task checklists](../rules/task-checklists.md)
- [Agentic rule](../rules/agentic.md)
