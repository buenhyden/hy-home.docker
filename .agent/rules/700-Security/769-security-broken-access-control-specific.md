---
trigger: always_on
glob: "**/*.{py,js,ts,java,go}"
description: "Security Access Control (OWASP A01): Prevent IDOR, enforce role checks, and secure routes."
---
# Security Access Control Standards (OWASP A01)

## 1. Principle of Least Privilege

- **Default Deny**: All endpoints/resources MUST deny access by default unless explicitly allowed.
- **Roles**: Use Role-Based Access Control (RBAC) or Attribute-Based Access Control (ABAC).
- **Hardcoding**: NEVER hardcode role checks like `if user.role == 'admin':`. Use a centralized permission system/decorator.

## 2. Insecure Direct Object References (IDOR)

- **Owner Check**: ALWAYS verify that the `current_user` owns the resource ID being accessed.
- **UUIDs**: Prefer UUIDs over sequential integer IDs to prevent enumeration.

## 3. Framework Specifics

### Python (Django/Flask/FastAPI)

- **Django**: Use `@login_required` and `UserPassesTestMixin`.
- **Flask**: Use `@login_required` and `current_user.id` checks.
- **FastAPI**: Use command `Depends(get_current_user)` for every protected route.

### JavaScript (Express/Node)

- **Middleware**: Use authentication middleware (e.g., `passport.authenticate`, custom generic auth middleware) on ALL protected routes.
- **Route Protection**:

  ```javascript
  // Bad:
  app.get('/admin', (req, res) => { ... });
  
  // Good:
  app.get('/admin', requireAdmin, (req, res) => { ... });
  ```

## 4. Testing Access Control

- **Vertical**: Test that a lower privilege user cannot access higher privilege resources.
- **Horizontal**: Test that User A cannot access User B's private resources (IDOR).
- **Unauthenticated**: Test that anonymous users are rejected.
