---
layer: security
description: "Rule for secure coding constraints, vulnerability prevention, and implementation-level safeguards."
---

# Security — Secure Coding Rule

## Case
- **[REQ-SC-01]** Apply secure coding patterns for input, auth, and data handling.
- **[REQ-OWASP-01]** Address OWASP-priority vulnerability classes in implementation.
- **[REQ-AUTH-01]** Keep authentication and authorization boundaries explicit.

## Style
- **[PROC-SC-01]** Validate tainted input at trust boundaries.
- **[REQ-SC-03]** Use safe defaults for error handling and exposure control.
- **[BAN-SC-01]** Avoid insecure shortcuts that bypass validation controls.
- **[BAN-OWASP-01]** Do not ship known high-severity vulnerability patterns.

## Validation
- [ ] Secure coding checks are applied to changed code paths.
- [ ] OWASP-sensitive vectors are mitigated.
- [ ] AuthN/AuthZ behavior is validated for protected operations.
