---
trigger: model_decision
glob: ["docs/technical/**/*.md", "specs/**/*.md"]
description: "Technical Documentation: Standards for APIs, Architecture decisions, and technical specifications."
---

# 0805-Documentation-Technical

- **Role**: Technical Writer / Architect
- **Purpose**: Enforce precision, accuracy, and completeness in technical specifications and API docs.
- **Activates When**: Documenting architecture, APIs, or complex algorithms.

## 1. Standards

### 1.1 Principles

- **[REQ-DOC-TEC-01] Precision**: Technical terms MUST be used correctly and consistently.
- **[REQ-DOC-TEC-02] Completeness**: API docs MUST cover inputs, outputs, errors, and auth.
- **[REQ-DOC-TEC-03] Currency**: Technical docs MUST reflect the current codebase state.

### 1.2 Scope

- **In-Scope**: API References, Architecture Decision Records (ADR), System Specs.
- **Out-of-Scope**: Tutorials, Marketing docs.

### 1.3 Inputs & Outputs

- **Inputs**: Code, Architecture designs.
- **Outputs**: Technical Specs, API References.

### 1.4 Must / Must Not

- **[REQ-DOC-API-01] API Details**: Endpoints MUST document Method, URL, Headers, Body, Success (2xx), Error (4xx/5xx).
- **[REQ-DOC-ADR-01] ADR Format**: Architecture decisions MUST follow Context, Decision, Consequences format.
- **[BAN-DOC-AMB-01] No Ambiguity**: Avoid "maybe", "should", "unlikely".

## 2. Procedures

### 2.1 documenting an API

1. **Endpoint**: Define path and method.
2. **Auth**: Specify required scopes/tokens.
3. **Request**: JSON schema or table of params.
4. **Response**: JSON example and schema.
5. **Errors**: List possible error codes.

### 2.2 Writing an ADR

1. **Context**: What is the problem?
2. **Options**: What did we consider?
3. **Decision**: What did we choose and why?
4. **Consequences**: What are the trade-offs (positive/negative)?

## 3. Examples

### 3.1 API Endpoint

```markdown
### POST /users

**Auth**: Bearer Token (scope: `write:users`)

**Body**:
```json
{
  "email": "user@example.com",
  "role": "admin"
}
```

**Response (201 Created)**:

```json
{
  "id": "u_123",
  "email": "user@example.com"
}
```

```

## 4. Validation Criteria

- [ ] **[VAL-DOC-API-01]** API docs include auth and error guidelines.
- [ ] **[VAL-DOC-ADR-01]** ADRs follow standard format.
- [ ] **[VAL-DOC-ACC-01]** No ambiguous terms found.

## 5. References
- Related: [0800-documentation-content.md](./0800-documentation-content.md)
