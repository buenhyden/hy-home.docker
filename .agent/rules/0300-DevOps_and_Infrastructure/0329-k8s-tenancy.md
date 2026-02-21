---
trigger: model_decision
glob:
  - "k8s/namespaces/**/*.yml"
  - "k8s/namespaces/**/*.yaml"
  - "k8s/**/namespace*.yml"
  - "k8s/**/namespace*.yaml"
  - "policies/**/*.yml"
  - "policies/**/*.yaml"
description: "Namespace multi-tenancy: deterministic isolation via RBAC, quotas, limit ranges, default-deny network policy, and policy enforcement."
---

# 1900-Namespace-Multi-Tenancy

- **Role**: Cluster Multi-Tenancy Owner
- **Purpose**: Enforce deterministic namespace isolation so teams and environments remain safely separated with explicit RBAC, quotas, policies, and network controls.
- **Activates When**: Creating/updating namespaces, namespace policies, RBAC, quotas, or network policies.

---

## 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites (Executable Contract)

- **[REQ-NS-PREREQ-01] Policy Enforcement**
  - A policy engine MUST exist to enforce baseline constraints (Pod Security, required labels, forbidden fields).
  - If policy enforcement is unavailable, multi-tenant production-like deployment MUST be blocked.

- **[REQ-NS-OUT-01] Out of Scope**
  - This Rule does NOT define cloud IAM.
  - This Rule defines Kubernetes namespace-level isolation and governance.

---

### 1.2 Namespace Naming and Labels

- **[REQ-NS-NAM-01] Naming Convention**
  - Namespaces MUST follow:
    - `<env>-<team>-<domain>`
  - Names MUST be lowercase and MUST NOT include spaces.

- **[REQ-NS-LBL-01] Mandatory Labels**
  - Namespaces MUST include labels:
    - `owner.team`
    - `environment`
    - `data.classification`

---

### 1.3 RBAC Isolation (Decision Rule)

- **[REQ-NS-RBAC-01] Least Privilege**
  - RBAC MUST grant minimum verbs and resources needed for the namespace.

- **[REQ-NS-RBAC-02] No Cross-Namespace Defaults**
  - Access to other namespaces MUST NOT be granted by default.

- **[BAN-NS-RBAC-01] Cluster-Admin for Tenant Workloads**
  - Tenant namespaces MUST NOT use cluster-admin bindings.

---

### 1.4 Resource Governance

- **[REQ-NS-RES-01] ResourceQuota Required**
  - Every tenant namespace MUST define a ResourceQuota.

- **[REQ-NS-RES-02] LimitRange Required**
  - Every tenant namespace MUST define a LimitRange.

- **[REQ-NS-RES-03] Requests/Limits Enforcement**
  - Workloads in tenant namespaces MUST define resource requests and limits.

---

### 1.5 Network Isolation

- **[REQ-NS-NET-01] Default Deny**
  - Tenant namespaces MUST have default-deny ingress and egress NetworkPolicies.

- **[REQ-NS-NET-02] Explicit Allows Only**
  - Traffic MUST be allowed explicitly for required dependencies.

- **[BAN-NS-NET-01] Wildcard Ingress/Egress**
  - Tenant namespaces MUST NOT allow unrestricted ingress or egress.

---

### 1.6 Success & Failure Behavior

- **[REQ-NS-SUCCESS-01] Success Criteria**
  - Multi-tenancy is valid ONLY if:
    - naming and labels exist
    - RBAC is least-privilege
    - quotas and limit ranges exist
    - default-deny network policies exist

- **[REQ-NS-FAIL-01] Failure Behavior**
  - Missing quotas/limit ranges/default-deny policies MUST block namespace creation and deployment.

---

### 1.7 Reference-First

- **[REQ-NS-REF-01] Canonical Examples**
  - Use canonical examples:
    - `namespaces/_examples/namespace-baseline.yaml`
    - `namespaces/_examples/resourcequota-baseline.yaml`
    - `namespaces/_examples/limitrange-baseline.yaml`
    - `namespaces/_examples/networkpolicy-default-deny.yaml`

---

## 2. Procedures (Phased Execution)

### Phase P1 — Create Namespace Baseline

1) Create namespace with required naming and labels.
2) Apply baseline policies.

- **Outcome**: Namespace identity and governance metadata exist.

### Phase P2 — Apply Isolation Controls

1) Apply least-privilege RBAC.
2) Apply ResourceQuota and LimitRange.
3) Apply default-deny NetworkPolicies.

- **Outcome**: Tenant isolation is enforceable.

### Phase P3 — Validate Isolation

1) Verify cross-namespace access is denied by default.
2) Verify only explicit traffic is allowed.

- **Outcome**: Isolation is verified, not assumed.

---

## 3. Examples

### Good Example — Tenant Namespace Baseline

**Input**

- Namespace includes required labels, RBAC, ResourceQuota, LimitRange, and default-deny NetworkPolicy.

**Expected Output**

- Workloads are isolated and resource usage is bounded.

### Bad Example — Missing Default Deny

**Input**

- Namespace created without any NetworkPolicy.

**Rejected Because**

- Violates `[REQ-NS-NET-01]` and `[REQ-NS-FAIL-01]`.

---

## 4. Validation Criteria (Final Checklist)

- [ ] Naming and mandatory labels exist. (`[REQ-NS-NAM-01]`, `[REQ-NS-LBL-01]`)
- [ ] RBAC is least-privilege and not cluster-admin. (`[REQ-NS-RBAC-01]`, `[BAN-NS-RBAC-01]`)
- [ ] ResourceQuota and LimitRange exist. (`[REQ-NS-RES-01]`, `[REQ-NS-RES-02]`)
- [ ] Default-deny NetworkPolicies exist with explicit allows. (`[REQ-NS-NET-*]`, `[BAN-NS-NET-01]`)

---

## See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- @0200-Security-Guardrails.md
- examples/namespaces/namespace-baseline.yaml
- examples/namespaces/resourcequota-baseline.yaml
- examples/namespaces/limitrange-baseline.yaml
- examples/namespaces/networkpolicy-default-deny.yaml
