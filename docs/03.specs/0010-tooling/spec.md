---
title: 09-Tooling Optimization Hardening Technical Specification
type: sdlc/spec
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0010
parent_ids:
  - AD-0024
created: 2026-07-05
updated: 2026-09-01
---
# 09-Tooling Optimization Hardening Technical Specification

## Overview

This document is the optimization/hardening technical specification for the `infra/09-tooling` tier (terraform, terrakube, registry, sonarqube, k6, locust, syncthing). It defines public-boundary security, network isolation, test runtime stability, CI policy gates, and catalog-based expansion items as implementation contracts. Because tooling compose includes are currently commented out in the root `docker-compose.yml`, this specification describes the owned implementation and standalone/root-commented optional execution contract.

## Strategic Boundaries & Non-goals

- **Owns**:
  - tooling public router middleware contract
  - tooling compose network boundary contract
  - locust/k6 runtime contract (health/volume)
  - `scripts/hardening/check-all-hardening.sh 09-tooling` policy gate contract
- **Does Not Own**:
  - Domain feature implementation details for each tool
  - Immediate full implementation of catalog expansion items
  - New tool adoption/replacement

## Related Inputs

- **PRD**: [../../01.requirements/0021-tooling-optimization-hardening.md](../../01.requirements/0021-tooling-optimization-hardening.md)
- **ARD**: [../../02.architecture/descriptions/0024-tooling-optimization-hardening-architecture.md](../../02.architecture/descriptions/0024-tooling-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../02.architecture/decisions/0009-tooling-services.md](../../02.architecture/decisions/0009-tooling-services.md)
  - [../../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - `infra/09-tooling/*/docker-compose.yml` files are currently root-commented optional includes.
  - SonarQube/Terrakube/Syncthing routers use `gateway-standard-chain@file,sso-errors@file,sso-auth@file`.
  - registry/sonarqube/terrakube/syncthing/locust/k6/terraform compose files declare the `infra_net` external boundary.
  - locust-worker has a worker process healthcheck.
  - k6 mounts the `k6-data` volume at the baseline path (`/mnt/locust`).
- **Data / Interface Contract**:
  - tooling services keep existing PostgreSQL/Valkey/MinIO/InfluxDB integrations where needed.
  - Because 09-tooling includes are optional/commented in the root `docker-compose.yml`, service-local compose files require root network/secret/dependency context for runtime rendering.
- **Governance Contract**:
  - Passing `scripts/hardening/check-all-hardening.sh 09-tooling` is the tooling tier hardening baseline.
  - The CI `infrastructure-hardening` job blocks regressions at PR time through the full hardening baseline.

## Core Design

- **Gateway Security Plane**:
  - Public tooling UIs enforce the gateway standard chain and SSO chain after TLS termination.
- **Network Isolation Plane**:
  - tooling compose files explicitly declare the shared `infra_net` external boundary.
- **Runtime Stability Plane**:
  - Apply the locust worker healthcheck and k6 volume contract as the minimum stability baseline.
- **Policy Gate Plane**:
  - Block change regressions early with the tooling hardening checker and CI job.

## Data Modeling & Storage Strategy

- registry/sonarqube/syncthing/k6/locust keep the existing bind volume strategy.
- terrakube/terraform keep the existing state/artifact data boundary.
- drift/promotion policy is strengthened incrementally through operations/tasks.

## Interfaces & Data Structures

### Tooling Hardening Control Surface

```yaml
tooling_hardening_controls:
  ingress_security:
    sonarqube: gateway-standard-chain + sso-errors + sso-auth
    terrakube_api: gateway-standard-chain + sso-errors + sso-auth
    terrakube_ui: gateway-standard-chain + sso-errors + sso-auth
    terrakube_executor: gateway-standard-chain + sso-errors + sso-auth
    syncthing: gateway-standard-chain + sso-errors + sso-auth
  network_boundary:
    compose_network: infra_net (external)
  runtime_stability:
    locust_worker_healthcheck: required
    k6_volume_contract: k6-data -> /mnt/locust
```

## Edge Cases & Error Handling

- SSO chain hardening can block existing automation access paths, so apply the operational exception procedure.
- If the locust-worker healthcheck reports false positives, readjust it around the worker process.
- If execution fails because no k6 scenario exists, track baseline scenario preparation separately.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: tooling UI access policy regression
  - **Fallback**: roll back to the most recent working middleware settings
  - **Human Escalation**: Gateway/Auth operations approver
- **Failure Mode**: locust worker restart loop
  - **Fallback**: reapply the healthcheck/worker command contract
  - **Human Escalation**: Performance tooling owner
- **Failure Mode**: k6 execution data path mismatch
  - **Fallback**: restore the `k6-data` volume contract
  - **Human Escalation**: DevOps on-call

## Verification

```bash
bash scripts/hardening/check-all-hardening.sh 09-tooling
bash scripts/validation/check-template-security-baseline.sh
python3 scripts/validation/check-document-links.py --mode traceability
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-TLG-001**: tooling hardening check and documented optional root-context validation boundary pass.
- **VAL-TLG-002**: tooling hardening baseline script has zero failures.
- **VAL-TLG-003**: PRD~Runbook optimization-hardening document links remain consistent.
- **VAL-TLG-004**: catalog `09-tooling` expansion items are reflected in Plan/Tasks/Operations.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Guide**: [../../05.operations/guides/09-tooling/optimization-hardening.md](../../05.operations/catalog/09-tooling/0063-optimization-hardening/guide.md)
- **Policy**: [../../05.operations/policies/09-tooling/optimization-hardening.md](../../05.operations/catalog/09-tooling/0063-optimization-hardening/policy.md)
- **Runbook**: [../../05.operations/runbooks/09-tooling/optimization-hardening.md](../../05.operations/catalog/09-tooling/0063-optimization-hardening/runbook.md)
- **Governance**: [Infrastructure optimization governance](../../05.operations/catalog/00-workspace/0006-infrastructure-optimization-governance/policy.md)

## Boundaries and Inputs

The preserved ownership boundaries, dependencies, and inputs above remain authoritative.

## Behavior Contract

The behaviors and invariants already specified above remain the package behavior contract.

## Technical Approach

The implementation and component design recorded above remain the technical approach.

## Interfaces and Data

The interfaces, configuration, and data shapes recorded above remain authoritative.

## Failure Modes and Guardrails

The safety, validation, and operational constraints above remain the package guardrails.

## Acceptance Contract

The verification and success conditions above remain the acceptance contract.

## Traceability

The requirement, architecture, operations, and evidence links above provide traceability.
