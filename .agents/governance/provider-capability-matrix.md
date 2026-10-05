---
title: "Provider Capability Matrix"
version: "1.2.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
---

# Provider Capability Matrix

## Overview

Canonical agent governance supports exactly Claude and Codex. Capability
documentation separates provider support, repository adoption, and observed
runtime acceptance.

## Scope

Canonical ownership, provider adapters, tracked adoption, and observed runtime capabilities.

## Rules

### Authority Namespaces

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

Provider-native files may narrow behavior to actual capabilities. They cannot
invent shared policy, roles, skills, approvals, or unsupported parity. A documented capability, configured source, observed runtime result, and
hard-enforced control are separate facts. A configured event or discoverable
source proves tracked adoption, not a live event or picker result. Runtime
acceptance remains distinct from repository support. Account or subscription
limits remain unknown until directly observed. Git hooks, provider hooks, editor
actions, and CI are separate surfaces; an editor action requires its observed
version and action ID.

`.agents/` is the authored canonical source home, separate from generated native
roots. Unknown or unsafe entries fail closed and are preserved for review;
canonical files are never deleted or quarantined as stale projections.

## Exceptions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

## Related Documents

- [Provider registry](providers/registry.yaml)
- [Claude adapter](../../.claude/provider.md)
- [Codex adapter](../../.codex/provider.md)
- [Agentic policy](agentic.md)
