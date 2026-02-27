---
title: '[ARD-OBS-01] Observability Stack Architecture Reference'
status: 'Approved'
version: '1.0.0'
owner: 'Platform Architect'
prd_reference: '../prd/infra-baseline-prd.md'
adr_references: ['../adr/adr-0005-sidecar-resource-initialization.md']
tags: ['ard', 'observability', 'lgtm', 'alloy']
---

# [ARD-OBS-01] Observability Stack Architecture Reference

_Target Directory: `docs/ard/observability-ard.md`_

---

## 1. Executive Summary

The Hy-Home Observability stack implements the **LGTM** pattern, providing a unified platform for metrics, logs, and traces. It leverages Grafana Alloy as a single telemetry agent to minimize host overhead and simplify discovery.

## 2. Business Goals

- **Unified Visibility**: Single pane of glass for all infrastructure tiers.
- **Operational Intelligence**: Fast root-cause analysis via trace-to-log correlation.
- Reduce MTTR for infrastructure and application failures.
- Provide a single pane of glass for multi-tier resource monitoring.
- Enforce structured telemetry standards across all containerized services.

## 3. System Overview & Context

```mermaid
graph LR
    subgraph "Service Tiers"
        S[Containers]
    end
    subgraph "Telemetry Pipeline"
        L[Loki]
        P[Prometheus]
        T[Tempo]
    end
    subgraph "Visualization"
        G[Grafana]
    end

    S -- Logs --> L
    S -- Metrics --> P
    S -- Traces --> T
    L & P & T --> G
```

## 4. Architecture & Tech Stack Decisions

### 4.1 Component Architecture

- **Logging**: Docker natively pushes to Loki via the `loki` driver.
- **Metrics**: Grafana Alloy scrapes Prometheus endpoints via `infra_net`.
- **Tracing**: OTLP-compatible libraries export traces to Tempo.

### 4.2 Technology Stack

- **Logs**: Grafana Loki (Storage) & Docker Driver (Shipper)
- **Metrics**: Prometheus (Storage) & Grafana Alloy (Collector)
- **Traces**: Grafana Tempo
- **Visualization**: Grafana 11.x

## 5. Data Architecture

- **Retention Strategy**:
  - Logs: 14 days (local disk).
  - Metrics: 30 days (Prometheus TSDB).
  - Traces: 7 days.

## 6. Security & Compliance

- **Storage Security**: Local filesystem encryption for telemetry data.
- **Access Control**: RBAC enforced via Grafana integration with Keycloak.

## 8. Non-Functional Requirements (NFRs)

- **Ingestion Latency**: Logs MUST be queryable in Grafana within 2 seconds of generation.
- **Query Performance**: Standard dashboard panels SHALL load in < 500ms.

## 9. Architectural Principles, Constraints & Trade-offs

- **Constraints**: Relies on specific Docker plugins (Loki) being installed on the host.
- **What NOT to do**: Use local file logging inside containers.
- **Chosen Path Rationale**: LGTM stack chosen for its deep integration and shared metadata model.
or to reduce host I/O.
- **Chosen Path**: Single Alloy agent over fragmented exporters to minimize total system resource footprint.
- **Configuration Standard**: All services SHALL inherit from `infra/common-optimizations.yml` for unified observability labels and security settings.
