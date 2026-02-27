# [SPEC-INFRA-03] Infrastructure Automation Specification

## 0. Pre-Implementation Checklist

- [x] Traceability: PRD-AUTO-01 and ARD-AUTO-01 references.
- [x] Security: Least-privilege sidecar tokens.
- [x] Operations: Audit trail in Loki.

## 1. Technical Overview

This specification governs the implementation of self-provisioning sidecars and automated resource readiness across the Hy-Home infrastructure. It ensures that stateful services (Postgres, MinIO, Kafka) are not only running but also provisioned with required buckets, topics, and roles before application consumers attempt connection.

## 2. Coded Requirements

| Req ID | Requirement Description | Priority |
| --- | --- | --- |
| **SPEC-AUTO-01** | Sidecars MUST exit with code 0 upon successful provisioning. | P0 |
| **SPEC-AUTO-02** | Provisioning logic MUST be idempotent (Safe for multiple runs). | P0 |
| **SPEC-AUTO-03** | Sidecars SHALL utilize exponential backoff for target service health. | P1 |

## 3. Data Modeling & Storage

- **Configuration Storage**: provisioning scripts are mounted as read-only volumes from `./provisioning/` directories.
- **State tracking**: completion status is logged to Loki; sidecars do not maintain local state.

## 4. Interfaces & Internal API

- **Service Interaction**: Sidecars interact with target services via official CLI tools (e.g., `mc`, `psql`) over `infra_net`.
- **Readiness Protocol**: Sidecars use `HEALTHCHECK` instructions or `until` loops to wait for target endpoint availability.

## 5. Component Breakdown

### 5.1 MinIO-Init Sidecar

- **Image**: `minio/mc:latest`
- **Logic**: Creates `HY_BUCKET_NAME` and sets public/private policies.

### 5.2 Postgres-Init Sidecar

- **Image**: `postgres:17-alpine`
- **Logic**: Executes SQL schema migrations or role creations using `psql`.

## 6. Edge Cases & Failure Handling

- **Service Timeout**: If the target service is not healthy within 5 minutes, the sidecar MUST fail with exit code 1 to block downstream service starts.
- **Network Flapping**: Retries MUST be randomized to prevent "thundering herd" after a stack restart.

## 7. Verification Plan

- **Test-01**: Run `docker compose up os-init` and verify index template exists via `curl`.
- **Test-02**: verify successful exit (code 0) in `docker ps -a`.

## 8. Non-Functional Requirements (NFRs)

- **Performance**: Sidecar execution SHALL NOT exceed 60 seconds.
- **Portability**: All endpoint URLs MUST use service names instead of IPs.

## 11. Related Documents

- **PRD Reference**: [[PRD-AUTO-01] Infrastructure Automation PRD](../../docs/prd/infra-automation-prd.md)
- **Architecture Reference**: [[ARD-AUTO-01] Scaling & Autonomous Patterns Reference Document](../../docs/ard/infra-automation-ard.md)
