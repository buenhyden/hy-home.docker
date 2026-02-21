---
trigger: model_decision
glob:
  - "k8s/**/*.yml"
  - "k8s/**/*.yaml"
  - "manifests/**/*.yml"
  - "manifests/**/*.yaml"
  - "helm/**"
description: "Storage standards: StorageClass usage, PVC sizing, access modes, snapshot/retention, and encryption-at-rest requirements."
---

# 0900-Storage-Policy-Standards

- **Role**: Storage Platform Owner
- **Purpose**: Ensure storage usage is consistent, safe, and recoverable with deterministic policies for PVCs, snapshots, retention, and encryption.
- **Activates When**: Adding/modifying PVCs, StatefulSets, StorageClasses, or snapshot/backup-related configuration.

---

## 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites (Executable Contract)

- **[REQ-STO-PREREQ-01] StorageClass Defined**
  - Workloads MUST reference an explicit StorageClass.
  - If none is defined, the change MUST be blocked.

- **[REQ-STO-OUT-01] Out of Scope**
  - This Rule does NOT mandate a specific storage vendor.
  - This Rule enforces consistent storage policy behavior.

---

### 1.2 PVC Requirements

- **[REQ-STO-PVC-01] Explicit Size**
  - PVCs MUST define an explicit requested size.

- **[REQ-STO-PVC-02] Access Mode Correctness**
  - Access modes MUST match workload requirements (RWO/ROX/RWX).

- **[BAN-STO-PVC-01] Unbounded Growth Without Policy**
  - Unbounded expansion MUST NOT be used without capacity planning and monitoring.

---

### 1.3 Snapshot and Retention

- **[REQ-STO-SNP-01] Snapshot Policy for Critical Data**
  - Critical stateful workloads MUST define a snapshot/backup policy.

- **[REQ-STO-SNP-02] Retention**
  - Retention MUST be explicitly declared.

---

### 1.4 Encryption-at-Rest

- **[REQ-STO-ENC-01] Encryption Requirement**
  - Persistent data MUST be encrypted at rest when supported by the platform.

---

### 1.5 Success & Failure Behavior

- **[REQ-STO-SUCCESS-01] Success Criteria**
  - Storage configuration is valid ONLY if PVC sizing, access modes, and retention are explicit.

- **[REQ-STO-FAIL-01] Failure Behavior**
  - Missing StorageClass/PVC size/retention MUST block the change.

---

### 1.6 Reference-First

- **[REQ-STO-REF-01] Canonical Examples**
  - `storage/_examples/pvc-baseline.yaml`
  - `storage/_examples/snapshot-policy.yaml`

---

## 2. Procedures (Phased Execution)

### Phase P1 — Define Storage Needs

1) Identify stateful components and IO profile.
2) Choose StorageClass and access mode.

- **Outcome**: Storage intent is explicit.

### Phase P2 — Declare PVC and Policies

1) Add PVC with explicit size and access mode.
2) Add snapshot/retention if critical.

- **Outcome**: Storage is compliant.

---

## 3. Examples

### Good Example — Explicit PVC

**Input**

- PVC with size, StorageClass, and snapshot retention.

**Expected Output**

- Predictable capacity and recoverability.

### Bad Example — Missing StorageClass

**Input**

- PVC without StorageClass.

**Rejected Because**

- Violates `[REQ-STO-PREREQ-01]`.

---

## 4. Validation Criteria (Final Checklist)

- [ ] StorageClass is explicit. (`[REQ-STO-PREREQ-01]`)
- [ ] PVC size and access mode are explicit. (`[REQ-STO-PVC-*]`)
- [ ] Retention is declared for critical data. (`[REQ-STO-SNP-*]`)

---

## See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- examples/storage/pvc-baseline.yaml
- examples/storage/snapshot-policy.yaml
