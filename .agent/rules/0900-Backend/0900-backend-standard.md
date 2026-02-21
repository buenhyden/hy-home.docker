---
trigger: model_decision
glob: ["**/*.go", "**/*.py", "**/*.js", "**/*.ts", "**/services/**", "**/backend/**"]
description: "Backend General Standards: Enforces strict layering, stateless service design, and standardized API error contracts."
---

# Backend General Standards

- **Role**: Senior Backend Architect
- **Purpose**: Define standards for building robust, scalable, and maintainable server-side logic regardless of the specific implementation language or framework.
- **Activates When**: Writing backend services, designing business logic layers, or implementing data access repositories.

**Trigger**: model_decision — Apply during the design and implementation of any backend system component.

## 1. Standards

### Principles

- **[REQ-BE-00] Repository Workspace Separation**
  - Backend logic MUST be isolated within the `server/` root directory when developed alongside frontend codebases to prevent dependency entanglement.
  - **Backend Directory Blueprinting**: The internal structure of `server/` or `backend/` MUST dynamically adapt to the Architecture Style agreed upon in `ARCHITECTURE.md`:
    - **Monolithic**: Single `src/` directory with technical splits (e.g., `src/controllers/`, `src/services/`, `src/repositories/`).
    - **Modular Monolith**: Domain-based split within a single package (e.g., `src/modules/users/`, `src/modules/payments/`), where each module houses its own layered architecture.
    - **Microservices (MSA)**: Completely disjoint root server folders. `server/users-service/` and `server/payments-service/` MUST each contain their own dependency files (e.g., `package.json`, `go.mod`), Dockerfiles, and distinct databases.
- **[REQ-BE-01] Strict Separation of Layers**
  - Backend logic MUST follow a strict layering pattern: Controller (Entry) -> Service (Logic) -> Repository (Data). Cross-layer leaks are PROHIBITED.
- **[REQ-BE-02] Stateless Execution**
  - Backend services MUST remain stateless to support horizontal scaling. Session state MUST be persisted in external stores (e.g., Redis, DB).
- **[REQ-BE-03] Fail-Safe Input Validation**
  - All external inputs (Request bodies, parameters) MUST be validated at the entry boundary before being passed to the business logic layer.

### Architectural Baseline

| Layer | Requirement ID | Responsibility |
| --- | --- | --- |
| Controller | [REQ-BE-04] | Parsing, Validation, Response wrapping |
| Service | [REQ-BE-05] | Business rules, Transaction orchestration |
| Repository | [REQ-BE-06] | Data persistence, Query optimization |
| API Contract | [REQ-BE-07] | Standardized Error JSON structure |

### Must

- **[REQ-BE-08] Standardized Error Contracts**
  - All API errors MUST return a consistent JSON response including a machine-readable `code`, human-readable `message`, and a unique `trace_id`.
- **[REQ-BE-09] Explicit Authentication Defaults**
  - All endpoints MUST be "secure-by-default". Public access MUST be explicitly and intentionally declared via specific decorators or middleware.
- **[REQ-BE-10] Idempotent Mutations**
  - Write operations (POST/PUT/PATCH) SHOULD be designed as idempotent wherever possible to ensure safety during retries.

### Must Not

- **[BAN-BE-01] Global State Retention**
  - Do NOT use global variables or singleton state to store request-specific data; utilize request context or dependency injection.
- **[BAN-BE-02] Leaking Implementation Errors**
  - Internal system errors (e.g., DB stack traces) MUST NOT be exposed to the client; respond with opaque, summarized error messages.

### Failure Handling

- **Stop Condition**: Stop feature deployment if the service layer is identified as having direct dependencies on HTTP-specific objects (e.g., `Request`, `Response`).

## 2. Procedures

- **[PROC-BE-01] Complexity Threshold Audit**
  - IF a service method exceeds a complexity threshold THEN MUST refactor into sub-services or specialized strategy components.
- **[PROC-BE-02] Contract Sync**
  - Verify weekly that the internal data models accurately reflect the public API documentation (OpenAPI/Swagger).

## 3. Examples

### Standard Error Response (Good)

```json
{
  "error": {
    "code": "ENTITY_NOT_FOUND",
    "message": "User with ID 123 does not exist",
    "trace_id": "req-99f83a"
  }
}
```

## 4. Validation Criteria

- **[VAL-BE-01] Layer Isolation Check**
  - [ ] Audit confirms that Repository logic is exclusively accessed via the Service layer.
- **[VAL-BE-02] Error Consistency**
  - [ ] automated tests confirm that 100% of fail paths return the mandatory JSON error structure.
- **[VAL-BE-03] Stateless Verification**
  - [ ] Load tests with multiple instances confirm zero session-affinity or local state dependency issues.
