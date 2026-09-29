---
title: "Observability Dashboards, Signals and Alerting"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0193-TSK-0001"
parent_ids:
- "SPEC-0193"
- "SPEC-0193-PLAN-0001"
created: "2026-09-30"
---

# Observability Dashboards, Signals and Alerting

## Objective

Execute W1 to W8 of the [Plan](../plan.md) and record the evidence for every
acceptance criterion of [SPEC-0193](../spec.md).

## Inputs

- 2026-09-29 inventory: 151 Compose services (44 HOME, 55 OPTIONAL, 41 LAB,
  11 DEV); 39 dashboards; live Prometheus reads `prometheus.dev.yml`.
- Dashboard metric check: per dashboard, the share of queried metric names
  present in Prometheus (for example `haproxy` 0%, `vllm-monitoring` 4%,
  `node-exporter` 83%, `traefik` 100%).
- External-dashboard survey: vendor repositories and grafana.com, each
  candidate matched against the pinned exporter's metric names; upstream
  JSON copies are in the session scratchpad, not the repository.
- Alert audit: 78 rules, 26 with metric names absent from Prometheus, 28
  without a runbook link.
- Interim W8 figures for 2026-09-26 00:00 to 09-29 23:00 KST; Prometheus has
  gaps 09-26 11:05–18:10 and 09-27 11:55–13:25.

## Work Log

- 2026-09-30: Spec, Plan, and Task drafted.

## Verification Evidence

Not started.

## Review Evidence

None yet.

## Commit Ledger

None yet.

## Rulings

- 2026-09-30: Owner rulings 1–5 of the Spec.

## Deferred Items

None yet.
