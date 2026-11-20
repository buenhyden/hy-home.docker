---
title: "02-Auth Runtime Hardening and Fail-closed Policy"
version: "2.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "ADR-0017"
parent_ids:
- "AD-0002"
created: "2026-03-28"
---

# ADR-0017: 02-Auth Runtime Hardening and Fail-closed Policy

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

This document records the decision on the `02-auth` layer's runtime hardening approach and the fail-closed policy for authentication failures.

The OAuth2 Proxy in `infra/02-auth` handled secret injection through an inline Compose shell. This approach had low change traceability and reusability, and did not align with operating standards (minimal-privilege runtime, a clear entrypoint contract). Also, whether bypass is allowed during an authentication failure was not clearly fixed in documentation.

###### Sources
<!-- core-payload-level:4 -->

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked below, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

- **Requirement Package**: [REQ-0002 Auth requirements](../../01.requirements/0002-auth.md)
- **Architecture Description**: [AD-0002 Auth architecture](../01.descriptions/0002-auth-architecture.md)
- **Related ADR**: [ADR-0002](0002-keycloak-oauth2-proxy-choice.md)

##### Decision Scope

Explicit non-goals:

- Adding or replacing an authentication stack beyond Keycloak/OAuth2 Proxy
- Introducing fail-open as the default policy
- Introducing a new secret backend (forced migration to Vault)

#### Options

##### Considered Options

###### Keep the Compose inline shell
<!-- core-payload-level:4 -->

- Good:
  - Easy to apply immediately.
- Bad:
  - Secret handling logic is mixed into a declarative file, giving low traceability.
  - Hard to separate reuse/test points.

###### Adopt a fail-open exception as the default
<!-- core-payload-level:4 -->

- Good:
  - Short-term availability may rise during an IdP failure.
- Bad:
  - Authentication bypass risk grows and the security boundary collapses.

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Keep the Compose inline shell | Easy to apply immediately. | Secret handling logic is mixed into a declarative file, giving low traceability, and reuse/test points are hard to separate. | Not chosen because secret handling in a declarative file gives low traceability and hard-to-separate reuse/test points. |
| Adopt a fail-open exception as the default | Short-term availability may rise during an IdP failure. | Authentication bypass risk grows and the security boundary collapses. | Not chosen because authentication bypass risk grows and the security boundary collapses. |
| Unify OAuth2 Proxy secret injection into `docker-entrypoint.sh`, run as non-root `oauth2proxy`, and keep fail-closed as the default | A unified secret injection path eases audit and verification, minimal privilege reduces the runtime attack surface, and operators respond to failures consistently. | Creates a maintenance responsibility for the entrypoint script, and fail-closed means user impact can surface immediately during an IdP failure. | The inline shell had low traceability and reusability and did not align with operating standards, and bypass during authentication failure was not clearly fixed in documentation. |

Keeping the inline shell was not chosen because secret handling mixed into a declarative file gives low traceability and hard-to-separate reuse/test points. Fail-open as the default was not chosen because authentication bypass risk grows and the security boundary collapses.

#### Decision

##### Chosen Option

- Unify OAuth2 Proxy secret injection into `docker-entrypoint.sh`.
- Run the OAuth2 Proxy container as a non-root user (`oauth2proxy`).
- Keep fail-closed as the default behavior for authentication failures.
- Perform degraded-mode only in a limited way, per policy/runbook procedure, and require restoring the prior state afterward.
- Keep Keycloak on `template-infra-high`, given its stateful characteristics and current resource baseline (do not force a switch to readonly).

##### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval record is linked. Effective from 2026-03-28.

#### Consequences

##### Impacts

- **Positive**:
  - The secret injection path becomes unified, making audit and verification easier.
  - Minimal-privilege execution reduces the container runtime attack surface.
  - Operators can respond consistently to failures according to policy/procedure.
- **Trade-offs**:
  - Creates a maintenance responsibility for the entrypoint script.
  - Fail-closed means user impact can surface immediately during an IdP failure.

###### Agent-related Example Decisions
<!-- core-payload-level:4 -->

- Tool gating: Use `scripts/hardening/check-all-hardening.sh 02-auth` as a required CI gate
- Guardrail strategy: Prohibit plaintext secrets and bypass policies

##### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

No follow-up work is recorded in this decision.

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
