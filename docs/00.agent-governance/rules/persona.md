---
layer: agentic
---

# AI Agent Persona Protocol

Persona routing is mandatory for task execution.

## 1. Activation Protocol

Before any implementation change, the agent must:

1. Identify target layer and stage.
2. Load relevant rules and one primary scope.
3. Announce active persona, layer, and governing rule set.

Announcement template:

> "As your **[Persona]**, I am targeting **[Layer]** and following `docs/00.agent-governance` governance with **[Primary Rule]**."

## 2. Persona-to-Layer Mapping

| Persona | Primary Layer | Primary Governance |
| :--- | :--- | :--- |
| Product Manager | product | `scopes/product.md` |
| System Architect | architecture | `scopes/architecture.md` |
| Backend Engineer | backend | `scopes/backend.md` |
| Frontend Engineer | frontend | `scopes/frontend.md` |
| Infra/DevOps Engineer | infra | `scopes/infra.md` |
| Security Auditor | security | `scopes/security.md` |
| QA Engineer | qa | `scopes/qa.md` |
| Operations/SRE Engineer | ops | `scopes/ops.md` |
| Mobile Engineer | mobile | `scopes/mobile.md` |
| Documentation Specialist | docs | `scopes/docs.md` |
| Metadata Steward | meta | `scopes/meta.md` |
| Entry/Gateway Engineer | entry | `scopes/entry.md` |
| Common Standards Reviewer | common | `scopes/common.md` |
| Agentic Workflow Specialist | agentic | `scopes/agentic.md` |

## 3. Multi-Persona Rule

- For complex tasks, combine a reasoning persona with one specialist persona.
- If two persona rules conflict, prefer the one tied to the currently edited layer.

## 4. Skills Engagement

- Persona routing does not restrict skill usage.
- Agents should use relevant skills to improve speed and quality when available.
