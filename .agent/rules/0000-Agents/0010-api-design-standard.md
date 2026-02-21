---
trigger: model_decision
glob: ["**/*"]
description: "API Design Agent Standards: Enforces REST/GraphQL best practices, resource-oriented modeling, and breaking-change governance."
---

# API Design Agent Standards

- **Role**: REST & GraphQL Architect
- **Purpose**: Define standards for the creation, evolution, and documentation of intuitive, secure, and scalable API interfaces through resource-oriented design.
- **Template**: `templates/engineering/api-spec-template.md` (or OpenAPI JSON schema)
- **Directory**: `specs/<feature>/api/` (for both planning and generated reference files)
- **Activates When**: The user requests endpoint design, schema modeling (SQL/NoSQL/GraphQL), or API contract reviews.

**Trigger**: model_decision — Apply during all API design, documentation (OpenAPI), and integration phases.

## 1. Standards

### Principles

- **[REQ-API-00] Repository Workspace Separation**
  - When backend and frontend co-exist in a single repository, the API server implementation MUST be isolated within the `server/` root directory, independent from `web/` or `app/` clients.
- **[REQ-API-01] Strict Resource-Oriented Modeling**
  - API paths MUST use plural nouns to represent resources (e.g., `/users`, `/orders`). Verbs (e.g., `/getUsers`) are STRICTLY PROHIBITED in RESTful paths.
- **[REQ-API-11] Template Fidelity**
  - All new API specifications MUST follow the structure defined in `templates/engineering/api-spec-template.md` or a standard OpenAPI JSON/YAML definition.
- **[REQ-API-12] Cross-Document Traceability**
  - API Specs MUST link to their parent PRD (`docs/prd/`) and related Technical Spec (`specs/`).
- **[REQ-API-02] Immutable Versioning Discipline**
  - All public APIs MUST transition via explicit versioning (URL path `/v1/` or semantic Headers) to prevent silent breaking of client contracts.
- **[REQ-API-03] Normalized Error Response Schema**
  - API responses MUST utilize consistent HTTP status codes (2xx, 4xx, 5xx) and return a machine-readable error payload defining the failure cause.

### Architectural Matrix

| Category   | Requirement ID | Mandatory Standard                        |
| ---------- | -------------- | ----------------------------------------- |
| Transport  | [REQ-API-04]   | HTTPS 1.2+ mandatory for all endpoints    |
| Pagination | [REQ-API-05]   | Consistent Cursor or Skip/Limit for lists |
| Modeling   | [REQ-API-06]   | OpenAPI (REST) or SDL (GraphQL)           |
| Security   | [REQ-API-07]   | RBAC/Scopes enforced at the gateway level |

### Must

- **[REQ-API-08] Explicit Breaking-Change Lifecycle**
  - Any modification to a successful contract MUST be treated as a breaking change requiring a major version bump or a temporary feature flag.
- **[REQ-API-09] Mandatory Documentation Generation**
  - Every API feature MUST be accompanied by an updated OpenAPI specification or technical contract document.
- **[REQ-API-10] Defensive Input Validation (IDP)**
  - All endpoints MUST implement strict input validation (e.g., JSON Schema, Pydantic) to prevent injection and payload corruption.

### Must Not

- **[BAN-API-01] Over-Fetching Leakage**
  - DO NOT return sensitive data (e.g., hashed passwords, internal metadata) in public API responses. Utilize DTOs (Data Transfer Objects).
- **[BAN-API-02] Deep Resource Nesting**
  - Avoid nesting resources more than two levels deep (e.g., `/users/{id}/orders/{id}`). Prefer flat resource paths with filtering.

### Failure Handling

- **Stop Condition**: Stop API design if the proposed contract violates the project's security baseline (e.g., missing Auth) or introduces a naming collision.

## 2. Procedures

- **[PROC-API-01] Contract Verification Flow**
  - IF creating a new endpoint THEN MUST verify the path naming and response shape against the existing project API guidelines before implementation.
- **[PROC-API-02] Version Promotion Plan**
  - Upon releasing a new major version, MUST document a migration path and deprecation timeline for the previous version.

## 3. Examples

### compliant REST Paths (Good)

```text
GET    /v1/orders      - List orders
POST   /v1/orders      - Create order
PATCH  /v1/orders/{id} - Update order
```

## 4. Validation Criteria

- **[VAL-API-01] OpenAPI Scorecard**
  - [ ] audit confirms that the OpenAPI spec accurately reflects 100% of the active endpoint behavior.
- **[VAL-API-02] Naming Consistency**
  - [ ] build check confirms that zero endpoint paths utilize verbs or case-inconsistent resource names.
- **[VAL-API-03] PII Leakage Pass**
  - [ ] Security scan confirms that no sensitive fields are exposed in the JSON response payloads.
