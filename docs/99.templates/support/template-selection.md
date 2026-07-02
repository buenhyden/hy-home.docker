---
layer: agentic
---

# Template Selection

## Overview

This document maps document purpose and target path to the canonical copyable
template source.

## Stage Template Mapping

| Target Location | Template |
| --- | --- |
| `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md` | [prd.template.md](../templates/sdlc/prd.template.md) |
| `docs/02.architecture/requirements/####-<system-or-domain>.md` | [ard.template.md](../templates/sdlc/ard.template.md) |
| `docs/02.architecture/decisions/####-<short-title>.md` | [adr.template.md](../templates/sdlc/adr.template.md) |
| `docs/03.specs/<feature-id>/spec.md` | [spec.template.md](../templates/sdlc/spec.template.md) |
| `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` | [plan.template.md](../templates/sdlc/plan.template.md) |
| `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` | [task.template.md](../templates/sdlc/task.template.md) |
| `docs/05.operations/guides/**.md` | [guide.template.md](../templates/operations/guide.template.md) |
| `docs/05.operations/policies/**.md` | [policy.template.md](../templates/operations/policy.template.md) |
| `docs/05.operations/runbooks/**.md` | [runbook.template.md](../templates/operations/runbook.template.md) |
| `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>.md` | [incident.template.md](../templates/operations/incident.template.md) |
| `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>-postmortem.md` | [postmortem.template.md](../templates/operations/postmortem.template.md) |
| `docs/90.references/<category>/<item>.md` | [reference.template.md](../templates/common/reference.template.md) |
| `docs/98.archive/<original-stage>/<original-path>.md` | [archive.template.md](../templates/common/archive.template.md) |
| `README.md`, `docs/README.md`, folder `README.md` files | [readme.template.md](../templates/common/readme.template.md) |

## Spec Child Template Mapping

| Target Location | Template |
| --- | --- |
| `docs/03.specs/<feature-id>/api-spec.md` | [api-spec.template.md](../templates/spec-contracts/api-spec.template.md) |
| `docs/03.specs/<feature-id>/agent-design.md` | [agent-design.template.md](../templates/spec-contracts/agent-design.template.md) |
| `docs/03.specs/<feature-id>/data-model.md` | [data-model.template.md](../templates/spec-contracts/data-model.template.md) |
| `docs/03.specs/<feature-id>/service.md` | [service.template.md](../templates/spec-contracts/service.template.md) |
| `docs/03.specs/<feature-id>/tests.md` | [tests.template.md](../templates/spec-contracts/tests.template.md) |
| `docs/03.specs/<feature-id>/contracts/openapi.yaml` | [openapi.template.yaml](../templates/spec-contracts/openapi.template.yaml) |
| `docs/03.specs/<feature-id>/contracts/schema.graphql` | [schema.template.graphql](../templates/spec-contracts/schema.template.graphql) |
| `docs/03.specs/<feature-id>/contracts/service.proto` | [service.template.proto](../templates/spec-contracts/service.template.proto) |

## Governance Template Mapping

| Target Location | Template |
| --- | --- |
| `docs/00.agent-governance/memory/<note>.md` | [memory.template.md](../templates/governance/memory.template.md) |
| `docs/00.agent-governance/memory/progress.md` | [progress.template.md](../templates/governance/progress.template.md) |
| Task-specific harness contract docs | [harness-task-contract.template.md](../templates/governance/harness-task-contract.template.md) |

## Selection Rules

- Choose exactly one primary template for each target document.
- Use spec child templates only inside the matching feature spec directory.
- Use operations templates by purpose: guide for usage context, policy for
  controls and exceptions, runbook for ordered procedures and evidence.
- Use reference templates for stable facts only; do not put active policy or
  runbook procedure into Stage 90 references.
- Use archive templates only for tombstones, not for preserving stale body text.

## Related Documents

- [support README](./README.md)
- [template contract](./template-contract.md)
- [templates README](../templates/README.md)
