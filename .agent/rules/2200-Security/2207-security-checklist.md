---
trigger: always_on
glob: ["**/*"]
description: "Security Master Checklist: Comprehensive audit checklist for Authentication, Input Validation, Data Protection, and AI Safety."
---

# Security Master Checklist

- **Role**: Quality Assurance & Security Auditor
- **Purpose**: Provide a comprehensive verification checklist for ensuring cross-domain security compliance during the development and review process.
- **Activates When**: Performing code reviews, conducting a11y/security audits, or preparing for production release.

**Trigger**: always_on — Apply at all times to ensure continuous security verification.

## 1. Standards

### Principles

- **[REQ-SEC_CHK-01] Universal Verification**
  - All checklists MUST be completed for every major feature release to ensure no security regression.
- **[REQ-SEC_CHK-02] Evidence-Based Pass**
  - "Pass" status for checklist items MUST be supported by verifiable evidence (e.g., test logs, screenshots, audit reports).
- **[REQ-SEC_CHK-03] Cross-Domain Coverage**
  - Verification MUST span across Authentication, Input handling, Data Protection, API security, and AI Safety.

### Core Audit Blocks

| Domain | Reference Rule | Critical Verification |
| --- | --- | --- |
| Authentication | `2204-security-owasp.md` | Argon2 hashing / MFA used |
| Input Validation | `2220-secure-coding.md` | All inputs parameterized |
| Data Protection | `2400-compliance-pillar.md` | PII encrypted & masked |
| AI Safety | `2210-security-ai-foundations.md` | Prompt delimiters & Scrubbing |

### Must

- **[REQ-SEC_CHK-04] Mandatory MFA Audit**
  - [ ] Verify that MFA is enforced for all administrative and user-level sensitive actions.
- **[REQ-SEC_CHK-05] Injection Proofing**
  - [ ] Verify that 100% of database queries utilize parameterized statements or prepared queries.
- **[REQ-SEC_CHK-06] Secret Clearance**
  - [ ] Verify that zero hardcoded secrets exist in the source code or integrated configuration files.

### Must Not

- **[BAN-SEC_CHK-01] Silent Failure Adoption**
  - Checklists MUST NOT be marked as complete if a critical risk item is ignored or bypassed without a documented ADR.
- **[BAN-SEC_CHK-02] Generic Pass**
  - Avoid checking items as "Pass" without verifying the implementation against the specific target Rule.

### Failure Handling

- **Stop Condition**: Stop the release process if more than 3 high-risk items in the checklist are unverified or failed.

## 2. Procedures

- **[PROC-SEC_CHK-01] Audit Execution**
  - IF starting a security review THEN MUST work through each section of the Master Checklist sequentially.
- **[PROC-SEC_CHK-02] Compliance Reporting**
  - Generate a "Security Compliance Report" artifact based on the checklist results for every major PR.

## 3. Examples

### Checklist Application

```text
[x] [REQ-SEC_CHK-05] Parameterization: Confirmed in auth.py and user_dao.ts.
[x] [REQ-SEC_CHK-06] Secret Clearance: Gitleaks pass verified.
```

## 4. Validation Criteria

- **[VAL-SEC_CHK-01] Verification Completeness**
  - [ ] Every item in the checklist is accounted for in the final audit report.
- **[VAL-SEC_CHK-02] Compliance Traceability**
  - [ ] Every checklist pass links to a specific implementation task or rule requirement.
- **[VAL-SEC_CHK-03] AI Safety Maturity**
  - [ ] AI feature testing proves resilience against both Prompt Injection and Insecure Output Handling.
