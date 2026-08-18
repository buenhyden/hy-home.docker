---
layer: agentic
status: active
---

# Current Project Memory

## Current objective

- Current task: `docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`
- The taxonomy convergence branch is merged into `main`. The active unit is the
  Spec 137 pre-deletion gate track, now running on the converged taxonomy.

## Approved decisions

- The user directed on 2026-08-18 that the `.worktrees` trees be investigated,
  reviewed for resolution, and consolidated, and that
  `codex/sdlc-taxonomy-convergence` be merged and the repository organised in
  that worktree's direction.
- When the merge was found to remove the deletion-gated retiring pack as a side
  effect, the user chose to restore the pack and complete the merge, keeping the
  nine pre-deletion gates in force.
- The user chose to absorb the rebuild-finish branch's two memory notes together
  with its deferred-paths contract and stop-gate fix, and to retire the rest.

## Active boundary

- This unit covers the merge commit, its conflict resolutions, and the
  consolidation record. It does not migrate Spec 137's Stage 04 evidence into
  the converged co-located layout.
- The retiring pack stays at its original path under its deletion gates.

## Verified state

- Verified commit: `e2a93538` (merge `5afdd277`, absorption `e2a93538`)
- Verified at: `2026-08-18`
- All 66 merge conflicts were resolved with per-file verification: 19
  modify/delete and 47 both-modified. The gated retiring pack is intact at 20
  files, and this Task's migration ledger is intact at 231 rows, 11 columns,
  0 empty cells.
- Gate 4's hard counters hold: `clickable_links=0` and
  `forbidden_class_literals=0`.
- The merged repository-harness inventory measures 110 uniquely routed
  artifacts, which is neither side's recorded value.

## Blockers and unverified facts

- Gate 4 reports `failures=255`, of which 246 are `OLD-PATH-UNALLOWLISTED`. The
  34-row allowlist keys on file paths and roughly 1,128 files moved, so its keys
  no longer match. Reconciling it is required before deletion.
- `check-repo-contracts.sh` reports 13 failing subjects, dominated by
  cross-links that point at pre-migration paths, plus one Korean-text finding on
  a closed English-only surface.
- `AGC-MEMORY-BOUNDS` fails because the converged contract expects a Task
  co-located with its spec, while Spec 137's Task remains under
  `docs/04.execution/tasks/`. Migrating it is owned by the remaining taxonomy
  slices, not by this unit.
- `scripts/validation/check-doc-traceability.sh` no longer exists; the branch
  consolidated the document governance validators into
  `scripts/lib/document_governance/`.
- The taxonomy migration is complete through Task 10D. Slices 10E, 10F and 10G
  remain.
- Both `.worktrees/` trees are removed and both branches deleted. Their commits
  stay reachable through `preserve/rebuild-finish`, `preserve/taxonomy-final`,
  and `pre-taxonomy-merge-main`.

## Evidence links

- [Spec 137 rebuild Task](../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
- [Spec 136 taxonomy convergence](../../03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md)
- [Operations catalog migration ledger](../../98.archive/migrations/mig-0002-operations-catalog-convergence.md)
- [Spec 136 migration branch preservation](./spec-136-migration-branch-preservation.md)
- [Worktree consolidation record](./worktree-consolidation-2026-08-18.md)

## Next handoff

- Reconcile the gate 4 allowlist against the converged paths, then repair the 13
  failing contract subjects.
- Resume the taxonomy migration at slice 10E, domains 04 through 06.
- The Spec 137 deletion gates stay unsatisfied; the retiring pack must not be
  deleted or relocated until every gate is independently recorded.
