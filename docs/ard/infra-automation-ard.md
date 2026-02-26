# Phase 2 ARD: Scaling & Autonomous Patterns

## [REQ-PH2-02] Advanced Technical Spec

### Multi-Project Bridge Architecture

Infrastructure tiers SHALL define standardized `project_net` interfaces for seamless app-to-infra bridging without expose-port conflicts.

### Autonomous sidecars

- Services requiring post-boot setup (e.g., MinIO, OpenSearch) SHALL utilize the "Init-Sidecar" pattern.
- Init-containers MUST use standard images (e.g., `minio/mc`) and exit with code 0 upon success.

### Provisioned Observability

- **Grafana**: Dashboards and Datasources MUST be defined in `./infra/06-observability/grafana/provisioning`.
- **Alloy**: Standardized relabeling rules for `hy-home.scope` across all projects.

### Scaling Strategy

- **Horizontal**: Use of Docker Compose `deploy.replicas` for stateless components (e.g., n8n-worker).
- **Vertical**: Expansion of `resource-budgets/` spec to include dynamic scaling profiles.
