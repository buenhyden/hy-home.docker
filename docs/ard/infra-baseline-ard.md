# ARD: Infrastructure Architecture

## [REQ-SPT-05] Technical Specification

### Architecture Overview

The system follows a **Layered Modular Orchestration** pattern. A root orchestrator (`docker-compose.yml`) aggregates specialized service stacks from a multi-tier directory structure (`infra/`) using the `include` feature of Docker Compose v2.

- **Standalone Stack**: 루트 `include` 없이 별도 Compose로 운영 가능한 서비스(예: Supabase)

### Labeling Standards

To ensure consistent service discovery and telemetry, all infra services SHOULD include the following labels:

- `hy-home.scope`: Set to `infra` for system services, `app` for user applications.
- `hy-home.tier`: The category name (e.g., `gateway`, `auth`, `data`).
- `observability.logs`: Explicitly set to `"true"` to enable log scraping.
- `traefik.enable`: Set to `"true"` if the service needs external routing.

### Components (Tiers)

1. **Gateway (01-gateway)**: Edge routing and SSL termination (Traefik).
2. **Auth (02-auth)**: Identity management (Keycloak).
3. **Security (03-security)**: Secret vaulting (Vault).
4. **Data (04-data)**: Persistence layers (Postgres, MinIO, OpenSearch).
5. **Messaging (05-messaging)**: Async communication (Kafka).
6. **Observability (06-observability)**: LGTM stack.
7. **Workflow (07-workflow)**: Orchestration (Airflow, n8n).
8. **AI (08-ai)**: Local LLM inference (Ollama).
9. **Tooling (09-tooling)**: DevOps utilities.
10. **Communication (10-communication)**: Mail services.

### Storage Strategy

- **Volumes**: Standard Docker named volumes for persistence.
- **Object Storage**: MinIO for S3-compatible workloads.
- **Cluster HA**: Patroni for PostgreSQL HA clusters.

### Interface & Networking

- **Internal**: `infra_net` bridge for inter-service communication.
- **External**: `project_net` for app integration; `kind` for K8s bridging.
- **Ingress**: Traefik handles HTTP/HTTPS routing via Docker labels.

### Security Implementation

- **Secret Management**: Mandatory use of Docker Secrets. Files in `secrets/*.txt` are mounted at runtime.
- **Container Hardening**:
  - `no-new-privileges: true`
  - `cap_drop: [ALL]`
  - User namespaces (where applicable).

### Non-Functional Requirements (NFR)

- **High Availability**: PostgreSQL and Kafka stacks SHALL use multi-node replication (Patroni/KRaft).
- **Security Density**: Standard Linux capabilities SHALL be dropped by default (`cap_drop: [ALL]`).
- **Resource Limits**: Every service MUST have `deploy.resources.limits` to prevent OOM events.

### Verification Plan (Tests/Coverage)

- **Static Validation**: `scripts/validate-docker-compose.sh` for YAML schema check.
- **Security Scan**: Regular `trivy` or `docker scan` on core images.
- **Traceability**: Requirements map directly to task tables in `specs/`.

### Ops & Observability

- **Logs**: Loki integration via Alloy.
- **Metrics**: Prometheus with direct scrape or Alloy.
- **Traces**: OTLP ingest into Tempo.
