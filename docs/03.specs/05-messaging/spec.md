---
status: active
---
<!-- Target: docs/03.specs/05-messaging/spec.md -->

# 05-Messaging Optimization Hardening Specification

## Overview

This document defines the optimization/hardening implementation contract for the `infra/05-messaging` tier. Its core scope covers gateway controls for Kafka/RabbitMQ management paths (rate limit/retry/circuit breaker), image tag pinning, development Compose consistency, and CI baseline verification.

## Strategic Boundaries & Non-goals

- This specification owns the messaging infrastructure configuration hardening and operations/documentation traceability contract.
- Kafka/RabbitMQ application-level Producer/Consumer logic changes are out of scope.

## Related Inputs

- **PRD**: [../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md](../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md](../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md](../../02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md)
  - [../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - The `kafbat-ui` image forbids floating tags (`:main`) and uses a pinned version.
  - Externally exposed routers apply `gateway-standard-chain@file`.
  - Management UI routers (`kafka-ui`, `rabbitmq`) keep the SSO middleware chain. The current compose does not declare a separate dev-only Kafbat router.
  - Local volume paths in `docker-compose.dev.yml` use paths relative to the service directory.
- **Data / Interface Contract**:
  - The root-included messaging profile renders the single Kafka broker and single RabbitMQ node from `docker-compose.dev.yml`. `infra/05-messaging/kafka/docker-compose.yml` remains the full 3 broker compose outside the root context.
  - TLS termination is performed by Traefik, and internal `infra_net` communication uses service-internal protocols.
- **Governance Contract**:
  - Enforce `scripts/hardening/check-all-hardening.sh 05-messaging` through the CI `infrastructure-hardening` job.
  - The Stage 01-05 document set keeps reciprocal links across the optimization-hardening document set.

## Core Design

- **Component Boundary**:
  - `infra/05-messaging/kafka/docker-compose.yml`
  - `infra/05-messaging/kafka/docker-compose.dev.yml`
  - `infra/05-messaging/rabbitmq/docker-compose.yml`
- **Key Dependencies**:
  - `infra/common-optimizations.yml` common template
  - `01-gateway` Traefik dynamic middleware (`gateway-standard-chain`, `sso-*`)
  - `02-auth` SSO policy
- **Tech Stack**:
  - Kafka (Confluent CP 8.3.0)
  - RabbitMQ 4.3.1
  - Kafbat UI
  - Traefik TLS termination

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Kafka topics document retention/partition/compaction policy in operations documents based on catalog recommendations.
  - RabbitMQ queues manage dead-letter/retry/quorum queue strategy through operations policy.
- **Migration / Transition Plan**:
  - Phase 1: gateway path controls + image pinning + compose consistency + CI gate
  - Phase 2: apply DLQ/reprocessing/quorum queue standards
  - Phase 3: review messaging tier expansion (multi-AZ, mTLS, regional distribution)

## Interfaces & Data Structures

### Core Interfaces

```yaml
messaging_gateway_contract:
  routers:
    - schema-registry
    - kafka-connect
    - kafka-rest
    - kafka-ui
    - rabbitmq
  required_middlewares:
    - gateway-standard-chain@file
  privileged_routers:
    - kafka-ui
    - rabbitmq
  required_auth_middlewares:
    - sso-errors@file
    - sso-auth@file
```

## Catalog-aligned Expansion Targets

- Kafka:
  - Standardize topic governance (retention/compaction/partition criteria). However, the global `retention.ms` value is not currently pinned in compose.
  - Standardize DLQ + reprocessing pipelines.
- RabbitMQ:
  - Confirm quorum queue adoption scope.
  - Standardize dead-letter + retry policy.
- Gateway integration:
  - Template management-path security headers.
  - Improve per-service router access control policy (SSO/IP allowlist).

## Edge Cases & Error Handling

- Missing `gateway-standard-chain` increases the chance of error propagation during management API burst traffic.
- Floating image tags can introduce unexpected runtime regressions.
- Incorrect relative-path volume mounts cause boot failures in development environments.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: management UI access failure after applying Traefik middleware
- **Fallback**: roll back the relevant router middleware labels to the previous stable version
- **Human Escalation**: adjust policy after joint approval from Messaging Operator and Gateway Operator

## Verification

```bash
HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES='messaging dev' bash scripts/validation/validate-docker-compose.sh
docker compose --env-file .env.example --profile messaging config --services
bash scripts/hardening/check-all-hardening.sh 05-messaging
bash scripts/validation/check-template-security-baseline.sh
bash scripts/validation/check-doc-traceability.sh
```

Service-local compose validation boundary:

- `infra/05-messaging/kafka/docker-compose.yml`, `infra/05-messaging/kafka/docker-compose.dev.yml`, and `infra/05-messaging/rabbitmq/docker-compose.yml` fail with `undefined network infra_net` when `--profile messaging config` runs without the root `infra_net` and root-managed secrets context.
- Full 3 broker Kafka compose validation runs service-locally only in local environments with root network/secret context or an explicit temporary validation overlay.

Runtime verification where the environment allows:

```bash
docker compose --profile messaging up -d kafka-1 schema-registry kafka-connect kafka-rest-proxy kafbat-ui kafka-exporter kafka-init rabbitmq
docker inspect --format '{{json .State.Health}}' kafka-1
docker inspect --format '{{json .State.Health}}' rabbitmq
```

## Success Criteria & Verification Plan

- **VAL-SPC-MSG-001**: `check-all-hardening.sh 05-messaging` has zero failures.
- **VAL-SPC-MSG-002**: root profile messaging compose static validation passes and the service-local compose context boundary is documented.
- **VAL-SPC-MSG-003**: externally exposed router middleware chain contract is satisfied.
- **VAL-SPC-MSG-004**: Stage 01-05 optimization-hardening documents keep reciprocal links synchronized.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/05-messaging/optimization-hardening.md](../../05.operations/guides/05-messaging/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/05-messaging/optimization-hardening.md](../../05.operations/policies/05-messaging/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/05-messaging/optimization-hardening.md](../../05.operations/runbooks/05-messaging/optimization-hardening.md)
- **Catalog**: [../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
