---
trigger: always_on
glob: "**/*.{py,js,ts,go,java}"
description: "Security Authentication (OWASP A07): Password policies, MFA, and Session Management."
---
# Security Authentication Standards (OWASP A07)

## 1. Password Policy

- **Length**: Minimum 12 characters.
- **Complexity**: Require mixed case, numbers, and symbols (NIST guidelines suggest length is more important, but complexity prevents simple dictionary attacks).
- **Hashing**: NEVER store plain text. Use `Argon2id` (preferred), `Bcrypt`, or `PBKDF2`.

## 2. Multi-Factor Authentication (MFA)

- **Critical Actions**: Require MFA (TOTP, WebAuthn) for sensitive actions like changing passwords, changing email, or admin logins.
- **Recovery**: Provide secure recovery codes.

## 3. Session Management

- **Storage**: Use HTTP-only, Secure, SameSite cookies.
- **Rotation**: Rotate session IDs upon successful login to prevent Session Fixation.
- **Timeouts**: Implement absolute timeouts (e.g., 14 days) and idle timeouts (e.g., 30 mins).
- **Invalidation**: Invalidate all sessions on password change or remote logout.

## 4. Authentication Failures

- **Generic Messages**: Return generic error messages ("Invalid username or password") to prevent username enumeration.
- **Rate Limiting**: Implement strict rate limiting on login endpoints (e.g., 5 attempts per minute).

## 5. JWT Best Practices

- **Signing**: Use strong algorithms (EdDSA, RS256). Avoid `HS256` unless simple secret management is guaranteed.
- **Claims**: Include `exp` (expiration), `iat` (issued at), and `iss` (issuer).
- **Storage**: Do NOT store sensitivity tokens in LocalStorage (XSS vulnerable). Use Secure Cookies where possible, or short-lived tokens in memory.
