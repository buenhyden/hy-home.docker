---
status: draft
artifact_id: task-0152-01
artifact_type: task
parent_ids:
  - spec-0152
  - plan-0152
created: 2026-08-19
updated: 2026-08-19
---

# Task: Deleted Reference Leaf Disposition

## Overview

Evidence for the disposition of one Stage 90 reference leaf deleted by the SDLC
taxonomy merge. This Task holds the unit's open state. At registration, Step 1 of
the plan is complete and Steps 2 through 6 are open.

## Inputs

- `spec.md` `## Boundaries and Inputs` for the measured facts.
- `spec.md` `## Verification` for the two re-derivation command blocks.
- The content blob `9df3384d9fc4775c36dbb77d4be6f76d7c2296ff`, reachable from
  `57259e24`.

## Goals and Non-goals

Carried unchanged from `plan.md` `## Goals and Non-goals`. This Task restates no
goal independently, so the two cannot drift apart.

## Scope and Change Boundaries

**Allowed paths.** This unit's own three files, and — only once a disposition is
recorded — the Stage 90 reference path the disposition names.

**Forbidden paths.** The retiring research pack and its deletion gates, the
taxonomy migration ledgers, and the Spec 137 Task. This unit reads them and
writes none of them.

**Compose impact.** None. No service, image, or volume is touched.

**Security impact.** None. No secret, credential, or `secrets/` path is read or
written.

**Operations impact.** None. No runbook, policy, or operational control changes.

**Runtime impact.** None. No script, hook, or validator changes.

## Approval Evidence

**Approval source.** The user directed on 2026-08-19 that the disposition of this
leaf be registered as a separate unit, after the loss was found while tracing a
gate 4 review seat's observation inside the Spec 137 rebuild Task.

**Protected surfaces.** The retiring pack stays under its own deletion gates and
is not touched here. The commit-pinned target-surface convergence summary stays
unchanged, as Spec 137 pre-deletion gate 8 requires.

**Approval boundary.** Registration was approved. No disposition was approved;
`Discard` additionally requires the owner's recorded decision, per `plan.md`
`## Approval Gates`.

**Rollback or recovery.** A single `git revert` of this unit's commits. The
content is independently recoverable from the blob above, so no branch of this
unit can lose it.

**Redaction boundary.** No credential, token, raw log, or shell history is
recorded here.

## Work Breakdown

Carried unchanged from `plan.md` `## Work Breakdown`. Step 1 is complete; Steps 2
through 6 are open.

## Work Log

| Date | Unit | Evidence |
| ---------- | --------------------------------- | ------------------------------------------------- |
| 2026-08-19 | Unit registered and Step 1 closed | Registered as a separate unit on the user's direction, because a Stage 90 documentation judgement does not belong inside a pack retirement track. Re-derived every figure rather than carrying the originating record's: blob `9df3384d9fc4775c36dbb77d4be6f76d7c2296ff`, 533 lines, present at `57259e24`, absent at `HEAD`, deleted by the merge `5afdd277` on the `90b6b16b` side, 25 headings. **The originating record's survival figure was wrong and the way it was wrong is the finding.** It recorded 5 headings occurring in zero files. Re-running that predicate now returns fewer, because writing a heading into the record makes it occur in a tracked file -- the act of recording the loss falsified the measurement that justified recording it. Excluding the recording surfaces and the deletion-scheduled retiring directory, 10 of the 25 headings survive in no durable tracked file, twice the recorded figure. The exclusion set is written into the `spec.md` command so the figure stays re-derivable. |

## Verification Evidence

**Exact commands.** Both blocks in `spec.md` `## Verification`, run from the
repository root.

**Expected evidence.** Blob `9df3384d`, 533 lines, absent at `HEAD`, 25 headings,
10 non-surviving.

**Actual evidence.** All five figures matched at registration.

**Verification results.** Step 1 verified. Steps 2 through 6 are not yet run, and
no disposition is recorded, so this unit records no completion.

The 10 non-surviving headings, listed here rather than in `spec.md` because this
file is inside the exclusion set:

| # | Heading |
| :-- | :--- |
| 1 | Where Testing Sits |
| 2 | Static and Dynamic Verification |
| 3 | V&V Under Non-Determinism |
| 4 | Regulated-Domain Contrast |
| 5 | Repository Verification and Validation Surface |
| 6 | The gate population is verification, with two exceptions |
| 7 | The eval gate is verification, not validation |
| 8 | The dynamic test suite verifies the verifiers |
| 9 | The rest of validation is procedural |
| 10 | Terminology drift in tracked labels |

## Controlled Agent Pre-commit Evidence

**Controlled wrapper command.** Not run. The approved all-files wrapper is a final
QA gate and this unit has no implementation to gate.

**Controlled wrapper allowed prefixes.** Not applicable while unrun.

**Controlled wrapper exit status.** Not applicable while unrun.

**Controlled wrapper snapshot result.** Not applicable while unrun.

**Controlled wrapper observation boundary.** Not applicable while unrun.

**Controlled wrapper path sets.** Not applicable while unrun.

**Controlled wrapper disposition.** To be run before this unit records completion.

## Review Evidence

**Implementation review verdict.** Not run. No implementation exists yet.

**Specification review verdict.** Not run.

**Quality review verdict.** Not run.

**Review findings and disposition.** None recorded. The registration itself is
not self-approved: it carries the user's direction as its approval source and
claims no review it has not had.

## Commit Ledger

**Commit identity.** Recorded when this unit's registration is committed.

**Commit logical unit.** One commit registering the unit; later commits per
executed plan step.

**Commit validation.** `check-document-metadata.py --mode check-changed` over
this unit's three files.

## Deferred and Blocked Items

**Deferred items.** None. The unit's whole content is its open decision.

**Blocked items.** Steps 4 and 5 are blocked on the `doc-writer` disposition
decision. Steps 2 and 3 are not blocked and can proceed.

**Deferral destination.** Not applicable; nothing is deferred out of this unit.

## Related Documents

- [Specification](./spec.md)
- [Implementation plan](./plan.md)
- [SDLC taxonomy convergence Task](../spec-0136-sdlc-taxonomy-convergence/task.md)
