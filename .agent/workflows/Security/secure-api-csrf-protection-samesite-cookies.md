---
description: Prevent CSRF attacks
---

1. **Use SameSite Cookies**:

   ```ts
   response.headers.set('Set-Cookie', 'token=abc; SameSite=Strict; HttpOnly');
   ```

2. **Implement CSRF Tokens**:

   ```ts
   import { randomBytes } from 'crypto';
   export function generateCSRFToken() {
     return randomBytes(32).toString('hex');
   }
   ```

3. **Validate Origin**:

   ```ts
   const origin = request.headers.get('origin');
   if (!allowedOrigins.includes(origin)) {
     return Response.json({ error: 'Invalid origin' }, { status: 403 });
   }
   ```

4. **Pro Tips**:
   - Never use `*` in production.
   - Validate both token and origin.
