---
title: "AI Agent Identity Routing"
version: "1.0.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
---

# AI Agent Identity Routing

Before mutation, resolve exactly one canonical `agent_id` from `roles/`. Use its
scope, permission profile, work profile, and skill IDs without inventing a
provider-local identity. Provider-native adapters preserve role intent but do
not own names, permissions, or model policy.

If no role matches or multiple roles conflict, stop and route the ambiguity to
`workflow-supervisor`. Multi-role work keeps one supervising owner and separates
implementation from independent review.

## Related Documents

- [Roles](../roles/)
- [Provider registry](../providers/registry.yaml)
- [Bootstrap policy](bootstrap.md)
- [Agentic policy](./agentic.md)
