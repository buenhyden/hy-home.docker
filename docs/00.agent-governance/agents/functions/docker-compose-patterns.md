---
layer: agentic
---

# docker-compose-patterns

## Overview

Deployment strategy pattern library for Docker Compose environments. Provides Rolling, Blue-Green, and Canary deployment patterns adapted for Docker Compose with Traefik.

## Purpose

Enable safe, zero-downtime deployments using proven patterns without requiring Kubernetes or cloud-native infrastructure.

## Scope

**Covers:**

- Rolling update pattern (`docker compose up -d --no-deps`)
- Blue-Green pattern (Traefik router switch via compose profiles)
- Canary pattern (Traefik weighted routing with progressive traffic shift)
- Health check design (Liveness/Readiness/Startup with compose + Traefik labels)
- Rollback procedures and trigger conditions

**Excludes:**

- Kubernetes or cloud-specific deployment strategies
- CI/CD pipeline orchestration (see ci-cd-patterns)

## Structure

- Pattern selection → health check design → rollback planning

## Agents

- **infra-implementer** — primary caller
- **iac-reviewer** — uses patterns for review reference

## Skills

- This function is a reusable orchestration skill.

## Usage

- Trigger when planning or implementing deployment strategy changes.
- **Inputs:** deployment target, traffic split requirements, rollback SLO
- **Outputs:** deployment YAML configuration + rollback procedure

## Artifacts

- `_workspace/deployment_<strategy>_<date>.md`

## Related Documents

- `../../scopes/infra.md`
- `../functions/ci-cd-patterns.md`
- `../README.md`
