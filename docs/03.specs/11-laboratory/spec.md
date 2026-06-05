---
status: active
---
<!-- Target: docs/03.specs/11-laboratory/spec.md -->

# 11-Laboratory Optimization Hardening Technical Specification

## Overview

This document is the optimization/hardening technical specification for the `infra/11-laboratory` tier (dashboard, dozzle, portainer, redisinsight, open-notebook). It defines strengthened management UI ingress boundaries, standardized network isolation, least-privilege hardening, policy gate adoption, and catalog-based expansion items as implementation contracts.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Laboratory router middleware contract (gateway+allowlist+SSO)
  - compose network boundary (`infra_net` external) contract
  - dashboard direct exposure removal contract
  - dozzle socket least-privilege (read-only) contract
  - open-notebook UI route SSO/allowlist/large-body boundary and Docker Secret injection contract
  - `check-all-hardening.sh 11-laboratory` policy gate contract
- **Does Not Own**:
  - Detailed Keycloak realm policy
  - Traefik core entrypoints/global routing
  - Immediate automation of catalog expansion items

## Related Inputs

- **PRD**: [../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md](../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md](../../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/0011-laboratory-services.md](../../02.architecture/decisions/0011-laboratory-services.md)
  - [../../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - Every Laboratory compose keeps a static IP network block that joins the root `infra_net` context.
  - Every Laboratory UI router applies `gateway-standard-chain@file,<service>-admin-ip@docker,sso-errors@file,sso-auth@file`. Open Notebook also adds `large-body@file` for large upload support.
  - dashboard does not use direct host `ports`; it uses only `expose`.
  - dozzle mounts the docker socket as `:ro`.
  - Services provide mount-based or readiness-based healthchecks.
  - root-active Laboratory includes are Dozzle, RedisInsight, Open Notebook, and SurrealDB. Homer Dashboard and Portainer are optional/commented root includes until explicitly promoted.
- **Governance Contract**:
  - Passing `scripts/hardening/check-all-hardening.sh 11-laboratory` is the hardening baseline.
  - The CI `infrastructure-hardening` job blocks PR regressions.

## Core Design

- **Ingress Security Plane**:
  - Enforce the gateway chain, allowlist, and SSO chain after Traefik TLS termination.
- **Network Isolation Plane**:
  - Keep service network blocks that join the root `infra_net` context.
- **Least Privilege Plane**:
  - dozzle socket read-only
  - remove dashboard direct host exposure
- **Policy Gate Plane**:
  - detect regressions early with the lab hardening checker and CI job

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Laboratory services do not define shared application data schemas in this spec.
  - Service-specific state remains in the corresponding Docker volumes or upstream systems.
- **Migration / Transition Plan**:
  - Preserve existing service state while tightening ingress, network, socket, and policy gate contracts.
  - Treat new data-bearing laboratory tools as separate specs when they introduce durable state or user data boundaries.

## Interfaces & Data Structures

### Laboratory Hardening Control Surface

```yaml
laboratory_hardening_controls:
  ingress_security:
    dashboard: gateway-standard-chain + homer-admin-ip + sso-errors + sso-auth
    dozzle: gateway-standard-chain + dozzle-admin-ip + sso-errors + sso-auth
    portainer: gateway-standard-chain + portainer-admin-ip + sso-errors + sso-auth
    redisinsight: gateway-standard-chain + redisinsight-admin-ip + sso-errors + sso-auth
    open_notebook: gateway-standard-chain + open-notebook-admin-ip + large-body + sso-errors + sso-auth
  network_boundary:
    compose_network: root infra_net context
  least_privilege:
    dashboard_direct_port_exposure: forbidden
    dozzle_docker_socket: read-only
  active_root_admin_services:
    - dozzle
    - redisinsight
    - surrealdb
    - open_notebook
  optional_root_admin_services:
    - homer
    - portainer
```

## Edge Cases & Error Handling

- Operator IP access that is not allowed by the allowlist default can receive 403 responses.
- Switching dozzle to read-only can break existing operator habits that relied on write actions.
- After dashboard direct port removal, older bookmarked access paths can be blocked.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: management UI access blocked
  - **Fallback**: temporarily adjust allowlist environment variables, then redeploy
  - **Escalation**: Security/Platform approver
- **Failure Mode**: hardening gate failure
  - **Fallback**: restore contract items (middleware/network/port/socket)
  - **Escalation**: DevOps on-call

## Verification

- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`

Service-local standalone compose rendering is not readiness evidence for these
leaves because the compose files depend on the root `infra_net`, secret, and
common template context.

## Success Criteria & Verification Plan

- **VAL-LAB-001**: Laboratory compose static validation passes.
- **VAL-LAB-002**: Laboratory hardening baseline script has zero failures.
- **VAL-LAB-003**: PRD~Runbook optimization-hardening links remain consistent.
- **VAL-LAB-004**: catalog `11-laboratory` expansion items are reflected in Plan/Tasks/Operations.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Guide**: [../../05.operations/guides/11-laboratory/optimization-hardening.md](../../05.operations/guides/11-laboratory/optimization-hardening.md)
- **Policy**: [../../05.operations/policies/11-laboratory/optimization-hardening.md](../../05.operations/policies/11-laboratory/optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/11-laboratory/optimization-hardening.md](../../05.operations/runbooks/11-laboratory/optimization-hardening.md)
- **Catalog**: [../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md](../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md)
