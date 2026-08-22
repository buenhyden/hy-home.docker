---
profile_id: spec
status: draft
artifact_id: SPEC-0152
artifact_type: spec
parent_ids:
  - SPEC-0136
created: 2026-08-19
updated: 2026-08-19
---

# Deleted Reference Leaf Disposition Specification

## Overview

A Stage 90 reference leaf was deleted from the working tree by the SDLC taxonomy
merge and its content survives in no tracked file. This specification defines the
disposition decision for that content and the evidence any disposition must
produce. It does not itself restore, supersede, or discard the content.

The unit exists because the finding was made inside a different unit that does
not hold the decision. Recording it there kept it from being lost; deciding it
there would have placed a Stage 90 documentation judgement inside a pack
retirement track that has no authority over Stage 90 leaves.

## Boundaries and Inputs

**Measured inputs.** Every figure below is re-derivable from Git at the commands
given in `## Verification`.

| Fact | Value |
| :--- | :--- |
| Deleted path | `docs/90.references/research/ref-0085-verification-validation.md` |
| Content blob | `9df3384d9fc4775c36dbb77d4be6f76d7c2296ff` |
| Blob length | 533 lines |
| Last commit holding it | `57259e24` |
| Deleting commit | `5afdd277`, the taxonomy merge, on the `90b6b16b` side |
| State at `HEAD` | absent |
| Headings in the blob | 25 |
| Headings surviving in no durable tracked file | 10 |

**How the leaf reached the deleted path.** `57259e24` renamed it out of the
retiring research pack into the Stage 90 reference namespace as an `R096` rename,
in the same commit that created its surviving sibling
`ref-0084-github-actions-platform.md`. The predecessor path is not written here
because it names the retiring directory, which is under an active literal gate;
it is recorded once, under an allowlist row, in the Spec 137 Task.

**Why the merge review did not see it.** The delete appears on only one side of a
merge, so `git log --diff-filter=D` does not report it. The review checked the
retiring pack, and this leaf had already been moved out of that pack, so it sat
outside the surface being checked.

**Out of scope.** The retiring pack's own deletion gates, the taxonomy migration
slices, and any other leaf. This unit covers one leaf's content.

## Contracts

Not applicable. This unit changes no API, and declares that explicitly rather
than leaving the section to be read as unexamined.

## Core Design

The disposition is a choice among exactly three outcomes, and the outcome must be
recorded whichever is chosen.

1. **Restore.** Reinstate the blob at a Stage 90 reference path, reconciled to the
   converged taxonomy identity scheme and metadata contract.
2. **Supersede.** Record that a named successor surface carries the material, and
   register the supersession so the content is retrievable from the record.
3. **Discard.** Record that the material is not worth carrying, with the reason.

**Decision rule.** `Supersede` requires naming the surface for each of the 10
non-surviving headings. The successor pack holds a `verification-validation.md`,
but it is a different document and is not a superset; naming it wholesale does not
satisfy this rule.

**Self-invalidating-measurement guardrail.** The survival predicate must exclude
every surface that exists to record this loss. Writing a heading into the record
makes that heading occur in a tracked file, so a predicate that does not exclude
the record reports the content as surviving because it was written down. This is
not hypothetical: the first measurement of this loss reported 5 non-surviving
headings, and re-running the same predicate after the finding was recorded
returned a smaller set for that reason. The true figure under the corrected
predicate is 10.

## Interfaces and Data

Not applicable. No data contract, schema, or interface changes.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| A survival claim counts the loss record itself as survival | Exclude the recording surfaces named in `## Verification` |
| A survival claim counts the retiring pack as survival | Exclude the retiring directory; it is deletion-scheduled, so survival there is not survival |
| `Supersede` is chosen wholesale on a same-named successor | The decision rule requires a named surface per non-surviving heading |
| Restoration reintroduces a pre-migration identity or metadata shape | Restoration reconciles to the converged scheme before it is recorded complete |
| The decision is deferred again and lost | This Spec's Task holds the open state; it is not a bullet inside another unit |

## Verification

Re-derive every figure with these commands. `LEAF` is the deleted path.

```bash
LEAF=docs/90.references/research/ref-0085-verification-validation.md
git rev-parse 57259e24:"$LEAF"                 # 9df3384d9fc4775c36dbb77d4be6f76d7c2296ff
git show 57259e24:"$LEAF" | wc -l              # 533
git log -m --diff-filter=D --oneline 57259e24..HEAD -- "$LEAF"
test -f "$LEAF" || echo ABSENT
```

Re-derive the survival figure with the exclusion set applied. The exclusions are
the retiring directory, the Spec 137 Task, and this unit's own files.

```bash
LEAF=docs/90.references/research/ref-0085-verification-validation.md
git show 57259e24:"$LEAF" | grep '^#' | sed 's/^#* //' | while IFS= read -r h; do
  grep -rlF "$h" docs --include='*.md' \
    | grep -v 'agentic-research-pack-refresh' \
    | grep -v 'agentic-research-pack-rebuild' \
    | grep -v '0152-deleted-reference-leaf-disposition' \
    | grep -q . || printf '%s\n' "$h"
done | wc -l                                    # 10
```

A disposition is verified when the chosen outcome is recorded in this unit's Task
with the evidence its decision rule requires, and when the survival command above
returns a figure consistent with that outcome.

## Agent Role and IO Contract

The disposition owner is `doc-writer`, which owns the Stage 90 documentation
surfaces. No agent may choose `Discard` without the owner's recorded decision.

## Related Documents

- [Implementation plan](./plan.md)
- [Task evidence](./tasks/tsk-0001-reference-disposition.md)
- [SDLC taxonomy convergence](../0136-sdlc-taxonomy-convergence/spec.md)
- [Agentic research pack rebuild Task](../0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md)

## Behavior Contract

The behaviors and invariants already specified above remain the package behavior contract.

## Technical Approach

The implementation and component design recorded above remain the technical approach.

## Acceptance Contract

The verification and success conditions above remain the acceptance contract.

## Traceability

The requirement, architecture, operations, and evidence links above provide traceability.
