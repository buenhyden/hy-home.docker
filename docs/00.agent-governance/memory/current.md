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
- The user directed on 2026-08-19 that Spec 137 route 3 be amended for the
  gate-4 scanner contradiction, that the gate 9 operand question be taken up
  first, and that the disposition-type gap be resolved.

## Active boundary

- This unit covers the Spec 137 amendment, the gate evidence it changes, and the
  merge consolidation record. It does not migrate Spec 137's Stage 04 evidence
  into the converged co-located layout.
- The retiring pack stays at its original path under its deletion gates.
- Editing the successor research pack is outside this unit, so a claim needing a
  successor leaf is recorded as an open row rather than moved.

## Verified state

- Verified commit: `2004db0a`
- Verified at: `2026-08-19`
- Spec 137 carries `### Route-3 and disposition-vocabulary amendment`: the
  gate-4 scanner's own scan target is carved out of route 3's
  removal-on-completion condition, route 3's operand test is evaluated per
  mechanism, and a fifth disposition `carry` is defined and bound to
  pre-deletion gate 2 so it cannot fall outside gates 2 and 3.
- The migration ledger measures 231 rows, 11 columns, 0 empty cells, with
  dispositions 66 `Retain`, 27 `Carry`, 39 `Correct`, 15 `Supersede`, 84 `Omit`.
  The relabelling invalidated no review verdict because all 28 affected rows
  carried `Not Run`.
- Gate 4 measures `failures=40`, `clickable_links=0`,
  `unallowlisted_literals=0`, `forbidden_class_literals=0`, 30 reviewed and 10
  unreviewed allowlist rows.
- `check-repo-contracts.sh` measures 10 failing subjects and 595 findings.
- All 66 merge conflicts were resolved with per-file verification. The gated
  retiring pack is intact at 20 files.

## Blockers and unverified facts

- Gate 4's only remaining blocking condition is the 10 unreviewed allowlist
  rows; every literal now has a declared route. An independent allowlist
  re-review is required and has not run.
- Gate 1's second half and gate 3 stay NOT SATISFIED because all 68 sweep rows
  carry `Not Run`. Two review seats dispatched for these terminated on a
  transient provider `529` and need re-dispatch.
- Gate 2 stays unsatisfied on one row: `ai-agent-catalogs.md` upstream-practice
  research is barred from `carry` and needs `retain` into a successor leaf,
  which is outside this unit's boundary.
- `check-document-metadata.py --mode check-changed` reports 12 violations on the
  Spec 137 Spec and Task. Their frontmatter is unchanged, so all 12 are the
  pre-existing four-digit-identity and co-located-Task debt owned by the
  remaining taxonomy slices.
- The taxonomy migration is complete through Task 10D. Slices 10E, 10F and 10G
  remain. Their contract debt dominates the remaining findings: broken links
  pointing at pre-migration paths, of which 138 have multiple candidate targets
  and were deliberately left unresolved, and validator existence assertions that
  must be rewritten against the converged catalog rather than bulk-substituted.
- `docs/90.references/llm-wiki/` holds both `llm-wiki-index.md` and
  `ref-0082-llm-wiki-index.md` at different sizes, so a generated index exists
  under both the pre-migration and converged names and only the converged name
  is excluded from the English-only surface rule. Out of scope here; it belongs
  to the taxonomy slices.
- `scripts/validation/check-doc-traceability.sh` no longer exists; the branch
  consolidated the document governance validators into
  `scripts/lib/document_governance/`.
- Both `.worktrees/` trees are removed and both branches deleted. Their commits
  stay reachable through `preserve/rebuild-finish`, `preserve/taxonomy-final`,
  and `pre-taxonomy-merge-main`.
- `main` is ahead of `origin/main`; nothing has been pushed.

## Evidence links

- [Spec 137 rebuild Task](../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
- [Spec 136 taxonomy convergence](../../03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md)
- [Operations catalog migration ledger](../../98.archive/migrations/mig-0002-operations-catalog-convergence.md)
- [Spec 136 migration branch preservation](./spec-136-migration-branch-preservation.md)
- [Worktree consolidation record](./worktree-consolidation-2026-08-18.md)

## Next handoff

- Re-dispatch the two independent review seats: the allowlist re-review over the
  10 unreviewed rows including the three withdrawn classifications, the
  three-way `mig-0001` split, and the newly declared route 3 rows; and the
  disposition review over the 68 sweep rows.
- Resume the taxonomy migration at slice 10E, domains 04 through 06.
- The Spec 137 deletion gates stay unsatisfied; the retiring pack must not be
  deleted or relocated until every gate is independently recorded.
