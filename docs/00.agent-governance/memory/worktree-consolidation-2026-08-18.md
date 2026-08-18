---
layer: agentic
---

# Worktree Consolidation and the Two Retired Branches

- Date: 2026-08-18
- Layer: agentic
- Status: active
- Applies To: worktree cleanup, branch retirement, merge safety, deletion gates
- Tags: worktree, merge, data-loss, deletion-gate, taxonomy
- Retrieval Keywords: worktree remove, preserve tag, gated deletion, directory
  rename split, uncommitted work, taxonomy convergence
- Last Verified: 2026-08-18

## Problem

Two long-lived worktrees under `.worktrees/` were consolidated. Both carried
uncommitted work, and one of them carried this repository's own note recording
that unstaged work had previously been destroyed with no recovery route.

Merging the taxonomy branch also turned out to remove a deletion-gated pack as a
side effect, which no participant intended.

## Context

`codex/sdlc-taxonomy-convergence` was 67 commits ahead and 187 behind. It moved
1,128 files while `main` had moved 109, so the true conflict surface was only 66
paths even though a naive reading suggested a rewrite of the whole corpus.

`codex/agentic-research-rebuild-finish` held a gate 9 confined-descriptor
publication mechanism, including a compiled binary, plus a direct-deletion
controller design. Spec 137's decoupling amendment already recorded that the
mechanism gates nothing outside itself, and the controller design was never
adopted.

## What Worked

- **Commit uncommitted work on its own branch before anything destructive.**
  This turned 3,306 unstaged lines and a handoff record into recoverable Git
  objects. Nothing in the consolidation could then lose them.
- **Preview the merge with `git merge-tree` before running it.** It reported the
  conflicting paths and, critically, two `directory rename split` conflicts on
  `docs/04.execution`, which is where the active Task lives.
- **Resolve by evidence, not by side.** Choosing either side wholesale would
  have produced a repository that references files that do not exist, because
  the branch's taxonomy was computed against a corpus `main` had since replaced.
- **Re-measure anything a merge asserts.** A test asserting the harness
  inventory read 116 on one side and 107 on the other; the merged tree measures
  110. Taking either side would have asserted a count true of neither.
- **Tag before and after.** `pre-taxonomy-merge-main`, `preserve/taxonomy-final`
  and `preserve/rebuild-finish` keep every retired commit reachable after the
  branches are deleted.

## What To Watch

- A rename is not safer than a delete when gates bind to paths. The merge
  proposed renaming a deletion-gated pack rather than deleting it, which would
  have broken the migration ledger's blob provenance, the gate 4 allowlist, and
  every tracked path literal while satisfying no gate.
- A path-keyed allowlist does not survive a large move. Gate 4 went from
  `failures=9` to 246 `OLD-PATH-UNALLOWLISTED` purely because its keys are file
  paths and roughly 1,128 files moved.
- Absorb a mechanism without its data. The deferred-paths registry was absorbed
  empty, because its two entries belonged to the unadopted controller design.

## Recovery

- `preserve/rebuild-finish` holds the retired branch, including the gate 9
  object publisher, its C source and compiled artifact, and the direct-deletion
  controller and worker with their tests.
- `preserve/taxonomy-final` holds the taxonomy branch at the state that was
  merged.
- `pre-taxonomy-merge-main` holds `main` immediately before the merge.

## Related Documents

- [Reviewer checkout destroyed dirty state](./reviewer-checkout-destroyed-dirty-state.md)
- [Spec 136 migration branch preservation](./spec-136-migration-branch-preservation.md)
- [Current project memory](./current.md)
