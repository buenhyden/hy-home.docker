---
layer: agentic
status: active
---

# Direct-deletion branch holds unique work under an unadopted design

- Date: 2026-08-17
- Layer: agentic
- Status: active
- Applies To: `docs/03.specs/137-agentic-research-pack-rebuild/`, `docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md`, branch `codex/agentic-research-rebuild-finish`
- Tags: worktree, deletion-gate, unmerged-work, approval-evidence, preservation
- Retrieval Keywords: direct deletion controller, gate 9, step 0e, step 0f, ADR 0029, confined descriptor publication, landlock, approval stamp, tracked controller amendment
- Last Verified: 2026-08-17

## Problem

Branch `codex/agentic-research-rebuild-finish` (tip `ced4c4f0`, newer than
`main`) built a large deletion subsystem whose design authority rests on a Spec
amendment stamp that carries no recorded user wording. A future reader finding
that branch could reasonably treat it as the authoritative successor to `main`'s
Gate 9 line and resume 60 commits of work on an unapproved design, or could
delete the branch and lose genuinely unique artifacts.

Both errors are available because the branch is simultaneously more advanced,
more blocked, and less substantiated than `main`.

## Context

The two lines are divergent edits of the same three files from merge-base
`2ca5f4b8` (2026-08-11T12:29). `main` branched before the branch declared Step 0e
dead on 2026-08-12T11:31 and continued Step 0e unaware. `main` did not revive a
killed step; it never saw the kill. Both lines independently produced a commit
with the identical subject `fix(validation): linearize gate 9 bundle
publication`, four days apart.

The branch carries three approval stamps absent from `main`: a 2026-08-12
receipt-contract amendment, and two dated 2026-08-13. Their evidentiary weight
differs sharply.

| Stamp                                         | Recorded wording | Memory corroboration    | Stage 04 approval entry |
| :-------------------------------------------- | :--------------- | :---------------------- | :---------------------- |
| 2026-08-13 deletion-evidence decoupling       | present          | same-day                | absent                  |
| 2026-08-13 tracked direct-deletion controller | absent           | structurally impossible | absent                  |
| 2026-08-12 receipt-contract                   | absent           | absent                  | absent                  |

The decoupling amendment is narrow by its own words: it removes a mechanism
dependency, not a safety requirement, and preserves all nine pre-deletion gates.
The controller amendment's own section contains no user, no approval, and no
date; its rationale is entirely technical. The Task grounds that design in
reviewer verdicts on the very commit that asserts the approval, which is a closed
loop. The branch's own evidentiary standard elsewhere is a quoted user
instruction, which neither 2026-08-13 stamp meets.

The Step 0e kill itself is well substantiated and independent of any approval:
five review rounds exhausted on a delegated-write finding, stated concordantly in
ADR 0029, the Plan, and the Task.

Neither line has deleted anything. Both still track all twenty files of the
retiring pack. The branch's blocked state is worse than `main`'s: its
architecture audit is `BLOCKED C1/I1/M0`, its authority-FD corrections returned
`BLOCKED C3/I1/M0` and `BLOCKED C2/I3/M0`, its controller implementation failed
all three reviews including a Quality BLOCK at `C6/I5/M1`, its latest
synchronization is `Needs fixes`, and it declared its own Gates 1 through 8
evidence invalid for current admission. It also went through four successive
redesigns.

## Resolution

The user reviewed this evidence on 2026-08-17 and recorded uncertainty about the
tracked-controller approval. The evidentiary burden was therefore applied:

- The documented decoupling amendment was ported to `main` as its own Spec 137
  section, with the port and its provenance stated in the text.
- The tracked-controller amendment was **not** adopted. Spec 137 now states
  outright that no controller, worker, or confined-runtime subsystem derives
  authority from it.
- The branch and its worktree are preserved, not merged and not discarded.
- Its four Git-unbacked working-tree files were copied to durable storage outside
  the repository before any other worktree action, with digests compared.

The decoupling port made `main`'s Step 0e non-gating, which is why round 4's two
`Needs fixes` verdicts no longer block deletion. Those verdicts stay recorded;
nothing was retracted.

## Prevention

- A date stamp is not an approval record. Require the wording, or treat the
  amendment as deferred. This repository's own better practice is to quote the
  user instruction verbatim, and that standard existed on the same branch.
- Do not let reviewer verdicts substitute for user consent. Reviewers validating
  the commit that asserts an approval establishes nothing about the approval.
- Check the merge-base date before concluding that a line ignored a decision. A
  line that predates a decision is uninformed, not non-compliant, and the
  remedy is different.
- Weigh defence cost against what is protected. The deletion under guard is
  locally reversible, remotely replicated at twenty of twenty byte-identical
  blobs, and its restoration was verified by execution. Nine implementation
  rounds, thirteen Plan corrections, and four redesigns were spent guarding it.
  When the guard costs more than the asset, remeasure the threat model instead of
  iterating the guard.
- Copy Git-unbacked working-tree files to durable storage before any git
  operation touches a worktree. This branch already lost a comparable protected
  set that way.

## Evidence

- Branch tip `ced4c4f0`; merge-base `2ca5f4b8`; 94 commits ahead of that base and
  35 behind `main`.
- Twelve tracked paths exist only on the branch, including ADR 0029, a native
  confined publisher with a committed static ELF, and the controller, worker, and
  test trio. ADR slot 0029 is unused on `main`, so no identifier collides.
- The retiring pack resolves at twenty files on both `main` and the branch.
- Conflict surface against `main` is seven files, four of them large independent
  rewrites of the same helper, its tests, the Plan, and the Task, plus two live
  divergent revisions of Spec 137.
- The branch's `current.md` is frozen at 2026-08-13 while roughly sixty later
  commits changed its direction twice, so that record is not a reliable guide to
  its state.
- Preserved working-tree copies live under a dated preservation directory in the
  user's home, outside the repository and outside Git.

## Related Documents

- [Governance memory index](./README.md)
- [Current project memory](./current.md)
- [Spec 136 migration branch preservation](./spec-136-migration-branch-preservation.md)
- [Prior loss of protected dirty files](./ignored-sdd-scratch-deletion.md)
- [Spec 137](../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Rebuild Task holding the deletion gate](../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
