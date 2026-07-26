---
status: active
artifact_id: task:2026-07-26-agent-governance-canonical-convergence
artifact_type: task
parent_ids:
  - spec:134-agent-governance-canonical-convergence
  - plan:2026-07-26-agent-governance-canonical-convergence
---

# Task: Agent Governance Canonical Convergence

## Overview

This ledger records implementation, verification, review, commit, deletion,
and closure evidence for Spec 134. The implementation design remains in the
[Plan](../plans/2026-07-26-agent-governance-canonical-convergence.md).
Evidence in this file must be value-free and bounded: no secret values,
credentials, tokens, auth files, shell history, raw logs, or unbounded provider
output.

## Inputs

- [Spec 134](../../03.specs/134-agent-governance-canonical-convergence/spec.md)
- [Implementation Plan](../plans/2026-07-26-agent-governance-canonical-convergence.md)
- Base commit `e65bb18fa2f6e3fb6235725750c7c57cbe0227ee`
- Isolated branch `feat/agent-governance-canonical-convergence`
- Isolated worktree
  `.worktrees/agent-governance-canonical-convergence`

## Goals and Non-goals

The goal is to close AGCC-001 through AGCC-016 through six independently
reviewed logical commits. Remote mutation, live provider calls, runtime or
Compose changes, secret inspection, direct all-files pre-commit, push, and
remote merge are not authorized by this ledger.

## Scope and Change Boundaries

Allowed primary paths are root provider shims, `.agents/**`, `.claude/**`,
`.codex/**`, `.gemini/**`, `.github/**`, and
`docs/00.agent-governance/**`. Direct-impact paths are limited to Spec 134,
this Plan/Task, Stage 90 canonical evidence/generated owners, provider
renderer/sync code, governance/eval/workflow validators, focused tests, and the
controlled QA wrapper evidence route.

Docker Compose, infrastructure, deployment, release, user-global provider
configuration, credentials, and remote GitHub state remain out of scope.

## Approval Evidence

- User approved Spec 134, the six-task convergence design, and protected
  surfaces as an allowable scope class.
- User chose remote GitHub read-only observation and local tracked workflow
  changes only.
- User allowed subagents and selected Subagent-Driven as the execution method.
- User approved this exact Plan on 2026-07-26. The six local implementation
  tasks, protected local targets, and Plan-bounded destructive cleanup are
  authorized.
- User subsequently required a README-purpose GitHub entry document with a
  filename other than `README.md`; Task 5 now owns navigation-only
  `.github/INDEX.md` and explicitly forbids `.github/README.md`.
- No approval exists yet for the controlled all-files wrapper, push, remote
  merge, workflow dispatch, provider live call, or remote control-plane change.

Rollback is task-commit revert plus exact Git provenance for deleted historical
surfaces. No rollback command may discard unrelated user changes.

## Work Breakdown

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-AGCC-001 | Normalize active contracts and create retirement evidence | contract/data | AGCC-001–004 | Task 1 | duplicate/retirement tests, 14/22/3 contract pass | fresh rules implementer | completed |
| T-AGCC-002 | Update model facts, profiles, renderer, and projections | provider/code | AGCC-005–006, 011 | Task 2 | model/profile tests, native schema, drift 0 | `/root/task2_provider_models` | completed |
| T-AGCC-003 | Establish shared bounded project memory | governance/docs | AGCC-001–002, 007 | Task 3 | import parity, bounds, secret/stale checks | `/root/task3_shared_memory` | completed |
| T-AGCC-004 | Add functions and type harness, loop, and evals | harness/code | AGCC-008–010 | Task 4 | 14/24, 8 layers/states, 11/16 evals | `/root/task4_harness_loops_evals` | completed |
| T-AGCC-005 | Reconcile local Actions/QA, GitHub index, and remote observation | CI/security | AGCC-012–014 | Task 5 | navigation-only index, 16 jobs, zizmor pin, remote inventory | fresh CI implementer | not_started |
| T-AGCC-006 | Refresh canonical evidence and close branch | docs/QA | AGCC-014–016 | Task 6 | audit 11/161, aggregate QA, branch reviews | fresh closure implementer | not_started |

## Work Log

| Date | Task | Actor | Evidence summary |
| --- | --- | --- | --- |
| 2026-07-26 | Planning | Controller | Created isolated worktree, completed official-source and repository discovery, wrote and independently reviewed Spec 134, and drafted this Plan/Task. Dependency-locked validator/renderer baseline remains environment-blocked because `html5lib` is absent and restricted network resolution failed; hook parity passed. |
| 2026-07-26 | Planning review | Independent plan reviewer | Initial review returned C0/I3/M1 for configured-default/runtime eligibility conflation, draft approval overstatement, unsafe deletion sequencing, and thin per-task interfaces. Remediation split repository eligibility from runtime activation, aligned draft authorization, moved every active/generated deletion consumer into T5, and added six exact interface blocks. Re-review returned C0/I0/M0 and APPROVED. |
| 2026-07-26 | Execution approval | User / Controller | User approved the exact independently reviewed Plan. Plan and Task transitioned to `active`; remote mutation, provider live calls, and the controlled all-files wrapper remain separately gated. |
| 2026-07-26 | Active-chain validation | Controller | Scoped metadata validation selected 9 files with 0 violations; traceability and implementation-alignment checks reported 0 failures; generated LLM Wiki owners were fresh; scoped pre-commit passed. The wider merge-base metadata check still reports 8 pre-existing lifecycle-transition findings outside this activation unit. |
| 2026-07-26 | T-AGCC-001 RED | Fresh rules implementer | Added the four Plan-named contract tests before implementation. The focused command ran 4 methods and failed as expected with 4 failing subtests and 1 error: active role transfers and retired status were still accepted, deprecated provider lifecycle remained accepted, and the retirement-ledger interface was absent. The existing duplicate-key fail-closed assertion passed, confirming that no live duplicate-value claim was introduced. |
| 2026-07-26 | T-AGCC-001 implementation | Fresh rules implementer | Removed active role-transfer and deprecated-model state, added the five-record value-free Stage 90 retirement ledger with exact baseline commit/path/blob provenance, added deterministic ledger validation and the two required historical-state failure codes, and updated bounded native-contract observations. Focused GREEN passed 4/4; dependency-locked aggregates passed 143/143 contract and 22/22 native tests; the contract checker passed with `contracts=3 agents=14 functions=22 providers=3 failures=0`; syntax, active-state scan, and `git diff --check` passed. |
| 2026-07-26 | T-AGCC-001 specification review remediation | Independent specification reviewer / Fresh rules implementer | Specification review of `164f2dc5` returned C0/I1/M1. The Important finding showed that the ledger accepted active but unapproved replacements and other syntactically valid fact drift. RED produced 12 expected missing-finding subtest failures. Remediation `587b0373` binds every approved non-provenance fact for all five records and returns one deterministic value-free fact-mismatch code; focused offline GREEN passed 5/5, dependency-locked aggregates passed 144/144 contract and 22/22 native tests, and the contract checker passed with 0 failures. |
| 2026-07-26 | T-AGCC-001 specification re-review | Independent specification reviewer | Re-reviewed implementation `164f2dc5` plus remediation `587b0373`; prior I1 closed through mutation-backed exact fact binding, prior M1 was controller-owned evidence completion, and final specification verdict was C0/I0/M0 APPROVED. |
| 2026-07-26 | T-AGCC-001 quality/security review | Independent quality/security reviewer | Reviewed exact range `a4eb1cc0..587b0373`; confirmed confined duplicate-safe ledger loading, value-free findings, active-reference validation, no Task 2 drift, focused 5/5, native 22/22, checker 14/22/3, and diff check. Final verdict C0/I0/M0 APPROVED. |
| 2026-07-26 | T-AGCC-002 RED | Fresh provider implementer | Added the five Plan-named model/profile/native-renderer tests before implementation. The dependency-locked focused command ran 5 methods and failed as expected with `FAILED (failures=3, errors=2)`: the old 10-model catalog, three work profiles, fallback graph, and missing typed renderer-selection interface displaced the exact Task 2 contract. |
| 2026-07-26 | T-AGCC-002 implementation | Fresh provider implementer | Rebuilt the active catalog from the official sources retrieved at `2026-07-26T20:08:18+09:00`; separated lifecycle, repository disposition, runtime acceptance, entitlement, repository-default eligibility, and runtime activation; selected the exact 11 models, five profiles, and 14 role assignments; moved five displaced models to Stage 90 with immutable `2a8a3af2`/`a376b9d7` provenance; removed the active fallback graph; added typed provider selections and scoped Gemini reasoning overrides; and regenerated exactly 35 managed files with zero deletion. Focused GREEN passed 5/5; dependency-locked aggregates passed 147/147 contract, 23/23 native, and 21/21 renderer tests; contract and repository-provider checks passed; renderer and wrapper drift were zero; `git diff --check` passed. No live provider or entitlement call was made. |
| 2026-07-26 | T-AGCC-002 specification review | Independent specification reviewer | Reviewed exact range `2a8a3af2..63dbc883`; confirmed the exact 11-model catalog and six axes, five profiles, 14 role assignments, no active fallback graph, immutable superseded-model provenance, typed provider selections, native reasoning controls, 35 modified generated files, and zero deletion. Final verdict C0/I0/M1 APPROVED; the sole Minor was this Task ledger's missing implementation hash. |
| 2026-07-26 | T-AGCC-002 quality/security review | Independent quality/security reviewer | Reviewed exact range `2a8a3af2..63dbc883`; confirmed contract and repository-provider validation remained fail-closed, renderer output stayed confined and drift-free, native provider fields remained schema-compatible, and no Critical or Important defect was present. Final verdict C0/I0/M1 APPROVED; the sole Minor was the same Task ledger bookkeeping gap, corrected in this closure update. |
| 2026-07-26 | T-AGCC-003 RED | Fresh memory implementer | Added the four Plan-named shared-memory tests before implementation and corrected their class boundary before recording evidence. The exact focused class ran 4 methods and failed as expected with `FAILED (failures=2, errors=2)`: the current-memory profile and file were absent, root shims still selected historical progress, and the bounded validator constants/interface did not exist. |
| 2026-07-26 | T-AGCC-003 implementation | Fresh memory implementer | Added one advisory `governance-current-memory` profile and bounded seven-section record, routed all three root shims to the same README/current pair, converted progress to append-preserved historical navigation without rewriting its rows, limited provider overlays to loading mechanics, and added value-free bounds, forbidden-material, Task-state, and Git-ancestry checks. Old verification timestamps do not create stale findings. Focused GREEN passed 4/4; the final dependency-locked contract module passed 151/151 after active-consumer and pre-read bound remediation; repository harness passed with 0 failures; traceability passed 46/0; implementation alignment passed 671 documents, 5,598 links, 141 operations documents, and 0 failures; changed metadata passed 19/0; scoped pre-commit passed on exactly 25 Task-owned paths; Ruff check and diff hygiene passed. Independent reviews remain pending. |
| 2026-07-26 | T-AGCC-003 active-consumer convergence | Controller / Fresh memory implementer | Controller expanded ownership to the exact 11 directly active Stage 00 consumers after bootstrap review exposed historical progress as an active instruction. The bounded 13-consumer subtests were added to the existing Plan-named root-parity method; the exact focused class produced expected RED `FAILED (failures=13)`. The governance hub, workflow, harness map, two hook rules, stage matrix, approval boundary, provider capability matrix, agentic rule, documentation protocol, and historical memory finding now use `current.md` for the bounded handoff, the applicable Stage 04 Task for progress/verification/final evidence, and `progress.md` only for append-preserved historical navigation. The historical finding is explicitly superseded, and the provider matrix copies only exact Task 2 model IDs. Final focused GREEN passed 4/4; repository harness, traceability, alignment, metadata 19/0, exact 25-path scoped pre-commit, and diff hygiene passed. No historical progress row was rewritten. |
| 2026-07-26 | T-AGCC-003 pre-read bound remediation | Controller / Fresh memory implementer | Final review found that `_validate_current_memory()` applied the general 2 MiB repository text cap before checking the 32 KiB current-memory contract. The existing size/line/secret/stale test now observes the reader argument and requires an oversized fixture to return only value-free `AGC-MEMORY-BOUNDS` without its payload marker. Focused RED failed exactly once with `32768 != 2097152`; the reader now receives `CURRENT_MEMORY_MAX_BYTES`, focused GREEN passed 4/4, and the final dependency-locked contract module passed 151/151. |
| 2026-07-26 | T-AGCC-003 specification review | `/root/task3_spec_review` | Reviewed exact range `cc7f515a..6a1a9fe3` and returned C0/I0/M1 APPROVED. The sole Minor was the Task ledger's stale `not_committed` implementation field. This bounded bookkeeping update records full implementation commit `6a1a9fe381194462598afdc7901587996e6d20fb`; quality/security review remains pending. |
| 2026-07-26 | T-AGCC-003 quality/security review | `/root/task3_quality_security_review` | Reviewed exact range `cc7f515a..a56234ee`; returned C0/I0/M0 and `QUALITY_SECURITY: APPROVED`. The specification-review bookkeeping Minor is closed, both independent Task 3 reviews are complete, and T-AGCC-003 transitions to `completed`. |
| 2026-07-26 | T-AGCC-004 RED | Fresh harness implementer | Added Task 4 capability/function, typed harness/workflow, renderer-cardinality, and evaluator-cardinality/context assertions before production changes. The nine-test focused slice failed as expected with `FAILED (failures=4, errors=10)`: the catalog still had 22 functions, both new function documents and projections were absent, typed layers/states were absent, and the evaluator still exposed 8 fixtures and 10 regressions. |
| 2026-07-26 | T-AGCC-004 implementation | `/root/task4_harness_loops_evals` | Added `provider-model-evaluation` and `project-memory-stewardship` without increasing the 14-role set; recorded the dated Agency upstream comparison as nine bounded `merge`/`defer`/`reject` intake rows without importing personality prose; typed exactly eight control-plane layers and the sole ordered eight-state discover-to-handoff lifecycle; bound the four existing loops to applicable states; expanded deterministic evaluation to 11 fixtures and 16 balanced regressions; and regenerated four new shared skills plus the two deterministic Claude owner skill lists. Focused GREEN passed 5/5 Task 4 contract tests and the nine-test cross-module slice; renderer passed 21/21; evaluator passed 38/38; integrated contract, repository, projection, fixture, metadata, traceability, alignment, Ruff, byte-compilation, diff-hygiene, and exact 20-path scoped pre-commit checks passed. No live provider call, runtime change, remote mutation, or controlled all-files wrapper was used. Specification and quality/security reviews were pending at implementation handoff. |
| 2026-07-26 | T-AGCC-004 controller aggregate RED | Controller / `/root/task4_harness_loops_evals` | The dependency-locked full contract module initially ran 156 tests with one failure: the governed inventory assertion remained at 112 while the two registered canonical function documents correctly raised the inventory to 114 (`112 != 114`). The inventory test now binds 114 to explicit membership of both new function paths rather than applying a blind cardinality bump. The renamed inventory test plus both Task 4 classes passed 6/6; the controller's final dependency-locked rerun passed 156/156 in 253.230 seconds. |
| 2026-07-27 | T-AGCC-004 specification review | `/root/task4_spec_review` | Reviewed exact range `b2e090bd..fe98190b` and returned C0/I0/M1 APPROVED. The sole Minor was bookkeeping that still described the implementation as a working tree with `not_committed_controller_owned`; this closure records full implementation commit `fe98190b2f7625adab7d0ee2be8735d0e5879a87`. Specification review is complete; quality/security review remains pending, so T-AGCC-004 remains `review_pending`. |
| 2026-07-27 | T-AGCC-004 quality/security review | `/root/task4_quality_security_review` | Reviewed exact range `b2e090bd..c45e2925` and returned C0/I0/M0 with `QUALITY_SECURITY: APPROVED`. Adversarial review covered bounded attempts and failure returns, approval and mutation authority, value-free evidence, source/runtime claim separation, path and renderer ownership, synthetic-only evaluation, and the no-live-provider/no-secret boundary. Specification and quality/security reviews are complete, so T-AGCC-004 transitions to `completed`. |
| 2026-07-26 | T-AGCC-005 interface amendment | User / Controller | Added the approved non-README GitHub entrypoint to the active Plan as `.github/INDEX.md`. Its authority is navigation-only, its frontmatter is forbidden, its exact five-section envelope and canonical links are validator-owned, and policy, job identity, secret/variable names, and remote enforcement claims remain in their canonical owners. |

Implementation rows are appended only after the responsible agent finishes a
logical unit. Review rows identify the exact reviewed commit range and finding
disposition.

## Verification Evidence

| Task | RED evidence | GREEN evidence | Aggregate evidence | State |
| --- | --- | --- | --- | --- |
| T-AGCC-001 | Initial focused 4 methods → expected `FAILED (failures=4, errors=1)` before implementation; duplicate-key assertion independently passed. Review remediation: offline `RetirementLedgerTests.test_retirement_ledger_rejects_exact_fact_mutations_without_values` → expected `FAILED (failures=12)` before exact-fact binding. | Initial focused 4 methods → `OK`. Offline remediation mutation test → 1 method/12 mutation cases `OK`; offline focused Task 1 set including the mutation test → 5/5 `OK`. | Current dependency-locked aggregates → 144/144 contract and 22/22 native `OK`. Current remediation checker → `PASS contracts=3 agents=14 functions=22 providers=3 failures=0`; `git diff --check` passed. Specification and quality/security reviews both C0/I0/M0 APPROVED. | completed |
| T-AGCC-002 | Dependency-locked five Plan-named tests → expected `FAILED (failures=3, errors=2)` before implementation: exact catalog/profile/fallback assertions failed and the typed renderer-selection interface was absent. | Focused five Plan-named tests → 5/5 `OK`; full provider-native module → 23/23 `OK`; full renderer module → 21/21 `OK`. | Dependency-locked contract module → 147/147 `OK`; contract checker → `PASS contracts=3 agents=14 functions=22 providers=3 failures=0`; repository provider section passed; renderer and locked wrapper checks both reported `providers=3 drift=0`; exact generated inventory was 35 modified, 0 deleted; scoped pre-commit and `git diff --check` passed. Specification and quality/security reviews both returned C0/I0/M1 APPROVED; the shared bookkeeping Minor is corrected in this closure update. | completed |
| T-AGCC-003 | Four Plan-named tests → expected `FAILED (failures=2, errors=2)` before implementation because the profile/file/root route and validator interface were absent. Active-consumer convergence → expected `FAILED (failures=13)` before the exact 11 additional consumers were remediated. Pre-read bound remediation → one expected failure, `32768 != 2097152`. | Focused `Task3SharedProjectMemoryTests` → 4/4 `OK`, including root parity, 13 bounded direct consumers, pre-read byte cap, value-free oversized rejection, forbidden material, inactive/missing Task, non-ancestor commit, and no wall-clock stale heuristic. | Final dependency-locked contract module → 151/151 `OK`; current repository harness → `failures=0`; traceability → 46/0; alignment → 671 documents / 5,598 links / 141 operations documents / 0 failures; changed metadata 19/0; exact 25-path scoped pre-commit and diff hygiene passed. Specification C0/I0/M1 APPROVED with its Minor closed; quality/security C0/I0/M0 APPROVED. | completed |
| T-AGCC-004 | Nine-test cross-module slice before production changes → expected `FAILED (failures=4, errors=10)` for 22/24 function cardinality, missing function documents/projections, missing layers/states, and 8/11 plus 10/16 evaluator cardinality. Controller full locked module → 156 tests with one inventory failure, `112 != 114`. | Final nine-test slice → 9/9 `OK`; exact Task 4 contract classes → 5/5 `OK`; renderer → 21/21 `OK`; evaluator → 38/38 `OK`; wrapper → 11/11 fixtures and 16/16 regressions. The renamed inventory test plus both Task 4 classes passed 6/6, including 114 artifacts and explicit inclusion of both new canonical function paths. | Final dependency-locked contract module → 156/156 `OK`; contract checker → `PASS contracts=3 agents=14 functions=24 providers=3 failures=0`; repository all → 0 failures; renderer drift → 0; metadata changed → 0 violations; traceability → 46/0; alignment → 671 documents / 5,598 links / 141 operations documents / 0 failures; Ruff, byte-compilation, `git diff --check`, and exact 20-path scoped pre-commit passed. Specification C0/I0/M1 APPROVED with its sole bookkeeping Minor closed; quality/security C0/I0/M0, `QUALITY_SECURITY: APPROVED`. | completed |
| T-AGCC-005 | not_run | not_run | not_run | not_started |
| T-AGCC-006 | not_run | not_run | not_run | not_started |

Environment-blocked checks retain their exact missing dependency or capability
and rerun route. They are never recorded as product pass or failure.

## Controlled Agent Pre-commit Evidence

| Field | Current evidence |
| --- | --- |
| Command | `not_run` |
| Approval | `not_approved_for_run` |
| Allowed prefixes | Plan Task 6 exact list; inactive until per-run approval |
| Exit status | `not_run` |
| Snapshot result | `not_run` |
| Observation boundary | Git-visible non-ignored paths only |
| Before/after/changed/unexpected path sets | `not_run` |
| Disposition | Direct `pre-commit run --all-files` remains prohibited |

## Review Evidence

| Task | Implementer | Specification reviewer | Quality/security reviewer | Exact range | Verdict | Findings |
| --- | --- | --- | --- | --- | --- | --- |
| T-AGCC-001 | `/root/task1_contract_retirement` | `/root/task1_spec_review` | `/root/task1_quality_review` | `a4eb1cc0..587b0373` | approved | initial spec C0/I1/M1; I1 remediated in `587b0373`; spec re-review C0/I0/M0; quality/security C0/I0/M0 |
| T-AGCC-002 | `/root/task2_provider_models` | `/root/task2_spec_review` | `/root/task2_quality_security_review` | `2a8a3af2..63dbc883` | approved | specification C0/I0/M1; quality/security C0/I0/M1; shared evidence-ledger Minor corrected in the closure update |
| T-AGCC-003 | `/root/task3_shared_memory` | `/root/task3_spec_review` | `/root/task3_quality_security_review` | `cc7f515a..a56234ee` | approved | specification C0/I0/M1 APPROVED with sole missing-commit Minor closed; quality/security C0/I0/M0, `QUALITY_SECURITY: APPROVED` |
| T-AGCC-004 | `/root/task4_harness_loops_evals` | `/root/task4_spec_review` | `/root/task4_quality_security_review` | `b2e090bd..c45e2925` | approved | specification C0/I0/M1 APPROVED with sole working-tree/not-committed bookkeeping Minor closed; quality/security C0/I0/M0, `QUALITY_SECURITY: APPROVED`; adversarial boundaries reviewed |
| T-AGCC-005 | not_assigned | not_assigned | not_assigned | not_available | not_reviewed | not_reviewed |
| T-AGCC-006 | not_assigned | not_assigned | not_assigned | not_available | not_reviewed | not_reviewed |
| Whole branch | not_applicable | not_assigned | not_assigned | `e65bb18f..HEAD` | not_reviewed | not_reviewed |

## Commit Ledger

| Task | Logical unit | Expected commit | Actual commit | Validation |
| --- | --- | --- | --- | --- |
| T-AGCC-001 | active contract/retirement normalization | `refactor(governance): normalize active agent contracts` | `164f2dc5` | 144/144 contract, 22/22 native, checker 14/22/3, scoped pre-commit pass |
| T-AGCC-001-R1 | exact retirement fact enforcement | `fix(governance): enforce retirement ledger facts` | `587b0373` | 12-case RED, focused 5/5, specification and quality/security re-review approved |
| T-AGCC-002 | model policy and provider projections | `feat(providers): update model policy and projections` | `63dbc883` | focused 5/5, contract 147/147, native 23/23, renderer 21/21, checker 14/22/3, repository providers and drift checks pass |
| T-AGCC-003 | shared project memory | `feat(governance): establish shared project memory` | `6a1a9fe381194462598afdc7901587996e6d20fb` | focused 4/4 with 13 direct consumers and pre-read cap, final contract 151/151, repository harness 0, traceability 46/0, alignment 671/5,598/141/0, metadata 19/0, exact 25-path scoped pre-commit pass |
| T-AGCC-004 | functions, harness, loop, evals | `feat(harness): converge agent functions and loops` | `fe98190b2f7625adab7d0ee2be8735d0e5879a87` | full locked contract 156/156, focused 5/5, renderer 21/21, evaluator 38/38, checker 14/24/3, repository all, drift, and exact 20-path scoped pre-commit pass; specification C0/I0/M1 and quality/security C0/I0/M0 APPROVED |
| T-AGCC-005 | local CI/QA and remote observation | `ci(governance): reconcile agent quality controls` | not_committed | not_run |
| T-AGCC-006 | canonical evidence and closure | `docs(governance): close canonical convergence evidence` | not_committed | not_run |

Review remediation and lifecycle closure commits are added as separate rows
when required.

## Deletion and Consolidation Ledger

| Path | Decision | Consumer scan | Canonical replacement | Provenance | Rollback | Review |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/00.agent-governance/contracts/agent-catalog.yaml#role_transfers` | removed from the active contract; historical role transitions retained only as evidence | active-contract scan found no `role_transfers:` or `status: retired`; focused catalog and ledger tests passed | `docs/90.references/data/governance/agent-governance-retirement-ledger.yaml` records `style-enforcer` → roles `qa-engineer`, `rules-engineer` plus function `style-validation`, and `wiki-curator` → role `doc-writer` plus function `knowledge-map-agent` | commit `e65bb18fa2f6e3fb6235725750c7c57cbe0227ee`, path `docs/00.agent-governance/contracts/agent-catalog.yaml`, blob `9f6a0fba4df6d37ab5f1a3390dc57d0dd99e8034` | `git restore --source=e65bb18fa2f6e3fb6235725750c7c57cbe0227ee -- docs/00.agent-governance/contracts/agent-catalog.yaml` | specification and quality/security C0/I0/M0 |
| `docs/00.agent-governance/contracts/provider-models.yaml#deprecated-models-and-fallback-approvals` | removed the three historical model rows and their fallback approvals from the active contract | active-contract scan found no deprecated lifecycle or retired model IDs; focused provider and ledger tests passed | retirement ledger records `claude-opus-4-1-20250805` → `claude-opus-4-8`, `gpt-5.2-codex` → `gpt-5.6-terra`, and `gemini-3.1-flash-lite-preview` → `gemini-3.1-flash-lite` | commit `e65bb18fa2f6e3fb6235725750c7c57cbe0227ee`, path `docs/00.agent-governance/contracts/provider-models.yaml`, blob `58ee9b29cb0e519a34ff919e1e29791171c458a4` | `git restore --source=e65bb18fa2f6e3fb6235725750c7c57cbe0227ee -- docs/00.agent-governance/contracts/provider-models.yaml` | specification and quality/security C0/I0/M0 |
| `docs/00.agent-governance/contracts/provider-models.yaml#superseded-models-and-fallback-policy` | displaced five legacy active records into historical evidence and removed the remaining active fallback registry/edge policy; current catalog-only models remain non-deprecated | exact active-set and no-fallback tests passed; consumer scan covered profiles, catalog roles, renderer, all provider projections, and validators; no displaced ID or fallback field remains active | retirement ledger records `claude-opus-4-8` → `claude-opus-5`, `gpt-5.6` → `gpt-5.6-sol`, `gemini-3.1-flash-lite` → `gemini-3.5-flash-lite`, and both `gemini-3.1-pro-preview` and `gemini-3.5-flash` → `gemini-3.6-flash` | commit `2a8a3af24b7e4b98d9f9a0dfba5c7f938af1ae82`, path `docs/00.agent-governance/contracts/provider-models.yaml`, blob `a376b9d76263c3c2c42fbcb480af1791c1ec7a6f` | restore Task 2 paths from `2a8a3af24b7e4b98d9f9a0dfba5c7f938af1ae82` or revert `63dbc883` | specification and quality/security C0/I0/M1 APPROVED; shared bookkeeping Minor corrected |
| `docs/00.agent-governance/memory/github-ci-contract-audit.md` | planned_remove in T-AGCC-005 | pending | Stage 00 GitHub policy plus Stage 90 remote observation | commit `e65bb18f`, blob `7bf6427ad8f29ab8b0d7c001cf330e29b941cdfe` | `git restore --source=e65bb18f -- docs/00.agent-governance/memory/github-ci-contract-audit.md` | pending |
| renderer-managed stale projections | preserved; renderer reported content updates only | renderer changed exactly 7 Claude role files, 13 Codex role files, 14 Gemini role files, and `.gemini/settings.json`; no stale path or deletion was reported | current renderer projection with exact models and provider-native reasoning controls | not_applicable because deletion count was zero | revert `63dbc883` | specification and quality/security C0/I0/M1 APPROVED; shared bookkeeping Minor corrected |
| all other target files | preserve unless exact Plan deletion gate is met | pending final scan | not_applicable | Git history | task commit revert | pending |

## Deferred and Blocked Items

| Item | State | Reason | Destination |
| --- | --- | --- | --- |
| Provider live acceptance, entitlement, quality/cost/latency comparison | deferred | requires separate runtime, privacy, cost, and external-action approval | future provider-evaluation spec |
| Remote ruleset, protection, required-check, environment, secret, and variable verification | unverified | GitHub authentication unavailable; remote is read-only | Stage 90 observation plus future approved GitHub task |
| Runtime, Compose, infrastructure, deployment, and release changes | deferred | explicitly outside Spec 134 | existing runtime readiness specs |
| Dependency-locked validator/renderer | resolved | the locked offline `uv --with-requirements scripts/requirements.txt` environment ran all 191 Task 2 aggregate tests and both drift checks successfully; bare system Python still fails closed on missing `html5lib` | retain the dependency-locked invocation for subsequent tasks |
| Controlled all-files wrapper | not_approved_for_run | requires separate exact user approval and clean committed candidate | T-AGCC-006 |
| Push/remote merge/remote branch cleanup | not_approved | requires separate finish action approval | finishing-a-development-branch handoff |

## Related Documents

- [Spec 134](../../03.specs/134-agent-governance-canonical-convergence/spec.md)
- [Implementation Plan](../plans/2026-07-26-agent-governance-canonical-convergence.md)
- [Agent governance](../../00.agent-governance/README.md)
- [Canonical research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Canonical audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
