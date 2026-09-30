---
name: "stateful-recovery-contract-review"
description: "Use when an explicitly supplied sanitized stateful recovery contract needs read-only readiness review before any separate recovery approval."
metadata:
  title: "stateful-recovery-contract-review"
  version: "0.1.0"
  type: "governance/skill"
  status: "draft"
  owner: "@buenhyden"
  updated: "2026-09-29"
  function_id: "stateful-recovery-contract-review"
  scope: "infra"
  owner_agent: "iac-reviewer"
---

# stateful-recovery-contract-review

## Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

An authorized reviewer must receive an explicitly supplied, sanitized recovery
contract. This procedure is read-only and does not authorize or perform a
restore, service action, credential access, or secret inspection.

## Inputs

- The sanitized contract facts required by the
  [recovery contract matrix](references/recovery-contract.md).
- Named implementer, independent reviewer, and human approver as three distinct
  identities or roles, plus the boundary of the separate operational approval.

## Procedure

1. Compare the supplied facts with every row in the recovery contract matrix.
2. Separate objectives from observations, and record missing or contradictory
   facts without inferring runtime state from configuration, a volume, or a runbook.
3. Complete the [verdict template](assets/verdict.md) with bounded evidence and
   one verdict: `READY_FOR_SEPARATE_RECOVERY_APPROVAL` or `BLOCKED`.

## Outputs

- A read-only readiness verdict with supplied evidence and its source/observation
  time, missing or contradictory inputs, responsible owners, the separate
  operational approval boundary, and distinct static, provider-native, supplied
  historical operational-evidence, and current-action status.

## Gates

- Every required matrix row is supplied and mutually consistent before a ready
  verdict is allowed.
- A volume is not treated as a backup, and rebuild is accepted only when its
  inputs and procedure are provable.
- Static review, native invocation, and successful operational recovery remain
  distinct evidence classes.
- The verdict never approves or reports a restore as executed.
- Implementer, independent reviewer, and human approver are pairwise distinct;
  the reviewer cannot approve the reviewed recovery action.
- Supplied historical recovery evidence never changes the operational action in
  this review from `NOT_RUN`.

## Failure Handling

Return `BLOCKED` with the exact missing or contradictory fields. Stop when the
input includes credential payloads, secret values, unapproved live inspection,
or instructions to execute recovery, and route those actions to the named human
approval boundary.

## Related Documents

- [IaC reviewer](../../roles/iac-reviewer.md)
- [Infrastructure cross-validation](../infra-cross-validate/SKILL.md)
- [Approval boundaries](../../governance/approval-boundaries.md)
