---
trigger: model_decision
glob: ["k8s/**/*.yml"]
description: "Progressive delivery: deterministic canary/blue-green rollouts with automated rollback triggers and post-deploy verification."
---
# 0600-Progressive-Delivery-Rollbacks

## Activation
- [ ] Apply when Deploying or changing production-like workloads, rollout controllers, traffic routing, or release strategies..
- [ ] Apply when editing files matching: `k8s/**/*.yml`.

## Rules
- **Role**: Release Engineering Owner
- **Purpose**: Enforce progressive delivery with deterministic rollout and rollback rules so production risk is minimized and failures revert automatically.
- **Activates When**: Deploying or changing production-like workloads, rollout controllers, traffic routing, or release strategies.

---

### 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites (Executable Contract)

- **[REQ-PD-PREREQ-01] Progressive Delivery Controller Exists**
  - A progressive delivery mechanism MUST exist (e.g., Argo Rollouts or equivalent).
  - If not available, production deployments MUST be blocked.

- **[REQ-PD-PREREQ-02] Metrics Provider Exists**
  - A metrics provider MUST exist for rollout analysis (latency/error/availability).
  - If analysis metrics are not available, progressive delivery MUST be blocked.

- **[REQ-PD-OUT-01] Out of Scope**
  - This Rule does NOT define business SLO targets.
  - This Rule defines rollout safety and automation behavior.

---

### 1.2 Allowed Strategies (Decision Rule)

- **[REQ-PD-STR-01] Allowed Release Strategies**
  - Production-like releases MUST use one of:
    - Canary
    - Blue-Green
  - Direct full traffic cutover MUST NOT be used.

- **[REQ-PD-STR-02] Strategy Must Be Explicit**
  - Rollout manifests MUST explicitly declare the strategy and steps.

- **[BAN-PD-STR-01] No Uncontrolled Deployments**
  - Deployments that bypass progressive delivery MUST be rejected.

---

### 1.3 Automated Analysis and Rollback

- **[REQ-PD-ANL-01] Analysis Metrics Required**
  - Rollouts MUST evaluate at minimum:
    - error rate
    - latency (p95 or histogram-based threshold)
    - availability (success ratio)

- **[REQ-PD-ANL-02] Deterministic Failure Thresholds**
  - Each workload MUST define concrete thresholds.
  - If thresholds are missing, the change MUST be blocked.

- **[REQ-PD-RBK-01] Automated Rollback**
  - If analysis fails, rollback MUST trigger automatically.
  - Manual rollback-only strategies MUST be rejected.

- **[REQ-PD-RBK-02] Rollback Completeness**
  - Rollback MUST restore:
    - prior stable replica set
    - prior stable traffic routing
    - prior stable config references

---

### 1.4 Post-Deploy Verification

- **[REQ-PD-VER-01] Smoke Verification**
  - After rollout completion, a smoke verification MUST run:
    - health endpoints
    - critical API route checks (if applicable)

- **[REQ-PD-VER-02] Observability Confirmation**
  - A release MUST confirm:
    - logs exist
    - metrics moved as expected
    - traces appear for a sample request (if tracing enabled)

---

### 1.5 Success & Failure Behavior

- **[REQ-PD-SUCCESS-01] Success Criteria**
  - A release is successful ONLY if:
    - rollout completes
    - analysis passes
    - smoke verification passes
    - observability confirmation passes

- **[REQ-PD-FAIL-01] Failure Behavior**
  - If analysis fails, rollback MUST be automatic.
  - If verification fails, rollback MUST trigger unless explicitly justified and approved.

---

### 1.6 Reference-First

- **[REQ-PD-REF-01] Canonical Rollout Examples**
  - Use canonical examples:
    - `delivery/_examples/canary-rollout.yaml`
    - `delivery/_examples/bluegreen-rollout.yaml`
    - `delivery/_examples/analysis-template.yaml`

- **[REQ-PD-REF-02] Minimal Snippets Only**
  - Snippets MAY be included only as anchors (≤ 30 lines OR ≤ 200 words).

---

### 2. Procedures (Phased Execution)

### Phase P1 — Strategy Selection

1) Choose Canary or Blue-Green based on blast radius and traffic routing capability.
2) Define rollout steps and analysis windows.

- **Outcome**: A declared progressive strategy exists per `[REQ-PD-STR-02]`.

### Phase P2 — Analysis Definition

1) Define error/latency/availability thresholds.
2) Bind analysis templates to rollout steps.

- **Outcome**: Automated analysis is enforceable per `[REQ-PD-ANL-*]`.

### Phase P3 — Execute Progressive Rollout

1) Shift traffic gradually (Canary) or switch environments (Blue-Green).
2) Run analysis at each step.

- **Outcome**: Rollout proceeds only if metrics remain healthy.

### Phase P4 — Rollback if Needed

1) If analysis fails, rollback automatically.
2) Confirm stable state restored.

- **Outcome**: Automated rollback completes per `[REQ-PD-RBK-*]`.

### Phase P5 — Post-Deploy Verification

1) Run smoke checks.
2) Confirm telemetry presence.

- **Outcome**: Release is either verified or reverted per `[REQ-PD-SUCCESS-01]`.

---

### 3. Examples

### Good Example — Canary with Auto Rollback

**Input**

- Canary steps: 10% → 25% → 50% → 100% with analysis at each step.

**Expected Output**

- If error rate increases above threshold, rollback triggers automatically.

### Bad Example — Direct Full Cutover

**Input**

- Deployment updates replicas and immediately routes 100% traffic without analysis.

**Rejected Because**

- Violates `[REQ-PD-STR-01]` and `[BAN-PD-STR-01]`.

---

### 4. Validation Criteria (Final Checklist)

- [ ] Progressive delivery controller exists. (`[REQ-PD-PREREQ-01]`)
- [ ] Metrics provider exists for analysis. (`[REQ-PD-PREREQ-02]`)
- [ ] Strategy is Canary or Blue-Green and explicit. (`[REQ-PD-STR-*]`)
- [ ] Thresholds are deterministic and present. (`[REQ-PD-ANL-02]`)
- [ ] Rollback is automatic and complete. (`[REQ-PD-RBK-*]`)
- [ ] Smoke + observability verification exists. (`[REQ-PD-VER-*]`)

---

### See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- examples/delivery/canary-rollout.yaml
- examples/delivery/bluegreen-rollout.yaml
- examples/delivery/analysis-template.yaml

## References
- None.
