---
layer: agentic
---

# Spec Contract Templates

> child contracts and machine-readable schema templates for feature specs

## Overview

`docs/99.templates/templates/spec-contracts` contains copyable templates for
contracts that live under a feature spec directory. These templates supplement
the parent SDLC spec; they do not replace the parent `spec.md`.

## Use When

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

## Do Not Use For

- Top-level requirements, architecture, design, plan, or task documents; use
  [SDLC templates](../sdlc/README.md).
- Standalone service operations procedures; use
  [operations](../operations/README.md).
- General references under Stage 90; use
  [common/reference.template.md](../common/reference.template.md).

## Target Rules

- Place contract documents under the matching `docs/03.specs/<feature-id>/`
  directory.
- Keep machine-readable contracts under the feature spec's `contracts/`
  subdirectory unless the approved spec states a narrower path.
- Link each child contract from the parent spec or API spec.
- Do not add Markdown frontmatter to YAML, GraphQL, or protobuf templates.

## Related Documents

- [templates catalog](../README.md)
- [template selection](../../support/template-selection.md)
- [template contract](../../support/template-contract.md)
- [frontmatter contract](../../support/frontmatter-contract.md)
