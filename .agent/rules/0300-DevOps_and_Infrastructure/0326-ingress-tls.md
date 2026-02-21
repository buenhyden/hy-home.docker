---
trigger: model_decision
glob:
  - "k8s/**/*.yml"
  - "k8s/**/*.yaml"
  - "manifests/**/*.yml"
  - "manifests/**/*.yaml"
  - "helm/**"
description: "Ingress/TLS/WAF standards: TLS enforcement, certificate automation, secure headers, rate-limits, and safe exposure rules."
---

# 1000-Ingress-TLS-WAF-Standards

- **Role**: Edge Security Owner
- **Purpose**: Enforce secure and deterministic ingress exposure with TLS automation, hardened headers, and controlled traffic policies.
- **Activates When**: Adding/updating Ingress, Gateway, TLS configuration, or externally exposed services.

---

## 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites

- **[REQ-EDGE-PREREQ-01] TLS Automation**
  - Certificate automation MUST exist (e.g., cert-manager or equivalent).
  - If TLS automation is missing, external exposure MUST be blocked.

---

### 1.2 TLS Enforcement

- **[REQ-EDGE-TLS-01] TLS Required**
  - Externally exposed endpoints MUST use TLS.

- **[BAN-EDGE-TLS-01] Plain HTTP Exposure**
  - Plain HTTP exposure MUST NOT be allowed without redirect to HTTPS.

---

### 1.3 Secure Headers and Rate Limiting

- **[REQ-EDGE-SEC-01] Security Headers**
  - Exposed services MUST include secure headers (HSTS when applicable).

- **[REQ-EDGE-RATE-01] Rate Limit Policy**
  - Public endpoints MUST define a rate limit policy.

---

### 1.4 Success & Failure

- **[REQ-EDGE-SUCCESS-01] Success Criteria**
  - Exposure is valid ONLY if TLS + policy controls are present.

- **[REQ-EDGE-FAIL-01] Failure Behavior**
  - Missing TLS MUST reject the change.

---

### 1.5 Reference-First

- **[REQ-EDGE-REF-01] Canonical Examples**
  - `edge/_examples/ingress-tls-baseline.yaml`
  - `edge/_examples/security-headers.yaml`
  - `edge/_examples/rate-limit-policy.yaml`

---

## 2. Procedures

### Phase P1 — Define Exposure

1) Identify public routes and threat model.

- **Outcome**: Exposure intent is explicit.

### Phase P2 — Enforce TLS and Policies

1) Add TLS and redirect behavior.
2) Add security headers and rate limits.

- **Outcome**: Exposure is secure by default.

---

## 3. Examples

### Good Example — HTTPS Only

**Input**

- Ingress with TLS, redirect, and rate limiting.

**Expected Output**

- Safe exposure with deterministic controls.

### Bad Example — HTTP Only

**Input**

- Public service without TLS.

**Rejected Because**

- Violates `[REQ-EDGE-TLS-01]`.

---

## 4. Validation Criteria

- [ ] TLS automation exists. (`[REQ-EDGE-PREREQ-01]`)
- [ ] External routes enforce TLS. (`[REQ-EDGE-TLS-01]`)
- [ ] Rate limiting exists where required. (`[REQ-EDGE-RATE-01]`)

---

## See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- examples/edge/ingress-tls-baseline.yaml
- examples/edge/security-headers.yaml
- examples/edge/rate-limit-policy.yaml
