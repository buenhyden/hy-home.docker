---
title: Archive Preservation Model Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0170-PLAN-0001
parent_ids: [SPEC-0170]
created: 2026-09-04
updated: 2026-09-04
---

# Archive Preservation Model Plan

## Objective

Turn `docs/98.archive/` from a pointer index into a retained archive with three
disposition subtrees, move every terminal document out of the active stages,
and restore the 104 retired documents that exist only in Git.

## Dependencies

- SPEC-0169 is complete: the section contract is enforced for every profile, so
  a new profile's declarations take effect the moment they are registered.
- Every Tombstone already records a valid `Recovery Commit`, which the
  restoration phase reads.
- ADR-0030 decided the pointer-only archive and must be superseded, not edited.

## Execution Sequence

1. **Phase 1 — declarations.** Add the `{archived_subpath}` path token, register
   the three preservation profiles, and widen the `unmanaged` frontmatter rule
   to archive-scoped profiles. Teach supersession resolution to read preserved
   records. Move the three `superseded` documents. → the gate stays green with
   a populated `superseded/` subtree.
2. **Phase 2 — completed packages.** Move the 21 completed Stage 03 packages
   whole, and repoint the 21 Tombstones, the Stage 03 README index, and the
   spec bodies that link to relocated members. → `docs/03.specs` holds only
   live packages.
3. **Phase 3 — restoration.** Restore 104 retired documents from the commit
   each Tombstone names, verifying the blob exists at that path and commit
   before writing. → every Tombstone has its record.
4. **Phase 4 — governing documents.** Rewrite the retention rules in REQ-0026,
   AD-0030, and `documentation-protocol.md`; supersede ADR-0030 with the
   preservation decision; correct the recovery statement in `bootstrap.md`.
5. **Phase 5 — enforcement.** Add the placement check and its mutation
   coverage: a terminal document in an active stage, a Tombstone without a
   record, and a record without a Tombstone each fail.

## Risk and Rollback

The largest risk is restoring 104 documents whose content is deliberately
wrong — Stage 01 requirements naming middleware chains, Stage 03 packages
describing steady state. They are preserved as history, not reinstated as
authority, which the disposition subtree makes structurally clear. If a
restoration cannot read its recorded blob it stops rather than reconstructing.

Every phase is a separate commit and the tree is green at each boundary, so
rollback is a revert of the phase that broke.

## Verification

- `run-ci-gate.py --profile full` exits `0` at every phase boundary.
- Tombstone-to-record correspondence is total in both directions.
- Each restored record is byte-identical to the recorded blob.
- No document under stages 01, 02, 03, 05, or 90 carries a terminal status.

## Related Documents

- [Specification](spec.md)
- [Execution task](tasks/tsk-0001-archive-preservation-model.md)
