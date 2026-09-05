---
title: "Test and Fixture Convergence Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0004"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Test and Fixture Convergence Task

## Objective

Align test placement with production ownership, replace execution-specific
fixtures with stable contracts or builders, and prevent production code from
depending on the test tree.

## Inputs

- [SPEC-0173](../spec.md), its [implementation plan](../plan.md), and the
  canonical owners established by Tasks 0002 and 0003.
- `tests/lib/`, `tests/validation/`, `tests/fixtures/`, test support modules,
  examples, and current fixture consumers.
- The mixed-ownership modules, historical fixed assertions, one-off fixtures,
  and near-duplicate supply-chain cases listed in the Plan.

## Work Log

Task 3 aligned script and operation ownership at `174c29d9` and recorded its
focused evidence at `74a8b05e`. Task 4 became ready at `22759ba6` and now
starts from a clean worktree. No Task 4 test or fixture has been moved,
renamed, rewritten, or removed; a fixture remains eligible only when an
independent current test consumes its stable format.

## Verification Evidence

No execution evidence exists in this draft. Acceptance requires an initial
failing production-to-tests dependency check, focused RED/GREEN tests for each
move, full discovery, and orphan-fixture verification.

## Review Evidence

No implementation review has occurred. Independent review must distinguish
behavior coverage from duplicate CLI coverage and confirm that test helpers do
not become accidental semantic owners.

## Commit Ledger

No implementation commit exists. The planning-package changes are not
implementation or acceptance evidence.

## Rulings

- `tests/lib/<domain>/` verifies library behavior; `tests/validation/` verifies
  CLI, entrypoint, and execution context behavior.
- Production modules must not import from or read `tests/**`.
- Replace completed-Spec names, fixed branch tips, and historical counts with
  generic contract data unless the historical value itself is the contract.

## Deferred Items

- Performance benchmarking and runtime service execution are outside this
  Task.
- Immutable historical evidence remains unchanged.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Script and operation ownership Task](tsk-0003-script-and-operation-ownership.md)
