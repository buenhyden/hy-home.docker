# [SPEC-INFRA-03] Infrastructure Automation Specification

- **Role**: Platform Engineer / DevOps Architect
- **Purpose**: Define implementation standards for self-provisioning sidecars and automated resource readiness.
- **Activates When**: Creating or modifying "Init" services (`os-init`, `k-init`) or automated dashboard pipelines.

## 1. Standards

### Principles

- **[REQ-AUTO-01] Idempotency Primacy**: All automation sidecars MUST BE strictly idempotent. Subsequent runs SHALL NOT produce errors if resources already exist.
- **[REQ-AUTO-02] Readiness Blocking**: Init containers MUST block dependent application startup until core backend services (9200, 9092) are functionally reachable.
- **[REQ-AUTO-03] Fail-Fast Execution**: Sidecars SHALL exit with code 1 upon unrecoverable configuration errors to stop downstream deployment.

## 2. Technical Specification [REQ-SPT-05]

### 2.1 Non-Functional Requirements (NFR)

- **NFR-AUTO-01**: Sidecar initialization SHALL complete in < 60 seconds post-backend readiness.
- **NFR-RES-01**: Sidecars MUST use the `template-infra-low` resource profile to minimize overhead.

### 2.2 Storage Strategy

- **ST-01**: Automation scripts SHALL reside in tier-specific `scripts/` directories.
- **ST-02**: Configuration templates MUST be mounted as read-only volumes.

### 2.3 Interfaces

- **INF-01**: Sidecars SHALL utilize standard Docker `depends_on` conditions (`service_healthy`).
- **INF-02**: Logs MUST be exported to Loki for auditing automation results.

### 2.4 Security

- **SEC-01**: Automation containers MUST NOT run with `privileged: true`.
- **SEC-02**: Access to backend APIs MUST utilize specialized service accounts with least privilege.

### 2.5 Ops & Observability

- **OBS-01**: Every sidecar SHALL log its version and environment state upon startup for troubleshooting.

## 3. Verification & Acceptance Criteria (GWT) [REQ-SPT-10]

### [AC-AUTO-01] OpenSearch Index Readiness

- **Given**: An uninitialized OpenSearch cluster.
- **When**: The `opensearch-init` service completes successfully.
- **Then**: The mapping API MUST return 200 OK for the `infra-logs` template.

### [AC-AUTO-02] Kafka Topic Persistence

- **Given**: A Kafka cluster with zero topics.
- **When**: `kafka-init` exits with code 0.
- **Then**: `kafka-topics --list` MUST contain the required system topics with the correct partition count.

### [AC-AUTO-03] Idempotency Validation

- **Given**: A previously initialized resource.
- **When**: Running the automation sidecar for the second time.
- **Then**: The container MUST exit with code 0 or log a "resource exists" warning without failing.
