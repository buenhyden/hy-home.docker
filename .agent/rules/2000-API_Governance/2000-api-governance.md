---
trigger: model_decision
glob: ["**/*.{json,yaml,yml,proto,graphql}"]
description: "API Governance Pillar: Enforces Contract-First design, versioning, and semantic protocol standards for REST, GraphQL, and gRPC."
---

# API Governance Pillar

- **Role**: API Solutions Architect
- **Purpose**: Enforce technical and structural consistency across all internal and external API interfaces using contract-first methodology.
- **Activates When**: Designing new API schemas, changing endpoint signatures, or configuring service-to-service communication.

**Trigger**: model_decision — Apply during the architectural design of API interfaces.

## 1. Standards

### Principles

- **[REQ-API-01] Contract-First Design**
  - All API interfaces MUST have a formal specification (OpenAPI, Protobuf, or GraphQL) defined and approved BEFORE implementation begins.
  - Canonical contract location MUST be `specs/<feature>/api/` and the spec MUST follow `templates/engineering/api-spec-template.md`.
- **[REQ-API-02] Major Versioning**
  - Breaking changes (e.g., removing fields, changing types) MUST result in a major version increment (e.g., `/v1/` to `/v2/`).
- **[REQ-API-03] Protocol Atomicity**
  - Use appropriate semantic protocols for each use case: REST for resources, gRPC for high-performance RPC, and GraphQL for complex client-driven data graphs.

### Protocol Baseline

| Protocol | Specification | Use Case |
| --- | --- | --- |
| REST | OpenAPI 3.x | Public / External Integrations |
| gRPC | Protocol Buffers (v3) | Internal Microservices |
| GraphQL | SDL (Schema Definition) | Multi-Consumer Frontend |

### Must

- **[REQ-API-04] Semantic HTTP Verbs**
  - RESTful APIs MUST utilize appropriate HTTP verbs: `GET` (Read), `POST` (Create), `PUT` (Replace), `DELETE` (Remove).
- **[REQ-API-05] Standardized Status Codes**
  - Responses MUST include appropriate HTTP status codes: `200` (OK), `201` (Created), `400` (Bad Request), `401` (Unauthorized), `500` (Internal Error).
- **[REQ-API-06] Schema Validation**
  - All incoming API payloads MUST be validated against the formal schema (e.g., Zod, JSON Schema) at the application entry point.

### Must Not

- **[BAN-API-01] Silent Contract Mutations**
  - Field names or data types MUST NOT be modified within an existing major version without explicit consumer coordination.
- **[BAN-API-02] Verbose Error Payloads**
  - Production API errors MUST NOT leak internal implementation details, such as SQL queries or stack traces.

### Failure Handling

- **Stop Condition**: Stop deployment if the generated server stub fails to align with the provided OpenAPI or Proto specification.

## 2. Procedures

- **[PROC-API-01] Contract Review Workflow**
  - IF modifying an API signature THEN MUST obtain sign-off from at least one primary consumer of that interface.
- **[PROC-API-02] Automated Linting**
  - Every API specification MUST pass automated linting (e.g., Spectral) before being merged into the main branch.

## 3. Examples

### RESTful Resource (Good)

```http
GET /api/v1/users/123
Accept: application/json
```

## 4. Validation Criteria

- **[VAL-API-01] Spec Conformity**
  - [ ] Every active endpoint is accounted for in the corresponding OpenAPI/Proto file.
- **[VAL-API-02] Versioning Strategy**
  - [ ] Breaking changes are verified to be hosted on a new URI or via header negotiation.
- **[VAL-API-03] Validation Latency**
  - [ ] Request validation middleware consumes < 5ms of total request processing time.
