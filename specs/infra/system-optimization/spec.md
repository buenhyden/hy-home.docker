# [SPEC-INFRA-04] Infrastructure Hardening & Optimization

- **Role**: Reliability & Security Engineer
- **Purpose**: Define standards for system isolation, resource density, and security hardening across the hy-home ecosystem.
- **Activates When**: Performing security audits or optimizing existing container workloads.

## 1. Standards

### Principles

- **[REQ-HARD-01] Universal Isolation**: All infrastructure containers SHALL BE isolated from host-level namespaces (`pid`, `network`, `ipc`) unless explicitly documented as a functional dependency.
- **[REQ-HARD-02] Resource Density Primacy**: Infrastructure services MUST NOT consume more than 20% of aggregate system memory under idle conditions.
- **[REQ-HARD-03] Immutable Execution**: Every container SHALL utilize read-only root filesystems wherever functionally feasible.

## 2. Technical Specification [REQ-SPT-05]

### 2.1 Non-Functional Requirements (NFR)

- **NFR-SEC-01**: Host-to-Container escape vectors MUST be mitigated via restricted kernel capability sets.
- **NFR-OBS-01**: Centralized log ingestion SHALL maintain a p95 latency of < 2 seconds.

### 2.2 Storage Strategy

- **ST-01**: Persistent mounts SHALL utilize `bind` mounts for deterministic IO performance.
- **ST-02**: All sensitive volumes MUST be restricted to owner-only permissions on the host system.

### 2.3 Interfaces

- **INF-01**: Interservice communication SHALL BE restricted to the dedicated `infra_net`.
- **INF-02**: External exposing of infrastructure-only ports is STRICTLY PROHIBITED.

### 2.4 Security

- **SEC-01**: `no-new-privileges: true` MUST BE present in every production service runtime.
- **SEC-02**: The `cap_drop: ALL` flag is mandatory for all non-privileged sidecars.

### 2.5 Ops & Observability

- **OBS-01**: Operational metrics SHALL BE collected via standard OTLP or Prometheus exporters.

## 3. Verification & Acceptance Criteria (GWT) [REQ-SPT-10]

### [AC-HARD-01] Privilege Escalation Protection

- **Given**: A deployed infrastructure container.
- **When**: Running `docker inspect --format '{{.HostConfig.SecurityOpt}}' <container>`.
- **Then**: The output MUST explicitly contain `no-new-privileges:true`.

### [AC-HARD-02] Resource Ceiling Enforcement

- **Given**: A service deployed with the `template-infra-high` template.
- **When**: Synthetic load is applied to the service.
- **Then**: The container MUST NOT exceed a memory utilization of `2GiB`.

### [AC-HARD-03] Log Ingestion Consistency

- **Given**: A critical log event in any tier.
- **When**: Inspecting the Loki aggregation point.
- **Then**: The event MUST BE searchable and present within 5 seconds of occurrence.
