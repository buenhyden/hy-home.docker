---
title: Validation Blind Spot Closure Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0162-PLAN-0001
parent_ids: [SPEC-0162]
created: 2026-09-03
updated: 2026-09-03
---

# Validation Blind Spot Closure Plan

## Objective

Close each unreachable rule in its own commit, ordered so that a contract is
never registered without the enforcement that makes it real.

## Dependencies

- SPEC-0161 left `registry.json` as the only profile authority, which is what
  makes the `common` contract editable in place rather than frozen in a blob.
- Every measurement runs inside the gate's curated environment, so a probe may
  not depend on an environment variable: `ci_gate_contract.py:1230` strips
  anything outside the allowlist and an env-based probe records nothing.

## Execution Sequence

1. Resynchronize the Stage 03 package index. One wrong status and three absent
   rows. Verify: index rows equal the package tree by set difference.
2. Replace the unreplaced `<title>` in ten hook policies. Verify: no authored
   document carries a template placeholder.
3. Bind the six README profiles to a lifecycle. Verify: every profile that
   allows a status names the state machine that status belongs to.
4. Correct the stale members of `common`, then stop restating the machine
   contract in policy prose. Verify: identity restatements 25 to 1, key
   restatements 22 to 11.
5. Repair `invalid-status`, which was gated on `status == "active"` and so could
   never see a wrong status. Verify: the validated-record count rises with no
   new violations, and a bogus status is reported.
6. Repoint `template-placeholder-in-target` at the vocabulary templates declare.
   Verify: the declared and used token sets are identical.
7. Give `invalid-transition` a committed predecessor in the full route. Verify:
   an illegal transition is reported and a legal one is not.
8. Name the Stage 90 member templates after their roles. Verify: the role source
   binding is enforced, so a missed consumer cannot pass silently.
9. Register the index contract and enforce the missing direction. Verify: one
   row removed from each of four indexes is reported, four times out of four.

## Risk and Rollback

Each step is one commit with a green full gate, so any step reverts alone. The
riskiest is step 5, because it puts 160 previously unvalidated documents under
validation at once; measuring three filter variants before choosing bounded that
risk to a known number.

Step 7 carries a distinct risk: validating history rather than the change
boundary would flag events that predate the contract and can never be repaired.
The plan therefore compares against HEAD and reports history instead.

## Verification

`python3 scripts/validation/run-ci-gate.py --profile full` after every step, plus
a negative test per repaired rule.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-blind-spot-closure.md)
