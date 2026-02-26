# [SPEC-INFRA-02] Infrastructure Implementation Baseline

- **Role**: Infrastructure Architect
- **Purpose**: Define core setup and security hardening requirements for the primary infrastructure engine.
- **Activates When**: Modifying root `docker-compose.yml` or Tier-1 service configurations.

## 1. Standards

### Principles

- **[REQ-BSL-01] Registry Integrality**: The root `docker-compose.yml` SHALL serve as the master registry for all `infra/` modules using the `include` pattern.
- **[REQ-BSL-02] Driver Standardisation**: All system-level services MUST utilize the `loki` log driver for centralized telemetry.
- **[REQ-BSL-03] Secrets Hermeticity**: Persistent credentials SHALL ALWAYS utilize Docker Secrets via the `/run/secrets/` path.

## 2. Technical Specification [REQ-SPT-05]

### 2.1 Non-Functional Requirements (NFR)

- **NFR-BOOT-01**: Cold-start bootstrap (Day-0) MUST complete in < 10 mins.
- **NFR-SEC-01**: Base images SHOULD be scanned for critical vulnerabilities monthly.

### 2.2 Storage Strategy

- **ST-01**: Host-level data persistence SHALL utilize `${DEFAULT_DATA_DIR}` for deterministic pathing.
- **ST-02**: Volumes and networks MUST be defined with explicit names to prevent collision across tiers.

### 2.3 Interfaces

- **INF-01**: The ingress layer (Traefik) SHALL be the sole entry point for external websecure traffic.
- **INF-02**: Internal services SHALL utilize the `infra_net` bridge for backend communication.

### 2.4 Security

- **SEC-01**: Every container `security_opt` MUST include `no-new-privileges:true`.
- **SEC-02**: Explicit `cap_drop: ALL` is mandatory for all internet-facing services.

### 2.5 Ops & Observability

- **OBS-01**: Every service definition SHALL include healthchecks verifying internal readiness.

## 3. Verification & Acceptance Criteria (GWT) [REQ-SPT-10]

### [AC-BSL-01] Aggregated Config Verification

- **Given**: A modular infrastructure directory structure.
- **When**: Executing `docker compose config` from the root.
- **Then**: All sub-tier services MUST be present in the flattened output.

### [AC-BSL-02] Bootstrap Failure Condition

- **Given**: A missing `.env` file or empty `secrets/` directory.
- **When**: Running the infrastructure orchestration.
- **Then**: The engine MUST fail with a clear diagnostic message regarding missing prerequisites.

### [AC-BSL-03] Telemetry Standardisation

- **Given**: A Tier-1 service (e.g. Traefik).
- **When**: Inspecting container log configuration.
- **Then**: The log type MUST BE exactly `loki`.
