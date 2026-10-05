---
name: "infra-cross-validate"
description: "Use when a proposed infrastructure diff needs independent read-only cross-file review against architecture, operations, security, and rollback contracts."
metadata:
  title: "infra-cross-validate"
  version: "1.2.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-10-05"
  function_id: "infra-cross-validate"
  scope: "infra"
  owner_agent: "iac-reviewer"
---

# infra-cross-validate

## Purpose

### Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

A proposed infrastructure diff, declared runtime contract, and static validation evidence must be available for independent review.

## Inputs

- Proposed infrastructure diff and declared runtime contract.
- Related architecture, operations, security, and rollback constraints.

## Procedure

1. Trace each changed service, network, volume, secret, health, and resource edge across all affected files.
2. Compare the proposal with architecture and operations contracts, distinguishing pre-change static risk from post-change observed drift.
3. When persistent state or recovery changes, route the sanitized recovery contract through [stateful recovery contract review](../stateful-recovery-contract-review/SKILL.md) before any operational recommendation.
4. Report conflicts and required corrections without applying the infrastructure change.

### Gates

- Review remains read-only.
- Cross-file dependencies and declared behavior are mutually consistent.
- A recovery-readiness verdict never authorizes or reports an operational restore.

## Outputs

- Cross-validation findings with exact file evidence, downstream observation needs, and any separate recovery-readiness verdict.

## Failure Handling

Mark runtime-only questions for `drift-detector` and security-sensitive gaps for `security-auditor`; never infer live state from configuration. Keep recovery readiness blocked when its required contract facts are missing.

## References

- [IaC reviewer](../../roles/iac-reviewer.md)
- [Drift detector](../../roles/drift-detector.md)
- [Infrastructure validation](../infra-validate/SKILL.md)
- [Stateful recovery contract review](../stateful-recovery-contract-review/SKILL.md)
