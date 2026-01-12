# Pushgateway

The Prometheus Pushgateway exists to allow ephemeral and batch jobs to expose their metrics to Prometheus. Since these jobs may not exist long enough to be scraped, they can push their metrics to the Pushgateway. Prometheus then scrapes the metrics from the Pushgateway.

## 🚀 Overview

- **Service**: `pushgateway`
- **Docker Image**: `prom/pushgateway:v1.11.2`
- **Port**: `9091` (Web UI/API)

## ⚙️ Configuration

Pushgateway is a simple binary and usually doesn't require a complex configuration file. It keeps the metrics in memory.

- **Persistence**: In this setup, persistence is **not enabled** by default (no `--persistence.file` flag turned on in `docker-compose.yml`), meaning metrics are lost on restart. This is typical for ephemeral job caching.

## 🔗 Integration

- **Client Apps**: Scripts or batch jobs send `POST` requests to `http://pushgateway:9091/metrics/job/...`.
- **Prometheus**: Scrapes Pushgateway (usually configured as a target in `prometheus.yml`, though specifically not listed in the default jobs unless added).
- **Traefik**: Exposed via `pushgateway.${DEFAULT_URL}` (HTTPS).

## ⚠️ When to use

**Reference**: [Prometheus Documentation - When to use the Pushgateway](https://prometheus.io/docs/practices/pushing/)

- **Do not use** Pushgateway to turn Prometheus into a push-based monitoring system.
- **Use it** for service-level batch jobs that need to report status after completion.

## 🛠 Directory Structure

```text
pushgateway/
└── README.md
```
