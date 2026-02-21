---
trigger: model_decision
glob:
  - "runbooks/incidents/**/*.md"
  - "docs/incidents/**/*.md"
  - "docs/postmortems/**/*.md"
description: "Incident response and postmortems: deterministic severity model, roles, comms, timelines, and action-item governance."
---

# 1400-Incident-Response-Postmortem

- **Role**: Incident Management Owner
- **Purpose**: Enforce deterministic incident response and postmortem practices so outages are contained quickly and corrective actions are tracked to completion.
- **Activates When**: Declaring an incident, handling production-impacting events, or creating/updating incident reports and postmortems.

---

## 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites (Executable Contract)

- **[REQ-INC-PREREQ-01] Incident Workspace**
  - An incident workspace MUST exist (channel/room + document location).
  - If no incident workspace exists, incident declaration MUST create it immediately.

- **[REQ-INC-PREREQ-02] Postmortem Template**
  - A canonical postmortem template MUST exist.
  - If no template exists, postmortem creation MUST be blocked until the template is added.

- **[REQ-INC-OUT-01] Out of Scope**
  - This Rule does NOT define product decisions.
  - This Rule defines response governance, documentation, and corrective-action tracking.

---

### 1.2 Severity Model (Decision Rule)

- **[REQ-INC-SEV-01] Severity Levels**
  - Incidents MUST be classified as one of: SEV-1, SEV-2, SEV-3.

- **[REQ-INC-SEV-02] SEV Criteria**
  - SEV-1 MUST mean: widespread user impact OR data loss risk OR security breach in progress.
  - SEV-2 MUST mean: partial user impact OR significant degradation OR high-risk dependency failure.
  - SEV-3 MUST mean: limited impact OR internal-only impact OR non-urgent degradation.

- **[REQ-INC-SEV-03] Escalation**
  - If impact expands, severity MUST be escalated immediately.
  - Severity MUST NOT be lowered until impact is proven reduced.

---

### 1.3 Roles and Responsibilities

- **[REQ-INC-ROLE-01] Required Roles**
  - Every incident MUST have:
    - Incident Commander (IC)
    - Communications Lead (CL)
    - Operations Lead (OL)
  - One person MAY hold multiple roles ONLY for SEV-3.

- **[REQ-INC-ROLE-02] Single Decision Authority**
  - IC MUST be the single authority for operational decisions during the incident.

---

### 1.4 Communication and Timeline

- **[REQ-INC-COMMS-01] Update Cadence**
  - Incidents MUST publish status updates on a fixed cadence:
    - SEV-1: at least every 15 minutes
    - SEV-2: at least every 30 minutes
    - SEV-3: at least every 60 minutes

- **[REQ-INC-COMMS-02] Status Content**
  - Each status update MUST include:
    - current impact
    - current hypothesis
    - mitigation actions
    - next update time

- **[REQ-INC-TIME-01] Event Timeline**
  - The incident document MUST include a timestamped timeline with:
    - detection time
    - declaration time
    - mitigation start
    - mitigation complete
    - full resolution time

---

### 1.5 Postmortem Requirements

- **[REQ-INC-PM-01] Postmortem Required**
  - SEV-1 and SEV-2 incidents MUST produce a postmortem.
  - SEV-3 incidents MUST produce a postmortem if:
    - recurring issue OR
    - systemic weakness OR
    - customer escalation

- **[REQ-INC-PM-02] Postmortem Contents**
  - Postmortem MUST include:
    - impact summary
    - root cause analysis (RCA)
    - contributing factors
    - detection gaps
    - remediation actions
    - prevention actions

- **[REQ-INC-PM-03] Action Items**
  - Every action item MUST have:
    - owner
    - due date
    - verification method
    - link to tracking ticket

- **[BAN-INC-PM-01] Blame Language**
  - Postmortems MUST NOT include blame-focused language.
  - Postmortems MUST describe system/process failures and verifiable facts.

---

### 1.6 Success & Failure Behavior

- **[REQ-INC-SUCCESS-01] Success Criteria**
  - Incident handling is valid ONLY if:
    - severity is classified
    - roles are assigned
    - timeline exists
    - comms cadence is met
    - postmortem is completed when required
    - action items are tracked

- **[REQ-INC-FAIL-01] Failure Behavior**
  - If required roles or cadence are missing for SEV-1/2, escalation MUST occur immediately.
  - If postmortem is required and missing, closure MUST be blocked.

---

### 1.7 Reference-First

- **[REQ-INC-REF-01] Canonical Templates**
  - Use canonical templates instead of copying:
    - `templates/operations/runbook-template.md`
    - `templates/operations/postmortem-template.md`

- **[REQ-INC-REF-02] Minimal Snippets Only**
  - Snippets MAY be included only as anchors (≤ 30 lines OR ≤ 200 words).

---

## 2. Procedures (Phased Execution)

### Phase P1 — Declare and Staff

1) Classify severity (SEV-1/2/3).
2) Assign IC, CL, OL.
3) Create incident workspace and incident doc.

- **Outcome**: Incident is operationally owned and documented.

### Phase P2 — Stabilize and Mitigate

1) Identify blast radius and immediate mitigations.
2) Execute mitigations under IC decision authority.

- **Outcome**: Impact is reduced measurably.

### Phase P3 — Communicate

1) Publish updates per cadence.
2) Maintain timeline entries.

- **Outcome**: Stakeholders have reliable situational awareness.

### Phase P4 — Resolve and Verify

1) Confirm service health and customer impact resolution.
2) Close incident only after verification.

- **Outcome**: Resolution is verified, not assumed.

### Phase P5 — Postmortem and Actions

1) Produce postmortem (if required).
2) Create action items with owners/dates/verifications.

- **Outcome**: Learnings become tracked improvements.

---

## 3. Examples

### Good Example — SEV-1 Handling

**Input**

- Widespread outage detected; SEV-1 declared; IC/CL/OL assigned; updates every 15 minutes; mitigation executed; postmortem created with action items.

**Expected Output**

- Incident closes only after verification; postmortem and action items exist and are tracked.

### Bad Example — Missing Postmortem

**Input**

- SEV-2 incident resolved, but no postmortem is created.

**Rejected Because**

- Violates `[REQ-INC-PM-01]` and `[REQ-INC-FAIL-01]`.

---

## 4. Validation Criteria (Final Checklist)

- [ ] Severity classified and recorded. (`[REQ-INC-SEV-01]`)
- [ ] IC/CL/OL assigned. (`[REQ-INC-ROLE-01]`)
- [ ] Update cadence met for severity. (`[REQ-INC-COMMS-01]`)
- [ ] Timeline includes required timestamps. (`[REQ-INC-TIME-01]`)
- [ ] Postmortem exists when required and contains required sections. (`[REQ-INC-PM-01]`, `[REQ-INC-PM-02]`)
- [ ] Action items have owner, due date, verification, ticket link. (`[REQ-INC-PM-03]`)
- [ ] No blame language present. (`[BAN-INC-PM-01]`)

---

## See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- templates/operations/runbook-template.md
- templates/operations/postmortem-template.md
