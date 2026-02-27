---
title: 'ADR-0007: Mandatory Resource Limits'
status: 'Accepted'
date: '2026-02-26'
authors: 'Site Reliability Engineer'
deciders: 'DevOps Team'
---

# Architecture Decision Record (ADR)

## Title: Mandatory Resource Limits

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Site Reliability Engineer
- **Deciders:** DevOps Team

## 1. Context and Problem Statement

Local workstations often freeze or experience "thrashing" when 20+ containers start simultaneously without bounds. A single memory leak in one service (e.g., OpenSearch or Kafka) can crash the entire Docker engine and the host OS.

## 2. Decision Drivers

- **Stability**: Prevent system-wide resource exhaustion on development hardware.
- **Predictability**: Ensure services have the memory they actually need to run correctly.
- **Observability**: Clearly define what "normal" resource usage looks like for each tier.

## 3. Decision Outcome

**Chosen option: "Unified Resource Reservations"**, because standardizing `deploy.resources.reservations` and `limits` in every Compose file ensures a floor for essential services and a ceiling for bursty ones, preventing OOM cascades.

### 3.1 Core Engineering Pillars Alignment

- **Performance**: Prevents noisy neighbor effects on local dev machines.
- **Observability**: Resource limits provide a baseline for alerting.
- **Scalability**: Ensures the stack can grow without unpredictable crashes.

### 3.2 Positive Consequences

- Stable local environment for multitasking developers.
- Faster detection of memory leaks (containers will restart/restart-policy).

### 3.3 Negative Consequences

- Containers might fail to start if the host is truly out of RAM (strict fail-fast).

## 4. Alternatives Considered (Pros and Cons)

### No Limits (Default)

Let Docker and the OS handle allocation dynamically.

- **Good**, because it is zero-config and flexible.
- **Bad**, because it causes kernel panic or UI lag on shared workstations when one service goes rogue.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Industry standard for reliable container deployments.
- **Technical Requirements Addressed**: REQ-PRD-SYS-01, REQ-PRD-BASE-07
