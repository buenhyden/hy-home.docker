---
profile_id: task
status: active
artifact_id: task-0153-0012
artifact_type: task
parent_ids:
  - SPEC-0153
  - plan-0153
created: 2026-08-21
updated: 2026-08-28
---

# Task 0012: Gates

## Objective

Replace overlapping gates with the six public validation suites and remove duplicate wrappers and fixtures.

## Inputs

- [Specification](../spec.md)
- [Implementation Plan](../plan.md)
- [Migration 0003](../../../98.archive/migrations/0003-workspace-governance-simplification.md)
- Task 11 script/test structure, gate routing contracts, approved Migration owner_task 12 rows.

## Work Log

| Event | Actual result |
| :--- | :--- |
| RED | 125 focused tests exposed 3 failures and 2 errors for missing public profiles/explain, copied routes, obsolete adapter command, and retirement absence. |
| Public routing | Installed exact `changed`/`full` profiles over the six manifest-owned suites; workflow, pre-commit, local wrapper, and hooks now select only public profiles. |
| Retirement | Deleted six successor-backed owner-task-12 scripts after active-consumer rewrites; retained sample-service delivery rehearsal and restored provider-hook parity because no successor reproduces DATA-0072. |
| Snapshot retirement | Replaced the Spec 133 fixed SHA/dirty-tree equality with live suite ownership, impact, route, trackedness, and absence invariants. |
| Current consumers | Repointed the exact active Operations/infra consumers identified by Migration 0003; preserved historical and Task 13-owned surfaces. |
| Finalization | Made unstaged Task 12 deletions explicit to the Operations reader; replaced the manifest checker's oscillating static-path fixed point with a lexical-scope-aware monotone conflict state and regression; reconciled all 32 strict evidence rows to truthful current consumers/tests; supplied 61 Stage99-permitted Operations parents; repaired data-0061 in its generator and regenerated it; and closed all five Task 12-owned cross-link findings. |
| Review fix round | Joined explain and execution on one exact-once manifest plan; added fail-closed local/PR/push/manual execution contexts; repaired 43 infra runner links and their live checker; tightened lexical-scope evidence; restored the DATA-0072 generator/test; updated the documented two-job ruleset; and corrected the exact Task 4 forbidden path. |
| Review fix round 2 | Restored all 35 retained Task 11 validator identities and suite owners; separated and anchored automated execution-context eligibility; completed event-base-to-metadata-adapter dataflow; reduced machine required-quality jobs to the exact two workflow identities; and made the reviewer bounded metadata/Operations/version proof green after deletion. |
| Review fix round 3 | Reproduced the final base-plan context bypass as two RED failures; enforced admission on every final invocation, excluded local hardening, rejected manual/runtime/recursive rebindings, and admitted internal calls only by exact path/argv/context. |

## Verification Evidence

| Check | Command | Result |
| :--- | :--- | :--- |
| Focused Task 12 | `PYTHONPATH=. timeout 90s python3 -m unittest tests.validation.test_ci_gate_adapters tests.validation.test_ci_gate_contract tests.validation.test_ci_gate_runner tests.validation.test_github_workflow_contract tests.validation.test_target_surface_delta_contracts tests.validation.test_security_automation_readiness tests.validation.test_script_manifest -q` | PASS, 163 tests, zero failures/errors; 11 pre-existing Wave A skips; 35.326 seconds |
| Final-plan admission | `PYTHONPATH=. timeout 90s python3 -m unittest -q tests.validation.test_ci_gate_runner` | PASS, 27 tests; 155 forbidden rebind subcases, exact adapter positives/negatives, hidden-invocation rejection, and CLI executor-not-called proof; 6.869 seconds |
| Live target-surface tests | `PYTHONPATH=. python3 -m unittest tests.validation.test_target_surface_delta_contracts` | PASS, 19 tests |
| Operations taxonomy | `PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_operations_taxonomy` | PASS, 19 tests; no retired script is opened from the unstaged index |
| Manifest unit | `PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest` | PASS, 49 tests; conflicting reassignment, lexical-scope, and validator-producer freshness regressions included |
| Provider parity | `PYTHONPATH=. python3 -m unittest tests.validation.test_provider_hook_parity tests.validation.test_script_manifest` | PASS, 55 tests; DATA-0072 generator/test restored |
| Entrypoint smoke | `PYTHONPATH=. python3 -m unittest tests.validation.test_validator_entrypoints` | PASS, 3 tests; `run-ci-gate.py` is classified as Python |
| Manifest standalone | `/usr/bin/time -f 'elapsed=%e' timeout 60s python3 scripts/validation/check-script-manifest.py` | PASS; zero findings, elapsed 6.32 seconds on the final run (initial pre-fix run exited 124 with no output) |
| Explain changed | `python3 scripts/validation/run-ci-gate.py --profile changed --explain` | PASS; local context renders 23 canonical invocations exactly once without execution; all 35 retained validator owners remain registered |
| Explain full | `python3 scripts/validation/run-ci-gate.py --profile full --explain` | PASS; local final plan 44 = 23 explained validators + 21 exact internal calls, hardening 0; PR/push/initial-push/dispatch final counts 57/56/55/55 with 24 explained validators each |
| Workflow contract | `PYTHONPATH=. python3 scripts/validation/check-github-workflow-contract.py` | PASS; 7 workflows, 9 jobs, 8 actions |
| Live route contract | `python3 scripts/validation/check-target-surface-delta-contract.py --mode blocking` | PASS |
| LLM Wiki successor | `python3 scripts/knowledge/generate-llm-wiki.py --check` | PASS; both outputs fresh |
| Active retirement scan | `rg -n 'check-repo-contracts' .codex .claude scripts/hooks docs/00.agent-governance .github .pre-commit-config.yaml scripts/validation` | PASS; zero matches |
| Scoped metadata | `check-document-metadata.py --mode check-changed --base-ref 2b5fa6f7...` with 76 repeated `--changed-path` arguments | PASS; selected 76, violations 0, legacy exceptions 0, transition overrides 0; no branch-wide verdict used |
| Static syntax | Ruff/`py_compile` on 33 Python; YAML parse on 4 files; `bash -n` on 9 shell files | PASS |
| Reviewer bounded suite | `PYTHONPATH=. timeout 60s python3 -m unittest -q tests.lib.document_governance.test_operations_taxonomy tests.lib.document_governance.test_metadata_validator tests.validation.test_tech_stack_version_contract` | PASS, 60 tests, no skips/failures/errors; 10.375 seconds |
| Generated freshness | LLM Wiki, security readiness, tech-stack provenance, provider-hook parity | PASS |
| Cross-links/audit matrix | Both document-link modes; audit-matrix `--check` | Five Task 12 alignment findings fixed; 1 traceability and 26 alignment findings remain exclusively in untouched paths; audit matrix rejects old overview path |

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Task self-review | Done | Focused behavior and static checks pass; Task 12 manifest, metadata, and changed-link findings are zero; untouched cross-link, semantic-audit, and audit-matrix observations are recorded without weakening validators. |
| Fix round 1 | Superseded in part | H3/H4/H5/M2 remain verified; independent re-review reopened H1/H2/M1 and the bounded metadata/version proof. |
| Fix round 2 | Superseded in part | Immutable 35-validator ownership, metadata event bases, and exact two required jobs remain verified; independent re-review identified a final base-plan admission bypass. |
| Fix round 3 | Done | All final direct invocations are context-eligible canonical validators or exact admitted internal commands; local hardening is absent, manual/runtime/recursive rebindings fail before execution, and focused 163 plus reviewer 60 tests pass. |

## Commit Ledger

| Commit | Description |
| :--- | :--- |

## Rulings

- Do not regenerate the Spec 133 158-row predecessor-to-HEAD plus dirty-tree
  snapshot. Preserve it as historical Git/Migration evidence and validate live
  six-suite routing instead; this supersedes the old 20F/2E result.
- Retain `rehearse-sample-service-delivery.sh`; no successor exists and none may
  be invented.
- Retain `report-provider-hook-parity.sh` and its focused test; no other current
  generator reproduces DATA-0072.
- Preserve the 35 retained Task 11 validator identities and original suite
  owners. Automated execution eligibility is separate and cannot be changed by
  reclassifying a validator or mutating its anchored context policy.

## Deferred Items

- Audit-matrix freshness is blocked before comparison by its pre-existing fixed
  overview-path authority; Task 12 records but does not weaken or retarget it.
- Link validation exposes one traceability and 26 alignment findings solely in
  untouched paths. Semantic-audit fixtures retain the Task 9 Stage 90 path
  mismatch. Neither is promoted into or used to qualify the Task 12 verdict.
