---
trigger: always_on
glob: "**/*"
description: "Secret Detection Standards: Preventing credential leaks and secure management."
---
# Secret Detection Standards

## 1. Prevention

- **Hardcoding**: NEVER hardcode API keys, tokens, or passwords.
- **Environment**: Use `.env` files (gitignored) and `os.environ`/`process.env`.
- **Detectors**: Use pre-commit hooks (git-secrets) to catch leaks early.

## 2. Detection Patterns (Regex)

Monitor codebases for these high-risk patterns:

- **AWS**: `(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}`
- **Stripe**: `(sk|pk)_(test|live)_[0-9a-zA-Z]{24,}`
- **Private Keys**: `-----BEGIN ((EC|PGP|DSA|RSA|OPENSSH) )?PRIVATE KEY-----`
- **Generic**: Assignments to `password`, `secret`, `token` with high entropy.

## 3. Remediation

1. **Revoke** immediately.
2. **Rotate** credentials.
3. **Squash/Rewrite** history (BFG) if critical.

## 4. Common Patterns to Avoid

- **AWS/Cloud Keys**: `AKIA...`
- **Private Keys**: `-----BEGIN PRIVATE KEY-----`
- **DB Strings**: `postgres://user:pass@host`

### Example: Secure Config

#### Good (Config)

```python
import os
api_key = os.environ.get("API_KEY")
```

#### Bad (Config)

```python
api_key = "sk_live_1234567890"
```
