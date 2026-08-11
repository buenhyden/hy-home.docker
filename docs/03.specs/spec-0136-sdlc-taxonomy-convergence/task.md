---
status: active
artifact_id: task-0136-01
artifact_type: task
parent_ids:
  - spec-0136
  - plan-0136
created: 2026-08-09
updated: 2026-08-11
---
# Task: SDLC Taxonomy and Agent Governance Convergence

## Overview

Execution evidence for the approved SDLC Taxonomy and Agent Governance
Convergence implementation plan.

## Inputs

- [Specification](spec.md)
- [Approved implementation plan](plan.md)

## Goals and Non-goals

- Complete the approved implementation plan without changing Runtime, remote
  systems, secrets, or the Operations stage number.
- Keep stable identifiers in documentation paths and preserve execution
  evidence through the planned migration.

## Scope and Change Boundaries

Allowed paths and exclusions are defined by the approved implementation plan.

- Operations remains Stage 05.
- No Runtime, remote action, secret, or compatibility-surface change is in
  scope.

## Approval Evidence

| Approval source | Protected surface | Boundary | Rollback or recovery | Redaction boundary |
| :-- | :-- | :-- | :-- | :-- |
| Approved implementation plan (corrected at `5d22b5f0`) and Task 5 controller authorization | Documentation taxonomy, typed metadata, migration ledger, and validation scripts | Tasks 1–5 only. Task 5 includes the single cycle-breaking Operations exception in which the frozen `policy-0006` move row and Stage 04 roadmap merge row converge on the same target; no other Operations migration and no Runtime, remote, secret, deployment, or compatibility-surface change | Git revert of the applicable logical commit; migration mappings retain source-to-target provenance | Record only paths, commit IDs, and command outcomes; do not record credentials or remote state |

## Work Breakdown

1. Task 1: Add the Stable Document Taxonomy Engine
2. Task 2: Establish Canonical Stage 00 and Stage 99 Contracts
3. Task 3: Freeze the Migration Ledger and Script Manifest
4. Task 4: Migrate Requirements and Architecture
5. Task 5: Co-locate Spec, Plan, and Task and Remove Stage 04
6. Task 6A: Reorganize Operations Domains 00 through 03
7. Task 6B: Reorganize Operations Domains 04 through 06
8. Task 6C: Reorganize Operations Domains 07 through 09
9. Task 6D: Complete Operations Domains 10 through 12
10. Task 7: Consolidate References and Archive on Stable IDs
11. Task 8: Reconcile Stage 00 Rules and Provider Projections
12. Task 9: Enforce the Script Manifest and Consolidate Generators
13. Task 10: Consolidate Document Validators
14. Task 11: Decompose the Repository Policy Monolith and Remove One-Time Tools
15. Task 12: Align CI, Local, and Hook Gates
16. Task 13: Repair Cross-Links, Indexes, Memory, and Generated Evidence
17. Task 14: Remove Transition Contracts and Complete Regression Verification

## Work Log

| Task | Work performed | Result |
| :-- | :-- | :-- |
| Task 1 | Added the stable document taxonomy engine, its focused tests, and this Task scaffold. | Approved; commits `cc4ff8d3`, `c8aaac30`, and `e3f40c70`. |
| Task 2 | Established the Stage 00 and Stage 99 typed document contracts, including the bounded metadata-validator update required for the target profiles. | Approved; commits `a69e8681`, `6aca9919`, `10dc809b`, and `232effd9`. |
| Task 3 | Froze the evidence-based SDLC migration ledger and script manifest, including replacement-preservation coverage. | Approved; commits `0dd2579f`, `a6f602f5`, `068d6645`, and `ce52501e`. |
| Task 4 | Migrated Stage 01/02 to stable PRD, Architecture Description, and ADR identities; corrected the Description README ledger row; migrated tracked inbound links and taxonomy regressions. | Committed as `4122cecf` (`docs: migrate requirements and architecture identities`). |
| Task 5 | Co-located current Specs, Plans, and Tasks; moved completed evidence into typed change packets; restored four current Specs; rewrote 28 retired Specs as concise provenance tombstones; removed capability child READMEs and Stage 04; executed the authorized `policy-0006` move-and-merge exception; migrated inbound consumers and rewrote the Stage 03/98 indexes. | APPROVED after two remediation rounds; implementation committed as `65e994f3`. |

## Verification Evidence

| Command | Expected evidence | Actual evidence | Result |
| :-- | :-- | :-- | :-- |
| `PYTHONPATH=. .venv/bin/python tests/validation/test_document_taxonomy.py` (Task 1) | Stable-identity taxonomy checks pass after each correction. | GREEN results progressed from `2` to `4` to `5` tests, all `OK`; the recorded RED states covered the missing module, direct-only inherited identity, and mismatched inherited identity. | PASS (recorded outcome) |
| `PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py` (Task 1) | Preserve the approved metadata baseline without new failures. | `225` tests, `16` failures, exit `1`; Task 1 added no failure. | Approved baseline preserved |
| `git diff --check` and `git diff --cached --check` (Task 1) | No whitespace errors before commit. | Both passed with no whitespace errors. | PASS (recorded outcome) |
| `python3 scripts/validation/check-document-metadata.py --mode check-contracts` and `python3 scripts/validation/check-agent-governance-contract.py --mode contract` (Task 2) | Typed metadata and Stage 00 contracts have no violations. | `violations=0`; `contracts=3 agents=14 functions=24 providers=3 failures=0`. The Task 2 report records that these `python3` invocations used the repository virtual environment on `PATH`. | PASS (recorded outcome) |
| `PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py`, `PYTHONPATH=. .venv/bin/python tests/validation/test_agent_governance_contract.py`, and `PYTHONPATH=. .venv/bin/python tests/validation/test_document_taxonomy.py` (Task 2) | Complete metadata, governance, and focused taxonomy suites pass. | Metadata `237/237`; governance `158/158`; taxonomy `5/5`. | PASS (recorded outcome) |
| `.venv/bin/python scripts/operations/provider_surface_renderer.py --check` and `git diff --check` (Task 2) | Provider projections have no drift and diff has no whitespace errors. | `providers=3 drift=0`; diff check passed with no output. | PASS (recorded outcome) |
| `python3 -m unittest tests.validation.test_script_manifest -v`, `python3 -m unittest tests.validation.test_document_taxonomy -v`, and `python3 -m unittest tests.validation.test_document_metadata.Task2StableTaxonomyFixtures -v` (Task 3) | Manifest, taxonomy, and Task 2 profile fixtures pass. | `23` tests in `5.802s`, `5` tests in `0.000s`, and `14` tests in `3.135s`; all `OK`. These are the final commands recorded in the Task 3 report. | PASS (recorded outcome) |
| `python3 scripts/validation/check-document-metadata.py --mode check-contracts` and `python3 -m py_compile tests/validation/test_script_manifest.py` (Task 3) | Metadata contracts have no violations and the manifest test compiles. | `violations=0`; compilation `PASS`. These are the final commands recorded in the Task 3 report. | PASS (recorded outcome) |
| `PYTHONPATH=. .venv/bin/python tests/validation/test_document_taxonomy.py` (Task 4 RED) | New migration assertions fail against the pre-migration paths. | `7` tests with `2` expected failures: `25` Stage 01 leaves lacked `prd-`; `26` Stage 02 paths remained under `requirements/`. | RED confirmed |
| Task 4 focused taxonomy suite (same command after migration) | Stage 01/02 path, metadata, parent, ledger-row, link, and legacy-vocabulary assertions pass. | Task 4 report records `14/14` passed, zero old link destinations, zero active old-path publications outside evidence-only provenance, and zero Stage 01/02 legacy architecture vocabulary. | PASS (recorded outcome) |
| `PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py` (Task 4) | Full metadata suite passes. | Task 4 report records `237/237` passed in `95.941` seconds. | PASS (recorded outcome) |
| `bash scripts/validation/check-doc-implementation-alignment.sh` (Task 4) | Findings do not increase. | Task 4 report records `181` findings with exit `1`, all predecessor active-to-archive links, down from `590`; moved-path missing links were zero. | Non-increase gate satisfied; repository-wide legacy findings deferred |
| `git diff --check` (Task 4) | No whitespace errors. | Task 4 report records no output. | PASS (recorded outcome) |
| `PYTHONPATH=. .venv/bin/python tests/validation/test_document_corpus_lifecycle.py` (Task 5 RED) | New co-location checks fail before migration on current directory shapes and Stage 04 presence. | `125` tests with `44` failures; the focused four-test class then failed on `27` legacy capability directories and Stage 04 presence. | RED confirmed |
| `PYTHONPATH=. .venv/bin/python -m unittest tests.validation.test_document_corpus_lifecycle.CoLocatedExecutionTests -v` (Task 5 remediation GREEN) | Stable capability identities, zero broken moved/current links, no child READMEs, canonical Plan/Task role names, no Stage 04, exact execution of all `337` selected ledger rows, stale-consumer fail-closed behavior, and an exactly bounded promoted reconciliation. | `10/10` passed in `21.520s`; the new RED state was three `AttributeError` failures before the execution/link proof existed. | PASS |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD`, `--mode check-contracts`, and `PYTHONPATH=. .venv/bin/python tests/validation/test_document_metadata.py` (Task 5 remediation) | Every Task 5 changed typed document passes, contracts remain valid, and the complete metadata suite passes. | Changed range `selected=556 violations=0 legacy_exceptions=76`; contracts `violations=0`; `238/238` tests passed in `134.326s`. | PASS |
| `PYTHONPATH=. .venv/bin/python tests/validation/test_document_corpus_lifecycle.py` (Task 5 remediation full suite) | Task 5 structural, link, execution-proof, source-blob, and historical-source regressions pass without errors; later-wave repository debt remains visible. | Root-controller rerun after remediation round 2: `133` tests in `620.246s`; `43` failures and `0` errors. Task 5 focused assertions are `11/11`. Residual classes remain Acceptance Finding remediation `18`, archive provenance `2`, final-review validator remediation `9`, transitional human contracts `6`, target-surface/sample manifest fixtures `7`, and promoted CLI transition debt `1`; Plan Tasks 7, 10, and 14 own those surfaces. | Task 5 subset PASS; later-wave residual recorded |
| `python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-promoted` (Task 5 final) | Every Task 5 stale promoted finding is reconciled without accepting later-wave debt. | Findings reduced from `72` to `42`; the exact Task 5 subset reduced from `30` to `0`. The retained `42` are Operations Task 6 `28`, Task 4 Stage 01/02 successor debt `4`, and unrelated Task 7/13/14 target-surface debt `10`. | Task 5 scoped gate PASS; repository command exits `1` on retained later-wave debt |
| `bash scripts/validation/check-doc-implementation-alignment.sh` (Task 5 remediation) | No active document links directly to Stage 98 and active links resolve. | `381` stage documents, `2,529` links checked, `archive_direct_links_total=0`, `failures=0`. | PASS |
| Task 5 taxonomy, manifest, provider, compilation, and diff gates | Stable taxonomy, frozen-ledger consumers, provider projections, Python syntax, and whitespace remain valid. | Taxonomy `14/14`; script manifest `23/23`; provider renderer `providers=3 drift=0`; `py_compile` passed; both cached and worktree `git diff --check` passed; `docs/04.execution` is absent. | PASS |

## Controlled Agent Pre-commit Evidence

| Command | Allowed prefixes | Exit status | Snapshot result | Observation boundary | Path sets | Disposition |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Not run for Tasks 1–5 | N/A | N/A | No controlled-wrapper snapshot is available in the examined ledger or Task 4 report, and Task 5 did not run the controlled all-files wrapper. | No claim of ignored/outside-write detection. | N/A | Skipped: the approved Task 5 brief requires focused lifecycle, metadata, promoted, alignment, taxonomy, manifest, provider, and diff gates rather than the controlled all-files wrapper. |

## Review Evidence

| Review | Verdict | Findings and disposition |
| :-- | :-- | :-- |
| Task 1 independent review | APPROVED | Scratch ledger records approval of direct/inherited stable identities, parent/child correlation, dated-path findings, deterministic ordering, caller-supplied profiles, and the Task scaffold. Reviewer identity is unavailable in the examined durable evidence. |
| Task 2 independent review | APPROVED | Scratch ledger records approval of the Stage 00/99 contracts, typed role dates, conditional Operations headings, bounded migration phase, stable-ID CLI enforcement, Stage 98 archive authority, active routes, and negative scans. Reviewer identity is unavailable in the examined durable evidence. |
| Task 3 independent review | APPROVED | Scratch ledger records approval that all `66` script rows and all `796` ledger rows have the required evidence and preservation properties. Reviewer identity is unavailable in the examined durable evidence. |
| Task 4 initial review | CHANGES_REQUIRED (`C0/I1/M0`) | One Important finding: the canonical Task had blank work, verification, review, and commit evidence even though Task 4 was committed. This evidence remediation records the factual ledger and `4122cecf`; no production behavior changed. |
| Task 4 scoped re-review | APPROVED | The original Important finding is ADDRESSED; no new Critical or Important finding. Reviewed fix range: `b827289f..8513d0d1`. The changed-metadata `path-id-mismatch` is explicitly non-blocking because Plan Task 5 owns the atomic capability-directory move. Reviewer identity is not recorded in the supplied evidence. |
| Task 5 initial independent review | CHANGES_REQUIRED (`C0/I3`) | Important findings: `1,010` broken change-packet links plus `8` active/non-archive consumers; `560` changed-metadata violations across `556` selected documents; and an over-broad Foundation consumer-mismatch reconciliation predicate. |
| Task 5 remediation round 1 | ADDRESSED | Rebased all `1,010` change-packet links and repaired the `8` consumers; changed metadata is `selected=556 violations=0 legacy_exceptions=76 transition_overrides=0`; reconciliation now requires the exact `337`-row action distribution, every disposition target, Stage 03/04 topology, and current-link resolution. Focused resolver and negative proofs passed; historical candidate-manifest proofs passed `3/3`; alignment (`381` docs, `2,529` links, `0` failures), taxonomy (`14/14`), manifest (`23/23`), provider (`3`, drift `0`), compilation, and both diff checks passed. |
| Task 5 second independent re-review | CHANGES_REQUIRED (`C0/I1/M0`) | Important finding: the reconciliation source proof accepted a syntactically valid `source_commit` without proving that `source_commit:legacy_path` resolves to a regular Git blob. |
| Task 5 remediation round 2 | ADDRESSED | Every selected ledger source now requires an exact Git commit and regular-blob proof before promoted reconciliation can be enabled; invalid commit, missing path, and tree-object negatives fail closed while the exact `337`-row distribution and current target/source/link checks remain enforced. |
| Task 5 third scoped re-review | APPROVED | The prior Important finding is ADDRESSED. The reviewer reproduced focused Task 5 `11/11`, source/promoted `4/4`, promoted residual `42` with Task 5 subset zero, compilation, and cached diff hygiene; no Critical or Important finding remains. |

## Commit Ledger

| Commit identity | Logical unit | Validation |
| :-- | :-- | :-- |
| `cc4ff8d3`, `c8aaac30`, `e3f40c70` | Task 1 taxonomy engine and inherited-identity fixes | Focused taxonomy `5/5`; metadata at approved `225`-test/`16`-failure baseline; diff hygiene. |
| `a69e8681`, `6aca9919`, `10dc809b`, `232effd9` | Task 2 canonical document contracts and typed archive routes | Metadata `237/237`; governance `158/158`; taxonomy `5/5`; zero CLI findings and provider drift. |
| `0dd2579f`, `a6f602f5`, `068d6645`, `ce52501e` | Task 3 migration ledger and script manifest | Manifest/ledger `23/23`; taxonomy `5/5`; Task 2 fixtures `14/14`; metadata `237/237`; compilation and diff hygiene. |
| `4122cecf` | Task 4 requirements and architecture identity migration | Task 4 RED/GREEN evidence, metadata `237/237`, ledger/manifest `23/23`, governance contracts and provider projections recorded in the Task 4 report; alignment non-increase gate satisfied. |
| `8513d0d1` | Task 4 execution-evidence remediation | Scoped re-review APPROVED for `b827289f..8513d0d1`; original Important finding ADDRESSED, with no new Critical or Important finding. |
| `65e994f3` | Task 5 Stage 03/04 co-location and archive migration | RED/GREEN lifecycle evidence, metadata, promoted, alignment, taxonomy, manifest, provider, link, exact source-blob proof, and diff gates are recorded in the Task 5 report; third scoped re-review APPROVED. |

## Deferred and Blocked Items

| Item | Status | Deferral destination |
| :-- | :-- | :-- |
| Repository-wide alignment findings after Task 4 | Deferred | Later migration tasks: `181` predecessor active-to-archive links remained; no moved-path missing link remained. |
| Exploratory Task 4 `check-changed` deficits | Deferred | Later Tasks 5, 6D, and 11: `120` pre-existing unsupported Stage 04/05 and archive-profile deficits; bounded Task 4 target selection had zero violations. |
| Task 4 changed-metadata `path-id-mismatch` | Closed by Task 5 | The atomic move to `docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md` aligns `task-0136-01` with the owning stable capability path. |
| CI-only and controlled all-files pre-commit evidence for Tasks 1–4 | Unavailable / not run | No durable execution record was found; do not infer a pass from local validation. |
| Task 5 promoted residual `42` | Deferred outside Task 5 | Task 6 owns `28` Operations findings; the remaining `14` are existing Task 4 successor and Tasks 7, 13, and 14 target-surface/archive-transition work. The Task 5 regression asserts that none can be silently recategorized as Task 5. |
| Task 5 full lifecycle residual `43` | Deferred outside Task 5 | Plan Tasks 7, 10, and 14 own the archive identity/provenance, validator consolidation, transition-contract, and final full-suite surfaces. Task 5 closes with zero errors, focused lifecycle `11/11`, and historical-source regressions green. |

## Related Documents

- [Specification](spec.md)
- [Approved implementation plan](plan.md)
- [Task template](../../99.templates/templates/sdlc/task.template.md)
