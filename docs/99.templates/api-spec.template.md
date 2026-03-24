<!-- Target: docs/04.specs/<feature-id>/api-spec.md -->
# [Feature Name] API Specification

> Use this template for `docs/04.specs/<feature-id>/api-spec.md`.
>
> Rules:
>
> - This document is a child of the feature Spec, not a separate top-level doc type.
> - Do not create a parallel `docs/api/` tree for this document.
> - Use this for REST, GraphQL, or gRPC contracts.
> - Link the parent Spec near the top.

---

## Overview (KR)

이 문서는 [기능명]이 외부에 노출하는 API 계약을 정의한다. 엔드포인트, 인증, 요청/응답 스키마, 에러, 버저닝, 비기능 요구를 상세히 기술한다.

## Parent Spec

- **Spec**: `[./spec.md]`

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
