---
title: "Provider Capability Matrix"
version: "1.4.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-19"
---

# Provider Capability Matrix

## Purpose and Scope

### Objective

Canonical agent governance supports exactly Claude and Codex. Capability
documentation separates provider support, repository adoption, and observed
runtime acceptance.

#### Authority

This policy is the canonical owner of the provider capability matrix and authority namespaces under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Canonical ownership, provider adapters, tracked configuration, and observed runtime capabilities.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| PROVIDER-CAPABILITY-MATRIX-R1 | `.agents/governance`, roles and skills | Required: own shared behavior, workflow, approval, role separation and reusable procedures | none | none |
| PROVIDER-CAPABILITY-MATRIX-R2 | `.agents/governance`, roles and skills | Forbidden: owning provider syntax or document profiles | none | none |
| PROVIDER-CAPABILITY-MATRIX-R3 | Stage 99 Registry | Required: own document paths, profiles, identifiers, lifecycle values and template mappings | none | none |
| PROVIDER-CAPABILITY-MATRIX-R4 | Stage 99 Registry | Forbidden: owning agent workflow or provider runtime translation | none | none |
| PROVIDER-CAPABILITY-MATRIX-R5 | Provider Registry | Required: own provider identities, projection routes, model/permission translations, semantic events and hook commands | none | none |
| PROVIDER-CAPABILITY-MATRIX-R6 | Provider Registry | Forbidden: owning shared workflow, retry, evidence or stop policy | none | none |
| PROVIDER-CAPABILITY-MATRIX-R7 | Authored native `provider.md` | Required: own provider loading and syntax differences | none | none |
| PROVIDER-CAPABILITY-MATRIX-R8 | Authored native `provider.md` | Forbidden: owning shared governance or model policy | none | none |
| PROVIDER-CAPABILITY-MATRIX-R9 | Generated native files and runtime controls | Required: hold provider configuration consuming the owners above | none | none |
| PROVIDER-CAPABILITY-MATRIX-R10 | Generated native files and runtime controls | Forbidden: holding independent shared authority | none | none |
| PROVIDER-CAPABILITY-MATRIX-R11 | Role intent | Required: owned by `.agents/roles/*.md`, adapted by `.claude/agents/*.md` and `.codex/agents/*.toml` | none | none |
| PROVIDER-CAPABILITY-MATRIX-R12 | Procedures | Required: owned by `.agents/skills/*/SKILL.md`, adapted by thin generated `.claude/skills/*/SKILL.md` and Codex canonical native skill discovery and explicit reads | none | none |
| PROVIDER-CAPABILITY-MATRIX-R13 | Explicit invocation | Required: owned by skill-local control and shared approval, adapted by Claude `disable-model-invocation: true` and Codex `agents/openai.yaml` `policy.allow_implicit_invocation: false` | none | none |
| PROVIDER-CAPABILITY-MATRIX-R14 | Model and effort | Required: owned by the Provider Registry, adapted by native model and effort (Claude) and native model and reasoning (Codex) | none | none |
| PROVIDER-CAPABILITY-MATRIX-R15 | Permissions | Required: owned by the role plus the Provider Registry, adapted by Claude permission mode and Codex sandbox mode | none | none |
| PROVIDER-CAPABILITY-MATRIX-R16 | Semantic events | Required: owned by the Registry plus native hook config, adapted by the Claude and Codex adapters | none | none |
| PROVIDER-CAPABILITY-MATRIX-R17 | Native skill frontmatter | Required: use `name`, `description` and nested governance `metadata` | none | none |
| PROVIDER-CAPABILITY-MATRIX-R18 | Native skills | Required: folder, name and stable function identity agree | none | none |
| PROVIDER-CAPABILITY-MATRIX-R19 | Skill discovery | Forbidden: treating discovery as invocation or approval | none | none |
| PROVIDER-CAPABILITY-MATRIX-R20 | Skills | Forbidden: a skill adding tool grants or installers | none | none |
| PROVIDER-CAPABILITY-MATRIX-R21 | Always | Required: keep `.agents/` as the authored canonical source home, separate from generated native roots | none | none |
| PROVIDER-CAPABILITY-MATRIX-R22 | Unknown or unsafe entries | Required: fail closed | none | none |
| PROVIDER-CAPABILITY-MATRIX-R23 | Unknown or unsafe entries | Required: preserve them for review | none | none |
| PROVIDER-CAPABILITY-MATRIX-R24 | Canonical files | Forbidden: deleting or quarantining them as stale projections | none | none |

#### Authority Namespaces

| Namespace | Owns | Does not own |
| --- | --- | --- |
| `.agents/governance`, roles, and skills | shared behavior, workflow, approval, role separation, reusable procedures | provider syntax or document profiles |
| Stage 99 Registry | document paths, profiles, identifiers, lifecycle values, and template mappings | agent workflow or provider runtime translation |
| Provider Registry | provider identities, projection routes, model/permission translations, semantic events, and hook commands | shared workflow, retry, evidence, or stop policy |
| Authored native `provider.md` | provider loading and syntax differences | shared governance or model policy |
| Generated native files and runtime controls | provider configuration consuming the owners above | independent shared authority |

| Capability | Canonical owner | Claude adapter | Codex adapter |
| --- | --- | --- | --- |
| Role intent | `.agents/roles/*.md` | `.claude/agents/*.md` | `.codex/agents/*.toml` |
| Procedures | `.agents/skills/*/SKILL.md` | thin generated `.claude/skills/*/SKILL.md` | canonical native skill discovery and explicit reads |
| Explicit invocation | skill-local control and shared approval | `disable-model-invocation: true` | `agents/openai.yaml`: `policy.allow_implicit_invocation: false` |
| Model and effort | Provider Registry | native model and effort | native model and reasoning |
| Permissions | role plus Provider Registry | permission mode | sandbox mode |
| Spawned reviewer read-only enforcement | Review Risk in `workflows.md` | tool allowlist of the generated reviewer agent; a spawned reviewer was observed with no write or shell tool and a refused sensitive read (SPEC-0212 TSK-0079) | on 0.169.0 a spawned reviewer keeps its parent's sandbox despite `sandbox_mode = "read-only"`; a read-only parent enforces it |
| Semantic events | Registry plus native hook config | Claude adapter | Codex adapter |

Native skill frontmatter uses `name`, `description`, and nested governance
`metadata`; the folder, name, and stable function identity agree. Discovery is
not invocation or approval. No skill adds tool grants or installers.

`.agents/` is the authored canonical source home, separate from generated native
roots. Unknown or unsafe entries fail closed and are preserved for review;
canonical files are never deleted or quarantined as stale projections.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](../../docs/00.workspace/02.process/approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

Provider-native files may narrow behavior to actual capabilities. They cannot
invent shared policy, roles, skills, approvals, or unsupported parity. A documented capability, configured source, observed runtime result, and
hard-enforced control are separate facts. A configured event or discoverable
source proves tracked configuration, not a live event or picker result. Runtime
acceptance remains distinct from repository support. Account or subscription
limits remain unknown until directly observed. Git hooks, provider hooks, editor
actions, and CI are separate surfaces; an editor action requires its observed
version and action ID.

### Limits

The policy names no check for any rule in Requirements.

- Authority namespaces (R1-R10): no check is named.
- Capability ownership (R11-R16): no check is named.
- Native skills (R17-R20): no check is named.
- Canonical source (R21-R24): no check is named.
- Enforcement gap: a configured event or discoverable source proves tracked configuration only, and runtime acceptance and account or subscription limits stay unknown until directly observed.
- Rules stated under Enforcement (Mechanisms) are outside this table.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](../../docs/00.workspace/02.process/approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Provider registry](providers/registry.yaml)
- [Agentic policy](agentic.md)
- [Claude adapter](../../.claude/provider.md)
- [Codex adapter](../../.codex/provider.md)
