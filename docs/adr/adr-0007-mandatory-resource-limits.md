# Architecture Decision Record (ADR)

_Target Directory: `docs/adr/adr-0007-mandatory-resource-limits.md`_

## Title: adr-0007: Mandatory Resource Limits

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Site Reliability Engineer
- **Deciders:** DevOps Team

## 1. Context and Problem Statement

Local workstations often freeze or experience "thrashing" when 20+ containers start simultaneously without bounds. A single memory leak in one service can crash the entire Docker engine.

## 2. Decision Drivers

- **Stability**: Prevent system-wide resource exhaustion.
- **Predictability**: Ensure services have the memory they actually need to run correctly.
- **Observability**: Clearly define what "normal" resource usage looks like.

## 3. Decision Outcome

**Chosen option: "Unified Resource Reservations"**, because standardizing `deploy.resources.reservations` and `limits` in every Compose file ensures a floor for essential services and a ceiling for bursty ones, preventing OOM cascades.

### 3.1 Core Engineering Pillars Alignment

- **Performance**: Prevents noisy neighbor effects on local dev machines.
- **Quality**: Forces developers to consider the footprint of their services.

### 3.2 Positive Consequences

- Stable local environment.
- Faster detection of memory leaks.

### 3.3 Negative Consequences

- Containers might fail to start if the host is truly out of RAM (fail-fast instead of thrashing).

## 4. Alternatives Considered

### No Limits (Default)

- **Good**: Maximum flexibility.
- **Bad**: Causes kernel panic or UI lag on shared workstations.

## 5. Confidence Level

- **Confidence Rating**: High
