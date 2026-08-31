---
profile_id: task
status: completed
artifact_id: task-0157-0001
artifact_type: task
parent_ids: [SPEC-0157, plan-0157]
created: 2026-08-31
updated: 2026-09-01
---

# Recover and Complete Script Surface Ownership Convergence

## Objective

Revalidate the implementation discovered on the branch, complete the remaining
approved work, and close its execution Plan while preserving SPEC-0157's legal
`active` endpoint without asserting retroactive approval.

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
| 28 | Closed the Stage 90 preservation re-review | Independent re-review returned `Spec compliance: PASS` and `Quality: APPROVED`. It confirmed that no historical SHA is a protected-content baseline, the Task 2 current execution-baseline package is the sole protection subject, and Task 6 must establish the package-local persistent declaration and existing reference-test coverage before transient Task evidence retires. Design commits: `f7ccecfb`, `b00c697f`. No Stage 90 artifact was changed or dispositioned. |
| 29 | Strengthened Stage 90 cleanup to a completion condition | The user confirmed that the latest externally researched `RES-0002` package is preserved and every other baseline Research, Audit, or Data package must reach terminal disposition. Draft SPEC-0158 now requires consumer and needed-meaning migration followed by deletion, a final package-root set containing only `RES-0002`, and zero unresolved or pending dispositions. Root/category READMEs are structural indexes, not packages. No Stage 90 artifact was changed or dispositioned by this design correction. |
| 30 | Revalidated the mandatory cleanup design against current tracked evidence | The protected package still has 21 tracked execution-baseline paths as an observation rather than a count pin; Stage 90 status and diff are empty; the search for superseded optional-retention wording returned zero hits. Metadata contracts and changed-document metadata reported zero violations, all links reported zero failures, and diff hygiene passed. This validates the design boundary only; actual migration and deletion remain unobserved SPEC-0158 work. |
| 31 | Corrected the Stage 98 retention design after the user ruling | Current inspection found three Migration documents and direct consumers across the active ADR, Stage 99, governance libraries, generators, manifests, and tests. Draft SPEC-0158 now treats the Migration layer as temporary historical input: it must move every current consumer first, remove the active Migration contract, delete all Migration documents and their directory, and retain only the structural index plus minimal archive records proven necessary by explicit preservation or live recovery navigation. SPEC-0157 changed no Stage 98 artifact and makes no implementation-completion claim. |
| 32 | Added the archive-isolation and stage-ownership ruling | The user fixed Stage 00 as AI-agent governance/role/skill authority; Stages 01--03 as the consistent SDLC chain; Stage 05 as Operations Guide/Incident/Postmortem/Runbook ownership; Stage 90 as Audit/Research/Data evidence; Stage 98 as isolated archive; and Stage 99 as docs template authority. A read-only search found existing inbound archive-file citations and links across current and historical documents. Draft SPEC-0158 now requires zero such inbound references from Stages 00/01/02/03/05/90, including generated indexes, while allowing retained archive records to point outward. This is design evidence only; the current corpus remains `needs_revalidation` until SPEC-0158 executes and verifies the cleanup. |
| 33 | Revalidated the corrected Stage 98 and stage-ownership design | Repository metadata contracts reported `violations=0`; changed-document metadata selected 16 documents with `violations=0`, `legacy_exceptions=0`, and `transition_overrides=0`; the existing all-links check reported `failures=0`; and diff hygiene passed. The current link check does not yet enforce the newly approved archive-isolation predicate, so these results validate document shape and existing links only. Actual zero-inbound proof remains unobserved SPEC-0158 work. |
| 34 | Completed Task 5 full-profile test registration | The pre-registration oracle measured 20 on-disk modules absent from the reachable local full plan and zero plan-only modules; its admission-only negative stayed GREEN. Eight RED modules were repaired or dispositioned against current owners before routing. Four new responsibility leaves and the existing supply-chain fixture leaf now route all 20 modules through exact adapter argv and public-suite ownership. The final set equality, focused contracts, manifest, and workflow checks are GREEN. Full execution reaches every module and stops only at the same five Task 6-owned `ChangedBodyDeficitGitTests` results. |
| 35 | Added the current-implementation truth ruling | The user required current implementation to be reflected in the registered Stage 01 and Stage 02 forms. Draft SPEC-0158 now classifies implemented obligations and guarantees to Stage 01, implemented structure and durable decisions to Stage 02, and requires bidirectional zero-gap alignment without copying code, execution logs, or a fixed inventory into documentation. Actual corpus observation and promotion remain unexecuted SPEC-0158 work. |
| 36 | Revalidated the current-implementation design amendment | Repository metadata contracts and changed-document metadata reported zero violations, legacy exceptions, and transition overrides; all links and the existing implementation-alignment mode reported zero failures; diff hygiene passed. These results prove the design change preserves current contracts only. They do not replace SPEC-0158 Task 2's implementation-subject inventory or Task 5's future bidirectional zero-gap proof. |
| 37 | Witnessed the Task 6 fixed-workspace invariant RED | The new invariant reported exactly seven dependencies: all three forbidden tokens in `test_document_metadata.py`; `HISTORICAL_COMMIT` and the retired support path in `test_document_corpus_lifecycle.py`; and the retired support path in both `test_target_surface_contracts.py` and `test_spec_packages.py`. No historical body was copied into this evidence. |
| 38 | Replaced fixed-workspace document fixtures with current authority | Positive cases now derive from the current Registry, current declared templates, current Stage 05 catalog, or current Spec Package records; negative cases mutate bounded temporary copies. `HistoricalDocument` remains only in a temporary Git repository that proves exact regular-blob recovery and rejects tree, missing, and symlink objects. Assertions owned only by the retired support taxonomy or Migration fixture authority were deleted rather than recreated. The invariant, metadata, lifecycle, target-surface, Spec Package, and Operations suites are GREEN, and the exact forbidden-token search is empty. |
| 39 | Corrected the first nested Full-Gate test capability boundary | Full execution exposed that the supply-chain wrapper test subprocess dropped the Gate's held root descriptor. Commit `ecdb7b9e` forwarded only a `/proc/self/fd/N` descriptor proven to be the same directory as the repository root. The wrapper class is GREEN for all 28 tests both directly and with an explicit held-root environment; this independent test-harness correction does not alter Task 6 document contracts. |
| 40 | Converged the subsequently reached held-root consumers | The first Task 6 Full run passed the document suites, then exposed the same closed-descriptor cause in 36 tech-stack subcases and eight Python entrypoints. Commit `3b3733de` moved the device/inode/type check to one test-only helper and connected the supply, tech-stack, and entrypoint consumers. The explicit held-root bundle is GREEN for 49 tests, and Task 6's lifecycle plus metadata suites are GREEN for 64 tests with the same helper. |
| 41 | Completed the Task 6 full-profile boundary | The exact seven Task 6 paths were staged with no unstaged change. All six focused suites, the forbidden-token absence check, metadata contracts, changed-document metadata, all links, implementation alignment, and diff hygiene are GREEN. The final Full Gate ran every registered bundle and reported `FULL exit=0`; Task 6 has no deferred RED. |
| 42 | Removed the residual archive fixture authority found in final self-review | The passing diff still contained one target-surface test that read a Tombstone and Migration, one Spec Package lifecycle fixture that copied the Migration document from the workspace, and two disabled `_legacy_*` template-fixture methods. The target-surface assertion and dead methods were deleted; the lifecycle test now uses an isolated temporary Git repository and a bounded empty migration-authority mock because its subject is snapshot removal, not archive content. The affected metadata, target-surface, and Spec Package suites are GREEN for 110 tests under the held-root environment. |
| 43 | Closed Task 6 after the residual-authority correction | Supporting held-root commits `ecdb7b9e` and `3b3733de` plus current-authority fixture commit `11529e0c` form the completed Task 6 unit. Its final staged Full Gate reported `FULL exit=0`; no Stage 98 fixture body or retired Stage 99 support path remains current test authority. |
| 44 | Measured and corrected the Task 7 history-scan design | The six stage patch-history projections ranged from 892,728 to 20,716,362 bytes and showed why the 64 MiB patch stopgap was excessive. A path-only identity proposal was rejected before implementation because Requirement child IDs exist only in bodies, Stage 90 leaf names can be references rather than package identities, and a Tombstone path names its retired target rather than its own ID. The new invariant was first RED against the retained `-G`/patch parser and 64 MiB cumulative budget. |
| 45 | Replaced historical patch parsing with bounded object-name projection | Six path-bounded `git rev-list --objects` queries select source blobs; batched `git grep` returns only identity-bearing lines, while paths select the legal identity family rather than the ID value. The pre/post issued-set captures are byte-identical at SHA-256 `c96d855fe9b5d9667c01a059a9ceb33e44313eff74bd594c8d46b5e37e495bd6`. All 17 identity-history tests and the registered full-history metadata route are GREEN; the measured historical Git output is 2,454,189 bytes under the 8 MiB cumulative cap. |
| 46 | Completed the Task 7 full-profile boundary | The exact four Task 7 paths were staged with no unstaged change. Static compilation, the 17-test identity module, full-history metadata contracts, changed-document metadata, all links, alignment links, and diff hygiene are GREEN. Every registered Full profile bundle passed, including the expanded 294-test document-governance bundle, and the final marker is `FULL exit=0`. |
| 47 | Measured the Task 8 production and consumer baselines | The untruncated live-consumer search has 30 rows. `metadata_validator.py` measured 6,794 lines and the lifecycle CLI 5,206 lines. The focused baselines are 51 metadata tests and 13 lifecycle tests; `check-public`, `check-contract`, `check-promoted`, and `check-recovery` all exited 0. |
| 48 | Witnessed the Task 8 compatibility RED | The new declared-API test failed only because the monolith had no `metadata_validator.__all__`. The dependency analysis rejected a line-only split and established the acyclic production direction `profile -> heading -> identity -> lifecycle -> reference`. |
| 49 | Split the metadata responsibility surface | The five implementation modules now own Registry/profile models, heading/body validation, identity validation, lifecycle records, and repository references respectively. The compatibility facade is 107 lines, uses explicit re-exports, and preserves every measured direct or adapter-mediated consumer. The five direct consumer suites ran 163 tests in 176.426 seconds and passed before the additional responsibility contract was added. |
| 50 | Split the lifecycle responsibility surface | The 5,206-line CLI became a 245-line parser/dispatch adapter, including its six-line direct-execution package bootstrap. `contract.py` owns common manifest and safety mechanics, `promoted.py` owns reconciliation, `public.py` owns current Spec Package findings, and `recovery.py` owns only minimal archive recovery validation. The 13-test baseline and all four mode exits remain GREEN. |
| 51 | Reconciled manifest and source-location ownership | The pre-update manifest reported nine stale direct-consumer edges. After staging exposed the new tracked paths, the new modules were registered as libraries under existing owners and one mirrored responsibility test directly proved all nine APIs without adding a Gate, workflow job, or fixture suite. Source-string tests now inspect their actual profile, promoted, contract, or reference owners instead of the thin facades. The manifest and workflow contracts are GREEN. |
| 52 | Reached the Task 8 pre-Full focused boundary | Static compilation and diff hygiene are GREEN. The first combined focused run executed 188 tests and retained one stale taxonomy source-location assertion. After repointing it to `lifecycle/promoted.py`, the complete bundle reran 188 tests in 173.784 seconds and passed. The Full Gate remains pending. |
| 53 | Repaired the lifecycle entrypoint boundary exposed by Full | The first staged Full run rejected the recreated CLI's `100644` mode; restoring `100755` satisfied the entrypoint contract. The next run reached the 13-test lifecycle bundle and exposed package import before held-root validation. A six-line repository-path bootstrap now permits direct execution while `contract.py` still rejects invalid, closed, and foreign `HYHOME_CI_GATE_ROOT` descriptors. The lifecycle suite and all four business modes are GREEN. |
| 54 | Repointed the final shared-governance source contract | The next Full run reached the 295-test document-governance bundle and failed one assertion because `test_links.py` still searched the thin CLI for `metadata_contract`. The test now inspects `lifecycle/contract.py`, rejects metadata-CLI dynamic loading across both surfaces, and is registered as direct contract evidence. The focused test and manifest are GREEN. |
| 55 | Reconciled the exact taxonomy-consumer oracle | The following Full run passed all 295 document-governance tests, then failed one of 128 later tests because `test_script_manifest.py` still expected the compatibility facade as taxonomy's sole consumer. The exact oracle now names the two measured importers, `metadata/lifecycle.py` and `metadata/profile.py`; its focused 53-test module and manifest are GREEN. |
| 56 | Completed the Task 8 full-profile boundary | The final staged Full run passed every registered bundle: 39, 19, 33, 43, 20, 13, 52, 15, 40, 295, 233, 17, 13, 31, 15, 45, 6, and 128 tests. The final marker is `FULL exit=0`; Task 8 adds no Gate leaf, workflow job, or fixture suite. |
| 57 | Committed the Task 8 responsibility unit | Commit `e72e1ee8` contains the verified 22-file production split, direct manifest evidence, source-owner corrections, and final Full evidence. The worktree was clean before Task 9 began. |
| 58 | Measured the Task 9 test baselines | The pre-split metadata module ran 52 tests in 58.299 seconds and the lifecycle module ran 13 tests in 14.017 seconds; both passed. The source contains ten metadata TestCase classes and three lifecycle TestCase classes. |
| 59 | Split the test responsibility surfaces without redirects | Whole TestCase classes moved to five metadata and three behavioral lifecycle owners; one `test_promoted.py` structural mirror records that no fourth TestCase existed to move without duplication. Two shared support modules retain only current Registry/CLI, temporary Git, and held-root mechanics. The two legacy aggregate files were deleted after independent discovery passed 52 and 13 tests. |
| 60 | Rewired the existing Gate leaves and current consumers | The two existing Gate leaves now admit exact five-module and four-module argv tuples; no Gate leaf or workflow job was added. Manifest, workflow, agentic-audit semantics, 9 ownership/archive tests, 52 metadata tests, 13 lifecycle tests, and 162 runner/workflow/manifest/audit tests are GREEN. Active script, test, and GitHub surfaces contain zero old aggregate paths. |
| 61 | Corrected the historical migration assertion reached by Full | The first pre-closure Full run passed the split modules and then found one archive test that still required the deleted aggregate metadata-test path because historical row `r0842` had once planned a rename. The assertion now applies only to the still-unexecuted `r0848` and `r0852` dispositions; the compact historical projection, digest, and count remain unchanged, and no placeholder or redirect was restored. The focused archive suite and manifest are GREEN. |
| 62 | Applied the legal document lifecycle endpoints | SPEC-0154 and SPEC-0155 take their merge-base-legal `active -> completed` hop; SPEC-0157 remains `active` because its merge-base endpoint is `draft`; plan-0157 and task-0157-0001 complete under the execution lifecycle. Repository metadata contracts report `violations=0`; changed-document metadata reports `selected=18 violations=0 legacy_exceptions=0 transition_overrides=0`; all links and alignment each report zero failures and `archive_direct_links_total=0`; the script manifest is GREEN. |
| 63 | Reached the Task 9 pre-closure Full boundary | After the historical-assertion correction, the staged Full profile passed bundles of 39, 19, 33, 43, 20, 13, 52, 15, 40, 295, 233, 17, 13, 31, 15, 45, 6, and 128 tests. The marker is `FULL exit=0`. Final generated-index freshness and post-record Full verification remain the closure boundary. |
| 64 | Completed the Task 9 post-record Full boundary | With the legal lifecycle endpoints and rows 60 through 63 staged, both generated LLM Wiki outputs were fresh and the Full profile again passed bundles of 39, 19, 33, 43, 20, 13, 52, 15, 40, 295, 233, 17, 13, 31, 15, 45, 6, and 128 tests. The final marker in `/tmp/g-task9-postrecord1.txt` is `FULL exit=0`. This row and the completed Plan checklist are the last authored sources; the commit gate reruns generated-index freshness and the same Full profile without any intervening file change. |
| 65 | Closed SPEC-0157 after local main integration | The verified implementation branch fast-forwarded local `main` to `9700c80a`. From that active endpoint, this dedicated closure changes only SPEC-0157 to `completed`; changed-document metadata reports `selected=1 violations=0 legacy_exceptions=0 transition_overrides=0`, active metadata and repository contracts report zero violations, links and implementation alignment report zero failures with `archive_direct_links_total=0`, and the 16-test Spec Package suite is GREEN. The closure Full profile passed bundles of 39, 19, 33, 43, 20, 13, 52, 15, 40, 295, 233, 17, 13, 31, 15, 45, 6, and 128 tests with `FULL exit=0`. No remote push or GitHub control-plane mutation occurred. |

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

### Task 4 — implemented and independently approved

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

### Task 5 — every test module is reachable from the local full plan

The reachability test was written before routing. Its first run left the
admission-only negative GREEN and reported this exact `on_disk - reachable`
set; `reachable - on_disk` was empty:

~~~text
tests.lib.agent_governance.test_agent_governance_contract
tests.lib.ops.test_postgres_logical_upgrade_rehearsal
tests.lib.supply_chain.test_grype_db_seed
tests.lib.test_surface_ownership
tests.validation.test_agentic_audit_semantic_freshness
tests.validation.test_audit_criterion_contract
tests.validation.test_compose_core_readiness
tests.validation.test_generate_llm_wiki
tests.validation.test_provider_hook_parity
tests.validation.test_provider_native_surfaces
tests.validation.test_provider_surface_renderer
tests.validation.test_reference_stage_repo_contract
tests.validation.test_sample_service_delivery_rehearsal
tests.validation.test_script_manifest
tests.validation.test_security_automation_readiness
tests.validation.test_stop_gate_deferred_paths
tests.validation.test_supply_chain_policy
tests.validation.test_tech_stack_version_contract
tests.validation.test_validator_entrypoints
tests.validation.test_workspace_governance_migration
~~~

Direct execution classified twelve modules GREEN: PostgreSQL rehearsal, Grype
seed, audit criterion, all three provider modules, reference-stage contract,
security readiness, stop-gate deferred paths, tech-stack versions, validator
entrypoints, and workspace-governance migration. The other eight were RED and
received these current-owner dispositions before registration:

| Module | Measured cause | Disposition |
| :--- | :--- | :--- |
| `tests.lib.agent_governance.test_agent_governance_contract` | Three subcases copied a Task from retired SPEC-0153 | Replaced with a local semantic fixture in `50583a90` |
| `tests.lib.test_surface_ownership` | The newly written equality oracle reported the exact 20-module gap | Closed by the reachable ownership routes in this Task 5 unit |
| `tests.validation.test_agentic_audit_semantic_freshness` | The fixture copied retired Task evidence | Added a bounded test-owned evidence fixture in `b25b7e32` |
| `tests.validation.test_compose_core_readiness` | A runtime contract test read deleted `docs/04.execution` approval documents | Removed the historical document dependency while preserving resource-limit assertions in `bd0e7645` |
| `tests.validation.test_generate_llm_wiki` | Generated Stage 90 navigation output was stale after the active Task entered the tracked corpus | Regenerated the two declared outputs in `d1bdccd9` |
| `tests.validation.test_sample_service_delivery_rehearsal` | Tests depended on absent mutable `_workspace` readiness and recovery verdicts | Added explicit test-owned verdict fixtures and narrow overrides in `3d765f52` |
| `tests.validation.test_script_manifest` | One generator fixture required retired Task evidence and one assertion contradicted the current retained hook owner | Replaced the fixture in `b25b7e32` and corrected the current-owner expectation in `2f1468f9` |
| `tests.validation.test_supply_chain_policy` | A status assertion read deleted completed-Spec documents instead of the current supply-chain contract | Removed that obsolete assertion in `3ec4246d` |

The retained modules have one responsibility route each:

| Public owner | Reachable leaf | Modules |
| :--- | :--- | :--- |
| `agent-governance` | `leaf.agent-governance-regressions` | Agent-governance contract |
| `agent-governance` | `leaf.provider-governance-regressions` | Provider hook parity, native surfaces, renderer, and stop-gate deferred paths |
| `repository-integrity` | `leaf.repository-integrity-regressions` | Surface ownership, audit semantic freshness, audit criterion, Stage 90 repository contract, script manifest, tech-stack versions, and validator entrypoints |
| `document-lifecycle` | `leaf.document-lifecycle-regressions` | LLM Wiki generation, security readiness, and workspace-governance migration |
| `operations` | `leaf.supply-chain-fixture-policy` | Compose readiness, PostgreSQL rehearsal, Grype seed, supply-chain policy, and delivery rehearsal |

The first integrated Full run exposed one execution-boundary defect that a
standalone provider test could not show: the Gate's sealed
`HYHOME_CI_GATE_ROOT=/proc/self/fd/N` value reached a non-Gate subprocess after
that descriptor was no longer inherited. The provider renderer test now drops
only that internal variable from the subprocess it owns, matching the existing
document-governance test pattern without weakening Gate invocation isolation.
The four new leaves plus local reachability for the existing supply-chain
fixture leaf changed the generated security-readiness observation from 69 to
74 reachable typed gates; the declared 13-control model was regenerated
without adding another Gate or a count assertion.

Final Task 5 evidence:

~~~text
surface ownership and gate/workflow contracts: Ran 96 tests; OK (skipped=11)
agent and provider responsibility groups: Ran 52 tests; OK
repository-integrity group: Ran 127 tests; OK
document-lifecycle group: Ran 40 tests; OK
operations fixture group: Ran 233 tests; OK
check-github-workflow-contract.py: PASS (workflows=7, jobs=9, actions=8)
check-script-manifest.py: PASS
on_disk - reachable: empty
reachable - on_disk: empty

full Gate document-metadata module: Ran 251 tests in 127.543s
FAILED (failures=3, errors=2)
FULL exit=1
~~~

The five Full results are exactly the Task 6 boundary already recorded after
Task 4: the two registered Operations-move fixture errors and the three
source-baseline authorization failures. No Task 5 module, adapter admission,
public owner, local/CI route, generated readiness check, manifest check, or
workflow contract remains RED.

### Task 6 — current document authority and recovery-only history

The fixed-workspace invariant was written before fixture replacement. Its RED
set contained exactly these seven file/token pairs:

~~~text
tests/validation/test_document_metadata.py: HISTORICAL_COMMIT
tests/validation/test_document_metadata.py: LEGACY_CONTRACT_FIXTURE_COMMIT
tests/validation/test_document_metadata.py: docs/99.templates/support/
tests/validation/test_document_corpus_lifecycle.py: HISTORICAL_COMMIT
tests/validation/test_document_corpus_lifecycle.py: docs/99.templates/support/
tests/lib/target_surface/test_target_surface_contracts.py: docs/99.templates/support/
tests/lib/document_governance/test_spec_packages.py: docs/99.templates/support/
~~~

The replacement keeps current document behavior at its current owner. Registry
and template tests load `docs/99.templates/registry.json` and the template path
declared by the applicable role. Operations tests derive their current mapping
from the Stage 05 catalog. Spec Package and target-surface tests use current
registered records. Negative cases copy the bounded current value into a
temporary directory and mutate one relevant field or section.

Tests whose sole subject was the deleted support taxonomy, retired profile
aliases, fixed branch history, or the Stage 98 Migration fixture authority were
removed. They were not translated into a new fixture because no current
Registry, template, or public lifecycle mode owns those contracts. The retained
body-contract tests cover current deficit preservation, non-leaking mutation
diagnostics, template-instruction rejection, Registry key boundaries, and code-
span exclusion.

`HistoricalDocument` is retained only for recovery behavior. That test creates
its own temporary Git repository, commits a regular file and a symlink, removes
the worktree paths, reads the exact regular `commit:path`, and rejects tree,
missing, and non-regular objects. No workspace commit literal, Stage 98 body,
or retired Stage 99 support path remains fixture authority.

Focused GREEN evidence before the final Full boundary:

~~~text
tests.lib.test_surface_ownership: Ran 8 tests; OK
tests.validation.test_document_metadata: Ran 51 tests; OK
tests.validation.test_document_corpus_lifecycle: Ran 13 tests; OK
tests.lib.target_surface.test_target_surface_contracts: Ran 43 tests; OK
tests.lib.document_governance.test_spec_packages: Ran 16 tests; OK
tests.lib.document_governance.test_operations_catalog: Ran 30 tests; OK
forbidden fixed-workspace token search: no output

held-root supply-chain wrapper contract: Ran 28 tests; OK
held-root tech-stack, entrypoint, and supply bundle: Ran 49 tests; OK
held-root lifecycle and metadata bundle: Ran 64 tests; OK
supporting test-harness commits: ecdb7b9e, 3b3733de
~~~

Final staged Full-Gate evidence:

~~~text
Ran 39 tests; OK
Ran 19 tests; OK
Ran 33 tests; OK
Ran 43 tests; OK
Ran 20 tests; OK
Ran 13 tests; OK
Ran 51 tests; OK
Ran 15 tests; OK
Ran 40 tests; OK
Ran 291 tests; OK
Ran 233 tests; OK
Ran 17 tests; OK
Ran 13 tests; OK
Ran 31 tests; OK
Ran 15 tests; OK
Ran 45 tests; OK (skipped=11)
Ran 6 tests; OK
Ran 128 tests; OK
FULL exit=0
~~~

Final document-boundary evidence is also GREEN: repository metadata contracts
reported zero violations; changed-document metadata selected 16 documents with
zero violations, legacy exceptions, or transition overrides; all-links and
implementation-alignment link modes reported zero failures and zero direct
Stage 98 links; and cached diff hygiene passed.

### Task 7 — bounded object-name identity history

The pre-change scanner asked Git for every matching historical patch under six
stage roots. Direct measurement of those patch streams produced:

~~~text
docs/01.requirements 892728
docs/02.architecture 1367353
docs/03.specs 18113008
docs/05.operations 6817929
docs/90.references 20716362
docs/98.archive 11542284
~~~

Object-name enumeration was materially smaller, but the first proposed
path-only value derivation was not sound. Requirement children can declare an
ID only in a document body; Stage 90 can place `ref-*` leaves below an Audit,
Research, or Data package; and a Tombstone filename identifies the retired
target while the Tombstone's own identity remains in frontmatter. Task 7
therefore uses paths only to select the allowable stage and identity family.
It obtains actual issued values from the identity-bearing lines in each source
blob.

The regression was written before the implementation. It rejected the old
`git log -G` route, `_record_history_patch`, and the 64 MiB cumulative history
budget. The replacement:

1. runs one path-bounded `git rev-list --objects` query for each governed stage;
2. validates every returned object path before grouping source object IDs;
3. requests at most 256 objects per `git grep` batch and returns only
   `artifact_id:` lines plus Stage 01 Requirement child-ID lines;
4. shares one 8 MiB output budget and 45-second deadline across the cumulative
   issued-history projection; and
5. leaves the single pinned predecessor-snapshot transition check on a
   separately named 64 MiB per-snapshot budget.

The implementation does not restore branch-SHA tracking or make a historical
commit the current baseline. Current documents still use the existing
regular-file and symlink-safe local reader. Historical objects are immutable
source blobs selected from reachable refs, while identity-family admission is
derived from the current stage contract.

The complete issued-identity set was captured immediately before and after the
scanner replacement. Both canonical JSON captures have the same SHA-256:

~~~text
c96d855fe9b5d9667c01a059a9ceb33e44313eff74bd594c8d46b5e37e495bd6
IDENTITY_SET_EQUAL exit=0
~~~

This hash is transient execution evidence, not a permanent expected-value
oracle. Instrumentation of the new full-history route reported:

~~~text
elapsed_seconds=2.329
identity_spaces=38
grep: calls=37 bytes=839127
ls-files: calls=1 bytes=73008
rev-list: calls=6 bytes=1615062
rev-parse: calls=1 bytes=5
history_git_output_bytes=2454189
~~~

Focused verification before the Full boundary:

~~~text
key bounded-scan regressions: Ran 6 tests in 5.097s; OK
tests.lib.document_governance.test_identity_history:
  Ran 17 tests in 16.188s; OK
check-document-metadata.py --mode check-contracts --history-scope full:
  metadata repository contracts: violations=0
python bytecode compilation: exit=0
git diff --check: exit=0
~~~

Final staged Full-Gate evidence:

~~~text
Ran 39 tests; OK
Ran 19 tests; OK
Ran 33 tests; OK
Ran 43 tests; OK
Ran 20 tests; OK
Ran 13 tests; OK
Ran 51 tests; OK
Ran 15 tests; OK
Ran 40 tests; OK
Ran 294 tests; OK
Ran 233 tests; OK
Ran 17 tests; OK
Ran 13 tests; OK
Ran 31 tests; OK
Ran 15 tests; OK
Ran 45 tests; OK (skipped=11)
Ran 6 tests; OK
Ran 128 tests; OK
FULL exit=0
~~~

Final document-boundary checks are also GREEN: changed-document metadata
selected 16 documents with zero violations, legacy exceptions, or transition
overrides; all-links and alignment modes reported zero failures and zero direct
Stage 98 links; and cached diff hygiene passed.

### Task 8 — production responsibility surfaces

The live consumer command from the Plan produced these 30 untruncated rows
before any production move:

~~~text
tests/lib/document_governance/test_references.py:71:                code = metadata_validator.main(["--root", str(root), "--mode", "check-active"])
tests/lib/document_governance/test_taxonomy.py:480:                "metadata_validator.TARGET_MARKDOWN_PREFIXES",
tests/lib/document_governance/test_taxonomy.py:481:                metadata_validator.TARGET_MARKDOWN_PREFIXES,
tests/lib/document_governance/test_spec_packages.py:670:            ROOT / "scripts/lib/document_governance/metadata_validator.py"
tests/lib/document_governance/test_spec_packages.py:678:                    f"scripts/lib/document_governance/metadata_validator.py:{stale}"
scripts/manifest.yaml:134:  - scripts/lib/document_governance/metadata_validator.py
scripts/manifest.yaml:157:  - scripts/lib/document_governance/metadata_validator.py
scripts/manifest.yaml:168:  - scripts/lib/document_governance/metadata_validator.py
scripts/manifest.yaml:180:  - scripts/lib/document_governance/metadata_validator.py
scripts/manifest.yaml:207:  - tests/lib/document_governance/test_metadata_validator.py
scripts/manifest.yaml:208:- path: scripts/lib/document_governance/metadata_validator.py
scripts/manifest.yaml:219:  - tests/lib/document_governance/test_metadata_validator.py
scripts/manifest.yaml:255:  - scripts/lib/document_governance/metadata_validator.py
scripts/manifest.yaml:268:  - scripts/lib/document_governance/metadata_validator.py
scripts/manifest.yaml:279:  - scripts/lib/document_governance/metadata_validator.py
scripts/manifest.yaml:302:  - scripts/lib/document_governance/metadata_validator.py
tests/lib/document_governance/test_registry.py:25:from scripts.lib.document_governance.metadata_validator import (
tests/lib/document_governance/test_registry.py:118:        from scripts.lib.document_governance.metadata_validator import build_registry_profiles
tests/lib/document_governance/test_registry.py:132:        from scripts.lib.document_governance.metadata_validator import build_registry_profiles
tests/lib/document_governance/test_registry.py:1367:            metadata_validator.__file__
tests/lib/document_governance/test_registry.py:1381:        signature = inspect.signature(metadata_validator.load_profiles)
tests/lib/document_governance/test_registry.py:1383:        profiles = metadata_validator.load_profiles()
scripts/lib/document_governance/metadata_contract.py:5:from scripts.lib.document_governance.metadata_validator import (
tests/lib/document_governance/test_metadata_validator.py:14:from scripts.lib.document_governance.metadata_validator import (
tests/lib/document_governance/test_metadata_validator.py:189:        profiles = metadata_validator.build_registry_profiles(self.registry)
tests/lib/document_governance/test_metadata_validator.py:192:        self.assertEqual("unsupported", metadata_validator.infer_artifact_type(
tests/lib/document_governance/test_metadata_validator.py:256:        from scripts.lib.document_governance.metadata_validator import (
tests/validation/test_script_manifest.py:98:    "scripts/lib/document_governance/metadata_validator.py": "check-write",
tests/validation/test_script_manifest.py:611:            ["scripts/lib/document_governance/metadata_validator.py"],
tests/validation/test_script_manifest.py:630:                "scripts/lib/document_governance/metadata_validator.py",
~~~

The production baselines were 6,794 metadata-validator lines and 5,206
lifecycle-CLI lines. The behavior baselines were 51 and 13 tests respectively,
and every surviving lifecycle mode exited 0. The compatibility test was written
before the split and failed on the missing `__all__` declaration.

The metadata graph is deliberately one-way:

~~~text
profile -> heading -> identity -> lifecycle -> reference -> compatibility facade
~~~

`profile.py` owns shared models, Registry projection, and path classification;
`heading.py` owns Markdown/template-body contracts; `identity.py` owns tracked
source and internal identity validation; `lifecycle.py` owns records and
transition evidence; and `reference.py` owns repository-wide composition,
reports, and the CLI implementation. The facade has explicit imports and a
declared API; it does not use wildcard imports, dynamic loading, or mutable
state forwarding.

The lifecycle graph separates common contract mechanics from each current
surface. `contract.py` owns manifest models, I/O, bounded reads, and safety;
`promoted.py` owns semantic reconciliation; `public.py` owns current Spec
Package lifecycle findings; and `recovery.py` invokes only the minimal Stage 98
recovery-row API. The entrypoint retains parser, CLI-shape, dispatch, common
exit mapping, and explicit compatibility imports.

Measured split sizes:

~~~text
metadata_validator.py 107
metadata/heading.py 864
metadata/identity.py 379
metadata/lifecycle.py 1380
metadata/profile.py 2999
metadata/reference.py 1428
check-document-corpus-lifecycle.py 245
lifecycle/contract.py 3074
lifecycle/promoted.py 1961
lifecycle/public.py 54
lifecycle/recovery.py 30
~~~

Focused evidence before the final Full boundary:

~~~text
metadata compatibility RED: AttributeError for missing __all__
metadata compatibility GREEN: Ran 1 test; OK
metadata direct consumers: Ran 163 tests in 176.426s; OK
lifecycle baseline: Ran 13 tests in 14.144s; OK
surface ownership and validator entrypoints: Ran 11 tests; OK
responsibility-module contract: Ran 1 test; OK
check-public exit=0
check-contract exit=0
check-promoted exit=0
check-recovery exit=0
check-script-manifest.py: PASS
check-github-workflow-contract.py: PASS (workflows=7, jobs=9, actions=8)
affected plus complete taxonomy module: Ran 18 tests; OK
final combined focused bundle: Ran 188 tests in 173.784s; OK
TASK8_FOCUSED_FINAL exit=0
python bytecode compilation: exit=0
git diff --check: exit=0
~~~

Full-boundary convergence evidence:

~~~text
entrypoint mode RED: expected executable 100755; restored from 100644
held-root RED: lifecycle bundle Ran 13 tests; 1 invalid-root assertion failed before package bootstrap
held-root GREEN: lifecycle bundle Ran 13 tests; OK; four business modes exit=0
source-owner RED: document-governance Ran 295 tests; 1 stale CLI-location assertion
source-owner GREEN: focused shared-governance test Ran 1 test; OK
consumer-oracle RED: document-governance Ran 295 tests; OK; later bundle Ran 128 tests; 1 stale taxonomy consumer assertion
consumer-oracle GREEN: test_script_manifest.py Ran 53 tests; OK
final Full bundles: 39,19,33,43,20,13,52,15,40,295,233,17,13,31,15,45,6,128
FULL exit=0
~~~

The manifest changes register libraries and direct dependency evidence only.
They add no public suite, Gate leaf, workflow job, fixture, or fixed test-count
oracle. Task 9 still owns physical TestCase relocation and corresponding runner
rewiring.

### Task 9 — mirrored test responsibility surfaces

The pre-split and post-split inventories are equal:

~~~text
metadata baseline: Ran 52 tests in 58.299s; OK
lifecycle baseline: Ran 13 tests in 14.017s; OK
metadata split: Ran 52 tests in 60.038s; OK
lifecycle split: Ran 13 tests in 13.132s; OK
ownership plus archive derivation: Ran 9 tests; OK
runner, workflow, manifest, and audit contracts: Ran 162 tests; OK (skipped=11)
check-script-manifest.py: PASS
check-github-workflow-contract.py: PASS (workflows=7, jobs=9, actions=8)
audit_semantic_freshness: PASS assertions=11 failures=0
~~~

Whole-class ownership is:

| New test module | Moved TestCase classes | Tests |
| :--- | :--- | ---: |
| `metadata/test_profile.py` | SharedFrontmatterExtraction, FrontmatterParsing, CurrentRegistryContract, TemplateRoleInference, TemplateMetadata | 22 |
| `metadata/test_heading.py` | CurrentBodyContract | 9 |
| `metadata/test_identity.py` | CheckerCli | 9 |
| `metadata/test_lifecycle.py` | TransitionOverrideEvidencePath | 2 |
| `metadata/test_reference.py` | MetadataValidatorCompatibility, RepositoryContractIntegration | 10 |
| `lifecycle/test_contract.py` | SharedProvenance | 3 |
| `lifecycle/test_public.py` | CurrentPublicContract | 9 |
| `lifecycle/test_recovery.py` | HistoricalDocumentRecovery | 1 |
| `lifecycle/test_promoted.py` | No pre-split TestCase existed; direct module and Gate evidence remain | 0 |

No assertion body was re-authored. Unused historical migration globals and
helpers were not copied into the new support modules. The old aggregate paths
have neither body copies nor redirects.

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

Stage 90 preservation correction re-review: `Spec compliance: PASS`;
`Quality: APPROVED`. The reviewer confirmed that the current Task 2 measurement
is the sole protection subject, every named commit is illustrative
provenance only, and the persistent package-local declaration plus existing
reference-test coverage must be GREEN before transient Task evidence retires.
The review also confirmed that the correction adds no top-level Gate, public
suite, validator, schema, content hash, byte-equality oracle, or count pin and
does not mutate any Stage 90 artifact. The preservation design is approved;
actual Stage 90 disposition remains deferred to draft SPEC-0158.

Mandatory Stage 90 cleanup revalidation: the current tracked `RES-0002` package
remains unchanged and complete at this design boundary, while every other
baseline package is now a mandatory delete-after-migration target. Repository
metadata, changed-document metadata, links, and diff hygiene are GREEN, and the
superseded optional-retention phrases are absent. Per the workspace audit
revalidation procedure, implementation acceptance remains `needs_revalidation`
until SPEC-0158 executes the consumer migrations, deletions, persistent
protection declaration, and final package-root measurement.

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
| Task 5 full-profile registration | 50583a90, b25b7e32, bd0e7645, 3ec4246d, 2f1468f9, 3d765f52, d1bdccd9; 9f984929 | Complete; focused contracts GREEN and Full retains only the five Task 6 results |
| Full-Gate held-root test harness | ecdb7b9e, 3b3733de | Complete; one test-only capability helper serves all reached nested subprocess consumers, with 49 supporting and 64 Task 6 tests GREEN under an explicit held-root environment |
| Task 6 current-authority fixtures | ecdb7b9e, 3b3733de; 11529e0c | Complete; fixed-history and archive fixture authority removed, focused suites and final Full GREEN |
| Task 7 bounded identity history | d101142b | Complete; issued set preserved, cumulative history output bounded at 8 MiB, final Full GREEN |
| Task 8 production responsibility split | e72e1ee8 | Complete; explicit production owners, compatibility surfaces, manifest evidence, and final Full GREEN |

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
   count or predecessor list. Its completed invariant is set equality, not a
   twenty-module count pin; every retained module has exact argv admission and
   one reachable public owner.
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
    declaration, and mandatory terminal disposition of every non-protected
    baseline Research, Audit, or Data package. Its completion package-root set
    contains only `RES-0002`, with zero unresolved or pending dispositions;
    structural root/category READMEs are excluded from that set.
18. Stage 00 owns AI-agent governance, system rules, roles, skills, provider
    boundaries, and the common SDLC workflow; Stages 01--03 own the consistent
    Requirements, Architecture, and Spec chain; Stage 05 owns current
    operational profiles; Stage 90 owns non-normative Audit, Research, and Data;
    Stage 98 owns isolated minimal archive records; and Stage 99 owns the docs
    templates and document-shape contract.
19. Stage 98 Migration records are temporary historical inputs, not a durable
    authority or retention target. Draft SPEC-0158 must first decouple the
    active ADR, Stage 99, validators, generators, manifests, tests, and every
    other current consumer; then it removes the Migration contract, documents,
    and directory. Validation stays limited to safe paths, minimal retained-
    record shape, and regular-blob recovery when claimed; no body, digest,
    count, topology, or current-membership contract survives.
20. Stages 00, 01, 02, 03, 05, and 90 must contain zero citations or
    cross-links to Stage 98 documents or files. Draft SPEC-0158 owns the
    source-bounded inventory, current-owner migration, protected-research path
    corrections, generated-index correction, and existing-suite regression.
    Archive navigation is one-way from a retained minimal record to a current
    replacement. This active SPEC-0157 Task performs no archive disposition.
21. Current implementation truth is promoted by meaning: implemented required
    behavior, obligations, invariants, and guarantees belong in Stage 01;
    implemented structure, boundaries, data flow, integration shape, and
    durable decisions belong in Stage 02. Stage 03, Stage 05, Stage 90,
    validators, tests, and code remain evidence or execution surfaces rather
    than the sole durable owner. Draft SPEC-0158 must prove both implementation
    coverage and reverse agreement without a fixed count or new Gate.
22. Cumulative issued-identity history is a bounded object-name and matched-line
    projection, not a historical patch stream. Paths select an allowable
    identity family but never manufacture the identity value. One shared 8 MiB
    budget covers the historical object-name and identity-line output; the
    single predecessor snapshot used by transition validation has a separate
    per-snapshot budget. Neither mechanism makes a branch SHA the current
    baseline.
23. Metadata production dependencies flow only from profile to heading,
    identity, lifecycle, and reference. The compatibility facade declares and
    explicitly re-exports measured consumer names; it does not preserve
    incidental globals, wildcard imports, or assignment forwarding. Lifecycle
    production separates common contract mechanics, promoted reconciliation,
    current public Spec Package checks, and minimal recovery validation behind
    one thin dispatch entrypoint.
24. A production-library split updates direct manifest consumers and uses one
    existing mirrored responsibility test until Task 9 relocates whole test
    classes. It creates no new Gate leaf, workflow job, fixture suite, or count
    pin. Source-contract tests inspect the implementation owner set rather than
    a facade path whose emptiness would make them falsely GREEN.

## Deferred Items

- Stage 90 consumer/lifecycle remeasurement and cleanup belong to draft
  SPEC-0158. Its execution must preserve the atomic `RES-0002` research pack;
  migrate consumers and needed meaning from every other baseline package, then
  delete it. SPEC-0158 cannot complete until only `RES-0002` remains as a
  package and unresolved/pending dispositions are zero. This active SPEC-0157
  Task performs no Stage 90 disposition.
- Stage 98 consumer decoupling, Migration removal, minimal archive
  reclassification, and inbound-reference cleanup belong to draft SPEC-0158.
  This active SPEC-0157 Task changes fixture design so no new current test reads
  archive documents, but it does not mutate Stage 98 or claim the existing
  inbound citations are already removed.
- The subject-level audit and promotion of current implemented obligations to
  Stage 01 and current implemented structures or durable decisions to Stage 02
  belong to draft SPEC-0158. This design record does not claim that the current
  Requirement and Architecture corpus already has zero gaps or contradictions.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Stage 03 index](../../README.md)
