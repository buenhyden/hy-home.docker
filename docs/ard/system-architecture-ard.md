# ARD: Hy-Home Infrastructure Target Architecture (ARD-001)

## 1. Overview

The target architecture follows a modular, tier-based design using Docker Compose `include`. It prioritizes the **LGTM (Loki, Grafana, Tempo, Prometheus)** observability stack and hardened container boundaries.

## 2. Component Diagram (C4 Level 2 - Containers)

[Mermaid diagram placeholder - will be added in implementation phase]

## 3. Storage Strategy

- **Volumes**: Local bind mounts for data persistence (e.g., `/infra-data/prometheus`).
- **Secrets**: Docker Secrets (file-based) mounted at `/run/secrets/`.

## 4. Networking [REQ-SPT-05]

- **infra_net**: Dedicated bridge network for core infrastructure services.
- **project_net**: External network for application-level services.
- **Gateway**: Traefik (Edge) handles TLS termination and routing.

## 5. Security Architecture

- **Rootless Operation**: Services MUST run as non-root (UID 1000:1000) where possible.
- **Isolation**: `security_opt: [no-new-privileges:true]`, `cap_drop: [ALL]`.
- **Secrets Management**: No environment variable injection for sensitive data; use Docker Secrets.

## 6. Observability Path

1. **Collector**: Grafana Alloy collects logs (Docker containers) and metrics (cAdvisor, service endpoints).
2. **Storage**: Loki (Logs), Prometheus (Metrics), Tempo (Traces).
3. **Visualization**: Grafana serves as the unified dashboard.
