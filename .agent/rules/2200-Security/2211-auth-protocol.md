---
trigger: always_on
glob: ["**/*.{env,yaml,json,js,ts}", "**/auth/**"]
description: "Authentication Protocol Security: Enforces secure secret management, MFA, and least-privilege identity access."
---

# Auth Protocol Security Standards

- **Role**: Security Architect
- **Purpose**: Define standards for implementing secure authentication and authorization protocols while mitigating credential exposure risks.
- **Activates When**: Modifying authentication logic, configuring secret management, or designing identity access management (IAM) roles.

**Trigger**: always_on — Apply during the implementation of authentication and authorization components.

## 1. Standards

### Principles

- **[REQ-AUTH-01] Externalized Secret Management**
  - Credentials (API keys, secrets, tokens) MUST NOT be hardcoded. Use OS environment variables or a dedicated Secret Vault.
- **[REQ-AUTH-02] Least-Privilege Identity (PoLP)**
  - Users and services MUST be granted the minimum permissions required to perform their tasks using Role-Based Access Control (RBAC).
- **[REQ-AUTH-03] Secure Session Persistence**
  - Authentication tokens (JWT, Cookies) MUST be transmitted via encrypted channels and utilize secure flags (`HttpOnly`, `Secure`, `SameSite=Strict`).

### Protocols & Mechanisms

| Mechanism | Requirement ID | Standard Recommendation |
| --- | --- | --- |
| Secret Storage | [REQ-AUTH-04] | .env / AWS Secrets / HashiCorp Vault |
| Auth Protocol | [REQ-AUTH-05] | OAuth2 / OIDC |
| Password Hash | [REQ-AUTH-06] | Argon2 / Bcrypt (Cost >= 10) |
| Multi-Factor | [REQ-AUTH-07] | TOTP / FIDO2 / Passkeys |

### Must

- **[REQ-AUTH-08] Mandatory Correlation (Audit)**
  - Every authentication event (Success/Failure) MUST be logged with sufficient metadata (TraceID, IP, Timestamp) for security auditing.
- **[REQ-AUTH-09] Session Rotation**
  - Authenticated sessions MUST be rotated upon login and provide a mechanism for global sign-out (revocation).
- **[REQ-AUTH-10] .gitignore Secret Guard**
  - Configuration files containing secrets (e.g., `.env`) MUST be explicitly listed in `.gitignore` to prevent accidental commits.

### Must Not

- **[BAN-AUTH-01] Plain-Text PII Storage**
  - Do NOT store passwords or PII in plain text; use cryptographically strong hashing and salting primitives.
- **[BAN-AUTH-02] Client-Side Permission Control**
  - Authorization checks MUST NEVER be performed exclusively on the client; the server MUST validate every privileged request.

### Failure Handling

- **Stop Condition**: Stop feature execution if a hardcoded secret is identified in the source code or if a session cookie is missing the `HttpOnly` flag.

## 2. Procedures

- **[PROC-AUTH-01] Secret Audit**
  - IF committing code THEN MUST run a secret scanner (e.g., Gitleaks) to detect accidentally exposed credentials.
- **[PROC-AUTH-02] Privilege Review**
  - Conduct a quarterly review of defined RBAC roles to ensure they still adhere to the principle of least privilege.

## 3. Examples

### Secure Auth Pattern (Good)

```javascript
// Securely accessing secret via environment
const apiKey = process.env.PAYMENT_GATEWAY_KEY;
if (!apiKey) throw new AuthError("Configuration missing");
```

## 4. Validation Criteria

- **[VAL-AUTH-01] Gitleaks Pass**
  - [ ] Automated scans of the repository history confirm zero committed secrets or tokens.
- **[VAL-AUTH-02] JWT Integrity**
  - [ ] Verification confirms that tokens are signed using strong algorithms (e.g., RS256) and contain valid expirations.
- **[VAL-AUTH-03] Cookie Flag Verification**
  - [ ] Web audit confirms that 100% of authentication cookies utilize the `Secure` and `HttpOnly` flags.
