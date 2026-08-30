---
profile_id: task
status: active
artifact_id: task-0155-0001
artifact_type: task
parent_ids: [SPEC-0155, plan-0155]
created: 2026-08-30
updated: 2026-08-30
---

# Full Gate Restoration

## Objective

Make `run-ci-gate.py --profile full` exit 0, so every later Task of this Spec
Package can be verified against a working gate. Plan Task 1.

## Inputs

- `tests/validation/test_document_metadata.py`, `init_git` at line 1110 and `copy_registry_contract_fixture` at line 1289.
- `scripts/lib/document_governance/identity_history.py`, `_run_git` at line 88 and its four `--is-ancestor` call sites.
- SPEC-0154 Task 5, which routed this failure here after rejecting the deadline and output-cap hypotheses.

## Work Log

Three defects stacked in one failure, each masking the next. SPEC-0154 saw only
the outermost one and could not name it, because the message it produced was
identical to four other conditions and discarded Git's own words.

| Step | Action                                                                        | Result                                                        |
| :--- | :---------------------------------------------------------------------------- | :------------------------------------------------------------ |
| 1    | Reproduced and timed the baseline                                             | `errors=1`, `RuntimeError` from the fixture helper, **114 s** |
| 2    | Neutralized `core.hooksPath` in `init_git`                                    | Defect A closed                                               |
| 3    | Re-measured                                                                   | `failures=1`, **24 s**, and the real symptom surfaced         |
| 4    | Wrote three predicate tests                                                   | 3 FAIL, `no attribute 'git_predicate'`                        |
| 5    | Gave `_run_git` an `answer_codes` set, retained stderr, added `git_predicate` | 3 OK                                                          |
| 6    | Converted all four `--is-ancestor` sites to one `require_ancestor` assertion  | Defect B closed                                               |
| 7    | Re-ran the target test                                                        | The message now names the commit and the relation             |
| 8    | Measured Option 1, `descend_from_head=True`                                   | **OK, 54.9 s**                                                |
| 9    | Measured Option 2, rename instead of repoint                                  | **OK, 53.6 s**                                                |
| 10   | Ran the whole metadata module under Option 2                                  | **261 tests, OK, 174 s**                                      |
| 11 | Ran `--profile full` to completion for the first time | **5 failures behind the one this Task was scoped to** |
| 12 | Compared each against the branch point `e2ef015e` | 3 caused by SPEC-0154, 1 predating the branch |
| 13 | Repaired all five | see the regression table below |

**The 75 `AOE-CATALOG-*` lines are not failures.** Each appears on a test line
that ends `... ok`. They are the stdout of negative-path fixtures whose test
asserts the checker emits those markers. The real count is
`Ran 287 tests ... failures=4, errors=1`.

**Correction to the SPEC-0154 closure.** That Spec Package was closed reporting
acceptance items 1 to 4 and 6 to 10 as met, with item 5 unmet and attributed
solely to the identity scan. The attribution was wrong. The gate stopped at the
identity scan and never reached the four failures behind it, three of which
SPEC-0154 itself caused. This is the third instance in this branch of one
pattern: a claim verified against the part of the gate that runs.

| Failing test | `e2ef015e` | After SPEC-0154 | Cause | Repair |
| :--- | :--- | :--- | :--- | :--- |
| `test_active_markdown_publishes_no_legacy_stage_01_or_02_path` | OK | FAIL | SPEC-0154 Task 5 wrote a legacy path literal into its own prose | Named the directories in words instead of publishing the path |
| `test_current_operations_has_exact_final_topology` | OK | FAIL | SPEC-0154 Task 3 added `Related Documents` to 16 profiles; `operations_catalog.py` pins the exact shape of 5 of them in code | Aligned the five pinned tuples |
| `test_current_repository_has_exact_canonical_spec_surface` | OK | FAIL | Package count pinned at 30; SPEC-0154 issued three | Repinned to 33 with the reason, as the prior repin did |
| `test_active_route_authority_uses_only_canonical_spec_execution_paths` | OK | ERROR | The route list reads `roles/qa.md`, which SPEC-0154 Task 1 deleted | Pointed at `policies/quality-standards.md`, which received its content |
| `test_generic_allocation_rejects_retired_reuse_and_requires_atomic_advance` | FAIL | FAIL | Predates the branch. The test pins `SPEC-0154` as its example of an unallocated identity; real work issued that number | Derived the unallocated number from the registry's high water |

**Two pinned copies of the registry contract exist, not one.**
`operations_catalog.py` carries `_OPERATIONS_PROFILE_CONTRACT`, a literal copy
of five profiles' exact field shape, so a registry edit the registry itself
accepts fails a test in an unrelated module. Stage 99 is declared the only
machine authority for required sections; a second copy in Python competes with
it. The copy is aligned here because Task 1 owns the gate, not the duplication.
**Routed to SPEC-0155 Task 4.**

**Defect A, the fixture ran the operator's commit hooks.** `core.hooksPath` is
a global Git setting on this machine, pointing at `/home/hy/.codex/git-hooks`.
Every fixture repository inherited it, so `git commit` inside a temporary
fixture ran the operator's pre-commit hook against a tree the fixture does not
own. The hook reported `${VAR}` interpolations and a `secrets.GITHUB_TOKEN`
reference in `infra/` and `.github/` as credential assignments and blocked the
commit; the helper then raised the hook's output as a fixture construction
error. No plaintext secret is involved and none was added or removed here.
`init_git` already defends against one global-config leak, `init.defaultBranch`,
with a comment explaining why. This is the same class and now sits beside it.

**Defect B, a Git verdict was read as a Git failure.** `git merge-base
--is-ancestor A B` exits 0 for true and **1 for false**; only 2 and above are
errors. `_run_git` treated every non-zero return as a scan failure. All five of
its failure branches raised the identical string `bounded Git identity scan
failed` and discarded stderr, so a true verdict of "not an ancestor" surfaced as
`configuration-error` naming neither the command nor the commits. `_run_git`
now takes an `answer_codes` set, retains stderr, and carries the return code
out; `git_predicate` reads exit 1 as `False`; and the four call sites, which
all discarded the result and were therefore assertions rather than scans,
became one `require_ancestor` helper that says which commit failed to precede
which.

**Defect C, the fixture discarded the history it had just cloned.** The target
test clones this repository so the CLI validates "against real Git history".
`copy_registry_contract_fixture` then calls `init_git(root)`, which runs
`git symbolic-ref HEAD refs/heads/main` and repoints HEAD at an **unborn**
branch, so the next `commit_all` writes a root commit and no commit of this
repository can be its ancestor. `init_git`'s own `descend_from_head` comment
describes this exact failure; the defense existed and this call site did not
use it.

**Ruling on Defect C, measured rather than reasoned.** Both repairs pass the
target test. Option 2 was kept because Option 1 binds every clone-based fixture
to `ROOT`'s HEAD at the moment the test runs, which moves during a Task that
commits. Option 2 keeps the fixture's ancestry its own. Its blast radius is
wider, 15 `init_git` call sites rather than one, which is why the whole module
was run rather than the target test alone.

**Rollback.** `git revert` of the Task 1 commit. The three edits are
independent and can be reverted individually: the `core.hooksPath` line, the
`_run_git` and `git_predicate` change with its call sites, and the `init_git`
branch handling.

**Skipped checks.** None.

## Verification Evidence

| Measure                                                 |                     Before |                                         After |
| :------------------------------------------------------ | -------------------------: | --------------------------------------------: |
| Target test outcome                                     |                 `errors=1` |                                        **OK** |
| Target test runtime                                     |                      114 s |                                          54 s |
| `--is-ancestor` call sites                              |       4, results discarded |                        **1 assertion helper** |
| Distinct messages for the 5 `_run_git` failure branches |                          1 | 2, one naming the command and carrying stderr |
| `tests.validation.test_document_metadata`               | not runnable to completion |                              **261 tests OK** |

| Command | Result |
| :--- | :--- |
| `python3 -m unittest ...test_reverse_transition_without_override_is_blocked` | **OK** |
| `python3 -m unittest tests.validation.test_document_metadata` | **261 OK** |
| `python3 -m unittest tests.lib.document_governance.test_identity_history` | **14 OK** |
| `python3 -m unittest tests.lib.document_governance.test_spec_packages` | **16 OK** |
| `python3 -m unittest tests.lib.document_governance.test_operations_catalog` | **33 OK** |
| `python3 -m unittest tests.lib.document_governance.test_taxonomy` | **17 OK** |
| `run-ci-gate.py --profile full` test set | **287 tests, OK**, from `failures=4, errors=1` |
| `generate-llm-wiki.py --write` | two snapshots regenerated |
| `run-ci-gate.py --profile full` | pending, requires the change to be tracked |
| `run-ci-gate.py --profile changed` | pending |

## Review Evidence

Pending independent review. Self-review confirmed that the three defects are
distinct and ordered: closing A changed the failure class, closing B changed the
message from an unnamed configuration error to a named precondition, and only
then was C readable without instrumentation.

## Commit Ledger

| Subject                                                                      | Paths                                                                                                                                                                    |
| :--------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fix(tests): Stop three defects from masking each other in one gate failure` | `tests/validation/test_document_metadata.py`, `tests/lib/document_governance/test_identity_history.py`, `scripts/lib/document_governance/identity_history.py`, this Task |

## Rulings

Plan rulings 1 to 7 apply. Two execution rulings were made.

1. **A fixture does not run the operator's hooks.** A temporary fixture
   repository is a sandbox, not a contribution. Inheriting `core.hooksPath`
   made a machine-level setting decide whether the suite passes, which is why
   this failure was invisible to reasoning about the repository's own contents.
2. **One error message per condition.** Five branches raising one string is not
   a bound, it is a blindfold. The repair keeps the bound and removes the
   blindfold: the failure now names the command, the exit code, and Git's own
   stderr.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
- [Governance consistency convergence](../../0154-governance-consistency-convergence/spec.md)
