# Phase 2 ARD: Scaling & Autonomous Patterns

## [REQ-SPT-05] Technical Specification

### Architecture Overview

Expansion of the baseline architecture to include autonomous resource setup and project-bridging network aliases.

### NFR (Non-Functional Requirements)

- **Zero-Touch Reliability**: Initialization containers MUST be idempotent and handle transient service unavailability.
- **Network Isolation**: `project_net` MUST be used exclusively for app-to-infra traffic.

### Storage Strategy

- **S3 Dynamic**: MinIO buckets handled by `minio-mc` sidecar.
- **Search Sharding**: OpenSearch templates optimized for 1-shard per index on local machines.

### Interfaces

- **External Bridge**: `project_net` (External bridge network).
- **Service Discovery**: Docker Label based discovery for Traefik and Prometheus/Alloy.

### Security

- **Init Security**: Sidecars MUST run as non-privileged users with `no-new-privileges:true`.
- **Secret Access**: Initialization secrets MUST be scoped to the sidecar only.

### Verification (Tests/Coverage)

- **GWT Verification**: Every init-script has a matching GWT case in its corresponding spec.
- **Health Checks**: Containers MUST wait for upstream dependency healthiness before running init logic.

### Ops & Observability

- **Provisioning**: Grafana dashboards stored in `grafana/dashboards/*.json`.
- **Relabeling**: Alloy dynamic network detection for multi-repo log aggregation.
