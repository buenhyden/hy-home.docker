---
title: "Stale Fact Convergence Implementation Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0176-PLAN-0001"
parent_ids:
- "SPEC-0176"
created: "2026-09-07"
---

# Stale Fact Convergence Implementation Plan

## Objective

Correct every statement SPEC-0176 names, at the document that owns it, without
changing the implementation those statements describe. The order below exists so
that each correction is made against a measured current fact rather than against
an earlier document, and so that the two lifecycle promotions land as atomic
result trees rather than as intermediate authority states.

The transition budget is the binding constraint on sequence. The metadata check
reads `previous_status` from the merge base with `origin/main`, so each document
admits one transition on this branch. W5 and W8 each spend that budget on the
documents they move, and no later unit may need a second transition on the same
document.

## Dependencies

- Audit baseline: local `main` at `e37b2dbcd`, six commits ahead of
  `origin/main` at `d890b862e`. That was the merge base when the package
  opened. Each later integration moves the base, and the Task records the base
  each transition was measured against.
- Position is read from Git, not from a branch name. The three commands are in
  the Spec's Boundaries section and in the Task's Inputs.
- SPEC-0173 declared the retention-owner promotion as its open dependency and
  wrote its required sequence into its own Plan. W5 follows that sequence and
  records the result in this package's Task, not in SPEC-0173's.
- `ADR-0033` already exists as the reviewed successor design. This package
  performs its acceptance; it does not re-author the decision.
- `.agents/governance/documentation-protocol.md` already carries the accepted
  preservation model and is an input to W5, never an output of it.
- The root `docker-compose.yml` `include:` list and every Compose file are
  inputs to W2 through W4 and are not modified by them.

## Execution Sequence

1. W1: Open the package. Write the Spec, this Plan, and the Task at their
   lifecycle initial statuses, advance `identity_spaces.spec` from 175 to 176,
   and add the Stage 03 index row.
2. W2: Re-measure the Compose facts. Count tracked Compose files, service
   directories, and root `include:` entries, and read the `profiles:` value of
   every service named in a document this package corrects. Record the commands
   and results before editing any prose.
3. W3: Converge the seventy-four service and operations documents that describe a
   Compose file as a commented, optional, or standalone root include onto the
   profile model POL-0078 owns.
4. W4: Correct the four Compose documents that carry their own wording: the
   `infra/README.md` inventory snapshot and its four-state vocabulary, the MinIO
   README's cluster-variant prohibition, POL-0078's system scope counts, and the
   root `docker-compose.yml` `include:` comment.
5. W5: Promote the retention owner. Transition `ADR-0033` to `accepted`,
   transition `ADR-0031` to `superseded` and move its body unchanged to
   `docs/98.archive/superseded/`, apply reciprocal supersession metadata, amend
   `REQ-0026` and `AD-0030` to the accepted preservation unit, and refresh the
   Stage 02 indexes.
6. W6: Correct the canonical knowledge members. Restate the bootstrap load order
   in `repository-map.md` including both new categories, and give
   `verification-surface-map.md` a provenance that names the commit for each
   transcribed source.
7. W7: Replace dead-branch position in the two active Spec packages and remove
   the `tests/fixtures/` sentence from SPEC-0173's behavior contract.
8. W8: Complete and preserve SPEC-0175. Transition its Spec, Plan, and Task to
   `completed`, move all three bodies to `docs/98.archive/completed/`, and update
   the Stage 03 index in the same result tree.
9. W9: Correct the remaining index facts: the Stage 02 counts and structure tail,
   and the `docs/README.md` rows that claim co-located Plan and Task evidence for
   a Spec-only preserved package.
10. W10: Regenerate every affected registered output with its own generator,
    stage the tree, and run the freshness checks on the staged tree.
11. W11: Run the changed profile and the applicable document checks on the final
    path set, then obtain an independent exact-diff review and correct only
    findings inside the current authorization.
12. W12: Close the bilingual predicate gap and restore the `_workspace` tracking
    contract that the second review round found.
13. W13: Work the deferred items under the explicit scope extension the Task
    records.
14. W14: Answer the third review round with the claim-shape sweep.
15. W15: Answer review rounds four and five and fix the directory-identity guard.
16. W16: Re-baseline against a later HEAD and close the partial Stage 02 sweep.
17. W17: Correct the Deferred Items whose inputs had moved.
18. W18: Register the fenced command path check.
19. W19: Register the Compose include and profile check and amend criterion 1.
20. W20: Answer review round six, reconcile the receipts and take the first
    lifecycle step.
21. W21: Answer review round seven and take the second lifecycle step.
22. W22: Answer review rounds eight and nine, record the changed profile on the
    final path set, and complete and preserve the package.

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| A Compose sentence is corrected from prose instead of from the Compose file | W2 records the measured `profiles:` value before W3 edits anything | Re-read the service file and correct the sentence; the edit is one line |
| A count is corrected by arithmetic rather than measurement | W2 records the command and its output for every count W4 writes | Re-run the command and correct the number |
| The retention promotion leaves an intermediate authority state | W5 applies both transitions, the move, the reciprocal metadata, and both amendments in one result tree | Revert the W5 commit; no other unit depends on its tree |
| A frozen body is edited to agree with the new contract | `ADR-0031` is compared before and after the move and only its transition-owned frontmatter differs | Restore the pre-move body from Git and redo the move |
| A second transition is attempted on a document already advanced on this branch | The budget is measured against the merge base in W1 and each promotion unit spends it once | Leave the document where it stands and record the unmet remote precondition |
| SPEC-0173 is advanced as a side effect of W7 | W7 touches two sentences and no status, and the diff is reviewed against its acceptance criteria | Revert the two hunks. W20 later completed SPEC-0173 under the operator's 2026-09-14 request, as a named unit rather than a side effect |
| SPEC-0175's members move without the index | W8 stages the three moves and the index row together | Revert the W8 commit; the package returns to completion-ready |
| A generated output is hand-edited | W10 runs generators only and never edits their outputs | Regenerate and restage |

## Verification

The Task records every actual command, working directory, selected path set,
exit code, scope, review finding, and PASS/FAIL/BLOCKED/NOT_RUN/N/A state. This
Plan records order and resume conditions and makes no execution claim.

Completion requires every numbered acceptance criterion in the Spec to be
satisfied as written and recorded in the Task's receipt, one row per criterion
and work-unit pair. Criterion 17 requires the changed profile to exit 0 on the
final path set; a focused check that passes on a subset does not satisfy it.
Criterion 18 requires an independent exact-diff review of the whole package.

This package's own three documents walk their lifecycle across integrations,
because each document admits one transition per base and an active Plan or an
in-progress Task requires an active Spec. The walk is Spec `review` to
`approved` first. Next the Spec becomes `active`, together with an `active`
Plan and an `in-progress` Task. Last, all three reach `completed` and move to
the archive in one result tree. Each step waits for the remote to carry the
one before it.

## Rulings

- Corrections are applied at the owner of the wrong statement. A second sentence
  is never added beside a wrong one to explain it.
- A dated observation is never rewritten to look current. Where a later fact
  contradicts an earlier measurement, the later fact is recorded as a later
  entry with its own date.
- A guard that fires is treated as correct until proven otherwise; the change is
  adjusted rather than the guard weakened.
- Unexecuted checks are recorded as NOT_RUN or BLOCKED with their missing input
  and are never promoted to a PASS.
- No package already preserved under `docs/98.archive/` gains a retroactively
  authored member, and no frozen body is edited.
- SPEC-0173 is not advanced, completed, or restructured as a side effect of this
  package. W20 completed it as its own unit under the operator's 2026-09-14
  request, and SPEC-0173's Task 0006 W40 records that work.

## Related Documents

- [Specification](spec.md)
- [Task 0001 evidence](tasks/tsk-0001-stale-fact-convergence.md)
- [Stage 03 index](../README.md)
