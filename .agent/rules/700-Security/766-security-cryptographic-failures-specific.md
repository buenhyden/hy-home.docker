---
trigger: always_on
glob: "**/*.{py,js,ts,go,java}"
description: "Security Cryptography (OWASP A02): Strong hashing, secrets management, and TLS."
---
# Security Cryptography Standards (OWASP A02)

## 1. Algorithms

- **Forbidden**: `MD5`, `SHA1`, `DES`, `RC4`.
- **Recommended**:
  - **Hashing**: `SHA-256` or `SHA-512`.
  - **Passwords**: `Argon2` (preferred), `Bcrypt`, or `PBKDF2`.
  - **Encryption**: `AES-256-GCM`.

## 2. Secrets Management

- **Storage**: NEVER hardcode secrets in source code. Use environment variables or a secrets manager (Vault, AWS Secrets Manager).
- **Detection**: Use tools like `trufflehog` or `git-secrets` to scan for accidental commits.

## 3. Randomness

- **CSPRNG**: Use Cryptographically Secure Pseudo-Random Number Generators.
  - **Python**: `secrets` module (NOT `random`).
  - **Node.js**: `crypto.randomBytes` (NOT `Math.random`).

## 4. Data in Transit

- **TLS**: Enforce TLS 1.2 or 1.3. Disable older protocols (SSLv3, TLS 1.0/1.1).
- **Certificates**: ALWAYS validate SSL certificates in production (`verify=True`).

### Example: Secure Password Hashing

#### Python (Bcrypt)

```python
import bcrypt
# Hash
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# Check
if bcrypt.checkpw(password.encode(), hashed):
    pass
```

#### Node.js (Bcrypt)

```javascript
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(password, 10);
const match = await bcrypt.compare(password, hash);
```
