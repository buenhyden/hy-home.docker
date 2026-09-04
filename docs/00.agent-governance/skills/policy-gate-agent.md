---
title: "policy-gate-agent"
version: "1.0.0"
type: "governance/skill"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
function_id: "policy-gate-agent"
scope: "agentic"
owner_agent: "rules-engineer"
---

# policy-gate-agent

## Preconditions

The governed change, canonical policy owner, typed contract, and applicable approval evidence must be identifiable.

## Inputs

- Governed change and canonical policy.
- Path authority, precedence, protected-surface approvals, and validation evidence.

## Procedure

1. Resolve the change to exactly one authority profile and identify its owner, contributors, mandatory reviewers, and rollback.
2. Compare the diff with typed metadata, section, lifecycle, provider, and approval obligations without accepting duplicate policy prose.
3. Return a pass or bounded findings with the exact canonical correction owner.

## Outputs

- A policy-gate verdict with evidence, owner, and unresolved approvals.

## Gates

- One canonical authority governs each policy topic.
- Protected changes have explicit approval and review evidence.

## Failure Handling

Fail closed on ambiguous ownership, conflicting policy, unsafe paths, or missing approvals and escalate to the workflow supervisor.

## Related Documents

- [Rules engineer](../roles/rules-engineer.md)
- [Agent governance artifacts contract](../../99.templates/registry.json)
- [Approval boundaries](../policies/approval-boundaries.md)
