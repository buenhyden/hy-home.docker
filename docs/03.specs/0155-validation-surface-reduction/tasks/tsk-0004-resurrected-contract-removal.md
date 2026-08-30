---
profile_id: task
status: completed
artifact_id: task-0155-0004
artifact_type: task
parent_ids: [SPEC-0155, plan-0155]
created: 2026-08-30
updated: 2026-08-30
---

# Resurrected Migration Contract Removal

## Objective

Stop every profile load from resurrecting a completed migration's contract out
of a pinned commit, and retire the predicates whose inputs no longer exist.
Plan Task 4, which also closes plan Task 6's Stage 04 literals.

## Inputs

- `scripts/lib/document_governance/metadata_validator.py`, `load_migration_contract` and the promoted-witness machinery.
- `scripts/validation/check-document-corpus-lifecycle.py`, 6,356 lines across 18 modes.
- `scripts/lib/document_governance/suite_registry.py`, which registers one mode.

## Work Log

| Step | Action                                                         | Result                                                     |
| :--- | :------------------------------------------------------------- | :--------------------------------------------------------- |
| 1    | Enumerated the checker's modes and their registrations         | 18 modes, **1** invoked by any gate                        |
| 2    | Resolved `DEFAULT_MIGRATION_CONTRACT`                          | A `HistoricalDocument`, not a path; the file is **absent** |
| 3    | Measured `load_promoted_transition_witnesses` on the CLI route | Returns `{}` at its own baseline                           |
| 4    | Wrote absence tests                                            | 9 FAIL                                                     |
| 5    | Removed the witness class, two predicates, and the loader      | 4 definitions                                              |
| 6    | Removed the witness logic from `validate_record`               | 27 references to **0**                                     |
| 7    | Removed `load_migration_contract` and six pinned constants     | **382 lines** in one definition                            |
| 8    | Narrowed the checker's contract read to its data               | Shape assertion gone, rows still read                      |
| 9    | Relocated two names to their sole consumer                     | Charged to one module, not every profile load              |
| 10   | Pruned `APPROVED_MIGRATION_PATHS`                              | 47 entries to **19**                                       |
| 11   | Removed `TARGET_SURFACE_DECLARED_OUTPUTS`                      | Defined once, **never read**                               |
| 12   | Removed 13 tests of the removed machinery                      |                                                            |
| 13   | Pruned the test's hand-maintained copy of the allowlist        | Same 28 paths                                              |
| 14   | Added an existence invariant to the allowlist                  |                                                            |

**What the machinery was.** `DEFAULT_MIGRATION_CONTRACT` was not a path. It was
a `HistoricalDocument` resolving
`docs/99.templates/support/document-corpus-migration-contract.yaml` out of the
pinned commit `49406580`, a file absent from the working tree. Every
`load_profiles()` call in this repository read it back out of Git and validated
its 384-line shape, including eight named migration waves whose source document,
SPEC-0153, was deleted. One caller discarded the result outright. The other,
`load_promoted_transition_witnesses`, returned `{}` on every route the CLI
takes, because its guard short-circuits when the profiles carry `_registry` and
the profiles the CLI builds always do. Measured, not inferred: called at its own
`TARGET_SURFACE_BASELINE` with CLI profiles, it returns `{}`.

This is the branch-SHA tracking the Spec Package was asked to reduce, in its
purest form: a validator resurrecting a deleted file to enforce policy about a
migration that finished.

**Where the Stage 04 literals actually were.** Plan Task 6 expected them in
`planned_partitions` inside the validator. They are in the resurrected YAML,
which maps `docs/04.execution/plans` to `docs/03.specs/####-<capability>/plan.md`
as a record of where Stage 04 content went, and the validator asserted that map
had one exact shape. Two more sets carried Stage 04 paths directly:
`TARGET_SURFACE_DECLARED_OUTPUTS`, which nothing read, and
`APPROVED_MIGRATION_PATHS`, which is read. `docs/04.execution` now appears
nowhere in the validator, so plan Task 6's second half is closed here.

**A predicate is pruned, not deleted, when part of it still binds.**
`APPROVED_MIGRATION_PATHS` held 47 paths of which 19 still resolve, all Stage 90
audit READMEs and Stage 99 operations templates. The 28 that do not, four Stage
04 routes, sixteen `ref-00xx` research files, two three-digit spec paths, and six
retired templates, were removed. The predicate keeps its live behavior.

**A third hand-maintained copy of a validator constant.** The test module
pinned the same allowlist across four `PRESERVED_*` frozensets, and exactly the
same 28 paths were dead there. This is the third instance in this Spec Package,
after the operations profile contract in Task 1 and the validator counts in Task 3. The pin is updated and an invariant added: every allowlisted path must
resolve, so the list cannot drift silently again.

**The remaining contract read is data, not policy.**
`check-document-corpus-lifecycle.py` still reads the historical contract for the
rows its wave modes iterate. What was removed is the assertion that an absent
file has one exact 384-line shape. The registered mode, `check-public`, does not
reach the read at all; it returns first.

**Deviation, this Task's first evidence table was wrong.** It recorded
`tests.validation.test_document_corpus_lifecycle` as `OK`. That reading came
from `tail -1` of the run, which showed the checker's own stdout line
`public document lifecycle: violations=0`, not the unittest verdict. The module
was reporting `FAILED (failures=3, errors=16)`. The full gate caught it on the
next run. Four defects were behind it, all mine and all from this Task:

| Defect | Cause | Repair |
| :--- | :--- | :--- |
| 16 errors | `metadata.promoted_single_hop_transition_valid` and its helper were removed while the checker still called them | Relocated both to the checker, their sole consumer |
| Same | The relocated helper referenced `metadata.TARGET_SURFACE_COMPLETION_PATH`, which `metadata_contract` never re-exported | Defined the constant locally, and corrected the route I had typed as `133-` to the real `0133-` |
| 2 failures | The narrowed contract reader raised nothing for malformed YAML, so a bad contract surfaced as `internal-error` instead of `configuration-error` | Catch `OSError`, `UnicodeError`, and `yaml.YAMLError` and raise `ProfileError` **without echoing the payload**, plus check the three mappings the modes consume |
| 1 failure | One `load_profiles(profiles_path, contract_path)` call site was missed | Dropped the removed argument |

The third is the one worth naming: narrowing the shape assertion also removed a
guarantee the tests held, that a malformed contract fails cleanly and never
echoes its content. Removing dead policy must not remove live safety, and the
redaction test is what caught the difference.

**Verification order ruling.** A unittest verdict is read from the `Ran N` and
`OK`/`FAILED` lines, never from `tail -1`, because a module under test can print
to stdout after the summary.

**Rollback.** `git revert` of the Task 4 commit.

**Skipped checks.** None.

## Verification Evidence

| Measure                                           | Before |      After |
| :------------------------------------------------ | -----: | ---------: |
| `scripts/**/*.py`                                 | 43,992 | **43,363** |
| `tests/**/*.py`                                   | 52,172 | **51,400** |
| Git reads of a deleted file per `load_profiles()` |      1 |      **0** |
| `docs/04.execution` literals in the validator     |      4 |      **0** |
| `APPROVED_MIGRATION_PATHS` entries                |     47 |     **19** |
| Allowlisted paths that do not resolve             |     28 |      **0** |
| Promoted-witness references in the validator      |     27 |      **0** |

| Command                                                                                                 | Result                                            |
| :------------------------------------------------------------------------------------------------------ | :------------------------------------------------ |
| `check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"`              | **violations=0**                                  |
| `check-document-corpus-lifecycle.py --mode check-public`                                                | **violations=0**                                  |
| `--mode {check-contract,check-promoted,check-full,check-recovery,check-archive,check-directory-budget}` | all run, `check-recovery` still resolves 276 rows |
| `python3 -m unittest tests.validation.test_document_metadata`                                           | **249 OK**                                        |
| `python3 -m unittest tests.lib.document_governance.test_registry`                                       | **48 OK**                                         |
| `python3 -m unittest tests.lib.document_governance.test_metadata_validator`                             | **OK**                                            |
| `python3 -m unittest tests.validation.test_document_corpus_lifecycle` | **153 OK**, after the four repairs recorded above |
| `run-ci-gate.py --profile full`                                                                         | pending, requires the change to be tracked        |

## Review Evidence

Pending independent review. Self-review confirmed by measurement, not reading,
that the only consumer of the removed contract returned `{}` on the CLI route
before any code was deleted.

## Commit Ledger

| Subject                                                                                 | Paths                                                                                                                                                                                                                                                                               |
| :-------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `refactor(validation): Stop resurrecting a finished migration's contract on every load` | `scripts/lib/document_governance/metadata_validator.py`, `scripts/lib/document_governance/metadata_contract.py`, `scripts/validation/check-document-corpus-lifecycle.py`, `tests/validation/test_document_metadata.py`, `tests/lib/document_governance/test_registry.py`, this Task |

## Rulings

Plan rulings 1 to 8 apply. Three execution rulings were made.

1. **A predicate is pruned to what still binds.** Deleting
   `APPROVED_MIGRATION_PATHS` outright would have dropped 19 live documents from
   a real exemption. Keeping all 47 preserved 28 references to deleted paths.
   Neither is correct; the measured intersection is.
2. **A pin that can drift gets an invariant, not just a new value.** Three
   hand-maintained copies of validator state have now gone stale in this Spec
   Package. Updating the number is the smaller half of the fix.
3. **Data may be read from history; policy may not be enforced from it.** The
   wave modes still read the historical contract's rows. What was removed is the
   assertion that a deleted file conforms to a shape defined by a deleted Spec.

## Deferred Items

- 14 of the checker's 18 modes remain unreachable from any registered gate. They
  run, and their removal is a larger cut than this Task's invariant-by-invariant
  scope allows. No Spec Package owns it yet.
- `_native_migration_compaction_witness` remains, unreachable in effect since
  Task 2. Plan Task 5 owns its removal.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
