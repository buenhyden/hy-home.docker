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
- No approval exists yet for the controlled all-files wrapper, push, remote
  merge, workflow dispatch, provider live call, or remote control-plane change.

Rollback is task-commit revert plus exact Git provenance for deleted historical
surfaces. No rollback command may discard unrelated user changes.

## Work Breakdown

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-AGCC-001 | Normalize active contracts and create retirement evidence | contract/data | AGCC-001–004 | Task 1 | duplicate/retirement tests, 14/22/3 contract pass | fresh rules implementer | important_remediation_complete_re_review_pending |
| T-AGCC-002 | Update model facts, profiles, renderer, and projections | provider/code | AGCC-005–006, 011 | Task 2 | model/profile tests, native schema, drift 0 | fresh provider implementer | not_started |
| T-AGCC-003 | Establish shared bounded project memory | governance/docs | AGCC-001–002, 007 | Task 3 | import parity, bounds, secret/stale checks | fresh memory implementer | not_started |
| T-AGCC-004 | Add functions and type harness, loop, and evals | harness/code | AGCC-008–010 | Task 4 | 14/24, 8 layers/states, 11/16 evals | fresh harness implementer | not_started |
| T-AGCC-005 | Reconcile local Actions/QA and remote observation | CI/security | AGCC-012–014 | Task 5 | 16 jobs, zizmor pin, remote inventory | fresh CI implementer | not_started |
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
| 2026-07-26 | T-AGCC-001 specification review remediation | Independent specification reviewer / Fresh rules implementer | Specification review of `164f2dc5` returned C0/I1/M1. The Important finding showed that the ledger accepted active but unapproved replacements and other syntactically valid fact drift. RED produced 12 expected missing-finding subtest failures. Remediation now binds every approved non-provenance fact for all five records and returns one deterministic value-free fact-mismatch code; focused offline GREEN passed 5/5, dependency-locked aggregates passed 144/144 contract and 22/22 native tests, and the contract checker passed with 0 failures. The remediation remains uncommitted and re-review pending; the exact remediation commit, Minor disposition, and reviewer-final fields remain controller-owned. |

Implementation rows are appended only after the responsible agent finishes a
logical unit. Review rows identify the exact reviewed commit range and finding
disposition.

## Verification Evidence

| Task | RED evidence | GREEN evidence | Aggregate evidence | State |
| --- | --- | --- | --- | --- |
| T-AGCC-001 | Initial focused 4 methods → expected `FAILED (failures=4, errors=1)` before implementation; duplicate-key assertion independently passed. Review remediation: offline `RetirementLedgerTests.test_retirement_ledger_rejects_exact_fact_mutations_without_values` → expected `FAILED (failures=12)` before exact-fact binding. | Initial focused 4 methods → `OK`. Offline remediation mutation test → 1 method/12 mutation cases `OK`; offline focused Task 1 set including the mutation test → 5/5 `OK`. | Current dependency-locked aggregates → 144/144 contract and 22/22 native `OK`. Current remediation checker → `PASS contracts=3 agents=14 functions=22 providers=3 failures=0`; `git diff --check` passed. Exact remediation commit and final reviewer verdict pending. | important_remediation_complete_re_review_pending |
| T-AGCC-002 | not_run | not_run | not_run | not_started |
| T-AGCC-003 | not_run | not_run | not_run | not_started |
| T-AGCC-004 | not_run | not_run | not_run | not_started |
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
| T-AGCC-001 | not_assigned | not_assigned | not_assigned | not_available | not_reviewed | not_reviewed |
| T-AGCC-002 | not_assigned | not_assigned | not_assigned | not_available | not_reviewed | not_reviewed |
| T-AGCC-003 | not_assigned | not_assigned | not_assigned | not_available | not_reviewed | not_reviewed |
| T-AGCC-004 | not_assigned | not_assigned | not_assigned | not_available | not_reviewed | not_reviewed |
| T-AGCC-005 | not_assigned | not_assigned | not_assigned | not_available | not_reviewed | not_reviewed |
| T-AGCC-006 | not_assigned | not_assigned | not_assigned | not_available | not_reviewed | not_reviewed |
| Whole branch | not_applicable | not_assigned | not_assigned | `e65bb18f..HEAD` | not_reviewed | not_reviewed |

## Commit Ledger

| Task | Logical unit | Expected commit | Actual commit | Validation |
| --- | --- | --- | --- | --- |
| T-AGCC-001 | active contract/retirement normalization | `refactor(governance): normalize active agent contracts` | not_committed | not_run |
| T-AGCC-002 | model policy and provider projections | `feat(providers): update model policy and projections` | not_committed | not_run |
| T-AGCC-003 | shared project memory | `feat(governance): establish shared project memory` | not_committed | not_run |
| T-AGCC-004 | functions, harness, loop, evals | `feat(harness): converge agent functions and loops` | not_committed | not_run |
| T-AGCC-005 | local CI/QA and remote observation | `ci(governance): reconcile agent quality controls` | not_committed | not_run |
| T-AGCC-006 | canonical evidence and closure | `docs(governance): close canonical convergence evidence` | not_committed | not_run |

Review remediation and lifecycle closure commits are added as separate rows
when required.

## Deletion and Consolidation Ledger

| Path | Decision | Consumer scan | Canonical replacement | Provenance | Rollback | Review |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/00.agent-governance/contracts/agent-catalog.yaml#role_transfers` | removed from the active contract; historical role transitions retained only as evidence | active-contract scan found no `role_transfers:` or `status: retired`; focused catalog and ledger tests passed | `docs/90.references/data/governance/agent-governance-retirement-ledger.yaml` records `style-enforcer` → roles `qa-engineer`, `rules-engineer` plus function `style-validation`, and `wiki-curator` → role `doc-writer` plus function `knowledge-map-agent` | commit `e65bb18fa2f6e3fb6235725750c7c57cbe0227ee`, path `docs/00.agent-governance/contracts/agent-catalog.yaml`, blob `9f6a0fba4df6d37ab5f1a3390dc57d0dd99e8034` | `git restore --source=e65bb18fa2f6e3fb6235725750c7c57cbe0227ee -- docs/00.agent-governance/contracts/agent-catalog.yaml` | pending |
| `docs/00.agent-governance/contracts/provider-models.yaml#deprecated-models-and-fallback-approvals` | removed the three historical model rows and their fallback approvals from the active contract | active-contract scan found no deprecated lifecycle or retired model IDs; focused provider and ledger tests passed | retirement ledger records `claude-opus-4-1-20250805` → `claude-opus-4-8`, `gpt-5.2-codex` → `gpt-5.6-terra`, and `gemini-3.1-flash-lite-preview` → `gemini-3.1-flash-lite` | commit `e65bb18fa2f6e3fb6235725750c7c57cbe0227ee`, path `docs/00.agent-governance/contracts/provider-models.yaml`, blob `58ee9b29cb0e519a34ff919e1e29791171c458a4` | `git restore --source=e65bb18fa2f6e3fb6235725750c7c57cbe0227ee -- docs/00.agent-governance/contracts/provider-models.yaml` | pending |
| `docs/00.agent-governance/memory/github-ci-contract-audit.md` | planned_remove in T-AGCC-005 | pending | Stage 00 GitHub policy plus Stage 90 remote observation | commit `e65bb18f`, blob `7bf6427ad8f29ab8b0d7c001cf330e29b941cdfe` | `git restore --source=e65bb18f -- docs/00.agent-governance/memory/github-ci-contract-audit.md` | pending |
| renderer-managed stale projections | remove_only_if_reported_and_confined | pending renderer report | current renderer projection | record exact path/blob before deletion | restore from task parent commit | pending |
| all other target files | preserve unless exact Plan deletion gate is met | pending final scan | not_applicable | Git history | task commit revert | pending |

## Deferred and Blocked Items

| Item | State | Reason | Destination |
| --- | --- | --- | --- |
| Provider live acceptance, entitlement, quality/cost/latency comparison | deferred | requires separate runtime, privacy, cost, and external-action approval | future provider-evaluation spec |
| Remote ruleset, protection, required-check, environment, secret, and variable verification | unverified | GitHub authentication unavailable; remote is read-only | Stage 90 observation plus future approved GitHub task |
| Runtime, Compose, infrastructure, deployment, and release changes | deferred | explicitly outside Spec 134 | existing runtime readiness specs |
| Dependency-locked baseline validator/renderer | environment_blocked | missing `html5lib`; restricted package resolution | rerun with `uv --with-requirements scripts/requirements.txt` when available |
| Controlled all-files wrapper | not_approved_for_run | requires separate exact user approval and clean committed candidate | T-AGCC-006 |
| Push/remote merge/remote branch cleanup | not_approved | requires separate finish action approval | finishing-a-development-branch handoff |

## Related Documents

- [Spec 134](../../03.specs/134-agent-governance-canonical-convergence/spec.md)
- [Implementation Plan](../plans/2026-07-26-agent-governance-canonical-convergence.md)
- [Agent governance](../../00.agent-governance/README.md)
- [Canonical research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Canonical audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
