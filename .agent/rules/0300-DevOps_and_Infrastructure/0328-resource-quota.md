---
trigger: model_decision
glob:
  - "k8s/**/*.yml"
  - "k8s/**/*.yaml"
  - "manifests/**/*.yml"
  - "manifests/**/*.yaml"
  - "helm/**"
description: "Resource policy: requests/limits, autoscaling, disruption budgets, scheduling constraints, and namespace quotas."
---

# 1200-Resource-Quota-Scheduling

- **Role**: Cluster Reliability Owner
- **Purpose**: Enforce deterministic resource and scheduling policies to prevent noisy-neighbor issues and ensure stable scaling and availability.
- **Activates When**: Creating/updating Deployments/StatefulSets, HPA, PDB, or namespace resource policies.

---

## 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites

- **[REQ-RES-PREREQ-01] Resource Governance Enabled**
  - Cluster MUST support resource requests/limits and quotas.
  - If not supported, production-like deploys MUST be blocked.

---

### 1.2 Requests & Limits

- **[REQ-RES-RL-01] Requests Required**
  - Every container MUST define CPU and memory requests.

- **[REQ-RES-RL-02] Limits Required**
  - Every container MUST define CPU and memory limits (unless explicitly justified).

---

### 1.3 Autoscaling and Availability

- **[REQ-RES-HPA-01] Autoscaling Policy**
  - Customer-facing services MUST define HPA or a scaling strategy.

- **[REQ-RES-PDB-01] Disruption Budget**
  - Multi-replica workloads MUST define a PDB.

---

### 1.4 Scheduling Constraints

- **[REQ-RES-SCH-01] Anti-Affinity for HA**
  - Critical workloads SHOULD distribute replicas across nodes via anti-affinity.
  - If anti-affinity is not possible, justification MUST be recorded.

> Note: This is the only place “should” appears in this document.
> Replace with MUST in your environment if strict enforcement is required.

---

### 1.5 Success & Failure

- **[REQ-RES-SUCCESS-01] Success Criteria**
  - Workloads are valid ONLY if requests/limits exist and availability is protected.

- **[REQ-RES-FAIL-01] Failure Behavior**
  - Missing requests MUST reject the change.

---

### 1.6 Reference-First

- **[REQ-RES-REF-01] Canonical Examples**
  - `resources/_examples/requests-limits-baseline.yaml`
  - `resources/_examples/hpa-baseline.yaml`
  - `resources/_examples/pdb-baseline.yaml`

---

## 2. Procedures

### Phase P1 — Define Baselines

1) Set requests/limits for each container.

- **Outcome**: Resource boundaries exist.

### Phase P2 — Add Availability Controls

1) Add HPA if applicable.
2) Add PDB for multi-replica services.

- **Outcome**: Scaling and disruptions are controlled.

---

## 3. Examples

### Good Example — Stable Baselines

**Input**

- Requests/limits + HPA + PDB for a critical service.

**Expected Output**

- Predictable scaling and safe maintenance.

### Bad Example — No Requests

**Input**

- Deployment without resource requests.

**Rejected Because**

- Violates `[REQ-RES-RL-01]`.

---

## 4. Validation Criteria

- [ ] CPU/memory requests exist. (`[REQ-RES-RL-01]`)
- [ ] CPU/memory limits exist or justified. (`[REQ-RES-RL-02]`)
- [ ] HPA exists when required. (`[REQ-RES-HPA-01]`)
- [ ] PDB exists for multi-replica workloads. (`[REQ-RES-PDB-01]`)

---

## See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- examples/resources/requests-limits-baseline.yaml
- examples/resources/hpa-baseline.yaml
- examples/resources/pdb-baseline.yaml
