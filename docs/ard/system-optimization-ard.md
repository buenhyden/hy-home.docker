# [ARD-SYS-01] Optimized Infrastructure Architecture Reference

## 1. System Topology

The Hy-Home infrastructure utilizes a multi-tier, isolated container topology to minimize blast radius and ensure operational stability.

### 1.1 Infrastructure Tiers

- **Tier 1 (Gateway)**: Core ingress tier (Traefik/NGINX) handling TLS termination and internal routing.
- **Tier 2 (Identity & Auth)**: Keycloak and OAuth2 Proxy managing centralized OIDC authentication.
- **Tier 3 (Stateful Data)**: Dedicated clusters for PostgreSQL, Valkey, and MinIO with isolated network segments.
- **Tier 4 (Observability Stack)**: Unified LGTM pipeline (Loki, Grafana, Tempo, Alloyl) collecting cross-tier telemetry.

## 2. Standardization Patterns [[SPEC-INFRA-01]](/specs/infra/global-baseline/spec.md)

To ensure consistency across heterogeneous service stacks, the following architectural patterns are enforced:

### 2.1 Configuration Inheritance (`extends`)

Implementation SHALL utilize global service templates in `infra/common-optimizations.yml` via the `extends` keyword to ensure cross-file architectural invariants across all service tiers:

- **`template-infra-low/med/high`**: Standardized service templates combining resource quotas, security baseline, and restart policies.
- **`base-security`**: Universal `cap_drop: ALL` and `no-new-privileges: true` baseline.
- **`base-resource-low/med/high`**: Specific resource quota presets (`deploy.resources`).

Local `docker-compose.yml` files MUST define their own internal YAML anchors for labels (`&labels-base`) and logging (`&logging-loki`) to maintain file independence and handle container-specific metadata properly.

### 2.2 Telemetry Architecture

```mermaid
graph TD
    subgraph Services
        S1[Tier 1: Gateway]
        S2[Tier 2: Auth]
        S3[Tier 3: Data]
    end
    subgraph Collector
        A[Grafana Alloy]
    end
    subgraph Storage
        L[Loki: Logs]
        P[Prometheus: Metrics]
        T[Tempo: Traces]
    end

    S1 & S2 & S3 -- "Push Logs (Loki Driver)" --> L
    S1 & S2 & S3 -- "Osh Scrape" --> A
    A -- "Remote Write" --> P
    A -- "Export Traces" --> T

### 2.3 Network Portability [ADR-0008]

All infrastructure services SHALL operate without explicit `ipv4_address` assignments. Service discovery is performed via:
- **Internal DNS**: Relying on Docker's embedded DNS server and service names within the `infra_net` bridge.
- **Service Aliases**: Utilizing network aliases for cross-stack compatibility where services belong to multiple networks.

### 2.4 Standardized Init Process [ADR-0012]

Every containerized service MUST utilize `init: true` to ensure robust signal handling (SIGTERM/SIGINT) and the proper reaping of zombie processes. This improves observability stability and ensures clean shutdowns during orchestration events.
```

## 3. Security Boundaries

- **Network Strategy**: Direct container-to-container access is restricted via tier-specific user-defined networks.
- **Credential Lifecycle**: 100% of sensitive material MUST be managed via Docker Secrets mounted at runtime, as per **[ADR-009]**.
