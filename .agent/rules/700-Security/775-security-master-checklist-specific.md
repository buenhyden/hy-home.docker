---
trigger: always_on
glob: "**/*"
description: "Security Master Checklist: A comprehensive 70-point security audit checklist covering Auth, Data, API, and Infrastructure."
---
# Security Master Checklist (Base Practices)

## 1. Authentication & Authorization

- [ ] **MFA**: Implement Multi-Factor Authentication.
- [ ] **OAuth**: Secure OAuth 2.0 / OIDC integration.
- [ ] **JWT**: Secure token handling (signature, expiration).
- [ ] **Session**: Secure session management (HttpOnly, Secure).
- [ ] **RBAC**: Enforce Role-Based Access Control.

## 2. Input Validation

- [ ] **Server-Side**: Validate all inputs on the server.
- [ ] **SQL**: Use parameterized queries (No SQLi).
- [ ] **XSS**: Escape output / Context-aware sanitization.
- [ ] **CSRF**: Implement Anti-CSRF tokens / SameSite cookies.
- [ ] **Command**: Prevent Command Injection (avoid `exec`).

## 3. Data Protection

- [ ] **Encryption**: Encrypt data at rest (AES-256) and transit (TLS 1.2+).
- [ ] **Keys**: Secure Key Management (HSM/KMS).
- [ ] **PII**: Minimize and protect Personally Identifiable Information.
- [ ] **Retention**: Enforce data retention and deletion policies.

## 4. API Security

- [ ] **Auth**: distinct API Authentication (Keys/Tokens).
- [ ] **Rate Limiting**: Throttling to prevent abuse.
- [ ] **Versioning**: Secure API lifecycle management.
- [ ] **CORS**: Restrictive Cross-Origin Resource Sharing.

## 5. Network & Infrastructure

- [ ] **HTTPS**: Enforce HTTPS everywhere (HSTS).
- [ ] **Firewall**: proper WAF and Network Firewall rules.
- [ ] **DDoS**: Mitigation strategies (CDN/Filtering).
- [ ] **Patching**: Regular security updates and patch management.
- [ ] **Headers**: Security Headers (CSP, X-Frame-Options, X-Content-Type).

## 6. Code & Development

- [ ] **SAST/DAST**: Static and Dynamic analysis in CI/CD.
- [ ] **Dependencies**: Scan for vulnerable packages (Snyk/Dependabot).
- [ ] **Secrets**: No hardcoded secrets (Use Vault/Env).
- [ ] **Logging**: Secure logging (no sensitive data).

## 7. Compliance & Testing

- [ ] **Standards**: OWASP Top 10, GDPR, SOC2 compliance.
- [ ] **PenTesting**: Regular penetration testing.
- [ ] **Incident Response**: Defined procedure for security breaches.
