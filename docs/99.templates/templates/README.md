---
title: Template Catalog
version: 1.0.0
type: common/readme
status: active
owner: "@buenhyden"
---

# Template Catalog

## Overview

This directory holds every copyable source registered by
[`../registry.json`](../registry.json). It is the only navigation surface for
templates; category directories carry no README of their own. Contract
explanations live in the [Stage 99 README](../README.md), and the rules a
finished document must satisfy live with its owning stage.

## Audience

- Documentation Writers
- Repository Maintainers
- AI Agents

## Scope

| Category | Directory | Registered roles |
| :--- | :--- | :--- |
| Governance | `governance/` | Contract, Control, Rule, Provider, Role, Skill |
| Runtime | `runtime/` | Claude agent projection, Codex agent projection |
| Requirements | `requirements/` | Requirement Package |
| Architecture | `architecture/` | Architecture Description, Architecture Decision |
| Specs | `specs/` | Spec, Plan, Task, and `contracts/` Data Model, OpenAPI, GraphQL, Proto |
| Operations | `operations/` | Guide, Policy, Runbook, Incident, Postmortem |
| References | `references/` | Research, Audit, Data — one pack form and one reference form each |
| Archive | `archive/` | Migration, Tombstone |
| Common | `common/` | Stage, domain, and package README forms |

## Structure

| Registered type | Source |
| :--- | :--- |
| `governance/sdlc` | [governance/contract.template.md](./governance/contract.template.md) |
| `governance/policy` | [governance/control.template.md](./governance/control.template.md) |
| `governance/hook-policy` | [governance/rule.template.md](./governance/rule.template.md) |
| `governance/provider` | [governance/provider.template.md](./governance/provider.template.md) |
| `governance/role` | [governance/role.template.md](./governance/role.template.md) |
| `governance/skill` | [governance/skill.template.md](./governance/skill.template.md) |
| `governance/claude-agent` | [runtime/claude-agent.template.md](./runtime/claude-agent.template.md) |
| `governance/codex-agent` | [runtime/codex-agent.template.toml](./runtime/codex-agent.template.toml) |
| `sdlc/requirement` | [requirements/requirement-package.template.md](./requirements/requirement-package.template.md) |
| `sdlc/architecture-description` | [architecture/description.template.md](./architecture/description.template.md) |
| `sdlc/architecture-decision` | [architecture/decision.template.md](./architecture/decision.template.md) |
| `sdlc/spec` | [specs/spec.template.md](./specs/spec.template.md) |
| `sdlc/plan` | [specs/plan.template.md](./specs/plan.template.md) |
| `sdlc/task` | [specs/task.template.md](./specs/task.template.md) |
| `sdlc/data-model` | [specs/contracts/data-model.template.md](./specs/contracts/data-model.template.md) |
| `sdlc/openapi` | [specs/contracts/openapi.template.yaml](./specs/contracts/openapi.template.yaml) |
| `sdlc/graphql` | [specs/contracts/schema.template.graphql](./specs/contracts/schema.template.graphql) |
| `sdlc/proto` | [specs/contracts/service.template.proto](./specs/contracts/service.template.proto) |
| `reference/category-readme` | [common/readme-category.template.md](./common/readme-category.template.md) |
| `common/documentation-readme` | [common/readme-documentation.template.md](./common/readme-documentation.template.md) |
| `common/repository-readme` | [common/readme-repository.template.md](./common/readme-repository.template.md) |
| `common/package-readme` | [common/readme-package.template.md](./common/readme-package.template.md) |
| `common/runtime-governance-readme` | [common/readme-runtime-governance.template.md](./common/readme-runtime-governance.template.md) |
| `operation/guide` | [operations/guide.template.md](./operations/guide.template.md) |
| `operation/policy` | [operations/policy.template.md](./operations/policy.template.md) |
| `operation/runbook` | [operations/runbook.template.md](./operations/runbook.template.md) |
| `operation/incident` | [operations/incident.template.md](./operations/incident.template.md) |
| `operation/postmortem` | [operations/postmortem.template.md](./operations/postmortem.template.md) |
| `operation/domain-readme` | [common/readme-domain.template.md](./common/readme-domain.template.md) |
| `reference/research-pack` | [references/research-pack.template.md](./references/research-pack.template.md) |
| `reference/research` | [references/research.template.md](./references/research.template.md) |
| `reference/audit-pack` | [references/audit-pack.template.md](./references/audit-pack.template.md) |
| `reference/audit` | [references/audit.template.md](./references/audit.template.md) |
| `reference/data-pack` | [references/data-pack.template.md](./references/data-pack.template.md) |
| `reference/data` | [references/data.template.md](./references/data.template.md) |
| `archive/migration` | [archive/migration.template.md](./archive/migration.template.md) |
| `archive/tombstone` | [archive/tombstone.template.md](./archive/tombstone.template.md) |
| `common/readme` | [common/readme-stage.template.md](./common/readme-stage.template.md) |

Replaced sources are recoverable through Git history.

## How to Work in This Area

1. Resolve the role in [`../registry.json`](../registry.json) and copy its
   registered `source`.
2. Replace every placeholder: `<name>` for free text, `####` for a four-digit
   number, `YYYY-MM-DD` for a date, and `"#.#.#"` for a semantic version.
   Machine contract sources use `__UPPER_SNAKE__` tokens instead.
3. Keep the declared `type`; allocate an identity above the persisted
   high-water mark where the profile declares one.
4. Run `python3 scripts/validation/run-ci-gate.py --profile full`.

Do not select a template by scanning directories, and do not copy a historical
template out of Git into current authoring.

## Related Documents

- [Stage 99 authority](../README.md)
- [Registry](../registry.json)
- [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md)
