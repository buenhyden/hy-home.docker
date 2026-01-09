---
description: Standard workflow for API design and implementation
---

# API Design Workflow

Based on `700-api-general.md` and `701-api-rest-implementation-specific.md`.

1. **Resource Naming**
   - Use plural nouns (`/users`, `/orders`).
   - Use kebab-case for paths.

2. **HTTP Methods**
   - GET: Retrieve
   - POST: Create
   - PUT: Full Replace
   - PATCH: Partial Update
   - DELETE: Remove

3. **Versioning**
   - URL path: `/api/v1/users`

4. **Error Response**

   ```json
   {
     "code": "VALIDATION_ERROR",
     "message": "Email format is invalid",
     "trace_id": "abc-123"
   }
   ```

5. **Pagination**
   - Cursor-based preferred for large datasets.
   - Envelope: `{ "data": [...], "meta": { "next_cursor": "..." } }`
