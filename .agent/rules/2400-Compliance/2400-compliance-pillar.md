---
trigger: model_decision
glob: ["**/*"]
description: "Compliance Pillar: Enforces GDPR, HIPAA, and data privacy standards through minimization, residency, and encryption."
---

# Compliance Pillar

- **Role**: Compliance Officer / Data Protection Officer (DPO)
- **Purpose**: Ensure legal and ethical handling of user data and regulatory adherence.
- **Activates When**: Handling PII, designing data storage, or implementing system logs.

**Trigger**: model_decision — Apply during data architecture and privacy-sensitive design.

## 1. Standards

### Principles

- **[REQ-COM-01] Data Minimization**
  - Collection MUST be limited strictly to the data necessary for the declared business purpose.
- **[REQ-COM-02] Right to Deletion**
  - All systems MUST support the "Right to Forget" through hard deletion of user-identifiable data.
- **[REQ-COM-03] Regional Residency**
  - User data MUST reside in the legally required geographic region (e.g., EU data on EU servers).

### Compliance Frameworks

| Standard | Region | Core Requirement |
| --- | --- | --- |
| GDPR | European Union | Privacy by Design |
| CCPA | California, US | Consumer Data Control |
| HIPAA | United States | Protected Health Info (PHI) Safety |

### Must

- **[REQ-COM-04] Mandatory Encryption**
  - Personally Identifiable Information (PII) MUST be encrypted both at rest and in transit.
- **[REQ-COM-05] Schema Tagging**
  - Database schema definitions MUST explicitly tag PII fields (e.g., `@PII`) for auditability.
- **[REQ-COM-06] PII Masking**
  - Application logs MUST mask or redact PII fields (email, phone, IP) before persistence.

### Must Not

- **[BAN-COM-01] Unindexed PII Storage**
  - PII MUST NOT be stored in untracked, plain-text files or ephemeral storage.
- **[BAN-COM-02] Cross-Border Exfiltration**
  - User data MUST NOT be transferred across restricted jurisdictional boundaries without explicit legal framework (e.g., SCCs).

### Failure Handling

- **Stop Condition**: Stop data processing if an unauthorized PII leak is detected in logs or analytics.

## 2. Procedures

- **[PROC-COM-01] PII Audit**
  - IF creating a new data model THEN MUST perform a PII scan and update the tagging registry.
- **[PROC-COM-02] Deletion Verification**
  - IF a user requests account deletion THEN MUST verify hard deletion across all distributed databases.

## 3. Examples

### Semantic Tagging (Prisma)

```prisma
model User {
  id    Int    @id
  email String @unique // @PII
}
```

## 4. Validation Criteria

- **[VAL-COM-01] Log Hygiene**
  - [ ] A search for common PII patterns (email, phone) in production logs returns zero results.
- **[VAL-COM-02] Residency Verification**
  - [ ] Infrastructure audits confirm that EU customer data is hosted exclusively within EU availability zones.
- **[VAL-COM-03] Deletion Logic**
  - [ ] Deletion API tests confirm that data is removed, not just soft-deleted, from the primary database.
