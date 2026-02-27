# Infrastructure Optimization Analysis Results

## 1. Identified Optimization Opportunities

### 1.1 Service Profiles for Modular Orchestration

- **Problem**: The current root `docker-compose.yml` includes all sub-stacks, which can lead to high resource consumption in local development environments.
- **Solution**: Implement Docker Compose **Profiles** (`core`, `data`, `obs`, `workflow`, `ai`, `messaging`) to allow selective service startup.

### 1.2 Capability and Security Hardening

- **Problem**: While many services use `extends` from `common-optimizations.yml`, some newly added services might lack uniform security boundaries.
- **Solution**: Ensure consistent application of `no-new-privileges`, `cap_drop: ALL`, and `user: "1000:1000"` where possible.

### 1.3 Healthcheck-Driven Dependency Management

- **Problem**: Some services depend on others only by `service_started`, which can cause race conditions during bootstrap.
- **Solution**: Transition all cross-stack dependencies to `service_healthy`.

## 2. Profile Categorization Map

| Profile | Services / Tiers | Description |
| --- | --- | --- |
| `core` | `01-gateway/traefik`, `02-auth/keycloak` | Essential ingress and identity services. |
| `data` | `04-data/*` (Postgres, Valkey, Minio, etc.) | Persistence and storage services. |
| `obs` | `06-observability/*` | LGTM Stack (Loki, Grafana, Tempo, Prometheus). |
| `messaging` | `05-messaging/kafka` | Event-driven infrastructure. |
| `workflow` | `07-workflow/*` (Airflow, n8n) | Automation and workflow engines. |
| `ai` | `08-ai/*` (Ollama, Qdrant) | Local AI and Vector Database stack. |

## 3. Recommended Implementation Steps

1. **Modify Sub-stacks**: Add `profiles` list to each service in their respective `docker-compose.yml`.
2. **Root Configuration**: Update root `docker-compose.yml` comments to describe the profile map.
3. **Bootstrap Script**: Update `scripts/bootstrap.sh` (if exists) or `README.md` to utilize profiles.
