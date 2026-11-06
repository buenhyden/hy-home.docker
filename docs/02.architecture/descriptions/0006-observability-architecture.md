---
title: "Observability Architecture Description"
version: "1.1.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "AD-0006"
parent_ids:
- "REQ-0007"
created: "2026-03-26"
---

# Observability Architecture Description

## Overview

`06-observability` collects, stores and shows platform telemetry so incidents
can be correlated across logs, metrics, traces and profiles. It runs Loki,
Grafana, Tempo and Prometheus with Grafana Alloy, Alertmanager, Pushgateway,
cAdvisor, node-exporter, Gatus, Pyroscope and a DCGM GPU exporter,
fully self-hosted.

## Scope

- **Owns:** centralized logs (Loki), metrics and alerting (Prometheus,
  Alertmanager), traces (Tempo), profiles (Pyroscope), dashboards (Grafana),
  telemetry collection (Alloy), availability checks (Gatus), and optional
  Docker-log inspection (Dozzle, a separate leaf).
- **Consumes:** SeaweedFS (`04-data`) S3 storage for logs and traces;
  Keycloak (`02-auth`) OIDC for Grafana, Gatus and Dozzle; `mng-pg` for
  Grafana state. Gatus keeps a local SQLite store.
- **Does not own:** application security logs (`03-security`) or business
  statistics.
- **Non-goals:** dependence on external cloud monitoring vendors.

## Structure

### Architecture

All core services are in `infra/06-observability/docker-compose.yml`; Dozzle
is in `infra/06-observability/dozzle/docker-compose.yml`. Alloy discovers
Docker logs and forwards them to Loki, receives OTLP traces and forwards them
to Tempo, and declares pprof scrape targets for Pyroscope. Prometheus scrapes
exporters, services and Alloy self-metrics directly. Grafana queries each
datasource. Traefik sends its own traces straight to Tempo.

## Runtime and Deployment

### Runtime View

- **Metrics:** cAdvisor, exporters and services -> Prometheus; Alloy
  self-metrics -> Prometheus scrape.
- **Logs:** Docker logs -> Alloy -> Loki -> SeaweedFS `loki-bucket`
  (`retention_period: 168h`).
- **Traces:** application OTLP -> Alloy -> Tempo -> SeaweedFS `tempo-bucket`.
- **Quality metrics:** k6 OTLP -> authenticated Alloy receiver
  (`config.home.alloy`) -> Prometheus remote write. A 2026-10-08 HOME canary
  passed for the named inputs (SPEC-0214, since deleted); that dated result
  does not certify later source or real application load.
- **Profiles:** declared Alloy pprof targets -> Pyroscope (local filesystem
  backend); collection success is not verified.

Prometheus keeps a local TSDB. Scrapes and datasource queries use `obs_net`,
object storage `object_net`, UI routes `edge_net`. Approved Kubernetes LAN
ingress and query exceptions stay under POL-0096.

### Deployment View

`obs` selects the full set; `obs-core` (Prometheus, Grafana), `obs-host`
(node-exporter, cAdvisor), `logs`, `tracing`, `profiling`, `alerting`,
`availability` (Gatus) and `batch-metrics` (Pushgateway) select narrower sets.
`dev` selects Prometheus, Grafana, node-exporter, cAdvisor and Gatus.
`obs-gpu` alone selects `dcgm-exporter`. Dozzle is selected by `admin` or
`admin-logs`. Prometheus, Grafana, Loki, Alloy, Tempo, Pyroscope,
node-exporter, cAdvisor, Gatus, Alertmanager and `dcgm-exporter` are HOME;
Pushgateway is OPTIONAL. Starting a HOME profile does not stop an already
running optional container.

## Quality and Risks

### Quality Attributes

- **Performance:** Alloy batches traces before export.
- **Security:** Grafana, Gatus and Dozzle use native Keycloak OIDC; the other
  UIs use ForwardAuth; the Prometheus API route uses `prometheus-api-auth@file`.
- **Reliability:** recovery covers Loki and Tempo object blocks in SeaweedFS
  together with each service's local WAL and working state.
- **Scalability:** the Prometheus local TSDB is the durable authority; the
  enabled remote-write receiver does not imply an external long-term store.
- **Observability:** the stack includes self-monitoring dashboards.

### Risks

The Tempo policy targets 24h retention, but `tempo/config/tempo.yaml` sets no
`block_retention`, so the version default (336h) applies. This gap is open.

### Evolution

A long-term metrics store or a Tempo retention setting needs a Stage 03
change.

## Related Documents

- [REQ-0007 Observability requirements](../../01.requirements/0007-observability.md)
- [ADR-0006 LGTM stack selection](../decisions/0006-lgtm-stack-selection.md)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
