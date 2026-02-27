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

Implementation SHALL utilize global service templates in `infra/common-optimizations.yml` via the `extends` keyword. This ensures cross-file architectural invariants:

- **`template-infra-low/med/high`**: Preferred composite templates for standardizing resource quotas, security baseline, and Loki logging.
- **`base-security`**: Core isolation baseline (`cap_drop: ALL`, `no-new-privileges: true`).
- **`base-security-hardened`**: Extends `base-security` with `read_only: true` and default `tmpfs` mounts.

Local `docker-compose.yml` files MUST define internal YAML anchors (e.g., `&labels-base`) for tier-specific metadata that cannot be captured in global generic templates.

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

## 3. Mandatory Directive Standard

To ensure schema compliance and operational visibility, every service definition MUST include:
1.  **`image`**: Pinned version tag (e.g., `redis:7.4-alpine`).
2.  **`container_name`**: Service-prefixed unique name.
3.  **`hostname`**: Identical to container name for internal DNS consistency.
4.  **`secrets`**: External references only, mapped to `/run/secrets/`.
5.  **`networks`**: Member of `infra_net` (external).
6.  **`extends`**: Config inheritance from `common-optimizations.yml`.

## Network Topology

The infrastructure utilizes a flat `infra_net` bridge for inter-service communication, isolated from host ports except through the `traefik` entrypoints.
Stateless services (exporters, proxies, UIs) MUST utilize `read_only: true` for the root filesystem. Transient write requirements MUST be handled via `tmpfs` mounts to ensure zero persistent side-effects and prevent runtime binary tampering.

## 4. Security Boundaries

- **Network Strategy**: Direct container-to-container access is restricted via tier-specific user-defined networks.
- **Credential Lifecycle**: 100% of sensitive material MUST be managed via Docker Secrets mounted at runtime, as per **[ADR-009]**.
