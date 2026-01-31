# Prometheus

Prometheus is an open-source systems monitoring and alerting toolkit. It collects metrics from configured targets at given intervals, evaluates rule expressions, displays the results, and can trigger alerts if some condition is observed to be true.

## 🚀 Overview

- **Service**: `prometheus`
- **Docker Image**: `prom/prometheus:v3.9.0`
- **Port**: `9090` (Web UI/API)

## ⚙️ Configuration

The configuration files are located in the `config/` directory.

### Setup

1. **Copy the example configuration:**

    ```bash
    cp prometheus.yml.example prometheus.yml
    cp alert_rules.yml.example alert_rules.yml
    ```

2. **Edit `prometheus.yml`:**
    - Review `scrape_configs` to ensure all target services are correctly defined.
    - If using external services or custom ports, update the `targets`.

3. **Edit `alert_rules.yml`:**
    - Define your recording rules and alerting rules here.

### Scrape Jobs

This configuration includes monitoring for various infrastructure components:

- **Self**: Prometheus, Alertmanager, Cadvisor, Alloy.
- **Databases**: PostgreSQL Cluster, Redis Cluster, MongoDB (Mng), CouchDB.
- **Middleware**: Kafka, Traefik, HAProxy.
- **Applications**: Keycloak, MinIO, N8n, Qdrant, Ollama.

## 🔔 Alerting

- **Alertmanager**: Configured to send alerts to `alertmanager:9093`.
- **Rules**: Loaded from `alert_rules.yml`.

## 🔗 Integration

- **Grafana**: Uses Prometheus as a primary data source for dashboards.
- **Tempo**: Receives trace-related metrics via remote write (if configured).

## 🛠 Directory Structure

```text
prometheus/
├── config/
│   ├── alert_rules.yml          # Alerting rules (Ignored by Git)
│   ├── alert_rules.yml.example  # Template rules
│   ├── prometheus.yml           # Main configuration (Ignored by Git)
│   └── prometheus.yml.example   # Template configuration
└── README.md
```
