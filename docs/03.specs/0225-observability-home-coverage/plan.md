---
title: "Observability HOME Coverage Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0225-PLAN-0001"
parent_ids:
- "SPEC-0225"
created: "2026-10-09"
---

# Observability HOME Coverage Plan

## Overview

Audit every dashboard query on HOME, classify each empty panel, move the
LAB-only items out, add the missing collection, correct or remove the
dashboard queries, roll out on HOME, document and validate.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Move LAB dashboards and rules out of HOME | None | TSK-0001 | Task evidence |
| W2 | 2 | SeaweedFS scrape network, node-exporter host namespace, OpenBao retention, Keycloak bucket, checkpointer collector, Gatus TLS check | W1 | TSK-0001 | Task evidence |
| W3 | 3 | Dashboard query corrections and removals | W2 | TSK-0001 | Task evidence |
| W4 | 3 | HOME rollout and re-audit; Stage 05 documents | W3 | TSK-0001 | Task evidence |
| W5 | 4 | Changed gate, staged style check, candidate quality, merge | W4 | TSK-0001 | Task evidence |

## Verification Plan

A query audit of every provisioned dashboard against HOME Prometheus and Loki
before and after, unit and contract tests, promtool, Compose rendering, HOME
target and listener checks, the changed gate, the staged style check and the
remote candidate.

## Risks and Rollback

- Recreating SeaweedFS master, volume and filer pauses object storage for
  Loki, Tempo and MLflow for seconds; clients retry.
- Recreating Keycloak interrupts sign-in for under a minute.
- OpenBao's retention change needs a restart, which needs the owner's manual
  unseal; until then its usage gauges stay sparse.
- If `obs_net` is ever recreated on another subnet, node-exporter's listener
  and the Prometheus and Alloy `extra_hosts` must move with it.
- Rollback: revert the commits and recreate the same services; Grafana reloads
  the dashboards from files, and `labs/dashboards/` can move back.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-observability-home-coverage.md)
