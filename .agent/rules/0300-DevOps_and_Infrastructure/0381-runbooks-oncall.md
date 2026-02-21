---
trigger: model_decision
glob:
  - "runbooks/**/*.md"
  - "services/**"
  - "docs/oncall/**/*.md"
description: "Runbook and on-call standards: deterministic runbook structure, service ownership, dashboards/alerts linkage, and escalation rules."
---

# 1500-Runbook-And-Oncall-Standards

- **Role**: Operations Readiness Owner
- **Purpose**: Ensure every service is operable via a deterministic runbook and on-call process with clear ownership, escalation, and verification steps.
- **Activates When**: Creating/updating services, operational docs, dashboards/alerts, or on-call procedures.

---

## 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites (Executable Contract)

- **[REQ-RBK-PREREQ-01] Service Ownership**
  - Every service MUST have an owner team and a primary contact route.

- **[REQ-RBK-PREREQ-02] Runbook Location**
  - Each service MUST have a runbook at:
    - `runbooks/services/<service-name>.md`
  - If no runbook exists, production-like deployment MUST be blocked.

- **[REQ-RBK-OUT-01] Out of Scope**
  - This Rule does NOT define incident severity. See incident rule.
  - This Rule defines service operational readiness and on-call structure.

---

### 1.2 Runbook Structure (Decision Rule)

- **[REQ-RBK-STR-01] Mandatory Sections**
  - Every service runbook MUST include:
    - Service Overview
    - Dependencies
    - SLOs/SLIs (if customer-facing)
    - Dashboards
    - Alerts (with routing)
    - Common Failures and Fixes
    - Safe Rollback Procedure
    - Data Safety Notes (if stateful)
    - Escalation Path
    - Verification Steps (post-fix)

- **[REQ-RBK-STR-02] Deterministic Steps**
  - Each remediation procedure MUST be written as a step-by-step checklist with expected outcomes.

- **[BAN-RBK-STR-01] Narrative-Only Runbooks**
  - Runbooks MUST NOT be narrative-only documents without executable steps.

---

### 1.3 Dashboard and Alert Linkage

- **[REQ-RBK-LNK-01] Dashboard Links**
  - Runbooks MUST link to the primary dashboards for:
    - latency
    - errors
    - saturation
    - dependency health

- **[REQ-RBK-LNK-02] Alert Links and Routing**
  - Runbooks MUST link to alert definitions and specify the routing destination for pages/tickets.

---

### 1.4 On-Call Standards

- **[REQ-ONC-STD-01] Escalation Path**
  - Every service MUST define:
    - primary on-call route
    - secondary escalation
    - management escalation for SEV-1

- **[REQ-ONC-STD-02] Handoff Procedure**
  - On-call rotations MUST include a handoff checklist:
    - ongoing incidents
    - recent changes
    - known risks
    - pending action items

- **[REQ-ONC-STD-03] Paging Criteria**
  - Paging MUST be reserved for conditions that require immediate human action.

---

### 1.5 Success & Failure Behavior

- **[REQ-RBK-SUCCESS-01] Success Criteria**
  - A service is operationally ready ONLY if:
    - runbook exists and is complete
    - dashboards and alerts are linked
    - escalation path exists
    - rollback and verification steps exist

- **[REQ-RBK-FAIL-01] Failure Behavior**
  - If a required runbook section is missing, the change MUST be blocked for production-like deploys.

---

### 1.6 Reference-First

- **[REQ-RBK-REF-01] Canonical Templates**
  - Use canonical templates:
    - `templates/operations/runbook-template.md`
    - `templates/guides/handoff-checklist-template.md`

- **[REQ-RBK-REF-02] Minimal Snippets Only**
  - Snippets MAY be included only as anchors (≤ 30 lines OR ≤ 200 words).

---

## 2. Procedures (Phased Execution)

### Phase P1 — Create/Update Runbook

1) Create service runbook from canonical template.
2) Fill mandatory sections with links and checklists.

- **Outcome**: Runbook is executable and complete.

### Phase P2 — Link Observability and Alerts

1) Link dashboards and alerts.
2) Validate routing destinations.

- **Outcome**: Operators can navigate from symptoms to actions.

### Phase P3 — Validate Rollback and Verification

1) Document safe rollback steps.
2) Document verification steps and expected outputs.

- **Outcome**: Fixes can be safely applied and verified.

### Phase P4 — On-Call Readiness

1) Define escalation chain.
2) Establish handoff checklist.

- **Outcome**: On-call operation is deterministic.

---

## 3. Examples

### Good Example — Operable Service

**Input**

- New service includes runbook with dashboards, alerts, rollback, verification, and escalation chain.

**Expected Output**

- Service is deployable to production-like environments.

### Bad Example — Missing Rollback Procedure

**Input**

- Runbook exists but includes no rollback steps.

**Rejected Because**

- Violates `[REQ-RBK-STR-01]` and `[REQ-RBK-FAIL-01]`.

---

## 4. Validation Criteria (Final Checklist)

- [ ] Runbook exists at required path. (`[REQ-RBK-PREREQ-02]`)
- [ ] Mandatory sections exist. (`[REQ-RBK-STR-01]`)
- [ ] Procedures are checklist-based with outcomes. (`[REQ-RBK-STR-02]`)
- [ ] Dashboards and alerts are linked with routing. (`[REQ-RBK-LNK-*]`)
- [ ] Escalation and handoff procedures exist. (`[REQ-ONC-STD-*]`)
- [ ] Rollback and verification steps exist. (`[REQ-RBK-STR-01]`)

---

## See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- @1400-Incident-Response-Postmortem.md
- templates/operations/runbook-template.md
- templates/guides/handoff-checklist-template.md
