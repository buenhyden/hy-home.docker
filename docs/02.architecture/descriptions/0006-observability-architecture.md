---
title: "Observability Architecture Description"
version: "1.0.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0006"
parent_ids:
- "REQ-0007"
created: "2026-03-26"
---
# Observability Architecture Description

> Integrated Telemetry Pipeline with LGTM Stack and Grafana Alloy.

## Context and Stakeholders

This document defines the reference architecture of `06-observability`, the observability layer of the `hy-home.docker` platform. To secure cloud-level observability in a local environment, it integrates the currently implemented LGTM stack (Loki, Grafana, Tempo, Prometheus) with Grafana Alloy, Alertmanager, Pushgateway, cAdvisor, and Pyroscope.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded in this section and the following views. Only concerns confirmed in the existing document are covered here.

The Observability tier collects, stores, and visualizes status information across the system, and accelerates problem resolution through correlation analysis during incidents. The current compose provides OTLP trace ingress, Docker log discovery, and Prometheus scrape/remote-write paths, and Loki/Tempo use SeaweedFS-based S3 backend storage.

## System Boundaries

This section preserves the system boundaries, consumption relationships, non-goals, and constraints the current document already records.

- **Owns**:
  - Centralized logging (Loki)
  - Time-series metric collection and alerting (Prometheus/Alertmanager)
  - Distributed tracing (Tempo)
  - Continuous profiling (Pyroscope)
  - Unified dashboard (Grafana)
  - Unified telemetry collection (Alloy)
- **Consumes**:
  - **SeaweedFS (04-data)**: S3 storage for log and trace data.
  - **Keycloak (02-auth)**: OIDC provider for Grafana SSO login.
- **Does Not Own**:
  - Application security logs (owned by 03-security)
  - Business statistics data (owned by the Data Warehouse)
- **Non-goals**:
  - Dependency on external cloud monitoring vendors (fully self-hosted orientation)

## Quality Attributes

### Quality Scenarios

Quality scenarios point to the existing configuration these attributes apply to and the verification expectations tied to the failure boundary. Concrete execution evidence belongs to the related Spec and Operations documents.

- **Performance**: Minimizes application overhead through asynchronous data processing via Alloy.
- **Security**: Applies role-based access control (RBAC) based on Keycloak OIDC.
- **Reliability**: A recovery boundary that covers Loki/Tempo's SeaweedFS object blocks together with each service's local WAL/working state.
- **Scalability**: For Prometheus, the local TSDB is currently the durable authority; enabling the remote-write receiver alone does not imply an external long-term store.
- **Observability**: Includes a self-monitoring dashboard.

## Components

### Viewpoints and Views

This section uses the context, component, or deployment representation as the view for the relevant concern.

In the current source, Docker logs and OTLP traces pass through **Grafana Alloy** to Loki/Tempo, and Prometheus scrapes exporters/services directly. Only Alloy self-metrics are delivered to Prometheus via remote write. A Pyroscope write sink exists, but with no profile source, end-to-end profile collection is not established with the current configuration alone. Users query each datasource in **Grafana**.

## Data Flow

### Data and Control Flows

Data and control flows include only the interactions specified in this section and the existing infrastructure/deployment description.

- **Key Entities / Flows**:
  - **Metrics Flow**: cAdvisor/Exporters/Services -> Prometheus; Alloy self-metrics -> Prometheus remote write
  - **Logs Flow**: Docker Logs -> Alloy -> Loki -> SeaweedFS
  - **Traces Flow**: App (OTLP) -> Alloy -> Tempo -> SeaweedFS
  - **Profiles Flow**: Pyroscope sink is configured, but no Alloy profile source is declared
- **Storage Strategy**:
  - Metrics: Prometheus local TSDB
  - Logs: Loki SeaweedFS bucket `loki-bucket`, `retention_period: 168h`
  - Traces: Tempo SeaweedFS bucket `tempo-bucket`, `block_retention: 24h`
  - Profiles: Pyroscope local filesystem backend
- **Data Boundaries**: The principle is that all telemetry data communicates only within the `obs_net` internal network.

## Deployment View

- **Runtime / Platform**: Container orchestration based on Docker Compose v2.x.
- **Deployment Model**: `prometheus`, `grafana`, `loki`, `alloy`,
  `node-exporter`, `cadvisor`, `gatus`, and `alertmanager` are `HOME`.
  `tempo`, `pyroscope`, and `pushgateway` are `OPTIONAL`. `obs` is the full
  compatibility profile, and `obs-core`, `obs-host`, `logs`, `tracing`,
  `profiling`, `alerting`, `availability`, and `batch-metrics` provide narrower
  activation. A HOME profile start does not automatically stop an already
  running optional container.
- **Operational Evidence**: Grafana provisioning files, root compose profile validation, service-local compose validation with root network/secret context, and hardening script output.

## Traceability

The disposition of the upstream requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Related Documents

- **PRD**: [../../01.requirements/0007-observability.md](../../01.requirements/0007-observability.md)
- **Spec**: [../../03.specs/007-observability/spec.md](0006-observability-architecture.md)
- **ADR**: [../decisions/0006-lgtm-stack-selection.md](../decisions/0006-lgtm-stack-selection.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
