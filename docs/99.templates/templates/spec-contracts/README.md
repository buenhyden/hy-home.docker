---
layer: agentic
---

# Spec Contract Templates

## Overview

`docs/99.templates/templates/spec-contracts`는 parent Spec 아래에서 별도로
검토할 Markdown 및 기계 판독 가능 계약 원본을 안내한다.

## Audience

- Documentation Writers
- AI Agents
- Software and QA Engineers

## Scope

- API, Agent, Data Model, Service, Tests Markdown 계약
- OpenAPI, GraphQL, Protobuf 기계 판독 가능 계약
- parent Spec가 유지하는 계약 소유권과 연결 경계

## Structure

| Role | Template |
| --- | --- |
| API Spec | [api-spec.template.md](./api-spec.template.md) |
| Agent Design | [agent-design.template.md](./agent-design.template.md) |
| Data Model | [data-model.template.md](./data-model.template.md) |
| Service | [service.template.md](./service.template.md) |
| Tests | [tests.template.md](./tests.template.md) |
| OpenAPI | [openapi.template.yaml](./openapi.template.yaml) |
| GraphQL | [schema.template.graphql](./schema.template.graphql) |
| Protobuf | [service.template.proto](./service.template.proto) |

## How to Work in This Area

1. [template selection](../../support/template-selection.md)에서 parent Spec에 필요한 계약 역할을 확인한다.
2. Markdown 원본의 모든 `{{token_name}}`을 계약 근거로 바꾼다.
3. 기계 판독 원본의 모든 `__TOKEN_NAME__`을 실제 계약 값으로 바꾼다.
4. parent Spec에는 자식 계약의 요약, 소유권, 링크만 유지한다.
5. 변경 후 [template contract](../../support/template-contract.md)와 저장소 검증을 확인한다.

## Related Documents

- [templates catalog](../README.md)
- [SDLC template catalog](../sdlc/README.md)
- [template selection](../../support/template-selection.md)
- [template contract](../../support/template-contract.md)
- [frontmatter contract](../../support/frontmatter-contract.md)
