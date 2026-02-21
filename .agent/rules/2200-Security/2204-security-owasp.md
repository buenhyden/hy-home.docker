---
trigger: always_on
glob: "**/*.{py,js,ts,go,java,json,yaml}"
description: "OWASP Security Standards: Technical standards for Injection, Authentication, Access Control, and Data Protection based on OWASP Top 10."
---

# OWASP Security Standards

- **Role**: Application Security Lead
- **Purpose**: Define technical standards for mitigating the OWASP Top 10 vulnerabilities through consistent implementation patterns.
- **Activates When**: Developing application logic, handling authentication, or configuring security headers.

**Trigger**: always_on — Apply at all times during the implementation phase.

## 1. Standards

### Principles

- **[REQ-OWASP-01] Parameterized Execution**
  - All external commands and database queries MUST use parameterized inputs to prevent injection (A03).
- **[REQ-OWASP-02] Absolute Denial**
  - Access control MUST default to "Deny" for all resources. Permissions MUST be explicitly granted (A01).
- **[REQ-OWASP-03] Cryptographic Hygiene**
  - Only modern, peer-reviewed cryptographic algorithms (e.g., Argon2, AES-256-GCM) MUST be used for sensitive data (A02).

### Top 10 Mapping

| Category | Requirement ID | Critical Action |
| --- | --- | --- |
| A01: Broken Access Control | [REQ-OWASP-04] | Deny by Default |
| A02: Crypto Failures | [REQ-OWASP-05] | Argon2id for Hashing |
| A03: Injection | [REQ-OWASP-06] | Prepared Statements |
| A07: Auth Failures | [REQ-OWASP-07] | MFA for Admin Roles |

### Must

- **[REQ-OWASP-08] Secure Cookie Attributes**
  - Session cookies MUST be configured with `HttpOnly`, `Secure`, and `SameSite=Strict`.
- **[REQ-OWASP-09] IDOR Prevention**
  - Systems MUST verify that the authenticated user explicitly owns the resource identified by the UUID.
- **[REQ-OWASP-10] Strict SSRF Validation**
  - Outgoing URLs MUST be validated against a strict domain allow-list before request initiation.

### Must Not

- **[BAN-OWASP-01] Raw Password Storage**
  - Passwords MUST NOT be stored in plain text or using weak hashing (MD5, SHA1).
- **[BAN-OWASP-02] Verbose Error Leakage**
  - Stack traces and internal error messages MUST NOT be exposed to end users in production.

### Failure Handling

- **Stop Condition**: Stop the deployment if the automated dependency audit (SCA) identifies any "Critical" vulnerabilities.

## 2. Procedures

- **[PROC-OWASP-01] Secure Header Audit**
  - IF deploying a web application THEN MUST verify that HSTS, CSP, and X-Content-Type-Options headers are active.
- **[PROC-OWASP-02] Password Rotation**
  - Rotate session IDs immediately upon user login to prevent session fixation attacks.

## 3. Examples

### Secure Authentication Flow

```javascript
// Good: Secure cookie configuration
res.cookie('sessionID', id, { httpOnly: true, secure: true, sameSite: 'strict' });
```

## 4. Validation Criteria

- **[VAL-OWASP-01] DAST/SAST Pass**
  - [ ] Automated security scanners confirm zero high-risk vulnerabilities on the primary branch.
- **[VAL-OWASP-02] Penetration Smoke Test**
  - [ ] Manual verification confirms that standard IDOR patterns are successfully blocked.
- **[VAL-OWASP-03] CSP Efficacy**
  - [ ] Browser console verifies that CSP rules correctly block unauthorized script execution.
