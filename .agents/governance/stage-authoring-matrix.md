---
title: "Stage Authoring Matrix"
version: "1.4.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# Stage Authoring Matrix

## Purpose and Scope

### Objective

Map each stage to its layer, canonical owner, and completion evidence.

#### Authority

This policy is the canonical owner of the stage ownership and document type family map under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Current stage roles, document families, canonical ownership, and verification routes.

#### Exclusions

Shared README profiles, native envelopes, and scoped registry/schema/template reads keep the exceptions the documentation protocol registers.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| STAGE-AUTHORING-MATRIX-R1 | Authoring or classifying a document | Required: give every document a `type` as a `family/kind` pair whose family names the owning authority | none | none |
| STAGE-AUTHORING-MATRIX-R2 | Mapping stages | Required: keep the stage-to-layer-to-owner map (agent governance/01/02/03/05/90/98/99) | none | Completion evidence column of the stage table |
| STAGE-AUTHORING-MATRIX-R3 | Always | Required: a `layer` value is the stage directory name without its numeric prefix | none | none |
| STAGE-AUTHORING-MATRIX-R4 | Always | Required: the Stage 99 profile determines whether `layer` is required or omitted | none | none |
| STAGE-AUTHORING-MATRIX-R5 | Stage 98 | Required: register no `archive` type; its README uses `common/readme` | none | none |
| STAGE-AUTHORING-MATRIX-R6 | A template source | Required: declare the layer of its destination where the profile requires it | none | none |
| STAGE-AUTHORING-MATRIX-R7 | Always | Required: document language and README navigation follow the `documentation-protocol.md#document-language` and `#readme-navigation` rules | none | none |
| STAGE-AUTHORING-MATRIX-R8 | Files outside docs | Forbidden: treating stage ownership as making an individual stage document a current instruction source | none | none |
| STAGE-AUTHORING-MATRIX-R9 | Files outside docs | Required: use README navigation and canonical agent rules | none | none |
| STAGE-AUTHORING-MATRIX-R10 | Scoped execution reads and required registry/schema/template inputs | Allowed: retain the narrow exceptions in the documentation protocol | none | none |
| STAGE-AUTHORING-MATRIX-R11 | Claude and Codex skill discovery | Required: explicit invocation and keep canonical role-selected reads available | none | none |
| STAGE-AUTHORING-MATRIX-R12 | Native skill entry | Required: entry fields are `name` and `description` and governance fields nest in `metadata` | none | none |
| STAGE-AUTHORING-MATRIX-R13 | Always | Forbidden: a generated provider surface becoming a shared authority | none | none |
| STAGE-AUTHORING-MATRIX-R14 | `knowledge/` and `prompts/` | Required: treat as canonical categories not stages that route to owners and declare contracts while the owning policy/stage document/Task keeps authority | none | none |
| STAGE-AUTHORING-MATRIX-R15 | Stage 03 | Required: approval enables the registered transition, review remains read-only, and execution is recorded separately in the current Task | none | none |
| STAGE-AUTHORING-MATRIX-R16 | Stage 03 | Required: Task summary and lifecycle-event shape belong to Stage 99 and the Task carries observed evidence | none | none |
| STAGE-AUTHORING-MATRIX-R17 | Stage 03 | Forbidden: the Task authenticating an approval source | none | none |
| STAGE-AUTHORING-MATRIX-R18 | Document-family state, cardinality, and table shapes | Required: the Registry owns state vocabulary/direct parent cardinality/result and review table shapes/lifecycle generation and the SDLC owns their execution meaning | none | none |
| STAGE-AUTHORING-MATRIX-R19 | Canonical home | Required: contain only registered canonical category sources | none | none |
| STAGE-AUTHORING-MATRIX-R20 | Unknown or unsafe canonical-home entries | Required: fail closed and preserve for review | fail-closed handling | none |
| STAGE-AUTHORING-MATRIX-R21 | Unknown or unsafe canonical-home entries | Forbidden: automatic deletion as stale generated files | none | none |

| Stage | `layer` | Purpose | Canonical owner | Completion evidence |
| --- | --- | --- | --- | --- |
| Agent governance | — | shared policies, roles, skills, and provider translations | `.agents/` plus authored native adapters | contract, renderer parity, Task |
| 01 | `requirements` | solution-independent requirements | Requirement Package | acceptance and traceability |
| 02 | `architecture` | current structure and durable decisions | Description or ADR | architecture traceability |
| 03 | `specs` | implementable change contract and execution | Spec Package: Spec contracts behavior, Plan sequences work, Task records execution and item evidence | focused tests, Task, review |
| 05 | `operations` | operational knowledge and incidents | Operations Guide, Policy, Runbook, or Incident | safe procedure and observed result |
| 90 | `references` | non-normative evidence | Research, Audit, or Data | provenance and observation date |
| 98 | `archive` | the disposition scheme only; holds no records | its README | version history holds removed bodies; retired numbers live in the Registry |
| 99 | — | document contracts | registry, schemas, templates | registry/schema tests |

A `layer` value is the stage directory name without its numeric prefix.
The Stage 99 profile determines whether `layer` is required or omitted.
Canonical governance paths state their authority outside the numbered stages;
shared README profiles and native envelopes follow their registered exceptions.
Document language and README navigation follow
[documentation protocol](documentation-protocol.md#document-language) and its
[README navigation](documentation-protocol.md#readme-navigation) rule.
A template source declares the layer of its destination where the profile requires it.
Stage ownership does not make an individual stage document a current instruction
source for files outside docs. Use README navigation and canonical agent rules;
scoped execution reads and required registry/schema/template inputs retain the
narrow exceptions in that protocol.

#### Document Type Families

`type` is a `family/kind` pair. The family names the authority that owns the
document; the kind names its role inside that family.

| Family | Owning stage | Kinds |
| --- | --- | --- |
| `governance` | canonical agent governance | `workflow`, `policy`, `rule`, `control`, `role`, `skill`, `prompt`, `provider`; native `claude-agent`, `codex-agent` |
| `sdlc` | 01, 02, 03 | `requirement`, `architecture-description`, `architecture-decision`, `spec`, `plan`, `task`, `data-model`, `openapi`, `graphql`, `proto` |
| `operation` | 05 | `guide`, `policy`, `runbook`, `incident`, `postmortem` |
| `reference` | 90 | `research-pack`, `research`, `audit-pack`, `audit`, `data-pack`, `data` |
| `common` | any | `readme`, `agent-guide` (folder `AGENTS.md`); supporting `template-source`, `unsupported` |

Stage 98 registers no `archive` type; its README uses `common/readme`.
A Stage 90 `*-pack` kind is the container index; the bare kind is one `m####`
member inside it.

Claude discovers thin generated `.claude/skills/` adapters; Codex discovers the
canonical `.agents/skills/<skill_id>/SKILL.md` packages. Both require explicit
invocation and keep canonical role-selected reads available. Native entry fields
are `name` and `description`; existing governance fields are nested in `metadata`.
Discovery, instruction loading, invocation, and runtime acceptance are separate.
No generated provider surface becomes a shared authority.

`knowledge/` and `prompts/` are canonical categories, not stages. They route to owners and declare contracts; the owning policy, stage document, or Task keeps its authority.

For Stage 03, approval enables the registered transition but review remains
read-only and execution is recorded separately in the current Task. Task
summary and optional lifecycle-event shape belong to Stage 99; the Task carries
observed evidence and never authenticates an approval source. The Registry owns
document-family state vocabulary, direct parent cardinality, result and review
table shapes, and lifecycle generation; the SDLC owns their execution meaning.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

The canonical home contains only registered canonical category sources.
Unknown or unsafe entries fail closed and are preserved for review; they are not
stale generated files eligible for automatic deletion.

### Limits

The policy names no check tied to a specific rule; most of the map rests on review:

- Type families, stage-to-layer-to-owner map, `layer` values, and Stage 99 profile (R1-R7): no check is named here; stage completion evidence is a record, not a check.
- Instruction-source boundary, provider discovery, and generated-surface authority (R8-R13): no check is named, and discovery, instruction loading, invocation, and runtime acceptance are separate and not proven by this policy.
- Category and Stage 03 rules (R14-R18): rest on review; the Task never authenticates an approval source.
- Canonical home (R19, R21): no check is named; unknown or unsafe entries are preserved for review, so their disposition is manual.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Documentation protocol](documentation-protocol.md)
- [SDLC](sdlc.md)
- Stage 99 registry (`docs/99.templates/registry.json`)
- [Documentation index](../../docs/README.md)
