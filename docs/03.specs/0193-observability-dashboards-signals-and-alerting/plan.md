---
title: "Observability Dashboards, Signals and Alerting Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0193-PLAN-0001"
parent_ids:
- "SPEC-0193"
created: "2026-09-30"
---

# Observability Dashboards, Signals and Alerting Plan

## Objective

Make every service visible once, correlate metrics, logs, traces and
profiles, and keep only alerts that can fire, as [SPEC-0193](spec.md)
describes.

## Dependencies

- Owner approval of the package and of each W6 recreate.
- The owner generates the Grafana reader password before W6.
- The final SPEC-0182 W8 figures, available from 2026-10-03, for W7.

## Execution Sequence

1. W1 Collection and datasources: scrape jobs (merge, add, static labels,
   recording rules) in both Prometheus files; service metrics settings
   (Airflow statsd mapping, Keycloak, registry, OAuth2 Proxy, Connect and
   Schema Registry JMX); Grafana datasource links, Pyroscope UID and the
   PostgreSQL datasources with the reader role and secret metadata
   (criteria 5, 6).
2. W2 Drilldown backends: Loki volume, patterns and levels; Tempo
   `local-blocks` and TraceQL metrics; Alloy `pprof` scrape; OTLP tracing in
   Keycloak, Grafana and Airflow (criterion 7).
3. W3 Dashboards: apply the dispositions, vendor the external dashboards
   with source and revision, resolve datasource references, write the
   coverage table (criteria 1, 2, 3).
4. W4 Alerting: rewrite or drop the 26 dead rules, rename the OpenBao file,
   fix runbook links, add rules for new jobs, `promtool` (criterion 8).
5. W5 Contract test and documents: dashboard, datasource and coverage test;
   GDE, POL and RUN-0041, RUN-0045, Grafana README (criteria 1, 10).
6. W6 Rollout: raise Grafana's memory limit first; create the reader role;
   reload Prometheus; recreate the changed services one at a time; check
   datasource health, dashboard data, the Drilldown apps and `ALERTS`
   (criteria 4, 5, 6, 7).
7. W7 Resources, after 2026-10-03: take the final W8 figures from SPEC-0182,
   set the named limits and the container-resource alert thresholds, and
   record the figures (criterion 9).
8. W8 Gates: full gate and both suites (criterion 11).

## Risk and Rollback

Each unit is its own commit. Dashboards and rules revert with Git and reload
without restart. A service recreate reverts by restoring the previous
Compose file and recreating it. The reader role is dropped with one
statement. Relabelled series keep old labels until retention removes them.

## Verification

- The contract tests, `promtool check rules`, `amtool`-free rule unit checks
  where present, and pre-commit.
- Grafana `/api/datasources/uid/<uid>/health` for each datasource, dashboard
  query checks against Prometheus, and the Drilldown apps' backing APIs
  (Loki volume and patterns, Tempo TraceQL metrics, Pyroscope label values).
- `run-ci-gate.py --profile full`, `tests/lib`, and `tests/validation`.

## Rulings

- 2026-09-30: The owner's five rulings are recorded in the Spec.
