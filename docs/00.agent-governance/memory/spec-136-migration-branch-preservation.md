---
layer: agentic
---

# Spec 136 migration lives only on an unmerged branch

- Date: 2026-08-17
- Layer: agentic
- Status: active
- Applies To: `docs/03.specs/136-sdlc-taxonomy-convergence/`, `docs/04.execution/`, branch `codex/sdlc-taxonomy-convergence`
- Tags: worktree, migration, taxonomy, unmerged-work, preservation
- Retrieval Keywords: spec 136, sdlc taxonomy convergence, migration ledger, spec-0136, docs/98.archive/migrations, worktree consolidation, ops catalog
- Last Verified: 2026-08-17

## Problem

`main` carries Spec 136 at `status: active` and its Plan
`docs/04.execution/plans/2026-08-07-sdlc-taxonomy-convergence.md` at
`status: active`, but no Task and no implementation. A reader on `main` sees an
approved, in-force taxonomy migration with no trace of execution and can
reasonably conclude the work was never started, or start it again from zero.

The execution exists. It is on the unmerged branch
`codex/sdlc-taxonomy-convergence` (tip `cb117edd`), 67 commits ahead of its
merge-base `5d22b5f0` and 134 behind `main`.

## Context

The branch implements Spec 136 on every point the Spec states, including the
later correction that Operations stays Stage 05 rather than being renumbered.
Its scope is 1,128 files: 626 renames, 263 modifications, 160 deletions, 76
additions. The scheme moves specs to `spec-NNNN-slug`, co-locates Plan and Task
inside the owning spec folder, removes `docs/04.execution/` entirely, introduces
`docs/05.operations/catalog/<NN-domain>/ops-NNNN-*`, flattens dated research
paths to `ref-NNNN-slug`, and adds `docs/98.archive/{migrations,tombstones}/`.

Two artifacts exist nowhere else. `docs/98.archive/migrations/` is absent from
`main` altogether, and it holds `mig-0001-sdlc-taxonomy-convergence.md` and
`mig-0002-operations-catalog-convergence.md`, roughly 9,600 lines that are the
provenance ledger Spec 136 asks for. The `docs/05.operations/catalog/`
structure with its 13 domain indexes is also branch-only.

Three reasons block a merge in the branch's current shape:

1. The work is incomplete by its own accounting. The tip commit covers
   operations domains 00 through 03, and the branch's own current-memory record
   names domains 04 through 06 as the next slice with two further slices
   reserved. Roughly four of seven slices are done.
2. The branch deletes `docs/04.execution/`, and `main` has since added four
   documents into that tree plus further dated research and spec paths. Every
   one of them would surface as an add/delete conflict and would need migrating
   under the branch's own convention.
3. A research-pack identity clash runs the wrong way. The branch's `ref-0039`
   through `ref-0058` are renames of the **retiring** 2026-07-05 pack, because
   the canonical 2026-08-08 pack did not exist at the branch's merge-base. Its
   copies are stale against `main`'s deepened leaves. Merging naively would
   promote retired content to canonical identities and could revert `main`'s
   2026-08-14 deepening.

Reason 3 also puts this branch in direct tension with
`codex/agentic-research-rebuild-finish`, whose purpose is to delete that same
2026-07-05 pack. The two branches both rewrite `docs/04.execution/` and cannot
be integrated in parallel.

## Resolution

The user decided on 2026-08-17 to preserve the branch and hold it outside the
active session's boundary rather than merge, rebase, or discard it.

The branch and its worktree at `.worktrees/sdlc-taxonomy-convergence` stay in
place. Its three working-tree modifications were copied to durable storage
outside the repository before any other worktree action, because they are not
backed by a Git object. Those three files are a single bookkeeping closure:
each flips Task 10D from `FINAL_APPROVED_UNCOMMITTED` to committed and records
`cb117edd`.

By contrast, `codex/agentic-research-generated-freshness` was removed in the
same session after three preconditions were each verified: a clean tree
including untracked files, content that is a strict subset of `main`'s later
regeneration, and the commit surviving as an ancestor of another branch.
Nothing comparable holds for this branch, which is why the dispositions differ.

## Prevention

- Read `main`'s active Spec and Plan status together with the branch list before
  concluding that an approved migration was never executed. An active Spec with
  an active Plan and no Task is a signal to look for unmerged execution, not a
  signal to restart.
- Copy Git-unbacked working-tree files to durable storage before any git
  operation touches a worktree. This branch's sibling already lost a comparable
  protected set to a reviewer checkout; see the linked note.
- Sequence the two competing branches. Settle the deletion-authority question
  first, then replay this migration onto the resulting `main`. Replaying is the
  viable route; merging the branch as-is is not, for the three reasons above.
- When resuming, re-derive the remaining slice scope independently rather than
  trusting the branch's own status fields, and re-pin the research-pack
  identities against the canonical 2026-08-08 pack instead of the retiring one.
- One recovery input for a completed merge step is a `/tmp` archive that will
  not survive a reboot. Treat it as already gone and re-derive if that step
  needs auditing.

## Evidence

- Branch `codex/sdlc-taxonomy-convergence` at `cb117edd`, merge-base
  `5d22b5f0`, 67 ahead and 134 behind `main` at `894920f0`.
- `docs/98.archive/migrations/` resolves on the branch and does not resolve on
  `main`.
- `main`'s Spec 136 changed only by whitespace realignment since the merge-base,
  so the branch is not diverging from a moved target.
- The rename detection that established reason 3 shows the retiring pack's
  leaves mapping to `ref-00NN` identities, with the branch copies shorter than
  `main`'s deepened equivalents.
- Preserved working-tree copies live under a dated preservation directory in the
  user's home, outside the repository and outside Git.

## Related Documents

- [Governance memory index](./README.md)
- [Current project memory](./current.md)
- [Prior loss of protected dirty files](./ignored-sdd-scratch-deletion.md)
- [Spec 136](../../03.specs/136-sdlc-taxonomy-convergence/spec.md)
- [Spec 136 Plan](../../04.execution/plans/2026-08-07-sdlc-taxonomy-convergence.md)
