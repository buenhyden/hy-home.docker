---
trigger: always_on
glob: "**/*.{js,ts,py}"
description: "Advanced Security Patterns: Auth Implementation, Input Validation, and XSS/CSRF Prevention."
---
# Advanced Security Implementation Patterns

## 1. Authentication Implementation

- **Hashing**: Use `bcrypt` or Argon2. Never MD5/SHA1.
- **JWT**: Rotate refresh tokens. Use short-lived access tokens (e.g., 15m).
- **MFA**: Implement TOTP (Speakeasy/PyOTP) for critical systems.
- **Lockout**: Implement exponential backoff or account lockout after failed attempts.

## 2. Input Validation (Sanitization)

- **Sanitization**: Use libraries like `DOMPurify` (JS) or `bleach` (Python) to strip dangerous HTML.
- **Validation**: Strict allow-list validation for all inputs (Email, URL, UUID).
- **NoSQL Injection**: Sanitize MongoDB queries (remove `$` operators from user input).

### Example: Input Sanitization

#### Good (Sanitization)

```javascript
const clean = DOMPurify.sanitize(dirtyInput, { ALLOWED_TAGS: ['b', 'i'] });
```

## 3. Transport & Headers

- **Helmet**: Use `helmet()` in Express/Node to set secure headers (HSTS, X-Frame-Options).
- **CSP**: Define a strict Content Security Policy. Avoid `'unsafe-inline'`.

## 4. File Uploads

- **Validation**: Check Magic Bytes (File Signature), NOT just extensions.
- **Storage**: Store uploads outside the web root. Rename files randomly.
- **Scanning**: Malware scan uploads if possible.
