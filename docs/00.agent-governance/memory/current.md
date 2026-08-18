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

- Verified commit: `a89c101d`
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

- Both independent review seats have now run and both returned Needs fixes.
  Their verdicts and this Task's re-derivation of the load-bearing measurements
  are recorded in the Task's Review Evidence.
- Gate 4 has three open blockers, not one. Route 1 is met by no allowlist row,
  because it requires a claim-ledger disposition the ledger has no slot to give
  and the 2026-08-18 amendment rejected the vacuity reading without changing
  route 1. The scanner keys allowlist rows by path at
  `scripts/validation/old_path_gate_contract.py:422`, so a split row collapses to
  its last member and the exactly-one-route requirement is unenforceable there.
  Three rows declare a class the table marks withdrawn. Six of the twelve
  unsettled rows do settle, including all three route 3 declarations.
- Gate 2 is unsatisfied on forty rows, not one. Besides the mis-dispositioned
  `ai-agent-catalogs.md` row, the 39 sweep rows labelled `Retain` or `Correct`
  name the Task file as their own destination. The 2026-08-19 `carry` amendment
  reached the other class exhibiting the same defect and not these, and they
  cannot be relabelled as they stand because none states per-claim uniqueness or
  a remediation owner, and at least 13 need a successor leaf this unit may not
  create.
- Gate 1 fails on coverage as well as on review: an unresolved Mythos Preview
  lifecycle conflict has no ledger row, and the vendor catalog's `Caveat` column
  was never swept as a claim family.
- `check-document-metadata.py --mode check-changed` reports 12 violations on the
  Spec 137 Spec and Task. Their frontmatter is unchanged, so all 12 are the
  pre-existing four-digit-identity and co-located-Task debt owned by the
  remaining taxonomy slices.
- The taxonomy migration is complete through Task 10D. Slices 10E, 10F and 10G
  remain. Their contract debt dominates the remaining findings: broken links
  pointing at pre-migration paths, of which 138 have multiple candidate targets
  and were deliberately left unresolved, and validator existence assertions that
  must be rewritten against the converged catalog rather than bulk-substituted.
- The LLM Wiki duplication is contract-converged but not code-converged. The
  merge left two generator families alive; `scripts/manifest.yaml` registers only
  `generate-llm-wiki.py`, which now carries the ported retiring-pack exclusion,
  and the two shell generators are recorded as `lifecycle: transition`,
  `disposition: merge`, successor `generate-llm-wiki.py`. All four generated
  outputs were STALE and now pass. Deletion is deferred because the shell pair is
  the only implementation of the gate 9 sealed internal-manifest protocol that
  `agentic-research-gate9-evidence.py` consumes, proven by a dedicated regression
  module; the Python generator implements only `--check` and `--write`.
  `tests/validation/test_generate_llm_wiki.py` still fails on 43 versus 45
  tracked scripts and will stay failing until that pair is deleted.
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

- Decide the two route-level questions the seats surfaced: whether route 1 is
  amended or every row admitted under it is re-routed, and whether the gate 4
  scanner keys allowlist rows on path plus anchor so a split row survives.
- Decide how the 39 self-referential sweep rows reach a real destination, given
  that 13 of them need a successor leaf outside this unit's boundary.
- Resume the taxonomy migration at slice 10E, domains 04 through 06.
- The Spec 137 deletion gates stay unsatisfied; the retiring pack must not be
  deleted or relocated until every gate is independently recorded.
