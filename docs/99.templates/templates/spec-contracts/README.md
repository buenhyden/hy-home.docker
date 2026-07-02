---
layer: agentic
---

# Spec Contract Templates

> child contracts and machine-readable schema templates for feature specs

## Overview

`docs/99.templates/templates/spec-contracts` contains copyable templates for
contracts that live under a feature spec directory. These templates supplement
the parent SDLC spec; they do not replace the parent `spec.md`.

## Templates

| Need | Template |
| --- | --- |
| Define endpoint, authentication, error, and compatibility rules | [api-spec.template.md](./api-spec.template.md) |
| Specify an agent role, IO contract, tools, memory, guardrails, and evals | [agent-design.template.md](./agent-design.template.md) |
| Describe entities, relationships, validation, storage, and migrations | [data-model.template.md](./data-model.template.md) |
| Capture service image, hardening, network, secret, healthcheck, and ops requirements | [service.template.md](./service.template.md) |
| Define verification goals, test matrix, evals, fixtures, and evidence | [tests.template.md](./tests.template.md) |
| Seed an OpenAPI contract owned by the parent API spec | [openapi.template.yaml](./openapi.template.yaml) |
| Seed a GraphQL schema contract owned by the parent API spec | [schema.template.graphql](./schema.template.graphql) |
| Seed a protobuf service contract owned by the parent API spec | [service.template.proto](./service.template.proto) |

## Target Rules

- Markdown contract templates target
  `docs/03.specs/<feature-id>/{api-spec,agent-design,data-model,service,tests}.md`.
- `openapi.template.yaml` targets
  `docs/03.specs/<feature-id>/contracts/openapi.yaml`.
- `schema.template.graphql` targets
  `docs/03.specs/<feature-id>/contracts/schema.graphql`.
- `service.template.proto` targets
  `docs/03.specs/<feature-id>/contracts/service.proto`.
- Markdown contract templates use target-relative links; machine-readable
  templates use `Cross-links:` comments.

## Related Documents

- [templates catalog](../README.md)
- [template selection](../../support/template-selection.md)
- [template contract](../../support/template-contract.md)
- [frontmatter contract](../../support/frontmatter-contract.md)
