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
| 3a | Revalidated Task 1 focused checks | Lifecycle suite and all four modes passed; the shared manifest check then failed only on five Task 3 package markers, resolved by the Task 3 repair below. |
| 3b | Revalidated Task 2 focused checks | Archive and lifecycle suites passed; Spec Package suite failed one fixed count. Task 2 is reopened. |
| 3c | Revalidated Task 3 focused checks | Surface ownership and workflow contract passed; manifest initially failed only because the five package markers were unregistered. |
| 4 | Recovery metadata/link checks | All three commands passed: contract violations=0, changed-document violations=0, links failures=0. |
| 5 | Committed recovery record | 923b2765 docs(spec): Activate script surface convergence with recovered evidence. |
| 6 | Applied review round 1 corrections | Plan activated; complete pre-Task-0 diff-stat captured; completed bookkeeping fixed; manifest snippets and library ownership contract corrected. |
| 7 | Revalidated Task 1 implementation at `dd665618` | Consumer inventory resolves exactly four reachable modes (`check-public`, `check-contract`, `check-promoted`, `check-recovery`). The lifecycle suite, all four modes, and the workflow contract are GREEN. The shared manifest bundle is RED only for five Task 3-owned package markers; no Task 1 production change or duplicate production commit was made. |
| 8 | Repaired the remaining Task 2 Spec Package count pin | Directly observed the existing `34 != 35` failure and the new targeted guard RED. Replaced the pin with the loader-to-directory set relation; targeted guard plus archive, lifecycle, and Spec Package suites are GREEN. Independent review remains pending. |
| 9 | Repaired Task 3 package markers | Captured the exact five-marker manifest RED and dependency evidence, deleted only those markers with `apply_patch`, then confirmed namespace imports, manifest, ownership, and workflow checks GREEN. The focused-test RED is Task 5 unregistered agent-governance fixture work; all five full-Gate results are Task 6 registered recovery-fixture work. |
| 10 | Revalidated the responsibility-split acceptance scope | Measured 37 files above the earlier diagnostic threshold: 32 Python and 5 shell. Only four have named split boundaries in SPEC-0157, leaving 33 outside this Spec, and no authoritative repository-wide limit or exception mechanism exists. Replaced the unsupported global limit with the four measured responsibility contracts. |
| 11 | Validated the responsibility-split contract correction | Metadata contracts reported `violations=0`; changed-document metadata selected 14 documents with `violations=0`; the all-links check reported `failures=0`; `git diff --check` passed. |
| 12 | Reconciled Task 4 with the actual test mirror and gate wiring | Fixed the move set at eight modules, prohibited new package markers, replaced the impossible generated-prefix rewrite with exact dotted modules, enumerated all current machine/current-document references, and corrected the Task 4 through Task 6 full-Gate ownership boundaries. Rebased four forward references in draft SPEC-0158 without activating or executing it. |
| 13 | Validated the Task 4 preflight correction | Metadata contracts reported `violations=0`; changed-document metadata selected 14 documents with `violations=0`; the all-links check reported `failures=0`; `git diff --check` passed. No production, test, Gate, manifest, workflow, or generated-provider file was modified. |
| 14 | Received independent Task 4 preflight review | `Spec compliance: FAIL`; `Quality: CHANGES_REQUESTED`. The review found that Task 5 could falsely count admission-only strings as registration and that Task 4's old-path sweep had no reproducible untruncated command. |
| 15 | Corrected full-profile reachability and stale-path proof | Replaced the Task 5 source-string union with an Acceptance 4 oracle derived from the local full public execution plan, added an admission-only negative regression and an independently owned agent-governance leaf contract, and added a complete 16-form old-path sweep that excludes only `.git` and `graphify-out/`. Independent re-review remains pending. |
| 16 | Rechecked the moved-suite execution boundary | A source-of-truth review found that `_UNITTEST_MODULE` still admitted only `tests.validation` and `tests.lib.document_governance`; runner parity alone would therefore leave the moved gate, ops, supply-chain, target-surface, and agent-governance modules rejected by the adapter. Task 4 now writes the adapter regression RED first, admits valid nonempty dotted segments below the two authoritative roots `tests.validation` and `tests.lib`, keeps outside-root and malformed shapes rejected, and leaves actual authority in the runner's exact argv map. |
| 17 | Validated the independent-review correction | Metadata contracts reported `violations=0`; changed-document metadata selected 14 documents with `violations=0`, `legacy_exceptions=0`, and `transition_overrides=0`; the all-links check reported `failures=0`; `git diff --check` passed. Independent re-review remains pending. |
| 18 | Witnessed the Task 4 ownership and adapter RED | Surface ownership failed on the five missing mirror domains and the existing placeholder roots. The positive adapter regression produced eight `ci-gate-adapter-arguments` errors for the moved modules, while the existing validation/document-governance cases and the outside/empty/invalid negative remained GREEN. |
| 19 | Mirrored the measured library-unit test surface | Moved exactly eight tests with `git mv`, changed the seven repository-root depths, expanded only the adapter's structural root grammar, rewired exact runner/workflow/manifest/current references, and deleted the three placeholder READMEs without a redirect or tombstone. Implementation commit: `6663f02c`. |
| 20 | Verified the Task 4-owned execution boundary | The adapter regressions, 207-test moved-suite bundle, surface ownership, CI runner, README profiles, script manifest checker, and workflow-contract checker are GREEN. The explicit agent-governance suite retains only its three Task 5-owned missing-SPEC-0153 subcase errors. |
| 21 | Classified two pre-existing unreachable manifest-test failures | The full `test_script_manifest` module remains RED on the unchanged hook-disposition assertion and an already-absent SPEC-0153 input. Start-HEAD object inspection and a dynamically expanded local full plan prove both predate Task 4 and the module is unreachable; the two Task 4-owned manifest assertions pass directly. |
| 22 | Verified current documents, stale paths, and full-Gate ownership | Metadata contracts, changed metadata, links, and diff check passed. The untruncated old-path sweep produced 681 historical/evidence lines and zero prohibited current/live hits. After staging the exact implementation paths for entrypoint-identity verification, the full Gate retained only the five exact Task 6-owned `ChangedBodyDeficitGitTests` results. |
| 23 | Received independent Task 4 implementation review | Task review: `Spec FAIL`, `Quality CHANGES_REQUESTED`; Python review: `CHANGES_REQUESTED`; CI/Gate review: `APPROVED`. The requested changes were the numeric-leading unittest-segment admission and the evidence record that copied raw search output into its own search surface while misstating the manifest run count. |
| 24 | Corrected the unittest identifier boundary | Added three numeric-leading cases and witnessed all three fail because `AdapterError` was not raised. Restricted every segment to `[A-Za-z_][A-Za-z0-9_]*`; the focused pair, 15-test adapter module, 30-test runner, manifest checker, and workflow checker are GREEN. Correction commit: `ff12147d`. |
| 25 | Revalidated the corrected full-Gate and evidence boundary | The staged correction full Gate ran 251 tests in 156.679 seconds and retained only the exact Task 6 five. The manifest module ran 53 tests with only its two base-proven unreachable failures. Raw old-path output was removed from the ignored scratch report, and the current authoritative live surfaces were separately rechecked with zero prohibited hits. Metadata contracts and changed-document checks reported zero violations, all links reported zero failures, and diff hygiene passed. Independent Task/Python re-review remains pending. |
| 26 | Recorded the user-directed Stage 90 preservation boundary | The entire tracked 21-file `RES-0002` research pack observed at this ruling is one atomic `PROTECT_LATEST` unit, but SPEC-0158 Task 2 must remeasure the current execution baseline. Commit `95142c3a` promoted and activated the draft; `07b94403` later restored and merged substantive content across all 21 files; `3bf50f94` later added claim-bearing corrections; `65e8dfde` remains the last new-leaf addition; and `6663f02c` changes only three link destinations. Other later governance or path edits may exist. Every identifier is illustrative provenance only, never the final protected state, a restore target, Gate, baseline, or branch-lineage control. No Stage 90 artifact was changed or dispositioned by this ruling. |
| 27 | Corrected the Stage 90 preservation design after independent review | Review returned `Spec FAIL` and `Quality CHANGES_REQUESTED`: the first version mislabeled `95142c3a` as the final research-body state and left the protected path inventory only in transient Task evidence. The correction makes the Task 2 current package measurement the sole preservation subject and requires Task 6 to persist the non-hash path declaration in the `RES-0002` package README before Task evidence retirement. Correction is pending independent re-review and claims no approval. |

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

### Task 1 — revalidated; shared manifest bundle resolved by Task 3

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

Task 1 lifecycle and workflow behavior are GREEN. At this historical
revalidation point the shared manifest bundle was RED only for the five Task 3
markers; Task 3 subsequently resolved that shared dependency. Independent
review is pending and this revalidation is not an approval.

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

### Task 3 — repaired; independent review pending

Discovered logical commits: `d6b7eafe` (move/ownership) and `e23d93f1`
(operations ordering follow-up). They are measured discovered work, not
retroactively approved. New marker repair commit: `58981986`
`refactor(scripts): Drop redundant package markers`.

Before the repair, `check-script-manifest.py` reported exactly five RED rows:
`scripts/lib/{agent_governance,gate,ops,supply_chain,target_surface}/__init__.py`.
Each was a one-line docstring; the dependency sweep found no package-level
attributes, side effects, exports, or wildcard consumers. The five files were
removed with `apply_patch`; no manifest rows were added. The ownership rule is
that `scripts/lib/<domain>` is importable and has no manifest
`execution_contexts`; an entrypoint guard alone is irrelevant.

~~~text
namespace_packages=5
python_modules=7
exact_package_imports=7
ops_namespace=PASS
ops_shell_files=2

PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership
Ran 3 tests in 0.102s
OK

PYTHONPATH=. python3 scripts/validation/check-script-manifest.py
PASS: script manifest is valid

PYTHONPATH=. python3 scripts/validation/check-github-workflow-contract.py
PASS: GitHub workflow contract (workflows=7, jobs=9, actions=8)

Moved-library focused tests
Ran 224 tests in 142.672s
FAILED (errors=3)
three subcases of `test_mutable_task_token_evidence_is_statement_bounded` in
the currently unregistered agent-governance test module:
`case='evidence-only-edit'`, `case='new-active-authority'`, and
`case='altered-statement'`. Each calls `copy2` on the absent
`docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md`
(Task 5 measured-unregistered repair)

PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full
Ran 251 tests in 148.982s
FAILED (failures=3, errors=2)
FULL exit=1
~~~

The full-Gate results are outside Task 3. All five are already-registered
`tests.validation.test_document_metadata.ChangedBodyDeficitGitTests` cases,
owned by Task 6 fixed-workspace/recovery-fixture work:

1. Error: `test_registered_operations_catalog_move_uses_migration_0003_body_baseline`
2. Error: `test_registered_operations_profile_transition_holds_the_registry_boundary`
3. Failure: `test_preexisting_target_cannot_borrow_registered_source_baseline`
4. Failure: `test_registered_operations_move_requires_its_exact_source_at_base`
5. Failure: `test_unrelated_operations_readme_does_not_receive_transition_authorization`

Task 3 did not expand into that repair.

### Responsibility-split scope preflight

The preflight counted current Python and shell files under `scripts/` and
`tests/`, then searched Stage 00, Requirements, Architecture, and Stage 99 for
an authoritative 800-line rule:

~~~text
total=37 python=32 shell=5
authoritative 800-line policy matches: 0
~~~

The four files named by SPEC-0157 have explicit domain or mode boundaries;
the other 33 do not. No registered exception mechanism exists for a global
source-size rule. The Spec and Plan therefore treat length only as diagnostic
evidence and verify the four selected files by responsibility boundary,
compatibility behavior, lifecycle modes, and preserved test counts. Defining a
repository-wide limit would require a separately approved Requirement, ADR,
and Spec rather than an implicit validator or exception registry here.

### Task 4 ownership and wiring preflight

The authoritative mirror set is exactly these eight moves:

~~~text
tests/validation/test_agent_governance_contract.py -> tests/lib/agent_governance/test_agent_governance_contract.py
tests/validation/test_ci_gate_adapters.py -> tests/lib/gate/test_ci_gate_adapters.py
tests/validation/test_ci_gate_contract.py -> tests/lib/gate/test_ci_gate_contract.py
tests/validation/test_github_workflow_contract.py -> tests/lib/gate/test_github_workflow_contract.py
tests/validation/test_grype_db_seed.py -> tests/lib/supply_chain/test_grype_db_seed.py
tests/validation/test_postgres_logical_upgrade_rehearsal.py -> tests/lib/ops/test_postgres_logical_upgrade_rehearsal.py
tests/validation/test_target_surface_contracts.py -> tests/lib/target_surface/test_target_surface_contracts.py
tests/validation/test_target_surface_delta_contracts.py -> tests/lib/target_surface/test_target_surface_delta_contracts.py
~~~

No new `__init__.py` is created. Seven moved files change their repository-root
derivation from `parents[2]` to `parents[3]`; `test_ci_gate_adapters.py` has no
such root constant.

The CI runner cannot be corrected by replacing old module strings because its
current block generates a `tests.validation` prefix from bare stems. Task 4
replaces it with this exact dotted-module tuple:

~~~text
tests.validation.test_agent_output_eval_fixtures
tests.lib.gate.test_ci_gate_contract
tests.validation.test_ci_gate_runner
tests.lib.gate.test_ci_gate_adapters
tests.lib.gate.test_github_workflow_contract
tests.validation.test_agent_governance_ci_routing
tests.validation.test_document_corpus_lifecycle
tests.validation.test_document_metadata
tests.validation.test_hook_rules
tests.lib.target_surface.test_target_surface_contracts
tests.lib.target_surface.test_target_surface_delta_contracts
tests.validation.test_compose_baseline_gates
~~~

The runner tuple is only the outer admission boundary. The lower
`ci_gate_adapters.py` grammar currently accepts `tests.validation.*` and
`tests.lib.document_governance.*`, so the newly mirrored gate, ops,
supply-chain, target-surface, and agent-governance modules would pass runner
parity and then fail adapter dispatch. Task 4 therefore writes focused adapter
regressions before the move: all eight moved `tests.lib.<domain>.*` modules must
be accepted, while a root outside `tests.validation` or `tests.lib`, an empty
segment, and an invalid segment must be rejected. The grammar does not enumerate
domains because that would duplicate ownership; `_INTERNAL_ADAPTER_CONTEXTS`
continues to grant permission only to exact complete argv tuples.

Current machine references to rewire are the six workflow-contract leaves
`leaf.ci-gate-adapter-regressions`, `leaf.ci-gate-contract-regressions`,
`leaf.workflow-contract-regressions`, `leaf.local-target-surface-regressions`,
`leaf.local-target-delta-regressions`, and `leaf.supply-chain-fixture-policy`;
the last keeps its other modules while moving both PostgreSQL and Grype tests.
The same change covers the two supply-chain semantic strings in
`github_workflow_contract.py` and its moved test, the CI runner's negative
PostgreSQL name, every manifest reference with sorted test lists, the
PostgreSQL expectation in `test_script_manifest.py`, the current comment in
`ci_gate_contract.py`, the agent-governance CODEOWNERS row, accepted manifest
test roots, the exact two unclassified test READMEs, and the surface-ownership
invariants.

Current document references to update are the two target-surface commands in
`scripts/README.md`; the ownership descriptions in `tests/README.md`,
`tests/lib/README.md`, and `tests/validation/README.md`; the PostgreSQL runbook
command; and only the live Markdown destinations in
`quality-ci-formatting.md`, `scope-application-matrix.md`, and
`workspace-baseline.md` (one CI-gate link and two agent-governance links). The
three placeholder READMEs under `tests/docs`,
`tests/qa`, and `tests/setup` are deleted without redirects or tombstones.
Completed evidence and historical literals stay unchanged.

Draft SPEC-0158 contained four forward instructions for the old
agent-governance test path: two file references, one dotted unittest command,
and one staging path. They are rebased to
`tests/lib/agent_governance/test_agent_governance_contract.py` because the user
included work in progress in this convergence. SPEC-0158 remains draft and is
not executed by this Task.

Seven already-registered moved suites must be GREEN. The moved
agent-governance suite is run explicitly and may retain only its three measured
Task 5-owned missing-SPEC-0153 fixture subcases. At the Task 4 and Task 5 full
Gate boundaries, only the five exact Task 6-owned
`ChangedBodyDeficitGitTests` results recorded above may remain RED. Task 6 owns
their repair and must restore `FULL exit=0`; no moved-module import or
registration failure may be deferred.

### Task 4 preflight review correction

Independent review rejected the first preflight because the proposed Task 5
invariant unioned quoted module names from `ci_gate_runner.py` and the workflow
contract. `_INTERNAL_ADAPTER_CONTEXTS` admits an exact internal argv but does
not put that invocation in a plan; a module could therefore appear in the
allowlist, have no reachable leaf, and falsely count as registered.

The corrected Acceptance 4 oracle loads `.github/workflow-contract.yml` and
`scripts/manifest.yaml`, selects every public suite for profile `full`, expands
their `public_gate.suite_roots`, builds the local public validation plan, and
collects dotted modules only from its reachable `run-unittest` invocations. The
on-disk `test_*.py` set must equal that set. A focused negative test temporarily
admits a nonexistent module without creating a leaf and proves it remains
unregistered.

Every retained Task 5 module now requires both exact runner admission and a
full-profile reachable leaf under its recorded public-suite owner. The repaired
agent-governance contract test receives the independent leaf
`leaf.agent-governance-regressions` directly under
`public_gate.suite_roots["agent-governance"]`; it is also wired through the CI
repo-contract root and all three local profile projections. It is not placed in
the document-governance aggregate.

The Task 4 stale-path proof now runs one untruncated `rg` over all eight old
filesystem paths and all eight old dotted module names. It uses
`--hidden --no-ignore`, saves complete output under `/tmp`, prints both its line
count and full content, and excludes only `.git` plus the verified generated
graph root `graphify-out/`. Every line must be classified as preserved
historical evidence or prohibited current/live usage.

### Task 4 — implemented; correction pending independent re-review

Implementation commit: `6663f02c`
`refactor(tests): Mirror library ownership in the test surface`.

The pre-implementation ownership run produced two failures. The exact missing
mirror set was `agent_governance`, `gate`, `ops`, `supply_chain`, and
`target_surface`; the placeholder assertion stopped at the first existing root,
`tests/docs`, and a direct empty-directory check confirmed that `tests/docs`,
`tests/qa`, and `tests/setup` contained no file after their three READMEs were
deleted. The pre-implementation adapter run executed two test methods: its
positive method produced eight `ci-gate-adapter-arguments` errors, one for each
new moved module, while the existing `tests.validation` and
`tests.lib.document_governance` cases passed and the outside/empty/invalid
negative method was GREEN.

The implementation then moved exactly this set:

~~~text
tests/validation/test_agent_governance_contract.py -> tests/lib/agent_governance/test_agent_governance_contract.py
tests/validation/test_ci_gate_adapters.py -> tests/lib/gate/test_ci_gate_adapters.py
tests/validation/test_ci_gate_contract.py -> tests/lib/gate/test_ci_gate_contract.py
tests/validation/test_github_workflow_contract.py -> tests/lib/gate/test_github_workflow_contract.py
tests/validation/test_grype_db_seed.py -> tests/lib/supply_chain/test_grype_db_seed.py
tests/validation/test_postgres_logical_upgrade_rehearsal.py -> tests/lib/ops/test_postgres_logical_upgrade_rehearsal.py
tests/validation/test_target_surface_contracts.py -> tests/lib/target_surface/test_target_surface_contracts.py
tests/validation/test_target_surface_delta_contracts.py -> tests/lib/target_surface/test_target_surface_delta_contracts.py
~~~

No `__init__.py` was added. Seven moved modules changed their root derivation
from `parents[2]` to `parents[3]`; the adapter test has no root constant. The
three placeholder READMEs and their now-empty directories were removed without
a redirect or tombstone.

Focused GREEN evidence:

~~~text
adapter allow/reject regressions: Ran 2 tests; OK
seven registered moved suites: Ran 207 tests in 109.926s; OK (skipped=11)
surface ownership: Ran 5 tests; OK
CI gate runner: Ran 30 tests in 8.212s; OK
README profiles: Ran 4 tests; OK
Task 4 PostgreSQL/retired-root manifest assertions: Ran 2 tests; OK
check-script-manifest.py: PASS
check-github-workflow-contract.py: PASS (workflows=7, jobs=9, actions=8)
~~~

The full `tests.validation.test_script_manifest` run executed 53 tests and
retained exactly two failures:

1. `ScriptManifestTests.test_plan_mandatory_dispositions_and_high_risk_operations`
   with `path='scripts/hooks/post-tool-validate.sh'`: expected `rewrite`, current
   manifest row `retain`.
2. `ScriptManifestTests.test_stage90_generators_require_write_and_touch_only_declared_output`
   with `script='scripts/validation/generate-audit-implementation-matrix.sh'`:
   missing `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0010-archive.md`.

These are Task 5 measured-unreachable work, not Task 4 regressions. The
`git diff --unified=0 0453dcee -- tests/validation/test_script_manifest.py
scripts/manifest.yaml` result changed only the moved PostgreSQL path, the new
retired-root regression, and moved manifest references; neither failing test
body nor the hook row changed. At `0453dcee`, the manifest already declared the
hook `retain`, the test constant already required `rewrite`, and
`git cat-file -e 0453dcee:docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0010-archive.md`
failed because that path did not exist. Dynamic expansion of the local `full`
public plan found 25 reachable unittest modules and reported
`reachable_test_script_manifest=False`. The two exact Task 4-owned manifest
methods ran separately and are GREEN; no assertion was weakened and no deleted
fixture was restored.

The explicit eighth moved suite retained exactly the measured Task 5 boundary:

~~~text
tests.lib.agent_governance.test_agent_governance_contract
Ran 19 tests in 4.205s
FAILED (errors=3)
test_mutable_task_token_evidence_is_statement_bounded(case='evidence-only-edit')
test_mutable_task_token_evidence_is_statement_bounded(case='new-active-authority')
test_mutable_task_token_evidence_is_statement_bounded(case='altered-statement')
all three: missing docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md
~~~

Document and full-Gate evidence:

~~~text
metadata repository contracts: violations=0
metadata check-changed: selected=16 violations=0 legacy_exceptions=0 transition_overrides=0
document links: mode=all documents=568 links=4868 failures=0
git diff --check: exit=0

initial full-Gate attempt before staging:
FAIL [ci-gate-entrypoint-identity] scripts/lib/gate/ci_gate_adapters.py
The entrypoint was then staged with the exact Task 4 implementation paths so
the runner could compare the file descriptor with the reviewed index object.

registered focused bundles inside the full Gate:
Ran 39 tests; OK
Ran 48 tests; OK
Ran 20 tests; OK
Ran 116 tests; OK

final full bundle:
Ran 251 tests in 119.766s
FAILED (failures=3, errors=2)
FULL exit=1
~~~

The final five results are exactly the Task 6-owned
`ChangedBodyDeficitGitTests` boundary and no others:

1. Error: `test_registered_operations_catalog_move_uses_migration_0003_body_baseline`
2. Error: `test_registered_operations_profile_transition_holds_the_registry_boundary`
3. Failure: `test_preexisting_target_cannot_borrow_registered_source_baseline`
4. Failure: `test_registered_operations_move_requires_its_exact_source_at_base`
5. Failure: `test_unrelated_operations_readme_does_not_receive_transition_authorization`

After the identifier-shape correction was staged and reviewed, the affected
adapter module ran 15 tests and the CI runner ran 30 tests, both GREEN. The
manifest and workflow checkers also passed. The correction full Gate then ran
251 tests in 156.679 seconds and retained the same two errors and three failures
listed above, with no adapter, import, manifest, workflow, metadata, or link
regression.

The exact untruncated old-path sweep was captured from the staged implementation
snapshot that became commit `6663f02c`, before documentation evidence was added.
It produced 681 lines. Classification by authority surface is exhaustive: 101
`.superpowers` lines are immutable SDD review/recovery snapshots or the consumed
Task 4 predecessor/proof brief; 224 Stage 03 lines are predecessor
plans/completed evidence or this Task's explicit source-to-destination mappings
and proof expression; 318 Stage 90 lines are dated observations or generated
historical datasets; and 38 Stage 98 lines are migration/recovery history. The
four groups sum to 681, with zero prohibited current/live hits. The complete raw
capture remains only in `/tmp/spec0157-task4-old-path-hits.txt`; the ignored SDD
scratch report retains only its summary and hash, and its prior self-recursive
raw copy was removed. The capture SHA-256 is
`e8ba87b1edf3b1779d9e30904892e92a34c3f662b2778fdf51fdb3cd0051b8b7`.

At current HEAD, the same 16-form old-path expression was separately rerun over
`.github/`, `scripts/`, `tests/`, the current PostgreSQL runbook, and draft
SPEC-0158's forward plan: zero hits. The three Stage 90 research documents were
also checked for stale Markdown link destinations: zero hits. Their six
non-link dated-prose literals remain preserved historical evidence rather than
current/live references.

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

Task 3 review round 1: packaging/Python review is APPROVED. The Task review is
Spec FAIL with quality CHANGES_REQUESTED solely because the focused and full
Gate failure attribution was imprecise. This correction is pending re-review;
it is not final approval.

Task 3 review round 2 adds the exact three parameterized focused-test subcase
identities. It is pending re-review and does not claim approval.

Task 4 preflight independent review: `Spec compliance: FAIL`; `Quality:
CHANGES_REQUESTED`. Finding 1: the Task 5 source-string union could count a
runner admission with no reachable workflow leaf. Finding 2: Task 4 described
an untruncated old-path sweep without giving an executable command. The current
correction derives registration from the local full public plan, adds the
admission-only negative regression and agent-governance ownership leaf, and
specifies the complete saved-output `rg` proof. Independent re-review is
pending. A subsequent source-of-truth check also found the adapter's narrower
module grammar; the corrected Task 4 now owns its RED allow/reject regressions
and two-root structural repair while exact runner argv remains authoritative.
This is not an approval or completion claim.

Task 4 implementer self-review: the production diff is limited to the exact
eight moves, three placeholder deletions, adapter/runner/workflow/manifest
wiring, and current/future reference destinations authorized by the Plan.
Focused Task 4 checks are GREEN; the two base-proven unreachable manifest-test
failures, three agent-governance fixture errors, and five full-Gate fixture
results are attributed above to Tasks 5 and 6. The independent Task review
returned `Spec FAIL` and `Quality CHANGES_REQUESTED`; the Python review returned
`CHANGES_REQUESTED`; and the CI/Gate review returned `APPROVED`. The Task/Python
findings are corrected by `ff12147d` and this evidence update but remain pending
independent re-review, so this is not an approval or completion claim.

Task 4 correction re-review: `Spec compliance: PASS`; `Quality: APPROVED`;
Python review `APPROVED`; CI/Gate review `APPROVED`. The reviewers independently
confirmed the identifier grammar, numeric-leading negative cases, 53-test
manifest boundary, summary-only SDD evidence, exact eight moves, and the final
full-Gate boundary of only the five Task 6-owned results. Task 4 is complete;
SPEC-0157, its Plan, and this execution Task remain active for Tasks 5--9.

Stage 90 preservation review: `Spec compliance: FAIL`; `Quality:
CHANGES_REQUESTED`. Finding 1 identified the incorrect claim that `95142c3a`
was the final research-body state even though `07b94403` later changed all 21
files substantively and `3bf50f94` later added claim-bearing corrections.
Finding 2 identified that Task 2 evidence would be removed before the
protection oracle had a durable source. The current correction uses only the
Task 2 current execution-baseline package as the preservation subject and
requires a package-local README declaration plus existing reference-test
coverage before Task retirement. Independent re-review is pending; this is not
an approval.

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
| Task 1 lifecycle reduction | 412542b0, 8b4f8e9b | Revalidated: lifecycle/workflow GREEN; shared manifest bundle resolved by Task 3 repair |
| Task 2 census derivation | dd41a675, 342863ff; 053a39ab | Archive/lifecycle relations revalidated; current Spec Package repair GREEN; independent review pending |
| Task 3 library ownership move | d6b7eafe, e23d93f1; 58981986 | Five package-marker repair revalidated; packaging/Python APPROVED; Task review round 2 attribution detail pending re-review |
| Task 0 recovery record | 923b2765 | Recovery chain and observed evidence |
| Task 4 test ownership mirror | 6663f02c; ff12147d | Complete; Task, Python, and CI/Gate reviews APPROVED |

## Rulings

1. SPEC-0157 remains active on this branch because its merge base is draft; no
   record here claims retroactive approval or completion.
2. Task 2 measures and fixes the actual remaining count pins.
3. Task 3 removes the five package markers and proves namespace imports rather
   than adding manifest rows.
4. Task 4 mirrors library-unit tests below tests/lib/<domain>, includes
   tests/lib/ops, and keeps validation/entrypoint tests in tests/validation.
   Agent-output evaluation modules remain validation entrypoints.
5. Task 5 uses both measured post-Task-4 differences between on-disk modules
   and local-full reachable modules, with current names rather than a stale
   count or predecessor list.
6. Task 6 uses tests/lib/target_surface/test_target_surface_contracts.py; Task
   9 updates ci_gate_runner.py, workflow contract, and manifest whenever split
   test module names change.
7. A library is determined by its manifest execution contexts and filesystem
   entrypoint ownership, not by an argparse or __main__ guard.
8. File length is diagnostic evidence only. SPEC-0157 decomposes the four
   measured files with named responsibility boundaries; the other 33 measured
   files are out of scope, and a repository-wide source-size policy requires a
   separate approved Requirement, ADR, and Spec.
9. Task 4 moves exactly eight primary-owner tests, uses implicit namespace
   packages, and rewires current executable/current-link references only.
   Historical literals remain evidence; draft SPEC-0158's future instructions
   are rebased without changing its lifecycle.
10. Every Task boundary runs the full Gate and records owned/deferred RED.
    Task 4 and Task 5 may retain only the five measured Task 6 failures; Task 6
    and the final boundary require `FULL exit=0`.
11. A test is registered only when its exact adapter argv is admitted and its
    owning public-suite leaf is reachable in the local full execution plan.
    Source-string presence and admission-only entries are not registration.
12. Task 4 stale-path evidence covers all eight old paths in both filesystem
    and dotted forms, saves and prints the full untruncated result, and excludes
    only `.git` and generated `graphify-out/` content.
13. A moved unittest module must cross both the runner's exact argv admission
    and the adapter's closed module grammar. The grammar accepts only the ASCII
    Python identifier shape `[A-Za-z_][A-Za-z0-9_]*` for each nonempty dotted
    segment below `tests.validation` or `tests.lib`, rejects outside-root and
    malformed shapes, and does not duplicate domain ownership; the exact runner
    argv remains the permission boundary.
14. A Task 4-focused expectation cannot hide a pre-existing failure in an
    unreachable module. Task 4 proves its two changed manifest assertions
    GREEN and records the unchanged two-failure module boundary; Task 5 owns
    the dynamic disposition when it compares on-disk tests with the local full
    plan.
15. The full Gate verifies an internal entrypoint against the Git index object.
    When Task 4 changes that entrypoint, the exact implementation paths are
    staged and reviewed before the full Gate; an unstaged identity failure is
    evidence that the protection worked, not a reason to bypass it.
16. An absence proof remains untruncated without turning the authoritative Task
    into a log store. The exact command, count, classification totals, zero
    prohibited result, and capture SHA-256 live here; the complete 681-line raw
    output stays only in `/tmp`, while the ignored SDD scratch report keeps a
    summary and hash. Removing its prior raw copy prevents the evidence file
    from recursively extending the searched surface. This is an
    evidence-retention boundary, not a search truncation or exclusion.
17. The complete existing tree at
    `docs/90.references/research/0002-agentic-engineering-research-pack/`
    remains one atomic `PROTECT_LATEST` unit until draft SPEC-0158 Task 2
    remeasures the tracked current execution-baseline package, which is the
    sole preservation subject. SPEC-0157 does not delete, archive, or reduce
    its research body, sources, or claims and does not broaden Task 4 to
    perform Stage 90 cleanup. `95142c3a`, `07b94403`, `3bf50f94`, `65e8dfde`,
    and `6663f02c` illustrate different authoring or maintenance events only;
    no named historical commit is the final protected content, a restore
    target, Gate, checksum, expected branch SHA, or retention baseline. Draft
    SPEC-0158 owns the dynamic classification, persistent package-local
    declaration, and any permitted cleanup.

## Deferred Items

- Task 5 dynamic disposition of the unreachable `test_script_manifest` module
  and repair/registration of the three agent-governance fixture subcases.
- Task 6 repair of the five exact `ChangedBodyDeficitGitTests` results.
- Stage 90 consumer/lifecycle remeasurement and cleanup belong to draft
  SPEC-0158. Its execution must preserve the atomic `RES-0002` research pack;
  this active SPEC-0157 Task performs no Stage 90 disposition.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Stage 03 index](../../README.md)
