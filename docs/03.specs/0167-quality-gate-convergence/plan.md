---
title: Quality Gate Convergence Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0167-PLAN-0001
parent_ids: [SPEC-0167]
created: 2026-09-03
updated: 2026-09-03
---

# Quality Gate Convergence Plan

## Objective

Make the declared quality configuration and the executed quality gate describe
the same repository.

## Dependencies

- Routing the lint gate into CI is only safe once the corpus passes it. The
  local hook sees changed files only, so violations accumulate unseen in files
  nobody has touched. Measure the whole corpus before routing.
- The measurement must use the pinned hook revisions, not whatever version is
  installed on this machine; the local `markdownlint-cli2` is a minor version
  ahead of the pin.

## Execution Sequence

1. Reconcile the configuration files with the tree. Verify: every remaining
   path exists; each removal is backed by a measured finding count.
2. Break the orchestration cycle in the CI entrypoint and route
   `leaf.pre-commit` through the changed-profile fallback suite. Verify: a CI
   plan contains it, a local plan does not, in every execution context.
3. Remove the gate nodes no plan can execute, and prune the env allowlist to
   the keys nodes declare. Verify: the contract tests assert equality rather
   than a literal copy.
4. Run the approved all-files wrapper and clear whatever backlog it reports.
   Verify: a clean run under the pinned revisions.

## Risk and Rollback

Step 2 is the one that changes what CI does. Its failure mode is a red gate on
`main`, not data loss, and it reverts as a single commit. Step 4 is where the
real uncertainty lives: the size of the accumulated backlog is unknown until
the wrapper runs, and a rule that cannot be auto-fixed needs a judgment call
rather than a formatter.

Step 1 carries a quieter risk: removing an ignore can expose content that was
being hidden for a reason no longer written down. Each removal is therefore
measured before it is made.

## Verification

`python3 scripts/validation/run-ci-gate.py --profile full` after every step,
plus `scripts/validation/run-agent-precommit-all-files.sh` once at step 4.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-quality-gate-convergence.md)
