---
title: "Stage Authoring Matrix"
version: "1.5.1"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-19"
---

# Stage Authoring Matrix

## Purpose and Scope

### Objective

Map each stage to its layer, canonical owner, and completion evidence.

#### Authority

This policy is the canonical owner of the stage ownership and document type family map under [bootstrap precedence](../../../.agents/governance/bootstrap.md#authority-and-precedence).

### Applies To

Current stage roles, document families, canonical ownership, and verification routes.

#### Exclusions

Shared README profiles, native envelopes, and scoped registry/schema/template reads keep the exceptions the documentation protocol registers.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| STAGE-AUTHORING-MATRIX-R1 | Mapping stages | Required: each stage keeps the `layer`, purpose, canonical owner and completion evidence given in the stage table | none | none |
| STAGE-AUTHORING-MATRIX-R2 | Always | Required: a `layer` value is the stage directory name without its numeric prefix | none | none |
| STAGE-AUTHORING-MATRIX-R3 | Always | Required: the Stage 99 profile determines whether `layer` is required or omitted | none | none |
| STAGE-AUTHORING-MATRIX-R4 | Canonical governance paths | Required: agent governance states its authority outside the numbered stages; Stage 00 holds the workspace policy | none | none |
| STAGE-AUTHORING-MATRIX-R5 | Shared README profiles and native envelopes | Required: follow their registered exceptions | none | none |
| STAGE-AUTHORING-MATRIX-R6 | Always | Required: document language follows the `documentation-protocol.md#document-language` rule | none | none |
| STAGE-AUTHORING-MATRIX-R7 | Always | Required: README navigation follows the `documentation-protocol.md#readme-navigation` rule | none | none |
| STAGE-AUTHORING-MATRIX-R8 | A template source | Required: declare the layer of its destination where the profile requires it | none | none |
| STAGE-AUTHORING-MATRIX-R9 | Files outside docs | Forbidden: treating stage ownership as making an individual stage document a current instruction source | none | none |
| STAGE-AUTHORING-MATRIX-R10 | Files outside docs | Required: use README navigation and canonical agent rules | none | none |
| STAGE-AUTHORING-MATRIX-R11 | Scoped execution reads and required registry/schema/template inputs | Allowed: retain the narrow exceptions in the documentation protocol | none | none |
| STAGE-AUTHORING-MATRIX-R12 | Authoring or classifying a document | Required: `type` is a `family/kind` pair whose family names the owning authority and whose kind names its role in that family | none | none |
| STAGE-AUTHORING-MATRIX-R13 | Assigning a `type` | Required: use a family, owning stage and kind from the Document Type Families table | none | none |
| STAGE-AUTHORING-MATRIX-R14 | Stage 98 | Forbidden: registering an `archive` type | none | none |
| STAGE-AUTHORING-MATRIX-R15 | Stage 98 README | Required: use `common/readme` | none | none |
| STAGE-AUTHORING-MATRIX-R16 | Stage 90 kinds | Required: a `*-pack` kind is the container index and the bare kind is one `m####` member inside it | none | none |
| STAGE-AUTHORING-MATRIX-R17 | Skill discovery | Required: Claude discovers thin generated `.claude/skills/` adapters and Codex discovers the canonical `.agents/skills/<skill_id>/SKILL.md` packages | none | none |
| STAGE-AUTHORING-MATRIX-R18 | Claude and Codex skills | Required: explicit invocation | none | none |
| STAGE-AUTHORING-MATRIX-R19 | Claude and Codex skills | Required: keep canonical role-selected reads available | none | none |
| STAGE-AUTHORING-MATRIX-R20 | Native skill entry | Required: entry fields are `name` and `description` | none | none |
| STAGE-AUTHORING-MATRIX-R21 | Native skill entry | Required: existing governance fields nest in `metadata` | none | none |
| STAGE-AUTHORING-MATRIX-R22 | Always | Required: keep discovery, instruction loading, invocation and runtime acceptance separate | none | none |
| STAGE-AUTHORING-MATRIX-R23 | Always | Forbidden: a generated provider surface becoming a shared authority | none | none |
| STAGE-AUTHORING-MATRIX-R24 | `knowledge/` and `prompts/` | Required: treat them as canonical categories, not stages | none | none |
| STAGE-AUTHORING-MATRIX-R25 | `knowledge/` and `prompts/` | Required: they route to owners and declare contracts while the owning policy, stage document or Task keeps its authority | none | none |
| STAGE-AUTHORING-MATRIX-R26 | Stage 03 | Required: approval enables the registered transition | none | none |
| STAGE-AUTHORING-MATRIX-R27 | Stage 03 | Required: review remains read-only | none | none |
| STAGE-AUTHORING-MATRIX-R28 | Stage 03 | Required: record execution separately in the current Task | none | none |
| STAGE-AUTHORING-MATRIX-R29 | Stage 03 | Required: Task summary and optional lifecycle-event shape belong to Stage 99 | none | none |
| STAGE-AUTHORING-MATRIX-R30 | Stage 03 | Required: the Task carries observed evidence | none | none |
| STAGE-AUTHORING-MATRIX-R31 | Stage 03 | Forbidden: the Task authenticating an approval source | none | none |
| STAGE-AUTHORING-MATRIX-R32 | Document-family state, cardinality and table shapes | Required: the Registry owns state vocabulary, direct parent cardinality, result and review table shapes and lifecycle generation | none | none |
| STAGE-AUTHORING-MATRIX-R33 | Document-family state, cardinality and table shapes | Required: the SDLC owns their execution meaning | none | none |
| STAGE-AUTHORING-MATRIX-R34 | Assigning a common rule | Required: exactly one owner among the layers in the Responsibility Layers table | none | none |
| STAGE-AUTHORING-MATRIX-R35 | Approval meaning | Required: the approval scope people and agents share lives only in Stage 00 approval boundaries; the agent layer keeps only how an agent confirms the source, withdrawal and stop, and links there | none | none |
| STAGE-AUTHORING-MATRIX-R36 | Machine-read hook rules and native bindings | Forbidden: moving them out of the agent layer as policy text | none | none |

| Stage | `layer` | Purpose | Canonical owner | Completion evidence |
| --- | --- | --- | --- | --- |
| 00 | — | workspace policy that people and agents share | `docs/00.workspace/` policies | contract, link checks, Task |
| Agent governance | — | agent execution policies, roles, skills, and provider translations | `.agents/` plus authored native adapters | contract, renderer parity, Task |
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
[documentation protocol](../03.process/documentation-protocol.md#document-language) and its
[README navigation](../03.process/documentation-protocol.md#readme-navigation) rule.
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
| `governance` | Stage 00 and canonical agent governance | `workflow`, `policy`, `rule`, `control`, `role`, `skill`, `prompt`, `provider`; native `claude-agent`, `codex-agent` |
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

#### Responsibility Layers

Each common rule has one meaning owner. A layer is a responsibility, not a
directory to create.

| Layer | Owns | Current owner |
| --- | --- | --- |
| W, workspace | purpose, responsibilities, change process, documentation, Git, approval scope, quality and done criteria | `docs/00.workspace/` |
| P, product | durable requirements, structure, quality scenarios and operating procedures | Stages 01, 02 and 05 |
| R, request | change scope, normal and failure behavior, acceptance, work and evidence | the Spec, Plan and Task of Stage 03 |
| C, event | facts of deployments, incidents, reviews and observations | Runbooks, Incidents, Postmortems, Tasks and the Git and deployment record |
| A, agent | role selection, delegation, approval-source confirmation, context and stop | `.agents/`, root and folder guides, native adapters |
| I, enforcement | checks, hooks, CI, tests and permission enforcement | `scripts/`, `tests/`, `.github/` and native settings |
| T, form | common sections, tables, types, states and path bindings | Stage 99 Registry, schemas and templates |

A machine check implements the rule its owner states and never becomes a
second owner. Hookify rules and native bindings are I and A inputs and stay
with their loaders.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](../04.quality/approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

The canonical home contains only registered canonical category sources.
Unknown or unsafe entries fail closed and are preserved for review; they are not
stale generated files eligible for automatic deletion.

### Limits

The policy names no check that enforces or verifies any rule in this table; every row records `none`.

- Stage map, `layer`, governance paths, language, navigation and template layer rules (R1-R11) name no check; the stage table's completion evidence column describes each stage's evidence, not a check of this policy.
- Document type families, Stage 98 and Stage 90 kinds (R12-R16) name no check.
- Skill discovery, invocation, native entry fields and generated-surface authority (R17-R23) name no check; discovery, instruction loading, invocation and runtime acceptance are kept separate, not proven by this policy.
- Category and Stage 03 rules (R24-R33) name no check; the Task carries observed evidence and never authenticates an approval source.
- Responsibility layer, approval-meaning and hook-input rules (R34-R36) name no check.
- Rules stated under Enforcement/Mechanisms (the canonical home and its unknown or unsafe entries) are outside the table.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](../04.quality/approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Documentation protocol](../03.process/documentation-protocol.md)
- [SDLC](../03.process/sdlc.md)
- Stage 99 registry (`docs/99.templates/registry.json`)
- [Documentation index](../../README.md)
