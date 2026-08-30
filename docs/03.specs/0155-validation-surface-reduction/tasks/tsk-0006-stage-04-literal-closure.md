---
profile_id: task
status: completed
artifact_id: task-0155-0006
artifact_type: task
parent_ids: [SPEC-0155, plan-0155]
created: 2026-08-30
updated: 2026-08-30
---

# Stage 04 Literal Closure

## Objective

Confirm the corpus is clean, then remove the Stage 04 references that still
instruct agents rather than record history. Plan Task 6.

## Inputs

- `scripts/lib/document_governance/metadata_validator.py`, plan Task 6's named target.
- `scripts/README.md`, `tests/README.md`, `scripts/hooks/agent-event-hook.sh`.
- The eleven Stage 04 literals remaining under `scripts/`.

## Work Log

| Step | Action                                                | Result                                      |
| :--- | :---------------------------------------------------- | :------------------------------------------ |
| 1    | Ran the advisory inventory                            | **exit 0**, `invalid-status` **0**          |
| 2    | Looked for the advisory guard the plan names          | **Does not exist**; Task 4 removed it       |
| 3    | Looked for `planned_partitions`                       | **Does not exist**; Task 4 removed it       |
| 4    | Swept every Stage 04 literal under `scripts/`         | 11 found, **9 correct**, 2 defects          |
| 5    | Checked whether the wrapper enforces the README's path | It enforces `docs/03.specs/`, not Stage 04  |
| 6    | Corrected three instructions and one routing entry    | Stage 04 gone from both files               |
| 7    | Corrected `tests/README.md`                           | Structure and blocking-gate claim           |

**The plan's targets were already gone, and its premise held.** Plan Task 6
names an advisory `ProfileError` guard and a `planned_partitions` literal in
`metadata_validator.py`. Neither exists: Task 4 removed the Stage 04 literals
from that module, taking the count to zero, and no guard by that description
remains. Step 1's precondition was confirmed rather than assumed, as the plan
required: the advisory inventory exits 0 with zero `invalid-status`.

**Counting grep hits as defects was wrong, and this Task corrects that.** An
earlier reading of this branch reported "Stage 04 references in eighteen files"
as drift. Measured one by one, nine of the eleven under `scripts/` are correct
and must stay:

| Literal | Why it stays |
| :--- | :--- |
| `spec_packages.py:712`, `os.stat("04.execution")` | Asserts Stage 04 has **not** returned |
| `spec_packages.py:1094`, `git ls-tree ... docs/04.execution` | Reads a pinned historical commit |
| `check-script-manifest.py:68`, `FORBIDDEN_EVIDENCE_PREFIXES` | Forbids citing the removed stage as evidence |
| `check-document-corpus-lifecycle.py`, seven literals | Absence assertions and frozen ledger paths |

A path in an absence check and a path in a history read are not stale; they are
the mechanism that keeps the removal true.

**The two real defects were normative text, and the tooling was already
right.** `scripts/README.md` told agents to invoke the only approved all-files
wrapper with `--task docs/04.execution/tasks/YYYY-MM-DD-feature.md`. The wrapper
accepts only `docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` and exits
`EXIT_TASK` on anything else, so an agent following the README could not run it.
The second was `agent-event-hook.sh`, which routed to `execution-plan-agent` on
the keywords `stage 04` and `04.execution` and described it as "Stage 03→04";
that skill's own document already says the Plan is co-located at
`docs/03.specs/####-<slug>/plan.md`.

**`tests/README.md` claimed the blocking gate was off.** It stated the metadata
test "does not activate the changed/new blocking gate before Task 8 approval".
SPEC-0155 Task 2 brought that gate to zero violations and it is what CI
enforces. The README now states the blocking command, and states that the base
ref is computed rather than pinned, which is Task 2's ruling 1. Its `Structure`
block listed two files under one directory against an actual six directories.

**Rollback.** `git revert` of the Task 6 commit.

**Skipped checks.** None.

## Verification Evidence

| Measure                                          | Before |    After |
| :----------------------------------------------- | -----: | -------: |
| Stage 04 literals in `metadata_validator.py`     |      0 |    **0** |
| Stage 04 literals under `scripts/` that instruct |      2 |    **0** |
| Stage 04 literals under `scripts/` that record   |      9 |    **9** |
| `tests/README.md` claims contradicting CI        |      1 |    **0** |
| Documented commands that cannot run              |      1 |    **0** |

| Command                                                                                    | Result                                     |
| :----------------------------------------------------------------------------------------- | :----------------------------------------- |
| `check-document-metadata.py` (advisory, no mode)                                            | **exit 0**, `invalid-status=0`             |
| `check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"` | **violations=0**                           |
| `check-document-links.py --mode all`                                                       | **failures=0**, 561 documents              |
| `run-ci-gate.py --profile full`                                                            | pending, requires the change to be tracked |

## Review Evidence

Pending independent review. Self-review reversed an earlier claim of this
branch's own: the Stage 04 grep hits were counted as defects before they were
read, and nine of eleven turned out to be the mechanism enforcing the removal.

## Commit Ledger

| Subject                                                            | Paths                                                                                     |
| :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------ |
| `docs(scripts): Stop instructing agents to use a removed stage` | `scripts/README.md`, `tests/README.md`, `scripts/hooks/agent-event-hook.sh`, this Task |

## Rulings

Plan rulings 1 to 8 apply. Two execution rulings were made.

1. **A path literal is read before it is counted.** A reference to a removed
   stage inside an absence assertion or a history read is the removal working.
   Only a reference that instructs is a defect.
2. **When documentation and tooling disagree, the tooling is checked first.**
   The README named a path the wrapper rejects. Changing the wrapper to match
   the README would have widened an approval boundary to fit stale prose.

## Deferred Items

- The advisory full inventory remains advisory by design; making it blocking was
  plan Task 6's Step 2 against a guard that no longer exists, and the inventory
  already reports zero findings. No change is needed and none was invented.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
