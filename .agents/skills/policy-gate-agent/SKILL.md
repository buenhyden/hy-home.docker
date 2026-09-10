---
name: "policy-gate-agent"
description: "Use when a governed change needs a read-only verdict on canonical ownership, typed contracts, protected-surface approval, and evidence."
metadata:
  title: "policy-gate-agent"
  version: "1.2.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-10"
  function_id: "policy-gate-agent"
  scope: "agentic"
  owner_agent: "rules-engineer"
---

# policy-gate-agent

## Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

The governed change, canonical policy owner, typed contract, and applicable approval evidence must be identifiable.

## Inputs

- Governed change and canonical policy.
- Path authority, precedence, protected-surface approvals, and validation evidence.
- The registered gates that decide the verdict this procedure reports. The typed
  gate DAG in `.github/workflow-contract.yml` owns which gates exist and how they
  compose; the [execution boundary](../../governance/quality-standards.md#4-execution-boundary)
  owns which of them may run locally. Deriving that set by hand invites a verdict
  that no gate actually produced.

## Procedure

1. Resolve the change to exactly one authority profile and identify its owner, contributors, mandatory reviewers, and rollback.
2. Compare the diff with typed metadata, section, lifecycle, provider, and approval obligations without accepting duplicate policy prose.
3. Return a pass or bounded findings with the exact canonical correction owner,
   naming for each finding the gate that produced it and distinguishing a gate
   that passed from one that was skipped, blocked, or never run.

## Outputs

- A policy-gate verdict with evidence, owner, and unresolved approvals.

## Gates

- One canonical authority governs each policy topic.
- Protected changes have explicit approval and review evidence.

## Failure Handling

Fail closed on ambiguous ownership, conflicting policy, unsafe paths, or missing approvals and escalate to the workflow supervisor.

## Related Documents

- [Rules engineer](../../roles/rules-engineer.md)
- Agent governance artifacts contract (`docs/99.templates/registry.json`)
- [Approval boundaries](../../governance/approval-boundaries.md)
- [Documentation index](../../../docs/README.md)
