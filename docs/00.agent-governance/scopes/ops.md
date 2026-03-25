---
layer: ops
title: 'Operations & SRE Scope'
---

# Operations & SRE Scope

**Monitoring, alerting, incident response, and environment reliability standards.**

## 1. Context & Objective

- **Goal**: Minimize MTTR (Mean Time To Recovery) and maximize system availability.
- **Stack**: **LGTM** (Loki, Grafana, Tempo, Mimir/Prometheus) stack.

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
