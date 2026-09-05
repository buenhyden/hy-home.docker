---
title: "Stage Authoring Matrix"
version: "1.0.1"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
---

# Stage Authoring Matrix

| Stage | `layer` | Purpose | Canonical owner | Completion evidence |
| --- | --- | --- | --- | --- |
| 00 | — | policies, roles, provider adapters, skills | Stage 00 plus provider registry | contract, renderer parity, Task |
| 01 | `requirements` | solution-independent requirements | Requirement Package | acceptance and traceability |
| 02 | `architecture` | current structure and durable decisions | Description or ADR | architecture traceability |
| 03 | `specs` | implementable change contract and execution | Spec Package | focused tests, Task, review |
| 05 | `operations` | operational knowledge and incidents | Operations catalog | safe procedure and observed result |
| 90 | `references` | non-normative evidence | Research, Audit, or Data | provenance and observation date |
| 98 | `archive` | minimal recovery navigation | Migration or Tombstone | recovery commit |
| 99 | — | document contracts | registry, schemas, templates | registry/schema tests |

A `layer` value is the stage directory name without its numeric prefix.
Stage 00 and Stage 99 documents declare no `layer`: their canonical path is
their authority. A template source declares the layer of the stage it authors
into, so a Stage 00 authoring form declares none.

## Document Type Families

`type` is a `family/kind` pair. The family names the authority that owns the
document; the kind names its role inside that family.

| Family | Owning stage | Kinds |
| --- | --- | --- |
| `governance` | 00 | `sdlc`, `policy`, `hook-policy`, `role`, `skill`, `provider`, `provider-index`, `claude-agent`, `codex-agent` |
| `sdlc` | 01, 02, 03 | `requirement`, `architecture-description`, `architecture-decision`, `spec`, `plan`, `task`, `data-model`, `openapi`, `graphql`, `proto` |
| `operation` | 05 | `guide`, `policy`, `runbook`, `incident`, `postmortem`, `domain-readme` |
| `reference` | 90 | `research-pack`, `research`, `audit-pack`, `audit`, `data-pack`, `data`, `category-readme` |
| `archive` | 98 | `migration`, `tombstone` |
| `common` | any | `readme`, `documentation-readme`, `repository-readme`, `package-readme`, `runtime-governance-readme`, `template-source`, `unsupported` |

A Stage 90 `*-pack` kind is the container index; the bare kind is one `m####`
member inside it.

Claude discovers its generated `.claude/skills/` projection. Codex reads the
canonical Stage 00 `skills/` files explicitly through its adapter and role
instructions. Native discovery and canonical instruction loading are distinct;
neither makes a provider projection a second policy source.

An absent or empty real `.agents/` root is an allowed non-authoritative physical
container, not a shared role/skill projection, generated README, or native
picker route. Unknown or nonempty contents fail closed and are preserved without
automatic deletion.

## Related Documents

- [Documentation protocol](documentation-protocol.md)
- [SDLC](../sdlc.md)
- [Stage 99 registry](../../99.templates/registry.json)
