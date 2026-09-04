---
title: "Provider Capability Matrix"
version: "1.0.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
---

# Provider Capability Matrix

Stage 00 supports exactly Claude and Codex. Capability documentation separates
provider support, repository adoption, and observed runtime acceptance.

## Authority Namespaces

| Namespace | Owns | Does not own |
| --- | --- | --- |
| Stage 00 policies, roles, and skills | shared behavior, workflow, approval, role separation, reusable procedures | provider syntax or document profiles |
| Stage 99 Registry | document paths, profiles, identifiers, lifecycle values, and template mappings | agent workflow or provider runtime translation |
| Provider Registry | provider identities, projection routes, model/permission translations, semantic events, and hook commands | shared workflow, retry, evidence, or stop policy |
| Native runtime files | tracked provider configuration that consumes the owners above | independent governance authority |

| Capability | Canonical owner | Claude adapter | Codex adapter |
| --- | --- | --- | --- |
| Role intent | `roles/*.md` | `.claude/agents/*.md` | `.codex/agents/*.toml` |
| Procedures | `skills/*.md` | `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` |
| Model and effort | provider registry | native model and effort | native model and reasoning |
| Permissions | role plus provider registry | permission mode | sandbox mode |
| Semantic events | registry plus hook config | Claude adapter | Codex adapter |

Provider-native files may narrow behavior to actual capabilities. They may not
invent policy, roles, skills, approvals, or unsupported parity. A configured
event is tracked adoption, not proof that a live event ran. Runtime acceptance
remains distinct from configured repository support.

## Related Documents

- [Provider registry](../providers/registry.yaml)
- [Claude adapter](../providers/claude.md)
- [Codex adapter](../providers/codex.md)
- [Agentic policy](./agentic.md)
