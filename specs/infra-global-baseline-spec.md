# [SPEC-INFRA-01] Infrastructure Global Baseline Specification

- **Role**: Principal Infrastructure & Reliability Architect
- **Purpose**: Define standard extension fields and service templates for cross-file inheritance for the hy-home ecosystem.
- **Activates When**: Drafting Product Requirements Documents (PRDs), refining user stories, or creating technical specifications for system components within the infrastructure domain.

## 1. Standards

### Principles

- **[REQ-INF-01] Global Inheritance Primacy**: All infrastructure services SHALL extend from a baseline template in `infra/common-optimizations.yml` to ensure architectural consistency.
- **[REQ-INF-02] Mandatory Least Privilege**: All containers MUST drop all capabilities (`cap_drop: ALL`) and prohibit privilege escalation (`no-new-privileges: true`) unless explicitly granted in a tier-specific specification.
- **[REQ-INF-03] Standardized Resource Quotas**: Every service definition SHALL define CPU and Memory limits using one of the established standard profiles (Low/Med/High).

## 2. Technical Specification [REQ-SPT-05]

### 2.1 Non-Functional Requirements (NFR)

- **NFR-REL-01**: Every service SHALL handle unexpected termination via an `unless-stopped` restart policy.
- **NFR-PERF-01**: Infrastructure services MUST NOT collectively exceed 4GB RAM utilization under idle conditions.

### 2.2 Storage Strategy

- **ST-01**: All persistent data SHALL reside in `${DEFAULT_DATA_DIR}` using local bind mounts for maximum host-level observability.
- **ST-02**: Secrets MUST be injected via Docker Secrets (`/run/secrets/`) and NEVER committed as plain text.

### 2.3 Interfaces

- **INF-01**: All services SHALL utilize the `infra_net` bridge network for inter-tier communication.
- **INF-02**: All logs SHALL be exported via the `loki` driver to the centralized LGTM stack.

### 2.4 Security

- **SEC-01**: Root user execution inside any production container is STRICTLY PROHIBITED.
- **SEC-02**: All infrastructure components MUST be isolated from the host `pid`, `network`, and `ipc` namespaces by default.

### 2.5 Ops & Observability

- **OBS-01**: Every service SHALL be tagged with standard metadata (`hy-home.tier`, `hy-home.managed`) for automated filtering.

## 3. Verification & Acceptance Criteria (GWT) [REQ-SPT-10]

### [AC-INF-01] Security Baseline Verification

- **Given**: A service definition inheriting from `base-security`.
- **When**: Executing `docker compose config`.
- **Then**: The resulting JSON MUST show `security_opt: ["no-new-privileges:true"]`.

### [AC-INF-02] Resource Quota Enforcement

- **Given**: A container running with the `template-infra-low` profile.
- **When**: Inspecting container limits via `docker stats --no-stream`.
- **Then**: The memory limit MUST BE exactly `128MiB`.

### [AC-INF-03] Telemetry Compliance

- **Given**: A newly deployed infrastructure service.
- **When**: Querying Loki with `{job="infra"}`.
- **Then**: The server MUST produce structured logs within the centralized dashboard.
