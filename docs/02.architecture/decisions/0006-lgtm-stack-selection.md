---
title: "LGTM Stack and Grafana Alloy Selection"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0006"
parent_ids:
- "AD-0006"
created: "2026-03-26"
---
# ADR-0006: LGTM Stack and Grafana Alloy Selection

## Context

This document records the background and reasons for selecting the currently implemented Grafana LGTM stack (Loki, Grafana, Tempo, Prometheus) and the Grafana Alloy collector as the observability tools for the `hy-home.docker` platform. Long-term metrics storage is treated only as a separate expansion candidate not currently implemented in tracked compose.

In a modern microservices environment, correlation across metrics, logs, and tracing is essential. Existing fragmented tools lacked a connecting link between data types, causing loss of context during incident response. In addition, there was an operational burden of managing a different agent for each data type (Promtail, Otel-Collector, etc.).

### Traceability

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked in `Related Documents`, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

## Decision

- **Adopt the Grafana LGTM Stack**: use an integrated ecosystem that supports free navigation between data (e.g., jump to logs from traces).
- **Adopt Grafana Alloy**: use a unified agent that supports both the OpenTelemetry (OTLP) and Prometheus ecosystems, collecting, processing, and routing various telemetry data in a single binary.
- **S3 (MinIO) Backend**: store Loki and Tempo data in cloud-native S3 (MinIO) to secure durability and scalability.

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

### Alternative 1: ELK Stack (Elasticsearch, Logstash, Kibana)

- **Good**: powerful full-text search, favorable for structured data analysis.
- **Bad**: high memory and storage footprint, relatively weak tracing integration.

### Alternative 2: OpenTelemetry Collector (Vanilla)

- **Good**: industry standard and vendor-neutral.
- **Bad**: lacks tight integration features (discovery, etc.) with the Grafana ecosystem (Loki/Prometheus, etc.) compared to Alloy.

## Consequences

- **Positive**:
  - **Unified user experience**: all observability data can be analyzed from a single Grafana UI.
  - **Simplified operations**: Alloy alone replaces all collection functions, reducing management points.
  - **Cost efficiency**: S3-based storage reduces the cost of storing large volumes of data.
- **Trade-offs**:
  - **Learning curve**: need proficiency with Grafana Alloy's new configuration language (HCL-like).
  - **Additional infrastructure**: operational burden of backend infrastructure such as MinIO.

### Explicit Non-goals

- Does not fully exclude the ELK (Elasticsearch, Logstash, Kibana) stack (evaluated individually when specialized search is needed).
- Does not support immediate migration to a commercial SaaS (Datadog, etc.).

## Related Documents

- **PRD**: [../../01.requirements/0007-observability.md](../../01.requirements/0007-observability.md)
- **Architecture Description**: [../descriptions/0006-observability-architecture.md](../descriptions/0006-observability-architecture.md)
- **Spec**: [../../03.specs/007-observability/spec.md](../descriptions/0006-observability-architecture.md)
