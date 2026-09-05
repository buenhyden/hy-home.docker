---
name: "infra-cross-validate"
description: "Use when a proposed infrastructure diff needs independent read-only cross-file review against architecture, operations, security, and rollback contracts."
metadata:
  title: "infra-cross-validate"
  version: "1.1.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-06"
  function_id: "infra-cross-validate"
  scope: "infra"
  owner_agent: "iac-reviewer"
---

# infra-cross-validate

## Preconditions

Invoke this procedure explicitly. Invocation does not select a role or grant the
owning role's permissions. Use the already selected role's permission profile and
approved Task scope; route to the owner when incompatible.

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

- [IaC reviewer](../../roles/iac-reviewer.md)
- [Drift detector](../../roles/drift-detector.md)
- [Infrastructure validation](../infra-validate/SKILL.md)
