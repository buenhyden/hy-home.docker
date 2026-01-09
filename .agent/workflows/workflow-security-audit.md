---
description: Standard workflow for security auditing
---

# Security Audit Workflow

Based on `775-security-master-checklist-specific.md` and `780-security-secrets-specific.md`.

1. **Secret Scanning**
   - Check for hardcoded keys (AWS, Stripe, Private Keys).
   - Check `.env` handling.

2. **Dependency Audit**
   - Run `npm audit` or `pip-audit`.
   - Check lockfiles.

3. **Code Analysis**
   - **Injection**: Check SQL concatenation, `eval()`, `os.system()`.
   - **Auth**: Verify `login_required` or equivalent on protected routes.
   - **Data**: Verify PII masking in logs.

4. **Configuration Check**
   - `DEBUG=False`?
   - HTTPS enforced?

5. **Report**
   - Document findings with Severity (S1-S5).
