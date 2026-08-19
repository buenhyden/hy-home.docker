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

- The user extended this unit's boundary on 2026-08-19 to edit the successor
  research pack, so claims needing a successor leaf are written directly rather
  than deferred to a later unit.

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

- Verified commit: `82474ca7`
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
- Gate 4 stands at 35 settled and 8 unsettled allowlist rows with `failures=34`.
  It rose to 44 first, when two wrongly settled verdicts were withdrawn, then
  fell as seven rows settled on the seat's own verdict and four took bounded
  edits. Four rows remain admitted under no route and need their owning units
  rather than an edit here: two present-tense canonical-owner statements in
  `Required Behavior` tables, an `Allowed Paths` write grant into the
  deletion-gated directory in an active unit, and a scan-exemption constant.
- Two of the three original gate 4 blockers are closed. Spec 137's `Route-1 admission and
  split-row evaluation amendment` replaces route 1's unsatisfiable claim-ledger
  conjunct with the Spec's own Historical-evidence boundary, and the scanner now
  stores allowlist rows per path as a list and collapses them fail-closed, so a
  split row survives and one unsettled sibling leaves the whole path unreviewed.
  Gate 4 counts all 43 declared rows where it counted 41. What remains open is
  the six unsettled rows the seat would not settle, three of which declare a
  class the table marks withdrawn.
- Gate 2 has no row without a destination. The 39 self-referential sweep rows
  were classified by destination: 22 are repository-state claims, now `Carry`
  with their substance in the carried-claims section; the other 17 plus the
  `ai-agent-catalogs.md` row are source-backed or upstream material written into
  eleven successor leaves. Zero of the 246 ledger rows now name themselves as
  their own destination. What remains is review, not routing.
- Six independent seats re-reviewed the repaired state on 2026-08-19 in six
  batches: the 47 `Carry` rows returned 7 settled / 40 held, and the 54
  successor-leaf rows returned 47 settled / 7 held. Every hold is now closed.
- The owner requirement failed measurement SEVEN times, each differently: a count
  of mentions rather than names; a blanket justification asserted without per-row
  evaluation; a per-row justification propagated rather than evaluated; a
  measurement on the ledger while the gate reads the destination; a resolver that
  prefixed the governance directory onto arbitrary tokens, discarded unwritten; a
  closure claim that measured field PRESENCE and reported it as correctness; and
  a survival-predicate sweep whose two halves were a path-token false positive and
  a paraphrase-blind zero, also not written. The pattern is that every attempt
  produced output that looked more thorough than the state it replaced.
- Spec 137 gained `### Uniqueness-predicate amendment`; all 47 uniqueness
  statements are re-derived under it by three seats: 11 UNIQUE, 23 PARTIAL, 13
  NOT UNIQUE. Only 11 carries are the sole surviving record. The PARTIAL rows
  share a shape: the fact survives and the quantification and judgement vanish.
  Two verdicts inverted — the three Gemini rows were NOT unique on grounds the
  predicate excludes and are UNIQUE; two UNIQUE rows are NOT UNIQUE.
- The owner requirement is now enforced by
  `scripts/validation/carry_owner_contract.py`, which compares each record's
  stated owner against the SSOT row it cites. It found 24 failures on its first
  run and measures 0 now, with 10 regression tests pinning the historical failure
  modes. Seven prior measurements failed because none of them could fail.
- **Task 10E is unblocked and its RED already exists.** The repository runs tests
  with `python3 -m unittest discover -s tests/validation`, not `pytest`; the
  recorded pytest blocker was never real. Two further claims made on discovering
  that are also wrong and are corrected in the Spec 136 Task. The suite has NOT
  regressed: it declares 50 tests at `cb117edd` and 50 now, and every input it
  consumes is identical across that range, so its 4 failures existed at the commit
  recorded as `authoritative Operations 47/47`. That 47 is round 1's figure and
  rounds 2 and 3 added the other three afterwards. The 4 failures are Task 10E and
  10F's RED: 10D's remediation wrote coverage that fails closed until the later
  domains converge. The `51` missing rules is `04-data` alone after its renames
  ran; at rest `--mode complete` measures 154 findings of which only 4 are
  `semantic-rewrite-rule-missing`, and no domain's true count is measurable before
  its renames execute. The suite costs `214.853s`, so rule work must batch per
  domain.
- **`04-data`'s semantic half is sized in a synthetic tree, with no repo
  mutation.** All 51 labels are one family, `stale:legacy-subject-path:`, over 19
  subjects, and the stale artifact is a `<!-- Target: -->` self-reference marker,
  not an H1, so Task 10D's handler shape does not transfer. Synthetic RED is 201
  findings. A rule with no source replacement drops that to 99 but is fail-open:
  repointing a marker at another subject in the same domain produced zero
  findings. Passing two other adversarial mutations was not evidence of soundness.
  Adding the row's own final path as `required_target` closes it and passes 50 of
  51. The one that fails, the `ops-0032` rehearsal runbook, carries no marker and
  contains its old slug zero times, so its approved label has no basis in the text
  it labels -- a frozen-map defect, recorded not worked around.

- Both surfaces now measure 47 of 47 on owner and uniqueness. The 25 destination
  paragraphs were resolved one at a time against the surface each claim must
  change to be remediated, not against every path the paragraph quotes.
- There is more than one duplicate group: four ledger rows declare NOT unique,
  the three Gemini rows plus the Changelog-authority row.

- The ownership tables hold 33 patterns, not the 24 previously recorded.
- The Gemini stale-identifier claim is REMEDIATED, not live: `Flash` occurs zero
  times in `providers/gemini.md` since `6bd7c62d`. Its three rows stay `carry`
  under the audit-trail subtype and must not be read as a live defect.
- Both destination seats reported and their bounded findings are applied. The
  most serious was mine: restoring an enumeration a seat said had been degraded,
  I wrote six source names from memory and published fabricated upstream content,
  caught on the next source comparison. Restoring content is as source-bound as
  writing it. Five further published leaf defects are corrected, the caveat
  family set is completed at twenty families, eleven pre-merge path citations are
  repointed through the migration ledger, and two drifting measurements are
  replaced by their re-derivation commands.
- Both gate 1 coverage holes are filled. The vendor catalog's `Caveat` column is
  deduplicated into fifteen reading-rule families in the successor leaf with
  fourteen new ledger rows, and the Mythos Preview lifecycle conflict has its own
  row and paragraph. The per-row identity data stays uncarried and re-derivable.
- The `Omit` provenance finding is refuted by measurement: the pointer is the
  ledger's `Old commit` and `Old blob` pair, and `git cat-file -t` returns `blob`
  for 20 of 20 distinct pairs across all 84 `Omit` rows. The narrower residual,
  reason cells asserting a surviving surface without a resolvable path, is
  recorded and does not block gate 3.
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

- **Both remaining gates are blocked on independent review, not on edits.** Gate 2
  needs one more review over the current state; the 2026-08-19 seats reviewed the
  state before their own findings were applied, so their settled counts do not
  carry forward. Gate 4 needs a seat for its four corrected rows. Neither can be
  settled from inside this unit, and the session instruction in force forbids
  spawning review agents unless the user asks, so both wait on that request.
- Gate 4's residual is enumerated from the scanner's own allowlist reader: 43
  rows, 8 unsettled, needing three different actors. Four are corrected and wait
  only on an independent seat (two `mig-0001` rows, two route 2 selector rows).
  Three sit in Specs carrying `status: completed`, so they have no actor. One,
  the `test_document_taxonomy.py` scan exemption, reads two ways after the route 3
  amendment and the admitting reading is the one favourable to this unit, so it
  was not taken. Two mechanical escapes were rejected: importing the scanner's
  carved-out constant binds an unrelated test to a module scheduled to go, and
  assembling the path from components hides a literal the gate exists to expose.
- The deleted Stage 90 leaf now has its own unit at
  `docs/03.specs/spec-0152-deleted-reference-leaf-disposition/` with Spec, Plan
  and Task, on the user's direction. Registering it re-derived the figures and
  corrected one: the loss is 10 of 25 headings, not 5. The recorded 5 was true
  when taken and false when written, because writing a heading into the record
  makes it occur in a tracked file. The corrected predicate excludes the
  recording surfaces and the deletion-scheduled retiring directory, and its
  command is in that unit's Spec. The disposition itself is open and belongs to
  `doc-writer`.
- Route the three completed-Spec allowlist rows and the one unadmitted exemption
  row to their owning units; none is fixable inside this unit.
- No gate has been recorded satisfied.
- Resume the taxonomy migration at slice 10E, domains 04 through 06.
- The Spec 137 deletion gates stay unsatisfied; the retiring pack must not be
  deleted or relocated until every gate is independently recorded.
