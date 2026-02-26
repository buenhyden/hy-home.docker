# Architecture Decision Record (ADR)

_Target Directory: `docs/adr/adr-0005-sidecar-resource-initialization.md`_

## Title: adr-0005: Sidecar-Driven Resource Initialization

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** DevOps Engineer
- **Deciders:** Engineering Team

## 1. Context and Problem Statement

Manual bucket creation in MinIO, topic creation in Kafka, or index template setup in OpenSearch is error-prone and violates the principle of "Immutable Infrastructure". These steps are often forgotten during stack bootstrap.

## 2. Decision Drivers

- **Automation**: Zero-touch provisioning on Day-0.
- **Reliability**: Ensure dependencies (buckets/topics) exist before application start.
- **Idempotency**: Setup scripts must be safe to rerun.

## 3. Decision Outcome

**Chosen option: "Init-Sidecar Pattern"**, because utilizing one-off containers (e.g., `minio/mc`, `curlimages/curl`) that wait for the core service to be healthy ensures that all required resources are provisioned automatically without manual intervention.

### 3.1 Core Engineering Pillars Alignment

- **Architecture**: Promotes autonomous service discovery and setup.
- **Security**: Sidecar users are scoped only to resource initialization permissions.

### 3.2 Positive Consequences

- Self-healing resources.
- Fully automated stack recovery.

### 3.3 Negative Consequences

- Increased container count on host.
- Slightly higher resource overhead during initial startup.

## 4. Alternatives Considered

### Manual CLI Commands

- **Good**: No extra containers.
- **Bad**: High human error rate; not reproducible.

## 5. Confidence Level

- **Confidence Rating**: High
- **Notes**: Battle-tested pattern in Kubernetes (InitContainers).
