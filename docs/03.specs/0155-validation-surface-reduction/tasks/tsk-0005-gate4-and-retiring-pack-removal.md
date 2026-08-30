---
profile_id: task
status: completed
artifact_id: task-0155-0005
artifact_type: task
parent_ids: [SPEC-0155, plan-0155]
created: 2026-08-30
updated: 2026-08-30
---

# Gate 4 and Retiring Pack Removal

## Objective

Retire the old-path gate and delete the pack it guarded, then narrow the
reference rule that made a completed migration's targets permanent. Unplanned;
opened when plan Task 5's premise failed measurement and the full gate surfaced
Gate 4 as the only remaining failure.

## Inputs

- `scripts/validation/old_path_gate_contract.py` and `check-old-path-gate.py`, plus their tests.
- `docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md`, the allowlist source.
- `docs/90.references/research/0001-agentic-research-pack-refresh/`, the retiring pack.
- `scripts/lib/document_governance/references.py`, the Task 9 migration rules.

## Work Log

| Step | Action                                                        | Result                                         |
| :--- | :------------------------------------------------------------ | :--------------------------------------------- |
| 0    | Measured plan Task 5's premise                                | **Wrong for two of three modules**             |
| 1    | Read the full gate verdict from `FULL exit=`                  | 13 modules OK, **1** failure: Gate 4           |
| 2    | Traced Gate 4's allowlist to its owning document              | A `cancelled` Task, **2.4 MB**                 |
| 3    | Removed the two Gate 4 modules and their test                 | **1,958 lines**                                |
| 4    | Removed suite, manifest, and entrypoint registrations         | 82 manifest entries to **80**                  |
| 5    | Repinned two validator counts with their reasons              | 32 to 30, 10 to 9                              |
| 6    | Deleted the RES-0001 pack                                     | 20 documents, **980 KB**                       |
| 7    | Removed the LLM wiki generator's retiring-pack prefix         | Constant plus an 82-line test module           |
| 8    | Deleted the 2.4 MB allowlist Task and delinked four documents | Link gate **failures=0**                       |
| 9    | Set `plan-0137` to `cancelled`                                | Package now internally consistent              |
| 10   | Wrote `tombstone-0158` and advanced the identity space        | `high_water` 157 to 158                        |
| 11   | Narrowed two reference rules against failing tests            | 23 blocking violations to **0**                |
| 12   | Repaired two pre-existing failures in an unregistered module  | `test_generate_llm_wiki` 17 OK                 |

**Plan Task 5's premise did not survive measurement.** The plan reads that of
1,499 lines across `git_provenance.py`, `identity_history.py`, and
`provenance_policy.py`, "the surviving behavior is resolving that tuple to a Git
blob" and "everything else exists for a design the Spec records as already
superseded". Measured:

| Module               | Lines | Production consumers                                   | Registered gate |
| :------------------- | ----: | :----------------------------------------------------- | :-------------- |
| `git_provenance`     |   563 | `archive.py`, `metadata_validator.py`, three checkers   | **yes**         |
| `identity_history`   |   613 | `metadata_validator.py`                                 | **yes**         |
| `provenance_policy`  |   373 | `check-document-corpus-lifecycle.py --mode check-recovery` | **no**       |

`HistoricalDocument` alone has five production consumers, and
`identity_history` runs on every full gate through
`ci_gate_runner.py:568`, which passes `--history-scope full`. Collapsing the
three as written would have deleted live gate behavior. That is the same
mistake Task 4 made and the reason plan ruling 9 exists, so the plan was not
followed literally. Provenance narrowing is re-scoped and deferred below.

**The gate's own verdict, read correctly.** The background run reported shell
exit 0 while the gate itself reported `FULL exit=1`. Thirteen unittest modules
passed; the single failure was Gate 4 reporting two unallowlisted literals at
`tests/lib/document_governance/test_links.py:894` and `:902`. Those literals
were introduced by Task 3, which rewrote that test to assert the link-gate
exemption's absence and wrote the retired pack's path into the source to do it.

**What Gate 4 was.** Its allowlist lives in
`docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md`, a
`cancelled` Task of 2.4 MB, which is past the link checker's 2 MiB ceiling: no
validator in this repository can read the document that grants the gate's
exemptions. The table carries an interpretation it adopted on 2026-08-18, its
own supersession notice, the amendment that replaced it, an unenforceable
procedural constraint, and this sentence about the constraint:

> "The checker cannot see who settled a row and nothing detects a violation, so
> a green run is not evidence"

The gate existed to keep references off RES-0001 so the pack could be deleted.
The pack was never deleted, SPEC-0137 is dispositioned, and its Tasks are all
cancelled. Both were removed together, on the operator's decision.

**Three mechanisms existed only to route around one pack.** The link gate's
`DEFERRED_PREFIXES`, removed in Task 3; the LLM wiki generator's
`RETIRING_PACK_PREFIX`, whose comment states it exists because "a regeneration
without it injects 20 clickable retiring-pack links into the index and gate 4's
hard `clickable_links=0` fails"; and Gate 4 itself. Deleting the pack removed
the subject all three guarded.

**A rename that happened stays a rename.** Deleting the pack made the frozen
Task 9 ledger report `migration-target-missing` twenty times and
`package-missing` once, because `validate_current_references` read the ledger as
a permanence guarantee: every target it names must exist forever. The available
repair was to rewrite twenty `rename` rows as `delete` and repin the
`105 renames / 11 deletions` assertion. That was rejected. The rename did
happen; the deletion is a separate later event, and Stage 98 already owns that
record. The rule now consults `tombstoned_paths(root)` and skips a target a
tombstone retires, matching on whole path components so one pack tombstone
covers its leaves and never covers a sibling with a longer name. A target
missing with no tombstone still fails, asserted directly.

**Two pre-existing failures in a module no gate runs.**
`tests.validation.test_generate_llm_wiki` was failing on `main`: it pinned 43
script paths against a live 39, and its fixture asserted
`docs/04.execution/plan.md` classifies as "Active stage docs" after Stage 04 was
removed on 2026-08-29. Neither was caused here, verified by measurement: the set
holds only `.sh` files plus the generator and five companions, and the two `.py`
validators Gate 4 took were never members. Both are repaired; the module's
registration belongs to plan Task 8.

**Rollback.** `git revert` of the Task 5 commit restores Gate 4, the RES-0001
pack, the allowlist Task, the generator prefix, both reference rules, and the
registry identity space.

**Skipped checks.** None.

## Verification Evidence

| Measure                                        |  Before |    After |
| :--------------------------------------------- | ------: | -------: |
| `scripts/**/*.py`                              |  43,363 | **42,613** |
| `tests/**/*.py`                                |  51,400 | **50,263** |
| `scripts/manifest.yaml` entries                |      82 |   **80** |
| Registered validators                          |      32 |   **30** |
| Validators with no execution context           |      10 |    **9** |
| Tracked Markdown under `docs/`                 |     603 |  **583** |
| Mechanisms routing around the retiring pack    |       2 |    **0** |
| Governance documents past the checker ceiling  |       1 |    **0** |

| Command                                                                                    | Result                            |
| :----------------------------------------------------------------------------------------- | :-------------------------------- |
| `check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"` | 23 to **violations=0**            |
| `check-document-links.py --mode all`                                                       | **failures=0**, 560 documents     |
| `check-script-manifest.py`                                                                 | **PASS**                          |
| `python3 -m unittest tests.lib.document_governance.test_references`                        | **19 OK**, 2 written RED first    |
| `python3 -m unittest tests.validation.test_ci_gate_runner`                                 | **30 OK**                         |
| `python3 -m unittest tests.lib.document_governance.test_registry`                          | **48 OK**                         |
| `python3 -m unittest tests.lib.document_governance.test_links`                             | **39 OK**                         |
| `python3 -m unittest tests.validation.test_generate_llm_wiki`                              | 2 FAIL to **17 OK**               |
| `python3 -m unittest tests.validation.test_validator_entrypoints`                          | **3 OK**                          |
| `run-ci-gate.py --profile full`                                                            | pending, requires tracked change  |

## Review Evidence

Pending independent review. Self-review measured plan Task 5's premise before
acting on it and found it wrong, which is the only reason the three provenance
modules are still present.

## Commit Ledger

| Subject                                                                | Paths                                                                                                                                                                                                        |
| :--------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `refactor(validation): Retire gate 4 and the pack three mechanisms routed around` | `scripts/validation/`, `tests/validation/`, `scripts/manifest.yaml`, `scripts/lib/document_governance/suite_registry.py`, `scripts/lib/document_governance/references.py`, `scripts/knowledge/generate-llm-wiki.py`, `docs/90.references/`, `docs/98.archive/tombstones/90.references/`, `docs/03.specs/0137-*`, `docs/99.templates/registry.json`, this Task |

## Rulings

Plan rulings 1 to 8 apply. Four execution rulings were made.

1. **A plan step is measured before it is executed.** Plan Task 5 named 1,499
   lines as dead. Two of the three modules run on every full gate. A plan is
   evidence of intent, not of fact.
2. **A gate whose exemptions live in a document no validator can read is not a
   gate.** Gate 4's allowlist is 2.4 MB, past the link checker's ceiling, in a
   `cancelled` Task that states its own green run is not evidence.
3. **History is not rewritten to satisfy a present rule.** Twenty rename rows
   stay renames. The later deletion is recorded where the repository already
   records deletions, and the rule was narrowed to read that record.
4. **A pre-existing failure found while passing through is repaired and
   attributed, not inherited silently.** Two assertions in an unregistered
   module were stale before this branch; both are fixed and the measurement
   showing they are not mine is recorded.

## Deferred Items

- Provenance narrowing, plan Task 5's real scope: `provenance_policy.py` (373
  lines) is reachable only from `check-recovery`, which no gate registers, and
  `archive.py` carries `TASK10_BASELINE_COMMIT` with
  `APPROVED_BASELINE_RECOVERY_PATHS`, 14 paths of which **0** exist, resurrected
  from a pinned commit. `docs/98.archive/README.md` still pins `f259c139` as a
  permanent recovery procedure while all 42 tombstones carry 17 other commits
  and neither migration uses it. This is the SHA-tracking reduction the Spec
  owns, re-scoped away from the two live modules.
- `_native_migration_compaction_witness` remains, unreachable in effect.
- Registering `tests.validation.test_generate_llm_wiki` in a gate so its pins
  cannot drift again. Plan Task 8.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
- [Agentic research pack rebuild](../../0137-agentic-research-pack-rebuild/spec.md)
