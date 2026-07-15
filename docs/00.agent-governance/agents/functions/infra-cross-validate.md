---
layer: agentic
artifact_type: agent-function
function_id: infra-cross-validate
scope: infra
status: active
---

# infra-cross-validate

## Preconditions

A proposed infrastructure diff, declared runtime contract, and static validation evidence must be available for independent review.

## Inputs

- Proposed infrastructure diff and declared runtime contract.
- Related architecture, operations, security, and rollback constraints.

## Procedure

1. Trace each changed service, network, volume, secret, health, and resource edge across all affected files.
2. Compare the proposal with architecture and operations contracts, distinguishing pre-change static risk from post-change observed drift.
3. Report conflicts and required corrections without applying the infrastructure change.

## Outputs

- Cross-validation findings with exact file evidence and downstream observation needs.

## Gates

- Review remains read-only.
- Cross-file dependencies and declared behavior are mutually consistent.

## Failure Handling

Mark runtime-only questions for `drift-detector` and security-sensitive gaps for `security-auditor`; never infer live state from configuration.

## Related Documents

- [IaC reviewer](../agents/iac-reviewer.md)
- [Drift detector](../agents/drift-detector.md)
- [Infrastructure validation](./infra-validate.md)
