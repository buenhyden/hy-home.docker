---
title: 'Infrastructure Global Baseline Specification'
status: 'Validated'
version: '1.0'
owner: 'Principal Infrastructure & Reliability Architect'
prd_reference: '/docs/prd/infra-baseline-prd.md'
api_reference: 'N/A'
arch_reference: '/docs/ard/system-optimization-ard.md'
tags: ['spec', 'implementation', 'infra', 'baseline']
---

# [SPEC-INFRA-01] Infrastructure Global Baseline Specification

> **Status**: Validated
> **Related PRD**: [/docs/prd/infra-baseline-prd.md](/docs/prd/infra-baseline-prd.md)
> **Related Architecture**: [/docs/ard/system-optimization-ard.md](/docs/ard/system-optimization-ard.md)

_Target Directory: `specs/infra/global-baseline/spec.md`_

---

## 0. Pre-Implementation Checklist (Governance)

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Modular Compose | Section 1         |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | Tier Isolation  | Section 1         |
| Backend Stack      | Are language/framework/libs decided?                  | Must     | Docker Compose  | Section 1         |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | Config Linting  | Section 7         |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | Docker Secrets  | Section 4         |
| Data Protection | Encryption/access policies for sensitive data? | Must     | Least Privilege | Section 9         |

## 1. Technical Overview & Architecture Style

This specification defines standard extension fields and service templates for cross-file inheritance for the hy-home ecosystem.

- **Component Boundary**: Global configuration invariants and resource templates.
- **Key Dependencies**: `infra/common-optimizations.yml`
- **Tech Stack**: Docker Compose v2.20+

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **[REQ-INF-01]** | Global Inheritance Primacy: All infrastructure services SHALL extend from a baseline template in `infra/common-optimizations.yml`. | Critical | REQ-PRD-FUN-06 |
| **[REQ-INF-02]** | Mandatory Least Privilege: All containers MUST drop all capabilities (`cap_drop: ALL`) and prohibit privilege escalation (`no-new-privileges: true`). | Critical | REQ-SYS-04 |
| **[REQ-INF-03]** | Standardized Resource Quotas: Every service definition SHALL define CPU and Memory limits using established profiles (Low/Med/High). | High     | REQ-PRD-MET-03 |
| **[REQ-INF-04]** | Environment Portability: All services MUST rely on internal DNS for discovery; explicit static IPs are PROHIBITED [ADR-0008]. | Critical | REQ-SYS-05      |
| **[REQ-INF-05]** | Managed Process Lifecycle: All services MUST utilize `init: true` for robust signal handling [ADR-0012]. | High     | REQ-SYS-06      |
| **[REQ-INF-06]** | Functional Metadata Overlays: Services SHALL maintain local `labels` for service-specific functional requirements (e.g. Traefik rules) while extending global security invariants. | Medium   | REQ-SYS-08 |

## 3. Data Modeling & Storage Strategy

- **Database Engine**: Containerized local storage.
- **Schema Strategy**: Deterministic volume mounting.
- **Migration Plan**: YAML anchor-to-extends migration.

## 4. Interfaces & Data Structures

- **Common Interface**: `infra_net` bridge network.
- **Logging Interface**: `loki` driver aggregation point.

## 5. Component Breakdown

- **`infra/common-optimizations.yml`**: Primary inheritance template provider.

## 6. Edge Cases & Error Handling

- **Error**: Unknown extension fields -> `docker compose config` validation failure.
- **Error**: Overlapping limits -> Container runtime OOM or throttling.

## 7. Verification Plan (Testing & QA) [REQ-SPT-10]

- **[REQ-SPC-010] External Secret Reference**: Services SHALL reference secrets as `external: true` to source from the root compose.
- **[REQ-SPC-011] Version Pinning Enforcement**: The use of `latest` image tags is PROHIBITED.
- **[VAL-SPC-007] Network Isolation Check**: `docker compose config` must verify no services expose `ports` directly to the host except for Gateway tier.

- **[VAL-SPC-001] Security Baseline Verification**:
  - **Given**: A service definition inheriting from `base-security`.
  - **When**: Inspecting via `docker inspect <container_name> --format '{{.HostConfig.SecurityOpt}}'`.
  - **Then**: JSON output MUST contain `no-new-privileges:true`.

- **[VAL-SPC-002] Resource Quota Enforcement**:
  - **Given**: A container running with the `template-infra-low` profile.
  - **When**: Inspecting container limits via `docker stats --no-stream --format "{{.MemLimit}}"`.
  - **Then**: Memory limit MUST be exactly `256MiB` (as defined in `infra/common-optimizations.yml`).

  - **Then**: Structured logs MUST appear in the centralized plane.

- [VAL-SPC-004] DNS-Based Connectivity Verification:
  - Given: Two services on the infra_net bridge.
  - When: Executing ping -c 1 <service_name> from one container to another.
  - Then: ICMP response MUST be received without IP-level configuration.

- [VAL-SPC-006] Filesystem Immutability Verification:
  - Given: A stateless service (e.g., pg-exporter).
  - When: Inspecting via docker inspect <container> --format '{{.HostConfig.ReadonlyRootfs}}'.
  - Then: Boolean value MUST be true.

- **[VAL-SPC-005] Init Process Verification**:
  - **Given**: A running container.
  - **When**: Inspecting via `docker inspect --format '{{.Config.Init}}'`.
  - **Then**: Output MUST be `true`.

## 8. Non-Functional Requirements (NFR) & Scalability

- **Reliability**: termination handling via `unless-stopped` policy.
- **Efficiency**: Idle memory utilization MUST NOT exceed 4GB aggregate.

## 9. Operations & Observability

- **Monitoring**: Prometheus scraping of container resources.
- **Logging**: Mandatory Loki forwarding.
- **Identity**: Root execution inside containers is STRICTLY PROHIBITED.
