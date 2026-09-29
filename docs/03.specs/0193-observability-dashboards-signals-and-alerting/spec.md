---
title: "Observability Dashboards, Signals and Alerting Specification"
version: "0.4.0"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0193"
parent_ids:
- "REQ-0007"
created: "2026-09-30"
---

# Observability Dashboards, Signals and Alerting Specification

## Overview

On 2026-09-29 and 09-30 the 39 provisioned Grafana dashboards, the five
Grafana datasources, the Prometheus scrape and rule files, and the Loki,
Tempo, Pyroscope and Alloy settings were compared with the 151 Compose
services (HOME, OPTIONAL, LAB and DEV, running or stopped) and with the
series Prometheus holds. Findings:

- **Dashboards without data by design error.** Of 39 dashboards, 12 query
  metric names that no service in this repository emits: `vllm-monitoring`
  (no vLLM service), `neo4j` and `neo4j-operations` (Neo4j 5 Community has no
  metrics endpoint), `vaults` (Vault is retired; OpenBao replaced it),
  `airflow-dag`, `airflow-dag-overview` and `airflow-operators` (Airflow 2
  names), `otel-collector` (no OpenTelemetry Collector; Alloy collects),
  `loki-dashboard` (Kubernetes labels), `openbao` (job `openbao-internal`),
  and `n8n-workflow-analytics` and `airflow-monitoring` (SQL queries, but no
  PostgreSQL datasource exists).
- **Duplicated roles.** `redis-overview` and `valkey-overview` are the same
  30 metrics; `cadvisor`, `docker-metrics` and `docker-monitoring` all chart
  container resources; `postgres` and `postgres-exporter` chart one
  exporter; `loki-global` and `loki-metrics` chart Loki internals; five
  Airflow dashboards cover one statsd source.
- **Duplicated collection.** Jobs `airflow-monitor` and `airflow-exporter`
  scrape the same target, and Alloy's own metrics arrive twice (job `alloy`
  and remote-written `integrations/self`).
- **Uncollected sources.** Grafana, Pyroscope and Flower serve `/metrics`
  without a scrape job; the registry and OAuth2 Proxy have metrics switched
  off; Kafka Connect and Schema Registry have no JMX exporter. SeaweedFS
  exposes metrics from `seaweedfs-s3` only, by an earlier contract.
- **Services without a dashboard.** SeaweedFS, Gatus, Alloy, Grafana,
  Pyroscope, Flower, OAuth2 Proxy and the Kafka Connect and Schema Registry
  workers.
- **Datasources.** Prometheus `timeInterval` is 15 s against a 30 s scrape;
  there are no exemplar, trace-to-profile, trace-to-metric or log-to-trace
  links; Tempo's log link uses a `container_name` tag Loki does not carry;
  Pyroscope has no fixed UID.
- **Drilldown apps.** Metrics, Logs, Traces and Profiles Drilldown are
  installed. Pyroscope holds no profile (Alloy has a writer but no source),
  only Traefik sends traces, Tempo lacks the `local-blocks` processor that
  TraceQL metrics need, and Loki has neither the volume endpoint nor the
  pattern ingester enabled.
- **Alerting.** 26 of 78 alert rules query metric names absent from
  Prometheus. Some belong to stopped LAB services (HAProxy), but others can
  never fire: every Keycloak rule (Keycloak 26 emits different names and its
  event metrics are off), the OpenSearch rules (they use `elasticsearch_*`
  names), `TraefikServiceDown`, `N8nWorkflowFailed`, `GpuXidError` and three
  PostgreSQL rules. 28 rules have no runbook link and 43 link a directory
  README. `alert_rules.vault.yml` is named for the retired Vault.
- **Resources (SPEC-0182 W8, interim 2026-09-26 to 09-29).** Grafana peaked
  at 97% of its 512 MiB limit and `airflow-triggerer` at 91% of 256 MiB;
  OpenBao's CPU p95 reached 92% of its one-core quota during a 4.5 h spike;
  ComfyUI, Ollama, SeaweedFS volume, Loki and the n8n and Airflow servers
  stayed under 15% of their limits.

## Boundaries and Inputs

In scope: `infra/06-observability/` (Grafana dashboards and provisioning,
Prometheus scrape, alert and recording rules, Loki, Tempo, Alloy), the
metrics, tracing and resource settings of the services named in the
Behavior Contract, the related contract tests, and GDE, POL and RUN-0041,
RUN-0045 and the Grafana README.

Out of scope: the k3d cluster's own dashboards (it is not a Compose
service), eBPF profiling, enabling metrics that need a service rebuild or a
licence (Neo4j Enterprise, InfluxDB 3, Supabase, Trino, Flink, Spark, Kong,
Vector), and alert routing and receivers.

Inputs: the external-dashboard survey of 2026-09-29 (vendor repositories and
grafana.com, each matched against the metric names the pinned exporter
emits) and the owner's rulings below.

### Owner rulings (2026-09-30)

1. Add read-only PostgreSQL datasources for the n8n and Airflow databases.
2. Collect profiles by pulling `pprof` from Go services; no eBPF.
3. Turn on OTLP tracing in Keycloak, Grafana and Airflow.
4. Keep upstream mixin dashboards unmodified by adding static `cluster` and
   `namespace` labels and the mixins' recording rules.
5. Where an external dashboard exists for a service, use it.

## Behavior Contract

1. **Coverage.** Every Compose service is visualized: by the container
   dashboard (resource use by Compose service and project) and Logs
   Drilldown for all, and by one service dashboard for each service with a
   metrics source. The Grafana README lists every service with its metrics
   source and dashboard, or states that it has none and why.
2. **One role per dashboard.** No two provisioned dashboards chart the same
   source for the same purpose; the dispositions below apply.
3. **External first.** A service dashboard is the vendor's or a grafana.com
   dashboard when one matches the emitted metrics; its source and revision
   are recorded next to it. A local dashboard is kept only where none
   matches (Ollama, OAuth2 Proxy, Flower, n8n system health).
4. **Datasource identity.** Dashboards reference the provisioned UIDs
   (`Prometheus`, `Loki`, `Tempo`, `Pyroscope`, `alertmanager` and the two
   PostgreSQL UIDs) or a datasource variable; no unresolved `__inputs`.
5. **Collected once.** Each source is scraped by exactly one job; every
   available metrics endpoint in scope is scraped.
6. **Correlated signals.** Metrics link to traces by exemplar, traces to
   logs, metrics and profiles, and logs to traces by trace ID.
7. **Drilldown-ready backends.** Loki serves volume and patterns and detects
   levels; Tempo computes TraceQL metrics; Pyroscope receives profiles.
8. **Live alerting.** Each alert rule queries metrics that its source emits
   when running, links an existing runbook, and has no duplicate.
9. **Resources from measurement.** Limits named in the W8 findings are set
   from the final SPEC-0182 W8 figures, and the container-resource alerts
   use the same thresholds.

## Technical Approach

- Prometheus (both `prometheus.yml` and `prometheus.dev.yml`): merge the
  Airflow jobs; drop Alloy's self remote-write; add Grafana, Pyroscope,
  Flower, registry, OAuth2 Proxy, Kafka Connect and Schema Registry jobs and
  the on-demand LAB exporters; add `cluster="hy-home"` and
  `namespace="hy-home"` as external or target labels; add the Loki, Tempo
  and Alloy mixin recording rules.
- Services: Airflow statsd mapping rules for DAG runs, pools and task
  instances; Keycloak metrics, HTTP histograms, cache and user-event
  metrics; registry debug metrics; OAuth2 Proxy metrics address; the JMX
  agent for Connect and Schema Registry with Confluent's rule files; OTLP
  tracing in Keycloak, Grafana and Airflow at a low sampling ratio.
- Grafana datasources: `timeInterval` equal to the scrape interval,
  exemplar links to Tempo, Loki derived fields to Tempo, Tempo links to Loki
  by `service_name`, to Prometheus and to Pyroscope, a fixed Pyroscope UID,
  and two PostgreSQL datasources that read their password from a Docker
  secret through a role limited to `SELECT` on the n8n and Airflow tables.
- Backends: Loki `volume_enabled`, `pattern_ingester` and
  `discover_log_levels`; Tempo `local-blocks` with TraceQL metrics; Alloy
  `pyroscope.scrape` of the Go services' `pprof` endpoints.
- Alerting: rename or rewrite rules to emitted names, drop rules without a
  possible source, rename `alert_rules.vault.yml` for OpenBao, point every
  `runbook_url` at an existing runbook, and add rules for the new jobs.
- A contract test covers dashboard UIDs, datasource references, the
  service-to-dashboard table and the absence of duplicate jobs.

## Interfaces and Data

- Datasource UIDs: `Prometheus`, `Loki`, `Tempo`, `alertmanager`, and new
  fixed `Pyroscope`, `n8n-db` and `airflow-db`.
- New Docker secret: the Grafana reader password, generated by the owner
  through the existing secret metadata; no new `.env` key holds a value.
- New scrape jobs and labels: `cluster="hy-home"` and `namespace="hy-home"`
  on every series; job names follow the service names.

### Dashboard dispositions

| Current file | Disposition | Source after change |
| --- | --- | --- |
| `vllm-monitoring`, `neo4j`, `neo4j-operations`, `vaults`, `otel-collector`, `loki-dashboard` | Remove | None; logs move to Logs Drilldown |
| `airflow-dag`, `airflow-dag-overview`, `airflow-operators`, `airflow3-monitoring` | Replace with one | Airflow mixin overview, after the statsd mapping gains its rules |
| `airflow-monitoring`, `n8n-workflow-analytics` | Keep | Read-only PostgreSQL datasources |
| `redis-overview`, `valkey-overview` | Replace with one | `oliver006/redis_exporter` contrib dashboard; Valkey cluster adds grafana.com 21914 |
| `cadvisor`, `docker-metrics`, `docker-monitoring` | Replace with one | grafana.com 19792 (Compose labels) |
| `postgres`, `postgres-exporter` | Replace with one | grafana.com 9628 without Kubernetes variables |
| `loki-global`, `loki-metrics` | Replace | Loki mixin (operational, reads, writes, chunks) |
| `otel-tempo` | Replace | Tempo mixin (operational, reads, writes) |
| `prometheus`, `alertmanager` | Replace | Prometheus and Alertmanager mixins |
| `keycloak` | Replace | Keycloak troubleshooting and capacity-planning dashboards |
| `openbao` | Keep, fix | grafana.com 23725, job and datasource corrected |
| `qdrant` | Replace | grafana.com 24603 |
| `kafka-overview`, `kafka-exporter` | Replace | Confluent KRaft cluster and topics dashboards; grafana.com 7589 for consumer lag |
| `etcd`, `opensearch` | Replace | etcd and OpenSearch mixins |
| `node-exporter`, `dcgm-exporter`, `traefik`, `haproxy`, `k6`, `docker-registry`, `n8n-system-health`, `ollama` | Keep, refresh | Latest upstream revision where one exists |
| (new) | Add | SeaweedFS repository dashboard, Gatus example, Grafana, Alloy and Pyroscope mixins, Confluent Connect and Schema Registry, PostgreSQL Patroni 18870, MongoDB 16490, CouchDB mixin, Cassandra (criteo), OAuth2 Proxy and Flower (local) |

## Failure Modes and Guardrails

| Failure | Guard |
| --- | --- |
| Grafana runs out of memory with more dashboards, tracing and two SQL datasources | Its limit is raised with the W8 figures before tracing is enabled |
| Static labels change every series identity | Recording and alert rules are updated in the same unit; old series age out under the 15-day retention |
| The PostgreSQL datasource exposes more than intended | A dedicated role with `SELECT` only on named tables; its password is a Docker secret the owner generates |
| Tracing adds load | Sampling ratio of 0.1 or lower, sent to Alloy's existing OTLP receiver |
| A vendored dashboard drifts from upstream | Source and revision recorded; refresh is a reviewed change |
| A stopped service's job shows as down | `up == 0` is expected for on-demand services and is excluded from `PrometheusInfraTargetsMissing` |

## Acceptance Contract

1. The Grafana README table covers all 151 Compose services, and the
   contract test fails if a scrape job has no dashboard or a dashboard names
   no service.
2. The dispositions are applied: no removed file remains, and no two
   dashboards share more than half their metric names.
3. Every external dashboard records its source and revision, and every
   datasource reference resolves.
4. For each running service with a metrics source, its dashboard's queried
   metric names exist in Prometheus.
5. All datasources report healthy; the two PostgreSQL datasources can only
   read.
6. No source is scraped twice; the added jobs are `up` for running services.
7. Logs Drilldown shows volume, patterns and levels; Traces Drilldown shows
   Keycloak, Grafana, Airflow and Traefik spans and TraceQL metrics;
   Profiles Drilldown shows the Go services; Metrics Drilldown uses the
   scrape interval.
8. No alert rule queries a metric its source cannot emit; every rule links an
   existing runbook; `promtool check rules` passes.
9. After 2026-10-03, the limits for Grafana, `airflow-triggerer` and OpenBao
   and the container-resource alert thresholds are set from the final W8
   figures, with the figures recorded.
10. GDE, POL and RUN-0041, RUN-0045 and the Grafana README describe the new
    state.
11. `run-ci-gate.py --profile full`, `tests/lib` and `tests/validation` pass.

## Traceability

- REQ-0007: observability tier. AD-0006: observability architecture.
- GDE, POL and RUN-0041 (Grafana); RUN-0045 (Prometheus).
- SPEC-0182 Tasks 0002 and 0003: W8 resource window and records.
- SPEC-0192: host backup alerts, which this package keeps.

## Open Questions

None; the owner's rulings above settle the design choices.

## Operational Impact

Grafana, Prometheus, Loki, Tempo, Alloy, Keycloak, Airflow, the registry,
OAuth2 Proxy, Kafka Connect and Schema Registry are recreated or reloaded in
W6 with owner approval. The owner generates the Grafana reader password.
Existing series keep their old labels until retention removes them.
