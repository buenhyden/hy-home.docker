---
layer: agentic
---

# Memory: Ignored SDD Scratch Deletion Breaks Cited Advisory Inputs

- Date: 2026-08-11
- Layer: agentic
- Status: active
- Applies To: `.superpowers/sdd/`, Stage 04 Task input tables, agent workspace cleanup
- Tags: destructive-action, git-ignored-scratch, dangling-evidence, out-of-scope-breakage
- Retrieval Keywords: superpowers, sdd, scratch, rm -rf, git-ignored, SHA-256, advisory input, worktree cleanup
- Last Verified: 2026-08-11

## Problem

An agent working the 2026-08-11 research pack source refresh deleted
`.superpowers/` in the `codex/agentic-research-rebuild` worktree while trying to
remove an empty scratch directory it had just created. The directory was not
empty and did not belong to the active unit: it held the entire subagent-driven
development working set of the prior 2026-08-08 rebuild plan.

Three of the deleted files are cited by SHA-256 in the Inputs table of
`docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`:
`vv-external-research-report.md`, `vv-workspace-audit-report.md`, and
`vv-leaf-blueprint.md`. Those citations are now dangling; the recorded digests
can never be re-satisfied.

## Context

`git check-ignore -v .superpowers/sdd` returns non-ignored, which reads as "safe
to delete" at a glance. The actual ignore rule lives in `.superpowers/sdd/.gitignore`
and ignores that directory's children, not the directory itself. So the contents
were untracked and unrecoverable from Git objects while the probed path looked
tracked-clean.

Recovery was attempted and failed. The main checkout at
`/home/hy/projects/hy-home.docker/.superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/`
exists but does not contain the three cited files. The sibling
`sdlc-taxonomy-convergence` worktree does not contain them either. No trash or
snapshot layer exists on this WSL2 filesystem.

The deletion was executed in the same shell invocation as the `find` that listed
the contents, so the listing could not gate the removal.

## Resolution

The loss is bounded but real:

- Review diff packages are reconstructible, because every commit SHA is recorded
  in the tracked Task ledger and the objects remain in Git.
- Task briefs and implementer reports are approximately reconstructible from the
  tracked Plan and Task.
- The three cited advisory reports are unrecoverable. Each is labeled in the
  Task's own Inputs table as advisory input only and explicitly not durable
  authority, so no durable evidence claim depends on their bytes.

The user approved recording this breakage as a Memory note and continuing the
approved refresh, rather than pausing to attempt reconstruction.

## Prevention

- Never probe deletion safety with `git check-ignore` on a parent directory. A
  nested `.gitignore` inverts the result you expect.
- Never combine listing and removal in one shell invocation. Inspect the target
  in one call, decide, then remove in a separate call.
- Treat `.superpowers/sdd/<plan-name>/` as owned by that plan. Only the plan's
  own controller may delete its directory, and only after that plan's final
  review is clean.
- Prefer the session scratchpad for a new unit's scratch artifacts when the
  repository does not track an ignore rule for the tool's default workspace.

## Evidence

- Deleted path: `.worktrees/codex-agentic-research-rebuild/.superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/`
- Dangling citations: `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md` Inputs table rows for the three `vv-*` reports
- Recorded digests that can no longer be verified:
  `e6df4c9242e0e5bec7779ddb5f025f2bda1a1ed0e5fa198d75fbac22d275d9a5`,
  `5693b4a8dffb57b74e7c9747efba33315912a6d461f5972c62cb98470f628670`,
  `4309a1b80c1c91a57d044b2d728f8289c187ab4394db3ad7c54fd66f9f5d5502`
- Deletion occurred after refresh BASE `0b9bd01b` and after refresh ledger commit `8976824a`

## Related Documents

- [Governance memory index](./README.md)
- [Current project memory](./current.md)
- [Rebuild Task holding the dangling citations](../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
- [Source refresh Task](../../04.execution/tasks/2026-08-11-agentic-research-pack-source-refresh.md)
- [Memory template](../../99.templates/templates/governance/memory.template.md)
