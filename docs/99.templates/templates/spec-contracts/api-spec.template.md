---
status: draft
artifact_id: <artifact-id>
artifact_type: spec
parent_ids: [<parent-artifact-id>]
---
<!-- Target: docs/03.specs/NNN-<feature-id>/api-spec.md -->

# [API Name] Specification

> Use this template for `docs/03.specs/NNN-<feature-id>/api-spec.md`.
>
> Rules:
>
> - This document is a child of the feature Spec, not a separate top-level doc type.
> - Do not create a parallel `docs/api/` tree for this document.
> - Use this for REST, GraphQL, or gRPC contracts.
> - Link the parent Spec near the top.
> - Write this document in English. Preserve code identifiers, command names,
>   service names, environment variables, and quoted upstream terms exactly.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.

---

## Overview

This document defines the API contract exposed by [feature name]. It describes
endpoints, authentication, request and response schemas, errors, versioning, and
non-functional requirements.

## Parent Spec

- **Spec**: [./spec.md](./spec.md)

## Scope & Non-goals

- **Covers**:
- **Does Not Cover**:
- **Parent Design Context**: full design rationale remains in `spec.md`

## API Style

- **Type**: `REST | GraphQL | gRPC`
- **Audience**:
- **Versioning Strategy**:

## Authentication & Authorization

- **Auth Mechanism**:
- **Scopes / Roles**:
- **Rate Limit / Abuse Control**:

## Endpoint / Operation Catalog

| Operation ID | Method / Type | Path / Name | Purpose | Caller |
| --- | --- | --- | --- | --- |
| API-001 | GET | `/example` | [Purpose] | [Client] |

## Request / Response Schemas

### Request

```json
{
  "example": "value"
}
```

### Response

```json
{
  "id": "123",
  "status": "ok"
}
```

## Error Model

| Code | Meaning | Retryable | Notes |
| --- | --- | --- | --- |
| 400 | Bad Request | No | Validation error |

## Data Contract Compatibility

- **Backward Compatibility Rule**:
- **Breaking Change Rule**:
- **Deprecation Policy**:

## Non-Functional Requirements

- **Latency Budget**:
- **Availability Expectation**:
- **Observability**:
- **Audit / Traceability**:

## Machine-readable Contract Files

- `./contracts/openapi.yaml`
- `./contracts/service.proto`
- `./contracts/schema.graphql`

## Verification

- Contract lint
- Mock / integration test
- Consumer compatibility check

## Related Documents

- **Parent Spec**: [./spec.md](./spec.md)
- **Data Model**: [./data-model.md](./data-model.md)
- **Tests**: [./tests.md](./tests.md)
