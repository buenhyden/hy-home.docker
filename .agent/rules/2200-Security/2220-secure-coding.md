---
trigger: always_on
glob: "**/*.{py,js,ts,rs,go}"
description: "Secure Coding Standards: Enforces input validation, output encoding, and vulnerability mitigation strategies."
---

# Secure Coding Standards

- **Role**: Defensive Security Engineer
- **Purpose**: Define standards for writing code that is inherently resilient to attacks and data leakage.
- **Activates When**: Developing application logic, handling user input, or configuring data persistence.

**Trigger**: always_on — Apply at all times during the implementation phase.

## 1. Standards

### Principles

- **[REQ-SEC-01] Zero Trust Input**
  - All external input (HTTP, CLI, Files) MUST be assumed malicious until validated against an allow-list.
- **[REQ-SEC-02] Least Privilege Access**
  - Components and services MUST operate with the minimum permissions necessary for their task.
- **[REQ-SEC-03] Secure Default State**
  - Security controls MUST fail to a "Deny" state by default. Access MUST only be granted via explicit opt-in.

### Vulnerability Mitigation

| Vulnerability | Mitigation Strategy | Priority |
| --- | --- | --- |
| Injection (SQL/Cmd) | Parameterization / No-Shell | Critical |
| XSS | Output Encoding | Critical |
| IDOR | Ownership Validation | Critical |
| SSRF | Domain Allow-listing | High |

### Must

- **[REQ-SEC-04] Parameterized Queries**
  - All database interactions MUST use prepared statements or parameterized queries to prevent SQLi.
- **[REQ-SEC-05] Context-Aware Encoding**
  - User-generated content MUST be encoded based on the output context (HTML, JS, URL) before rendering.
- **[REQ-SEC-06] Ownership Guarding**
  - Systems MUST verify that the authenticated user owns or has explicit permission for the requested resource ID.

### Must Not

- **[BAN-SEC-01] Hardcoded Secrets**
  - API keys, tokens, or credentials MUST NOT be stored in source code (use Environment Variables or Vaults).
- **[BAN-SEC-02] Direct DOM/Injection**
  - Logic MUST NOT insert untrusted strings directly into execution sinks like `innerHTML`, `eval()`, or `os.system()`.

### Failure Handling

- **Stop Condition**: Stop execution if a required authorization check is missing for a sensitive operation.

## 2. Procedures

- **[PROC-SEC-01] Input Sanitization**
  - IF receiving multi-line text input THEN MUST sanitize via an allow-list library (e.g., DOMPurify, Bleach).
- **[PROC-SEC-02] Secret Scanning**
  - Run automated secrets detection (e.g., gitleaks) on every commit to prevent credential leakage.

## 3. Examples

### Safe Query (Python)

```python
# Good: Using parameterization
cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
```

## 4. Validation Criteria

- **[VAL-SEC-01] SAST Verification**
  - [ ] Static analysis (SonarQube/Snyk) returns zero critical security vulnerabilities.
- **[VAL-SEC-02] Secret Audit**
  - [ ] No hardcoded strings matching private key or API token patterns are found in the repository.
- **[VAL-SEC-03] Auth Coverage**
  - [ ] Every API endpoint has a verified unit test for unauthorized access (401/403).
