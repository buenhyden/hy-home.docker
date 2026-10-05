---
title: "Workflow Hardening and HA Expansion Strategy"
version: "1.1.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0022"
parent_ids:
- "AD-0022"
created: "2026-03-28"
---
# ADR-0022: Workflow Hardening and HA Expansion Strategy

## Context

This document records the decision to first carry out immediately applicable hardening (boundary security, health-based dependencies, n8n image hardening, CI gate) for the `07-workflow` layer, while pursuing catalog expansion items in phases.

The workflow tier has a broad operational impact scope, and failure propagation risk grows high if management path exposure/startup race conditions/image drift accumulate. At the same time, the catalog requires Airflow/n8n expansion items, so a decision that separates short-term stabilization from mid-term expansion is needed.

### Traceability

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked under `Related Documents`, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

## Decision

- Carry out immediate hardening.
  - Align the Airflow/n8n management path middleware to `gateway-standard-chain + sso-errors + sso-auth`.
  - Give the service-local Airflow compose a Valkey health-based dependency, and document the shared `mng-valkey` boundary of the root-included dev compose.

    The two compose files this instruction pointed to were merged into one after SPEC-0156 and SPEC-0171.
    The Valkey health dependency and the shared `mng-valkey` boundary remain as before, but now
    a `dedicated-valkey` profile splits the two within each single file,
    `infra/07-workflow/airflow/docker-compose.yml` and `infra/07-workflow/n8n/docker-compose.yml`.
    The n8n instruction below is the same. The original instruction text is preserved as a
    point-in-time record. SPEC-0176 recorded this.
  - Add n8n worker/task-runner healthcheck and dependency gating, and document the shared `mng-valkey` boundary of the root-included dev compose.
  - Promote the n8n custom image to the compose default image and enforce non-root + secret guard.
  - Introduce `scripts/hardening/check-all-hardening.sh 07-workflow` and the CI `infrastructure-hardening` job.
- Carry out catalog expansion in phases.
  - Document and gradually introduce Airflow DAG quality gate/worker autoscale criteria
  - Standardize n8n workflow Git backup/Vault credential integration

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

### Implement all catalog expansion immediately

- Good:
  - Short-term functional expansion is felt
- Bad:
  - Increased change scope raises stabilization/rollback difficulty

### Update documentation only, hold off on runtime/CI hardening

- Good:
  - Reduces short-term implementation cost
- Bad:
  - Lacks the ability to actually block regressions

## Consequences

- **Positive**:
  - Workflow management boundary security and startup stability improve.
  - Workflow tier change regressions can be automatically blocked at the PR stage.
  - Catalog expansion items become executable at the document/task level.
- **Trade-offs**:
  - Strengthened SSO requires adjusting some existing automated access methods.
  - Custom image builds can add build time in CI/dev environments.

### Explicit Non-goals

- Immediately switching to a multi-cluster workflow architecture
- Simultaneously pursuing a new workflow service's full production rollout
- Refactoring individual DAG/workflow business logic

### Agent-related Example Decisions

- Guardrail strategy: The workflow management path requires the gateway+SSO chain
- Tool gating: Enforce the workflow hardening verification script as a policy gate

## Related Documents

- **PRD**: [../01.requirements/0008-workflow.md](../../01.requirements/0008-workflow.md)
- **Architecture Description**: [../02.architecture/descriptions/0022-workflow-optimization-hardening-architecture.md](../descriptions/0022-workflow-optimization-hardening-architecture.md)
- **Spec**: [../03.specs/008-workflow/spec.md](../descriptions/0007-workflow-architecture.md)
- **Related ADR**: [ADR-0007](0007-airflow-n8n-hybrid-workflow.md)
