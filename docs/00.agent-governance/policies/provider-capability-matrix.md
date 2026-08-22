---
profile_id: governance-policy
layer: agentic
---

# Provider Capability Matrix

Stage 00 supports exactly Claude and Codex. Capability documentation separates
provider support, repository adoption, and observed runtime acceptance.

| Capability | Canonical owner | Claude adapter | Codex adapter |
| --- | --- | --- | --- |
| Role intent | `roles/*.md` | `.claude/agents/*.md` | `.codex/agents/*.toml` |
| Procedures | `skills/*.md` | `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` |
| Model and effort | provider registry | native model and effort | native model and reasoning |
| Permissions | role plus provider registry | permission mode | sandbox mode |
| Semantic events | registry plus hook config | Claude adapter | Codex adapter |

Provider-native files may narrow behavior to actual capabilities. They may not
invent policy, roles, skills, approvals, or unsupported parity. A configured
event is tracked adoption, not proof that a live event ran.

## Related Documents

- [Provider registry](../providers/registry.yaml)
- [Claude adapter](../providers/claude.md)
- [Codex adapter](../providers/codex.md)
- [Agentic policy](./agentic.md)
