---
trigger: always_on
glob: "**/*"
description: "Security Core: OWASP Top 10, Zero Trust, Rate Limiting, and Auditing."
---
# Security General Standards

## 1. Zero Trust Architecture

- **Identity First**: Validate identity on *every* request (mTLS or JWT).
- **Least Privilege**: Grant only permissions necessary. No wildcard (`*`) IAM.
- **Network**: Assume hostile. TLS 1.2+ for all traffic.

## 2. OWASP Top 10 Defenses

- **Injection**: Parameterized queries for SQL. Avoid shell execution.
- **Broken Access Control**: Deny by default. Check ownership in controllers.
- **Cryptographic Failures**: Use `bcrypt`/`argon2` for passwords.

### Example: Hashing

**Good**

```python
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

**Bad**

```python
hash = hashlib.sha256(password.encode()).hexdigest() // Unsafe for passwords
```

## 3. Rate Limiting

- **Global**: Protect all public endpoints from brute-force/DDoS.
- **User-Specific**: Stricter limits for sensitive endpoints (login, password reset).
- **Headers**: Return `X-RateLimit-Remaining` and `Retry-After`.

### Example: Rate Limit

**Good**

```text
429 Too Many Requests
Retry-After: 60
```

## 4. Data Protection

- **Encryption at Rest**: Enable volume encryption (EBS/S3/RDS).
- **Secrets Management**: Use Vault, AWS Secrets Manager, Doppler.
- **Masking**: Redact PII in all logs.

## 5. Supply Chain

- **Scanning**: Run `npm audit`, `pip-audit`, or `trivy` in CI.
- **Pinning**: Verify checksums of all dependencies.
