# Phase 2 PRD: Infrastructure Automation & Advanced Operations

## [REQ-SPT-04] Vision

To evolve from a static infrastructure stack to an autonomous platform with self-provisioning capabilities and advanced error handling.

## Personas

- **DevOps Engineer**: Needs to reduce manual toil by automating repetitive setup tasks (buckets, topics).
- **Service Operator**: Needs clear visualization of infra health via pre-provisioned dashboards.

## Success Metrics [REQ-SPT-01]

- **Zero-Touch Provisioning**: Core buckets and DB schemas initialized automatically on first boot.
- **Observability Coverage**: 100% of services have dedicated Grafana dashboards.
- **Manual Toil Reduction**: 50% reduction in manual setup steps for new data clusters.

## Phase 2 Requirements (Persona Framed)

- [REQ-AUTO-01] **As a DevOps Engineer**, I want buckets and topics initialized via sidecars so that I don't have to run manual `mc` commands.
- [REQ-OBS-01] **As a Service Operator**, I want dashboards provisioned from code so that my telemetry is always consistent after a restart.
- [REQ-OPS-01] **As a Developer**, I want `project_net` bridging so that my apps in other repos can talk to the infra without port collisions.

## Acceptance Criteria (GWT) [REQ-SPT-06]

| ID | Given | When | Then |
| --- | --- | --- | --- |
| AC-PH2-01 | OpenSearch is running | `opensearch-init` completes | Index templates exist without manual input. |
| AC-PH2-02 | Grafana starts | User opens dashboard UI | Standard dashboards are pre-loaded from `/etc/grafana/dashboards`. |
| AC-PH2-03 | Project Net exists | Alloy relabeling is active | Logs from project containers are visible in Loki under `scope: app`. |
