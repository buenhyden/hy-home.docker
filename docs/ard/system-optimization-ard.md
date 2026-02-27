---
title: '[ARD-OPT-01] Optimized Infrastructure Reference'
status: 'Approved'
owner: 'Reliability Engineer'
prd_reference: '../prd/system-optimization-prd.md'
adr_references: ['../adr/adr-0008-removing-static-docker-ips.md', '../adr/adr-0012-standardized-init-process.md', '../adr/adr-0013-configuration-deduplication.md']
---

# Architecture Reference Document (ARD)

> **Status**: Approved
> **Owner**: Reliability Engineer
> **PRD Reference**: [[REQ-PRD-SYS-01] Hy-Home System Optimization](../prd/system-optimization-prd.md)
> **ADR References**: [ADR-0008](../adr/adr-0008-removing-static-docker-ips.md), [ADR-0012](../adr/adr-0012-standardized-init-process.md), [ADR-0013](../adr/adr-0013-configuration-deduplication.md)

---

## 1. Executive Summary

A hardened configuration model for the Hy-Home ecosystem focusing on resource density, kernel-level security options, and unified observability. Extends the baseline with surgical technical invariants for high-reliability hosting.

## 2. Business Goals

- Ensure 100% auditable security posture across all tiers.
- Achieve sub-4GB host RAM utilization for standard local operation.
- Provide zero-portability-risk configurations for developers.

## 3. System Overview & Context

```mermaid
graph TD
    subgraph "Infrastructure Tiers"
        T1[Tier 1: Gateway]
        T2[Tier 2: Identity]
        T3[Tier 3: Stateful Data]
        T4[Tier 4: Observability]
    end
    
    T1 <--> T2
    T1 <--> T3
    T3 --> T4
```

## 4. Component Architecture & Tech Stack Decisions

### 4.1 Standardization Patterns

Implementation utilizes global service templates in `infra/common-optimizations.yml` via the `extends` keyword:

- **`template-infra-low/med/high`**: Standardizing resource quotas and security base.
- **`base-security-hardened`**: Mandatory `read_only: true` with `tmpfs` support.

### 4.2 Technology Stack

- **Hardening**: `security_opt` (no-new-privileges), `cap_drop` (ALL).
- **Engine Directives**: `init: true`, driver-level `logging`.
- **Naming**: Unified `container_name` and `hostname` standards.

## 5. Data Architecture

- **Path Abstraction**: 100% of host volumes SHALL use `${DEFAULT_*_DIR}` variables.
- **Telemetry Architecture**:

```mermaid
graph LR
    S[Services] -- Loki Driver --> L[Loki]
    S -- Scrape --> A[Alloy]
    A --> P[Prometheus]
    A --> T[Tempo]
```

## 6. Security & Compliance

- **Network Isolation**: Tier-specific user-defined networks restricting cross-segment traffic.
- **Credential Lifecycle**: 100% runtime injection via Docker Secrets.
- **Runtime Integrity**: Immutable root filesystems and disabled binary execution escalation.

## 7. Infrastructure & Deployment

- **Orchestration**: Aggregated via root `docker-compose.yml` using the `include` directive.
- **Profiles**: Implements `core`, `data`, `obs`, `messaging`, `ai` profiles for selective startup.

## 8. Non-Functional Requirements (NFRs)

- **Resource Efficiency**: Aggregate idle RAM utilization MUST remain under 4GB.
- **Observability Stability**: 100% of service logs MUST be searchable in Loki with `hy-home.tier` labels.
- **Response Accuracy**: Sub-2s ingestion latency for all telemetry pipelines.

## 9. Architectural Principles, Constraints & Trade-offs

- **What NOT to do**: Use absolute host paths in compose files.
- **Trade-offs**: template inheritance increases configuration resolution complexity but ensures global standard enforcement.
- **Known Limitations**: `read_only` filesystems require manual identification of all writeable directories for `tmpfs` mapping.
