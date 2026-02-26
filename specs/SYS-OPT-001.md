# Spec: Home Lab System Optimization [SYS-OPT-001]

## Overview

This specification defines the technical implementation standards for optimizing the home lab's Docker-based infrastructure.

## 1. Build and Layer Optimization [REQ-OPT-01]

- **Multi-stage Builds**: Custom base images MUST use multi-stage builds to minimize image size.
- **Caching**: Dockerfiles MUST be ordered from least-frequently changed to most-frequently changed parts to maximize layer caching.

## 2. Security Hardening [REQ-OPT-02]

- **Network Isolation**:
  - `hy-net-ingress`: Only gateway and external proxy containers.
  - `hy-net-internal`: Core services, data, and logic.
  - `hy-net-observability`: Centralized telemetry collectors.
- **Secrets Protocol**: NO plain-text environment variables for passwords. Use `secrets` block in `docker-compose.yml`.

## 3. Observability Standard [REQ-OPT-03]

- **Logs**: All containers MUST use the `loki` log driver or export to a local promtail instance.
- **Metrics**: Standardized health check endpoints (`/health`) for Prometheus scraping.

## 4. Resource Management [REQ-OPT-04]

- **Quotas**: Every service MUST define `deploy.resources.limits.memory` and `deploy.resources.limits.cpus`.
- **Initialization**: Use `depends_on` with `condition: service_healthy` to ensure ordered startup.

## Verification Requirements [REQ-SPT-10]

- **AC-01**: `docker compose config` passes without warnings.
- **AC-02**: `/run/secrets/` contains the expected secret files in a running container.
- **AC-03**: Grafana shows resource usage metrics for 100% of running services.
