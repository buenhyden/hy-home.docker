---
trigger: model_decision
glob: ["k8s/**/*.yml"]
description: "Backup/Restore governance: deterministic schedules, retention, encryption, restore drills, and RPO/RTO validation for stateful systems."
---
# 0800-Backup-Restore-Drill

## Activation

- [ ] Apply when Deploying/updating stateful services (DB, object storage, message brokers, volumes) or changing storage/backup configuration..
- [ ] Apply when editing files matching: `k8s/**/*.yml`.

## Rules

- **Role**: Reliability & Data Protection Owner
- **Purpose**: Guarantee that every stateful component has deterministic backups and verified restore capability via drills that meet defined RPO/RTO expectations.
- **Activates When**: Deploying/updating stateful services (DB, object storage, message brokers, volumes) or changing storage/backup configuration.

---

### 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites (Executable Contract)

- **[REQ-BCK-PREREQ-01] Backup Mechanism Exists**
  - A backup tool/process MUST exist for each stateful service (native or platform-level).
  - If no backup mechanism exists, the change MUST be blocked.

- **[REQ-BCK-PREREQ-02] Restore Environment Exists**
  - A restore target MUST exist (staging namespace or isolated environment).
  - If no restore target exists, the change MUST be blocked.

- **[REQ-BCK-OUT-01] Out of Scope**
  - This Rule does NOT dictate a specific vendor.
  - This Rule dictates deterministic backup/restore requirements and validation.

---

### 1.2 Backup Requirements

- **[REQ-BCK-BKP-01] Backup Schedule**
  - Every stateful workload MUST define:
    - backup frequency
    - backup start window (if required)
    - retention period

- **[REQ-BCK-BKP-02] Encryption**
  - Backups MUST be encrypted at rest.
  - Backup transport MUST be encrypted in transit.

- **[REQ-BCK-BKP-03] Integrity Verification**
  - Backups MUST include integrity verification (checksum or tool-native validation).

- **[BAN-BCK-BKP-01] No Backup, No Merge**
  - Stateful changes MUST NOT be merged without backup definitions.

---

### 1.3 Restore Requirements (Decision Rule)

- **[REQ-BCK-RST-01] Restore Procedure Defined**
  - Each stateful service MUST have a restore procedure in a Runbook.

- **[REQ-BCK-RST-02] Restore Drill Frequency**
  - Restore drills MUST run on a fixed cadence.
  - If drills cannot be run, the change MUST be blocked for production-like deployments.

- **[REQ-BCK-RST-03] RPO/RTO Declaration**
  - Each stateful workload MUST declare target:
    - RPO (Recovery Point Objective)
    - RTO (Recovery Time Objective)

- **[REQ-BCK-RST-04] Measured Outcomes**
  - Drill results MUST capture actual:
    - achieved RPO
    - achieved RTO

---

### 1.4 Success & Failure Behavior

- **[REQ-BCK-SUCCESS-01] Success Criteria**
  - Data protection is valid ONLY if:
    - backups run successfully
    - restore drill succeeds
    - measured RPO/RTO meet targets

- **[REQ-BCK-FAIL-01] Failure Behavior**
  - If restore drill fails, the rollout MUST be blocked.
  - If RPO/RTO targets are not met, the backup strategy MUST be revised before merge.

---

### 1.5 Reference-First

- **[REQ-BCK-REF-01] Canonical Runbook and Templates**
  - Use canonical templates:
    - `templates/operations/runbook-template.md`
    - `examples/reliability/backup-schedule.yaml`
    - `examples/reliability/restore-drill-checklist.md`

- **[REQ-BCK-REF-02] Minimal Snippets Only**
  - Snippets MAY be included only as anchors (≤ 30 lines OR ≤ 200 words).

---

### 2. Procedures (Phased Execution)

### Phase P1 — Inventory Stateful Components

1) Identify databases, volume-backed services, and persistent brokers.
2) Assign ownership and backup mechanism per component.

- **Outcome**: Every stateful component has a backup path per `[REQ-BCK-PREREQ-01]`.

### Phase P2 — Define Backup Policy

1) Set schedule, retention, and encryption requirements.
2) Add integrity verification.

- **Outcome**: Backup policy is deterministic per `[REQ-BCK-BKP-*]`.

### Phase P3 — Define Restore Procedure

1) Write restore runbook steps.
2) Define RPO/RTO targets.

- **Outcome**: Restore is executable per `[REQ-BCK-RST-*]`.

### Phase P4 — Execute Restore Drill

1) Restore into isolated target environment.
2) Validate service health and data correctness.
3) Record achieved RPO/RTO.

- **Outcome**: Restore drill result exists and is measurable.

### Phase P5 — Gate the Change

1) If drill fails, block merge and deployments.
2) If targets are unmet, revise strategy.

- **Outcome**: Deterministic go/no-go per `[REQ-BCK-SUCCESS-01]`.

---

### 3. Examples

### Good Example — Verified Restore

**Input**

- Nightly backups, 14-day retention, encrypted backups, monthly restore drill with recorded RPO/RTO.

**Expected Output**

- Drill succeeds and meets declared targets.

### Bad Example — Backups Without Restore Drill

**Input**

- Backups exist but no restore drill has ever been executed.

**Rejected Because**

- Violates `[REQ-BCK-RST-02]` and `[REQ-BCK-SUCCESS-01]`.

---

### 4. Validation Criteria (Final Checklist)

- [ ] Backup mechanism exists for each stateful service. (`[REQ-BCK-PREREQ-01]`)
- [ ] Backups have schedule, retention, encryption, integrity checks. (`[REQ-BCK-BKP-*]`)
- [ ] Restore runbook exists and is executable. (`[REQ-BCK-RST-01]`)
- [ ] Restore drills run on cadence and record RPO/RTO. (`[REQ-BCK-RST-02]`, `[REQ-BCK-RST-04]`)
- [ ] Failures block merges and deployments. (`[REQ-BCK-FAIL-01]`)

---

### See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- templates/operations/runbook-template.md
- examples/reliability/backup-schedule.yaml
- examples/reliability/restore-drill-checklist.md

## References

- None.
