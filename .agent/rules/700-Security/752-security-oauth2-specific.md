---
trigger: always_on
glob: "**/*"
description: "OAuth2 / OIDC: Flows, Scopes, and Token Management."
---
# OAuth2 & OIDC Standards

## 1. Flows

- **PKCE**: Mandatory for Public Clients (Mobile, SPA).
- **Client Credentials**: Only for Service-to-Service.
- **Deprecated**: NEVER use Implicit Flow.

### Example: Flow

**Good (SPA)**

```text
Authorization Code Flow + PKCE
```

**Bad**

```text
Implicit Flow (Deprecated, insecure)
```

## 2. Scopes (Least Privilege)

- **Granularity**: Request ONLY the scopes needed. `read:user` not `*`.
- **Consent**: Users must understand what they grant.

### Example: Scopes

**Good**

```text
scope: openid profile email read:orders
```

**Bad**

```text
scope: * // Full access, unnecessary risk
```

## 3. Tokens

- **Validation**: Validate `aud` (Audience) and `iss` (Issuer) claims.
- **Storage**: Do NOT store Refresh Tokens in `localStorage`. Use HTTPOnly Cookies.
- **Expiry**: Short-lived Access Tokens (15m). Rotate Refresh Tokens on use.

### Example: Validation

**Good**

```python
jwt.decode(token, algorithms=["RS256"], audience="my-api", issuer="auth0.com")
```

**Bad**

```python
jwt.decode(token, options={"verify_signature": False}) // Accepting any token
```
