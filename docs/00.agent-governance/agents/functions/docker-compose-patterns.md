---
layer: agentic
artifact_type: agent-function
function_id: docker-compose-patterns
scope: infra
status: active
---

# docker-compose-patterns

## Preconditions

Compose requirements and workspace conventions must identify whether the task is local composition, availability design, or deployment planning.

## Inputs

- Compose requirements and workspace conventions.
- Service topology, statefulness, routing, health, resource, and secret constraints.

## Procedure

1. Classify the workload and eliminate patterns that violate state, network, volume, or host constraints.
2. Select the simplest Compose pattern that satisfies dependency, health, isolation, and operability requirements.
3. Record trade-offs and validation obligations without presenting orchestrator-only behavior as native Compose capability.

## Outputs

- A Compose pattern selection with rationale and validation requirements.

## Gates

- Selected YAML and Compose features are schema-valid.
- The pattern matches repository naming, secret, network, and lifecycle rules.

## Failure Handling

Escalate to architecture design when no Compose-native pattern meets the requirement; do not simulate unsupported deployment guarantees.

## Related Documents

- [Infrastructure implementer](../agents/infra-implementer.md)
- [Compose stack function](./compose-stack-agent.md)
- [Infrastructure scope](../../scopes/infra.md)
