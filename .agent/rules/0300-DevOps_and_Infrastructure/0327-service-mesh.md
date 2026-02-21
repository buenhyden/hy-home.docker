---
trigger: model_decision
glob:
  - "k8s/**/*.yml"
  - "k8s/**/*.yaml"
  - "manifests/**/*.yml"
  - "manifests/**/*.yaml"
description: "Service mesh traffic policy: mTLS, timeouts, retries, circuit breakers, and safe defaults for service-to-service calls."
---

# 1100-Service-Mesh-Traffic-Policy

- **Role**: Service Mesh Policy Owner
- **Purpose**: Enforce deterministic traffic behavior for reliability (mTLS, timeouts, retries, circuit breakers) across service boundaries.
- **Activates When**: Introducing/altering service-to-service communication, mesh policies, or routing rules.

---

## 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites

- **[REQ-MESH-PREREQ-01] Mesh Capability Exists**
  - If service mesh is enabled, policies MUST be declared.
  - If mesh is required but not available, the change MUST be blocked.

---

### 1.2 mTLS and Identity

- **[REQ-MESH-TLS-01] mTLS Default**
  - Service-to-service traffic MUST use mTLS where supported.

---

### 1.3 Timeouts, Retries, Circuit Breakers

- **[REQ-MESH-RT-01] Timeouts Mandatory**
  - Every inter-service call MUST define timeouts.

- **[REQ-MESH-RT-02] Retry Budget**
  - Retries MUST be bounded and MUST NOT amplify failures.

- **[REQ-MESH-CB-01] Circuit Breakers**
  - Circuit breaking MUST exist for critical dependencies.

---

### 1.4 Success & Failure

- **[REQ-MESH-SUCCESS-01] Success Criteria**
  - Policies are valid ONLY if mTLS + timeouts exist for service calls.

- **[REQ-MESH-FAIL-01] Failure Behavior**
  - Missing timeouts MUST reject the change.

---

### 1.5 Reference-First

- **[REQ-MESH-REF-01] Canonical Examples**
  - `mesh/_examples/mtls-default.yaml`
  - `mesh/_examples/timeout-retry-policy.yaml`
  - `mesh/_examples/circuit-breaker.yaml`

---

## 2. Procedures

### Phase P1 — Classify Dependencies

1) Identify critical vs non-critical dependencies.

- **Outcome**: Dependency tiers exist.

### Phase P2 — Apply Policies

1) Apply mTLS and timeouts universally.
2) Add bounded retries and circuit breakers for critical paths.

- **Outcome**: Failure containment exists.

---

## 3. Examples

### Good Example — Bounded Retries

**Input**

- Retry = 2 with timeout and circuit breaker.

**Expected Output**

- No retry storms under partial failure.

### Bad Example — No Timeouts

**Input**

- Service calls without timeouts.

**Rejected Because**

- Violates `[REQ-MESH-RT-01]`.

---

## 4. Validation Criteria

- [ ] mTLS is enabled where supported. (`[REQ-MESH-TLS-01]`)
- [ ] Timeouts exist for all service calls. (`[REQ-MESH-RT-01]`)
- [ ] Retries are bounded. (`[REQ-MESH-RT-02]`)
- [ ] Circuit breakers exist for critical dependencies. (`[REQ-MESH-CB-01]`)

---

## See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- examples/mesh/mtls-default.yaml
- examples/mesh/timeout-retry-policy.yaml
- examples/mesh/circuit-breaker.yaml
