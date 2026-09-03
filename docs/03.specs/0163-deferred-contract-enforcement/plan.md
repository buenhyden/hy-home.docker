---
title: Deferred Contract Enforcement Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0163-PLAN-0001
parent_ids: [SPEC-0163]
created: 2026-09-03
updated: 2026-09-03
---

# Deferred Contract Enforcement Plan

## Objective

Resolve each SPEC-0162 deferred item in its own commit, deciding enforce or
delete on measured evidence rather than on preference.

## Dependencies

- SPEC-0161 retired the legacy corpus that the README skip cited, so the skip's
  stated reason no longer exists and its removal is not blocked.
- SPEC-0162 made `--profile full` the route that decides, so a rule wired in
  here is reachable from the documented verification command.

## Execution Sequence

1. Fix the two documents that fail once the README section check covers them.
   Verify: 0 of 149 tracked READMEs are missing a required section.
2. Read sections from the classified profile instead of `readme`, removing the
   skip. Verify: one document per profile reports when a required heading is
   deleted, nine profiles out of nine.
3. Union `common.globally_forbidden` into each record's forbidden set. Verify:
   the three declared keys report `forbidden-key`; an arbitrary key still
   reports `type-inappropriate-key`.
4. Carry the archive contract violation to the operator as a finding with its
   path. Verify: a body pasted into a tombstone names the file and exits 1.

## Risk and Rollback

Each step is one commit with a green full gate. Step 2 is the widest: it puts
131 documents under a check for the first time, which is why step 1 precedes it
and why the impact was measured as exactly 2 failures before either was written.

Step 3 chose enforcement over deletion. The risk is enforcing a contract nothing
needed; the evidence against that is that the alternative check reports a
retired key and a typo identically, which is information the declaration
preserves.

## Verification

`python3 scripts/validation/run-ci-gate.py --profile full` after every step,
plus a negative test per contract.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-deferred-items.md)
