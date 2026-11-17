---
title: "Provider Capability Matrix"
version: "1.3.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
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
| PROVIDER-CAPABILITY-MATRIX-R1 | Always | Required: keep each authority namespace to what it owns (governance/roles/skills, Stage 99 Registry, Provider Registry, authored `provider.md`, generated native files) | none | none |
| PROVIDER-CAPABILITY-MATRIX-R2 | Always | Required: map each capability (role intent, procedures, explicit invocation, model and effort, permissions, semantic events) to its canonical owner and adapters | none | none |
| PROVIDER-CAPABILITY-MATRIX-R3 | Native skill frontmatter | Required: use `name`, `description` and nested governance `metadata` | none | none |
| PROVIDER-CAPABILITY-MATRIX-R4 | Native skills | Required: folder, name and stable function identity agree | none | none |
| PROVIDER-CAPABILITY-MATRIX-R5 | Always | Forbidden: treating discovery as invocation or approval | none | none |
| PROVIDER-CAPABILITY-MATRIX-R6 | Always | Forbidden: a skill adding tool grants or installers | none | none |
| PROVIDER-CAPABILITY-MATRIX-R7 | Always | Required: keep `.agents/` as the authored canonical source home, separate from generated native roots | none | none |
| PROVIDER-CAPABILITY-MATRIX-R8 | Unknown or unsafe entries | Required: fail closed and preserve them for review | none | none |
| PROVIDER-CAPABILITY-MATRIX-R9 | Always | Forbidden: deleting or quarantining canonical files as stale projections | none | none |

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
| Semantic events | Registry plus native hook config | Claude adapter | Codex adapter |

Native skill frontmatter uses `name`, `description`, and nested governance
`metadata`; the folder, name, and stable function identity agree. Discovery is
not invocation or approval. No skill adds tool grants or installers.

`.agents/` is the authored canonical source home, separate from generated native
roots. Unknown or unsafe entries fail closed and are preserved for review;
canonical files are never deleted or quarantined as stale projections.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

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

The policy names no check for its rules, so they rest on review and provider behavior:

- Authority namespaces: R1.
- Capability ownership: R2.
- Native skills: R3-R6.
- Canonical source: R7-R9.
- Provider-native files may narrow behavior only to actual capabilities; this rests on review.
- Configured sources and events prove tracked configuration only, not live events or picker results.
- Runtime acceptance, account or subscription limits and editor action versions need direct observation.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Provider registry](providers/registry.yaml)
- [Agentic policy](agentic.md)
- [Claude adapter](../../.claude/provider.md)
- [Codex adapter](../../.codex/provider.md)
