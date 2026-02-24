# Observability Stack (LGTM + Alloy) Architecture

## Overview

A comprehensive, enterprise-grade observability stack based on the **LGTM** pattern (Loki, Grafana, Tempo, Mimir/Prometheus). This stack provides full-spectrum visibility into infrastructure and application health, utilizing **Grafana Alloy** as a unified telemetry collector for metrics, logs, and distributed traces.

```mermaid
graph TB
    subgraph "Telemetry Sources (Push/Pull)"
        A[App Services] -->|OTLP Push| E[Grafana Alloy]
        B[Docker Containers] -->|Scrape| F[cAdvisor]
        C[Host Node] -->|Scrape| P[Node Exporter]
    end

    subgraph "Logic & Collection Layer"
        E -->|Remote Write| P[Prometheus<br/>Metrics]
        E -->|Logs Push| L[Loki<br/>Logs]
        E -->|Traces Push| T[Tempo<br/>Traces]
        F -->|Scrape Pull| P
    end

    subgraph "Visualization & Alerting"
        G[Grafana Dashboard]
        AM[Alertmanager]

        P -->|Query| G
        L -->|Query| G
        T -->|Query| G

        P -->|Alert Rules| AM
        AM -->|Notify| Slack[Slack Webhook]
        AM -->|Notify| Mail[SMTP Email]
    end

    subgraph "Identity"
        KC[Keycloak SSO] <-->|OAuth2| G
    end
```
