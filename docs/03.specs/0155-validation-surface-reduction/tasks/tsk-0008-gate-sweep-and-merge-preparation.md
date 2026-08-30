---
profile_id: task
status: completed
artifact_id: task-0155-0008
artifact_type: task
parent_ids: [SPEC-0155, plan-0155]
created: 2026-08-30
updated: 2026-08-30
---

# Gate Sweep and Merge Preparation

## Objective

Find gate nodes left without an implementation by Tasks 3 to 7, run the full
acceptance set, and record which acceptance items are met before the branch
merges. Plan Task 8.

## Inputs

- `.github/workflow-contract.yml`, 87 gate nodes.
- `scripts/validation/ci_gate_runner.py`, which names the registered test modules.
- SPEC-0155's fourteen-item Acceptance Contract.

## Work Log

| Step | Action                                              | Result                                     |
| :--- | :-------------------------------------------------- | :----------------------------------------- |
| 1    | Counted gate nodes and resolved every entrypoint    | 53 leaf, 28 aggregate, 6 setup; **0 missing** |
| 2    | Resolved every registered test module               | 31 registered, **0 missing**                |
| 3    | Ran the acceptance commands                         | Recorded below                              |
| 4    | Measured the line-count delta                       | **-16,282**                                 |
| 5    | Measured each acceptance item rather than asserting | **10 met, 4 not**                           |
| 6    | Completed both plans; left both specs `active`      | Forced by the transition rule, see below    |

**No gate node was orphaned.** Tasks 3 and 5 removed five validator modules and
Gate 4's allowlist source. Every one of the 23 distinct entrypoints in the
workflow contract resolves, and all 31 registered test modules exist. The
removals took their registrations with them, so Step 2's removal work was empty.

**Neither Spec Package can be completed in this change, and that is the rule
working.** Measured at the merge base `9407ba9c`, SPEC-0154's and SPEC-0155's
`spec.md` are both `draft`; at HEAD both are `active`. `check-changed` compares
those two endpoints without walking the commits between, and the `spec-package`
lifecycle allows `draft` to reach only `active` or `retired`. Marking either
`completed` here would be reported as `draft -> completed`. Both plans are a
different case: their lifecycle is `execution`, which Task 2 amended to allow
`draft -> completed`, and all thirteen Tasks across the two packages are
`completed`. Both plans are closed; both specs complete in the first change
after the merge.

Plan Step 5 says to transition SPEC-0155 to `completed`. That instruction
predates Task 2's measurement of the endpoint rule and cannot be followed
without an override that is itself unreachable. The plan is wrong here and the
rule is right.

**Four acceptance items are not met, measured.**

| Item | Requirement | Measured | Disposition |
| :--- | :--- | :--- | :--- |
| 5 | `grep -rn "f259c139" docs` returns no match | **4 matches** | 3 are Spec and Task documents naming the literal as the thing to remove, which is not a violation. The one normative pin, `docs/98.archive/README.md`, is paired with `TASK10_BASELINE_COMMIT` in `archive.py`; changing only the document would make it inaccurate in the other direction. **SPEC-0157** owns both. |
| 6 | `grep -rn "04.execution" scripts` returns no match | **10 matches** | The item is wrong as written. Task 6 read each one: nine are absence assertions and pinned history reads, which are the mechanism that keeps Stage 04 removed. Deleting them would delete the enforcement. The two that instructed agents were removed. |
| 7 | The full inventory runs in blocking mode and exits 0 | Still advisory | Task 6 found no guard to remove; Task 4 had already taken it. The inventory reports zero findings, so making it blocking changes no outcome today. **SPEC-0157** owns the decision. |
| 13 | A transition override with a co-located `evidence_task` is accepted, proven by a test | **0 wiring** | No gate node or workflow passes `--transition-override-file`. Task 2's repair rule removed the need for the two Stage 98 overrides this item was written for. The mechanism is unreachable and unused. **SPEC-0157** owns retiring or wiring it. |

Item 6 is the one worth naming: an acceptance item can be wrong. Written as a
`grep` returning nothing, it treats every occurrence of a string as a defect,
and nine of the ten occurrences are the code that enforces the removal the item
exists to confirm. It was not satisfied by deleting correct code.

**Deviation, a claim about gate coverage was wrong.** Commit `db2ded51` states
"No gate checks generator freshness", citing zero `stale generated` findings in a
complete `--profile full` log. Zero findings in a passing run means the check
passed, not that it was absent. The full gate does check it, through
`generate-llm-wiki.py --check`, and it failed on this Task's own run because the
Task 6, 7, and 8 documents were authored after the last regeneration. Inferring
absence from a green log is the same error as inferring absence from a truncated
search, which this branch already recorded once. The generated outputs are
regenerated and `--check` reports both fresh.

**Rollback.** `git revert` of the Task 8 commit restores both plan statuses.

**Skipped checks.** None. `python3 -m unittest discover -s tests` was not run as
a single command because several modules require `PYTHONPATH=.` and the
registered gate supplies it; the gate's own run is the evidence.

## Verification Evidence

| Measure                                   | Spec baseline |     Measured |
| :---------------------------------------- | ------------: | -----------: |
| `scripts/**/*.py`                         |        50,640 |   **42,635** |
| `tests/**/*.py`                           |        58,553 |   **50,276** |
| Combined                                  |       109,193 |   **92,911** |
| Delta                                     |             — |  **-16,282** |
| Gate leaf nodes                           |            53 |       **53** |
| Gate aggregate nodes                      |            28 |       **28** |
| Entrypoints without an implementation     |             — |        **0** |
| Registered test modules without a file    |             — |        **0** |

| Command                                                                                    | Result                    |
| :----------------------------------------------------------------------------------------- | :------------------------ |
| `run-ci-gate.py --profile changed`                                                         | **exit 0**                |
| `run-ci-gate.py --profile full --explain`                                                  | **exit 0**, 20 validators |
| `check-script-manifest.py`                                                                 | **PASS**                  |
| `check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"` | **violations=0**          |
| `check-document-links.py --mode all`                                                       | **failures=0**, 563 docs  |
| `check-agent-governance-contract.py --mode repository --section all`                       | **PASS failures=0**       |
| `sync-provider-surfaces.sh --check`                                                        | **PASS drift=0**          |
| `git diff --exit-code`                                                                     | **clean**                 |
| `run-ci-gate.py --profile full`                                                            | recorded at commit time   |

## Review Evidence

Pending independent review. Self-review declined to mark SPEC-0155 complete: its
own Acceptance Contract has four unmet items, and the transition the plan asks
for is one the blocking rule rejects.

## Commit Ledger

| Subject                                                     | Paths                                                                          |
| :------------------------------------------------------------ | :------------------------------------------------------------------------------- |
| `chore(spec): Close both plans and record the unmet acceptance items` | `docs/03.specs/0154-*/plan.md`, `docs/03.specs/0155-*/plan.md`, this Task |

## Rulings

Plan rulings 1 to 8 apply. Two execution rulings were made.

1. **An acceptance item can be wrong, and is corrected rather than satisfied.**
   Item 6 demands that a string not appear in `scripts/`. Nine of its ten
   occurrences are absence assertions and history reads that enforce the very
   removal the item checks. Satisfying it literally would remove the
   enforcement.
2. **A Spec Package is not completed against a contract it does not meet.**
   Four items are open. Three are routed to SPEC-0157 with the reason; one is
   corrected. Recording `completed` over an open contract would make the status
   field mean nothing.

## Deferred Items

- Acceptance items 5, 7, and 13 are routed to SPEC-0157.
- SPEC-0154 and SPEC-0155 `spec.md` complete in the first change after the merge,
  when `active -> completed` is the transition the endpoint comparison sees.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
- [Script surface ownership convergence](../../0157-script-surface-ownership-convergence/spec.md)
