---
title: "[API Name / Feature] API Specification"
status: "Draft | Proposed | Approved | Deprecated"
version: "v1.x.x"
base_url: "https://api.example.com/v1"
prd_reference: "[Link to PRD]"
spec_reference: "[Link to Tech Spec]"
adr_reference: "[Link to ADR]"
tags: ["api", "contract", "specification"]
---

# API Specification Template ([API Name / Feature])

> **Status**: Draft / Proposed / Approved / Deprecated
> **Version**: v1.x.x
> **Base URL**: `https://api.example.com/v1`
> **Related PRD**: [Link to PRD]
> **Related Technical Spec**: [Link to Tech Spec]
> **Related ADR**: [Link to ADR]

> **Purpose**: Define the exact contract, data models, and security requirements for an API feature before implementation begins. This document must be approved by human developers before Coder Agents execute it.

---

## 0. Canonical Location & Artifacts

This API contract MUST be stored under `specs/<feature>/api/` (contract-first). Generated outputs MAY live under `specs/<feature>/api/generated/`, but the source contract MUST be human-reviewed.

### 0.1 Recommended Structure

```text
specs/<feature>/api/
  <feature>-api.md        # The main specification document (this template)
  openapi.yaml            # OR schema.proto OR schema.graphql
  changelog.md            # Keep a Changelog format
  generated/              # Optional, generated outputs only
```

### 0.2 Allowed Contract Formats

- OpenAPI 3.x (YAML or JSON) for REST APIs.
- GraphQL SDL for GraphQL APIs.
- Protobuf (`.proto`) for gRPC APIs.

### 0.3 Versioning & Breaking Changes

- API contracts MUST be versioned (recommended: URL path prefix like `/v1/`).
- Breaking changes MUST NOT be made within an existing major version. Breaking changes MUST be released as a new major version (e.g., `/v2/`) or via an explicitly documented and approved version negotiation strategy.

### 0.4 Changelog

Each API contract MUST include `specs/<feature>/api/changelog.md` using Keep a Changelog sections:

- Added
- Changed
- Deprecated
- Removed
- Fixed
- Security

### 0.5 Governance

- Contract-first governance: `.agent/rules/2000-API_Governance/2000-api-governance.md`
- API design standards: `.agent/rules/0000-Agents/0010-api-design-standard.md`

### 0.6 API Governance Checklist (Fill Before Design)

> This document follows the **API Governance Pillar (2000)**. Ensure all endpoints
> adhere to RESTful/GraphQL standards and versioning policies.

| Item           | Check Question                              | Required | Alignment Notes |
| -------------- | ------------------------------------------- | -------- | --------------- |
| Protocol       | REST / GraphQL / gRPC / Webhook?            | Must     |                 |
| Versioning     | Is the major version in the URL or Header?  | Must     |                 |
| Auth           | Is AuthN/AuthZ scheme defined (JWT/Scopes)? | Must     |                 |
| Validation     | Are all inputs validated via Zod/Pydantic?  | Must     |                 |
| Error Handling | Standardized JSON error schema used?        | Must     |                 |
| Rate Limiting  | Are quotas/throttling defined?              | Must     |                 |
| Documentation  | Is OpenAPI/Swagger generated from this?     | Must     |                 |

---

## 1. Overview & Use Cases

**Objective**: Briefly describe the problem this API solves and its primary consumers (e.g., Web Client, Mobile App, 3rd Party Integration).

**Use Cases**:

- UC1: User can retrieve a list of widgets with pagination.
- UC2: User can create a new widget.

---

## 2. Resource Definitions

**Resource Models**: Define the core domain entities used in this API using JSON schema or simple tables.

*Example: Widget Resource*

```json
{
  "id": "uuid",
  "name": "string",
  "status": "enum(active, archived)",
  "created_at": "timestamp"
}
```

---

## 3. Endpoints Contract

Define all endpoints using RESTful plural nouns (no verbs in paths). Be sure to include explicit validation rules (e.g., via Zod, Pydantic, or JSON Schema) for all inputs.

### 3.1. `[METHOD] /v1/[resource]`

**Description**: What does this endpoint do?

**Request**:

- **Headers**:
  - `Authorization: Bearer <token>`
- **Query Parameters**:
  - `limit` (int, default 20)
  - `cursor` (string, optional)
- **Body**: (If applicable. Specify schema constraints like min-length, enums.)

**Response**:

- **Success (200 OK)**:

```json
{
  "data": [...],
  "meta": { "next_cursor": "abc" }
}
```

---

## 4. Webhooks & Events (Optional)

Define asynchronous event payloads or webhook triggers from this service.

- **Trigger**: [Event Name, e.g., `widget.created`]
- **Payload Schema**: [Define the JSON payload structure]
- **Security**: [e.g., HMAC Signature Verification via `X-Signature` header]

---

## 5. Authentication & Security

- **Auth Method**: OAuth2 / JWT / API Key
- **Required Scopes/Roles**: e.g., `widget:read`, `widget:write`

---

## 6. Non-Functional Requirements (NFRs)

- **Latency**: e.g., < 200ms (p95)
- **Rate Limit**: e.g., 100 requests / minute per user
- **Idempotency**: e.g., `X-Idempotency-Key` header required for `POST/PUT` operations

---

## 7. Error Handling

Define known failure states and their corresponding standard HTTP status codes.

- **400 Bad Request**: Validation failure (e.g., missing required field).
- **401 Unauthorized**: Missing or invalid token.
- **403 Forbidden**: Valid token, but lacks required role.
- **404 Not Found**: Target resource ID does not exist.
- **429 Too Many Requests**: Rate limit exceeded.

**Standard Error Schema**:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The name field is required."
  }
}
```

---

## 8. Versioning Strategy

- **API Version**: (e.g., v1)
- **Breaking Change Policy**: State how changes will be handled (e.g., major version bump in URL `/v2/` or via Accept headers).
