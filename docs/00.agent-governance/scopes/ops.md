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
3. **Recover**: Create and maintain runbooks in `docs/09.runbooks/`.

## 4. Operational Procedures

- **Incident Response**: Follow the `docs/10.incidents/` protocol for live tracking.
- **Post-mortems**: Mandatory retrospective in `docs/11.postmortems/` for any SEV1/SEV2 incident.

## 5. Maintenance & Safety

- **Backups**: Verified daily off-site backups for `04-data` volumes.
- **Drills**: Periodically perform disaster recovery drills (Chaos Engineering).

## 6. File Ownership SSOT

| Path Pattern              | Owner Agent          | Read-Only For                |
| ------------------------- | -------------------- | ---------------------------- |
| `docs/09.runbooks/`       | `incident-responder` | all other agents             |
| `docs/10.incidents/`      | `incident-responder` | `security-auditor` (read)    |
| `docs/11.postmortems/`    | `incident-responder` | `doc-writer` (template fill) |
| `infra/06-observability/` | `incident-responder` | read-only for others         |

## 7. Subagent Bridge

```text
# incident-responder agent preamble
@import docs/00.agent-governance/scopes/ops.md
# H100:25 Postmortem pattern — timeline → RCA → remediation
# MTTR target · LGTM stack · SEV1/SEV2 mandatory postmortem
```

Spawn via Task tool. Do not embed ops policy inline in agent files.
