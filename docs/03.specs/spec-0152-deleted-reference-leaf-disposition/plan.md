---
status: draft
artifact_id: plan-0152
artifact_type: plan
parent_ids:
  - spec-0152
created: 2026-08-19
updated: 2026-08-19
---

# Deleted Reference Leaf Disposition Implementation Plan

## Overview

This plan sequences the disposition decision defined in `spec.md`. The decision
itself belongs to `doc-writer`; this plan makes the decision cheap to take and
impossible to take on an unmeasured basis.

## Context and Inputs

The leaf, its blob, its deleting commit, and the survival figure are recorded in
`spec.md` under `## Boundaries and Inputs`, each with a re-derivation command
under `## Verification`. No figure in this plan is stated independently of those
commands.

The unit begins with the content already recovered in Git history, so no step
here risks losing it further. The risk this plan manages is the opposite one: a
disposition taken on a survival claim that counted the loss record as survival.

## Goals and Non-goals

**Goals.**

- Present the 10 non-surviving headings to the owner with their content.
- Take one of the three dispositions in `spec.md` and record it with the evidence
  its decision rule requires.
- Leave the survival figure re-derivable after the disposition.

**Non-goals.**

- Restoring or superseding any other deleted surface.
- Auditing the taxonomy merge for further losses. That belongs to `spec-0136`.
- Changing the retiring pack's deletion gates.

## Work Breakdown

- [ ] **Step 1. Re-derive the baseline.** Run both `## Verification` command
      blocks from `spec.md` and record the figures in `task.md`. Expected: blob
      `9df3384d`, 533 lines, absent at `HEAD`, 25 headings, 10 non-surviving.
- [ ] **Step 2. Extract the non-surviving material.** For each of the 10
      headings, extract its section body from the blob into `task.md`, so the
      owner decides against content rather than against titles.
- [ ] **Step 3. Test the `Supersede` option honestly.** For each of the 10
      headings, search the successor reference surfaces for material that carries
      the same claim, not the same words. Record per heading whether a successor
      surface carries it, and name that surface.
- [ ] **Step 4. Put the decision to the owner.** Present Steps 2 and 3 and take
      one disposition. `Discard` requires the owner's recorded decision.
- [ ] **Step 5. Execute the chosen disposition.** Restore, register the
      supersession, or record the discard, reconciling any restored file to the
      converged identity and metadata contract.
- [ ] **Step 6. Re-measure and close.** Re-run the survival command and record a
      figure consistent with the chosen outcome.

## Verification Plan

Run from the repository root after Step 5.

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-repo-contracts.sh
```

Expected: no new violation attributable to this unit's files, and a survival
figure consistent with the recorded disposition. A restored leaf must not
reintroduce a pre-migration identity form.

## Risks and Rollback

| Risk | Control |
| :--- | :--- |
| Survival is measured without excluding the recording surfaces | Step 1 uses the `spec.md` command, which carries the exclusions |
| `Supersede` is claimed on a same-named successor | Step 3 tests per heading and names a surface per heading |
| A restored leaf reintroduces a pre-migration identity | Step 5 reconciles before recording completion |
| The predecessor path literal is written into a new surface | The path is never written here; `spec.md` states why |

Rollback is a single `git revert` of this unit's commits. The content is not at
risk in any branch of this plan because the blob is reachable from `57259e24`.

## Approval Gates

- Step 4 requires the owner's decision and may not be taken by an implementer.
- `Discard` requires that decision to be recorded verbatim in `task.md`.

## Completion Criteria

- One disposition is recorded in `task.md` with its required evidence.
- The survival command returns a figure consistent with that disposition.
- `spec.md` and this plan carry `status: completed`.

## Related Documents

- [Specification](./spec.md)
- [Task evidence](./task.md)
- [SDLC taxonomy convergence plan](../spec-0136-sdlc-taxonomy-convergence/plan.md)
