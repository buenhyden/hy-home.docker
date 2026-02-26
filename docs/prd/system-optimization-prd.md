# [PRD-SYS-01] Hy-Home System Optimization

## 1. Vision

Establish a high-performance, secure, and observable home server infrastructure that provides a deterministic foundation for both AI workloads and standard development workflows.

## 2. Personas [REQ-SPT-08]

- **Persona: Hy (Developer)**: Wants a fast, reliable local environment where services are pre-integrated with security and logging by default.
- **Persona: Platform Architect**: Requires a standardized configuration model that reduces technical debt and simplifies cross-tier auditing.

## 3. Success Metrics [REQ-SPT-01]

- **Metric-01 (Security)**: 100% of services SHALL pass a `docker inspect` audit verifying `no-new-privileges: true` and `cap_drop: ALL`.
- **Metric-02 (Observability)**: 100% of infrastructure logs MUST be indexed in Loki with `hy-home.tier` metadata tags.
- **Metric-03 (Performance)**: Cold startup time for the core gateway (NGINX/Traefik) SHALL be < 15 seconds.

## 4. Use Cases [REQ-SPT-04]

- **[UC-SYS-01]**: A developer deploys a new database service, and it automatically inherits Loki logging and security constraints via include-templates.
- **[UC-SYS-02]**: An architect monitors real-time resource contention across the 'data' and 'observability' tiers using unified Grafana dashboards.

## 5. Scope

- **In-Scope**: `infra/` service refactoring, root orchestration hardening, metadata standardization, and local YAML anchor strategy.
- **Out-of-Scope**: Application-level logic, external cloud provider integration, or migration to Kubernetes.

## 6. Requirements [REQ-SPT-03]

- **[REQ-SYS-01]**: The system SHALL provide standardized YAML anchors for security baselines to prevent configuration drift.
- **[REQ-SYS-02]**: Every service MUST be integrated with the Loki logging driver with job-specific labels.
- **[REQ-SYS-03]**: Service startup MUST be ordered via `service_healthy` conditions to prevent race conditions.
- **[REQ-SYS-04]**: The system SHALL utilize Docker Compose `include` to propagate optimization blocks (`x-optimizations`) across all service tiers.

## 7. Acceptance Criteria [REQ-SPT-10] [REQ-SPT-06]

- **AC-1 (Given-When-Then)**: Given a running service, When queried via `docker inspect`, Then `CapDrop` MUST contain `ALL`.
- **AC-2**: Given the Loki dashboard, When logs are generated, Then they MUST contain the `hy-home.tier` label matching the service directory.
- **AC-3**: Given a full stack start, When `docker compose up` is executed, Then the Gateway SHALL only start after the Identity Provider is healthy.
