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
| 3a | Revalidated Task 1 focused checks | Lifecycle suite and all four modes passed; shared manifest check failed on five package markers. Task 1 is reopened pending the Task 3 repair. |
| 3b | Revalidated Task 2 focused checks | Archive and lifecycle suites passed; Spec Package suite failed one fixed count. Task 2 is reopened. |
| 3c | Revalidated Task 3 focused checks | Surface ownership and workflow contract passed; manifest and full Gate failed because the five package markers are unregistered. Task 3 is reopened. |
| 4 | Recovery metadata/link checks | All three commands passed: contract violations=0, changed-document violations=0, links failures=0. |
| 5 | Committed recovery record | 923b2765 docs(spec): Activate script surface convergence with recovered evidence. |
| 6 | Applied review round 1 corrections | Plan activated; complete pre-Task-0 diff-stat captured; completed bookkeeping fixed; manifest snippets and library ownership contract corrected. |
| 7 | Revalidated Task 1 implementation at `dd665618` | Consumer inventory resolves exactly four reachable modes (`check-public`, `check-contract`, `check-promoted`, `check-recovery`). The lifecycle suite, all four modes, and the workflow contract are GREEN. The shared manifest bundle is RED only for five Task 3-owned package markers; no Task 1 production change or duplicate production commit was made. |
| 8 | Repaired the remaining Task 2 Spec Package count pin | Directly observed the existing `34 != 35` failure and the new targeted guard RED. Replaced the pin with the loader-to-directory set relation; targeted guard plus archive, lifecycle, and Spec Package suites are GREEN. Independent review remains pending. |

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

### Exact discovered diff-stat before Task 0

The following is the complete output of git diff --stat
703e3cf6b76fc7f9d0c4bb6ac65c6f1111b8545f...71cf939029b18140bbbb4e86af6e50d8f7187347:

~~~text
 .github/CODEOWNERS                                 |    2 +-
 .github/workflow-contract.yml                      |   87 +-
 .github/workflows/document-corpus-lifecycle.yml    |   18 -
 .../plan.md                                        | 1490 ++++++++++++++
 .../spec.md                                        |   21 +-
 .../plan.md                                        | 1126 +++++++++++
 .../spec.md                                        |  342 ++++
 docs/03.specs/README.md                            |    5 +
 .../runbook.md                                     |    8 +-
 .../README.md                                      |    8 +-
 .../0078-security-automation-readiness/README.md   |    2 +-
 .../data/0082-llm-wiki-index/README.md             |    7 +-
 .../agent-model-selection.md                       |    4 +-
 .../ai-agent-catalogs.md                           |    2 +-
 .../memory-hierarchy.md                            |    6 +-
 .../scope-application-matrix.md                    |    2 +-
 docs/99.templates/registry.json                    |    2 +-
 scripts/README.md                                  |   23 +-
 scripts/lib/agent_governance/__init__.py           |    1 +
 .../agent_governance}/agent_governance_contract.py |    0
 scripts/lib/document_governance/archive.py         |   17 -
 .../lib/document_governance/metadata_validator.py  |    7 +-
 .../lib/document_governance/provenance_policy.py   |  373 ----
 scripts/lib/document_governance/references.py      |    2 +-
 scripts/lib/document_governance/suite_registry.py  |   34 +-
 scripts/lib/gate/__init__.py                       |    1 +
 .../{validation => lib/gate}/ci_gate_adapters.py   |    2 +-
 .../{validation => lib/gate}/ci_gate_contract.py   |    1 +
 .../gate}/github_workflow_contract.py              |    4 +-
 scripts/lib/ops/__init__.py                        |    1 +
 .../ops}/rehearse-postgres-logical-upgrade.sh      |    2 +-
 .../{validation => lib/ops}/validate-harness.sh    |    2 +-
 scripts/lib/supply_chain/__init__.py               |    1 +
 .../supply_chain}/grype_db_seed.py                 |    0
 scripts/lib/target_surface/__init__.py             |    1 +
 .../target_surface}/target_surface_contract.py     |    0
 .../target_surface_delta_contract.py               |    5 +-
 scripts/manifest.yaml                              |  288 ++-
 scripts/operations/provider_surface_renderer.py    |    7 +-
 scripts/security/seed-grype-db-cache.sh            |    2 +-
 .../security/verify-sample-service-supply-chain.sh |    2 +-
 .../validation/check-agent-governance-contract.py  |    8 +-
 .../validation/check-document-corpus-lifecycle.py  | 1284 +-----------
 .../validation/check-github-workflow-contract.py   |   10 +-
 .../validation/check-storybook-contract.sh         |    6 +-
 .../validation/check-target-surface-contract.py    |    2 +-
 .../check-target-surface-delta-contract.py         |    2 +-
 .../validation/ci_gate_runner.py                   |    5 +-
 .../generate-security-automation-readiness.sh      |    4 +-
 tests/lib/document_governance/test_archive.py      |   54 +-
 tests/lib/document_governance/test_links.py        |    4 +-
 .../document_governance/test_metadata_validator.py |    2 +-
 .../test_operations_taxonomy.py                    |   10 +-
 .../test_provenance_policy.py                      |  289 ---
 tests/lib/document_governance/test_registry.py     |    4 +-
 .../lib/document_governance/test_suite_registry.py |    2 +-
 tests/lib/test_surface_ownership.py                |   61 +
 tests/validation/test_agent_governance_contract.py |    2 +-
 tests/validation/test_ci_gate_adapters.py          |    2 +-
 tests/validation/test_ci_gate_contract.py          |    2 +-
 tests/validation/test_ci_gate_runner.py            |   58 +-
 tests/validation/test_document_corpus_lifecycle.py | 2122 +-------------------
 tests/validation/test_github_workflow_contract.py  |    7 +-
 tests/validation/test_grype_db_seed.py             |    2 +-
 .../test_postgres_logical_upgrade_rehearsal.py     |   14 +-
 .../test_reference_stage_repo_contract.py          |    2 +-
 tests/validation/test_script_manifest.py           |    8 +-
 tests/validation/test_supply_chain_policy.py       |    2 +-
 tests/validation/test_target_surface_contracts.py  |    2 +-
 .../test_target_surface_delta_contracts.py         |    4 +-
 .../validation/test_tech_stack_version_contract.py |    4 +-
 tests/validation/test_validator_entrypoints.py     |   12 +-
 72 files changed, 3495 insertions(+), 4403 deletions(-)
~~~

## Verification Evidence

### Task 1 — revalidated; shared manifest bundle pending Task 3

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

The following complete caller inventory was recovered read-only from
`412542b0^`, the production predecessor of the discovered lifecycle-reduction
commit. It is historical discovered evidence, not retroactive approval. It
records every line from the four Step 1 consumer searches.

~~~text
=== suite registry ===
412542b0^:scripts/lib/document_governance/suite_registry.py:41:        PurePosixPath("scripts/validation/check-document-corpus-lifecycle.py"): "document-lifecycle",
412542b0^:scripts/lib/document_governance/suite_registry.py:90:        "check-document-corpus-lifecycle.py": ("--mode", "check-public"),
=== workflow contract leaves ===
leaf.local-document-corpus-contract -> --mode check-contract
leaf.local-document-corpus-promoted -> --mode check-promoted
=== workflow run lines ===
412542b0^:.github/workflows/document-corpus-lifecycle.yml:34:        run: python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
412542b0^:.github/workflows/document-corpus-lifecycle.yml:36:        run: python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-promoted
412542b0^:.github/workflows/document-corpus-lifecycle.yml:42:            python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-impacted --base-ref HEAD~1
412542b0^:.github/workflows/document-corpus-lifecycle.yml:47:        run: python3 scripts/validation/check-document-corpus-lifecycle.py --mode report-full
412542b0^:.github/workflows/document-corpus-lifecycle.yml:53:          python3 scripts/validation/check-document-corpus-lifecycle.py --mode report-duplicates --output "$report_path"
=== every other caller in the repository ===
412542b0^:.github/workflow-contract.yml:952:      "entrypoint": "scripts/validation/check-document-corpus-lifecycle.py",
412542b0^:.github/workflow-contract.yml:1031:      "entrypoint": "scripts/validation/check-document-corpus-lifecycle.py",
412542b0^:.github/workflows/document-corpus-lifecycle.yml:34:        run: python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract
412542b0^:.github/workflows/document-corpus-lifecycle.yml:36:        run: python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-promoted
412542b0^:.github/workflows/document-corpus-lifecycle.yml:42:            python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-impacted --base-ref HEAD~1
412542b0^:.github/workflows/document-corpus-lifecycle.yml:47:        run: python3 scripts/validation/check-document-corpus-lifecycle.py --mode report-full
412542b0^:.github/workflows/document-corpus-lifecycle.yml:53:          python3 scripts/validation/check-document-corpus-lifecycle.py --mode report-duplicates --output "$report_path"
412542b0^:scripts/lib/document_governance/references.py:49:    pathlib.PurePosixPath("scripts/validation/check-document-corpus-lifecycle.py"),
412542b0^:scripts/lib/document_governance/suite_registry.py:41:        PurePosixPath("scripts/validation/check-document-corpus-lifecycle.py"): "document-lifecycle",
412542b0^:scripts/lib/document_governance/suite_registry.py:90:        "check-document-corpus-lifecycle.py": ("--mode", "check-public"),
412542b0^:scripts/manifest.yaml:130:  - scripts/validation/check-document-corpus-lifecycle.py
412542b0^:scripts/manifest.yaml:155:  - scripts/validation/check-document-corpus-lifecycle.py
412542b0^:scripts/manifest.yaml:188:  - scripts/validation/check-document-corpus-lifecycle.py
412542b0^:scripts/manifest.yaml:229:  - scripts/validation/check-document-corpus-lifecycle.py
412542b0^:scripts/manifest.yaml:277:  - scripts/validation/check-document-corpus-lifecycle.py
412542b0^:scripts/manifest.yaml:605:- path: scripts/validation/check-document-corpus-lifecycle.py
412542b0^:scripts/validation/check-document-corpus-lifecycle.py:2257:            generated_by="check-document-corpus-lifecycle.py",
412542b0^:scripts/validation/check-document-corpus-lifecycle.py:2313:        generated_by="check-document-corpus-lifecycle.py",
412542b0^:scripts/validation/ci_gate_runner.py:515:                if item.path.name in {"check-document-metadata.py", "check-document-corpus-lifecycle.py"}
412542b0^:scripts/validation/ci_gate_runner.py:517:                else () if item.path.name in {"check-document-metadata.py", "check-document-corpus-lifecycle.py"}
412542b0^:tests/lib/document_governance/test_links.py:20:LIFECYCLE_CLI = ROOT / "scripts/validation/check-document-corpus-lifecycle.py"
412542b0^:tests/lib/document_governance/test_taxonomy.py:512:                "scripts/validation/check-document-corpus-lifecycle.py",
412542b0^:tests/validation/test_ci_gate_runner.py:896:                for name in ("check-document-metadata.py", "check-document-corpus-lifecycle.py"):
412542b0^:tests/validation/test_document_corpus_lifecycle.py:31:SCRIPT = ROOT / "scripts/validation/check-document-corpus-lifecycle.py"
412542b0^:tests/validation/test_document_corpus_lifecycle.py:1016:            generated_by="check-document-corpus-lifecycle.py",
412542b0^:tests/validation/test_document_metadata.py:1373:            "generated_by": "scripts/validation/check-document-corpus-lifecycle.py",
412542b0^:tests/validation/test_document_metadata.py:1659:                    "scripts/validation/check-document-corpus-lifecycle.py",
412542b0^:tests/validation/test_document_metadata.py:1661:                    "scripts/validation/check-document-corpus-lifecycle.py",
412542b0^:tests/validation/test_document_metadata.py:1671:                "scripts/validation/check-document-corpus-lifecycle.py",
412542b0^:tests/validation/test_document_metadata.py:1675:                "scripts/validation/check-document-corpus-lifecycle.py",
412542b0^:tests/validation/test_script_manifest.py:103:    "scripts/validation/check-document-corpus-lifecycle.py": "check-write",
412542b0^:tests/validation/test_target_surface_contracts.py:18:LIFECYCLE_CHECKER = ROOT / "scripts/validation/check-document-corpus-lifecycle.py"
412542b0^:tests/validation/test_target_surface_contracts.py:311:            "generated_by": "check-document-corpus-lifecycle.py",
412542b0^:tests/validation/test_validator_entrypoints.py:18:    "scripts/validation/check-document-corpus-lifecycle.py",
~~~

The suite binding, the two workflow-contract leaves, and the five workflow run
lines are callers. `scripts/lib/document_governance/references.py`, manifest
rows, `generated_by` fields, CI-runner path handling, and every `tests/` match
above are reference, configuration, or test evidence rather than an additional
mode caller. The historical reachable set was the six modes `check-public`,
`check-contract`, `check-promoted`, `check-impacted`, `report-full`, and
`report-duplicates`.

At the Task 1 production baseline `dd665618`, revalidation found the exact
post-reduction reachable mode set by all consumer classes: `check-public` from the suite registry;
`check-contract`, `check-promoted`, and `check-recovery` from workflow-contract
leaves; and `check-contract` plus `check-promoted` from the scheduled workflow.
The broader repository sweep found references and test fixtures, but no further
mode invocation. The distinct reachable set is therefore exactly the four modes
in `MODES`.

~~~text
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle
Ran 116 tests in 105.953s
OK

check-public exit=0
check-contract exit=0
check-promoted exit=0
check-recovery exit=0

PYTHONPATH=. python3 scripts/validation/check-github-workflow-contract.py
PASS: GitHub workflow contract (workflows=7, jobs=9, actions=8)
~~~

The implementation remains the two discovered logical commits `412542b0` and
`8b4f8e9b`; their diffs match Task 1 Steps 1--9: four-mode tuple, recovery
leaf, retirement of the three scheduled non-gating calls, deletion of
`provenance_policy`, manifest/suite cleanup, and reduced mode matrices. No
duplicate production commit was created during revalidation.

The manifest check is not fully green, but its exact five failures are only the
Task 3-owned unregistered package markers:

~~~text
FAIL [manifest-record-missing] scripts/lib/agent_governance/__init__.py
FAIL [manifest-record-missing] scripts/lib/gate/__init__.py
FAIL [manifest-record-missing] scripts/lib/ops/__init__.py
FAIL [manifest-record-missing] scripts/lib/supply_chain/__init__.py
FAIL [manifest-record-missing] scripts/lib/target_surface/__init__.py
script_manifest_failures=5
~~~

Task 1 lifecycle and workflow behavior are GREEN; the shared manifest bundle
remains RED pending the Task 3 marker repair. Independent review is pending and
this revalidation is not an approval.

The evidence-only commit `7a10255f` and this correction's successor HEAD are
documentation state, not the production baseline used for the Task 1 checks.

### Task 2 — repaired; independent review pending

Discovered logical commits: `dd41a675` and `342863ff`. They already derive the
archive/lifecycle relations; this Task does not retroactively approve them.
Current repair commit: `053a39ab`.

~~~text
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_spec_packages
FAIL: test_current_repository_has_exact_canonical_spec_surface
AssertionError: 34 != 35

PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive.ArchiveMinimizationTests.test_no_current_repository_spec_package_cardinality_pin
FAIL: ['test_current_repository_has_exact_canonical_spec_surface:34']

PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive.ArchiveMinimizationTests.test_no_current_repository_spec_package_cardinality_pin
Ran 1 test in 0.019s
OK

PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive
Ran 22 tests in 40.992s
OK

PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle
Ran 116 tests in 134.804s
OK

PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_spec_packages
Ran 16 tests in 7.930s
OK
~~~

The repaired current-repository test compares the set of immediate Stage 03
directories containing `spec.md` with `{package.path for package in packages}`.
It retains the prefix, Stage 04, and legacy-role assertions. The AST guard
examines only `test_current_repository_*` methods for an integer literal against
`len(packages)`, so intentional one-package fixture cardinalities remain valid.

The documentation record was also checked after this repair:

~~~text
python3 scripts/validation/check-document-metadata.py --mode check-contracts
metadata repository contracts: violations=0

python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"
metadata check-changed: selected=14 violations=0 legacy_exceptions=0 transition_overrides=0

python3 scripts/validation/check-document-links.py --mode all
document links: mode=all documents=568 links=4868 catalog_pairs_total=46 archive_direct_links_total=0 removed_template_mentions_total=0 failures=0
PASS: document link mode all
~~~

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

Independent review round 1 requested corrections to the Plan status, discovered
diff-stat evidence, completion bookkeeping, Task 4 manifest snippets, and the
Spec/Plan ownership-rule conflict. Round 2 corrects Task 0 completion state and
the Task 4 primary-owner algorithm. Independent re-review is pending; neither
round is an independent approval.

Round 3 replaces substring domain matching with normalized full-domain-token
matching. Independent re-review remains pending; this is not an approval.

Independent review round 1 found the Spec PASS and requested quality changes to
Task 1 evidence and the Step 8 contract. This correction is pending re-review;
it is not an approval.

Round 2 read-only primary-owner output:

~~~text
tests.validation.test_agent_governance_contract -> tests.lib.agent_governance.test_agent_governance_contract
tests.validation.test_ci_gate_adapters -> tests.lib.gate.test_ci_gate_adapters
tests.validation.test_ci_gate_contract -> tests.lib.gate.test_ci_gate_contract
tests.validation.test_github_workflow_contract -> tests.lib.gate.test_github_workflow_contract
tests.validation.test_grype_db_seed -> tests.lib.supply_chain.test_grype_db_seed
tests.validation.test_postgres_logical_upgrade_rehearsal -> tests.lib.ops.test_postgres_logical_upgrade_rehearsal
tests.validation.test_target_surface_contracts -> tests.lib.target_surface.test_target_surface_contracts
tests.validation.test_target_surface_delta_contracts -> tests.lib.target_surface.test_target_surface_delta_contracts
mappings=8
~~~

No hardening-lib or validator_entrypoints mapping was emitted.

Round 3 read-only boundary evidence:

~~~text
tests.validation.test_agent_governance_contract -> tests.lib.agent_governance.test_agent_governance_contract
tests.validation.test_ci_gate_adapters -> tests.lib.gate.test_ci_gate_adapters
tests.validation.test_ci_gate_contract -> tests.lib.gate.test_ci_gate_contract
tests.validation.test_github_workflow_contract -> tests.lib.gate.test_github_workflow_contract
tests.validation.test_grype_db_seed -> tests.lib.supply_chain.test_grype_db_seed
tests.validation.test_postgres_logical_upgrade_rehearsal -> tests.lib.ops.test_postgres_logical_upgrade_rehearsal
tests.validation.test_target_surface_contracts -> tests.lib.target_surface.test_target_surface_contracts
tests.validation.test_target_surface_delta_contracts -> tests.lib.target_surface.test_target_surface_delta_contracts
mappings=8
gateway_negative= None
target_surface_positive= target_surface
~~~

Implementer self-review: complete. The diff is limited to the four authorized
Stage 03 documents; it activates the legal chain, records the observed RED
checks as reopened, and removes the obsolete Task 2--9 instructions identified
in the preflight rulings. git diff --check passed. No discovered implementation
is self-approved by this registration.

## Commit Ledger

| Logical unit | Commit(s) | Status |
| :--- | :--- | :--- |
| Task 1 lifecycle reduction | 412542b0, 8b4f8e9b | Revalidated: lifecycle/workflow GREEN; shared manifest bundle RED pending Task 3 |
| Task 2 census derivation | dd41a675, 342863ff; 053a39ab | Archive/lifecycle relations revalidated; current Spec Package repair GREEN; independent review pending |
| Task 3 library ownership move | d6b7eafe, e23d93f1 | Reopened by five package-marker manifest failures |
| Task 0 recovery record | 923b2765 | Recovery chain and observed evidence |

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
7. A library is determined by its manifest execution contexts and filesystem
   entrypoint ownership, not by an argparse or __main__ guard.

## Deferred Items

- Task 3 production repair: remove the five unnecessary package markers.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Stage 03 index](../../README.md)
