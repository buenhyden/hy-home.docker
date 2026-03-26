---
layer: security
description: "Rule for baseline hardening, least privilege enforcement, and secure default posture."
---

# Security — Hardening Rule

## Case
- **[REQ-SEC-01]** Deny by default for sensitive access paths.
- **[REQ-SEC-02]** Verify identity and trust boundaries for protected operations.
- **[REQ-SEC-03]** Apply least privilege to runtime and data access.
- **[REQ-SEC-10]** Enforce web/application hardening controls on exposed surfaces.

## Style
- **[PROC-SEC-GEN-01]** Keep hardening controls explicit and auditable.
- **[REQ-SEC-06]** Protect sensitive data in transit and at rest.
- **[BAN-SEC-01]** No plaintext credentials or secrets in source artifacts.

## Validation
- [ ] Access controls are explicit and least-privilege aligned.
- [ ] Hardening controls cover critical exposed surfaces.
- [ ] Secret/data protection checks pass.
