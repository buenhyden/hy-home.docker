---
profile_id: task
status: active
artifact_id: task-0157-0001
artifact_type: task
parent_ids: [SPEC-0157, plan-0157]
created: 2026-08-31
updated: 2026-08-31
---

# Recover and Complete Script Surface Ownership Convergence

## Objective

Revalidate the implementation discovered on the branch, complete the remaining
approved work, and close SPEC-0157 without asserting retroactive approval.

## Inputs

- Spec: SPEC-0157; Plan: plan-0157.
- Branch: codex/0157-governance-convergence-execution.
- Merge base: 703e3cf6b76fc7f9d0c4bb6ac65c6f1111b8545f.
- Recovery boundary: this Task's registration. The discovered commits are not
  retroactively approved or completed by this record.

## Work Log

| Step | Action | Result |
| :--- | :--- | :--- |
| 1 | Measured discovered branch work before Task 0 edits | git status --short --branch reported only ## codex/0157-governance-convergence-execution; the merge-base range had 12 non-merge commits and 72 files changed, 3495 insertions(+), 4403 deletions(-). |
| 2 | Activated SPEC-0157 and plan-0157; created this current Task and index link | Active recovery chain established. No transition override was used. |
| 3 | Revalidated Task 1 focused checks | Lifecycle suite and all four modes passed; shared manifest check failed on five package markers. Task 1 is reopened pending the Task 3 repair. |
| 3 | Revalidated Task 2 focused checks | Archive and lifecycle suites passed; Spec Package suite failed one fixed count. Task 2 is reopened. |
| 3 | Revalidated Task 3 focused checks | Surface ownership and workflow contract passed; manifest and full Gate failed because the five package markers are unregistered. Task 3 is reopened. |
| 4 | Recovery metadata/link checks | All three commands passed: contract violations=0, changed-document violations=0, links failures=0. |
| 5 | Commit recovery record | Pending after metadata/link checks and cached-diff review. |

### Discovered branch commits

~~~text
71cf9390 docs(plan): reconcile governance convergence execution
2a3cb9cb docs(spec): define document governance convergence
b189dc27 chore(docs): Regenerate the LLM wiki index for the moved script paths
e23d93f1 fix(tests): Order the operations suite validator tuple by the sorted manifest path
d6b7eafe refactor(scripts): Give each domain a library package and derive the standalone rule
342863ff fix(archive): Delete a dead count guard and two tautological test assertions
a4f36d99 fix(plan): Correct Task 3's move set and ownership invariant to what measurement shows
dd41a675 refactor(archive): Derive the recovery census instead of pinning it
8b4f8e9b refactor(validation): Remove sixteen orphaned corpus-lifecycle helpers
412542b0 refactor(validation): Reduce the corpus lifecycle to its four reachable modes
734ff9da fix(plan): Widen Task 1's reachability search to the workflows it missed
85af3767 docs(plan): Plan the script surface convergence as nine measured tasks
~~~

The discovered diff-stat command reported the 72-file, 3495 insertion, and
4403 deletion summary above. Its changed paths span the Task 1 lifecycle
reduction, Task 2 census derivation, Task 3 library move, their tests and gate
wiring, plus the previously authored planning and generated-reference surfaces.

## Verification Evidence

### Task 1 — reopened

Logical commits: 412542b0 and 8b4f8e9b.

~~~text
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle
Ran 116 tests in 108.517s
OK

check-public exit=0
check-contract exit=0
check-promoted exit=0
check-recovery exit=0

PYTHONPATH=. python3 scripts/validation/check-script-manifest.py
FAIL [manifest-record-missing] scripts/lib/agent_governance/__init__.py
FAIL [manifest-record-missing] scripts/lib/gate/__init__.py
FAIL [manifest-record-missing] scripts/lib/ops/__init__.py
FAIL [manifest-record-missing] scripts/lib/supply_chain/__init__.py
FAIL [manifest-record-missing] scripts/lib/target_surface/__init__.py
script_manifest_failures=5
~~~

The focused check is not fully green. It remains reopened; the recorded
manifest failure is owned by the Task 3 package-marker correction.

### Task 2 — reopened

Logical commits: dd41a675 and 342863ff.

~~~text
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive
Ran 21 tests in 31.453s
OK

PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle
Ran 116 tests in 109.165s
OK

PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_spec_packages
Ran 16 tests in 5.827s
FAILED (failures=1)
~~~

The remaining failure is the current valid-package assertion 34 != 35. Task 2
must measure and remove the actual remaining count pin, not recreate the
obsolete four-failure RED demonstration.

### Task 3 — reopened

Logical commit: d6b7eafe; follow-up ordering fix: e23d93f1.

~~~text
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership
Ran 3 tests in 0.063s
OK

PYTHONPATH=. python3 scripts/validation/check-script-manifest.py
script_manifest_failures=5

PYTHONPATH=. python3 scripts/validation/check-github-workflow-contract.py
PASS: GitHub workflow contract (workflows=7, jobs=9, actions=8)

PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full
Ran 251 tests in 134.008s
FAILED (failures=3, errors=2)
FULL exit=1
~~~

The required repair is to remove the five unnecessary __init__.py package
markers and verify namespace imports; adding five manifest rows is not allowed.

### Task 0 recovery checks

~~~text
python3 scripts/validation/check-document-metadata.py --mode check-contracts
metadata repository contracts: violations=0

python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"
metadata check-changed: selected=14 violations=0 legacy_exceptions=0 transition_overrides=0

python3 scripts/validation/check-document-links.py --mode all
document links: mode=all documents=568 links=4868 catalog_pairs_total=46 archive_direct_links_total=0 removed_template_mentions_total=0 failures=0
PASS: document link mode all
~~~

## Review Evidence

Independent review: pending.

Implementer self-review: complete. The diff is limited to the four authorized
Stage 03 documents; it activates the legal chain, records the observed RED
checks as reopened, and removes the obsolete Task 2--9 instructions identified
in the preflight rulings. git diff --check passed. No discovered implementation
is self-approved by this registration.

## Commit Ledger

| Logical unit | Commit(s) | Status |
| :--- | :--- | :--- |
| Task 1 lifecycle reduction | 412542b0, 8b4f8e9b | Reopened by the focused manifest check |
| Task 2 census derivation | dd41a675, 342863ff | Reopened by 34 != 35 |
| Task 3 library ownership move | d6b7eafe, e23d93f1 | Reopened by five package-marker manifest failures |
| Task 0 recovery record | This commit | Recovery chain and observed evidence |

## Rulings

1. SPEC-0157 remains active on this branch because its merge base is draft; no
   record here claims retroactive approval or completion.
2. Task 2 measures and fixes the actual remaining count pins.
3. Task 3 removes the five package markers and proves namespace imports rather
   than adding manifest rows.
4. Task 4 mirrors library-unit tests below tests/lib/<domain>, includes
   tests/lib/ops, and keeps validation/entrypoint tests in tests/validation.
   Agent-output evaluation modules remain validation entrypoints.
5. Task 5 uses the measured post-Task-4 unregistered module set and current
   module names rather than a stale count or predecessor list.
6. Task 6 uses tests/lib/target_surface/test_target_surface_contracts.py; Task
   9 updates ci_gate_runner.py, workflow contract, and manifest whenever split
   test module names change.

## Deferred Items

- Task 2 production repair: remove the measured Spec Package count pin.
- Task 3 production repair: remove the five unnecessary package markers.
- Task 0 metadata/link recovery checks and independent review.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Stage 03 index](../../README.md)
