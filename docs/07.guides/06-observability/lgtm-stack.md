---
tier: 07.guides
component: 06-observability
title: LGTM Stack Overview
status: production
updated: 2026-03-25
---

# LGTM Stack Overview

The LGTM stack (Loki, Grafana, Tempo, Mimir/Prometheus) provides a unified observability pipeline for `hy-home.docker`.

## 1. Core Architecture

The stack consists of the following components:

- **Loki**: Log aggregation system (Promtail/Alloy as agents).
- **Grafana**: Unified visualization and alerting dashboard.
- **Tempo**: Distributed tracing backend.
- **Prometheus**: Metrics collection and time-series database.
- **Alloy**: The unified telemetry collector (OpenTelemetry-compatible).

## 2. Data Flow

1. **Collection**: Alloy scrapes Prometheus metrics, tail logs for Loki, and receives OTLP traces for Tempo.
2. **Ingestion**: Alloy forwards data to the respective backends.
3. **Visualization**: Grafana queries all backends to provide a unified view.

## 3. Storage Architecture

Persistent data is stored in **MinIO** (04-data tier) to ensure scalability and cost-efficiency.

- Loki: S3-compatible chunk storage.
- Tempo: S3-compatible block storage.
- Prometheus: Local TSDB with optional remote write.

## 4. Security

- **Authentication**: Keycloak SSO via OAuth2 Proxy for Grafana.
- **Internal**: Mutual TLS or internal network isolation.

---
[Return to Observability Index](./README.md)
