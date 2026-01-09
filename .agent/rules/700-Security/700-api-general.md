---
trigger: always_on
glob: "**/*.{js,ts,py,go,java,php}"
description: "API Core: RESTful Design, Versioning, Errors, and HTTP Methods."
---
# API General Standards

## 1. Resource Naming

- **Nouns**: Plural nouns for resources. No verbs in paths.
- **Kebab-case**: URI paths should be `kebab-case`.

### Example: Naming

**Good**

```text
GET /users/123/orders
```

**Bad**

```text
GET /getUsersOrders?id=123
```

## 2. HTTP Methods

- **GET**: Safe, Cacheable. Retrieve.
- **POST**: Create a new resource.
- **PUT**: Idempotent Full Replace.
- **PATCH**: Partial Update.
- **DELETE**: Idempotent Delete.

## 3. Versioning

- **URL Path**: `/api/v1/users` (Recommended for simplicity).
- **Header**: `Accept: application/vnd.myapi.v1+json` (Cleaner URL, harder to debug).
- **Breaking Changes**: Only bump version on backwards-incompatible changes.

### Example: Versioning

**Good**

```text
GET /api/v2/users
```

**Bad**

```text
GET /api/users?version=2 // Query param versioning is fragile
```

## 4. Error Responses

- **Format**: Structured JSON.
- **Codes**: Use standard HTTP codes (`400`, `401`, `403`, `404`, `429`, `500`).

## 5. Security Principles

- **HTTPS**: Enforce HTTPS for all traffic.
- **BOLA/IDOR**: Validation Authorization on EVERY endpoint accessing a resource by ID.
- **Rate Limiting**: Implement rate limiting (429 Too Many Requests) to prevent abuse.

### Example: Error

**Good**

```json
{
  "code": "INVALID_EMAIL",
  "message": "Email format is incorrect",
  "trace_id": "abc-123"
}
```

**Bad**

```json
"Error: Invalid Email"
```
