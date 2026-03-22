---
title: '[API Name / Feature] API Specification'
status: 'Draft | Proposed | Approved | Deprecated'
version: 'v1.x.x'
openapi_version: '3.1.0'
base_url: 'https://api.example.com/v1'
prd_reference: '[Link to PRD]'
spec_reference: '[Link to Tech Spec]'
adr_reference: '[Link to ADR]'
tags: ['api', 'contract', 'specification']
layer: '<layer>'
---

# API Specification Template ([API Name / Feature])

> **Status**: [Draft | Proposed | Approved | Deprecated]
> **Version**: v1.x.x (OpenAPI 3.1.0)
> **Base URL**: `https://api.example.com/v1`
> **Related PRD**: [Link to PRD]
> **Related Technical Spec**: [Link to Tech Spec]
> **Related ADR**: [Link to ADR]

**Overview (KR):** [API의 목적, 해결하려는 문제, 그리고 주요 소비층(Web, Mobile 등)을 한국어로 1-2문장 요약하세요.]

---

## 0. Canonical Location & Artifacts

This API contract MUST be stored under `docs/api/<feature>/` (contract-first).

### 0.1 Recommended Structure

```text
docs/api/<feature>/
  README.md        # The main specification document (this template)
  openapi.yaml     # The formal OpenAPI 3.1 definition
  changelog.md     # Keep a Changelog format
```

### 0.2 Versioning & Breaking Changes

- API versions MUST be explicitly defined in the URL (e.g., `/v1/`) or via headers.
- Breaking changes require a major version bump.

### 0.3 API Governance Checklist

| Item           | Check Question                               | Required | Alignment Notes |
| -------------- | -------------------------------------------- | -------- | --------------- |
| Protocol       | REST / GraphQL / gRPC / Webhook?             | Must     |                 |
| Versioning     | Major version in URL or Header?              | Must     |                 |
| Auth           | AuthN/AuthZ scheme defined in components?    | Must     |                 |
| Validation     | All inputs validated via JSON Schema / Zod?  | Must     |                 |
| Error Handling | Standardized JSON error response used?       | Must     |                 |
| Rate Limiting  | Quotas and headers (`X-RateLimit-*`) defined?| Must     |                 |
| Examples       | Are examples provided for ALL responses?     | Must     |                 |

---

## 1. Overview & Use Cases

**Objective**: Briefly describe the problem this API solves.

**Primary Consumers**: [Web Client | Mobile App | Internal Service | 3rd Party]

**Use Cases**:

- **UC1**: [e.g., User can retrieve a list of widgets with cursor-based pagination]
- **UC2**: [e.g., User can create a new widget with validation]

---

## 2. API Tags & Grouping

Define tags used to organize the API endpoints.

| Tag         | Description                                   |
| ----------- | --------------------------------------------- |
| `Widgets`   | Operations related to widget management       |
| `Automations`| Operations related to background tasks        |

---

## 3. Data Models (Components/Schemas)

Define core domain entities. Use JSON Schema (2020-12) or structured tables.

### 3.1. `Widget` Model

| Property     | Type      | Required | Description                     | Example                |
| ------------ | --------- | -------- | ------------------------------- | ---------------------- |
| `id`         | `uuid`    | Yes      | Unique identifier               | `550e8400-e29b-...`    |
| `name`       | `string`  | Yes      | Name of the widget (min: 3)     | `Alpha Widget`         |
| `status`     | `enum`    | Yes      | `active`, `archived`            | `active`               |
| `created_at` | `iso8601` | Yes      | Timestamp in ISO format         | `2024-03-22T14:30:00Z` |

---

## 4. Endpoints Contract

### 4.1. `[METHOD] /v1/[resource]`

**Description**: [Detailed description of the endpoint's behavior]

**Tags**: `[Tag Name]`

**Request**:

- **Authentication**: `BearerAuth` (Mandatory)
- **Content-Type**: `application/json`
- **Headers**:
  - `Idempotency-Key` (Optional, UUID)
- **Query Parameters**:
  - `limit` (Integer, default: 20, max: 100)
  - `cursor` (String, Optional)
- **Body Schema**: (Reference model or define inline)

  ```json
  {
    "name": "string",
    "metadata": "object"
  }
  ```

**Responses**:

- **200 OK / 201 Created**:

  ```json
  {
    "data": { "id": "uuid", "name": "..." },
    "meta": { "timestamp": "..." }
  }
  ```
- **400 Bad Request**: Validation failure (provide specific error codes).
- **401 Unauthorized**: Missing or invalid credentials.
- **403 Forbidden**: Insufficient permissions (scopes).
- **429 Too Many Requests**: Rate limit exceeded.

---

## 5. Webhooks & Events (OpenAPI 3.1 Webhooks)

Define asynchronous event payloads.

- **Event Name**: `widget.updated`
- **Trigger**: Fired when a widget status changes.
- **Payload Schema**: Same as `Widget` model.
- **Security**: HMAC Signature (`X-Hub-Signature-256`)

---

## 6. Authentication & Security (Components)

### 6.1. Security Schemes

- **`BearerAuth`**: HTTP Bearer (JWT)
- **`ApiKeyAuth`**: `X-API-Key` Header

### 6.2. Scopes & Permissions

| Scope           | Description                                |
| --------------- | ------------------------------------------ |
| `widget:read`   | Permission to view widget details          |
| `widget:write`  | Permission to create/update widgets        |

---

## 7. Error Handling & Standard Responses

**Standard Error Schema**:

```json
{
  "error": {
    "code": "ERROR_CODE_STRING",
    "message": "Human readable message",
    "details": {}
  }
}
```

| Status | Code               | Description                            |
| ------ | ------------------ | -------------------------------------- |
| 400    | `VALIDATION_ERROR` | Request body or params failed check    |
| 404    | `NOT_FOUND`        | The requested resource was not found   |
| 409    | `CONFLICT`         | Resource state conflict (e.g. duplicate)|

---

## 8. Non-Functional Requirements (NFRs)

- **Latency**: P95 < [Value]ms
- **Availability**: [Value]% SLA
- **Rate Limit**: [Number] req/min per [ID Type]
- **Idempotency**: Supported for all non-GET requests via [Header Name].

---

## 9. References

- [Link to related ADR]
- [Link to External Documentation]
