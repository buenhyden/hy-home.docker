---
title: 'ADR-0005: Sidecar-Driven Resource Initialization'
status: 'Accepted'
date: '2026-02-26'
authors: 'DevOps Engineer'
deciders: 'Engineering Team'
---

# Architecture Decision Record (ADR)

## Title: Sidecar-Driven Resource Initialization

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** DevOps Engineer
- **Deciders:** Engineering Team

## 1. Context and Problem Statement

Manual bucket creation in MinIO, topic creation in Kafka, or index template setup in OpenSearch is error-prone and violates the principle of "Immutable Infrastructure". These steps are often forgotten during stack bootstrap, causing application failure at runtime.

## 2. Decision Drivers

- **Automation**: Zero-touch provisioning on Day-0 for application readiness.
- **Reliability**: Ensure dependencies exist before the consuming application starts.
- **Idempotency**: Setup scripts must be safe to rerun without side effects.

## 3. Decision Outcome

**Chosen option: "Init-Sidecar Pattern"**, because utilizing one-off containers that wait for core services to be healthy ensures that all required resources are provisioned automatically.

### 3.1 Core Engineering Pillars Alignment

- **Architecture**: Promotes autonomous service discovery and setup.
- **Security**: Sidecar users are scoped only to resource initialization permissions.
- **Observability**: Provisioning sequences are logged to Loki for audit.

### 3.2 Positive Consequences

- Self-healing resources on every stack restart.
- Fully automated stack recovery without manual CLI steps.

### 3.3 Negative Consequences

- Increased container count on the host.
- Slightly higher resource overhead during the first 60 seconds of startup.

## 4. Alternatives Considered (Pros and Cons)

### Manual CLI Commands

Run `mc` or `kafka-topics` manually from the host.

- **Good**, because zero extra container overhead.
- **Bad**, because high human error rate and not reproducible in CI.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Standard pattern in Kubernetes (InitContainers) adapted for Compose.
- **Technical Requirements Addressed**: REQ-PRD-AUTO-01, REQ-PRD-BASE-05
