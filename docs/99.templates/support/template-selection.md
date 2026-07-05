---
layer: agentic
---

# Template Selection

## Overview

This document maps document purpose and target path to the canonical copyable
template source.

## Stage Template Mapping

| Role | Target Location | Template |
| --- | --- | --- |
| PRD | `docs/01.requirements/NNN-<feature-or-system>.md` | [prd.template.md](../templates/sdlc/prd.template.md) |
| ARD | `docs/02.architecture/requirements/####-<system-or-domain>.md` | [ard.template.md](../templates/sdlc/ard.template.md) |
| ADR | `docs/02.architecture/decisions/####-<short-title>.md` | [adr.template.md](../templates/sdlc/adr.template.md) |
| Spec | `docs/03.specs/NNN-<feature-id>/spec.md` | [spec.template.md](../templates/sdlc/spec.template.md) |
| Plan | `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` | [plan.template.md](../templates/sdlc/plan.template.md) |
| Task | `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` | [task.template.md](../templates/sdlc/task.template.md) |
| Guide | `docs/05.operations/guides/**.md` | [guide.template.md](../templates/operations/guide.template.md) |
| Policy | `docs/05.operations/policies/**.md` | [policy.template.md](../templates/operations/policy.template.md) |
| Runbook | `docs/05.operations/runbooks/**.md` | [runbook.template.md](../templates/operations/runbook.template.md) |
| Incident packet incident file | `docs/05.operations/incidents/YYYY/INC-###-<incident-title>/INC-###-<incident-title>.md` | [incident.template.md](../templates/operations/incident.template.md) |
| Incident packet postmortem.md | `docs/05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md` | [postmortem.template.md](../templates/operations/postmortem.template.md) |
| Reference | `docs/90.references/{audits,data,research,learning}/**/*.md` | [reference.template.md](../templates/common/reference.template.md) |
| Archive | `docs/98.archive/<original-stage>/<original-path>.md` | [archive.template.md](../templates/common/archive.template.md) |
| README | `README.md`, `docs/README.md`, folder `README.md` files | [readme.template.md](../templates/common/readme.template.md) |

## Restructure Disposition Mapping

When a document restructure task classifies a target, choose the template or
target action from this mapping:

| Disposition | Template or Action | Selection Rule |
| --- | --- | --- |
| `active-canonical` | Keep the target's current primary template role. | Do not retag or move only because the document is old. |
| `historical-archive` | [archive.template.md](../templates/common/archive.template.md) for the tombstone. | Use after active links and current replacement pointers are reviewed. |
| `duplicate-remove` | Usually no new template; use archive template only when a tombstone is required for traceability. | Remove only after the canonical replacement is recorded. |
| `conflict-remove-or-archive` | Archive template when removing from active chain; otherwise create a gap/reference record. | Do not leave conflicting current-truth guidance active without a gap. |
| `evidence-preserve` | Preserve the existing evidence profile; add Stage 90 reference context if needed. | Do not rewrite historical evidence for style-only cleanup. |

## Spec Child Template Mapping

| Role | Target Location | Template |
| --- | --- | --- |
| API spec | `docs/03.specs/NNN-<feature-id>/api-spec.md` | [api-spec.template.md](../templates/spec-contracts/api-spec.template.md) |
| Agent design | `docs/03.specs/NNN-<feature-id>/agent-design.md` | [agent-design.template.md](../templates/spec-contracts/agent-design.template.md) |
| Data model | `docs/03.specs/NNN-<feature-id>/data-model.md` | [data-model.template.md](../templates/spec-contracts/data-model.template.md) |
| Service | `docs/03.specs/NNN-<feature-id>/service.md` | [service.template.md](../templates/spec-contracts/service.template.md) |
| Tests | `docs/03.specs/NNN-<feature-id>/tests.md` | [tests.template.md](../templates/spec-contracts/tests.template.md) |
| OpenAPI | `docs/03.specs/NNN-<feature-id>/contracts/openapi.yaml` | [openapi.template.yaml](../templates/spec-contracts/openapi.template.yaml) |
| GraphQL | `docs/03.specs/NNN-<feature-id>/contracts/schema.graphql` | [schema.template.graphql](../templates/spec-contracts/schema.template.graphql) |
| Protobuf | `docs/03.specs/NNN-<feature-id>/contracts/service.proto` | [service.template.proto](../templates/spec-contracts/service.template.proto) |

## Governance Template Mapping

| Role | Target Location | Template |
| --- | --- | --- |
| Memory | `docs/00.agent-governance/memory/<note>.md` | [memory.template.md](../templates/governance/memory.template.md) |
| Progress | `docs/00.agent-governance/memory/progress.md` | [progress.template.md](../templates/governance/progress.template.md) |
| Harness task contract | `docs/04.execution/tasks/YYYY-MM-DD-<harness-stream>.md` | [harness-task-contract.template.md](../templates/governance/harness-task-contract.template.md) |

## Selection Rules

- Choose exactly one primary template for each target document.
- Use spec child templates only inside the matching feature spec directory.
- Use operations templates by purpose: guide for usage context, policy for
  controls and exceptions, runbook for ordered procedures and evidence.
- Use reference templates for stable facts only; do not put active policy or
  runbook procedure into Stage 90 references.
- Use archive templates only for tombstones, not for preserving stale body text.
- Keep guide, policy, and runbook roles separate during bucket restructure
  work; path cleanup does not merge their templates or purposes.

## Related Documents

- [support README](./README.md)
- [template contract](./template-contract.md)
- [templates README](../templates/README.md)
