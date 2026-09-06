---
title: "Stage Authoring Matrix"
version: "1.1.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
---

# Stage Authoring Matrix

| Stage | `layer` | Purpose | Canonical owner | Completion evidence |
| --- | --- | --- | --- | --- |
| Agent governance | — | shared policies, roles, skills, and provider translations | `.agents/` plus authored native adapters | contract, renderer parity, Task |
| 01 | `requirements` | solution-independent requirements | Requirement Package | acceptance and traceability |
| 02 | `architecture` | current structure and durable decisions | Description or ADR | architecture traceability |
| 03 | `specs` | implementable change contract and execution | Spec Package | focused tests, Task, review |
| 05 | `operations` | operational knowledge and incidents | Operations catalog | safe procedure and observed result |
| 90 | `references` | non-normative evidence | Research, Audit, or Data | provenance and observation date |
| 98 | `archive` | frozen preserved bodies and recovery navigation | preserved records, Migration, or Tombstone | source-byte and Git recovery evidence |
| 99 | — | document contracts | registry, schemas, templates | registry/schema tests |

A `layer` value is the stage directory name without its numeric prefix.
The Stage 99 profile determines whether `layer` is required or omitted.
Canonical governance paths state their authority outside the numbered stages;
shared README profiles and native envelopes follow their registered exceptions.
A template source declares the layer of its destination where the profile requires it.

## Document Type Families

`type` is a `family/kind` pair. The family names the authority that owns the
document; the kind names its role inside that family.

| Family | Owning stage | Kinds |
| --- | --- | --- |
| `governance` | canonical agent governance | `sdlc`, `policy`, `hook-policy`, `role`, `skill`, `knowledge`, `knowledge-index`, `prompt`, `prompt-index`, `provider`, `provider-index`, `claude-agent`, `codex-agent` |
| `sdlc` | 01, 02, 03 | `requirement`, `architecture-description`, `architecture-decision`, `spec`, `plan`, `task`, `data-model`, `openapi`, `graphql`, `proto` |
| `operation` | 05 | `guide`, `policy`, `runbook`, `incident`, `postmortem`, `domain-readme` |
| `reference` | 90 | `research-pack`, `research`, `audit-pack`, `audit`, `data-pack`, `data`, `category-readme` |
| `archive` | 98 | `migration`, `tombstone` |
| `common` | any | `readme`, `documentation-readme`, `repository-readme`, `package-readme`, `runtime-governance-readme`, `template-source`, `unsupported` |

A Stage 90 `*-pack` kind is the container index; the bare kind is one `m####`
member inside it.

Claude discovers thin generated `.claude/skills/` adapters; Codex discovers the
canonical `.agents/skills/<skill_id>/SKILL.md` packages. Both require explicit
invocation and keep canonical role-selected reads available. Native entry fields
are `name` and `description`; existing governance fields are nested in `metadata`.
Discovery, instruction loading, invocation, and runtime acceptance are separate.
No generated provider surface becomes a shared authority.

`knowledge/` and `prompts/` are canonical categories, not stages. They route to owners and declare contracts; the owning policy, stage document, or Task keeps its authority.

The canonical home contains only registered canonical category sources.
Unknown or unsafe entries fail closed and are preserved for review; they are not
stale generated files eligible for automatic deletion.

## Related Documents

- [Documentation protocol](documentation-protocol.md)
- [SDLC](sdlc.md)
- [Stage 99 registry](../../docs/99.templates/registry.json)
