---
name: "docker-compose-patterns"
description: "Use when workload requirements need a Compose-native topology and configuration pattern consistent with repository constraints."
metadata:
  title: "docker-compose-patterns"
  version: "1.2.1"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-13"
  function_id: "docker-compose-patterns"
  scope: "infra"
  owner_agent: "infra-implementer"
---

# docker-compose-patterns

## Purpose and Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

Compose requirements and workspace conventions must identify whether the task is local composition, availability design, or deployment planning.

### When Not to Use

A requirement that no Compose-native pattern meets is outside this skill; it escalates to architecture design.

## Procedure

### Steps

1. Classify the workload and eliminate patterns that violate state, network, volume, or host constraints.
2. Select the simplest Compose pattern that satisfies dependency, health, isolation, and operability requirements.
3. Record trade-offs and validation obligations without presenting orchestrator-only behavior as native Compose capability.

#### Gates

- Selected YAML and Compose features are schema-valid.
- The pattern matches repository naming, secret, network, and lifecycle rules.

### Failure Handling

Escalate to architecture design when no Compose-native pattern meets the requirement; do not simulate unsupported deployment guarantees.

## Inputs and Outputs

### Inputs

- Compose requirements and workspace conventions.
- Service topology, statefulness, routing, health, resource, and secret constraints.

### Outputs

- A Compose pattern selection with rationale and validation requirements.

## Verification

### Checks

- `scripts/validation/validate-docker-compose.sh` accepts the selected YAML and Compose features.
- The chosen pattern follows the repository naming, secret, network, and lifecycle rules, with any exception recorded.
- Behavior that needs an orchestrator is labelled as not native to Compose.

### Completion and Handoff

Owning role, policies and related documents:

- [Infrastructure implementer](../../roles/infra-implementer.md)
- [Compose stack function](../compose-stack-agent/SKILL.md)
- [Infrastructure scope](../../governance/environment-constraints.md)
