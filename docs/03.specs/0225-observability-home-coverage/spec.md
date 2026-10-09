---
title: "Observability HOME Coverage"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0225"
parent_ids:
- "REQ-0007"
- "AD-0006"
created: "2026-10-09"
---

# Observability HOME Coverage

## Overview

Run against HOME Prometheus and Loki, the 50 provisioned Grafana dashboards
returned no data for 526 of their 1,269 panels and an error for one. Five
dashboards and four alert rules target services that now exist only in the
independent LAB, which HOME never scrapes. Most other empty panels came from
mixins and community dashboards written for Kubernetes or for features HOME
does not run, from metric names that changed in the pinned versions, and from
targets HOME did not scrape or kept for too short a time. The owner asked that
LAB-only items stop appearing on HOME and that each dashboard collect and show
the data its purpose needs.

## Scope

In scope: the Grafana dashboards and README, the Prometheus jobs, alert rules
and service networks in `infra/06-observability`, the metrics inputs of
SeaweedFS, node-exporter, OpenBao, Keycloak, the PostgreSQL exporters and
Gatus, their tests, the affected Stage 05 documents and the HOME rollout.
Out of scope: LAB observability wiring, the hy-home.k8s cluster's own
telemetry (it is an integrated cluster, not LAB), and panels that are empty
only because the activity they measure has not happened yet.

## Contracts

1. LAB separation. Dashboards for LAB-only services live in `labs/dashboards/`,
   outside Grafana provisioning; no HOME alert rule targets a LAB-only service.
2. HOME series. Every provisioned panel queries series HOME produces, with the
   pinned versions' metric names and the single-binary Loki and Tempo
   deployment; panels for features HOME does not run are removed rather than
   left empty. Cluster variables default to `hy-home`.
3. SeaweedFS metrics. Master, volume and filer serve metrics on 9324-9326 over
   `seaweedfs_metrics_net`, an internal network without a host address whose
   only other member is Prometheus. Prometheus therefore also reaches the
   internal SeaweedFS APIs and is inside that trust boundary.
4. Host metrics. node-exporter runs in the host network namespace with its
   listener bound to the `obs_net` gateway address, so its network collectors
   report the host and the LAN cannot reach it; any container on a
   non-internal bridge can. Prometheus keeps the `node-exporter` name through
   `extra_hosts`. The `processes` and `tcpstat` collectors are on; timex,
   interrupts and systemd stay off.
5. Retention and buckets. OpenBao keeps Prometheus metrics for 24 h so its
   ten-minute usage gauges stay visible; Keycloak adds a 250 ms HTTP bucket;
   both PostgreSQL exporters enable `stat_checkpointer`; Gatus checks the
   gateway certificate's expiry.

## Acceptance Criteria

1. No provisioned dashboard or HOME alert rule references a LAB-only service,
   and the moved dashboards keep their sources.
2. Compose, network, alert and dashboard contract tests cover the new
   networks, listeners, jobs, alert and coverage rows.
3. On HOME every query of every provisioned dashboard runs without error, and
   the remaining empty panels are explained as idle, on demand or stopped.
4. The changed gate, the staged style check and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-observability-home-coverage.md)
- [Datastore observation split](../0224-datastore-observation-split/spec.md)
