---
title: 'Standardized Service Requirements'
status: 'Proposed'
version: '1.0'
owner: 'Reliability & Security Engineer'
prd_reference: '/docs/prd/system-optimization-prd.md'
arch_reference: '/docs/ard/system-optimization-ard.md'
tags: ['spec', 'standard', 'docker', 'infrastructure']
---

# [SPEC-INFRA-05] Standardized Service Requirements

## 1. Requirement Summary

Every infrastructure service containerized within the `hy-home` ecosystem MUST adhere to a set of architectural invariants to ensure security, observability, and portability.

## 2. Technical Standards

| ID | Category | Requirement Detail | Verification |
| --- | --- | --- | --- |
| REQ-SYS-01 | Security | MUST use `extends` from `common-optimizations.yml`. | `docker compose config` |
| REQ-SYS-01 | Security | MUST implement `no-new-privileges: true` and `cap_drop: ALL`. | `docker inspect` |
| REQ-STD-03 | Observability | MUST include `hy-home.tier` and `hy-home.service` labels. | Loki Label filter |
| REQ-STD-04 | Observability | MUST defined a `healthcheck` for readiness signaling. | `docker ps` status |
| REQ-STD-05 | Portability | MUST utilize `${DEFAULT_..._DIR}` for volume mapping. | `.env` audit |
| REQ-STD-06 | Performance | MUST define CPU/RAM limits via global templates. | Grafana metrics |

## 3. Implementation Details

### 3.1 Metadata Labels

Labels MUST be applied using the tier-specific anchor:

```yaml
x-labels-base: &labels-base
  hy-home.managed: "true"
  hy-home.tier: <tier_name>
  observability.logs: "true"
```

### 3.2 Logging Strategy

Loki integration is MANDATORY for all infrastructure services.

```yaml
x-logging: &default-logging
  driver: "loki"
  options:
    loki-url: "http://infra-loki:3100/loki/api/v1/push"
    loki-external-labels: "container_name={{.Name}},tier=<tier_name>"
```

## 4. Verification Flow

1. **Schema Check**: `docker compose config` MUST exit with status 0.
2. **Security Audit**: `docker-bench-security` score MUST NOT degrade.
3. **Log Check**: Logs MUST appear in Grafana Explore under the correct labels.
