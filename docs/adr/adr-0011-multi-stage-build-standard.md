---
title: 'ADR-0011: Multi-Stage Build Standard'
status: 'Accepted'
date: '2026-02-27'
authors: 'Build Engineer'
deciders: 'Platform Team'
---

# Architecture Decision Record (ADR)

## Title: Multi-Stage Build Standard

- **Status:** Accepted
- **Date:** 2026-02-27
- **Authors:** Build Engineer
- **Deciders:** Platform Team

## 1. Context and Problem Statement

Custom Docker images for services were consistently using mono-stage builds, including unnecessary build-time dependencies (compilers, headers) in the final image. This leads to bloated images and a larger security attack surface.

## 2. Decision Drivers

- **Security**: Reduce attack surface by removing build tools from production.
- **Performance**: Smaller images mean faster pulls and less disk usage.
- **Consistency**: Standardize how custom components are built.

## 3. Decision Outcome

**Chosen option: "Mandatory Multi-Stage Docker Build"**, because separating the build environment from the runtime environment ensures that only necessary artifacts are shipped, dramatically reducing image size.

### 3.1 Core Engineering Pillars Alignment

- **Security**: Aligns with binary hardening standards.
- **Performance**: Optimizes image layers and startup weight.
- **Documentation**: Clearly defines the build lifecycle for custom services.

### 3.2 Positive Consequences

- Significant reduction in final image size (often >50%).
- Faster build/pull times in CI and local dev.

### 3.3 Negative Consequences

- Slightly more complex Dockerfile maintenance.

## 4. Alternatives Considered (Pros and Cons)

### Mono-stage with Cleanup

Run `apt-get clean` and remove packages in the same layer.

- **Good**, because it is simpler syntax.
- **Bad**, because it often misses hidden build dependencies and caches.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Best practice for modern containerized development.
- **Technical Requirements Addressed**: REQ-PRD-SYS-04
