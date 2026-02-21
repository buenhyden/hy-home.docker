---
trigger: model_decision
glob: ["**/*.ts", "**/*.go", "**/*.py"]
description: "API Standards: RESTfulness, URL naming, and Status Codes."
---

# 0910-Backend-API

- **Role**: API Designer
- **Purpose**: Ensure consistent, predictable, and standard API surfaces.
- **Activates When**: Designing or implementing API endpoints.

## 1. Standards

### 1.1 Principles

- **[REQ-API-GEN-01] RESTful**: Use HTTP verbs correctly (GET, POST, PUT, DELETE).
- **[REQ-API-GEN-02] Nouns**: URLs MUST represent resources (Nouns), not actions (Verbs).
- **[REQ-API-GEN-03] Versioning**: APIs MUST be versioned (URI or Header).

### 1.2 Scope

- **In-Scope**: HTTP APIs, OpenAPI/Swagger.
- **Out-of-Scope**: gRPC (separate standard).

### 1.3 Must / Must Not

- **[REQ-API-URL-01] Pluralization**: Use plural nouns (`/users` not `/user`).
- **[REQ-API-STA-01] Status Codes**:
  - 200: OK
  - 201: Created
  - 400: Bad Request
  - 401: Unauthorized (No Token)
  - 403: Forbidden (Bad Token)
  - 404: Not Found
  - 500: Server Error
- **[BAN-API-ACT-01] No Verbs in URL**: `/users/create` is BANNED. Use `POST /users`.

## 2. Procedures

### 2.1 Endpoint Design

1. **Resource**: Identify the noun (e.g., Order).
2. **Collection**: `GET /orders`, `POST /orders`.
3. **Item**: `GET /orders/:id`.
4. **Sub-resource**: `GET /orders/:id/items`.

## 3. Examples

### 3.1 RESTful Patterns

| Action | URL | Method |
| :--- | :--- | :--- |
| Read List | `/api/v1/users` | GET |
| Read One | `/api/v1/users/:id` | GET |
| Create | `/api/v1/users` | POST |
| Update | `/api/v1/users/:id` | PATCH |
| Delete | `/api/v1/users/:id` | DELETE |

## 4. Validation Criteria

- [ ] **[VAL-API-URL-01]** URLs are lowercase and kebab-case.
- [ ] **[VAL-API-VER-01]** Versioning is present.

## 5. References

- Related: [0900-backend-standard.md](./0900-backend-standard.md)
