---
title: "Grafana Visualization and Dashboards"
version: "1.0.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-01-12"
---

# Grafana Visualization and Dashboards

## Overview

`infra/06-observability/grafana` contains the Grafana implementation for the `06-observability` tier. Grafana runs as compose service `grafana`, container `infra-grafana`, image [declared runtime image](../../tech-stack.versions.json), persists runtime state in `grafana-data`, mounts provisioning and dashboard trees read-only, and uses Keycloak Generic OAuth role mapping for access control.

## Audience

- Developers exploring metrics, logs, traces, alerts, and profiles
- SREs maintaining datasource and dashboard provisioning
- Operators troubleshooting SSO, dashboard, and datasource failures
- AI Agents collecting redacted evidence without exposing secrets or tokens

## Scope

### In Scope

- Grafana compose service and protected route `https://grafana.${DEFAULT_URL}`
- Datasource provisioning in `provisioning/datasources/datasource.yml`
- Dashboard provisioning in `provisioning/dashboards/dashboards.yml`
- Dashboard JSON files in `dashboards/`
- Keycloak Generic OAuth role mapping and Docker Secret file references

### Out of Scope

- UI-only dashboard changes that are not exported to JSON
- Keycloak realm/client changes outside the Grafana compose boundary
- Backend telemetry storage managed by Prometheus, Loki, Tempo, or Pyroscope
- Runtime role mapping, secret, route, image, or provisioning policy changes without operations evidence

## Structure

```text
grafana/
├── dashboards/       # Provisioned dashboard JSON tree
├── provisioning/
│   ├── dashboards/   # Dashboard provider YAML
│   └── datasources/  # Datasource provisioning YAML
└── README.md         # This file
```

## Service Boundary

| Field | Evidence |
| --- | --- |
| Purpose | Visualization hub for metrics, logs, traces, alerts, and profiles in the `06-observability` tier |
| Compose service | `grafana` in `infra/06-observability/docker-compose.yml` |
| Compose linkage | Declared in `infra/06-observability/docker-compose.yml` |
| Container | `infra-grafana` |
| Image | [declared runtime image](../../tech-stack.versions.json) |
| Config files | `provisioning/datasources/datasource.yml`, `provisioning/dashboards/dashboards.yml`, dashboard JSON files |
| Config values | Datasource UIDs `Prometheus`, `Loki`, `Tempo`, `alertmanager`; Pyroscope datasource type `grafana-pyroscope-datasource`; dashboard providers `editable: false`; role mapping for `/admins` and `/editors` |
| Volumes | `./grafana/provisioning:/etc/grafana/provisioning:ro`, `./grafana/dashboards:/etc/grafana/dashboards:ro`, `grafana-data:/var/lib/grafana:rw` |
| Secret refs | `grafana_admin_password`, `grafana_client_secret` |
| Networks | `edge_net`, `obs_net` |
| Ports | `traefik.http.services.grafana-svc.loadbalancer.server.port: ${GRAFANA_PORT:-3000}` |
| Labels | `traefik.http.routers.grafana.*`, `traefik.http.routers.grafana-static.*`, `traefik.http.services.grafana-svc.*` |
| Healthcheck | `http://localhost:${GRAFANA_PORT:-3000}/api/health` |
| Operations | Guide (`docs/05.operations/guides/0041-grafana.md`), Policy (`docs/05.operations/policies/0041-grafana.md`), Runbook (`docs/05.operations/runbooks/0041-grafana.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh), [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Start with the linked runbook, compose config rendering, service logs, healthcheck, and redacted OAuth/datasource evidence |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile obs up -d grafana` | Start Grafana from the repository root |
| `docker compose --profile obs restart grafana` | Restart Grafana after approved provisioning, dashboard, or secret-reference changes |
| `docker compose --profile obs logs -f grafana` | Tail Grafana logs from the repository root |

## Configuration

### Datasources

- **Prometheus**: `uid: Prometheus`, URL `http://prometheus:9090`
- **Loki**: `uid: Loki`, URL `http://loki:3100`
- **Tempo**: `uid: Tempo`, URL `http://tempo:3200`, `tracesToLogsV2` links to `Loki`
- **Alertmanager**: `uid: alertmanager`, URL `http://alertmanager:9093`
- **Pyroscope**: datasource type `grafana-pyroscope-datasource`, URL `http://pyroscope:4040`

### Dashboards and Access

- Dashboard providers mount JSON files from `/etc/grafana/dashboards/*`.
- Provider `editable: false` keeps dashboards code-owned.
- Current dashboard inventory is 63 tracked JSON files.
- Keycloak groups `/admins` and `/editors` map to Grafana `Admin` and `Editor`; other authenticated users default to `Viewer`.
- `grafana_admin_password` and `grafana_client_secret` are injected through Docker Secret file references.

## How to Work in This Area

1. Follow the Grafana guide (`docs/05.operations/guides/0041-grafana.md`) for usage and provisioning context.
2. Follow the Grafana runbook (`docs/05.operations/runbooks/0041-grafana.md`) for readiness, SSO, datasource, dashboard provisioning, restart, and rollback steps.
3. Keep admin passwords, OAuth client secrets, tokens, and rendered secret values out of docs, logs, task evidence, and commit messages.
4. Do not change role mapping, datasource UIDs, dashboard provider locks, secret references, image version, or route middleware without plan/task evidence and rollback notes.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking infrastructure documentation ready.
- Verify readiness with `docker compose --profile obs ps grafana` and `docker exec infra-grafana wget -q --spider http://localhost:3000/api/health`.
- Verify datasource provisioning with `rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml`.
- Verify dashboard provisioning with `rg -n 'folder:|editable: false|path: /etc/grafana/dashboards' infra/06-observability/grafana/provisioning/dashboards/dashboards.yml`.
- Verify dashboard inventory with `find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l`.

## Troubleshooting

- Start with `docker compose --profile obs config --quiet` to confirm network, volume, secret, environment, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For SSO failures, inspect redacted OAuth/role mapping logs and confirm `/admins` or `/editors` group membership separately.
- For datasource errors, confirm the datasource UID and backend endpoint in provisioning YAML.
- For dashboard loading errors, validate dashboard provider paths and dashboard JSON files.

### Convergence contract

- Classification: **HOME**. Exact profiles: `obs`, `obs-core`, `dev`, `logs`, `tracing`, `profiling`, `alerting`, `batch-metrics`.
- Source authority: `infra/06-observability/docker-compose.yml` plus this package's tracked config/build inputs; image declarations are authoritative and `infra/tech-stack.versions.json` is derived.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d grafana`.
- The stable entry point is [docs/README.md](../../../docs/README.md). Exact Stage 05 path: `docs/05.operations/guides/0041-grafana.md`; IDs `GDE-0041`, `POL-0041`, `RUN-0041`.
- Follow that runbook's planned isolated recovery. It is unexecuted unless dated evidence says otherwise; do not mutate live state from this README.

## Related Documents

- [infra/README.md](../../README.md)
- Operations index (`docs/05.operations/README.md`)
- Grafana guide (`docs/05.operations/guides/0041-grafana.md`)
- Grafana policy (`docs/05.operations/policies/0041-grafana.md`)
- Grafana runbook (`docs/05.operations/runbooks/0041-grafana.md`)
- [Documentation index](../../../docs/README.md)

Runtime pins are owned by the Compose/Dockerfile declarations; the [derived Compose image projection](../../tech-stack.versions.json) provides drift verification.
