---
profile_id: task
status: completed
artifact_id: task-0155-0003
artifact_type: task
parent_ids: [SPEC-0155, plan-0155]
created: 2026-08-30
updated: 2026-08-30
---

# SPEC-0137 Disposition and Gate Retirement

## Objective

Decide SPEC-0137's disposition from its own Task evidence, retire the gate
modules that disposition releases, and remove the link-gate exemption that was
waiting on it. Plan Task 3.

## Inputs

- `docs/03.specs/0137-agentic-research-pack-rebuild/` and its four Tasks.
- `scripts/lib/document_governance/suite_registry.py`, `scripts/manifest.yaml`, `tests/validation/test_ci_gate_runner.py`.
- `scripts/validation/check-document-links.py`, `DEFERRED_PREFIXES`.

## Work Log

| Step | Action                                                       | Result                                                                 |
| :--- | :----------------------------------------------------------- | :--------------------------------------------------------------------- |
| 1    | Read the four SPEC-0137 Task states                          | 3 `cancelled`, 1 `active`                                              |
| 2    | Read the `active` Task's blocking condition                  | Waits on **SPEC-0153**, which is deleted                               |
| 3    | Measured each gate module's consumers                        | **No consumer** outside its own tests, manifest row, and suite binding |
| 4    | Removed three modules and three tests                        | **13,504 lines**                                                       |
| 5    | Removed their suite, manifest, and entrypoint registrations  | 85 manifest entries to **82**                                          |
| 6    | Repinned two validator counts with their reasons             | 35 to 32, 12 to 10                                                     |
| 7    | Dispositioned SPEC-0137 and cancelled `tsk-0004`             | `active` to `completed`                                                |
| 8    | Removed `DEFERRED_PREFIXES`                                  | 159 dead links surfaced                                                |
| 9    | Aligned RES-0001 leaf statuses with its `superseded` README  | 159 to **110**                                                         |
| 10   | Delinked 94 distinct targets across 21 files                 | 110 to **1**                                                           |
| 11   | Delinked one out-of-repository reference                     | **0**                                                                  |
| 12   | Rewrote the selection test to assert the exemption's absence | 39 OK                                                                  |

**The disposition was decided from Task evidence, as the plan required.**
`tsk-0004` states that "final acceptance and integration remain deferred until
SPEC-0153 Task 9 has independently established and merged its Stage 90 structure
into `main`". SPEC-0153 was deleted; `docs/98.archive/migrations/0003` is its
record. The condition can never be met, and the working branch the Task names,
`codex/0137-agentic-research-refresh`, no longer exists. The Task is `cancelled`
with the three that preceded it.

The Spec is `completed` rather than `retired` because its deliverable arrived:
the 21-file pack is present at
`docs/90.references/research/0002-agentic-engineering-research-pack/` carrying
`RES-0002` with `status: active`. The plan was abandoned; the product was not.
Both facts are stated in the Spec's own Overview.

**The removed count is the honest one.** The Spec measured 13,032 lines; the
actual removal is 13,504, because the module and test line counts were remeasured
here rather than carried forward.

**A test already knew one module could never run.** The note behind the pinned
validator count said `gate2_claim_review_contract.py` "owns the `document-contract`
suite and CI does not invoke it, because the Gate 2 evidence sections it reads
have never been authored, so it fails closed on a subject that does not yet
exist", and then raised the count to accommodate it. This Task lowered the count
by removing the module instead. Both pinned counts now name the removal and the
value they replace.

**The 159 dead links resolved in two moves, not one.** RES-0001 declared itself
`superseded` in its README while 19 of its 20 leaves declared `status: active`, so
the pack claimed to be retired and its members claimed to be current routes.
Aligning the leaves with the README removed 49 findings by the status rule
SPEC-0154 already established, without touching a single link. The remaining 110
are in the active pack RES-0002 and were delinked in the established form, the
label kept and the retired path stated inline. One escaped the repository
entirely, `../../../../../../.gemini/settings.json`, six levels up to a directory
that does not exist for a provider Stage 00 does not support.

**Deviation, a `git stash -u` left a mixed state.** Step 4's verification tried
to compare against the pre-Task tree with `git stash -q -u`. It failed on
`infra/secrets/certs` with a permission error after creating the stash but before
cleaning the worktree, so the subsequent `git stash pop` conflicted. No work was
lost: `git diff stash@{0}` was empty, proving the stash duplicated the worktree
byte for byte, and the patch was saved before the stash was dropped. The
comparison was then done in a separate clone instead. **`git stash -u` is not
used in this repository**; it tries to move untracked files under `infra/secrets/`
that the agent cannot read.

**The four `test_validator_entrypoints` failures are environmental.** They report
`ModuleNotFoundError: No module named 'scripts'` from subprocess `--help` runs and
reproduce at the pre-Task commit in a clean clone. `PYTHONPATH=. python3 -m
unittest tests.validation.test_validator_entrypoints` passes. The registered gate
sets `PYTHONPATH`; a bare module invocation does not.

**Rollback.** `git revert` of the Task 3 commit restores all six modules, their
registrations, the two pinned counts, the link-gate exemption, and the SPEC-0137
and RES-0001 statuses.

**Skipped checks.** None.

## Verification Evidence

| Measure                                           |             Before |                   After |
| :------------------------------------------------ | -----------------: | ----------------------: |
| Lines under `scripts/validation/` and their tests |            +13,504 |             **removed** |
| `scripts/manifest.yaml` entries                   |                 85 |                  **82** |
| Registered validators                             |                 35 |                  **32** |
| Validators with no execution context              |                 12 |                  **10** |
| Link-gate path exemptions                         |         2 prefixes |                   **0** |
| Documents the link gate reads                     |                534 |                 **557** |
| Link-gate failures                                | 0, with 159 hidden | **0, with none hidden** |

| Command                                                                                    | Result                                     |
| :----------------------------------------------------------------------------------------- | :----------------------------------------- |
| `check-document-links.py --mode all`                                                       | **failures=0**, 557 documents, 4,843 links |
| `check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"` | **violations=0**                           |
| `check-script-manifest.py`                                                                 | **PASS**                                   |
| `python3 -m unittest tests.validation.test_ci_gate_runner`                                 | **30 OK**                                  |
| `python3 -m unittest tests.validation.test_ci_gate_contract`                               | **13 OK**                                  |
| `PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_links`                | **39 OK**                                  |
| `PYTHONPATH=. python3 -m unittest tests.validation.test_validator_entrypoints`             | **3 OK**                                   |
| `run-ci-gate.py --profile full`                                                            | pending, requires the change to be tracked |

## Review Evidence

Pending independent review. Self-review confirmed that no removed module had a
consumer outside its own registration, measured before deletion rather than
after.

## Commit Ledger

| Subject                                                                                 | Paths                                                                                                                                                                                                                                                                                    |
| :-------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `refactor(validation): Retire 13,504 lines of gates for a deletion that never happened` | `scripts/validation/`, `tests/validation/`, `scripts/manifest.yaml`, `scripts/lib/document_governance/suite_registry.py`, `scripts/validation/check-document-links.py`, `tests/lib/document_governance/test_links.py`, `docs/03.specs/0137-*`, `docs/90.references/research/`, this Task |

## Rulings

Plan rulings 1 to 7 apply. Three execution rulings were made.

1. **A Spec Package is dispositioned on its deliverable, not only on its plan.**
   SPEC-0137's four Tasks are all cancelled and its product is present and
   active. Recording it `retired` would erase 21 tracked documents from the
   record of how they arrived.
2. **A pack's status binds its members.** RES-0001 declared itself `superseded`
   while its leaves declared themselves current. Aligning them removed 49 dead
   links without editing a link, because the status rule already covers a
   document that records a past observation.
3. **`git stash -u` is not used in this repository.** It attempts to move
   untracked files under `infra/secrets/` that the agent cannot read, and a
   partial failure leaves the worktree and the stash both holding the work.
   Compare against a separate clone instead.

## Deferred Items

- The old pack RES-0001 is still present. SPEC-0137 staged its deletion; that
  deletion is not part of this disposition and no Spec Package currently owns it.
- `_native_migration_compaction_witness` remains, now unreachable in effect.
  Plan Task 5 owns its removal.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
- [Agentic research pack rebuild](../../0137-agentic-research-pack-rebuild/spec.md)
