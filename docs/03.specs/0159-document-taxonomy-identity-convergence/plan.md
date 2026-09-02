---
title: Document Taxonomy and Identity Convergence Implementation Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0159-PLAN-0001
parent_ids: [SPEC-0159]
created: 2026-09-02
updated: 2026-09-02
---

# Document Taxonomy and Identity Convergence Implementation Plan

**Goal:** Land the taxonomy, envelope, and template-layout convergence in
reviewable units, each ending with the registered gate green.

## Objective

Converge `type`, `layer`, and the Stage 99 template layout on one Registry-owned
taxonomy; make `version` a required envelope key; and reduce Stage 99 to a
single catalog, without weakening any contract that already held.

## Dependencies

- SPEC-0158 must be complete, because it established the identity patterns this
  package assumes.
- The Registry is the single machine authority; corpus and validator changes
  follow it rather than the reverse.
- Stage 98 migration digests may be repinned only after byte-identical bodies
  are verified.

## Execution Sequence

1. Restate the contract: retype profiles, move template sources, rebuild
   `template_roles` from one mapping, and register the new forms.
2. Migrate the corpus `type` and `layer` from the Registry-derived table.
3. Align validators and tests with the new values, repairing each defect the
   change surfaces at its cause.
4. Record the taxonomy in the documentation protocol and stage authoring matrix.
5. Promote `version` to required, drop `layer` from Stage 00 and Stage 99, and
   regenerate every derived Stage 90 output.
6. Consolidate the Stage 99 catalogs into one template README.
7. Reconcile the docs index with the Registry path patterns.

## Risk and Rollback

| Risk | Control |
| :--- | :--- |
| A corpus-wide rewrite silently changes meaning | Every rewrite is a scripted, reviewable transformation over parsed frontmatter only |
| A frozen archive record is mutated | Repin only after verifying the body is byte-identical to its predecessor blob |
| Relaxing a contract to make the gate pass | Each surfaced defect is repaired at its cause; no required key or section was dropped to pass |
| Auto-formatter churn hides intent | Library diffs are restored to HEAD and the intended edits reapplied without the formatter |

Rollback is `git revert` of the listed commits; no runtime state changes.

## Verification

`python3 scripts/validation/run-ci-gate.py --profile full` must exit 0 at the
end of each step, and the acceptance contract in the Spec must hold at the end
of the package.

## Rulings

Three interpretation choices were decided by the requester before execution:
governance templates map one-to-one onto existing Stage 00 document kinds; the
common README form splits into stage, domain, and package variants; and a Stage
90 pack keeps a `-pack` type distinct from its member type.
