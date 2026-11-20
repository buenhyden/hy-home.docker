---
title: "Observability Hardening and HA Expansion Strategy"
version: "2.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "ADR-0021"
parent_ids:
- "AD-0021"
created: "2026-03-28"
---

# ADR-0021: Observability Hardening and HA Expansion Strategy

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-decision payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context

##### Problem and Drivers

This document records the decision to first apply immediately applicable hardening (gateway chain + SSO, strengthened health dependencies, container runtime hardening, CI baseline) for the `06-observability` layer, while pursuing catalog-based HA expansion in phases.

The observability layer provides many management paths, and failures can spread easily if the security chain is missing, startup order is unstable, or runtime hardening is insufficient. Layer-specific verification automation is needed to block operational regressions at the PR stage.

###### Sources
<!-- core-payload-level:4 -->

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked below, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

- **PRD**: [../01.requirements/0007-observability.md](../../01.requirements/0007-observability.md)
- **Architecture Description**: [AD-0021 06-Observability Optimization Hardening Architecture Description](../01.descriptions/0021-observability-optimization-hardening-architecture.md)
- **Tier Architecture Description**: [AD-0006 Observability Architecture Description](../01.descriptions/0006-observability-architecture.md)
- **Related ADR**: [ADR-0053](0053-observability-storage-on-seaweedfs.md)

##### Decision Scope

Explicit non-goals:

- Immediately switching to a multi-region observability cluster
- A wholesale overhaul of application code instrumentation logic

#### Options

##### Considered Options

###### Implement all catalog expansion immediately
<!-- core-payload-level:4 -->

- Good:
  - Short-term functional expansion effect
- Bad:
  - Increased change scope raises failure isolation/rollback difficulty

###### Update documentation only, keep runtime/CI unchanged
<!-- core-payload-level:4 -->

- Good:
  - Reduces short-term implementation burden
- Bad:
  - Lacks the ability to actually block regressions

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Implement all catalog expansion immediately | Short-term functional expansion effect. | Increased change scope raises failure isolation and rollback difficulty. | Not chosen because the increased change scope raises failure isolation and rollback difficulty. |
| Update documentation only, keep runtime/CI unchanged | Reduces short-term implementation burden. | Lacks the ability to actually block regressions. | Not chosen because it lacks the ability to actually block regressions. |
| Immediate hardening with phased catalog expansion through a policy approval procedure | Strengthens the management path security boundary, improves startup stability and regression detection, and strengthens the single contract across documents, configuration and CI. | Some automated access may need adjustment due to strengthened SSO, and short-term visible effect is centered on hardening. | Failures spread easily when the security chain, startup order or runtime hardening is weak, and layer-specific verification automation is needed to block regressions at the PR stage. |

Immediate full catalog expansion was not chosen because the increased change scope raises failure isolation and rollback difficulty. Documentation-only was not chosen because it lacks the ability to actually block regressions.

#### Decision

##### Chosen Option

- Perform immediate hardening.
  - Apply `gateway-standard-chain@file` plus `sso-errors@file,sso-auth@file` to the observability public router.
  - Raise the Loki/Tempo dependency for Alloy/Grafana to `service_healthy`.
  - Add a cAdvisor healthcheck.
  - Specify non-root execution/secret guard for the Loki/Tempo custom images.
  - Introduce `check-all-hardening.sh 06-observability` and the CI `infrastructure-hardening` job.
  - Create the PRD-through-Runbook document set to secure bidirectional traceability.
- Introduce catalog expansion (sampling/long-term retention/modularization) in phases through a policy approval procedure.

##### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval record is linked. Effective from 2026-03-28.

#### Consequences

##### Impacts

- **Positive**:
  - The management path security boundary strengthens.
  - Startup stability and operational regression detection improve.
  - The single contract (SSoT) across documents/configuration/CI strengthens.
- **Trade-offs**:
  - Some automated access may need adjustment due to strengthened SSO.
  - Catalog expansion is applied in phases, so short-term visible effect is centered on hardening.

###### Agent-related Example Decisions
<!-- core-payload-level:4 -->

- Tool gating: Use `check-all-hardening.sh 06-observability` as a required PR gate
- Guardrail strategy: Require a security chain on public routers, require non-root/secret guard

##### Follow-up

###### Current documentation applicability
<!-- core-payload-level:4 -->

On 2026-11-20 the owner's P05 document/SDLC reconciliation directs an in-place
clarification of the original documentation step. Its 2026-03-28 document set
records this observability rollout; it does not require a full artifact set
or reciprocal links for every later change. Current responsibility and
directional relations follow the
[documentation protocol](../../00.workspace/03.process/documentation-protocol.md).
The accepted hardening and phased expansion choice, its product duties,
original date and actual evidence remain unchanged.

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

Catalog expansion (sampling/long-term retention/modularization) follows in phases through a policy approval procedure, as decided above.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
