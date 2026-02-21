---
trigger: model_decision
glob: ["**/*"]
description: "Security Pillar Standard: Enforces OWASP Top 10, Auth/Authz, Data Protection, and Infrastructure Security."
---
# Security Pillar Standard

## Activation
- [ ] Apply when Writing authentication logic, handling sensitive data, or configuring infrastructure..
- [ ] Apply when editing files matching: `**/*`.

## Rules
- **Role**: Security Engineer
- **Purpose**: Enforce defense-in-depth across the entire stack using OWASP patterns.
- **Activates When**: Writing authentication logic, handling sensitive data, or configuring infrastructure.

**Trigger**: model_decision — Apply when handling security.

---

### 1. Standards

### 1.1 Authentication & Identity (OWASP A07)
- **[REQ-SEC-AUTH-01] Passwords**: MUST use `Argon2` or `Bcrypt`. Length >= 12 chars.
- **[REQ-SEC-AUTH-02] MFA**: Critical actions MUST require MFA (TOTP/WebAuthn).
- **[REQ-SEC-AUTH-03] Session**: Cookies MUST be `HttpOnly`, `Secure`, `SameSite=Strict`.

### 1.2 Access Control (OWASP A01)
- **[REQ-SEC-ACC-01] IDOR**: ALL resource access requests MUST verify that `current_user` owns the resource ID.
- **[REQ-SEC-ACC-02] RBAC**: Authorization logic EXPLICITLY separate from business logic (Middleware/Decorators).

### 1.3 Data Protection (OWASP A03)
- **[REQ-SEC-DATA-01] PII**: Personally Identifiable Information MUST be encrypted at rest (AES-256).
- **[REQ-SEC-DATA-02] Secrets**: Secrets/Keys MUST NEVER be committed to Git. Use Secret Managers (Vault/AWS SM).

### 1.4 Injection Prevention (OWASP A03)
- **[REQ-SEC-INJ-01] SQL**: Parameterized queries are MANDATORY.
- **[REQ-SEC-INJ-02] XSS**: Outputs MUST be contextually encoded. `innerHTML` is FORBIDDEN.

---

### 2. Procedures

### 2.1 Dependencies Protocol
1. **Audit**: Run `npm audit` / `pip-audit` in CI.
2. **Lock**: Commit lockfiles (`package-lock.json`, `poetry.lock`).
3. **Pin**: Avoid loose version ranges (`^1.2.3`).

### 2.2 Security Reviews
1. **Threat Model**: Identify trust boundaries.
2. **Scan**: Static Analysis (SAST) via SonarQube/Semgrep.
3. **PenTest**: Dynamic Analysis (DAST) on staging.

---

### 3. Examples

### 3.1 Secure Endpoint (FastAPI)
```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, user: User = Depends(get_current_user)):
    item = db.get_item(item_id)
    if item.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return item
```

---

### 4. Validation Criteria
- [ ] Are secrets excluded from Git?
- [ ] Is IDOR checked on every ID access?
- [ ] Are SQL queries parameterized?

## References
- None.
