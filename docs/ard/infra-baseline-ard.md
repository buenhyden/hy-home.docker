---
title: '[ARD-BASE-01] Infrastructure Baseline Reference'
status: 'Approved'
owner: 'Platform Architect'
prd_reference: '../prd/infra-baseline-prd.md'
adr_references: ['../adr/adr-0001-root-orchestration-include.md']
---

# Architecture Reference Document (ARD)

> **Status**: Approved
> **Owner**: Platform Architect
> **PRD Reference**: [[REQ-PRD-BASE-01] Infrastructure Baseline PRD](../prd/infra-baseline-prd.md)
> **ADR References**: [ADR-0001](../adr/adr-0001-root-orchestration-include.md) to [ADR-0004](../adr/adr-0004-tiered-directory-structure.md)

---

## 1. Executive Summary

A modular service orchestrator utilizing Docker Compose v2 `include` to manage a multi-tier infrastructure stack. This baseline focuses on security consistency, ease of bootstrap, and local environment stability for the Hy-Home ecosystem.

## 2. Business Goals

- Provide a reproducible local sandbox for DevOps pattern testing.
- Minimize "Day-0" installation time for new contributors.
- Enforce production-grade security standards in a local development context.

## 3. System Overview & Context

```mermaid
C4Context
    title Infrastructure System Context
    Person(dev, "Developer", "Uses local infra for app testing")
    System(infra, "Hy-Home Infra", "LGTM stack, PG Cluster, Kafka, MinIO")
    System_Ext(docker, "Docker Host", "Provides container runtime")

    Rel(dev, infra, "Bootstraps via CLI")
    Rel(infra, docker, "Runs on")
```

## 4. Component Architecture & Tech Stack Decisions

### 4.1 Component Architecture

```mermaid
C4Container
    title Infra Tier Hierarchy
    Container(gateway, "Gateway Tiers", "Traefik", "SSL & Routing")
    Container(data, "Data Tier", "Postgres/MinIO/OpenSearch", "Persistence")
    Container(obs, "Observability", "LGTM Stack", "Telemetry")

    Rel(gateway, data, "Routes to")
    Rel(data, obs, "Sends logs/metrics")
```

### 4.2 Technology Stack

- **Orchestration**: Docker Compose v2.20+ (`include` / `extends`)
- **Gateway/Ingress**: Traefik 3.x
- **Core Data**: PostgreSQL 17 (Patroni), Kafka 3.9+ (KRaft), MinIO (S3 compatible)
- **Init System**: `tini` (Docker-integrated `init: true`)

## 5. Data Architecture

- **Domain Model**: Tiered service folders (`01-gateway`, `04-data`, etc.)
- **Storage Strategy**: Bind mounts to `${DEFAULT_DATA_DIR}` for persistent data.
- **Data Flow**: Direct container push to Loki for logs; sidecar initialization for schema readiness.

## 6. Security & Compliance

- **Authentication**: Centralized OIDC via Keycloak.
- **Secrets**: 100% file-based secrets in `secrets/*.txt` via Docker Secret API.
- **Hardening**: Global enforcement of `cap_drop: [ALL]` and `no-new-privileges: true`.

## 7. Infrastructure & Deployment

- **Deployment Hub**: Local Linux/macOS host with Docker Engine.
- **Orchestration**: Root `docker-compose.yml` aggregating sub-stacks via `include`.
- **CI/CD Pipeline**: Pre-commit hooks for YAML and Markdown validation.

## 8. Non-Functional Requirements (NFRs)

- **Availability**: 3-node HA clusters for critical data path (Kafka/Postgres).
- **Performance**: Bootstrap time SHALL be < 10 mins on standard SSD hardware.
- **Scalability**: Config inheritance allows adding tiers without modifying root logic.

## 9. Architectural Principles, Constraints & Trade-offs

- **What NOT to do**: Use static IP addresses for inter-service communication.
- **Constraints**: Limited by host RAM (target < 4GB idle footprint).
- **Chosen Path Rationale**: Docker Compose chosen for low overhead and developer familiarity over local K8s.
- **Known Limitations**: Lacks the native service discovery features of a full mesh.
