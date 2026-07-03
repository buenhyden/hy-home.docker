---
status: active
---
<!-- Target: docs/03.specs/06-observability/spec.md -->

# 06-Observability Optimization Hardening Specification

## Overview

This document defines the optimization/hardening implementation contract for the `infra/06-observability` tier. Its core scope covers gateway boundaries (security headers/SSO), health-based dependencies, host collector health signals, custom image runtime hardening, and CI baseline verification.

## Strategic Boundaries & Non-goals

- This specification owns the management-path hardening and operations/documentation traceability contract for observability infrastructure.
- Application code instrumentation (OTel SDK) changes are out of scope.

## Related Inputs

- **PRD**: [../../01.requirements/2026-03-28-06-observability-optimization-hardening.md](../../01.requirements/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0021-observability-optimization-hardening-architecture.md](../../02.architecture/requirements/0021-observability-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/0006-lgtm-stack-selection.md](../../02.architecture/decisions/0006-lgtm-stack-selection.md)
  - [../../02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - Observability public routers apply `gateway-standard-chain@file,sso-errors@file,sso-auth@file`.
  - Alloy/Grafana depend on Loki/Tempo with `service_healthy`.
  - cAdvisor has a `/healthz` healthcheck and independent `cadvisor` Traefik route/service labels.
  - Pyroscope must render as the `pyroscope:4040` service in both the root-included dev compose and the local obs compose.
- **Data / Interface Contract**:
  - Collection/storage/query traffic keeps `infra_net` internal boundaries by default.
  - External access to management paths is controlled through the Traefik `websecure` entrypoint.
- **Governance Contract**:
  - Enforce `scripts/hardening/check-all-hardening.sh 06-observability` through the CI `infrastructure-hardening` job.
  - The Stage 01-05 document set keeps reciprocal links across the optimization-hardening document set.

## Core Design

- **Component Boundary**:
  - `infra/06-observability/docker-compose.yml`
  - `infra/06-observability/loki/{Dockerfile,docker-entrypoint.sh}`
  - `infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
- **Key Dependencies**:
  - `infra/common-optimizations.yml`
  - Traefik dynamic middleware (`gateway-standard-chain`, `sso-*`)
  - Keycloak SSO
  - MinIO object storage for Loki/Tempo
- **Tech Stack**:
  - Prometheus `v3.13.0`, Grafana `13.1.0`, Loki `3.7.3-custom`, Tempo `3.0.2-custom`, Alloy `1.17.1`, Alertmanager `0.33.0`, Pushgateway `1.11.3`, Pyroscope `2.1.0`, cAdvisor `0.55.1`

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Metrics/logs/traces/profiles operate with service-specific retention policies.
- **Migration / Transition Plan**:
  - Phase 1: gateway/health/container hardening + CI gate + docs traceability
  - Phase 2: refine scrape budget/cardinality/sampling policies
  - Phase 3: apply a long-term retention and scalable HA operating model

## Interfaces & Data Structures

### Core Interfaces

```yaml
observability_gateway_contract:
  routers:
    - prometheus
    - alloy
    - grafana
    - alertmanager
    - pushgateway
    - loki
    - tempo
    - pyroscope
    - cadvisor
  required_middlewares:
    - gateway-standard-chain@file
    - sso-errors@file
    - sso-auth@file
```

## Catalog-aligned Expansion Targets

- Prometheus:
  - scrape budget, evaluation delay budget, remote_write tiering
- Loki:
  - label cardinality budget, separated retention/compactor operations
- Tempo:
  - service/endpoint-specific sampling policies and span surge protection
- Alloy:
  - collection module templating and standardized onboarding for new services

## Edge Cases & Error Handling

- Applying the SSO chain to only some routers creates inconsistent management-path exposure.
- `service_started` dependencies can cause boot races and downstream service errors.
- Running custom images as root increases security baseline violations and runtime risk.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: UI/API access failure after middleware/depends_on changes
- **Fallback**: roll back to the previous stable Compose contract, then rerun the hardening script
- **Human Escalation**: apply a policy exception with SRE and Gateway Operator approval

## Verification

```bash
HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 06-observability
bash scripts/validation/check-template-security-baseline.sh
bash scripts/validation/check-doc-traceability.sh
```

Service-local `docker compose -f infra/06-observability/docker-compose.yml config` requires the root network and Docker Secret context, or a local validation overlay that declares `infra_net`, `k3d-hyhome`, and the referenced secret files.

Runtime verification where the environment allows:

```bash
docker compose -f infra/06-observability/docker-compose.yml --profile obs up -d
docker inspect --format '{{json .State.Health}}' infra-prometheus
docker inspect --format '{{json .State.Health}}' infra-grafana
docker inspect --format '{{json .State.Health}}' cadvisor
```

## Success Criteria & Verification Plan

- **VAL-SPC-OBS-001**: `check-all-hardening.sh 06-observability` has zero failures.
- **VAL-SPC-OBS-002**: root profile or overlay-backed observability Compose static validation passes.
- **VAL-SPC-OBS-003**: public router middleware chain contract is satisfied.
- **VAL-SPC-OBS-004**: Stage 01-05 optimization-hardening documents keep reciprocal links synchronized.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/06-observability/optimization-hardening.md](../../05.operations/guides/06-observability/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/06-observability/optimization-hardening.md](../../05.operations/policies/06-observability/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/06-observability/optimization-hardening.md](../../05.operations/runbooks/06-observability/optimization-hardening.md)
- **Catalog**: [../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
